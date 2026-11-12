"""Experiment: results figure for a synthetic memory-policy study (four bare panels, 178 x 129 mm).

Source. gallery/before/experiment.png, an older four-panel drawing of the same study, and the bundled
analysis (data/experiment/analysis.json). The analysis is the output of a constructed online-memory
simulator: 4 policies x 4 task families x 4 memory budgets x 24 matched seed blocks x 96 episodes.
The numbers are SYNTHETIC; the figure says so once, in the words of the file's own `data_status`.

Content.
  (a) the four paired contrasts, all 24 seed-block effects per contrast, mean and paired 95% CI, and the
      printed "mean [CI]" values;
  (b) verified - unfiltered by task family x memory budget, with the cells whose CI includes zero marked;
  (c) mean success against model tokens per episode for every policy x budget, with 95% CIs on both axes;
  (d) for the four policies: the share of the memory budget given to the rejection history, corrupted
      reads and repeat invalid writes per 100 episodes, and success.

Design decisions (references/visual-craft.md §1, §4, §6, §11).
  * Message: checking memory writes is worth +6.6 pp over unfiltered writes; the rejection history is not
    worth anything on net.
  * Charts sit bare on the page: no card, no header band, no boxed key. Each panel has a plain head (bold
    letter, regular title) with its units and encodings in one italic line under it; panels are separated
    by white gutters. One frameless key row defines the four policies.
  * Hero by difference: the primary contrast is the first row of (a), the only filled dot cloud and the
    only number at head size; the other three contrasts are open dots and regular numbers. No band, no
    thicker stroke.
  * One policy = one colour and one marker in every panel (blue circle, violet open diamond, amber
    triangle, grey square): three hues and a grey. The ablation is also dashed and drawn open, so it
    survives sitting on Verified and survives greyscale. Contrast labels are written in the two policies'
    colours.
  * (b) is a borderless heat table on a zero-anchored one-hue ramp in the Verified blue (every cell is a
    gain). Values are in the cells, so there is no colour bar. The margins are the row, column and grand
    means: the grand mean is the +6.6 of (a) (asserted), which shows the equal-weight estimand.
  * (c) labels every line at its end and every point with its budget, and prints the mean gain next to
    its mean token cost (both computed here; the mean vertical gap is asserted to equal the contrast in (a)).
  * (d) reads left to right on four shared rows: what the history costs (25% of the budget, drawn as the
    cut of a bar), what it removes (ratio brackets on the error bars), what it buys (nothing: the two
    success dots coincide).
  * Type: Times/STIX at three sizes, 10 pt (heads and the claim number), 7.4 pt (labels), 6.4 pt (ticks,
    notes). Strokes: 0.6 pt (axes, grid, whiskers, brackets, dot outlines) and 1.2 pt (series lines, mean
    ticks, the open marker).
  * Charts are hand-placed on the paperkit canvas in millimetres, so every label goes through the
    text-overlap audit.

Every plotted value is read from the analysis file; differences, ratios and means are computed below.

    python render_experiment.py --out DIR [--analysis analysis.json]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

import numpy as np  # noqa: E402
from matplotlib import colors as mcolors  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from paperkit import INK, LINE, MUTED, PT_PER_MM, ROLE, Canvas, mix  # noqa: E402

GRID = "#E3E6EA"
AXIS = "#9AA0A8"
TICK = "#4A5059"
T, B, A_ = 10.0, 7.4, 6.4     # heads and the claim number, labels, ticks and notes (pt)
THIN, SERIES = 0.6, 1.2       # the two stroke weights (pt)
DASH = (0, (2.2, 1.4))

# one policy = one colour + one marker in every panel; `k` evens out the optical size of the markers
POL = {
    "none":       dict(name="No memory", role="neutral", color="#5E6875", marker="s", k=0.86, note="nothing stored"),
    "unfiltered": dict(name="Unfiltered", role="amber", color=ROLE["amber"]["mark"], marker="^", k=1.05,
                       note="unchecked records"),
    "verified":   dict(name="Verified", role="blue", color=ROLE["blue"]["mark"], marker="o", k=1.0,
                       note="checked + {h:.0f}% history"),
    "no_history": dict(name="No history", role="purple", color=ROLE["purple"]["mark"], marker="D", k=0.74,
                       note="checked records only"),
}
ORDER = ["verified", "no_history", "unfiltered", "none"]  # ours first, then its ablation, then the baselines


def ink(p):
    return ROLE[POL[p]["role"]]["ink"]


def lin(d0, d1, m0, m1):
    """Linear scale: data [d0, d1] -> millimetres [m0, m1]."""
    k = (m1 - m0) / (d1 - d0)
    return lambda v: m0 + (np.asarray(v, float) - d0) * k


def signed(v, nd=1):
    s = f"{v:+.{nd}f}"
    if float(s) == 0:
        s = "+" + s[1:]
    return s.replace("-", "−")


def thousands(v):
    return f"{v:,}"


def mark(cv, x, y, p, d=2.0, z=12):
    """A policy's marker, d mm across. The no-history ablation is drawn open so it survives sitting on Verified."""
    q = POL[p]
    hollow = p == "no_history"
    cv.ax.plot([x], [y], ls="none", marker=q["marker"], ms=d * PT_PER_MM * q["k"],
               mfc="white" if hollow else q["color"], mec=q["color"] if hollow else "white",
               mew=SERIES if hollow else THIN, zorder=z)


