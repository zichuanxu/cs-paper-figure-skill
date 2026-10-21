"""Restyled 'experiment' example: SYNTHETIC memory-policy study (paired effects,
heterogeneity, quality/cost, mechanism diagnostics), drawn with paperkit.

Every number is read from the preserved analysis.json (no re-simulation); derived
ratios are computed here and asserted against it.

    python render_experiment.py --analysis <analysis.json> --out <dir>
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import numpy as np  # noqa: E402
from matplotlib import colors as mcolors  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402
from paperkit import Canvas, ROLE, INK, MUTED, mix  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ANALYSIS = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "experiment"), "analysis.json")

HERO = ROLE["blue"]
ABL = "#7FA6D9"                       # ablation of the hero (verified, no history): hero hue, lighter
GREY_D, GREY_L = "#5E6875", "#8E99A8"  # baselines
GRID = "#E6E9ED"
TICK = "#5A626D"
COL = {"verified": HERO["mark"], "no_history": ABL, "unfiltered": GREY_D, "none": GREY_L}
INKC = {"verified": HERO["ink"], "no_history": "#3F6FAE", "unfiltered": GREY_D, "none": "#6E7886"}
NAME = {"verified": "Verified", "no_history": "No history", "unfiltered": "Unfiltered", "none": "No memory"}
W, H = 178, 124
TOP_Y, TOP_H = 63.0, 59.0          # top row cards
BOT_Y, BOT_H = 2.0, 58.5           # bottom row cards
LX, LW, RX, RW = 2.0, 101.0, 105.5, 70.5


def card(cv, x, y, w, h, title, sub):
    cv.group(x, y, w, h, "neutral", title, band=True, size=7.6, radius=2.0, lw=0.6, fill="white")
    cv.text(x + 2.0, y + h - 7.6, sub, size=6.2, color=MUTED, ha="left", style="italic")


def sgn(v, nd=1):
    s = f"{v:+.{nd}f}"
    return s.replace("-", "−")


def ci(lo, hi):
    return f"[{sgn(lo)}, {sgn(hi)}]"


# ------------------------------------------------------------------ (a) ---
def panel_effects(cv, A):
    card(cv, LX, TOP_Y, LW, TOP_H, "(a) Paired success changes",
         "percentage points · ○ = 24 seed blocks · bar = paired 95% CI")
    rows = [("verified", "unfiltered"), ("verified", "no_history"), ("verified", "none"), ("unfiltered", "none")]
    con = {(c["left"], c["right"]): c for c in A["contrasts"]}
    x0, x1, lo, hi = 36.0, 82.0, -3.0, 12.5

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    ys = [TOP_Y + 41.5 - i * 9.0 for i in range(4)]
    yb = ys[-1] - 6.0
    for v in (0, 5, 10):
        cv.ax.plot([X(v)] * 2, [yb, ys[0] + 4.1], color="#9AA0A8" if v == 0 else GRID,
                   lw=0.6 if v == 0 else 0.5, zorder=1.6)
        cv.text(X(v), yb - 2.4, sgn(v, 0) if v else "0", size=6.2, color=TICK)
    cv.ax.plot([x0, x1], [yb, yb], color="#9AA0A8", lw=0.6, zorder=1)
    cv.text((x0 + x1) / 2, yb - 5.2, "success difference (pp)", size=6.3, color=MUTED)
    rng = np.random.default_rng(7)
    out = {}
    for i, (l, r) in enumerate(rows):
        c, y, hero = con[(l, r)], ys[i], i == 0
        if hero:
            cv.box(LX + 1.2, y - 4.1, LW - 2.4, 8.2, "blue", fill=HERO["fill"], stroke="none", lw=0, radius=1.2, z=1.5)
        mc = HERO["mark"] if hero else GREY_D
        lab = f"{NAME[l]} − {NAME[r].lower()}"
        cv.text(4.2, y, lab, size=6.9 if hero else 6.6, color=HERO["ink"] if hero else INK,
                weight="bold" if hero else "normal", ha="left")
        sv = np.asarray(c["seed_values"])
        jit = rng.uniform(-2.3, 2.3, sv.size)
        for v, j in zip(sv, jit):
            cv.ax.add_patch(Circle((X(v), y + j), 0.42, fc="white",
                                   ec=HERO["stroke"] if hero else "#A3ACB8", lw=0.4, zorder=4))
        cv.ax.plot([X(c["lo"]), X(c["hi"])], [y, y], color=mc, lw=2.2 if hero else 1.6,
                   solid_capstyle="round", zorder=5)
        cv.ax.add_patch(Circle((X(c["mean"]), y), 1.05 if hero else 0.8, fc=mc, ec="white", lw=0.6, zorder=6))
        if hero:
            cv.text(LX + LW - 2.0, y + 1.3, f"{sgn(c['mean'])} pp", size=9.0, color=HERO["ink"],
                    weight="bold", ha="right")
            cv.text(LX + LW - 2.0, y - 2.3, ci(c["lo"], c["hi"]), size=6.2, color=HERO["ink"], ha="right")
        else:
            cv.text(LX + LW - 2.0, y + 1.2, sgn(c["mean"]), size=7.2, color=INK, weight="bold", ha="right")
            cv.text(LX + LW - 2.0, y - 2.2, ci(c["lo"], c["hi"]), size=6.2, color=MUTED, ha="right")
        out[(l, r)] = c
    cv.text(4.2, ys[1] - 3.0, "history ablation", size=6.0, color=MUTED, ha="left", style="italic")
    return out


# ------------------------------------------------------------------ (b) ---
def panel_hetero(cv, A):
    card(cv, RX, TOP_Y, RW, TOP_H, "(b) Gain by task and budget",
         "verified − unfiltered, pp · ○ = CI includes 0")
    het = A["heterogeneity"]
    fams = [f["name"] for f in A["config"]["task_families"]]
    buds = A["config"]["budgets_tokens"]
    gx, cw, ch = 125.0, 12.2, 8.6
    gtop = TOP_Y + 42.5
    cm = mcolors.LinearSegmentedColormap.from_list("hero", ["#FFFFFF", HERO["soft"], HERO["stroke"], HERO["ink"]])
    vmax = 14.0
    cv.text(gx + 2 * cw, gtop + 5.6, "memory budget (tokens)", size=6.2, color=MUTED, style="italic")
    for j, b in enumerate(buds):
        cv.text(gx + (j + 0.5) * cw, gtop + 2.0, f"{b:,}", size=6.4, color=TICK)
    zero_ci = []
    for i, fam in enumerate(fams):
        yy = gtop - (i + 1) * ch
        cv.text(gx - 1.6, yy + ch / 2, fam, size=6.6, color=INK, ha="right")
        for j in range(len(buds)):
            m, lo_, hi_ = het["mean"][i][j], het["lo"][i][j], het["hi"][i][j]
            t = max(m, 0) / vmax
            cv.ax.add_patch(Rectangle((gx + j * cw, yy), cw, ch, fc=cm(t), ec="white", lw=0.8, zorder=4))
            dark = t > 0.55
            cv.text(gx + (j + 0.5) * cw, yy + ch / 2, sgn(m), size=6.8, color="white" if dark else HERO["ink"],
                    weight="bold" if m >= 10 else "normal", z=6)
            if lo_ <= 0 <= hi_:
                zero_ci.append((fam, b := buds[j]))
                cv.ax.add_patch(Circle((gx + (j + 0.5) * cw + 4.3, yy + ch / 2 + 0.2), 0.6, fc="none",
                                       ec=HERO["ink"], lw=0.5, zorder=7))
    # range callout: smallest vs largest cell
    flat = [(het["mean"][i][j], i, j) for i in range(4) for j in range(4)]
    mn, mx = min(flat), max(flat)
    cv.rich(RX + RW / 2, TOP_Y + 2.6, [("range ", MUTED), (sgn(mn[0]), HERO["ink"], "bold"),
                                     (f" ({fams[mn[1]].lower()}, {buds[mn[2]]:,}) to ", MUTED),
                                     (sgn(mx[0]), HERO["ink"], "bold"),
                                     (f" ({fams[mx[1]].lower()}, {buds[mx[2]]:,})", MUTED)], size=6.1, ha="center")
    return zero_ci, mn, mx


# ------------------------------------------------------------------ (c) ---
def panel_cost(cv, A):
    card(cv, LX, BOT_Y, LW, BOT_H, "(c) Success versus token cost",
         "mean over task families · budgets 256–2,048 tokens · 95% CI on both axes")
    T = A["tradeoff"]
    ax = cv.axes(15.0, BOT_Y + 11.0, 71.0, 36.0)
    ax.set_xlim(2.95, 4.55)
    ax.set_ylim(50, 70)
    ax.set_xticks([3.0, 3.5, 4.0, 4.5])
    ax.set_xticklabels(["3.0", "3.5", "4.0", "4.5"])
    ax.set_yticks([50, 55, 60, 65, 70])
    ax.grid(axis="y", color=GRID, lw=0.5)
    ax.tick_params(labelsize=6.2, labelcolor=TICK)
    ax.patch.set_alpha(0)
    cv.text(LX + 3.4, BOT_Y + 29.0, "success (%)", size=6.3, color=MUTED, rotation=90)
    cv.text(50.5, BOT_Y + 4.0, "model tokens per episode (×10³)", size=6.3, color=MUTED)
    style = {"verified": dict(lw=1.9, ms=4.4, mfc=HERO["mark"], ls="-", z=6),
             "no_history": dict(lw=1.1, ms=3.4, mfc="white", ls=(0, (3, 1.6)), z=5),
             "unfiltered": dict(lw=1.0, ms=3.2, mfc=GREY_D, ls="-", z=4),
             "none": dict(lw=1.0, ms=3.2, mfc=GREY_L, ls="-", z=4)}
    pts = {}
    for p in ("none", "unfiltered", "no_history", "verified"):
        s, t = T[p]["success"], T[p]["tokens"]
        k = 1 if p == "none" else 4      # no memory ignores the budget: plot once
        xs, ys = t["mean"][:k], s["mean"][:k]
        st = style[p]
        ax.errorbar(xs, ys, yerr=[np.subtract(ys, s["lo"][:k]), np.subtract(s["hi"][:k], ys)],
                    xerr=[np.subtract(xs, t["lo"][:k]), np.subtract(t["hi"][:k], xs)],
                    fmt="none", ecolor=mix(COL[p], "#FFFFFF", 0.35), elinewidth=0.6, capsize=0, zorder=st["z"] - 1)
        ax.plot(xs, ys, color=COL[p], lw=st["lw"], ls=st["ls"], marker="o", ms=st["ms"], mfc=st["mfc"],
                mec=COL[p] if p == "no_history" else "white", mew=0.8 if p == "no_history" else 0.6, zorder=st["z"],
                solid_capstyle="round")
        pts[p] = list(zip(xs, ys))
    # budget labels on the hero line
    for (x, y), b, (dx, dy) in zip(pts["verified"], A["config"]["budgets_tokens"],
                                   ((-0.035, 0.0), (0.06, -1.8), (0.0, 1.9), (-0.02, 2.0))):
        ax.text(x + dx, y + dy, f"{b:,}", fontsize=6.0, color=HERO["ink"],
                ha="left" if dx > 0 else ("right" if dx < 0 else "center"),
                va="center", zorder=8)
    # direct labels
    ex, ey = pts["verified"][-1]
    ax.text(4.03, 68.6, "Verified", fontsize=7.0, color=HERO["ink"], weight="bold", ha="left", va="center")
    hx, hy = pts["no_history"][-1]
    sx, sy = pts["no_history"][0]
    ax.text(sx - 0.07, sy + 2.4, "No history", fontsize=6.5, color=INKC["no_history"], ha="right", va="center")
    ux, uy = pts["unfiltered"][-1]
    ax.text(ux + 0.04, uy - 1.9, "Unfiltered", fontsize=6.5, color=GREY_D, ha="left", va="center")
    nx, ny = pts["none"][0]
    ax.text(nx + 0.05, ny - 1.6, "No memory", fontsize=6.5, color=INKC["none"], ha="left", va="center")
    # gap callout at the largest budget: verified minus unfiltered means
    gap = ey - uy
    bx = 4.50
    for yy, xx in ((ey, ex), (uy, ux)):
        ax.plot([xx + 0.03, bx], [yy, yy], color=HERO["stroke"], lw=0.5, ls=(0, (1.5, 1.2)), zorder=3)
    ax.plot([bx, bx], [uy, ey], color=HERO["mark"], lw=0.8, zorder=7)
    for yy in (uy, ey):
        ax.plot([bx - 0.015, bx], [yy, yy], color=HERO["mark"], lw=0.8, zorder=7)
    ax.text(bx + 0.02, (uy + ey) / 2 + 1.0, f"{sgn(gap)} pp", fontsize=7.6, color=HERO["ink"], weight="bold",
            ha="left", va="center", clip_on=False)
    ax.text(bx + 0.02, (uy + ey) / 2 - 1.4, "at 2,048", fontsize=6.0, color=MUTED, ha="left", va="center",
            clip_on=False, style="italic")
    return gap


# ------------------------------------------------------------------ (d) ---
def panel_diag(cv, A):
    card(cv, RX, BOT_Y, RW, BOT_H, "(d) Rejection-history diagnostic",
         "events per 100 episodes · history uses 25% of capacity")
    pol = A["config"]["policies"]
    D = A["diagnostics"]
    order = ["none", "unfiltered", "no_history", "verified"]
    ys = {p: BOT_Y + 36.5 - i * 6.6 for i, p in enumerate(order)}
    for p in order:
        hero = p == "verified"
        cv.text(RX + 2.0, ys[p], NAME[p], size=6.8 if hero else 6.6, color=INKC[p],
                weight="bold" if hero else "normal", ha="left")
    axes = [("corrupt_read", "corrupted reads", 123.5, 20.0, (0, 10, 20)),
            ("repeat_invalid_write", "repeat invalid writes", 150.0, 15.0, (0, 5, 10, 15))]
    ratios = {}
    yb = ys["verified"] - 5.0
    for key, title, ax0, vmax, ticks in axes:
        aw = 18.0

        def X(v):
            return ax0 + v / vmax * aw
        cv.text(ax0 + aw / 2, ys["none"] + 5.2, title, size=6.4, color=INK)
        for v in ticks:
            cv.ax.plot([X(v)] * 2, [yb, ys["none"] + 2.6], color="#9AA0A8" if v == 0 else GRID,
                       lw=0.6 if v == 0 else 0.5, zorder=1)
            cv.text(X(v), yb - 2.3, f"{v}", size=6.2, color=TICK)
        cv.ax.plot([ax0, ax0 + aw], [yb, yb], color="#9AA0A8", lw=0.6, zorder=1)
        d = D[key]
        for p in order:
            k = pol.index(p)
            m, lo_, hi_ = d["mean"][k], d["lo"][k], d["hi"][k]
            hero = p == "verified"
            cv.ax.plot([X(lo_), X(hi_)], [ys[p]] * 2, color=COL[p], lw=1.6, solid_capstyle="round", zorder=5)
            cv.ax.add_patch(Circle((X(m), ys[p]), 0.95 if hero else 0.75,
                                   fc="white" if p == "no_history" else COL[p],
                                   ec=COL[p] if p == "no_history" else "white", lw=0.6, zorder=6))
            right = hi_ < 0.6 * vmax      # label beside the interval, on the side with room
            cv.text(X(hi_) + 1.4 if right else X(lo_) - 1.4, ys[p], f"{m:.1f}", size=6.4, color=INKC[p],
                    weight="bold" if hero else "normal", ha="left" if right else "right")
        r = d["mean"][pol.index("no_history")] / d["mean"][pol.index("verified")]
        ratios[key] = r
        # ratio bracket between no-history and verified rows, at the axis' right side
        bx = ax0 + aw + 0.6
        cv.line([(bx - 0.8, ys["no_history"]), (bx, ys["no_history"]), (bx, ys["verified"]),
                 (bx - 0.8, ys["verified"])], color=HERO["mark"], lw=0.7, radius=0.3)
        cv.text(bx + 0.7, (ys["no_history"] + ys["verified"]) / 2, f"{r:.1f}×", size=7.4, color=HERO["ink"],
                weight="bold", ha="left")
    q = next(c for c in A["contrasts"] if (c["left"], c["right"]) == ("verified", "no_history"))
    cv.rich(RX + RW / 2, yb - 6.0, [("fewer errors with history, yet success ", MUTED),
                                    (f"{sgn(q['mean'])} pp", HERO["ink"], "bold"), (" in (a)", MUTED)],
            size=6.1, ha="center")
    return ratios


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", default=DEFAULT_ANALYSIS)
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    A = json.load(open(a.analysis))
    assert A["data_status"].startswith("SYNTHETIC DATA")
    cv = Canvas(W, H, family="serif", size=7.0)
    con = panel_effects(cv, A)
    zero_ci, mn, mx = panel_hetero(cv, A)
    gap = panel_cost(cv, A)
    ratios = panel_diag(cv, A)
    # in-art status tag (data could be mistaken for results)
    cv.chip(RX + RW - 2.0, TOP_Y + TOP_H - 2.35, "SYNTHETIC DATA", "amber", size=6.0, ha="right", z=12)

    # ---- plotted values tied to analysis.json
    p = con[("verified", "unfiltered")]
    assert (sgn(p["mean"]), sgn(p["lo"]), sgn(p["hi"])) == ("+6.6", "+6.0", "+7.1")
    q = con[("verified", "no_history")]
    assert (sgn(q["mean"]), sgn(q["lo"]), sgn(q["hi"])) == ("+0.0", "−0.4", "+0.5")
    assert sgn(con[("verified", "none")]["mean"]) == "+9.7" and sgn(con[("unfiltered", "none")]["mean"]) == "+3.1"
    assert all(len(c["seed_values"]) == A["config"]["n_seeds"] == 24 for c in A["contrasts"])
    assert zero_ci == [("Fact recall", 256), ("Fact recall", 512)], zero_ci
    assert (sgn(mn[0]), sgn(mx[0])) == ("+0.3", "+12.5")
    # (c) gap of means equals the family-average paired difference at 2,048 (linearity)
    assert abs(gap - np.mean([r[3] for r in A["heterogeneity"]["mean"]])) < 1e-9 and sgn(gap) == "+9.1"
    assert f"{ratios['corrupt_read']:.1f}" == "2.2" and f"{ratios['repeat_invalid_write']:.1f}" == "4.2"
    assert A["config"]["history_fraction"] == 0.25 and A["config"]["bootstrap_replicates"] == 20000
    print("\n".join(cv.save(os.path.join(a.out, "memory_policy_study"))))


if __name__ == "__main__":
    main()
