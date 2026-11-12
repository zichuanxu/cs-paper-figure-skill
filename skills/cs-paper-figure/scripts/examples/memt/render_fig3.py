"""MemT-1.0 Figure 3: inference efficiency and storage overhead of MemT-1.0-Nano.

Source: Li et al., "MemT-1.0: Towards Memory-Native Evolution", arXiv:2610.26825v2, Figure 3
(values read from the figure; the speed-ups agree with the 1.86x and 3.99x stated in Section 6.5).

Content kept from the source
  * End-to-end latency in seconds (history preparation + a 128-token response) of Full Context,
    Temp-LoRA and MemT-1.0-Nano at 128K and 256K tokens of history: all six values.
  * Per-trajectory storage at 256K: Full Context 5.061 GiB, Temp-LoRA 172.5 MiB, MemT-1.0-Nano
    40.00 MiB; the last two are the same at 1M, Full Context at 1M is reported only as too large.

Design decisions
  * (a) is one slope chart on a log axis instead of two bar panels. Bars on a log axis start at an
    arbitrary floor, so their length means nothing; dots do not have that problem, and joining the two
    history lengths shows how each method scales. The gap to Full Context is shaded, so the reader sees
    it open from 1.86x to 3.99x, and each line carries its own growth factor for the doubling.
  * (b) is area-true: one cell is the 40 MiB state of MemT-1.0-Nano, so Full Context is a block of
    130 cells, Temp-LoRA 4.3 cells and Nano one cell. A log bar hid exactly this difference. The dashed
    cells after the block say that the Full Context state keeps growing; no size is drawn for 1M.
  * One colour per method in both panels: blue is MemT-1.0-Nano, the two greys are the baselines.
    Methods are labelled on their marks, so there is no legend.
  * Every ratio printed is computed below from the transcribed values and asserted.
  * Printed values are rounded for reading (16.19 -> 16.2, 1400.88 -> 1,401, 5.061 GiB -> 5.06 GiB);
    the exact values are in LATENCY and STORAGE and the rounding is asserted to stay within 0.4 %.
"""
import argparse
import math
import os
import sys

from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import INK, MUTED, ROLE, Canvas, mix  # noqa: E402

STEM = "memt_fig3_efficiency"
NANO, FULL, LORA = "MemT-1.0-Nano", "Full Context", "Temp-LoRA"

# ---------------------------------------------------------------- data (reported) ---
LATENCY = {  # seconds, history preparation + 128-token response; key = history length in K tokens
    LORA: {128: 700.82, 256: 1400.88},
    FULL: {128: 30.07, 256: 94.47},
    NANO: {128: 16.19, 256: 23.69},
}
STORAGE = {FULL: 5.061 * 1024, LORA: 172.5, NANO: 40.00}  # MiB per trajectory at 256K history
STORAGE_LABEL = {FULL: "5.06 GiB", LORA: "172.5 MiB", NANO: "40.0 MiB"}
STORAGE_AT = {FULL: "at 256K", LORA: "at 256K and 1M", NANO: "at 256K and 1M"}

# ---------------------------------------------------------------- derived, asserted ---
SPEEDUP = {k: LATENCY[FULL][k] / LATENCY[NANO][k] for k in (128, 256)}
GROWTH = {m: v[256] / v[128] for m, v in LATENCY.items()}
CELLS = {m: v / STORAGE[NANO] for m, v in STORAGE.items()}  # state size in units of Nano's state
assert f"{SPEEDUP[128]:.2f}" == "1.86" and f"{SPEEDUP[256]:.2f}" == "3.99", SPEEDUP  # as stated in Sec. 6.5
assert [f"{GROWTH[m]:.2f}" for m in (NANO, FULL, LORA)] == ["1.46", "3.14", "2.00"], GROWTH
assert GROWTH[NANO] < GROWTH[LORA] < GROWTH[FULL]
assert f"{CELLS[FULL]:.0f}" == "130" and f"{CELLS[LORA]:.1f}" == "4.3" and CELLS[NANO] == 1.0, CELLS
assert abs(float(STORAGE_LABEL[FULL].split()[0]) * 1024 - STORAGE[FULL]) / STORAGE[FULL] < 0.002

