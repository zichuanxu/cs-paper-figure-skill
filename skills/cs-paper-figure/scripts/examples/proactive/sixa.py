"""Shared series palette for the Proactive-AI redesigns: every figure imports it, so each of the six
capacities keeps one hue everywhere (the source paper re-picks colours per figure)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import series  # noqa: E402

NAMES = ("Awareness", "Anticipation", "Agenda", "Arbitration", "Action", "Adaptation")
SIXA = series(NAMES)  # green, blue, violet, amber, coral, teal
