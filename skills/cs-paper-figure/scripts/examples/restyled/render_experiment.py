"""Experiment: results figure for a synthetic memory-policy study (four panels, 178 x 131 mm).

Source. gallery/before/experiment.png, an older four-panel drawing of the same study, and the bundled
analysis (data/experiment/analysis.json). The analysis is the output of a constructed online-memory
simulator: 4 policies x 4 task families x 4 memory budgets x 24 matched seed blocks x 96 episodes.
The numbers are SYNTHETIC; the figure says so once, in the words of the file's own `data_status`.

Content kept from the source.
  (a) the four paired contrasts, all 24 seed-block effects per contrast, mean and paired 95% CI, and the
      printed "mean [CI]" values;
  (b) verified - unfiltered by task family x memory budget, with the cells whose CI includes zero marked;
  (c) mean success against model tokens per episode for every policy x budget, with 95% CIs on both axes;
  (d) corrupted reads and repeat invalid writes per 100 episodes for the four policies, and the remark
      that the rejection history takes 25% of the memory budget and buys no net success.

Design decisions.
  * Claim: checking memory writes is worth +6.6 pp over unfiltered writes; the rejection history is not
    worth anything on net. The hero is the first row of (a): tinted band, the largest number on the plate.
  * One policy = one colour and one marker in every panel (grey square, amber triangle, blue circle,
    violet open diamond). Contrast labels are written in the two policies' colours, so (a) needs no key.
  * The policy key is drawn as objects: each policy's memory budget as a bar, with the 25% the verified
    policy gives to its rejection history cut out of it (`history_fraction`). This replaces a sentence.
  * (a) separates the 24 seed effects (dot histogram above the row line) from the estimate (bar below), so
    the interval is never hidden under the dots.
  * (b) uses a zero-anchored one-hue ramp because every cell is a gain, and adds the row, column and grand
    means: the grand mean is the +6.6 of (a) (asserted), which shows the equal-weight estimand instead of
    describing it in a note.
  * (c) labels every line at its end and every point with its budget, and prints the mean gain next to its
    mean token cost (both computed here; the mean vertical gap is asserted to equal the contrast in (a)).
  * (d) puts success beside the two error rates on the same four rows: the error bars shrink with the
    history (ratio brackets) while the success dots of the two verified policies coincide.
  * Charts are hand-placed on the paperkit canvas in millimetres, so every label goes through the
    text-overlap audit. Times/STIX, text 5.9-11 pt.

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

# one policy = one colour + one marker in every panel; `k` evens out the optical size of the markers
POL = {
    "none":       dict(name="No memory", role="neutral", color="#5E6875", marker="s", k=0.86, note="nothing stored"),
    "unfiltered": dict(name="Unfiltered", role="amber", color=ROLE["amber"]["mark"], marker="^", k=1.05,
                       note="unchecked records"),
    "verified":   dict(name="Verified", role="blue", color=ROLE["blue"]["mark"], marker="o", k=1.0,
                       note="checked + {h:.0f}% history"),
    "no_history": dict(name="No history", role="purple", color=ROLE["purple"]["mark"], marker="D", k=0.8,
                       note="checked records only"),
}
ORDER = ["none", "unfiltered", "verified", "no_history"]


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


def mark(cv, x, y, p, d=1.9, z=12, hero=False):
    """A policy's marker, d mm across. The no-history ablation is drawn open so it survives sitting on Verified."""
    q = POL[p]
    hollow = p == "no_history"
    cv.ax.plot([x], [y], ls="none", marker=q["marker"], ms=d * PT_PER_MM * q["k"] * (1.2 if hero else 1.0),
               mfc="white" if hollow else q["color"], mec=q["color"] if hollow else "white",
               mew=0.9 if hollow else 0.5, zorder=z)


def hline(cv, x0, x1, y, color=AXIS, lw=0.6, z=3, **kw):
    cv.ax.plot([x0, x1], [y, y], color=color, lw=lw, zorder=z, solid_capstyle="butt", **kw)


