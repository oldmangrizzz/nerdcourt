# nerdcourt
nerd Court is where the story versus the Cannon go on trial. Rightly or wrongly editors will sometimes destroy a good story or character for their own reasons this is where those disputes get settled. (meant 100% as satire for under transformative works only)

## Getting Started

The repository now includes a small Python application that spins up a satirical Nerd Court transcript. Install dependencies (only the standard library is required) and run the CLI:

```bash
python -m nerdcourt.cli "Skywalker Legacy v. Princess Palpatine"
```

If you omit the case caption the program will prompt you for one interactively. Add `--seed <number>` to reproduce the exact same trial transcript.

### Tests

Unit tests are powered by `pytest`. Install it if necessary and execute:

```bash
pytest
```