BLUE = ROLE["blue"]
COL = {NANO: BLUE["mark"], FULL: "#5E6875", LORA: "#8E99A8"}   # marks
TXT = {NANO: BLUE["ink"], FULL: "#414A56", LORA: "#667182"}    # labels on those marks
T, B, A, HERO = 8.0, 7.0, 6.2, 11.0   # title, body, annotation, hero numeral (pt)


def secs(v):
    """Seconds as printed on the chart: one decimal below 100 s, whole seconds above."""
    return f"{v:.1f}" if v < 100 else f"{v:,.0f}"


for _m, _v in LATENCY.items():  # the printed value stays within 0.4 % of the reported one
    for _k, _x in _v.items():
        assert abs(float(secs(_x).replace(",", "")) - _x) / _x < 4e-3, (_m, _k)


def run(cv, x, y, segs, ha="left"):
    """One line of mixed-size text: segs = [(text, colour, size, weight, style)]. Returns the end x."""
    ws = [cv.text_width(s, size, weight) for s, _, size, weight, _ in segs]
    x -= sum(ws) if ha == "right" else 0
    for (s, col, size, weight, style), w in zip(segs, ws):
        cv.text(x, y, s, size=size, color=col, weight=weight, style=style, ha="left", va="baseline")
        x += w
    return x


def pill(cv, x, y, s):
    """The hero method's name: white bold on solid blue, left edge x, text baseline y. Returns the end x."""
    w = cv.text_width(s, B, "bold") + 2.6
    cv.ax.add_patch(FancyBboxPatch((x, y - 1.05), w, 3.5, boxstyle="round,pad=0,rounding_size=1.0",
                                   fc=BLUE["mark"], ec="none", zorder=6))
    cv.text(x + 1.3, y, s, size=B, color="white", weight="bold", ha="left", va="baseline")
    return x + w


def card(cv, x, y, w, h, letter, title, sub):
    cv.group(x, y, w, h, "neutral", f"({letter})  {title}", band=True, size=T, fill="white", stroke="#B4BBC5")
    cv.text(x + 2.0, y + h - T * 0.62 - 2.9, sub, size=A, color=MUTED, style="italic", ha="left")


