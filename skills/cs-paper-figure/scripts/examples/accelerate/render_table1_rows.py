#!/usr/bin/env python3
"""Accelerate Bench Table 1 as row-aligned measure panels (170 x 70 mm, full width).

Source: Liu et al., "Accelerate Bench: Evaluating Agents for Application-Level Program Optimization",
arXiv:2611.20882, Table 1 (p. 7): Score@1, geometric-mean speedup and the share of the 32 tasks on which
each of 16 agents is correct and at least 1.25x / 2x faster. All 64 values are transcribed from the
table; the vendor marks are cropped from the same table and stay the property of their owners.

Family: leaderboard as row-aligned measure panels (references/visual-craft.md section 11;
references/trending-study-2026-11.md). Model: assets/models/chart_measure_rows.png.
  * Message: two agents are ahead of a packed field, and what separates agents is how often they reach
    2x, not whether they reach 1.25x.
  * The picture: sixteen rows, named once at the left with the vendor's mark; three measures as three
    panels on those rows, each with the mark that suits it (bar from zero, dumbbell between two
    thresholds, lollipop from the 1x reference). Nothing is rotated and there is no legend.
  * Hero by difference: the two agents the paper's paired bootstrap separates from the field take the
    one hue in every panel; the other fourteen are grey. The bracket says, in the paper's words, that
    their order is not established, which a sorted bar chart otherwise claims by itself.
  * The dumbbell's key is two labels over its first row. Maxima are bold, as in the source table.
  * Type: Times/STIX at 8.2 pt (heads), 7.2 pt (names, values), 6.2 pt (ticks, notes). Strokes: 0.6 pt
    hairlines (axes, grid, bracket) and 1.4 pt (bars' stems and dumbbell links).

    python render_table1_rows.py --out DIR
"""
import argparse
import os
import sys

from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from paperkit import Canvas  # noqa: E402

STEM = "accelerate_table1_rows"
# agent, harness, Score@1 (%), geometric-mean speedup (x), A_1.25 (%), A_2 (%)
T1 = [
    ("Claude Sonnet 5.5", "Claude Code", 67.4, 3.83, 100.0, 71.9),
    ("Claude Opus 5.5", "Claude Code", 59.4, 3.94, 84.4, 68.8),
    ("GPT-6.1 Sol", "Codex", 49.2, 2.42, 78.1, 50.0),
    ("GPT-6 Astra", "Codex", 47.2, 2.40, 75.0, 53.1),
    ("Hy4-Preview", "Claude Code", 45.2, 2.31, 71.9, 50.0),
    ("Hy4", "Claude Code", 45.0, 2.41, 75.0, 46.9),
    ("Kimi K3", "Claude Code", 42.5, 2.47, 68.8, 40.6),
    ("DeepSeek-V4.1-Flash-1017", "Claude Code", 40.1, 2.28, 65.6, 34.4),
    ("GLM-5.3", "Claude Code", 39.7, 2.20, 65.6, 40.6),
    ("GLM-5.3-Flash", "Claude Code", 39.3, 2.20, 68.8, 34.4),
    ("DeepSeek-V4-Pro", "Claude Code", 37.9, 2.19, 62.5, 34.4),
    ("GPT-6.1 Terra", "Codex", 37.9, 1.92, 75.0, 25.0),
    ("DeepSeek-V4-Flash", "Claude Code", 34.1, 1.92, 56.2, 34.4),
    ("GLM-5.2", "Claude Code", 34.0, 1.98, 46.9, 37.5),
    ("Grok 4.6", "Claude Code", 33.9, 2.13, 50.0, 34.4),
    ("Hy3", "Claude Code", 25.5, 1.76, 37.5, 28.1),
]
MARK = {"Claude": "claude", "GPT": "openai", "Hy": "hy", "Kimi": "kimi", "DeepSeek": "deepseek", "GLM": "zai",
        "Grok": "grok"}
LEADERS = 2            # separated from every later agent by the paper's paired task bootstrap (p. 6)
HEAD, LABEL, FINE = 8.2, 7.2, 6.2
HAIR, LINK = 0.6, 1.4
ACC, ACC_PALE = "#2F6FC0", "#9DBCE6"
FIELD, FIELD_PALE, FIELD_BAR = "#5E6875", "#B4BBC5", "#A9B1BC"
NOTE = "#4A5059"          # secondary text that still has to be read at 170 mm

assert len(T1) == 16 and [r[2] for r in T1] == sorted((r[2] for r in T1), reverse=True)
assert all(r[4] >= r[5] for r in T1)                      # reaching 2x implies reaching 1.25x
BEST = [max(r[k] for r in T1) for k in (2, 3, 4)]
assert BEST == [67.4, 3.94, 100.0]


def vendor(name):
    return next(v for k, v in MARK.items() if name.startswith(k))