def hline(cv, x0, x1, y, color=AXIS, lw=THIN, z=3, **kw):
    cv.ax.plot([x0, x1], [y, y], color=color, lw=lw, zorder=z, solid_capstyle="butt", **kw)


def vline(cv, x, y0, y1, color=AXIS, lw=THIN, z=3, **kw):
    cv.ax.plot([x, x], [y0, y1], color=color, lw=lw, zorder=z, solid_capstyle="butt", **kw)


def whisker(cv, lo, hi, y, color=INK, cap=1.1, z=6):
    """Horizontal interval with end caps, so a short one does not read as a minus sign."""
    hline(cv, lo, hi, y, color=color, z=z)
    for v in (lo, hi):
        vline(cv, v, y - cap / 2, y + cap / 2, color=color, z=z)


def swarm(xs, d, gap=0.1):
    """Dot-histogram heights: each dot takes the lowest free place above the baseline (mm)."""
    placed, out = [], [0.0] * len(xs)
    for i in np.argsort(xs):
        x = float(xs[i])
        near = [(px, py) for px, py in placed if abs(x - px) < d + gap]
        cands = [0.0] + [py + math.sqrt((d + gap) ** 2 - (x - px) ** 2) for px, py in near]
        for c in sorted(cands):
            if all((x - px) ** 2 + (c - py) ** 2 >= (d + gap) ** 2 - 1e-9 for px, py in near):
                out[i] = c
                placed.append((x, c))
                break
    return out


def head(cv, x, ytop, letter, title, note=None):
    """Plain panel head on the page: bold letter, regular title, units and encodings in italic under it.
    Returns the top of the free area."""
    cv.rich(x, ytop - 1.9, [(f"({letter})", INK, "bold"), ("  " + title, INK)], size=T)
    if note:
        cv.text(x, ytop - 6.3, note, size=A_, style="italic", color=MUTED, ha="left")
    return ytop - 8.6


# ------------------------------------------------------------------ key ---
def policy_key(cv, x, ytop, w, A):
    """One frameless row: each policy's line and marker, its name and what it stores; the status label."""
    hist = A["config"]["history_fraction"]
    ya, yb = ytop - 1.8, ytop - 5.2
    x0 = x
    for p in ORDER:
        q = POL[p]
        if p != "none":  # the line style the policy has in panel (c); no memory is a single point there
            cv.ax.plot([x0, x0 + 6.0], [ya, ya], color=q["color"], lw=SERIES, ls=DASH if p == "no_history" else "-",
                       zorder=6, solid_capstyle="butt")
        mark(cv, x0 + 3.0, ya, p, d=2.2 if p == "verified" else 2.0)
        note = q["note"].format(h=100 * hist)
        cv.text(x0 + 7.4, ya, q["name"], size=B, weight="bold" if p == "verified" else "normal", color=ink(p),
                ha="left")
        cv.text(x0 + 7.4, yb, note, size=A_, style="italic", color=MUTED, ha="left")
        end = x0 + 7.4 + max(cv.text_width(note, A_, style="italic"), cv.text_width(q["name"], B, "bold"))
        x0 = end + 7.0  # entries are spaced by their own width, like words
    # the one in-art status label, in the analysis file's own words
    label, tail = A["data_status"].split(" — ")
    tag = dict(fill="#F4F5F7", soft="#E6E8EC", stroke="#262B33", ink="#262B33", mark="#3A4250")
    cv.chip(x + w, ya, label, tag, size=A_, h=3.3, pad=1.4, solid=True, ha="right", region=(x, ytop - 7, x + w, ytop))
    cv.text(x + w, yb, tail, size=A_, style="italic", color=MUTED, ha="right")
    assert x + w - cv.text_width(tail, A_, style="italic") > end + 4.0, "key row and status label collide"
    return ytop - 6.6


