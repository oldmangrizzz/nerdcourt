"""Tests for the nerdcourt.models module."""

from __future__ import annotations

import pytest

from nerdcourt import Argument, Case, CaseValidationError


def _valid_argument(**overrides):
    base = {
        "claim": "Canon is internally consistent",
        "weight": 0.5,
        "strength": 0.8,
        "tags": ("canon",),
    }
    base.update(overrides)
    return Argument(**base)


def test_argument_validation_rejects_blank_claim() -> None:
    with pytest.raises(CaseValidationError):
        _valid_argument(claim="   ")


def test_argument_validation_rejects_out_of_range_weight() -> None:
    with pytest.raises(CaseValidationError):
        _valid_argument(weight=2)


def test_case_requires_arguments_per_side() -> None:
    case = Case(
        title="Fanon vs Canon",
        summary="A light-hearted dispute",
        prosecution=[_valid_argument()],
        defense=[],
    )
    with pytest.raises(CaseValidationError):
        case.validate()


def test_case_to_dict_round_trip() -> None:
    case = Case(
        title="Battle of Endings",
        summary="Debating the alternate ending",
        prosecution=[_valid_argument()],
        defense=[_valid_argument(claim="Fanon ending is more satisfying")],
        metadata={"fandom": "Space Opera"},
    )
    case.validate()
    exported = case.to_dict()
    assert exported["title"] == case.title
    assert exported["metadata"]["fandom"] == "Space Opera"
