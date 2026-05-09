from __future__ import annotations

import argparse
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SECURITY_HEADERS = ["content-security-policy", "strict-transport-security", "x-frame-options", "referrer-policy", "permissions-policy"]

class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.h1 = []
        self.meta = {}
        self.links = []
        self._in_title = False
        self._in_h1 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.lower(): value or "" for key, value in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag == "meta":
            key = (data.get("name") or data.get("property") or "").lower()
            if key:
                self.meta[key] = data.get("content", "")
        elif tag == "a" and data.get("href"):
            self.links.append(data["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text:
            return
        if self._in_title:
            self.title += text
        elif self._in_h1:
            self.h1.append(text)

def fetch(url: str, timeout: int = 10) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "VegaSentinel/0.1 authorized-audit"})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(500_000)
            return {"ok": True, "status": response.status, "headers": dict(response.headers), "body": body.decode("utf-8", errors="replace"), "elapsed_ms": round((time.perf_counter() - started) * 1000)}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "headers": dict(exc.headers), "body": "", "elapsed_ms": round((time.perf_counter() - started) * 1000), "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "status": 0, "headers": {}, "body": "", "elapsed_ms": round((time.perf_counter() - started) * 1000), "error": str(exc)}

def tls_summary(url: str) -> dict:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return {"available": False, "reason": "not an https URL"}
    try:
        cert = ssl.get_server_certificate((parsed.hostname, parsed.port or 443), timeout=5)
        return {"available": True, "pem_bytes": len(cert), "host": parsed.hostname}
    except Exception as exc:
        return {"available": False, "reason": str(exc)}

def audit(url: str, safe_mode: bool) -> dict:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SystemExit("URL must include http:// or https:// and a host")
    base = f"{parsed.scheme}://{parsed.netloc}"
    page = fetch(url)
    parser = MetadataParser()
    parser.feed(page.get("body", ""))
    headers = {key.lower(): value for key, value in page.get("headers", {}).items()}
    robots = fetch(base + "/robots.txt") if safe_mode else {"ok": False, "status": 0}
    sitemap = fetch(base + "/sitemap.xml") if safe_mode else {"ok": False, "status": 0}
    trust = [link for link in parser.links if re.search(r"contact|about|privacy|security|terms", link, re.I)]
    return {
        "target": url,
        "status": page["status"],
        "elapsed_ms": page["elapsed_ms"],
        "security_headers": {name: headers.get(name, "") for name in SECURITY_HEADERS},
        "seo": {"title": parser.title, "description": parser.meta.get("description", ""), "h1_count": len(parser.h1)},
        "mobile": {"viewport": parser.meta.get("viewport", "")},
        "social": {"og:title": parser.meta.get("og:title", ""), "twitter:card": parser.meta.get("twitter:card", "")},
        "trust_signals": trust[:10],
        "robots": {"checked": safe_mode, "status": robots.get("status", 0)},
        "sitemap": {"checked": safe_mode, "status": sitemap.get("status", 0)},
        "tls": tls_summary(url),
        "boundaries": ["single URL", "robots.txt", "sitemap.xml", "no crawling", "no fuzzing", "no exploitation"],
    }

def markdown(report: dict) -> str:
    missing_headers = [key for key, value in report["security_headers"].items() if not value]
    return "\n".join([
        f"# Vega Sentinel Report: {report['target']}",
        "",
        f"- Status: {report['status']}",
        f"- Response time: {report['elapsed_ms']} ms",
        f"- Title: {report['seo']['title'] or '(missing)'}",
        f"- Meta description: {report['seo']['description'] or '(missing)'}",
        f"- H1 count: {report['seo']['h1_count']}",
        f"- Viewport: {report['mobile']['viewport'] or '(missing)'}",
        f"- Missing security headers: {', '.join(missing_headers) if missing_headers else 'none'}",
        f"- Robots status: {report['robots']['status']}",
        f"- Sitemap status: {report['sitemap']['status']}",
        f"- TLS: {json.dumps(report['tls'])}",
        "",
        "## Boundaries",
        "",
        "\n".join(f"- {item}" for item in report["boundaries"]),
    ]) + "\n"

def main() -> int:
    parser = argparse.ArgumentParser(description="Authorized single-domain public signal audit.")
    sub = parser.add_subparsers(dest="command", required=True)
    audit_cmd = sub.add_parser("audit")
    audit_cmd.add_argument("url")
    audit_cmd.add_argument("--out", type=Path)
    audit_cmd.add_argument("--json", dest="json_out", type=Path)
    audit_cmd.add_argument("--safe-mode", action="store_true", default=True)
    args = parser.parse_args()
    report = audit(args.url, args.safe_mode)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(markdown(report), encoding="utf-8")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if not args.out and not args.json_out:
        print(markdown(report))
    return 0
