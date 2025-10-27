"""CLI integration tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from nerdcourt.cli import run


def _write_case(path: Path) -> None:
    payload = {
        "title": "Showdown",
        "summary": "Who is right?",
        "prosecution": [
            {"claim": "Original text says so", "weight": 0.6, "strength": 0.8}
        ],
        "defense": [
            {"claim": "Author interview implies otherwise", "weight": 0.4, "strength": 0.7}
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf8")


def test_cli_success(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    case_path = tmp_path / "case.json"
    _write_case(case_path)
    exit_code = run([str(case_path)])
    assert exit_code == 0
    output = json.loads(capsys.readouterr().out)
    assert output["winner"] in {"prosecution", "defense", "split"}


def test_cli_handles_validation_errors(tmp_path: Path) -> None:
    case_path = tmp_path / "case.json"
    case_path.write_text("{}", encoding="utf8")

    # The CLI calls parser.exit which raises SystemExit.  Pytest treats this as
    # an exception so we can assert the exit code.
    with pytest.raises(SystemExit) as excinfo:
        run([str(case_path)])
    assert excinfo.value.code == 2