def vline(cv, x, y0, y1, color=AXIS, lw=0.6, z=3, **kw):
    cv.ax.plot([x, x], [y0, y1], color=color, lw=lw, zorder=z, solid_capstyle="butt", **kw)


def whisker(cv, lo, hi, y, color=INK, lw=0.7, cap=1.1, z=6):
    """Horizontal interval with end caps, so a short one does not read as a minus sign."""
    hline(cv, lo, hi, y, color=color, lw=lw, z=z)
    for v in (lo, hi):
        vline(cv, v, y - cap / 2, y + cap / 2, color=color, lw=lw, z=z)


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


def card(cv, x, y, w, h, letter, title, note=None):
    cv.group(x, y, w, h, "neutral", f"({letter}) {title}", band=True, size=8.0, fill="white", lw=0.6)
    bh = 8.0 * 0.62
    if note:
        cv.text(x + w - 2.0, y + h - bh / 2, note, size=6.0, style="italic", color=MUTED, ha="right", z=3)
    return y + h - bh  # top of the free area


# ------------------------------------------------------------------ key ---
def policy_key(cv, x, y, w, h, A):
    cfg = A["config"]
    hist = cfg["history_fraction"]
    cv.box(x, y, w, h, "neutral", lw=0.6, radius=2.0, container=True)
    ya, yb = y + h - 3.7, y + 3.4
    cv.text(x + 2.5, ya, "Policy", size=7.2, weight="bold", ha="left")
    cv.text(x + 2.5, yb, "memory budget", size=5.9, style="italic", color=MUTED, ha="left")
    ex, pitch, bw, bh = x + 17.5, 32.6, 10.5, 2.3
    for i, p in enumerate(ORDER):
        q, c = POL[p], ROLE[POL[p]["role"]]
        x0 = ex + i * pitch
        if p != "none":  # the line style the policy has in panel (c); no memory is a single point there
            cv.ax.plot([x0, x0 + 5.0], [ya, ya], color=q["color"], lw=1.7 if p == "verified" else 1.0,
                       ls=(0, (2.2, 1.4)) if p == "no_history" else "-", zorder=6, solid_capstyle="butt")
        mark(cv, x0 + 2.5, ya, p, d=2.0, hero=p == "verified")
        cv.text(x0 + 6.6, ya, q["name"], size=7.2, weight="bold", color=c["ink"], ha="left")
        by = yb - bh / 2
        if p == "none":
            cv.ax.add_patch(Rectangle((x0, by), bw, bh, fc="white", ec=c["stroke"], lw=0.55, ls=(0, (2, 1.4)), zorder=6))
        else:
            cut = hist if p == "verified" else 0.0
            cv.ax.add_patch(Rectangle((x0, by), bw * (1 - cut), bh, fc=c["soft"], ec="none", zorder=6))
            if cut:
                cv.ax.add_patch(Rectangle((x0 + bw * (1 - cut), by), bw * cut, bh, fc=c["mark"], ec="none", zorder=6))
            cv.ax.add_patch(Rectangle((x0, by), bw, bh, fc="none", ec=c["stroke"], lw=0.55, zorder=6.1))
        note = q["note"].format(h=100 * hist)
        cv.text(x0 + bw + 1.2, yb, note, size=5.9, style="italic", color=MUTED, ha="left")
        assert bw + 1.2 + cv.text_width(note, 5.9) < pitch - 0.8, note
    # the one in-art status label, in the analysis file's own words
    head, tail = A["data_status"].split(" — ")
    first, second = tail.split(", ")
    cx = x + w - 13.8
    tag = dict(fill="#F4F5F7", soft="#E6E8EC", stroke="#262B33", ink="#262B33", mark="#3A4250")
    cv.chip(cx, y + h - 2.9, head, tag, size=6.4, h=3.3, pad=1.4, solid=True, region=(x, y, x + w, y + h))
    cv.text(cx, y + 5.3, first + ",", size=5.9, style="italic", color=MUTED)
    cv.text(cx, y + 2.6, second, size=5.9, style="italic", color=MUTED)