# -------------------------------------------------------------- panel a ---
def panel_a(cv, x, ytop, w, A):
    n = A["config"]["n_seeds"]
    top = head(cv, x, ytop, "a", "Paired success differences",
               f"dot: one of {n} matched seed blocks;  bar and tick: 95% CI and mean")
    con = {(c["left"], c["right"]): c for c in A["contrasts"]}
    rows = [("verified", "unfiltered"), ("verified", "none"), ("unfiltered", "none"), ("verified", "no_history")]
    assert set(rows) == set(con)
    px0, px1 = x + 31.0, x + w - 17.5
    sx = lin(-3.0, 12.5, px0, px1)
    heights = [11.0] * 4  # equal rows: the hero is not the bigger one
    base = top - sum(heights)
    ax_y = base - 0.8  # the axis sits clear of the last row's estimate
    for t in (5, 10):
        vline(cv, float(sx(t)), ax_y, top, color=GRID, z=2)
    vline(cv, float(sx(0)), ax_y, top, color=LINE, z=2.5)
    hline(cv, px0, px1, ax_y, z=3)
    for t in (0, 5, 10):
        vline(cv, float(sx(t)), ax_y - 0.8, ax_y, z=3)
        cv.text(float(sx(t)), ax_y - 2.3, signed(t, 0) if t else "0", size=A_, color=TICK)
    cv.text((px0 + px1) / 2, ax_y - 5.7, "Success difference (percentage points)", size=B)
    y1 = top
    for k, (key, rh) in enumerate(zip(rows, heights)):
        c, hero = con[key], k == 0
        y0, yc = y1 - rh, y1 - rh / 2
        left, right = key
        col = POL[left]["color"]
        w8 = "bold" if hero else "normal"
        cv.rich(x, yc + (1.5 if hero else 0), [(POL[left]["name"], ink(left), w8), ("  −  ", INK),
                                               (POL[right]["name"], ink(right), w8)], size=B)
        if hero:
            cv.text(x, yc - 1.9, "primary contrast", size=A_, style="italic", color=MUTED, ha="left")
        vals = np.asarray(c["seed_values"], float)
        assert len(vals) == n
        d = 1.05
        yb = y0 + 3.7  # dot baseline; the estimate sits below it
        off = swarm(sx(vals), d, gap=0.06)
        assert yb + max(off) + d / 2 < y1 - 0.2, "seed dots leave the row"
        for vx, oy in zip(sx(vals), off):  # the primary contrast is the only filled cloud
            cv.ax.plot([vx], [yb + oy], ls="none", marker="o", ms=d * PT_PER_MM, mfc=col if hero else "white",
                       mec=col, mew=THIN, zorder=6)
        ye, eh = y0 + 1.6, 1.4  # estimate lane: CI bar, mean tick
        lo, hi = float(sx(c["lo"])), float(sx(c["hi"]))
        cv.ax.add_patch(Rectangle((lo, ye - eh / 2), hi - lo, eh, fc=mix(col, "#FFFFFF", 0.4), ec="none", zorder=7))
        vline(cv, float(sx(c["mean"])), ye - eh / 2 - 0.5, ye + eh / 2 + 0.5, color=ink(left), lw=SERIES, z=8)
        vx = x + w
        cv.text(vx, yc + 1.5, signed(c["mean"]) + (" pp" if hero else ""), size=T if hero else B, weight=w8,
                color=ink(left), ha="right")
        cv.text(vx, yc - (2.6 if hero else 1.9), f"[{signed(c['lo'])}, {signed(c['hi'])}]", size=A_, color=MUTED,
                ha="right")
        y1 = y0
    return con, ax_y - 7.0


