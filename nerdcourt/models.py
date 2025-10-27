"""Data models for Nerd Court.

The models are intentionally verbose – they provide docstrings, runtime
validation, and helpful reprs so debugging case definitions becomes painless.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import List, Mapping, Sequence, Tuple

from .exceptions import CaseValidationError


@dataclass(frozen=True, slots=True)
class Argument:
    """Represents an individual argument in the court case.

    Parameters
    ----------
    claim:
        Human readable statement describing the argument.
    weight:
        Relative importance within the side's overall case.  Must be in the
        ``[0, 1]`` range.  We treat ``weight`` as the share of attention the
        panel should give to the argument.
    strength:
        Empirical strength of evidence in favour of the argument, again in the
        ``[0, 1]`` range.
    tags:
        Optional taxonomy that calling code can use to categorise arguments.
    """

    claim: str
    weight: float
    strength: float
    tags: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        # Defensive programming: eagerly validate to catch errors as early as
        # possible.  Raising ``CaseValidationError`` keeps error handling
        # consistent for library consumers.
        if not self.claim or not self.claim.strip():
            raise CaseValidationError("Argument claim must be a non-empty string.")
        if not 0.0 <= self.weight <= 1.0:
            raise CaseValidationError(
                f"Argument weight for '{self.claim}' must be between 0 and 1;"
                f" received {self.weight!r}."
            )
        if not 0.0 <= self.strength <= 1.0:
            raise CaseValidationError(
                f"Argument strength for '{self.claim}' must be between 0 and 1;"
                f" received {self.strength!r}."
            )
        # Normalise tags to a tuple with stripped whitespace.
        object.__setattr__(self, "tags", tuple(tag.strip() for tag in self.tags))


@dataclass(slots=True)
class Case:
    """A complete case pitting canon against fanon arguments."""

    title: str
    summary: str
    prosecution: Sequence[Argument]
    defense: Sequence[Argument]
    metadata: Mapping[str, str] | None = None

    def all_arguments(self) -> List[Argument]:
        """Return every argument regardless of side.

        Returning a ``list`` instead of a generator aids debugging because the
        caller can inspect the repr without accidentally exhausting an iterator.
        """

        return [*self.prosecution, *self.defense]

    def validate(self) -> None:
        """Ensure the case contains sane data.

        The method raises :class:`CaseValidationError` when the structure is not
        acceptable.  Validation is idempotent so callers can safely run it
        multiple times during unit tests or CLI processing.
        """

        _validate_text(self.title, "title")
        _validate_text(self.summary, "summary")
        if not self.prosecution:
            raise CaseValidationError("Prosecution must contain at least one argument.")
        if not self.defense:
            raise CaseValidationError("Defense must contain at least one argument.")
        for argument in self.all_arguments():
            if not isinstance(argument, Argument):
                raise CaseValidationError(
                    "Every argument must be an instance of nerdcourt.Argument."
                )
        for side, arguments in {
            "prosecution": self.prosecution,
            "defense": self.defense,
        }.items():
            weight_total = sum(argument.weight for argument in arguments)
            if weight_total <= 0:
                raise CaseValidationError(
                    f"The {side} side must have a positive sum of weights."
                )
            if weight_total > 1.5:
                # We allow the sum to exceed 1 a little to give authors freedom,
                # but cap it to avoid runaway scores.
                raise CaseValidationError(
                    f"The {side} side seems over-specified (total weight {weight_total:.2f})."
                )

    def to_dict(self) -> Mapping[str, object]:
        """Serialise the case into basic Python types.

        This helper simplifies JSON export and makes the CLI output easier to
        unit test.
        """

        return {
            "title": self.title,
            "summary": self.summary,
            "prosecution": [asdict(argument) for argument in self.prosecution],
            "defense": [asdict(argument) for argument in self.defense],
            "metadata": dict(self.metadata or {}),
        }


@dataclass(frozen=True, slots=True)
class Verdict:
    """Outcome of an evaluated case."""

    winner: str
    prosecution_score: float
    defense_score: float
    confidence: float
    notes: str

    def as_dict(self) -> Mapping[str, float | str]:
        """Return a JSON-serialisable representation of the verdict."""

        return {
            "winner": self.winner,
            "prosecution_score": round(self.prosecution_score, 4),
            "defense_score": round(self.defense_score, 4),
            "confidence": round(self.confidence, 4),
            "notes": self.notes,
        }


def _validate_text(value: str, field_name: str) -> None:
    """Validate user-facing text fields.

    Keeping validation logic in a dedicated helper keeps :class:`Case` readable
    without sacrificing the clarity of the error messages.
    """

    if not value or not value.strip():
        raise CaseValidationError(f"Case {field_name} must be a non-empty string.")


__all__ = [
    "Argument",
    "Case",
    "Verdict",
]