# -------------------------------------------------------------- panel a ---
def panel_a(cv, x, y, w, h, A):
    n = A["config"]["n_seeds"]
    top = card(cv, x, y, w, h, "a", "Paired success differences",
               f"dot: one seed block (n = {n})  ·  tick, bar: mean, 95% CI")
    con = {(c["left"], c["right"]): c for c in A["contrasts"]}
    rows = [("verified", "unfiltered"), ("verified", "none"), ("unfiltered", "none"), ("verified", "no_history")]
    assert set(rows) == set(con)
    px0, px1, base = x + 33.5, x + 80.0, y + 10.0
    sx = lin(-3.0, 12.5, px0, px1)
    heights = [12.2, 10.5, 10.5, 10.5]
    assert base + sum(heights) <= top - 0.3
    ytop = base + sum(heights)
    # hero band first, then the grid over it
    cv.ax.add_patch(Rectangle((x + 1.2, ytop - heights[0] + 0.25), w - 2.4, heights[0] - 0.25,
                              fc=ROLE["blue"]["fill"], ec="none", zorder=1.5))
    cv.ax.add_patch(Rectangle((x + 1.2, ytop - heights[0] + 0.25), 0.9, heights[0] - 0.25,
                              fc=ROLE["blue"]["mark"], ec="none", zorder=1.6))
    for t in (5, 10):
        vline(cv, float(sx(t)), base - 1.0, ytop, color=GRID, lw=0.5, z=2)
    ax_y = base - 1.0  # the axis sits clear of the last row's estimate
    vline(cv, float(sx(0)), ax_y, ytop, color=LINE, lw=0.7, z=2.5)
    hline(cv, px0, px1, ax_y, z=3)
    for t in (0, 5, 10):
        vline(cv, float(sx(t)), ax_y - 0.8, ax_y, z=3)
        cv.text(float(sx(t)), ax_y - 2.2, signed(t, 0) if t else "0", size=6.2, color=TICK)
    cv.text((px0 + px1) / 2, ax_y - 5.3, "Success difference (percentage points)", size=6.8)
    y1 = ytop
    for k, (key, rh) in enumerate(zip(rows, heights)):
        c, hero = con[key], k == 0
        y0, yc = y1 - rh, y1 - rh / 2
        if k > 1:
            hline(cv, x + 2.0, x + w - 2.0, y1, color=GRID, lw=0.5, z=1.8)
        left, right = key
        col = POL[left]["color"]
        cv.rich(x + 3.4, yc, [(POL[left]["name"], ink(left), "bold"), ("  −  ", INK),
                              (POL[right]["name"], ink(right), "bold")], size=7.6 if hero else 7.0)
        vals = np.asarray(c["seed_values"], float)
        assert len(vals) == n
        d = 1.05
        yb = y0 + (4.4 if hero else 3.5)  # dot baseline; the estimate sits below it
        off = swarm(sx(vals), d, gap=0.06)
        assert yb + max(off) + d / 2 < y1 - 0.3, "seed dots leave the row"
        for vx, oy in zip(sx(vals), off):
            cv.ax.plot([vx], [yb + oy], ls="none", marker="o", ms=d * PT_PER_MM, mfc="white", mec=col, mew=0.55,
                       zorder=6)
        ye, eh = y0 + (2.2 if hero else 1.6), (1.6 if hero else 1.4)  # estimate lane: CI bar, mean tick
        lo, hi = float(sx(c["lo"])), float(sx(c["hi"]))
        cv.ax.add_patch(Rectangle((lo, ye - eh / 2), hi - lo, eh, fc=mix(col, "#FFFFFF", 0.35), ec="none", zorder=7))
        vline(cv, float(sx(c["mean"])), ye - eh / 2 - 0.5, ye + eh / 2 + 0.5, color=ink(left),
              lw=1.6 if hero else 1.3, z=8)
        vx = x + w - 2.8
        if hero:
            cv.text(vx, yc + 1.5, signed(c["mean"]) + " pp", size=11.0, weight="bold", color=ink(left), ha="right")
            cv.text(vx, yc - 3.0, f"[{signed(c['lo'])}, {signed(c['hi'])}]", size=6.4, color=MUTED, ha="right")
        else:
            cv.text(vx, yc + 1.4, signed(c["mean"]), size=8.0, weight="bold", color=ink(left), ha="right")
            cv.text(vx, yc - 2.0, f"[{signed(c['lo'])}, {signed(c['hi'])}]", size=6.0, color=MUTED, ha="right")
        y1 = y0
    return con


