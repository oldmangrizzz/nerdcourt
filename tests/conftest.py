"""Pytest configuration helpers."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is importable when running the test suite directly from
# a source checkout.  This mirrors what ``pip install -e .`` would do without
# requiring contributors to install the package into their virtual environment
# beforehand.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
