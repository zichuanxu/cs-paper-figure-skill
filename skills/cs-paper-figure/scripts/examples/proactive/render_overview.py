"""Redesign of Fig. 1 of "Proactive AI for Superintelligent Agents": proactive vs. reactive agents.

Content from the source figure: a reactive agent answers when asked ("How is the report going?" /
"Here is the latest update"; act to fulfil the goal from the prompt); a proactive agent runs five stages
(Aware: continuously monitor context; Anticipate: identify / infer gaps between current progress and
intended state; Agenda: generate candidate goals to address gaps, e.g. draft report, update charts,
prepare summary, review data, schedule meeting; Arbitrate: decide whether initiative is worthwhile,
timely and safe; Act: suggest, assist or execute before being asked) and Adaptation learns from outcomes
and feedback. The proactive scene's dialogue is illustrative wording for the source's outcome panel.

Layout change: the left column contrasts what the user experiences (asked vs. unasked); the right block
explains how the proactive agent gets there, each stage in its fixed series colour.

    python render_overview.py --out <dir>
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sixa import SIXA  # noqa: E402
from paperkit import Canvas, INK, MUTED, ROLE  # noqa: E402

ART, SCENES = os.path.join(HERE, "art"), os.path.join(HERE, "scenes")
STAGES = [  # (series name, short name, icon, description lines, extra list)
    ("Awareness", "Aware", "aware", ["Continuously", "monitor context"], None),
    ("Anticipation", "Anticipate", "anticipate", ["Identify / infer gaps", "between current", "progress and", "intended state"], None),
    ("Agenda", "Agenda", "agenda", ["Generate candidate", "goals to address", "gaps"],
     ["Draft report", "Update charts", "Prepare summary", "Review data", "Schedule meeting"]),
    ("Arbitration", "Arbitrate", "arbitrate", ["Decide whether", "initiative is", "worthwhile, timely", "and safe"], None),
    ("Action", "Act", "act", ["Suggest, assist or", "execute before", "being asked"], None),
]
W, H = 178, 96
INDIGO = dict(fill="#EEEFF8", soft="#DADCF0", stroke="#5A5FA8", ink="#2B2F6E", mark="#3B3F8C")


def art(cv, name, cx, cy, w, fallback=None, fit="width"):
    p = os.path.join(ART, name + ".png")
    if os.path.exists(p):
        return cv.image(p, cx, cy, w, fit=fit)
    if fallback:
        fallback()
    return w


def scene_card(cv, x, y, w, h, r, title, scene, bubbles, footer):
    c = r if isinstance(r, dict) else ROLE[r]
    cv.box(x, y, w, h, "neutral", fill=c["fill"], stroke=c["stroke"], lw=0.7, radius=2.2)
    cv.text(x + 2.4, y + h - 3.6, title, size=8.2, weight="bold", color=c["ink"], ha="left")
    p = scene if os.path.isabs(scene) else os.path.join(SCENES, scene + ".png")
    ih = cv.image(p, x + w / 2, y + h * 0.43, w * 0.84) if os.path.exists(p) else 0
    for text, bx, by, tail in bubbles:
        cv.bubble(x + bx * w, y + by * h, text, tail=(x + tail[0] * w, y + tail[1] * h), size=6.2)
    cv.chip(x + w / 2, y + 3.6, footer, c if isinstance(c, dict) else r, size=6.6, pad=1.2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.0)
    # left: what the user experiences
    scene_card(cv, 2, 50, 56, 44, "neutral", "Reactive agent", os.path.join(ART, "reactive_ask.png"),
               [("How is the\nreport going?", 0.26, 0.80, (0.30, 0.58)),
                ("Here is the\nlatest update.", 0.74, 0.80, (0.66, 0.60))], "acts when asked")
    scene_card(cv, 2, 2, 56, 44, INDIGO, "Proactive agent", "proactive",
               [("Report drafted,\ncharts updated,\nmeeting scheduled.", 0.66, 0.78, (0.70, 0.56))],
               "acts before being asked")
    # right: how the proactive agent gets there
    x0, cw, gap, cy0, ch = 62.6, 21.6, 1.6, 46.0, 43.0
    cv.text(x0, H - 3.4, "Inside the proactive agent", size=8.4, weight="bold", color=INDIGO["ink"], ha="left")
    cv.text(x0 + 43.0, H - 3.4, "five stages run without a new request; Adaptation tunes all of them", size=6.4,
            color=MUTED, ha="left", style="italic")
    for k, (series, short, icon, desc, extra) in enumerate(STAGES):
        c = SIXA[series]
        x = x0 + k * (cw + gap)
        cv.box(x, cy0, cw, ch, "neutral", fill=c["fill"], stroke=c["stroke"], lw=0.7, radius=2.0)
        art(cv, icon, x + cw / 2, cy0 + ch - 8.0, 10.0, fit="box",
            fallback=lambda: cv.ax.add_patch(__import__("matplotlib").patches.Circle((x + cw / 2, cy0 + ch - 8.0), 4.0, fc=c["soft"], ec=c["stroke"], lw=0.6, zorder=6)))
        cv.badge(x + 3.4, cy0 + ch - 3.4, k + 1, c, d=3.4)
        cv.text(x + cw / 2, cy0 + ch - 16.2, short, size=8.2, weight="bold", color=c["ink"])
        for j, line in enumerate(desc):
            cv.text(x + cw / 2, cy0 + ch - 20.4 - j * 2.7, line, size=6.2, color=INK)
        if extra:
            ey = cy0 + ch - 20.4 - len(desc) * 2.7 - 0.9
            for j, item in enumerate(extra):
                yy = ey - j * 2.6
                cv.ax.add_patch(__import__("matplotlib").patches.FancyBboxPatch(
                    (x + 2.2, yy - 0.75), 1.5, 1.5, boxstyle="round,pad=0,rounding_size=0.3", fc="white", ec=c["stroke"], lw=0.4, zorder=8))
                cv.text(x + 4.6, yy, item, size=5.9, color=c["ink"], ha="left")
        if k < 4:
            cv.arrow([(x + cw + 0.2, cy0 + ch / 2), (x + cw + gap - 0.2, cy0 + ch / 2)], color="#4B5563", lw=0.9, head=1.1)
    # adaptation: learns from outcomes, tunes every stage
    T = SIXA["Adaptation"]
    bx0, bx1, by0, bh = x0, x0 + 5 * cw + 4 * gap, 24.0, 11.0
    cv.box(bx0, by0, bx1 - bx0, bh, "neutral", fill=T["fill"], stroke=T["stroke"], lw=0.7, radius=2.0)
    art(cv, "adapt", bx0 + 6.0, by0 + bh / 2, 8.0)
    cv.badge(bx0 + 12.4, by0 + bh / 2, 6, T, d=3.4)
    cv.text(bx0 + 15.0, by0 + bh / 2 + 1.6, "Adaptation", size=8.2, weight="bold", color=T["ink"], ha="left")
    cv.text(bx0 + 15.0, by0 + bh / 2 - 2.2, "learn from outcomes and feedback", size=6.4, color=INK, ha="left")
    for k in range(5):
        xx = x0 + k * (cw + gap) + cw / 2
        cv.arrow([(xx, by0 + bh), (xx, cy0)], color=T["mark"], lw=0.7, head=1.0, dashed=True)
    # outcome from Act returns to Adaptation (feedback path)
    ax = x0 + 4 * (cw + gap) + cw * 0.82
    cv.arrow([(ax, cy0), (ax, by0 + bh)], color=SIXA["Action"]["mark"], lw=0.7, head=1.0)
    cv.text(x0 + 4 * (cw + gap) + cw / 2 - 1.6, (by0 + bh + cy0) / 2, "outcome &\nfeedback", size=5.9, color=MUTED, ha="right", style="italic",
            linespacing=1.0)
    # the proactive scene on the left is what this pipeline produces
    cv.arrow([(x0 - 0.6, cy0 + ch / 2), (61.0, cy0 + ch / 2), (61.0, 30.0), (58.8, 30.0)], color=INDIGO["mark"],
             lw=0.9, head=1.3, radius=1.0)
    print("\n".join(cv.save(os.path.join(a.out, "proactive_overview"))))


if __name__ == "__main__":
    main()
