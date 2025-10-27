"""Core storytelling logic for the Nerd Court trial simulator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import random


@dataclass(frozen=True)
class TrialOutcome:
    """Represents the verdict delivered by Judge Jerry Springer."""

    verdict: str
    finishing_move: str

    def describe(self) -> str:
        verdict = self.verdict.rstrip(".")
        finishing_move = self.finishing_move.rstrip(".")
        return f"Verdict: {verdict}. Finishing Move: {finishing_move}."


class TrialEngine:
    """Generate a single absurdly dramatic multi-verse trial transcript."""

    def __init__(self, rng: Optional[random.Random] = None) -> None:
        self._rng = rng or random.Random()

    def run_trial(self, case_caption: str) -> str:
        """Return a full trial transcript for the requested case."""

        prosecution = self._prosecution_sequence(case_caption)
        defense = self._defense_sequence(case_caption)
        clash = self._dimension_clash()
        verdict = self._render_verdict(case_caption)

        transcript_sections: List[str] = [
            self._intro(case_caption),
            prosecution,
            defense,
            clash,
            verdict.describe(),
        ]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"\n=== Nerd Court Transcript ({timestamp}) ===\n"
        return header + "\n\n".join(transcript_sections) + "\n"

    # ------------------------------------------------------------------
    # Narrative building blocks
    # ------------------------------------------------------------------
    def _intro(self, case_caption: str) -> str:
        bailiff_lines = [
            "All rise! The Court of Canonical Appeals is now in session.",
            "The Multiversal Bailiff reminds you to silence all timeline-hopping devices.",
            "Introducing the honorable Judge Jerry Springer, He Who Remains Petty.",
        ]
        intro = [
            f"Case on the docket: {case_caption}.",
            "Prosecuting on behalf of narrative integrity: Jason Todd, a.k.a. Red Hood, wielding Exhibit Crowbar A.",
            "Defense counsel present: an army of continuity lawyers from Variant Legal, LLP.",
        ]
        return "\n".join(bailiff_lines + intro)

    def _prosecution_sequence(self, case_caption: str) -> str:
        canon_grievances = [
            "citing Section 66 of the Sacred Holocron that forbids retconning midichlorian donors.",
            "arguing that the villainous heel turn violates the Saturday morning cartoon accords.",
            "presenting holographic flowcharts linking 37 comic crossovers that never actually happened.",
            "introducing an emotionally charged remix of the original trilogy's theme as Exhibit B-sharp.",
            "deploying a WayneTech projector that replays the exact moment canon got retconned in Dolby Multiverse.",
        ]
        flourish = self._rng.choice(
            [
                "He slams the crowbar for emphasis, shattering three adjacent realities.",
                "He produces sworn affidavits signed by five alternate-universe George Lucases.",
                "He calls in Nightwing as an expert witness on franchise trauma continuity.",
                "He opens a rift to Earth-1610 for corroborating testimony from Ultimate Aunt May.",
            ]
        )
        charge = self._rng.choice(canon_grievances)
        return (
            "\n".join(
                [
                    "PROSECUTION OPENING STATEMENT:",
                    f"Red Hood alleges that {case_caption} is in grievous breach of canonical character arcs, {charge}",
                    flourish,
                ]
            )
        )

    def _defense_sequence(self, case_caption: str) -> str:
        defenses = [
            "introduces a binding contract from the Council of Fanfic Elders authorizing creative reinterpretations.",
            "submits a reel of heartfelt fan tributes proving the new canon sparks more joy than the original.",
            "cites the Supreme Variants ruling in *Marvel v. Everyone* that vibes outrank continuity.",
            "argues the multiverse demanded a musical episode and the canon must learn to jazz hands along.",
            "presents sworn testimony from five future selves who all agree the twist is secretly brilliant.",
        ]
        curveballs = [
            "A surprise witness appears: a noir-version Princess Leia with receipts from the Time Variance Authority.",
            "Defense counsel calls the original showrunner from Earth-Prime, who admits the plot hole was intentional foreshadowing.",
            "A montage of con-goers cheering drowns out the prosecutor's objections.",
            "They unleash a pocket universe where the disputed canon already won three Emmys.",
            "A legal brief materializes in glittering runes, citing precedent from the 90s animated multiverse.",
        ]
        defense_choice = self._rng.choice(defenses)
        curveball_choice = self._rng.choice(curveballs)
        return "\n".join(
            [
                "DEFENSE REBUTTAL:",
                f"Counsel for {case_caption} {defense_choice}",
                curveball_choice,
            ]
        )

    def _dimension_clash(self) -> str:
        clashes = [
            "MID-TRIAL MULTIVERSE EVENT:",
            "A dimensional breach floods the courtroom with variants, including a Muppet version of everyone present.",
            "Judge Springer pauses proceedings to autograph a VHS copy of his 1998 specials for three different Batmen.",
            "The gallery erupts as Luke Skywalker morphs into the Joker, practicing a Mortal Kombat fatality in slow motion.",
            "Meanwhile, a documentary crew from Earth-1998 live-streams the chaos on dial-up internet.",
        ]
        return "\n".join(clashes)

    def _render_verdict(self, case_caption: str) -> TrialOutcome:
        verdicts = [
            "GUILTY of canon desecration—sentence: immediate narrative reboot with 12-issue redemption arc.",
            "NOT GUILTY—canon is hereby expanded to include musical laser fights and dramatic retcons.",
            "CONTEMPT OF CANON—ordered to host a crossover special with three unexpected cartoon cameos.",
            "MISTRIAL—timeline collapsed under the weight of references; retrial scheduled in Earth-23.",
        ]
        finishers = [
            "Luke-as-Joker performs a crowbar-assisted friendship move that rewrites Act Three in neon graffiti.",
            "Red Hood tag-teams with a Spider-Verse variant to drop the defendant into a narrative plot hole.",
            "Judge Springer declares 'Final Thoughts' and executes a reality-TV fatality complete with chair toss.",
            "A chorus line of multiversal selves breaks into synchronized 'Toasty!' while reality respawns.",
        ]
        return TrialOutcome(
            verdict=self._rng.choice(verdicts),
            finishing_move=self._rng.choice(finishers),
        )
