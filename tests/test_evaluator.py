"""Tests for the NerdCourt evaluator."""

from __future__ import annotations

import pytest

from nerdcourt import Argument, Case, CaseValidationError, NerdCourt


@pytest.fixture()
def simple_case() -> Case:
    return Case(
        title="Canon vs Fanon",
        summary="Classic dispute",
        prosecution=[Argument(claim="Canon line", weight=0.6, strength=0.7)],
        defense=[Argument(claim="Fanon twist", weight=0.4, strength=0.9)],
    )


def test_evaluate_case_returns_verdict(simple_case: Case) -> None:
    court = NerdCourt()
    verdict = court.evaluate_case(simple_case)
    assert verdict.winner in {"prosecution", "defense", "split"}
    assert 0.0 <= verdict.confidence <= 1.0


def test_bias_parameter_shifts_scores(simple_case: Case) -> None:
    unbiased = NerdCourt().evaluate_case(simple_case)
    prosecution_tilt = NerdCourt(bias=0.1).evaluate_case(simple_case)
    assert prosecution_tilt.prosecution_score >= unbiased.prosecution_score


def test_empty_side_raises(simple_case: Case) -> None:
    bad_case = Case(
        title=simple_case.title,
        summary=simple_case.summary,
        prosecution=simple_case.prosecution,
        defense=[],
    )
    court = NerdCourt()
    with pytest.raises(CaseValidationError):
        court.evaluate_case(bad_case)
