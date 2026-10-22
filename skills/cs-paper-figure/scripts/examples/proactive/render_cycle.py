"""Redesign of Fig. 6 of "Proactive AI for Superintelligent Agents": six interacting capacities (the 6A).

Content from the source figure: Awareness -> Anticipation -> Agenda -> Arbitration -> Action in a loop,
Adaptation in the centre learning from outcomes and feeding every capacity; the household running example
(observations, predictions, candidate goals, the four arbitration checks, the chosen action, the updates).
The robot illustrations are replaced by the example's own items, drawn as chips in each capacity's colour.

    python render_cycle.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sixa import SIXA  # noqa: E402
from paperkit import Canvas, INK, MUTED  # noqa: E402

CARDS = {  # name: (k, role line, example items, (x, y, w, h))
    "Awareness": (1, "continuously monitor the situation",
                  ["Owner stressed", "Groceries low", "Dishwasher full", "Meeting at 6 PM", "Rain tonight"], (3, 56, 55, 37)),
    "Anticipation": (2, "predict future needs and outcomes",
                     ["Owner may work late", "Groceries will run out", "Dinner time approaching",
                      "Dishwasher will fill up", "Rain expected tonight"], (61.5, 56, 55, 37)),
    "Agenda": (3, "generate candidate goals to address gaps",
               ["Prepare dinner", "Order groceries", "Start dishwasher", "Close windows before rain",
                "Bring in laundry"], (120, 56, 55, 37)),
    "Arbitration": (4, "decide whether, when and how to act",
                    ["Enough confidence", "Worthwhile", "Good timing", "Safe & reversible"], (120, 3, 55, 41)),
    "Action": (5, "execute the chosen action appropriately", [], (3, 3, 55, 41)),
    "Adaptation": (6, "learn from outcomes and feedback",
                   ["Update knowledge", "Refine preferences", "Calibrate thresholds", "Improve actions"], (64, 15, 50, 29)),
}
W, H = 178, 96


def flow(cv, x, y, w, items, c, size=6.0, check=False):
    """Wrap chips left to right inside width w starting at the top-left (x, y)."""
    cx, cy, hh = x, y, size * 0.62
    for it in items:
        tw = cv.text_width(it, size) + 2.0 + (2.4 if check else 0)
        if cx + tw > x + w:
            cx, cy = x, cy - hh - 1.3
        cv.box(cx, cy - hh / 2, tw, hh, c, fill="white", lw=0.45, radius=hh / 2)
        if check:
            cv.icon_check(cx + 1.8, cy, 1.4, color=c["mark"], lw=0.7)
        cv.text(cx + tw / 2 + (1.2 if check else 0), cy, it, size=size, color=c["ink"])
        cx += tw + 1.2
    return cy


def card(cv, name):
    k, line, items, (x, y, w, h) = CARDS[name]
    c = SIXA[name]
    cv.group(x, y, w, h, c, "", band=False, lw=0.8, radius=2.2)
    cv.badge(x + 4.2, y + h - 4.2, k, c, d=4.0)
    cv.text(x + 7.6, y + h - 4.2, name, size=8.6, weight="bold", color=c["ink"], ha="left")
    cv.text(x + 3.0, y + h - 9.2, line, size=6.4, color=INK, ha="left", style="italic")
    return x, y, w, h, c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.0)
    boxes = {}
    for name in CARDS:
        x, y, w, h, c = card(cv, name)
        boxes[name] = (x, y, w, h)
        items = CARDS[name][2]
        if name == "Arbitration":
            flow(cv, x + 3.0, y + h - 14.4, w - 6.0, items, c, check=True)
            cv.text(x + 3.0, y + 13.4, "chosen", size=6.0, color=MUTED, style="italic", ha="left")
            cv.box(x + 3.0, y + 4.6, w - 6.0, 6.4, SIXA["Action"], fill="white", lw=0.6, radius=1.4)
            cv.text(x + w / 2, y + 7.8, "Prepare dinner now · others later", size=6.3,
                    weight="bold", color=SIXA["Action"]["ink"])
        elif name == "Action":
            cv.box(x + 3.0, y + 13.0, w - 6.0, 10.0, c, fill="white", lw=0.6, radius=1.6)
            cv.text(x + w / 2, y + 20.0, "Preparing dinner", size=7.2, weight="bold", color=c["ink"])
            cv.text(x + w / 2, y + 16.0, "suggest · assist · execute", size=6.0, color=MUTED, style="italic")
        else:
            flow(cv, x + 3.0, y + h - 14.4, w - 6.0, items, c)
    # the loop: 1 -> 2 -> 3 -> 4 -> 5 -> 1
    A, N, G, R, X = (boxes[n] for n in ("Awareness", "Anticipation", "Agenda", "Arbitration", "Action"))
    loop = dict(color="#4B5563", lw=1.1, head=1.5)
    cv.arrow([(A[0] + A[2], A[1] + A[3] / 2), (N[0], N[1] + N[3] / 2)], **loop)
    cv.arrow([(N[0] + N[2], N[1] + N[3] / 2), (G[0], G[1] + G[3] / 2)], **loop)
    cv.arrow([(G[0] + G[2] / 2, G[1]), (R[0] + R[2] / 2, R[1] + R[3])], **loop)
    cv.arrow([(R[0], R[1] + 4.0), (X[0] + X[2], X[1] + 4.0)], **loop)
    cv.arrow([(X[0] + X[2] / 2, X[1] + X[3]), (A[0] + A[2] / 2, A[1])], **loop)
    # Adaptation feeds every capacity (dashed, its own colour), routed through the channel between the rows
    D_ = boxes["Adaptation"]
    T = SIXA["Adaptation"]
    fb = dict(color=T["mark"], lw=0.7, head=1.1, dashed=True, radius=1.0)
    cx, top, ch = D_[0] + D_[2] / 2, D_[1] + D_[3], (A[1] + X[1] + X[3]) / 2
    cv.arrow([(cx, top), (cx, N[1])], **fb)
    cv.arrow([(cx - 14.0, top), (cx - 14.0, ch), (A[0] + A[2] - 7.0, ch), (A[0] + A[2] - 7.0, A[1])], **fb)
    cv.arrow([(cx + 14.0, top), (cx + 14.0, ch), (G[0] + 7.0, ch), (G[0] + 7.0, G[1])], **fb)
    cv.arrow([(D_[0] + D_[2], D_[1] + 9.0), (R[0], D_[1] + 9.0)], **fb)
    cv.arrow([(D_[0], D_[1] + 9.0), (X[0] + X[2], D_[1] + 9.0)], **fb)
    cv.text(cx, D_[1] - 2.6, "Adaptation updates every capacity", size=6.0, color=T["ink"], style="italic")
    print("\n".join(cv.save(os.path.join(a.out, "proactive_cycle"))))


if __name__ == "__main__":
    main()
