# Contributing

## Development Setup

```bash
python3 -m pip install --user -e .
python3 scripts/verify.py
```

## Pull Requests

- Keep changes focused.
- Update docs when behavior changes.
- Add or update examples when a command shape changes.
- Run `python3 scripts/verify.py` before opening a pull request.

## Boundaries

Do not add exploitation, fuzzing, login bypass, brute force, or high-volume crawling. Vega Sentinel is for authorized, conservative public-signal review.