# -------------------------------------------------------------- panel b ---
def panel_b(cv, x, y, w, h, A, con):
    top = card(cv, x, y, w, h, "b", "Gain by task and budget")
    B = ROLE["blue"]
    bh = 8.0 * 0.62
    cv.rich(x + w - 2.0, y + h - bh / 2, [("Verified", ink("verified"), "bold"), (" − ", INK),
                                          ("Unfiltered", ink("unfiltered"), "bold")], size=6.4, ha="right", z=3)
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
    ramp = mcolors.LinearSegmentedColormap.from_list("gain", ["#FFFFFF", B["soft"], B["mark"]])
    cw, ch, gap = 9.9, 7.5, 1.3
    gx, gy = x + 18.5, top - 7.3  # left edge of the grid, top edge of the cells
    cv.text(gx + 2 * cw, top - 2.3, "Memory budget (tokens)", size=6.2, style="italic", color=MUTED)
    R, C = M.shape

    def cell(cx, cy, v, bold=False, frame=None):
        fc = ramp(v / vmax)
        cv.ax.add_patch(Rectangle((cx, cy), cw, ch, fc=fc, ec="#D5DBE4", lw=0.4, zorder=5))
        lum = 0.2126 * fc[0] + 0.7152 * fc[1] + 0.0722 * fc[2]
        cv.text(cx + cw / 2, cy + ch / 2, signed(v), size=7.4 if bold else 6.8, weight="bold" if bold else "normal",
                color="white" if lum < 0.55 else "#14305C", z=7)
        if frame:
            cv.ax.add_patch(Rectangle((cx, cy), cw, ch, fc="none", ec=frame, lw=1.0, zorder=6))

    for j, b in enumerate(buds):
        cv.text(gx + (j + 0.5) * cw, top - 5.5, thousands(b), size=6.4, color=TICK)
    mx, my = gx + C * cw + gap, gy - R * ch - gap - ch
    cv.text(mx + cw / 2, top - 5.5, "mean", size=6.4, style="italic", color=MUTED)
    for i, f in enumerate(fams):
        cy = gy - (i + 1) * ch
        cv.text(gx - 1.3, cy + ch / 2, f, size=6.8, ha="right")
        for j in range(C):
            cell(gx + j * cw, cy, M[i, j])
            if LO[i, j] <= 0 <= HI[i, j]:
                cv.ax.add_patch(Rectangle((gx + j * cw + 0.55, cy + 0.55), cw - 1.1, ch - 1.1, fc="none", ec=INK,
                                          lw=0.6, ls=(0, (2.2, 1.5)), zorder=6))
        cell(mx, cy, rmean[i])
    cv.ax.add_patch(Rectangle((gx, gy - R * ch), C * cw, R * ch, fc="none", ec=B["stroke"], lw=0.6, zorder=6.5))
    cv.text(gx - 1.3, my + ch / 2, "mean", size=6.4, style="italic", color=MUTED, ha="right")
    for j in range(C):
        cell(gx + j * cw, my, cmean[j])
    cell(mx, my, grand, bold=True, frame=B["ink"])  # the hero number of panel (a)
    # scale and the key for the dashed cells
    ky = y + 3.1
    sx0, sx1 = gx, gx + 21.0
    n = 64
    for k in range(n):
        cv.ax.add_patch(Rectangle((sx0 + (sx1 - sx0) * k / n, ky - 0.8), (sx1 - sx0) / n + 0.02, 1.6,
                                  fc=ramp((k + 0.5) / n), ec="none", zorder=5))
    cv.ax.add_patch(Rectangle((sx0, ky - 0.8), sx1 - sx0, 1.6, fc="none", ec=B["stroke"], lw=0.45, zorder=6))
    cv.text(sx0 - 0.9, ky, "0", size=6.0, color=TICK, ha="right")
    cv.text(sx1 + 0.9, ky, f"{signed(vmax, 0)} pp", size=6.0, color=TICK, ha="left")
    dx = mx + cw - 21.5
    cv.ax.add_patch(Rectangle((dx, ky - 1.1), 3.2, 2.2, fc="white", ec=INK, lw=0.6, ls=(0, (2.2, 1.5)), zorder=6))
    cv.text(dx + 4.1, ky, "95% CI includes 0", size=6.0, style="italic", color=MUTED, ha="left")


