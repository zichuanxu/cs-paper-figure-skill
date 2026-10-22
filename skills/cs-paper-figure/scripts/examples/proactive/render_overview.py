"""Redesign of Fig. 1 of "Proactive AI for Superintelligent Agents": proactive vs. reactive AI agents.

Content from the source figure: a reactive agent acts when asked ("How is the report going?" / "Here is the
latest update"); a proactive agent runs five stages without a new request (Aware: continuously monitor
context; Anticipate: identify / infer gaps between current progress and intended state; Agenda: generate
candidate goals to address gaps; Arbitrate: decide whether initiative is worthwhile, timely and safe; Act:
suggest, assist or execute before being asked), Adaptation learns from outcomes and feedback, and the user
receives finished work.

Kept from the original: the left-to-right story (reactive scene, five illustrated stages, delighted user),
one robot doing each stage, numbered stage headers, the Adaptation bar feeding every stage. Fixed: stage
colours come from the series palette shared by all figures, headers are solid with white titles, text in
the pixels (the agenda list, the screen) is gone, and the two modes end in matching verdict chips.

    python render_overview.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sixa import SIXA  # noqa: E402
from paperkit import Canvas, INK  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon  # noqa: E402

VIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vignettes")
REACT, PRO = "#7A8599", "#2B2F6E"  # the two ends of the reactive -> proactive ramp (as in the spectrum figure)
STAGES = [  # (vignette, series name, short name, description from the source figure)
    ("f1_aware", "Awareness", "Aware", "Continuously\nmonitor\ncontext"),
    ("f1_anticipate", "Anticipation", "Anticipate", "Identify or infer\ngaps between\nprogress and\nintended state"),
    ("f1_agenda", "Agenda", "Agenda", "Generate\ncandidate goals\nto address gaps"),
    ("f1_arbitrate", "Arbitration", "Arbitrate", "Decide if\ninitiative is\nworthwhile,\ntimely and safe"),
    ("f1_act", "Action", "Act", "Suggest, assist\nor execute\nbefore being\nasked"),
]
W, H = 178, 68


def rbox(cv, x, y, w, h, fc, ec="none", lw=0.0, r=1.4, z=5):
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.4)
    top = H - 7.6
    # ---- reactive agent (left) ------------------------------------------------------------------
    lx, lw_ = 1.0, 33.0
    cv.text(lx + lw_ / 2, H - 3.4, "Reactive AI agent", size=10, weight="bold", color=REACT)
    vh = 38.0
    cv.image(os.path.join(VIG, "f1_reactive.jpg"), lx + lw_ / 2, top - vh / 2, lw_, fit="cover", h=vh, radius=1.8,
             focus=(0.55, 0.45), z=5)
    cv.bubble(lx + 9.8, top - 4.4, "How is the\nreport going?", tail=(lx + 14.0, top - 11.5), size=6.2)
    cv.bubble(lx + 25.0, top - 13.0, "Here is the\nlatest update.", tail=(lx + 26.0, top - 19.0), size=6.2)
    rbox(cv, lx, top - vh - 7.4, lw_, 5.8, REACT, r=2.9)
    cv.text(lx + lw_ / 2, top - vh - 4.5, "Acts when asked", size=8.2, weight="bold", color="white")
    cv.text(lx + lw_ / 2, top - vh - 11.0, "acts to fulfil the goal\nstated in the prompt", size=6.6, color=INK,
            linespacing=1.1)
    cv.line([(lx + lw_ + 2.0, 2.0), (lx + lw_ + 2.0, H - 1.0)], color="#C9CED6", lw=0.6, dashed=True)
    # ---- proactive agent: five stages + adaptation -----------------------------------------------
    sx0, cw, gap = lx + lw_ + 4.4, 18.8, 2.6
    sx1 = sx0 + 5 * cw + 4 * gap
    cv.text((sx0 + sx1) / 2, H - 3.4, "Proactive AI agent", size=10, weight="bold", color=PRO)
    cv.text(sx1, H - 3.4, "no new request needed", size=6.6, color=PRO, style="italic", ha="right")
    hh, vh2, dh = 5.6, 22.4, 12.6
    bottom = top - hh - vh2 - dh
    adapt = SIXA["Adaptation"]
    for k, (vig, name, short, desc) in enumerate(STAGES):
        c = SIXA[name]
        x = sx0 + k * (cw + gap)
        rbox(cv, x, bottom, cw, top - bottom, c["fill"], c["stroke"], 0.6, r=1.8, z=3)
        rbox(cv, x, top - hh, cw, hh, c["mark"], r=1.8, z=4)
        rbox(cv, x, top - hh, cw, 2.0, c["mark"], r=0.0, z=4)
        cv.ax.add_patch(Circle((x + 2.9, top - hh / 2), 1.8, fc="white", ec="none", zorder=5))
        cv.text(x + 2.9, top - hh / 2 - 0.05, str(k + 1), size=6.6, weight="bold", color=c["mark"], z=6)
        cv.text(x + 5.1, top - hh / 2, short, size=7.8, weight="bold", color="white", ha="left", z=6)
        cv.image(os.path.join(VIG, vig + ".jpg"), x + cw / 2, top - hh - vh2 / 2 - 0.6, cw - 1.6, fit="cover",
                 h=vh2, radius=1.2, focus=(0.45, 0.4), z=5)
        cv.text(x + cw / 2, bottom + dh / 2 - 0.1, desc, size=6.2, color=c["ink"], linespacing=1.08)
        if k < 4:  # chevron to the next stage
            gx = x + cw + gap / 2
            yy = top - hh - vh2 / 2
            cv.ax.add_patch(Polygon([(gx - 0.9, yy + 1.5), (gx + 0.9, yy), (gx - 0.9, yy - 1.5)], closed=True,
                                    fc=SIXA[STAGES[k + 1][1]]["mark"], ec="none", zorder=6))
        # adaptation feeds every stage
        cv.arrow([(x + cw / 2, 13.4), (x + cw / 2, bottom - 0.3)], color=adapt["mark"], lw=0.8, head=1.0, dashed=True)
    # adaptation bar
    ay, ah = 1.0, 12.0
    rbox(cv, sx0, ay, sx1 - sx0, ah, adapt["fill"], adapt["stroke"], 0.7, r=2.0, z=3)
    cv.image(os.path.join(VIG, "f1_adapt.jpg"), sx0 + 11.6, ay + ah / 2, 21.6, fit="cover", h=ah - 1.6, radius=1.2,
             focus=(0.5, 0.45), zoom=1.2, z=5)
    cv.ax.add_patch(Circle((sx0 + 26.0, ay + ah / 2 + 2.2), 2.0, fc=adapt["mark"], ec="none", zorder=5))
    cv.text(sx0 + 26.0, ay + ah / 2 + 2.15, "6", size=7.0, weight="bold", color="white", z=6)
    cv.text(sx0 + 29.0, ay + ah / 2 + 2.2, "Adaptation", size=9.6, weight="bold", color=adapt["ink"], ha="left")
    sub = "learn from outcomes\nand feedback"
    cv.text(sx0 + 24.4, ay + ah / 2 - 3.0, sub, size=7.0, color=INK, ha="left", linespacing=1.05)
    # what Adaptation updates: measured chips flowed into the free part of the strip (right edge kept clear
    # for the return arrow), never hand-placed
    fx0 = sx0 + 24.4 + max(cv.text_width("Adaptation", 9.6, "bold") + 4.6, cv.text_width("learn from outcomes", 7.0)) + 2.4
    rows_h = 2 * 3.8 + 0.8
    cv.flow_chips(["Update knowledge", "Refine preferences", "Calibrate thresholds", "Improve actions"],
                  fx0, sx1 - 4.0, ay + ah / 2 + rows_h / 2, adapt, size=6.4, h=3.8, pad=0.9, gap=1.0,
                  region=(fx0, ay + 0.8, sx1 - 4.0, ay + ah - 0.8))
    # ---- outcome (right) -----------------------------------------------------------------------
    rx = sx1 + 4.4
    rw = W - 1.0 - rx
    cv.text(rx + rw / 2, H - 3.4, "Result", size=10, weight="bold", color=PRO)
    cv.image(os.path.join(VIG, "f1_outcome.jpg"), rx + rw / 2, top - vh / 2, rw, fit="cover", h=vh, radius=1.8,
             focus=(0.55, 0.5), z=5)
    act = SIXA["Action"]
    cv.arrow([(sx1 + 0.2, top - hh - vh2 / 2), (rx - 0.3, top - hh - vh2 / 2)], color=act["mark"], lw=1.4, head=1.6)
    rbox(cv, rx, top - vh - 7.4, rw, 5.8, PRO, r=2.9)
    cv.text(rx + rw / 2, top - vh - 4.5, "Acts before asked", size=8.2, weight="bold", color="white")
    cv.text(rx + rw / 2, top - vh - 11.0, "report drafted, charts\nupdated, meeting set", size=6.6, color=INK,
            linespacing=1.1)
    # outcome and feedback return to Adaptation
    cv.arrow([(rx + rw / 2, top - vh - 14.2), (rx + rw / 2, ay + ah / 2), (sx1 + 0.3, ay + ah / 2)],
             color=adapt["mark"], lw=0.8, head=1.1, dashed=True, radius=1.5)
    assert not cv.overlaps() and not cv.text_overlaps(), cv.overlaps() + cv.text_overlaps()
    print("\n".join(cv.save(os.path.join(a.out, "proactive_overview"))))


if __name__ == "__main__":
    main()