# -------------------------------------------------------------- panel b ---
def panel_b(cv, x, ytop, w, ybot, A, con):
    head(cv, x, ytop, "b", "Gain by task and budget")
    B_ = ROLE["blue"]
    ex = cv.rich(x, ytop - 6.3, [("Verified", ink("verified")), (" − ", MUTED), ("Unfiltered", ink("unfiltered")),
                                 (", percentage points", MUTED)], size=A_, style="italic")
    het = A["heterogeneity"]
    M, LO, HI = (np.asarray(het[k], float) for k in ("mean", "lo", "hi"))
    fams = [f["name"] for f in A["config"]["task_families"]]
    buds = A["config"]["budgets_tokens"]
    assert M.shape == (len(fams), len(buds))
    rmean, cmean, grand = M.mean(axis=1), M.mean(axis=0), M.mean()
    # equal weight over the 16 cells is the estimand of panel (a)
    assert abs(grand - con[("verified", "unfiltered")]["mean"]) < 1e-6, grand
    assert M.min() >= 0, "one-hue ramp assumes no negative cell"
    vmax = 2 * math.ceil(M.max() / 2)
    ramp = mcolors.LinearSegmentedColormap.from_list("gain", ["#FFFFFF", B_["soft"], B_["mark"]])
    R, C = M.shape
    gap, g = 1.6, 0.5                                  # margin before the means; white gutter between cells
    gx = x + 19.0
    cw = (x + w - gx - gap) / (C + 1)
    gy = ytop - 16.6                                   # top edge of the cells
    ch = (gy - ybot - gap) / (R + 1)
    cv.text(gx + C * cw / 2, ytop - 10.6, "Memory budget (tokens)", size=B)

    def cell(cx, cy, v, bold=False):
        fc = ramp(v / vmax)
        cv.ax.add_patch(Rectangle((cx + g / 2, cy + g / 2), cw - g, ch - g, fc=fc, ec="none", zorder=5))
        lum = 0.2126 * fc[0] + 0.7152 * fc[1] + 0.0722 * fc[2]
        cv.text(cx + cw / 2, cy + ch / 2, signed(v), size=B, weight="bold" if bold else "normal",
                color="white" if lum < 0.55 else "#14305C", z=7)

    for j, b in enumerate(buds):
        cv.text(gx + (j + 0.5) * cw, gy + 1.8, thousands(b), size=A_, color=TICK)
    mx, my = gx + C * cw + gap, gy - R * ch - gap - ch
    cv.text(mx + cw / 2, gy + 1.8, "mean", size=A_, style="italic", color=MUTED)
    for i, f in enumerate(fams):
        cy = gy - (i + 1) * ch
        cv.text(gx - 1.2, cy + ch / 2, f, size=B, ha="right")
        for j in range(C):
            cell(gx + j * cw, cy, M[i, j])
            if LO[i, j] <= 0 <= HI[i, j]:
                cv.ax.add_patch(Rectangle((gx + j * cw + 0.9, cy + 0.9), cw - 1.8, ch - 1.8, fc="none", ec=INK,
                                          lw=THIN, ls=DASH, zorder=6))
        cell(mx, cy, rmean[i])
    cv.text(gx - 1.2, my + ch / 2, "mean", size=A_, style="italic", color=MUTED, ha="right")
    for j in range(C):
        cell(gx + j * cw, my, cmean[j])
    cell(mx, my, grand, bold=True)  # the claim number of panel (a)
    # key for the dashed cells, on the note line
    lab = "95% CI includes 0"
    lx = x + w - cv.text_width(lab, A_, style="italic")
    cv.text(lx, ytop - 6.3, lab, size=A_, style="italic", color=MUTED, ha="left")
    cv.ax.add_patch(Rectangle((lx - 4.2, ytop - 6.3 - 1.05), 3.2, 2.1, fc="white", ec=INK, lw=THIN, ls=DASH, zorder=6))
    assert lx - 4.2 > ex + 2.0, "note and key collide"


