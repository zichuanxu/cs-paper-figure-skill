"""Redesign of Fig. 10 of "Proactive AI for Superintelligent Agents" (Yang et al., Google / UIUC):
Arbitration, the gate between a worthwhile goal and a warranted intervention.

Content from the source figure: a candidate action from Agenda passes four tests in order (uncertainty &
confidence, value vs. cost, timing, risk & reversibility); each failure has its own fallback; only when
all four pass is the agent licensed to intervene, which hands over to Action.

    python render_arbitration.py --out <dir>
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sixa import SIXA  # noqa: E402
from paperkit import Canvas, INK, MUTED  # noqa: E402
from matplotlib.patches import Arc, Polygon  # noqa: E402

ARB, AGD, ACT = SIXA["Arbitration"], SIXA["Agenda"], SIXA["Action"]
PASS = dict(fill="#EAF4EE", soft="#D3E9DB", stroke="#4E9166", ink="#1E5B36", mark="#2E8B57")
FAIL = dict(fill="#FBEEEC", soft="#F4D9D4", stroke="#C98B7E", ink="#7E2E22", mark="#B5523F")
GATES = [  # (title, question, failure label, fallback)
    ("Uncertainty & confidence", "Is the belief about the user's need confident enough?", "Low confidence", "clarify or seek more information"),
    ("Value vs. cost", "Does the expected value of acting outweigh the cost?", "Low net value", "suppress, defer or re-plan"),
    ("Timing", "When in the flow of events should it happen?", "Bad moment", "wait for a task boundary"),
    ("Risk & reversibility", "Is it safe enough given the chance of being wrong?", "Unsafe / unauthorized", "safer fallback, approval, escalation or refusal"),
]
W, H = 178, 84


def glyph(cv, k, x, y, c):
    """Small vector glyph per test: gauge, balance, clock, shield."""
    col, lw = c["stroke"], 0.6
    if k == 0:
        cv.ax.add_patch(Arc((x, y - 0.8), 5.0, 5.0, theta1=0, theta2=180, ec=col, lw=lw, zorder=12))
        a = math.radians(55)
        cv.line([(x, y - 0.8), (x + 2.0 * math.cos(a), y - 0.8 + 2.0 * math.sin(a))], color=col, lw=lw)
        cv.dot(x, y - 0.8, color=col, d=0.7)
    elif k == 1:
        cv.line([(x, y - 2.0), (x, y + 1.6)], color=col, lw=lw)
        cv.line([(x - 2.4, y + 1.0), (x + 2.4, y + 1.6)], color=col, lw=lw)
        for bx, by in ((x - 2.4, y + 1.0), (x + 2.4, y + 1.6)):
            cv.ax.add_patch(Arc((bx, by - 1.2), 2.0, 1.4, theta1=180, theta2=360, ec=col, lw=lw, zorder=12))
        cv.line([(x - 1.0, y - 2.0), (x + 1.0, y - 2.0)], color=col, lw=lw)
    elif k == 2:
        cv.icon_clock(x, y, 4.6, color=col)
    else:
        pts = [(x - 2.0, y + 1.8), (x, y + 2.4), (x + 2.0, y + 1.8), (x + 1.8, y - 0.6), (x, y - 2.4), (x - 1.8, y - 0.6)]
        cv.ax.add_patch(Polygon(pts, closed=True, fc="none", ec=col, lw=lw, zorder=12, joinstyle="round"))
        cv.text(x, y + 0.1, "!", size=6.2, color=col, weight="bold")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.0)
    ix, iy, iw, ih = cv.chapter(2, 2, W - 4, H - 4, ARB, "Arbitration", prev=("Agenda", AGD), nxt=("Action", ACT), tab_w=7.5)
    cv.text(ix + iw / 2, iy + ih + 0.6, "a worthwhile goal is not yet a warranted intervention", size=6.6,
            color=MUTED, style="italic")
    # gate column: four tests in order
    gx, gw, rh, gap = ix + 1.0, 112.0, 13.6, 2.6
    top = iy + ih - 3.6
    cv.chip(gx + 0.4, top - 0.4, "candidate action", AGD, size=6.2, ha="left", pad=0.9)
    bar_x, bar_w = gx + gw + 9.0, 15.0
    ys = []
    for k, (title, q, fl, fb) in enumerate(GATES):
        y = top - 2.6 - (k + 1) * rh - k * gap
        ys.append(y + rh / 2)
        cv.box(gx, y, gw, rh, ARB, fill="white", lw=0.6, radius=1.6)
        cv.badge(gx + 4.0, y + rh / 2, k + 1, ARB, d=3.6)
        glyph(cv, k, gx + 11.0, y + rh / 2, ARB)
        cv.text(gx + 16.5, y + rh / 2 + 2.6, title, size=7.4, weight="bold", color=ARB["ink"], ha="left")
        cv.text(gx + 16.5, y + rh / 2 - 2.4, q, size=6.4, color=INK, ha="left")
        # failure exit stays inside the gate's row, so pass lines never cross it
        fx = gx + 74.0
        cv.box(fx, y + 1.6, gw - 75.6, rh - 3.2, FAIL, lw=0.5, radius=1.2)
        lines = [fb] if len(fb) <= 34 else [fb[:fb.rfind(",", 0, 34) + 1], fb[fb.rfind(",", 0, 34) + 2:]]
        ly = y + rh / 2 + (2.9 if len(lines) == 2 else 1.8)
        cv.icon_cross(fx + 2.4, ly, 1.8, color=FAIL["mark"], lw=0.8)
        cv.text(fx + 4.4, ly, fl.upper(), size=5.9, weight="bold", color=FAIL["mark"], ha="left")
        for j, t in enumerate(lines):
            cv.text(fx + 1.6, ly - 3.4 - j * 2.7, t, size=6.1, color=FAIL["ink"], ha="left")
        # pass exit: into the AND bar
        cv.arrow([(gx + gw, y + rh / 2), (bar_x, y + rh / 2)], color=PASS["mark"], lw=0.8, head=1.1)
        cv.icon_check(gx + gw + 2.6, y + rh / 2 + 1.7, 1.6, color=PASS["mark"], lw=0.8)
        cv.text(gx + gw + 3.8, y + rh / 2 + 1.6, "pass", size=5.9, color=PASS["mark"], weight="bold", ha="left")
        # sequence: next test only after this one passes
        if k < 3:
            cv.arrow([(gx + 4.0, y), (gx + 4.0, y - gap)], color=ARB["stroke"], lw=0.6, head=0.9)
    # AND bar = licence to intervene
    y0, y1 = ys[-1] - rh / 2, ys[0] + rh / 2
    cv.box(bar_x, y0, bar_w, y1 - y0, PASS, lw=0.8, radius=2.0)
    cv.text(bar_x + bar_w / 2, (y0 + y1) / 2 + 9.0, "all four", size=6.4, color=PASS["ink"])
    cv.text(bar_x + bar_w / 2, (y0 + y1) / 2 + 5.8, "pass", size=6.4, color=PASS["ink"])
    cv.text(bar_x + bar_w / 2, (y0 + y1) / 2 - 1.0, "Licence", size=7.6, weight="bold", color=PASS["ink"])
    cv.text(bar_x + bar_w / 2, (y0 + y1) / 2 - 4.4, "to", size=7.6, weight="bold", color=PASS["ink"])
    cv.text(bar_x + bar_w / 2, (y0 + y1) / 2 - 7.8, "intervene", size=7.6, weight="bold", color=PASS["ink"])
    cv.arrow([(bar_x + bar_w, (y0 + y1) / 2), (ix + iw + 1.6, (y0 + y1) / 2)], color=PASS["mark"], lw=0.9, head=1.2)
    print("\n".join(cv.save(os.path.join(a.out, "proactive_arbitration"))))


if __name__ == "__main__":
    main()
