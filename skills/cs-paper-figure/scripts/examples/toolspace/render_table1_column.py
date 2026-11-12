#!/usr/bin/env python3
"""ToolSpace Table 1 as a single-column field chart (84 mm wide).

Source: ToolSpace, arXiv:2611.05036v1, Table 1 (p. 12): seven benchmark scores and the reported average
for each ToolSpace model, its backbone and two other models of the same scale. Values are imported from
render_fig1.py, which asserts them against the reported averages.

Register: line art; chart idiom: field chart (references/visual-craft.md §11).
  * Many systems x many conditions, so every series has two channels: hue and hatch. ToolSpace is index 0
    of paperkit.SERIES_STYLE, the only solid, unhatched bar, and first in each legend row.
  * No card, no header band. One y label for both panels, benchmark names on the bottom row only, one
    frameless legend row above each panel (the two scales compare different models).
  * The claim is the gain over the backbone: it is printed on the Average group, +12.0 and +18.0, computed
    from the table and asserted in render_fig1.py.
  * Check greyscale with `python paperkit.py grey toolspace_table1_column.png grey.png`.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperkit import Canvas, SERIES_STYLE, series_kw  # noqa: E402
from render_fig1 import BENCH, GAIN, SCALES, T1  # noqa: E402

STEM = "toolspace_table1_column"
SHORT = {"AutomationBench": "Automation\nBench", "SkillsBench": "Skills\nBench", "JobBench": "Job\nBench",
         "τ³-Bench Banking": "τ³-Bench\nBanking", "BFCL V4": "BFCL\nV4", "Harvey LAB": "Harvey\nLAB",
         "OfficeQA Pro": "OfficeQA\nPro"}
MARK = ("", "\u2020", "", "")   # position in SCALES: hero, its backbone (dagger), two others


def build():
    cv = Canvas(84, 63.5, family="serif", size=6.3)   # ticks 5.8 pt; labels and legend 5.8 pt; the gain 6.6 pt
    X, Y, W, H, VG = 9.5, 11.0, 73.5, 44.0, 8.5
    axs = cv.axes_grid(X, Y, W, H, 2, 1, gap=(0, VG), box=False, grid="y")
    cv.text(2.2, Y + H / 2, "score", size=5.8, rotation=90)
    groups = [SHORT[b] for b in BENCH] + ["Average"]
    bw, ph = 0.2, (H - VG) / 2
    for row, ((ax,), models, gain) in enumerate(zip(axs, SCALES, GAIN)):
        hs = []
        for k, m in enumerate(models):
            vals = T1[m][0] + [T1[m][1]]
            hs.append(ax.bar([g + (k - 1.5) * bw for g in range(len(groups))], vals, bw, zorder=3,
                             **series_kw(k, "bar")))
        ax.set_xlim(-0.55, len(groups) - 0.45)
        ax.set_ylim(0, 85)
        ax.set_yticks([0, 20, 40, 60, 80])
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels(groups, fontsize=5.8, linespacing=0.95)
        ax.tick_params(axis="x", length=0, pad=1.5)
        ax.axvline(len(groups) - 1.5, color="#9AA0A8", lw=0.5, ls=(0, (2, 2)))     # the average is not a benchmark
        hero, base = T1[models[0]][1], T1[models[1]][1]
        assert abs((hero - base) - gain) < 0.05
        x0, x1, top = len(groups) - 1 - 1.5 * bw, len(groups) - 1 - 0.5 * bw, hero + 5.0
        ax.plot([x0, x0, x1, x1], [hero + 1.5, top, top, base + 1.5], color="black", lw=0.6, zorder=4,
                solid_joinstyle="miter")                                            # gain = ours minus its backbone
        ax.text(len(groups) - 1, top + 1.5, f"+{gain:.1f}", fontsize=6.6, weight="bold", ha="center", va="bottom",
                color=SERIES_STYLE[0]["color"])
        cv.chart_legend(hs, [m + d for m, d in zip(models, MARK)], X - 0.3, Y + (1 - row) * (ph + VG) + ph + 0.7,
                        loc="lower left", ncol=2, size=5.8, handlelength=1.6, handleheight=0.9, columnspacing=2.0,
                        labelspacing=0.25)
    axs[0][0].tick_params(labelbottom=False)
    cv.text(83.0, 1.6, "\u2020 backbone of the ToolSpace model; bracket: gain over \u2020", size=5.8, ha="right",
            style="italic", color="#5A626D")
    assert not cv.overlaps() and not cv.text_overlaps() and not cv.wire_crossings(), cv.text_overlaps()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/toolspace")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
