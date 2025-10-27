"""Command line interface for evaluating Nerd Court cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .evaluator import NerdCourt
from .exceptions import CaseValidationError, NerdCourtError
from .models import Argument, Case


def build_parser() -> argparse.ArgumentParser:
    """Create an :class:`argparse.ArgumentParser` configured for the CLI."""

    parser = argparse.ArgumentParser(
        description="Evaluate a Nerd Court case defined in JSON format.",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to a JSON file containing the case definition.",
    )
    parser.add_argument(
        "--bias",
        type=float,
        default=0.0,
        help="Optional bias applied to the prosecution (positive) or defense (negative).",
    )
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Entrypoint used by ``python -m nerdcourt.cli`` and tests.

    Returning an integer instead of calling :func:`sys.exit` directly improves
    testability and allows embedding the CLI in other scripts with minimal
    friction.
    """

    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        case = _load_case(args.path)
        court = NerdCourt(bias=args.bias)
        verdict = court.evaluate_case(case)
    except FileNotFoundError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover - parser.error already exits in real usage.
    except (CaseValidationError, NerdCourtError, json.JSONDecodeError) as exc:
        parser.exit(status=2, message=f"error: {exc}\n")
    else:
        print(json.dumps(verdict.as_dict(), indent=2))
        return 0


def _load_case(path: Path) -> Case:
    """Load a :class:`Case` from a JSON file."""

    data = json.loads(path.read_text(encoding="utf8"))
    try:
        prosecution = [_argument_from_dict(item) for item in data["prosecution"]]
        defense = [_argument_from_dict(item) for item in data["defense"]]
    except KeyError as exc:  # pragma: no cover - triggered by user input.
        raise CaseValidationError(f"Missing required key: {exc.args[0]}") from exc

    case = Case(
        title=data.get("title", "Untitled case"),
        summary=data.get("summary", "No summary provided."),
        prosecution=prosecution,
        defense=defense,
        metadata=data.get("metadata", {}),
    )
    case.validate()
    return case


def _argument_from_dict(payload: dict[str, object]) -> Argument:
    """Construct an :class:`Argument` from a plain dictionary."""

    try:
        claim = str(payload["claim"])  # type: ignore[index]
        weight = float(payload["weight"])  # type: ignore[index]
        strength = float(payload["strength"])  # type: ignore[index]
    except KeyError as exc:  # pragma: no cover - triggered by user input.
        raise CaseValidationError(f"Argument is missing '{exc.args[0]}'") from exc
    tags_raw = payload.get("tags", ())
    if isinstance(tags_raw, str):
        tags = (tags_raw,)
    else:
        tags = tuple(str(tag) for tag in tags_raw)
    return Argument(claim=claim, weight=weight, strength=strength, tags=tags)


if __name__ == "__main__":  # pragma: no cover - manual execution helper.
    raise SystemExit(run())
