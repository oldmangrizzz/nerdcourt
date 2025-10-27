"""Core evaluation logic for Nerd Court."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import pstdev
from typing import Sequence

from .exceptions import ArgumentScoreError, CaseValidationError
from .models import Argument, Case, Verdict


@dataclass(slots=True)
class ScoreBreakdown:
    """Detailed scoring information for a single side of the case."""

    weighted_strength: float
    total_weight: float
    dispersion: float

    @property
    def average(self) -> float:
        """Return the mean strength, guarding against division by zero."""

        if self.total_weight <= 0:
            raise ArgumentScoreError("Cannot compute average with zero total weight.")
        return self.weighted_strength / self.total_weight


class NerdCourt:
    """Evaluate cases by comparing canonical and fanon arguments.

    Parameters
    ----------
    bias:
        Optional constant that favours the prosecution (positive values) or the
        defense (negative values).  This simulates the predisposition of a
        particular judging panel.
    confidence_floor:
        Minimum confidence returned by :meth:`evaluate_case`.  A non-zero value
        prevents the CLI from reporting totally indecisive verdicts.
    """

    def __init__(self, *, bias: float = 0.0, confidence_floor: float = 0.15) -> None:
        self.bias = bias
        self.confidence_floor = confidence_floor

    def evaluate_case(self, case: Case) -> Verdict:
        """Run the specified :class:`Case` through the scoring algorithm."""

        case.validate()
        prosecution_breakdown = self._score_side(case.prosecution)
        defense_breakdown = self._score_side(case.defense)

        # Apply the optional bias after computing the raw scores.  This keeps the
        # reasoning transparent: the bias is a flat adjustment instead of being
        # buried inside the scoring formulas.
        prosecution_score = prosecution_breakdown.average + max(self.bias, 0)
        defense_score = defense_breakdown.average + max(-self.bias, 0)

        winner, notes = self._determine_winner(
            prosecution_score=prosecution_score,
            defense_score=defense_score,
            case=case,
            prosecution_breakdown=prosecution_breakdown,
            defense_breakdown=defense_breakdown,
        )
        confidence = self._confidence(prosecution_score, defense_score)
        return Verdict(
            winner=winner,
            prosecution_score=prosecution_score,
            defense_score=defense_score,
            confidence=confidence,
            notes=notes,
        )

    def _score_side(self, arguments: Sequence[Argument]) -> ScoreBreakdown:
        """Calculate the weighted average strength for a list of arguments."""

        if not arguments:
            raise CaseValidationError("Cannot score an empty side of a case.")
        weights = [argument.weight for argument in arguments]
        total_weight = sum(weights)
        if total_weight <= 0:
            raise ArgumentScoreError("Total weight must be positive.")
        weighted_strength = sum(argument.weight * argument.strength for argument in arguments)
        # Dispersion communicates how contentious the side's evidence is.  We use
        # population standard deviation to avoid divide-by-zero issues when there
        # is only a single argument.
        dispersion = pstdev([argument.strength for argument in arguments]) if len(arguments) > 1 else 0.0
        return ScoreBreakdown(
            weighted_strength=weighted_strength,
            total_weight=total_weight,
            dispersion=dispersion,
        )

    def _determine_winner(
        self,
        *,
        prosecution_score: float,
        defense_score: float,
        case: Case,
        prosecution_breakdown: ScoreBreakdown,
        defense_breakdown: ScoreBreakdown,
    ) -> tuple[str, str]:
        """Return the winner and a human readable explanation string."""

        margin = prosecution_score - defense_score
        if abs(margin) < 0.05:
            # Too close to call – return a split verdict.
            winner = "split"
        elif margin > 0:
            winner = "prosecution"
        else:
            winner = "defense"

        notes = (
            "Case '{title}' resolved with a margin of {margin:.3f}."
            " Prosecution avg: {pros:.3f} (dispersion {pros_disp:.3f});"
            " Defense avg: {defn:.3f} (dispersion {def_disp:.3f})."
        ).format(
            title=case.title,
            margin=margin,
            pros=prosecution_breakdown.average,
            pros_disp=prosecution_breakdown.dispersion,
            defn=defense_breakdown.average,
            def_disp=defense_breakdown.dispersion,
        )
        return winner, notes

    def _confidence(self, prosecution_score: float, defense_score: float) -> float:
        """Translate score difference into a confidence value between 0 and 1."""

        # Confidence is basically the scaled absolute margin, but clamped so it
        # remains a proper probability-like value.  The ``confidence_floor``
        # ensures that even very tight margins communicate some level of
        # certainty about the result.
        margin = abs(prosecution_score - defense_score)
        scaled = min(1.0, margin * 1.5)
        return max(self.confidence_floor, round(scaled, 4))


__all__ = ["NerdCourt", "ScoreBreakdown"]
