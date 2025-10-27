import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nerdcourt.trial import TrialEngine


def test_run_trial_deterministic_output():
    engine = TrialEngine(rng=random.Random(1234))
    transcript = engine.run_trial("Skywalker Legacy v. Princess Palpatine")

    assert "Nerd Court Transcript" in transcript
    assert "Skywalker Legacy v. Princess Palpatine" in transcript
    assert "PROSECUTION OPENING STATEMENT" in transcript
    assert "DEFENSE REBUTTAL" in transcript
    assert "Verdict:" in transcript

    expected_snippet = (
        "Red Hood alleges that Skywalker Legacy v. Princess Palpatine is in grievous breach"
    )
    assert expected_snippet in transcript
