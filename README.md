# Vega Sentinel

[![Release](https://img.shields.io/github/v/release/Vega-Starboard/vega-sentinel?label=release)](https://github.com/Vega-Starboard/vega-sentinel/releases/tag/v0.1.0)
[![CI](https://github.com/Vega-Starboard/vega-sentinel/actions/workflows/ci.yml/badge.svg)](https://github.com/Vega-Starboard/vega-sentinel/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**Authorized web audit engine for public-facing technical signals.**

Vega Sentinel performs bounded, non-invasive inspection of public web surfaces. It checks security headers, SEO metadata, mobile readiness, social tags, trust signals, robots/sitemap presence, and TLS certificate metadata - without fuzzing, crawling, or exploitation.

## Why Vega Sentinel?

Security and compliance reviews often start with basic surface checks that don't require penetration testing tools. Vega Sentinel fills the gap between manual browser inspection and full vulnerability scanners by providing:

- Repeatable, scriptable public-signal audits
- Clear ethical boundaries documented in every report
- Safe-mode controls that limit request scope
- Structured output for integration with review workflows

## Legal & Ethical Boundaries

**Use Vega Sentinel only on websites you own or are explicitly authorized to assess.**

This tool is designed for authorized security review, internal compliance checking, and educational purposes. Unauthorized scanning of third-party websites may violate computer access laws in your jurisdiction.

### What Vega Sentinel Does

- Fetches a single page plus `robots.txt` and `sitemap.xml` (safe mode)
- Inspects response headers for security best practices
- Parses rendered HTML for SEO and metadata signals
- Checks TLS certificate availability and basic metadata
- Documents its own boundaries in every report

### What Vega Sentinel Does NOT Do

- - Crawl or spider multiple pages
- - Fuzz parameters or inject payloads
- - Attempt authentication bypass
- - Brute force directories or endpoints
- - Exploit vulnerabilities
- - Make vulnerability claims without evidence
- - Access cookies, localStorage, or session data
- - Perform high-volume or concurrent requests

## Features

- **Security header audit** - checks CSP, HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy
- **SEO inspection** - extracts title, meta description, H1 count
- **Mobile readiness** - checks viewport meta tag presence
- **Social metadata** - detects Open Graph and Twitter Card tags
- **Trust signals** - identifies contact, about, privacy, security, and terms links
- **Robots/sitemap check** - verifies `robots.txt` and `sitemap.xml` availability (safe mode)
- **TLS inspection** - validates HTTPS and captures certificate metadata
- **Markdown reports** - human-readable output with boundary documentation
- **JSON export** - machine-readable reports for pipeline integration
- **Safe mode** - limits requests to single page + standard discovery files

## Install

```bash
git clone https://github.com/Vega-Starboard/vega-sentinel.git
cd vega-sentinel
python3 -m pip install --user -e .
```

Requires Python 3.10+. No external dependencies beyond the standard library.

## Quickstart

```bash
# Basic audit with Markdown report
PYTHONPATH=src python3 -m vega_sentinel audit https://example.com --out reports/example.md

# Audit with JSON export and safe mode enabled
PYTHONPATH=src python3 -m vega_sentinel audit https://example.com --json reports/example.json --safe-mode

# Print report to stdout (no file output)
PYTHONPATH=src python3 -m vega_sentinel audit https://example.com
```

## Commands

### `audit`

Perform a single-URL public signal audit.

```bash
vega-sentinel audit <url> [--out PATH] [--json PATH] [--safe-mode]
```

| Option | Description |
|--------|-------------|
| `url` | Target URL (must include `http://` or `https://`) |
| `--out` | Write Markdown report to specified path |
| `--json` | Write JSON report to specified path |
| `--safe-mode` | Enable robots.txt and sitemap.xml checks (default: enabled) |

## Outputs & Artifacts

### Markdown Report (`--out`)

```markdown
# Vega Sentinel Report: https://example.com

- Status: 200
- Response time: 342 ms
- Title: Example Domain
- Meta description: (missing)
- H1 count: 1
- Viewport: (missing)
- Missing security headers: content-security-policy, strict-transport-security
- Robots status: 200
- Sitemap status: 404
- TLS: {"available": true, "pem_bytes": 1234, "host": "example.com"}

## Boundaries

- single URL
- robots.txt
- sitemap.xml
- no crawling
- no fuzzing
- no exploitation
```

### JSON Report (`--json`)

Structured report with all audit fields including security headers, SEO metadata, mobile/social signals, trust links, robots/sitemap status, TLS info, and boundary documentation.

## Security Headers Checked

| Header | Purpose |
|--------|---------|
| `content-security-policy` | Prevents XSS and data injection |
| `strict-transport-security` | Enforces HTTPS connections |
| `x-frame-options` | Prevents clickjacking |
| `referrer-policy` | Controls referrer information leakage |
| `permissions-policy` | Restricts browser feature access |

## Privacy & Safety

- **Local execution** - all processing happens on your machine
- **No telemetry** - zero data leaves your environment
- **No account required** - no registration or API keys
- **Conservative requests** - maximum 3 HTTP requests per audit (page, robots.txt, sitemap.xml)
- **User-Agent identification** - requests identify as `VegaSentinel/0.1 authorized-audit`
- **Boundary documentation** - every report explicitly states what was and wasn't checked

## Project Status

**MVP - v0.1.0 released.** Single-URL audit with Markdown and JSON export. Conservative request behavior with safe-mode controls.

### Known Limitations

- Single URL only - no multi-page or site-wide auditing
- No JavaScript-rendered content inspection (static HTML parsing only)
- TLS inspection is certificate metadata only (no chain validation or cipher suite checking)
- No screenshot capture

## Roadmap

- [ ] Optional Playwright integration for JavaScript-rendered page inspection
- [ ] Richer TLS chain inspection with cipher suite reporting
- [ ] Configurable report templates
- [ ] Multi-URL batch auditing
- [ ] Cookie and privacy header analysis

## Development

```bash
git clone https://github.com/Vega-Starboard/vega-sentinel.git
cd vega-sentinel
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Running Tests

```bash
python3 scripts/verify.py
```

### Project Structure

```
vega-sentinel/
+-- src/vega_sentinel/
|   +-- __init__.py
|   +-- __main__.py
|   `-- cli.py
+-- examples/
|   `-- reports/
|       `-- example.md
+-- docs/
|   `-- ethics-and-scope.md
+-- pyproject.toml
`-- README.md
```

## Repository Topics

`security-audit` `web-security` `headers-check` `tls` `seo` `compliance` `authorized-testing` `local-first` `cli-tool` `python`

## Support & Security

- **Issues:** [GitHub Issues](https://github.com/Vega-Starboard/vega-sentinel/issues)
- **License:** MIT - see [LICENSE](LICENSE)
- **Responsible disclosure:** If you discover a bug that could cause unintended request behavior, please report it via GitHub Issues with `[security]` in the title. Do not test against systems you do not own.
- **Legal notice:** You are responsible for ensuring you have authorization before auditing any target. See [`docs/ethics-and-scope.md`](docs/ethics-and-scope.md).

---
