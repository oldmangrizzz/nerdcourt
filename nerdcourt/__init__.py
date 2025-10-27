"""Nerd Court public API.

This package contains utilities for staging tongue-in-cheek debates between
canonical and fanon interpretations of fictional works.  The top-level module
re-exports the most useful classes so that they can be imported directly from
``nerdcourt``.
"""

from .evaluator import NerdCourt
from .exceptions import CaseValidationError, NerdCourtError
from .models import Argument, Case, Verdict

__all__ = [
    "Argument",
    "Case",
    "CaseValidationError",
    "NerdCourt",
    "NerdCourtError",
    "Verdict",
]