def build():
    n = len(T1)
    cv = Canvas(170, 70, family="serif", size=LABEL)
    X, Y, W, H = 45.0, 6.0, 122.0, 53.5
    axs, row_y = cv.row_panels(X, Y, W, H, n, widths=[45, 42, 29], gap=6.0,
                               xlims=[(0, 118), (0, 120), (1, 4.75)], size=FINE + 0.5)
    pitch = H / n
    for i in range(1, n, 2):                               # row guides: the eye crosses 120 mm of panels
        cv.ax.add_patch(Rectangle((1.0, row_y(i) - pitch / 2), 168.0, pitch, fc="#F4F5F7", ec="none", zorder=0))

    for i, (name, harness, *_rest) in enumerate(T1):
        cv.image(os.path.join(HERE, "logos", vendor(name) + ".png"), 3.2, row_y(i), 2.5)
        cv.text(5.6, row_y(i), name, size=LABEL, ha="left", color="black")
        if harness == "Codex":
            cv.text(5.6 + cv.text_width(name, LABEL) + 1.2, row_y(i), "Codex", size=FINE, ha="left", color=NOTE,
                    style="italic")
    cv.text(5.6, Y - 3.4, "Harness: Claude Code unless marked", size=FINE, ha="left", color=NOTE, style="italic")

    a, b, c = axs
    top = Y + H + 8.2
    for ax, letter, title in zip(axs, "abc", ("Score@1 (%)", "Correct and faster (%)",
                                              "Geo-mean speedup (\u00d7)")):
        cv.head(ax.get_position().x0 * cv.w, top, letter, title, size=HEAD)

    for i, (_n, _h, score, gm, a125, a2) in enumerate(T1):
        lead = i < LEADERS
        ink, pale = (ACC, ACC_PALE) if lead else (FIELD, FIELD_PALE)
        a.barh(i, score, height=0.62, color=ACC if lead else FIELD_BAR, zorder=3)
        a.text(score + 1.4, i, f"{score:.1f}", fontsize=LABEL, va="center", ha="left", color="black",
               weight="bold" if score == BEST[0] else "normal")
        b.plot([a2, a125], [i, i], color=pale, lw=LINK, solid_capstyle="butt", zorder=2)
        b.plot([a2], [i], "o", ms=3.4, mfc="white", mec=ink, mew=0.9, zorder=3)
        b.plot([a125], [i], "o", ms=3.4, mfc=ink, mec=ink, mew=0.9, zorder=3)
        b.text(a125 + 4.0, i, f"{a125:.0f}", fontsize=LABEL, va="center", ha="left", color="black",
               weight="bold" if a125 == BEST[2] else "normal")
        b.text(a2 - 4.0, i, f"{a2:.0f}", fontsize=LABEL, va="center", ha="right", color=NOTE)
        c.plot([1, gm], [i, i], color=pale, lw=LINK, solid_capstyle="butt", zorder=2)
        c.plot([gm], [i], "o", ms=3.4, mfc=ink, mec=ink, mew=0.9, zorder=3)
        c.text(gm + 0.17, i, f"{gm:.2f}", fontsize=LABEL, va="center", ha="left", color="black",
               weight="bold" if gm == BEST[1] else "normal")

    a.set_xticks([0, 25, 50, 75])
    b.set_xticks([0, 25, 50, 75, 100])
    c.set_xticks([1, 2, 3, 4])
    c.set_xticklabels(["1×", "2×", "3×", "4×"])
    # the dumbbell's key: two labels over its first row, in the first row's ink
    b.text(T1[0][5], -0.95, "≥ 2×", fontsize=FINE, ha="center", va="center", color=ACC, clip_on=False)
    b.text(T1[0][4], -0.95, "≥ 1.25×", fontsize=FINE, ha="center", va="center", color=ACC, clip_on=False)
    # what a sorted leaderboard cannot say by itself: which gaps are established
    bx = 88.0
    for r0, r1, ink, note in ((0, LEADERS - 1, ACC, "ahead of every\nlater agent"),
                              (LEADERS, n - 1, FIELD, "adjacent ranks\nnot separated\n(paired bootstrap)")):
        a.plot([bx - 1.5, bx, bx, bx - 1.5], [r0 - 0.3, r0 - 0.3, r1 + 0.3, r1 + 0.3], color=ink, lw=HAIR,
               solid_joinstyle="miter", zorder=4)
        a.text(bx + 2.2, (r0 + r1) / 2, note, fontsize=FINE, style="italic", color=ink, ha="left", va="center",
               linespacing=1.15)
    for ax, lo, hi in ((a, 0, 75), (b, 0, 100), (c, 1, 4)):     # the axis line ends where the scale does
        ax.spines["bottom"].set_bounds(lo, hi)
        ax.tick_params(labelcolor=NOTE)
    assert not cv.overlaps() and not cv.text_overlaps() and not cv.wire_crossings(), cv.text_overlaps()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/accelerate")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