# -------------------------------------------------------------- panel c ---
def panel_c(cv, x, y, w, h, A, con):
    n = A["config"]["n_seeds"]
    top = card(cv, x, y, w, h, "c", "Success versus token cost", f"mean over {n} seed blocks  ·  bar: 95% CI")
    T = A["tradeoff"]
    buds = A["config"]["budgets_tokens"]
    px0, px1, py0, py1 = x + 12.0, x + 85.0, y + 9.5, top - 2.2
    sx, sy = lin(2.95, 4.5, px0, px1), lin(50, 70, py0, py1)
    for t in (50, 55, 60, 65, 70):
        hline(cv, px0, px1, float(sy(t)), color=GRID, lw=0.5, z=2)
        cv.text(px0 - 1.4, float(sy(t)), str(t), size=6.2, color=TICK, ha="right")
    vline(cv, px0, py0, py1, z=3)
    hline(cv, px0, px1, py0, z=3)
    for t in (3.0, 3.5, 4.0, 4.5):
        vline(cv, float(sx(t)), py0 - 0.8, py0, z=3)
        cv.text(float(sx(t)), py0 - 2.2, f"{t:.1f}", size=6.2, color=TICK)
    cv.text((px0 + px1) / 2, py0 - 5.4, "Model tokens per episode (thousands)", size=6.8)
    cv.text(x + 3.6, (py0 + py1) / 2, "Success (%)", size=6.8, rotation=90)

    pts = {}
    for p in ORDER:
        s, tk = T[p]["success"], T[p]["tokens"]
        xs, ys = sx(tk["mean"]), sy(s["mean"])
        q, hero = POL[p], p == "verified"
        k = 1 if p == "none" else len(buds)  # no memory ignores its budget: one point
        if p == "none":
            assert len(set(s["mean"])) == 1 and len(set(tk["mean"])) == 1
        else:
            cv.ax.plot(xs, ys, color=q["color"], lw=1.8 if hero else 1.0, zorder=6 if hero else 5,
                       ls=(0, (2.2, 1.4)) if p == "no_history" else "-", solid_capstyle="round")
        for j in range(k):
            ci = dict(color=q["color"], lw=0.8 if hero else 0.6, z=5.5 if hero else 4.5, alpha=1.0 if hero else 0.75)
            vline(cv, float(xs[j]), float(sy(s["lo"][j])), float(sy(s["hi"][j])), **ci)
            hline(cv, float(sx(tk["lo"][j])), float(sx(tk["hi"][j])), float(ys[j]), **ci)  # mostly inside the marker
            mark(cv, float(xs[j]), float(ys[j]), p, d=2.3 if hero else 1.9, z=9 if hero else 8)
        pts[p] = (xs, ys)
    # budgets on the two lines the panel compares; end labels instead of a legend
    for j, b in enumerate(buds):
        vx, vy = pts["verified"]
        cv.text(float(vx[j]) - 1.1, float(vy[j]) + 2.4, thousands(b), size=6.0, color=ink("verified"), ha="right",
                z=11)
        ux, _ = pts["unfiltered"]
        cv.text(float(ux[j]), float(sy(T["unfiltered"]["success"]["lo"][j])) - 1.5, thousands(b), size=6.0,
                color=ink("unfiltered"), z=11)
    ex = px1 + 1.2
    cv.text(ex, float(pts["verified"][1][-1]) + 1.3, POL["verified"]["name"], size=7.2, weight="bold",
            color=ink("verified"), ha="left")
    cv.text(ex, float(pts["no_history"][1][-1]) - 1.9, POL["no_history"]["name"], size=6.8, color=ink("no_history"),
            ha="left")
    cv.text(float(pts["unfiltered"][0][-1]) + 2.6, float(pts["unfiltered"][1][-1]), POL["unfiltered"]["name"],
            size=6.8, color=ink("unfiltered"), ha="left")
    cv.text(float(pts["none"][0][0]) - 2.2, float(sy(T["none"]["success"]["hi"][0])) + 1.6, POL["none"]["name"],
            size=6.8, color=ink("none"), ha="left")

    # what the gain costs, averaged over the four budgets (the estimand of panel a)
    def mean_of(p, m):
        return float(np.mean(T[p][m]["mean"]))

    bx, by = px0 + 1.8, py1 - 11.4
    cv.box(bx, by, 39.0, 10.2, fill="white", stroke="#C9CED6", lw=0.5, radius=1.0, z=10, container=True)
    cv.rich(bx + 1.5, by + 8.0, [("Verified", ink("verified"), "bold"), (", mean over budgets", MUTED)], size=6.2,
            z=11)
    for r, other in enumerate(("unfiltered", "none")):
        gain = mean_of("verified", "success") - mean_of(other, "success")
        cost = 100 * (mean_of("verified", "tokens") / mean_of(other, "tokens") - 1)
        assert abs(gain - con[("verified", other)]["mean"]) < 1e-6, (other, gain)
        ry = by + 5.0 - r * 2.8
        cv.rich(bx + 1.5, ry, [("vs ", MUTED), (POL[other]["name"], ink(other))], size=6.2, z=11)
        cv.text(bx + 23.8, ry, signed(gain) + " pp", size=6.4, weight="bold", ha="right", z=11)
        cv.text(bx + 37.6, ry, f"{signed(cost, 0)}% tokens", size=6.2, color=MUTED, ha="right", z=11)


