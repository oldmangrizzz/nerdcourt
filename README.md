# Nerd Court

Nerd Court is a playful toolkit for staging debates between the canonical text of a story and the interpretations that fans love. It is intentionally tongue-in-cheek and exists solely for transformative, satirical fun.

## Features

- **Structured case management** – define the prosecution (canon) and defense (fanon) arguments with clear scoring metadata.
- **Deterministic yet interpretable verdicts** – the `NerdCourt` evaluator explains how each side scored so that results are reproducible and debuggable.
- **Thoughtful error handling** – validation catches common mistakes early and provides actionable feedback.
- **Comment-rich code** – the modules are heavily documented so new contributors can jump in quickly.
- **Pytest-based test-suite** – ensures behaviour stays consistent as new rulings are added.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
pytest
```

## Command line interface

You can evaluate a case described in JSON using the built-in CLI:

```bash
python -m nerdcourt.cli sample_case.json
```

The CLI prints the verdict and returns a non-zero exit code when validation fails so that it can be scripted easily.

## License

MIT – see the header comments for details.