# -------------------------------------------------------------- panel c ---
def panel_c(cv, x, ytop, w, ybot, A, con):
    n = A["config"]["n_seeds"]
    top = head(cv, x, ytop, "c", "Success versus token cost",
               f"mean over {n} seed blocks;  bars: 95% CI;  numbers on points: memory budget (tokens)")
    T_ = A["tradeoff"]
    buds = A["config"]["budgets_tokens"]
    px0, px1, py0, py1 = x + 10.0, x + w - 14.5, ybot + 8.8, top - 1.4
    sx, sy = lin(2.95, 4.5, px0, px1), lin(50, 70, py0, py1)
    for t in (50, 55, 60, 65, 70):
        if t % 10 == 0:  # grid on the tens only, so the summary sits between two lines
            hline(cv, px0, px1, float(sy(t)), color=GRID, z=2)
        hline(cv, px0 - 0.8, px0, float(sy(t)), z=3)
        cv.text(px0 - 1.6, float(sy(t)), str(t), size=A_, color=TICK, ha="right")
    vline(cv, px0, py0, py1, z=3)
    hline(cv, px0, px1, py0, z=3)
    for t in (3.0, 3.5, 4.0, 4.5):
        vline(cv, float(sx(t)), py0 - 0.8, py0, z=3)
        cv.text(float(sx(t)), py0 - 2.3, f"{t:.1f}", size=A_, color=TICK)
    cv.text((px0 + px1) / 2, py0 - 5.7, "Model tokens per episode (thousands)", size=B)
    cv.text(x + 1.4, (py0 + py1) / 2, "Success (%)", size=B, rotation=90)

    pts = {}
    for p in ORDER[::-1]:
        s, tk = T_[p]["success"], T_[p]["tokens"]
        xs, ys = sx(tk["mean"]), sy(s["mean"])
        q, hero = POL[p], p == "verified"
        k = 1 if p == "none" else len(buds)  # no memory ignores its budget: one point
        if p == "none":
            assert len(set(s["mean"])) == 1 and len(set(tk["mean"])) == 1
        else:  # one weight for every line; the ablation is dashed
            cv.ax.plot(xs, ys, color=q["color"], lw=SERIES, zorder=6 if hero else 5,
                       ls=DASH if p == "no_history" else "-", solid_capstyle="round")
        for j in range(k):
            ci = dict(color=q["color"], z=5.5 if hero else 4.5)
            vline(cv, float(xs[j]), float(sy(s["lo"][j])), float(sy(s["hi"][j])), **ci)
            hline(cv, float(sx(tk["lo"][j])), float(sx(tk["hi"][j])), float(ys[j]), **ci)  # mostly inside the marker
            mark(cv, float(xs[j]), float(ys[j]), p, d=2.4 if hero else 2.0, z=9 if hero else 8)
        pts[p] = (xs, ys)
    # budgets on the two lines the panel compares; end labels instead of a legend
    for j, b in enumerate(buds):
        vx, vy = pts["verified"]
        cv.text(float(vx[j]) - 1.2, float(vy[j]) + 2.3, thousands(b), size=A_, color=ink("verified"), ha="right", z=11)
        ux, _ = pts["unfiltered"]
        cv.text(float(ux[j]), float(sy(T_["unfiltered"]["success"]["lo"][j])) - 1.5, thousands(b), size=A_,
                color=ink("unfiltered"), z=11)
    ex = px1 + 1.4
    cv.text(ex, float(pts["verified"][1][-1]) + 1.4, POL["verified"]["name"], size=B, weight="bold",
            color=ink("verified"), ha="left")
    cv.text(ex, float(pts["no_history"][1][-1]) - 1.9, POL["no_history"]["name"], size=B, color=ink("no_history"),
            ha="left")
    cv.text(float(pts["unfiltered"][0][-1]) + 2.6, float(pts["unfiltered"][1][-1]), POL["unfiltered"]["name"],
            size=B, color=ink("unfiltered"), ha="left")
    cv.text(float(pts["none"][0][0]) - 2.0, float(sy(T_["none"]["success"]["hi"][0])) + 1.7, POL["none"]["name"],
            size=B, color=ink("none"), ha="left")

    # what the gain costs, averaged over the four budgets (the estimand of panel a)
    def mean_of(p, m):
        return float(np.mean(T_[p][m]["mean"]))

    bx, by = px0 + 2.2, py1 - 1.9
    cv.rich(bx, by, [("Verified", ink("verified"), "bold"), (", mean over budgets", MUTED)], size=A_)
    for r, other in enumerate(("unfiltered", "none")):
        gain = mean_of("verified", "success") - mean_of(other, "success")
        cost = 100 * (mean_of("verified", "tokens") / mean_of(other, "tokens") - 1)
        assert abs(gain - con[("verified", other)]["mean"]) < 1e-6, (other, gain)
        ry = by - 3.1 - r * 3.0
        cv.rich(bx, ry, [("vs ", MUTED), (POL[other]["name"], ink(other))], size=B)
        cv.text(bx + 25.5, ry, signed(gain) + " pp", size=B, weight="bold", ha="right")
        cv.text(bx + 27.0, ry, f"for {signed(cost, 0)}% tokens", size=A_, color=MUTED, ha="left")