def latency_panel(cv, x, y, w, h):
    card(cv, x, y, w, h, "a", "End-to-end latency",
         "history preparation + 128-token response; seconds, log scale")
    ax0, x1, x2 = x + 12.6, x + 30.5, x + 63.0
    yb, yt, lo, hi = y + 12.4, y + h - 11.8, 10.0, 2000.0
    k = (yt - yb) / (math.log10(hi) - math.log10(lo))

    def Y(v):
        return yb + (math.log10(v) - math.log10(lo)) * k

    # frame: decade grid, labelled; 3x minor lines, unlabelled
    for v, major in ((10, 1), (30, 0), (100, 1), (300, 0), (1000, 1)):
        cv.ax.plot([ax0, x2 + 2.0], [Y(v)] * 2, color="#E3E6EA" if major else "#EFF1F4", lw=0.5, zorder=2)
        if major:
            cv.text(ax0 - 1.2, Y(v), f"{v:,}", size=A, color="#5A626D", ha="right")
    cv.ax.plot([ax0, ax0], [yb, yt], color="#9AA0A8", lw=0.6, zorder=3)
    cv.text(x + 3.2, (yb + yt) / 2, "latency (s)", size=A, color="#5A626D", rotation=90)
    for xx, lab in ((x1, "128K"), (x2, "256K")):
        cv.ax.plot([xx, xx], [yb - 1.0, yt], color="#E3E6EA", lw=0.5, zorder=2)
        cv.text(xx, yb - 3.2, lab, size=B, color=INK, weight="bold")
    cv.arrow([(x1 + 5.2, yb - 3.2), (x2 - 5.2, yb - 3.2)], color="#9AA0A8", lw=0.6, head=1.2)
    cv.text((x1 + x2) / 2, yb - 3.2, "×2", size=A, color="#5A626D",
            bbox=dict(fc="white", ec="none", pad=1.2))
    cv.text((x1 + x2) / 2, yb - 7.4, "history length (tokens)", size=A, color="#5A626D")

    # hero: the gap between Full Context and Nano, opening with history
    yn, yf = [Y(LATENCY[NANO][c]) for c in (128, 256)], [Y(LATENCY[FULL][c]) for c in (128, 256)]
    cv.ax.add_patch(Polygon([(x1, yn[0]), (x2, yn[1]), (x2, yf[1]), (x1, yf[0])], closed=True,
                            fc=mix(BLUE["soft"], "#FFFFFF", 0.25), ec="none", zorder=3))

    def between(xx):  # mid-height of the gap at xx
        t = (xx - x1) / (x2 - x1)
        return (yn[0] + (yn[1] - yn[0]) * t + yf[0] + (yf[1] - yf[0]) * t) / 2

    cv.text(x1 + 2.6, between(x1 + 6.5), f"{SPEEDUP[128]:.2f}×", size=T, weight="bold", color=BLUE["mark"],
            ha="left")
    cv.text(x2 - 2.6, between(x2 - 7.5), f"{SPEEDUP[256]:.2f}×", size=HERO, weight="bold",
            color=BLUE["mark"], ha="right")

    for m in (LORA, FULL, NANO):
        hero = m == NANO
        ys = [Y(LATENCY[m][c]) for c in (128, 256)]
        cv.ax.plot([x1, x2], ys, color=COL[m], lw=1.9 if hero else 1.0, zorder=5 + hero,
                   solid_capstyle="round")
        for xx, yy in zip((x1, x2), ys):
            cv.ax.add_patch(Circle((xx, yy), 1.1 if hero else 0.85, fc=COL[m], ec="white", lw=0.7,
                                   zorder=7 + hero))
        w8 = "bold" if hero else "normal"
        cv.text(x1 - 2.4, ys[0], secs(LATENCY[m][128]), size=B, color=TXT[m], weight=w8, ha="right")
        if hero:
            pill(cv, x2 + 2.6, ys[1] + 1.0, m)
        else:
            cv.text(x2 + 2.6, ys[1] + 1.45, m, size=B, color=TXT[m], weight="bold", ha="left")
        cv.text(x2 + 2.6, ys[1] - (2.2 if hero else 1.45), secs(LATENCY[m][256]) + " s", size=B, color=TXT[m],
                weight=w8, ha="left")
        # growth for the doubling, at mid-line on the side away from the shaded gap
        side = 1 if m == FULL else -1
        cv.text((x1 + x2) / 2 - 2.0 * side, (ys[0] + ys[1]) / 2 + (2.7 if m == FULL else -2.4),
                f"×{GROWTH[m]:.2f}", size=A, color=TXT[m], style="italic", weight=w8)

    # reading key in the empty band between the baselines
    ky = (Y(100) + Y(300)) / 2
    assert LATENCY[FULL][256] < 100 and LATENCY[LORA][128] > 300
    kx = x1 + 3.4
    cv.ax.add_patch(Rectangle((kx, ky + 0.75), 2.6, 1.7, fc=mix(BLUE["soft"], "#FFFFFF", 0.25), ec="none", zorder=4))
    cv.text(kx + 3.6, ky + 1.6, "speed-up vs. Full Context", size=A, color=MUTED, style="italic", ha="left")
    cv.text(kx + 1.3, ky - 1.6, "×k", size=A, color=MUTED, style="italic")
    cv.text(kx + 3.6, ky - 1.6, "growth from 128K to 256K", size=A, color=MUTED, style="italic", ha="left")


