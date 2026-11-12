#!/usr/bin/env python3
"""Causal cache attention: one column grid for the cache, the mask and a worked read.

Source: gallery/before/attention.png (an original schematic with an illustrative numerical
example; it makes no empirical claim) and the bundled data/attention/inputs.json and
numerical_checks.json.

Content kept from the source
  * the eight cache slots in canonical order: prefix P0/P1, completed-chunk summaries S1/S2
    (of t1-t4 and t5-t8) and the current chunk's local keys t9-t12, each holding a key and a value;
  * the 4 x 8 additive mask M for queries q9-q12 (0 = permitted, -inf = blocked; a local key
    t_j is readable iff j <= i, the current token included) and its row counts 5, 6, 7, 8;
  * A = rowsoftmax(Q K^T / sqrt(d_k) + M), O = A V and the tensor shapes;
  * the worked read for q10: six supplied logits, their softmax weights, the six 2-D value
    vectors, the weighted contributions and o10 = (0.600050, 0.730184) shown to three decimals;
  * the availability rule for S3: absent from the key bank for q9-q12, formed from t9-t12 once
    chunk 3 is sealed, eligible for later reads.

Design
  * Five-second message: every query reads the prefix, the finished summaries and its own causal
    past; nothing from the future. The hero is the mask, whose staircase is the claim.
  * One column grid is shared by the cache slots, the mask and the worked row, so a key keeps its
    x position from the object that stores it to the weight it receives. An amber wire carries
    the q10 row from the mask into panel (c).
  * One hue per key group everywhere (slot, mask cell, bar, value cell, scatter marker):
    blue = prefix, purple = chunk summary, green = current-chunk local key. Amber is the worked
    query q10 and its output only. Grey hatching is "blocked / not instantiated" only.
  * Panel (c) replaces the six-decimal table by the calculation drawn on the grid (logits, weight
    bars, value vectors, weighted vectors, row sum) and a value-space scatter whose marker areas
    are the weights, so o10 reads as the weighted mean of the six points.
  * Every number is computed here from inputs.json and asserted against numerical_checks.json.
    The invented numbers carry an in-figure "illustrative values" tag; schematic status and the
    illustrative key/value shading belong in the caption.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import matplotlib  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Polygon, Rectangle  # noqa: E402
from paperkit import INK, MUTED, ROLE, Canvas, _round_top_rect  # noqa: E402

DATA = HERE / "data" / "attention"
PRE, SUM, LOC, QRY = "blue", "purple", "memory", "amber"
HATCH_FC, HATCH_EC = "#F1F2F5", "#AEB5BF"


# ------------------------------------------------------------------ data ---
def derive(inputs, checks):
    """Rebuild the mask and the q10 read from the inputs; assert every value against the checks."""
    I, C = json.loads(Path(inputs).read_text()), json.loads(Path(checks).read_text())
    keys, qs = I["key_order"], I["query_indices"]
    assert keys == C["key_order"] and qs == C["query_indices"]
    summaries = {s["id"]: s["covers"] for s in I["completed_summaries"]}
    always = set(I["prefix_keys"]) | set(summaries)
    local = {f"t{j}": j for j in I["local_token_indices"]}
    assert set(keys) == always | set(local)
    group = {k: PRE if k in I["prefix_keys"] else SUM if k in summaries else LOC for k in keys}
    permitted = [[int(k in always or local.get(k, math.inf) <= i) for k in keys] for i in qs]
    assert permitted == C["permitted_mask"]
    assert [[0 if p else "-Infinity" for p in row] for row in permitted] == C["additive_mask"]
    counts = [sum(r) for r in permitted]
    assert counts == C["permitted_counts"]
    s3 = I["excluded_summary"]
    assert s3["id"] not in keys and s3["excluded_from_queries"] == qs and s3["covers"] == qs

    ex = I["example"]
    row = qs.index(ex["query_index"])
    assert [k for k, p in zip(keys, permitted[row]) if p] == ex["allowed_keys"]
    assert [k for k, p in zip(keys, permitted[row]) if not p] == ex["masked_keys"]
    getcontext().prec = 70
    tol = Decimal("1e-50")
    logits = [Decimal(s) for s in ex["scaled_logits_decimal"]]
    exps = [x.exp() for x in logits]
    Z = sum(exps)
    w = [e / Z for e in exps]
    contrib = [[a * v for v in vv] for a, vv in zip(w, ex["value_vectors"])]
    out = [sum(c[d] for c in contrib) for d in range(I["dimensions"]["example_value_dimension"])]
    q = C["q10"]
    assert abs(Z - Decimal(q["softmax_normalizer"])) < tol
    assert all(abs(a - Decimal(b)) < tol for a, b in zip(w, q["softmax_weights"]))
    assert all(abs(a - Decimal(b)) < tol for a, b in zip(w + [Decimal(0)] * 2, C["q10_full_attention"]))
    assert all(abs(a - Decimal(b)) < tol for r, s in zip(contrib, q["weighted_value_contributions"])
               for a, b in zip(r, s))
    assert all(abs(a - Decimal(b)) < tol for a, b in zip(out, q["weighted_output"]))
    assert abs(sum(w) - 1) < tol and C["checks"]["passed"]
    return dict(I=I, keys=keys, qs=qs, group=group, permitted=permitted, counts=counts, row=row,
                summaries=summaries, s3=s3, logits=[float(x) for x in logits], Z=float(Z),
                w=[float(x) for x in w], values=ex["value_vectors"],
                contrib=[[float(x) for x in r] for r in contrib], out=[float(x) for x in out])


def num(x, nd=3):
    """0.232, 0, -0.155 with a true minus."""
    s = "0" if abs(x) < 5 * 10 ** -(nd + 1) else f"{x:.{nd}f}"
    return s.replace("-", "−")


# --------------------------------------------------------------- helpers ---
def hatch(cv, x, y, w, h, z=6.0, dashed=False):
    """Blocked / not-instantiated cell: grey hatching (the only meaning of hatching here)."""
    cv.ax.add_patch(Rectangle((x, y), w, h, fc=HATCH_FC, ec=HATCH_EC, hatch="////", lw=0, zorder=z))
    cv.ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=HATCH_EC, lw=0.45, zorder=z + 0.05,
                              ls=(0, (2, 1.4)) if dashed else "-"))


def cell(cv, x, y, w, h, r, s=None, z=6.0, size=6.5, weight="normal", strong=False):
    c = ROLE[r]
    cv.ax.add_patch(Rectangle((x, y), w, h, fc=c["soft"] if strong else c["fill"], ec=c["stroke"], lw=0.45, zorder=z))
    if s is not None:
        cv.text(x + w / 2, y + h / 2 - 0.05, s, size=size, color=c["ink"], weight=weight, z=z + 1)


def slot(cv, x, y, w, h, r, label, seed=0, ghost=False):
    """Cache slot as an object: solid name band over a key strip and a value strip."""
    c = ROLE[r]
    hb = 3.5
    cv.box(x, y, w, h, r, fill="white", lw=0.7, radius=1.0, dashed=ghost, z=5)
    if ghost:
        cv.text(x + w / 2, y + h - hb / 2 - 0.2, label, size=6.6, weight="bold", color=c["ink"], z=7)
        cv.icon_lock(x + w / 2, y + (h - hb) / 2 + 0.1, 2.9, color=c["stroke"])
        return
    cv.ax.add_patch(PathPatch(_round_top_rect(x, y + h - hb, w, hb, 1.0), fc=c["mark"], ec=c["mark"], lw=0.7, zorder=5.2))
    cv.text(x + w / 2, y + h - hb / 2 - 0.05, label, size=6.6, weight="bold", color="white", z=7)
    cs = 1.25
    x0, yy = x + (w - 5 * cs - 1.2) / 2, y + (h - hb - cs) / 2
    cv.vec(x0, yy, n=3, cell=cs, r=r, seed=seed)                 # key  (d_k cells, illustrative shading)
    cv.vec(x0 + 3 * cs + 1.2, yy, n=2, cell=cs, r=r, seed=seed + 50)  # value (d_v cells)


# ------------------------------------------------------------------ draw ---
def draw(d):
    W, H = 178.0, 118.0
    cv = Canvas(W, H)
    matplotlib.rcParams["hatch.linewidth"] = 0.45
    keys, qs, grp, K = d["keys"], d["qs"], d["group"], len(d["keys"])
    amber = ROLE[QRY]

    # shared column grid: 8 key columns, a small gap between the three key groups
    CW, GX, GAP = 10.0, 28.0, 1.4
    order = [PRE, SUM, LOC]
    xs = [GX + j * CW + GAP * order.index(grp[k]) for j, k in enumerate(keys)]
    span = {g: (min(x for x, k in zip(xs, keys) if grp[k] == g), max(x for x, k in zip(xs, keys) if grp[k] == g) + CW)
            for g in order}
    XR = xs[-1] + CW

    # ============================== (a) cache and mask ==========================================
    AX, AY, AW, AH = 1.5, 60.5, 118.5, 54.7
    cv.section(AX, AY, AW, AH, "neutral", "Cache slots and causal mask", letter="a", fill="#FAFBFC")
    names = {PRE: "Prefix", SUM: "Chunk summaries", LOC: "Current chunk: local keys"}
    for g in order:
        x0, x1 = span[g]
        cv.text((x0 + x1) / 2, 110.9, names[g], size=7.0, weight="bold", color=ROLE[g]["ink"])
        cv.ax.plot([x0 + 0.5, x1 - 0.5], [109.0, 109.0], color=ROLE[g]["mark"], lw=1.1, zorder=4, solid_capstyle="round")
    cv.text(sum(span[PRE]) / 2, 106.4, "always readable", size=6.5, style="italic", color=MUTED)
    cv.text(sum(span[LOC]) / 2, 106.4, r"$t_j$ readable iff $j \leq i$ (self included)", size=6.5,
            style="italic", color=MUTED)

    BY, BH = 93.4, 9.0
    for j, k in enumerate(keys):
        slot(cv, xs[j] + 0.5, BY, CW - 1.0, BH, grp[k], k, seed=j)
        if k in d["summaries"]:  # the finished chunk each summary stands for
            cover = d["summaries"][k]
            tw, tg = 2.3, 0.25
            tx = xs[j] + (CW - len(cover) * tw - (len(cover) - 1) * tg) / 2
            cv.tokens(tx, 104.9, len(cover), w=tw, h=3.0, r="neutral", gap=tg, labels=[f"t{i}" for i in cover], size=5.8)
            cv.arrow([(xs[j] + CW / 2, 104.9), (xs[j] + CW / 2, BY + BH)], lw=0.65, head=1.2)
    cv.text(26.3, 100.5, "Cache slots", size=6.8, weight="bold", ha="right")
    cv.text(26.3, 97.7, "key | value each", size=5.9, style="italic", color=MUTED, ha="right")
    cv.text(26.3, 94.9, r"$\mathbf{K}$: 8$\times$$d_k$   $\mathbf{V}$: 8$\times$$d_v$", size=6.5, ha="right")

    MT, RH = 91.0, 5.5
    for i, q in enumerate(qs):
        y = MT - (i + 1) * RH
        hot = i == d["row"]
        cv.box(17.0, y + 0.65, 9.0, RH - 1.3, QRY if hot else "neutral", f"q{q}", size=6.6, radius=0.9,
               fill=amber["mark"] if hot else None, title_color="white" if hot else None, name=f"q{q}")
        for j, k in enumerate(keys):
            if d["permitted"][i][j]:
                cell(cv, xs[j], y, CW, RH, grp[k], "0", strong=True)
            else:
                hatch(cv, xs[j], y, CW, RH)
                cv.text(xs[j] + CW / 2, y + RH / 2, "−∞", size=6.5, color="#59616D", z=7,
                        bbox=dict(fc=HATCH_FC, ec="none", pad=0.5))
        cv.text(XR + 4.4, y + RH / 2, f"{d['counts'][i]} keys", size=6.2, color=amber["ink"] if hot else MUTED,
                weight="bold" if hot else "normal")
    cv.text(XR + 4.4, MT + 1.6, "readable", size=5.9, style="italic", color=MUTED)
    cv.solids.append((xs[0], MT - len(qs) * RH, XR - xs[0], len(qs) * RH, "mask matrix", None))
    yh = MT - (d["row"] + 1) * RH
    cv.ax.add_patch(Rectangle((xs[0] - 0.35, yh - 0.05), XR - xs[0] + 0.7, RH + 0.1, fc="none", ec=amber["mark"],
                              lw=1.3, zorder=9))
    cv.text(7.0, MT - len(qs) * RH / 2, r"mask $\mathbf{M}$ (4 $\times$ 8)", size=6.4, rotation=90, color=INK)

    cv.text(GX, 64.8, r"$\mathbf{A}=\mathrm{rowsoftmax}(\mathbf{Q}\mathbf{K}^{\top}/\sqrt{d_k}+\mathbf{M})$,"
            r"   $\mathbf{O}=\mathbf{A}\mathbf{V}$", size=6.9, ha="left")
    lx = 82.5
    for n, g in enumerate(order):
        cv.ax.add_patch(Rectangle((lx + n * 1.5, 63.5), 1.5, 2.6, fc=ROLE[g]["soft"], ec=ROLE[g]["stroke"], lw=0.4, zorder=6))
    cv.text(lx + 5.3, 64.8, "0: permitted", size=6.0, ha="left", color=INK)
    hatch(cv, lx + 19.5, 63.5, 3.4, 2.6)
    cv.text(lx + 23.7, 64.8, "−∞: blocked", size=6.0, ha="left", color=INK)

    # ============================== (b) summary availability ===================================
    BX, BW = 123.0, 53.5
    cv.section(BX, AY, BW, AH, SUM, "Summary availability", letter="b")
    s3 = d["s3"]
    seal, tw, tg, tx0 = 152.6, 5.8, 0.7, 125.6
    cv.text(tx0 + (4 * tw + 3 * tg) / 2, 110.9, "chunk 3 open", size=6.8, weight="bold", color=ROLE[LOC]["ink"])
    cv.text((seal + BX + BW) / 2 + 2.6, 110.9, "sealed", size=6.8, weight="bold", color=ROLE[SUM]["ink"])
    cv.line([(seal, 69.8), (seal, 108.6)], color="#3A4250", lw=0.8, dashed=True)
    cv.tab(seal - 3.6, 108.6, 7.2, 3.6, "neutral", "seal", size=6.2, solid=True)
    cv.text(tx0, 106.6, "query step", size=5.9, style="italic", color=MUTED, ha="left")
    for n, q in enumerate(qs):
        hot = n == d["row"]
        cv.box(tx0 + n * (tw + tg), 100.6, tw, 4.2, QRY if hot else "neutral", f"q{q}", size=6.2, radius=0.9,
               fill=amber["mark"] if hot else None, title_color="white" if hot else None)
    cv.text(tx0, 97.3, "local keys written", size=5.9, style="italic", color=MUTED, ha="left")
    cv.tokens(tx0, 91.2, 4, w=tw, h=4.2, r=LOC, gap=tg, labels=[f"t{i}" for i in s3["covers"]], size=6.2)
    cv.text(tx0, 87.9, f"summary {s3['id']}", size=5.9, style="italic", color=MUTED, ha="left")
    gx1 = tx0 + 4 * tw + 3 * tg
    cv.box(tx0, 80.0, gx1 - tx0, 6.0, SUM, fill="white", dashed=True, radius=1.0, lw=0.7)
    cv.icon_lock(tx0 + 3.2, 83.0, 2.8, color=ROLE[SUM]["stroke"])
    cv.text(tx0 + 5.6, 83.0, f"{s3['id']} withheld", size=6.6, weight="bold", color=ROLE[SUM]["ink"], ha="left")
    cv.text(tx0, 76.8, f"{s3['id']} $\\notin$ key bank for q{qs[0]}–q{qs[-1]}", size=6.0, ha="left")
    # sealing: the four local keys are summarised into S3 (the summariser itself is unspecified -> neutral)
    cv.arrow([(gx1, 93.3), (155.4, 93.3)], lw=0.7, head=1.3)
    cv.trap(155.4, 90.3, 11.0, 6.0, "neutral", narrow="right", title="summarize", size=5.9)
    sx = 165.0
    cv.arrow([(166.4, 93.3), (sx + 4.8, 93.3), (sx + 4.8, 87.0)], lw=0.7, head=1.3, color=ROLE[SUM]["mark"])
    slot(cv, sx, 78.0, 9.6, 9.0, SUM, s3["id"], seed=9)
    zc = (seal + BX + BW) / 2
    cv.text(zc, 75.4, f"covers t{s3['covers'][0]}–t{s3['covers'][-1]}", size=6.0)
    cv.text(zc, 72.6, "eligible for later reads", size=6.0, color=ROLE[SUM]["ink"], weight="bold")
    cv.arrow([(tx0, 66.6), (BX + BW - 2.4, 66.6)], color=MUTED, lw=0.6, head=1.3)
    cv.text(BX + BW - 2.6, 64.3, "time", size=5.9, style="italic", color=MUTED, ha="right")

    # ============================== (c) worked read for q10 ====================================
    CY, CH = 1.5, 54.5
    cv.section(AX, CY, W - 2 * AX, CH, QRY, f"Worked read for q{qs[d['row']]}", letter="c")
    allowed = d["permitted"][d["row"]]
    it = iter(range(K))
    col = [next(it) if p else None for p in allowed]  # column -> index into the six permitted keys

    # row 0: which key each column is
    cv.box(9.0, 48.1, 9.0, 4.2, QRY, f"q{qs[d['row']]}", size=6.6, radius=0.9, fill=amber["mark"], title_color="white")
    for j, k in enumerate(keys):
        c = ROLE[grp[k]]
        cv.ax.add_patch(FancyBboxPatch((xs[j] + 0.5, 48.4), CW - 1.0, 3.6, boxstyle="round,pad=0,rounding_size=0.9",
                                       fc=c["soft"] if allowed[j] else "white", ec=c["stroke"], lw=0.5, zorder=6))
        cv.text(xs[j] + CW / 2, 50.15, k, size=6.3, weight="bold", color=c["ink"] if allowed[j] else MUTED, z=7)
    cv.text(26.3, 50.2, "key", size=6.4, ha="right")
    # the mask row of q10 feeds this panel
    cv.arrow([(17.0, yh + RH / 2), (13.5, yh + RH / 2), (13.5, 52.3)], color=amber["mark"], lw=0.95, head=1.5)

    # row 1: scaled logits + mask
    L0, LH = 42.6, 5.0
    for j, k in enumerate(keys):
        if allowed[j]:
            cell(cv, xs[j], L0, CW, LH, grp[k], f"{d['logits'][col[j]]:.1f}", strong=True)
        else:
            hatch(cv, xs[j], L0, CW, LH)
            cv.text(xs[j] + CW / 2, L0 + LH / 2, "−∞", size=6.5, color="#59616D", z=7,
                    bbox=dict(fc=HATCH_FC, ec="none", pad=0.5))
    cv.text(26.3, L0 + LH / 2, r"logit $\ell$ + mask", size=6.4, ha="right")

    # row 2: softmax weights as bars on a common zero baseline
    B0, BMAX = 29.0, 8.6
    top = max(d["w"])
    cv.ax.plot([xs[0], XR], [B0, B0], color="#9AA0A8", lw=0.6, zorder=5)
    for j, k in enumerate(keys):
        c = ROLE[grp[k]]
        if allowed[j]:
            a = d["w"][col[j]]
            bh = BMAX * a / top
            cv.ax.add_patch(Rectangle((xs[j] + 1.9, B0), CW - 3.8, bh, fc=c["mark"], ec=c["ink"], lw=0.4, zorder=6))
            cv.text(xs[j] + CW / 2, B0 + bh + 1.45, num(a), size=6.3, color=c["ink"], weight="bold")
        else:
            cv.text(xs[j] + CW / 2, B0 + 1.45, "0", size=6.3, color=MUTED)
    cv.text(26.3, 34.6, r"weight $a = e^{\ell}/Z$", size=6.5, ha="right")
    cv.text(26.3, 31.6, f"$Z$ = {d['Z']:.2f}", size=6.0, ha="right", color=MUTED)
    cv.text(XR + 1.4, 31.2, r"$\sum a = 1$", size=6.2, ha="left", color=MUTED)

    # rows 3-4: value vectors and weighted vectors (two components each)
    V0, A0, SH = 18.6, 8.2, 3.8
    for j, k in enumerate(keys):
        for comp in range(2):
            yv, ya = V0 + (1 - comp) * SH, A0 + (1 - comp) * SH
            if allowed[j]:
                cell(cv, xs[j] + 2.4, yv, CW - 4.8, SH, grp[k], num(d["values"][col[j]][comp], 0), size=6.4)
                cell(cv, xs[j] + 0.5, ya, CW - 1.0, SH, grp[k], num(d["contrib"][col[j]][comp]), size=6.3)
            else:
                hatch(cv, xs[j] + 2.4, yv, CW - 4.8, SH, dashed=True)
                hatch(cv, xs[j] + 0.5, ya, CW - 1.0, SH, dashed=True)
    cv.text(26.3, V0 + SH, r"value $\mathbf{v}$", size=6.4, ha="right")
    cv.text(26.3, A0 + SH, r"weighted $a\,\mathbf{v}$", size=6.4, ha="right")
    for comp in range(2):
        cv.text(XR + 1.4, V0 + (1.5 - comp) * SH, f"$v_{comp + 1}$", size=6.5, ha="left", color=MUTED)
    cv.solids.append((xs[0], A0, XR - xs[0], 2 * SH, "weighted-value row", None))
    ym = A0 + SH
    ox = XR + 8.6
    cv.arrow([(XR - 0.5, ym), (XR + 2.7, ym)], color=amber["mark"], lw=0.9, head=1.3)
    cv.op(XR + 4.4, ym, "Σ", r=QRY, d=3.4)
    cv.arrow([(XR + 6.1, ym), (ox, ym)], color=amber["mark"], lw=0.9, head=1.3)
    for comp in range(2):
        cv.ax.add_patch(Rectangle((ox, A0 + (1 - comp) * SH), 9.0, SH, fc=amber["soft"], ec=amber["mark"], lw=0.8, zorder=6))
        cv.text(ox + 4.5, A0 + (1.5 - comp) * SH - 0.05, num(d["out"][comp]), size=6.6, weight="bold", color=amber["ink"], z=7)
    cv.solids.append((ox, A0, 9.0, 2 * SH, "o10", None))
    cv.text(ox + 4.5, A0 + 2 * SH + 1.7, f"o{qs[d['row']]}", size=6.8, weight="bold", color=amber["ink"])

    cv.chip(3.6, 4.5, "ILLUSTRATIVE VALUES", "neutral", size=5.8, ha="left")
    cv.text(XR, 4.5, f"masked {', '.join(d['I']['example']['masked_keys'])}: weight 0, value not instantiated",
            size=5.9, style="italic", color=MUTED, ha="right")

    # value space: the six permitted values, marker area = weight, o10 = their weighted mean
    S, PX, PY, V1, V2 = 11.2, 135.0, 11.4, (-1.25, 2.25), (-0.3, 2.3)
    P = lambda a, b: (PX + (a - V1[0]) * S, PY + (b - V2[0]) * S)  # noqa: E731
    x0, y0 = P(V1[0], V2[0])
    x1, y1 = P(V1[1], V2[1])
    cv.ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="white", ec="none", zorder=3))
    for t in range(-1, 3):
        gx = P(t, 0)[0]
        cv.ax.plot([gx, gx], [y0, y1], color="#E3E6EA" if t else "#B7BDC6", lw=0.5 if t else 0.7, zorder=3.1)
        cv.ax.plot([gx, gx], [y0, y0 - 0.9], color="#9AA0A8", lw=0.6, zorder=4)
        cv.text(gx, y0 - 2.4, num(t, 0), size=6.0, color="#4A5059")
    for t in range(0, 3):
        gy = P(0, t)[1]
        cv.ax.plot([x0, x1], [gy, gy], color="#E3E6EA" if t else "#B7BDC6", lw=0.5 if t else 0.7, zorder=3.1)
        cv.ax.plot([x0, x0 - 0.9], [gy, gy], color="#9AA0A8", lw=0.6, zorder=4)
        cv.text(x0 - 1.6, gy, num(t, 0), size=6.0, color="#4A5059", ha="right")
    cv.ax.plot([x0, x0, x1], [y1, y0, y0], color="#9AA0A8", lw=0.6, zorder=4)
    cv.text(x1, y0 - 2.4, "$v_1$", size=6.5, ha="right")
    cv.text(x0 - 1.6, y1 - 0.6, "$v_2$", size=6.5, ha="right")
    o = P(*d["out"])
    off = {"P0": (2.6, 2.4, "left"), "P1": (-2.6, 0, "right"), "S1": (2.6, 0.6, "left"), "S2": (0, 3.2, "center"),
           "t9": (0, 3.3, "center"), "t10": (2.8, 0, "left")}
    for j, k in enumerate(keys):
        if not allowed[j]:
            continue
        c, a = ROLE[grp[k]], d["w"][col[j]]
        px, py = P(*d["values"][col[j]])
        area = 9.5 * a / top  # mm^2: marker area is proportional to the weight
        kw = dict(fc=c["mark"], ec="white", lw=0.5, zorder=7)
        if grp[k] == PRE:
            s = math.sqrt(area)
            cv.ax.add_patch(Rectangle((px - s / 2, py - s / 2), s, s, **kw))
        elif grp[k] == SUM:
            s = math.sqrt(4 * area / math.sqrt(3))
            hh = s * math.sqrt(3) / 2
            cv.ax.add_patch(Polygon([(px - s / 2, py - hh / 3), (px + s / 2, py - hh / 3), (px, py + 2 * hh / 3)], **kw))
        else:
            cv.ax.add_patch(Circle((px, py), math.sqrt(area / math.pi), **kw))
        dx, dy, ha = off[k]
        cv.text(px + dx, py + dy, k, size=6.3, weight="bold", color=c["ink"], ha=ha)
    org = P(0, 0)
    for q in ((o[0], org[1]), (org[0], o[1])):  # o10's two coordinates, dropped onto the zero axes
        cv.ax.plot([o[0], q[0]], [o[1], q[1]], color=amber["mark"], lw=0.5, ls=(0, (2, 1.5)), zorder=5)
    cv.arrow([org, o], color=amber["mark"], lw=1.1, head=1.6, z=8)
    cv.ax.add_patch(Circle(o, 0.95, fc=amber["mark"], ec="white", lw=0.5, zorder=9))
    cv.text(o[0] + 2.6, o[1] - 2.3, f"o{qs[d['row']]}", size=6.8, weight="bold", color=amber["ink"], ha="left")
    cv.text(x0 - 3.6, 51.0, r"Value space ($d_v$ = 2)", size=6.9, weight="bold", ha="left")
    cv.rich(x0 - 3.6, 45.6, [(r"$\mathbf{o}_{10}=\Sigma_j\,a_j\mathbf{v}_j$ = ", INK),
                             (f"({num(d['out'][0])}, {num(d['out'][1])})", amber["ink"], "bold")], size=6.9,
            va="baseline")
    cv.text(x1, 4.5, r"marker area $\propto$ weight $a$", size=5.9, style="italic", color=MUTED, ha="right")
    return cv


def build(inputs=DATA / "inputs.json", checks=DATA / "numerical_checks.json"):
    return draw(derive(inputs, checks))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="figures/attention")
    ap.add_argument("--inputs", default=str(DATA / "inputs.json"))
    ap.add_argument("--checks", default=str(DATA / "numerical_checks.json"))
    a = ap.parse_args()
    cv = build(a.inputs, a.checks)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    print("\n".join(cv.save(os.path.join(a.out, "attention"))))


if __name__ == "__main__":
    main()
