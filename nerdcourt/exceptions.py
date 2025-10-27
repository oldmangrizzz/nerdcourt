"""Custom exception hierarchy used by Nerd Court.

Having a dedicated module for exceptions keeps the rest of the package tidy and
encourages the code to raise meaningful, well-documented error types.  The
exceptions are intentionally lightweight so that catching them remains simple.
"""

from __future__ import annotations


class NerdCourtError(Exception):
    """Base class for all custom errors in the package."""


class CaseValidationError(NerdCourtError):
    """Raised when a case definition fails validation.

    The error message is written with end-users in mind so that mistakes in a
    JSON case file, for example, can be diagnosed without having to read the
    source code.
    """


class ArgumentScoreError(NerdCourtError):
    """Raised when argument scoring encounters an impossible state."""


__all__ = [
    "ArgumentScoreError",
    "CaseValidationError",
    "NerdCourtError",
]
