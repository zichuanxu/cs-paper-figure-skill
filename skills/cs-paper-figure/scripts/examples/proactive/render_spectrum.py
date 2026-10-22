"""Redesign of Fig. 4 of "Proactive AI for Superintelligent Agents": the reactivity-proactivity spectrum.

Content from the source figure: three settings along one axis (reactive -> more proactive), what the agent
provides (reactive response, mixed-initiative assistance, self-initiated agency) and the human's role
(operator, collaborator, reviewer). Scenes in scenes/ were generated with scripts/codex_icons.py (style
"scene", one cast, no text in pixels); all dialogue and labels are vector text. Dialogue in panels 2-3 is
illustrative wording for the source's "proposed work plan" and "work progress update" panels.

    python render_spectrum.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sixa  # noqa: E402,F401  (puts paperkit on the path)
from paperkit import Canvas, INK, mix  # noqa: E402

LIGHT, DARK = "#8FB0B8", "#2B2F6E"  # one hue ramp: lightness carries "more initiative"
SCENES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")
COLS = [  # scene, agent provides, human role, bubbles: (text, centre x, centre y, tail target) as panel fractions
    ("reactive", "Reactive response", "Operator",
     [("Good! Now close\nthe lid and run\na test print.", 0.24, 0.82, (0.25, 0.62)),
      ("Understood.\nPreparing the\ntest print…", 0.70, 0.82, (0.62, 0.44))]),
    ("mixed", "Mixed-initiative assistance", "Collaborator",
     [("I drafted a work plan.\nShall I go ahead?", 0.62, 0.80, (0.64, 0.58))]),
    ("proactive", "Self-initiated agency", "Reviewer",
     [("Update: analysis done,\nreport delivered,\nsync scheduled.", 0.62, 0.80, (0.70, 0.54))]),
]
W, H = 178, 92


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.0)
    x0, pw, gap = 27.0, 47.5, 2.75
    cv.spectrum(x0, W - 3.0, H - 7.0, LIGHT, DARK, labels=("Reactive", "More proactive"), size=7.6)
    cv.text(4.0, H - 7.0, "Initiative", size=7.2, weight="bold", color=INK, ha="left")
    shades = [mix(LIGHT, DARK, t) for t in (0.08, 0.5, 0.95)]
    py, ph = 31.0, 46.0
    for k, (scene, provides, role_, bubbles) in enumerate(COLS):
        px = x0 + k * (pw + gap)
        cv.box(px, py, pw, ph, "neutral", fill="#FAFBFC", stroke="#DCE0E5", lw=0.5, radius=2.0)
        cv.image(os.path.join(SCENES, scene + ".png"), px + pw / 2, py + ph * 0.36, pw * 0.9)
        for text, bx, by, (tx, ty) in bubbles:
            cv.bubble(px + bx * pw, py + by * ph, text, tail=(px + tx * pw, py + ty * ph), size=6.0)
        # agent provides / human role chips: same hue ramp as the axis
        fg = INK if k == 0 else "white"
        for row, (label, yy) in enumerate(((provides, 22.0), (role_, 11.0))):
            cv.box(px + 3.0, yy - 3.6, pw - 6.0, 7.2, "neutral", fill=shades[k] if row == 0 else "white",
                   stroke=shades[k], lw=0.9, radius=1.6)
            cv.text(px + pw / 2, yy, label, size=7.2, weight="bold",
                    color=(fg if row == 0 else mix(shades[k], "#000000", 0.25)))
    cv.text(4.0, 22.0, "Agent\nprovides", size=7.2, weight="bold", color=INK, ha="left", linespacing=1.1)
    cv.text(4.0, 11.0, "Human's\nrole", size=7.2, weight="bold", color=INK, ha="left", linespacing=1.1)
    print("\n".join(cv.save(os.path.join(a.out, "proactive_spectrum"))))


if __name__ == "__main__":
    main()
