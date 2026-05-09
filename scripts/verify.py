#!/usr/bin/env python3
from __future__ import annotations

import os
import py_compile
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "vega_sentinel"
COMMANDS = [['audit', 'https://example.com', '--out', '/tmp/vega-sentinel-example.md', '--json', '/tmp/vega-sentinel-example.json']]
REQUIRED_FILES = ['README.md', 'LICENSE', 'SECURITY.md', 'PRIVACY.md', 'docs/ethics-and-scope.md', 'src/vega_sentinel/cli.py']


def fail(message: str) -> None:
    print(f"verify: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")
    for path in (ROOT / "src" / PACKAGE).glob("*.py"):
        py_compile.compile(str(path), doraise=True)
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    for args in COMMANDS:
        result = subprocess.run(
            [sys.executable, "-m", PACKAGE, *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail("command failed: " + " ".join(args) + "\n" + result.stderr)
    print("verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