# -------------------------------------------------------------- panel d ---
def panel_d(cv, x, y, w, h, A, con):
    top = card(cv, x, y, w, h, "d", "Rejection-history diagnostic")
    D, S = A["diagnostics"], A["macro_success"]
    pol = A["config"]["policies"]
    cols = [("corrupt_read", ("Corrupted", "reads")), ("repeat_invalid_write", ("Repeat invalid", "writes"))]
    c0 = [x + 22.0, x + 38.5]
    cw = 13.5
    vmax = 20.0
    assert max(max(D[k]["hi"]) for k, _ in cols) <= vmax
    yr = [top - 10.2 - 8.2 * i for i in range(len(ORDER))]
    base = yr[-1] - 4.6
    ytop = yr[0] + 3.9
    for p, yc in zip(ORDER, yr):
        mark(cv, x + 3.8, yc, p, d=1.9, hero=p == "verified")
        cv.text(x + 6.2, yc, POL[p]["name"], size=6.9, color=ink(p), ha="left",
                weight="bold" if p == "verified" else "normal")
    for (key, head), x0 in zip(cols, c0):
        sx = lin(0, vmax, x0, x0 + cw)
        cv.text(x0 + cw / 2, top - 2.2, head[0], size=6.6, weight="bold")
        cv.text(x0 + cw / 2, top - 4.8, head[1], size=6.6, weight="bold")
        for t in (10, 20):
            vline(cv, float(sx(t)), base, ytop, color=GRID, lw=0.5, z=2)
        for t in (0, 10, 20):
            cv.text(float(sx(t)), base - 2.0, str(t), size=6.2, color=TICK)
        hline(cv, x0, x0 + cw, base, z=3)
        vline(cv, x0, base, ytop, color=LINE, lw=0.6, z=4)
        ends = {}
        for p, yc in zip(ORDER, yr):
            i = pol.index(p)
            v, lo, hi = D[key]["mean"][i], D[key]["lo"][i], D[key]["hi"][i]
            L = float(sx(v)) - x0
            if v > 0:
                cv.ax.add_patch(Rectangle((x0, yc - 1.9), L, 3.8, fc=POL[p]["color"], ec="none", zorder=5))
                whisker(cv, float(sx(lo)), float(sx(hi)), yc)
            lab = f"{v:.1f}" if v > 0 else "0"
            if L > 8.0:
                cv.text(x0 + L - 1.7, yc, lab, size=6.4, weight="bold", color="white", ha="right", z=7)
                ends[p] = x0 + L
            else:
                lx = (float(sx(hi)) if v > 0 else x0) + 1.0
                cv.text(lx, yc, lab, size=6.4, color=ink(p) if v > 0 else MUTED, ha="left", z=7)
                ends[p] = lx + cv.text_width(lab, 6.4)
        # how many times fewer events the history leaves
        i_v, i_n = pol.index("verified"), pol.index("no_history")
        ratio = D[key]["mean"][i_n] / D[key]["mean"][i_v]
        bx = max(ends["verified"], ends["no_history"]) + 1.5
        ya, yb = yr[ORDER.index("verified")], yr[ORDER.index("no_history")]
        cv.ax.plot([bx - 0.6, bx, bx, bx - 0.6], [ya, ya, yb, yb], color=LINE, lw=0.6, zorder=6,
                   solid_joinstyle="miter")
        cv.text(bx + 0.7, (ya + yb) / 2 + 1.25, f"{ratio:.1f}×", size=6.6, weight="bold", ha="left")
        cv.text(bx + 0.7, (ya + yb) / 2 - 1.25, "fewer", size=6.0, style="italic", color=MUTED, ha="left")
    mid = (c0[0] + c0[1] + cw) / 2
    cv.text(mid, base - 5.0, "Events per 100 episodes", size=6.8)
    # success on the same rows: fewer errors, same success
    x0, sw = x + 56.0, 13.5
    ss = lin(50, 70, x0, x0 + sw)
    cv.text(x0 + sw / 2, top - 2.2, "Success", size=6.6, weight="bold")
    cv.text(x0 + sw / 2, top - 4.8, "(%)", size=6.6, weight="bold")
    for t in (50, 60, 70):
        vline(cv, float(ss(t)), base, ytop, color=GRID, lw=0.5, z=2)
        cv.text(float(ss(t)), base - 2.0, str(t), size=6.2, color=TICK)
    hline(cv, x0, x0 + sw, base, z=3)
    for p, yc in zip(ORDER, yr):
        i = pol.index(p)
        whisker(cv, float(ss(S["lo"][i])), float(ss(S["hi"][i])), yc, color=POL[p]["color"], lw=0.9, cap=1.3)
        mark(cv, float(ss(S["mean"][i])), yc, p, d=1.9, hero=p == "verified")
    c = con[("verified", "no_history")]
    assert abs((S["mean"][pol.index("verified")] - S["mean"][pol.index("no_history")]) - c["mean"]) < 1e-6
    ya, yb = yr[ORDER.index("verified")], yr[ORDER.index("no_history")]
    vline(cv, float(ss(S["mean"][pol.index("verified")])), yb + 1.5, ya - 1.5, color=LINE, lw=0.6, z=5,
          ls=(0, (1.6, 1.2)))
    cv.text(float(ss(S["mean"][pol.index("verified")])) - 0.9, (ya + yb) / 2, signed(c["mean"]) + " pp", size=6.6,
            weight="bold", ha="right")


# ----------------------------------------------------------------- main ---
def render(analysis, out, stem="experiment"):
    with open(analysis) as f:
        A = json.load(f)
    W, H = 178.0, 131.0
    cv = Canvas(W, H, family="serif", size=7.0)
    m, g = 1.5, 2.5
    kh, h1, h2 = 12.0, 59.0, 52.0
    wl = 100.0
    wr = W - 2 * m - 3.0 - wl
    xr = m + wl + 3.0
    y2 = m
    y1 = y2 + h2 + g
    yk = y1 + h1 + g
    assert abs(yk + kh + m - H) < 1e-6
    policy_key(cv, m, yk, W - 2 * m, kh, A)
    con = panel_a(cv, m, y1, wl, h1, A)
    panel_b(cv, xr, y1, wr, h1, A, con)
    panel_c(cv, m, y2, wl, h2, A, con)
    panel_d(cv, xr, y2, wr, h2, A, con)
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
