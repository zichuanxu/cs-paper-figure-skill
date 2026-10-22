"""Redesign of Fig. 5 of PaperBanana (arXiv 2601.23265): code vs. image generation for statistical plots.

Data (as printed, win rate against human-made plots, %): Faithfulness 45.4 / 39.6, Conciseness 62.3 /
55.0, Readability 51.3 / 57.1, Aesthetic 54.4 / 62.4, Overall 56.0 / 56.8 (code / image). The source uses
grouped bars on an axis starting at 30, which inflates the gaps, and a dashed line for the human level.

Redesign: a dumbbell per dimension on a win-rate axis centred on human parity (50 %), the gap labelled
in points, and the side of parity shaded, so the two findings read at once: code wins faithfulness and
conciseness, image generation wins readability and aesthetics, and only faithfulness is below parity.

    python render_fig5.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import Canvas, INK, MUTED  # noqa: E402

DATA = [("Faithfulness", 45.4, 39.6), ("Conciseness", 62.3, 55.0), ("Readability", 51.3, 57.1),
        ("Aesthetic", 54.4, 62.4), ("Overall", 56.0, 56.8)]
CODE, IMG = "#2F6FC0", "#D9583B"
W, H = 88, 62


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    for name, c, i in DATA:  # the figure's claims, checked against the data
        assert 30 <= min(c, i) and max(c, i) <= 70
    assert [n for n, c, i in DATA if min(c, i) < 50] == ["Faithfulness"]
    cv = Canvas(W, H, family="sans", size=7.0)
    ax = cv.axes(24.0, 9.0, 60.0, 44.0)
    ax.set_xlim(35, 67)
    ax.set_ylim(-0.6, len(DATA) - 0.4)
    ax.axvspan(35, 50, color="#F4F5F7", zorder=0, lw=0)
    ax.axvline(50, color="#6B7280", lw=0.8, zorder=1)
    ax.text(50, len(DATA) - 0.25, "human parity", ha="center", va="bottom", fontsize=6.2, color="#4B5563")
    ax.text(35.6, -0.52, "worse than human", ha="left", va="bottom", fontsize=5.9, color=MUTED, style="italic")
    ax.text(66.4, -0.52, "better than human", ha="right", va="bottom", fontsize=5.9, color=MUTED, style="italic")
    for k, (name, c, i) in enumerate(DATA[::-1]):
        y = k
        bold = name == "Overall"
        ax.plot([c, i], [y, y], color="#C3C8D0", lw=2.2, zorder=2, solid_capstyle="round")
        ax.scatter([c], [y], s=26, color=CODE, zorder=4, edgecolors="white", linewidths=0.6)
        ax.scatter([i], [y], s=26, color=IMG, zorder=4, edgecolors="white", linewidths=0.6)
        for v, col in ((c, CODE), (i, IMG)):
            left = v < max(c, i)
            ax.text(v + (-0.9 if left else 0.9), y, f"{v:.1f}", ha="right" if left else "left", va="center",
                    fontsize=6.2, color=col, weight="bold" if bold else "normal", zorder=5,
                    bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none") if abs(v - 50) < 4 else None)
        gap = abs(c - i)
        ax.text((c + i) / 2, y + 0.24, f"Δ {gap:.1f}", ha="center", va="bottom", fontsize=5.8, color=MUTED)
        ax.text(34.4, y, name, ha="right", va="center", fontsize=7.0, color=INK, weight="bold" if bold else "normal",
                clip_on=False)
    ax.set_yticks([])
    ax.set_xticks([40, 45, 50, 55, 60, 65])
    ax.tick_params(axis="x", labelsize=6.2, colors="#4B5563", length=2)
    for sp in ("left", "right", "top"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#9AA1AB")
    ax.set_xlabel("win rate vs. human-made plots (%)", fontsize=6.6, color="#4B5563", labelpad=2)
    ax.grid(False)
    # direct legend in the title line
    cv.text(4.0, H - 3.4, "Plot generation:", size=7.2, weight="bold", color=INK, ha="left")
    cv.dot(29.6, H - 3.4, color=CODE, d=1.8)
    cv.text(31.2, H - 3.4, "write plotting code", size=7.0, color=CODE, ha="left", weight="bold")
    cv.dot(58.0, H - 3.4, color=IMG, d=1.8)
    cv.text(59.6, H - 3.4, "generate the image", size=7.0, color=IMG, ha="left", weight="bold")
    print("\n".join(cv.save(os.path.join(a.out, "paperbanana_fig5"))))


if __name__ == "__main__":
    main()
