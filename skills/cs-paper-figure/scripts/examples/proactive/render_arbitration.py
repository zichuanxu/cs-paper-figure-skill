"""Redesign of Fig. 10 of "Proactive AI for Superintelligent Agents" (Yang et al., Google / UIUC):
Arbitration, the gate between a worthwhile goal and a warranted intervention.

Content from the source figure: a candidate action from Agenda is tested on four criteria (uncertainty &
confidence, value vs. cost, timing, risk & reversibility); each failure has its own fallback; only when
all four pass is the agent licensed to intervene, which hands over to Action.

Kept from the original (its strengths): large title, a solid numbered header per test, solid fallback chips,
a solid licence column and "To Action" tab. Fixed: the four tests no longer take four unrelated hues (they
are one capacity, so one hue and a number), Agenda / Action carry their series colours, each fallback sits
inside its own row so no pass line runs past another test's failure, and every label is at least 6.6 pt.

    python render_arbitration.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sixa import SIXA  # noqa: E402
from paperkit import Canvas, INK, mix  # noqa: E402
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon  # noqa: E402

ARB, AGD, ACT = SIXA["Arbitration"], SIXA["Agenda"], SIXA["Action"]
# pass = the proactive indigo, fail = warm grey: neither borrows a capacity hue (green is Awareness, red Action)
PASS = dict(fill="#EEEFF8", soft="#D9DAEE", stroke="#9EA1CC", ink="#2B2F6E", mark="#2B2F6E")
FAIL = dict(fill="#F5F1EE", soft="#E6DDD6", stroke="#CDBFB5", ink="#5A4A40", mark="#7D6A5E")
GATES = [  # (title, question, failure label, fallback) as in the source figure
    ("Uncertainty & Confidence", "Is the agent's belief about the user's need\nconfident enough?", "LOW CONFIDENCE", "clarify or seek\nmore information"),
    ("Value vs. Cost", "Does the expected value of acting\noutweigh the cost?", "LOW NET VALUE", "suppress, defer\nor re-plan"),
    ("Timing", "When within the flow of events should\nthe intervention occur?", "BAD MOMENT", "wait or reschedule\nfor a task boundary"),
    ("Risk & Reversibility", "Is the action safe enough given\nthe chance of being wrong?", "UNSAFE / UNAUTHORIZED", "safer fallback, approval,\nescalation or refusal"),
]
W, H = 178, 96


def rbox(cv, x, y, w, h, fc, ec="none", lw=0.0, r=1.6, z=5):
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))


def glyph(cv, k, x, y, col, lw=0.9):
    """Line glyph per test (question cloud, balance, clock, shield), 8 mm, in the Arbitration ink."""
    if k == 0:
        for dx, dy, d in ((-1.6, -0.4, 3.6), (1.4, -0.2, 3.8), (0.0, 1.4, 4.2), (-0.2, -1.4, 3.8)):
            cv.ax.add_patch(Circle((x + dx, y + dy), d / 2, fc="white", ec=col, lw=lw, zorder=11))
        cv.ax.add_patch(Circle((x, y), 2.0, fc="white", ec="none", zorder=11.5))
        cv.text(x, y, "?", size=10, weight="bold", color=col, z=12)
    elif k == 1:
        cv.line([(x, y - 3.0), (x, y + 2.6)], color=col, lw=lw)
        cv.line([(x - 3.4, y + 1.8), (x + 3.4, y + 1.8)], color=col, lw=lw)
        for bx in (x - 3.4, x + 3.4):
            cv.line([(bx, y + 1.8), (bx - 1.3, y - 0.6)], color=col, lw=lw * 0.7)
            cv.line([(bx, y + 1.8), (bx + 1.3, y - 0.6)], color=col, lw=lw * 0.7)
            cv.ax.add_patch(Arc((bx, y - 0.6), 2.8, 1.8, theta1=180, theta2=360, ec=col, lw=lw, zorder=12))
        cv.line([(x - 1.6, y - 3.0), (x + 1.6, y - 3.0)], color=col, lw=lw)
    elif k == 2:
        cv.ax.add_patch(Circle((x, y), 3.3, fc="white", ec=col, lw=lw, zorder=11))
        cv.line([(x, y), (x, y + 2.2)], color=col, lw=lw, z=12)
        cv.line([(x, y), (x + 1.6, y - 0.9)], color=col, lw=lw, z=12)
    else:
        pts = [(x - 3.0, y + 2.4), (x, y + 3.4), (x + 3.0, y + 2.4), (x + 2.7, y - 0.8), (x, y - 3.4), (x - 2.7, y - 0.8)]
        cv.ax.add_patch(Polygon(pts, closed=True, fc="white", ec=col, lw=lw, zorder=12, joinstyle="round"))
        cv.text(x, y + 0.1, "!", size=9, color=col, weight="bold", z=13)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.6)
    # Arbitration chapter: tinted field, big title in its ink
    px, pw = 29.0, 121.0
    rbox(cv, px, 1.0, pw, H - 2.0, ARB["fill"], ARB["stroke"], 0.8, r=3.0, z=1)
    cv.text(px + pw / 2, H - 6.0, "Arbitration", size=15, weight="bold", color=ARB["ink"])
    cv.text(px + pw / 2, H - 11.2, "a worthwhile goal is not yet a warranted intervention", size=7.4,
            color=mix(ARB["ink"], "white", 0.15), style="italic")
    # gate rows
    gx, gw, rh, gap = px + 3.0, 86.0, 17.6, 2.4
    top = H - 15.0
    ys, pys = [], []
    for k, (title, q, fl, fb) in enumerate(GATES):
        y = top - (k + 1) * rh - k * gap
        ys.append(y + rh / 2)
        rbox(cv, gx, y, gw, rh, mix(ARB["soft"], "white", 0.45), ARB["stroke"], 0.6, r=2.0, z=4)
        glyph(cv, k, gx + 7.0, y + rh / 2 - 1.6, ARB["ink"])
        # solid numbered header tab
        tw = cv.text_width(title, 8.6, "bold") + 12.0
        rbox(cv, gx + 14.0, y + rh - 7.0, tw, 5.6, ARB["mark"], r=2.8, z=6)
        cv.ax.add_patch(Circle((gx + 17.2, y + rh - 4.2), 1.9, fc="white", ec="none", zorder=7))
        cv.text(gx + 17.2, y + rh - 4.25, str(k + 1), size=7.4, weight="bold", color=ARB["mark"], z=8)
        cv.text(gx + 20.4, y + rh - 4.2, title, size=8.6, weight="bold", color="white", ha="left", z=8)
        cv.text(gx + 14.6, y + 5.0, q, size=7.4, color=INK, ha="left", va="center", linespacing=1.1)
        # failure exit: solid chip beside the row, below the pass line (as in the source, but never crossed)
        fx, fw, fh = gx + gw + 4.4, 25.0, rh - 5.4
        rbox(cv, fx, y, fw, fh, FAIL["mark"], r=1.8, z=6)
        two = len(fl) >= 16
        cv.text(fx + fw / 2, y + fh - (3.0 if two else 2.3), fl.replace(" / ", " /\n") if two else fl,
                size=6.3 if two else 6.8, weight="bold", color="white", z=8, linespacing=1.0)
        cv.text(fx + fw / 2, y + (3.2 if two else 3.6), fb, size=6.4, color="white", z=8, linespacing=1.05)
        cv.arrow([(gx + gw, y + fh / 2), (fx - 0.3, y + fh / 2)], color=FAIL["mark"], lw=0.9, head=1.1)
        cv.text(gx + gw - 1.4, y + fh / 2 + 2.2, "FAIL", size=6.6, weight="bold", color=FAIL["mark"], ha="right")
        # pass exit along the top of the row, above the failure chip
        pys.append(y + rh - 2.4)
        cv.text(gx + gw - 1.4, y + rh - 2.4, "PASS", size=6.6, weight="bold", color=PASS["mark"], ha="right", z=8)
    # licence column (solid) = all four pass
    lx, lw_ = px + pw + 2.6, 14.4
    y0, y1 = 1.0, H - 1.0
    for y in pys:
        cv.arrow([(gx + gw, y), (lx - 0.3, y)], color=PASS["mark"], lw=1.0, head=1.3)
    rbox(cv, lx, y0, lw_, y1 - y0, PASS["mark"], r=2.4, z=5)
    mid = (ys[0] + ys[-1]) / 2
    cv.text(lx + lw_ / 2, mid + 8.0, "ALL\nFOUR\nPASS", size=8.6, weight="bold", color="white", linespacing=1.05)
    cv.line([(lx + 3.0, mid + 1.0), (lx + lw_ - 3.0, mid + 1.0)], color="white", lw=0.6)
    cv.text(lx + lw_ / 2, mid - 6.5, "licence\nto\nintervene", size=8.0, color="white", linespacing=1.1)
    # To Action tab, Action colour
    ax_ = lx + lw_ + 2.4
    cv.arrow([(lx + lw_, mid), (ax_ - 0.2, mid)], color=PASS["mark"], lw=1.1, head=1.3)
    rbox(cv, ax_, y0, W - ax_ - 1.0, y1 - y0, ACT["mark"], r=3.0, z=5)
    cv.text(ax_ + (W - ax_ - 1.0) / 2, mid, "To Action", size=11, weight="bold", color="white", rotation=-90)
    # candidate action from Agenda feeds every test
    cx, cw = 1.0, 21.0
    rbox(cv, cx, y0, cw, y1 - y0, AGD["mark"], r=2.4, z=5)
    cv.image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vignettes", "f1_agenda.jpg"), cx + cw / 2,
             mid + 14.0, cw - 2.4, fit="cover", h=24.0, radius=1.4, focus=(0.5, 0.42), zoom=1.15, z=6)
    cv.text(cx + cw / 2, mid - 4.0, "Candidate\naction", size=9.0, weight="bold", color="white", linespacing=1.05)
    cv.text(cx + cw / 2, mid - 11.4, "from Agenda", size=7.4, color="white")
    bus = px - 3.0
    cv.line([(cx + cw, mid), (bus, mid)], color=AGD["mark"], lw=1.0)
    cv.line([(bus, ys[-1]), (bus, ys[0])], color=AGD["mark"], lw=1.0)
    for y in ys:
        cv.arrow([(bus, y), (gx - 0.3, y)], color=AGD["mark"], lw=1.0, head=1.2)
    assert not cv.overlaps() and not cv.text_overlaps(), cv.overlaps() + cv.text_overlaps()
    print("\n".join(cv.save(os.path.join(a.out, "proactive_arbitration"))))


if __name__ == "__main__":
    main()
