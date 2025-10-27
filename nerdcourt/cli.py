"""Command line interface for the Nerd Court simulator."""

from __future__ import annotations

import argparse
import random
from textwrap import dedent

from .trial import TrialEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Spin up a Nerd Court trial transcript.")
    parser.add_argument(
        "case",
        nargs="?",
        help="Case caption in the format 'Plaintiff v. Defendant'. If omitted you will be prompted interactively.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed to make the transcript deterministic.",
    )
    return parser


def main(args: list[str] | None = None) -> int:
    parser = build_parser()
    namespace = parser.parse_args(args)

    rng_seed = namespace.seed
    engine = TrialEngine(rng=None if rng_seed is None else random.Random(rng_seed))

    case_caption = namespace.case
    if not case_caption:
        intro = dedent(
            """
            Welcome to Nerd Court! This satirical simulator lets you put any storyline on trial.
            Enter the two opposing forces you want to litigate (for example: "Skywalker Legacy v. Princess Palpatine").
            Press Ctrl+C or submit an empty line to exit.
            """
        ).strip()
        print(intro)
        try:
            case_caption = input("\nWho stands accused today? ")
        except KeyboardInterrupt:
            print("\nNerd Court adjourned.")
            return 0

    if not case_caption:
        print("No case submitted. Nerd Court adjourned without prejudice.")
        return 0

    transcript = engine.run_trial(case_caption)
    print(transcript)
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())