def cells(cv, x, ytop, n, cols, rows, pitch, colour, by="col"):
    """n unit cells (fractional), filled column by column from the bottom-left (or along one row)."""
    s, g = pitch - 0.4, 0.4
    full, frac = int(n), n - int(n)
    for i in range(full + (frac > 1e-9)):
        c, r = (i // rows, i % rows) if by == "col" else (i, 0)
        px, py = x + c * pitch, ytop - rows * pitch + g + r * pitch
        f = 1.0 if i < full else frac
        if f < 1.0:  # the outline is the whole cell, the fill is the fraction
            cv.ax.add_patch(Rectangle((px, py), s, s, fc="white", ec=colour, lw=0.4, zorder=5))
            cv.ax.add_patch(Rectangle((px, py), s * (1 if by == "col" else f), s * (f if by == "col" else 1),
                                      fc=colour, ec="none", zorder=5.1))
        else:
            cv.ax.add_patch(FancyBboxPatch((px, py), s, s, boxstyle="round,pad=0,rounding_size=0.45",
                                           fc=colour, ec="none", zorder=5))
    return full + (frac > 1e-9)


def storage_panel(cv, x, y, w, h):
    unit = STORAGE[NANO]
    card(cv, x, y, w, h, "b", "Storage overhead",
         f"state kept per trajectory; one cell = {unit:.0f} MiB, areas to scale")
    x0, pitch, rows, cols = x + 3.4, 3.4, 8, 17
    assert cols * rows >= CELLS[FULL] > (cols - 1) * rows

    def head(yy, m):
        xe = pill(cv, x0, yy, m) - 0.6 if m == NANO else run(cv, x0, yy, [(m, TXT[m], B, "bold", "normal")])
        run(cv, xe, yy, [("   " + STORAGE_LABEL[m], TXT[m], B, "bold", "normal"),
                         ("  " + STORAGE_AT[m], MUTED, A, "normal", "italic")])

    # Full Context: a block of 129.6 cells, then open-ended growth
    yy = y + h - 12.6
    head(yy, FULL)
    top = yy - 2.0
    used = cells(cv, x0, top, CELLS[FULL], cols, rows, pitch, COL[FULL])
    assert used == math.ceil(CELLS[FULL])
    s = pitch - 0.4
    for i in range(used, used + (rows - used % rows) % rows + 2 * rows):  # rest of the column, two more columns
        c, r = i // rows, i % rows
        a = max(0.25, 1.0 - 0.38 * (c - (cols - 1)))
        cv.ax.add_patch(Rectangle((x0 + c * pitch, top - rows * pitch + 0.4 + r * pitch), s, s, fc="white",
                                  ec=mix(COL[FULL], "#FFFFFF", 1 - a), lw=0.45, ls=(0, (1.6, 1.3)), zorder=4))
    gx = x0 + (cols + 2) * pitch + 0.6
    gy = top - rows * pitch / 2 + 0.2
    cv.arrow([(gx, gy), (gx + 4.2, gy)], color=COL[FULL], lw=0.7, head=1.3)
    cv.text(gx + 5.2, gy + 1.4, "too large", size=B, color=TXT[FULL], ha="left", style="italic")
    cv.text(gx + 5.2, gy - 1.4, "at 1M", size=B, color=TXT[FULL], ha="left", style="italic")

    # Temp-LoRA: 4.3 cells
    yy = top - rows * pitch - 6.0
    head(yy, LORA)
    cells(cv, x0, yy - 2.0, CELLS[LORA], 5, 1, pitch, COL[LORA], by="row")

    # MemT-1.0-Nano: one cell, and what that means against the two above
    yy = yy - 2.0 - pitch - 6.0
    head(yy, NANO)
    cells(cv, x0, yy - 2.0, CELLS[NANO], 1, 1, pitch, COL[NANO], by="row")
    by = yy - 2.0 - pitch / 2 - 0.95
    ex = run(cv, x0 + pitch + 2.2, by, [(f"{CELLS[FULL]:.0f}×", BLUE["mark"], HERO, "bold", "normal"),
                                        (" smaller than Full Context", BLUE["ink"], B, "normal", "normal")])
    run(cv, ex + 3.4, by, [(f"{CELLS[LORA]:.1f}×", BLUE["mark"], T, "bold", "normal"),
                           (" smaller than Temp-LoRA", BLUE["ink"], B, "normal", "normal")])


def render(out):
    cv = Canvas(178, 70, size=B)
    latency_panel(cv, 0.4, 0.4, 87.6, 69.2)
    storage_panel(cv, 91.0, 0.4, 86.6, 69.2)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=".")
    print("\n".join(render(ap.parse_args().out)))