# -------------------------------------------------------------- panel d ---
def panel_d(cv, x, ytop, w, ybot, A, con):
    head(cv, x, ytop, "d", "Rejection-history diagnostic")
    D, S = A["diagnostics"], A["macro_success"]
    pol = A["config"]["policies"]
    hist = A["config"]["history_fraction"]
    base = ybot + 7.2
    pitch = (ytop - 13.6 - base - 4.0) / (len(ORDER) - 1)
    yr = [ytop - 13.6 - pitch * i for i in range(len(ORDER))]
    ytopr = yr[0] + 3.4
    ya, yb = yr[ORDER.index("verified")], yr[ORDER.index("no_history")]
    assert abs(abs(ya - yb) - pitch) < 1e-9, "the two verified policies are adjacent rows"

    def col_head(cx, a, b):
        cv.text(cx, ytop - 6.2, a, size=B)
        cv.text(cx, ytop - 9.0, b, size=B)

    for p, yc in zip(ORDER, yr):
        mark(cv, x + 1.4, yc, p, d=2.2 if p == "verified" else 2.0)
        cv.text(x + 3.8, yc, POL[p]["name"], size=B, color=ink(p), ha="left",
                weight="bold" if p == "verified" else "normal")

    # what the history costs: its cut of the memory budget
    b0, bw, bh = x + 19.5, 8.5, 3.4
    col_head(b0 + bw / 2, "Memory", "budget")
    for p, yc in zip(ORDER, yr):
        c, by = ROLE[POL[p]["role"]], yc - bh / 2
        if p == "none":
            cv.ax.add_patch(Rectangle((b0, by), bw, bh, fc="white", ec=c["stroke"], lw=THIN, ls=DASH, zorder=6))
            continue
        cut = hist if p == "verified" else 0.0
        cv.ax.add_patch(Rectangle((b0, by), bw * (1 - cut), bh, fc=c["soft"], ec="none", zorder=6))
        if cut:
            cv.ax.add_patch(Rectangle((b0 + bw * (1 - cut), by), bw * cut, bh, fc=c["mark"], ec="none", zorder=6))
        cv.ax.add_patch(Rectangle((b0, by), bw, bh, fc="none", ec=c["stroke"], lw=THIN, zorder=6.1))
    cv.text(b0 + bw, ya - bh / 2 - 1.7, f"{100 * hist:.0f}% history", size=A_, style="italic", color=ink("verified"),
            ha="right")

    # what it removes: two error rates
    cols = [("corrupt_read", ("Corrupted", "reads")), ("repeat_invalid_write", ("Repeat invalid", "writes"))]
    c0, cw, vmax = [x + 32.0, x + 48.3], 11.6, 20.0
    assert max(max(D[k]["hi"]) for k, _ in cols) <= vmax
    for (key, hd), x0 in zip(cols, c0):
        sx = lin(0, vmax, x0, x0 + cw)
        col_head(x0 + cw / 2, *hd)
        for t in (10, 20):
            vline(cv, float(sx(t)), base, ytopr, color=GRID, z=2)
        for t in (0, 10, 20):
            cv.text(float(sx(t)), base - 2.2, str(t), size=A_, color=TICK)
        hline(cv, x0, x0 + cw, base, z=3)
        vline(cv, x0, base, ytopr, color=LINE, z=4)
        ends = {}
        for p, yc in zip(ORDER, yr):
            i = pol.index(p)
            v, lo, hi = D[key]["mean"][i], D[key]["lo"][i], D[key]["hi"][i]
            L = float(sx(v)) - x0
            if v > 0:
                cv.ax.add_patch(Rectangle((x0, yc - bh / 2), L, bh, fc=POL[p]["color"], ec="none", zorder=5))
                whisker(cv, float(sx(lo)), float(sx(hi)), yc)
            lab = f"{v:.1f}" if v > 0 else "0"
            if L > 7.0:
                cv.text(x0 + L - 1.5, yc, lab, size=A_, weight="bold", color="white", ha="right", z=7)
                ends[p] = x0 + L
            else:
                lx = (float(sx(hi)) if v > 0 else x0) + 0.9
                cv.text(lx, yc, lab, size=A_, color=ink(p) if v > 0 else MUTED, ha="left", z=7)
                ends[p] = lx + cv.text_width(lab, A_)
        # how many times fewer events the history leaves
        i_v, i_n = pol.index("verified"), pol.index("no_history")
        ratio = D[key]["mean"][i_n] / D[key]["mean"][i_v]
        bx = max(ends["verified"], ends["no_history"]) + 1.3
        cv.ax.plot([bx - 0.6, bx, bx, bx - 0.6], [ya, ya, yb, yb], color=LINE, lw=THIN, zorder=6,
                   solid_joinstyle="miter")
        cv.text(bx + 0.7, (ya + yb) / 2 + 1.3, f"{ratio:.1f}×", size=B, weight="bold", ha="left")
        cv.text(bx + 0.7, (ya + yb) / 2 - 1.3, "fewer", size=A_, style="italic", color=MUTED, ha="left")
    cv.text((c0[0] + c0[1] + cw) / 2, base - 5.6, "Events per 100 episodes", size=B)

    # what it buys: success on the same rows
    x0 = c0[1] + cw + 4.4
    sw = x + w - 1.3 - x0
    ss = lin(50, 70, x0, x0 + sw)
    col_head(x0 + sw / 2, "Success", "(%)")
    for t in (50, 60, 70):
        vline(cv, float(ss(t)), base, ytopr, color=GRID, z=2)
        cv.text(float(ss(t)), base - 2.2, str(t), size=A_, color=TICK)
    hline(cv, x0, x0 + sw, base, z=3)
    for p, yc in zip(ORDER, yr):
        i = pol.index(p)
        whisker(cv, float(ss(S["lo"][i])), float(ss(S["hi"][i])), yc, color=POL[p]["color"], cap=1.3)
        mark(cv, float(ss(S["mean"][i])), yc, p, d=2.2 if p == "verified" else 2.0)
    c = con[("verified", "no_history")]
    assert abs((S["mean"][pol.index("verified")] - S["mean"][pol.index("no_history")]) - c["mean"]) < 1e-6
    cv.text(x0 + sw / 2, (ya + yb) / 2, signed(c["mean"]) + " pp", size=B, weight="bold",
            bbox=dict(fc="white", ec="none", pad=0.6))


# ----------------------------------------------------------------- main ---
def render(analysis, out, stem="experiment"):
    with open(analysis) as f:
        A = json.load(f)
    W, H = 178.0, 129.0
    cv = Canvas(W, H, family="serif", size=B)
    m, gx, gy = 1.0, 9.0, 8.0          # outer margin; gutters between unframed panels
    wl = 90.0
    xr = m + wl + gx
    wr = W - m - xr
    y1 = policy_key(cv, m, H - m, W - 2 * m, A) - 4.6
    con, yb1 = panel_a(cv, m, y1, wl, A)
    panel_b(cv, xr, y1, wr, yb1, A, con)
    y2 = yb1 - gy
    panel_c(cv, m, y2, wl, m, A, con)
    panel_d(cv, xr, y2, wr, m, A, con)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, stem))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=".")
    ap.add_argument("--analysis", default=os.path.join(HERE, "data", "experiment", "analysis.json"))
    a = ap.parse_args()
    print("\n".join(render(a.analysis, a.out)))
