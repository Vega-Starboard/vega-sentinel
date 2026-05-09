# Vega Sentinel

[![Release](https://img.shields.io/github/v/release/Vega-Starboard/vega-sentinel?label=release)](https://github.com/Vega-Starboard/vega-sentinel/releases/tag/v0.1.0)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Vega Sentinel is an authorized web audit engine for public-facing technical signals. It checks headers, metadata, robots and sitemap presence, mobile readiness, social metadata, trust signals, and TLS metadata without fuzzing or invasive scanning.

## Safety

Use only on sites you own or are authorized to assess. The MVP fetches one page plus `robots.txt` and `sitemap.xml`; it does not crawl, exploit, brute force, bypass login, or make vulnerability claims without evidence.

## Usage

```bash
PYTHONPATH=src python3 -m vega_sentinel audit https://example.com --out reports/example.md
PYTHONPATH=src python3 -m vega_sentinel audit https://example.com --json reports/example.json --safe-mode
```

## Status

MVP. `v0.1.0` is released. Single-URL audit, Markdown export, JSON export, conservative request behavior.

## Roadmap

- Optional Playwright screenshots
- Richer TLS chain inspection
- Configurable report templates
