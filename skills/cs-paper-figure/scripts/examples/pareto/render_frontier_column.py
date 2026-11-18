#!/usr/bin/env python3
"""Quality against cost with the Pareto front drawn, one column (84 x 66 mm).

The numbers are SYNTHETIC: four learning harnesses on four models, made up to show the family. The figure
says so inside the plot. Devices are taken from ServeLearnBench Fig. 1 (arXiv:2610.07792) and its flaws
are left out (references/trending-study-2026-11.md).

Family: quality-cost scatter (references/visual-craft.md section 11).
Model: assets/models/chart_pareto_column.png.
  * Message: four of the six points on the front are ours, at every budget from under a cent up.
  * The picture: every harness-model pair is a point; the front is a step line with the region it
    dominates shaded; the points on it are full size and named in place; the dominated ones are the same
    marks, smaller and faded. An arrow in the empty corner says which way is better; the front is named
    on the line.
  * Two factors, two channels, two small legends: hue is the harness, marker shape is the model, and the
    shape key is drawn in grey so it claims no hue; the hue key is a short bar, because a square swatch
    would read as one of the model markers. Both keys sit on one column grid.
  * A step line, not a diagonal: between two points on the front no cheaper option reaches the higher
    reward, so the front is flat until the next point.
  * Type: Times/STIX at 7.0 pt (labels, legends) and 6.0 pt (ticks, notes). Strokes: 0.6 pt hairlines and
    1.1 pt for the front.

    python render_frontier_column.py --out DIR
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import MUTED, SERIES_STYLE, Canvas, pareto_front  # noqa: E402

STEM = "pareto_frontier_column"
STATUS = "SYNTHETIC DATA"
MODELS = {"S": "o", "B": "s", "L": "^", "XL": "D"}
# harness -> model -> (cost in USD per task, reward in %)
DATA = {
    "Replay": {"S": (0.0032, 30.5), "B": (0.0105, 38.0), "L": (0.041, 44.5), "XL": (0.150, 47.0)},
    "Notes":  {"S": (0.0046, 36.5), "B": (0.0170, 41.0), "L": (0.062, 50.5), "XL": (0.210, 52.0)},
    "Skills": {"S": (0.0061, 33.0), "B": (0.0240, 46.5), "L": (0.088, 55.0), "XL": (0.330, 61.5)},
    "Ours":   {"S": (0.0088, 52.5), "B": (0.0300, 61.0), "L": (0.105, 70.5), "XL": (0.270, 73.5)},
}
HUE = {"Ours": SERIES_STYLE[0]["color"], "Skills": SERIES_STYLE[1]["color"], "Notes": SERIES_STYLE[2]["color"],
       "Replay": SERIES_STYLE[3]["color"]}
LABEL, FINE = 7.0, 6.0
HAIR, FRONT = 0.6, 1.1
INK = "#30363F"


def build():
    cv = Canvas(84, 66, family="serif", size=LABEL)
    ax = cv.axes(10.5, 17.5, 71.0, 45.5)
    pts = [(h, m, c, r) for h, row in DATA.items() for m, (c, r) in row.items()]
    front = pareto_front([p[2] for p in pts], [p[3] for p in pts])
    assert [pts[i][0] for i in front].count("Ours") >= 3      # the message the head and the caption state
    ax.set_xscale("log")
    x_hi, y_lo = 0.5, 22
    ax.set_xlim(0.0011, x_hi)
    ax.set_ylim(y_lo, 80)

    # the front as a step, and the region it dominates
    fx = [pts[i][2] for i in front] + [x_hi]
    fy = [pts[i][3] for i in front]
    sx, sy = [fx[0]], [y_lo]
    for k, y in enumerate(fy):
        sx += [fx[k], fx[k + 1]]
        sy += [y, y]
    ax.fill_between(sx, sy, y_lo, color="#EEF0F3", lw=0, zorder=1)
    ax.plot(sx[1:], sy[1:], color=INK, lw=FRONT, zorder=3, solid_joinstyle="miter")
    ax.text((fx[3] * fx[4]) ** 0.5, fy[3] + 0.9, "Pareto front", fontsize=FINE, style="italic", color=INK,
            ha="center", va="bottom")                         # named on its longest flat segment

    on = set(front)
    for i, (h, m, c, r) in enumerate(pts):
        if i in on:
            ax.plot([c], [r], MODELS[m], ms=5.6, mfc=HUE[h], mec=INK, mew=0.8, zorder=5)
        else:
            ax.plot([c], [r], MODELS[m], ms=3.6, mfc=HUE[h], mec="none", alpha=0.45, zorder=4)
    for k, i in enumerate(front):                             # names on the front, on its open side
        h, m, c, r = pts[i]
        off, ha, va = ((-5.0, 0.0), "right", "center") if k < 2 else ((-4.6, 4.0), "right", "bottom")
        ax.annotate(f"{h} · {m}", (c, r), xytext=off, textcoords="offset points", fontsize=LABEL,
                    ha=ha, va=va, color="black", weight="bold" if h == "Ours" else "normal", zorder=6)

    ax.annotate("", xy=(0.00135, 77.0), xytext=(0.0021, 72.0),
                arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.22", color=MUTED, lw=HAIR))
    ax.text(0.0023, 71.6, "better", fontsize=FINE, style="italic", color=MUTED, ha="left", va="center")
    ax.text(0.455, 23.6, "dominated", fontsize=FINE, style="italic", color=MUTED, ha="right", va="bottom")
    ax.set_xticks([0.003, 0.01, 0.03, 0.1, 0.3])
    ax.set_xticklabels(["0.003", "0.01", "0.03", "0.1", "0.3"])
    ax.minorticks_off()
    ax.set_yticks([30, 40, 50, 60, 70])
    ax.grid(axis="both", color="#E3E6EA", lw=0.5, zorder=0)
    ax.tick_params(labelsize=FINE)
    ax.set_xlabel("API cost per task, USD (log scale)", fontsize=LABEL, labelpad=1.5)
    cv.text(2.4, 17.5 + 45.5 / 2, "Reward on hidden cases (%)", size=LABEL, rotation=90, color="black")

    # two keys on one column grid: hue as a short bar (a square would read as the model "B"), shape in grey
    for k, h in enumerate(("Ours", "Skills", "Notes", "Replay")):
        x = 22.0 + 13.0 * k
        cv.ax.plot([x, x + 3.0], [6.5, 6.5], color=HUE[h], lw=2.4, solid_capstyle="butt", zorder=5)
        cv.text(x + 4.0, 6.5, h, size=LABEL, ha="left", color="black", weight="bold" if h == "Ours" else "normal")
    for k, (m, mk) in enumerate(MODELS.items()):
        x = 22.0 + 13.0 * k
        cv.ax.plot([x + 1.5], [2.5], mk, ms=4.0, mfc="#8E99A8", mec="none", zorder=5)
        cv.text(x + 4.0, 2.5, m, size=LABEL, ha="left", color="black")
    cv.text(10.5, 6.5, "harness", size=FINE, ha="left", color=MUTED, style="italic")
    cv.text(10.5, 2.5, "model", size=FINE, ha="left", color=MUTED, style="italic")
    cv.text(81.5, 64.6, STATUS, size=FINE, ha="right", color=MUTED)
    assert not cv.overlaps() and not cv.text_overlaps() and not cv.wire_crossings(), cv.text_overlaps()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/pareto")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
