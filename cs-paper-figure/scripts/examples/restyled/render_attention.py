"""Restyle of the `attention` example: causal cache attention over a key/value bank.

Content (from inputs.json only):
  bank columns  P0 P1 | S1 S2 | t9 t10 t11 t12   (prefix, completed-chunk summaries, current chunk)
  S1 summarizes t1-t4, S2 summarizes t5-t8; S3 (t9-t12) is absent for q9-q12, eligible after sealing
  M_ij = 0 if key j is prefix/summary or a local token with index <= i, else -inf
  A = rowsoftmax(QK^T / sqrt(d_k) + M),  O = AV
  worked query q10: six supplied scaled logits, six 2-D value vectors -> o10
Every number is recomputed here (60-digit Decimal) and asserted against numerical_checks.json.
k/v cell shading in the bank glyphs is an illustrative texture, not data.

    python render_attention.py [--inputs inputs.json] [--out dir]
"""
import argparse
import json
import os
import sys
from decimal import Decimal, getcontext

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from paperkit import Canvas, ROLE, INK, MUTED, LINE  # noqa: E402

E_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "attention")
PRE, SUM, LOC, QRY, BANK = ROLE["blue"], ROLE["purple"], ROLE["memory"], ROLE["amber"], ROLE["frozen"]
BLK = dict(fill="#F1F3F5", hatch="#AEB6C0", ink="#7A838E", stroke="#B5BCC5")
W, H = 178, 138
SW, SG, GG = 8.6, 1.6, 4.4          # slot width, slot gap, group gap (mm)
X0 = 16.0                           # left edge of the first bank column


# ------------------------------------------------------------------ data ---
def compute(inp, chk):
    getcontext().prec = 60
    keys, qs = inp["key_order"], inp["query_indices"]
    always = set(inp["prefix_keys"]) | {s["id"] for s in inp["completed_summaries"]}
    loc = {f"t{i}": i for i in inp["local_token_indices"]}
    perm = [[1 if (k in always or loc.get(k, 99) <= q) else 0 for k in keys] for q in qs]
    assert perm == chk["permitted_mask"], "mask mismatch"
    assert [sum(r) for r in perm] == chk["permitted_counts"]
    ex = inp["example"]
    qrow = perm[qs.index(ex["query_index"])]
    assert [k for k, p in zip(keys, qrow) if p] == ex["allowed_keys"]
    assert [k for k, p in zip(keys, qrow) if not p] == ex["masked_keys"]
    logits = [Decimal(s) for s in ex["scaled_logits_decimal"]]
    exps = [l.exp() for l in logits]
    Z = sum(exps)
    a = [e / Z for e in exps]
    vals = ex["value_vectors"]
    contrib = [[w * v for v in vec] for w, vec in zip(a, vals)]
    out = [sum(c[d] for c in contrib) for d in range(2)]
    tol = Decimal("1e-50")
    ref = chk["q10"]
    for got, want in [(Z, ref["softmax_normalizer"])] + list(zip(a, ref["softmax_weights"])) + \
            list(zip(out, ref["weighted_output"])) + \
            [(g, w) for gc, wc in zip(contrib, ref["weighted_value_contributions"]) for g, w in zip(gc, wc)]:
        assert abs(got - Decimal(want)) < tol, (got, want)
    assert abs(sum(a) - 1) < tol
    assert "S3" not in keys and inp["excluded_summary"]["excluded_from_queries"] == qs
    return dict(keys=keys, qs=qs, perm=perm, logits=ex["scaled_logits_decimal"], a=[float(x) for x in a],
                vals=vals, contrib=[[float(x) for x in c] for c in contrib], out=[float(x) for x in out],
                Z=float(Z), allowed=ex["allowed_keys"], q=ex["query_index"])


def kind(k):
    return PRE if k.startswith("P") else SUM if k.startswith("S") else LOC


def col_x(keys):
    """Left edges of the 8 bank columns; shared by panels (a), (c) and (d)."""
    xs, x, prev = [], X0, None
    for k in keys:
        if prev is not None:
            x += SW + (GG if kind(k) is not kind(prev) else SG)
        xs.append(x)
        prev = k
    return xs


def sub(k):  # 't10' -> '$t_{10}$', 'P0' -> '$P_{0}$'
    return f"${k[0]}_{{{k[1:]}}}$"


# ------------------------------------------------------------ primitives ---
def card(cv, x, y, w, h, title, r="frozen"):
    cv.group(x, y, w, h, r, title, band=True, size=7.9, radius=2.0, lw=0.7, fill="white")


def hatched(cv, x, y, w, h, z=6, lw=0.35):
    cv.ax.add_patch(Rectangle((x, y), w, h, fc=BLK["fill"], ec=BLK["stroke"], lw=lw, zorder=z))
    cv.ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=BLK["hatch"], lw=0, hatch="//////", zorder=z + 0.01))


def slot(cv, x, y, k, r, seed, h=12.8, lw=0.6, dashed=False):
    """One cache slot: id over a key vector (3 cells) and a value vector (2 cells)."""
    cv.box(x, y, SW, h, r, lw=lw, dashed=dashed, radius=1.2)
    cv.text(x + SW / 2, y + h - 2.3, sub(k), size=7.0, color=r["ink"])
    cv.vec(x + SW / 2 - 1.95, y + 5.6, n=3, cell=1.3, r=r, seed=seed)
    cv.vec(x + SW / 2 - 1.3, y + 1.6, n=2, cell=1.3, r=r, seed=seed + 50)


def mini(cv, x, y, rows, cols, fills, cell=1.15, lw=0.3):
    """Shape glyph for a matrix: fills(i, j) -> colour or None (hatched)."""
    for i in range(rows):
        for j in range(cols):
            cx, cy = x + j * cell, y + (rows - 1 - i) * cell
            f = fills(i, j)
            if f is None:
                hatched(cv, cx, cy, cell, cell, z=7, lw=lw * 0.7)
            else:
                cv.ax.add_patch(Rectangle((cx, cy), cell, cell, fc=f, ec="white", lw=lw, zorder=7))
    cv.ax.add_patch(Rectangle((x, y), cols * cell, rows * cell, fc="none", ec=INK, lw=0.45, zorder=7.5))
    return cols * cell, rows * cell


# ---------------------------------------------------------------- panels ---
def panel_a(cv, d, xs):
    card(cv, 2, 100, 110, 36, "(a) Key/value cache bank")
    y0, h = 109.6, 12.8
    cv.box(xs[0] - 1.6, y0 - 1.0, xs[-1] + SW - xs[0] + 3.2, h + 2.0, "neutral", fill="#F7F8FA",
           stroke=BANK["stroke"], lw=0.7, radius=1.6, z=3)
    for j, (k, x) in enumerate(zip(d["keys"], xs)):
        slot(cv, x, y0, k, kind(k), seed=j)
    cv.text(xs[0] - 2.6, y0 + 6.25, r"$\mathbf{k}_j$", size=6.8, color=INK, ha="right")
    cv.text(xs[0] - 2.6, y0 + 2.25, r"$\mathbf{v}_j$", size=6.8, color=INK, ha="right")
    # provenance of the completed-chunk summaries
    for x, rng in ((xs[2], "$t_1$–$t_4$"), (xs[3], "$t_5$–$t_8$")):
        cs = cv.tokens(x + 0.05, 125.9, 4, w=1.85, h=1.85, gap=0.37, r="neutral", lw=0.4)
        cv.text(x + SW / 2, 129.6, rng, size=6.6, color=SUM["ink"])
        cv.arrow([(x + SW / 2, 125.9), (x + SW / 2, y0 + h + 1.0 - 0.02)], color=SUM["stroke"], lw=0.6, head=1.0)
    cv.text((xs[0] + xs[1] + SW) / 2, 127.2, "always readable", size=6.1, color=PRE["ink"], style="italic")
    cv.rich((xs[4] + xs[7] + SW) / 2, 127.2, [(r"$t_j$", LOC["ink"]), (r" readable iff ", LOC["ink"]),
                                               (r"$j\leq i$", LOC["ink"])], size=6.5, ha="center")
    # group brackets
    for a_, b_, r, lab in ((0, 1, PRE, "prefix"), (2, 3, SUM, "summaries"), (4, 7, LOC, "current chunk")):
        xa, xb = xs[a_], xs[b_] + SW
        cv.line([(xa, 107.0), (xb, 107.0)], color=r["mark"], lw=0.9)
        cv.text((xa + xb) / 2, 104.3, lab, size=6.5, color=r["ink"], weight="bold")


def panel_b(cv, d):
    card(cv, 115, 100, 61, 36, "(b) Summary availability")
    y0, h = 109.6, 12.8
    qw, qg, qx = 6.2, 1.2, 118.0
    yq = y0 + h / 2
    cv.line([(qx - 0.8, yq), (qx + 4 * qw + 3 * qg + 0.8, yq)], color=QRY["stroke"], lw=0.6, z=4)
    for n, q in enumerate(d["qs"]):
        x = qx + n * (qw + qg)
        hero = q == d["q"]
        cv.box(x, yq - 2.7, qw, 5.4, "amber", f"$q_{{{q}}}$", weight="normal", size=6.8,
               lw=1.0 if hero else 0.55, fill=QRY["soft"] if hero else QRY["fill"], radius=1.0)
    xe = qx + 4 * qw + 3 * qg
    cv.text((qx + xe) / 2, 127.2, "query steps", size=6.1, color=QRY["ink"], style="italic")
    # S3 is absent from K for every query of the chunk
    hatched(cv, qx, 103.4, xe - qx, 4.2, z=5, lw=0.45)
    cv.rich((qx + xe) / 2, 105.5, [(r"$S_3\notin\mathbf{K}$", SUM["ink"]), (r"  for $q_9$–$q_{12}$", INK)],
            size=6.6, ha="center", z=21)
    # seal boundary, then S3 is finalized from t9-t12
    xs_ = 152.4
    cv.line([(xs_, 102.4), (xs_, 128.2)], color=INK, lw=0.7, dashed=True, z=4)
    cv.text(xs_, 129.8, "seal", size=6.6, weight="bold", color=INK)
    x3 = 159.0
    cv.tokens(x3 + 0.05, 125.9, 4, w=1.85, h=1.85, gap=0.37, r="memory", lw=0.4)
    cv.text(x3 + SW / 2, 129.6, "$t_9$–$t_{12}$", size=6.6, color=LOC["ink"])
    cv.arrow([(x3 + SW / 2, 125.9), (x3 + SW / 2, y0 + h)], color=SUM["stroke"], lw=0.6, head=1.0)
    slot(cv, x3, y0, "S3", SUM, seed=9, lw=0.9)
    cv.arrow([(xe, yq), (x3, yq)], color=LINE, lw=0.6, head=1.1)
    cv.text(x3 + SW / 2, 105.6, "later reads", size=6.1, color=SUM["ink"], style="italic")


def panel_c(cv, d, xs):
    card(cv, 2, 52, 174, 45, "(c) Additive causal mask over the bank")
    keys, qs, perm = d["keys"], d["qs"], d["perm"]
    rh, top = 5.6, 83.2
    cw = SW + 1.0
    for a_, b_, r, lab in ((0, 1, PRE, "prefix"), (2, 3, SUM, "summaries"), (4, 7, LOC, "local causal block")):
        xa, xb = xs[a_] - 0.5, xs[b_] + SW + 0.5
        cv.line([(xa, 88.1), (xb, 88.1)], color=r["mark"], lw=0.9)
        cv.text((xa + xb) / 2, 90.1, lab, size=6.6, color=r["ink"], weight="bold")
    for k, x in zip(keys, xs):
        cv.text(x + SW / 2, 85.7, sub(k), size=7.0, color=kind(k)["ink"])
    cv.text(xs[-1] + SW + 4.6, 85.7, "reads", size=6.1, color=MUTED, style="italic")
    for i, q in enumerate(qs):
        yb = top - (i + 1) * rh
        hero = q == d["q"]
        cv.chip(9.0, yb + rh / 2, f"$q_{{{q}}}$", "amber", size=6.8, solid=hero, pad=1.0, h=4.0)
        for j, (k, x) in enumerate(zip(keys, xs)):
            cx = x - 0.5
            if perm[i][j]:
                cv.ax.add_patch(Rectangle((cx, yb), cw, rh, fc=kind(k)["soft"], ec="white", lw=0.6, zorder=6))
                cv.text(cx + cw / 2, yb + rh / 2, "$0$", size=6.8, color=kind(k)["ink"])
            else:
                hatched(cv, cx + 0.15, yb + 0.15, cw - 0.3, rh - 0.3)
                cv.text(cx + cw / 2, yb + rh / 2, r"$-\infty$", size=6.6, color=BLK["ink"],
                        bbox=dict(fc=BLK["fill"], ec="none", pad=0.4))
        cv.text(xs[-1] + SW + 4.6, yb + rh / 2, f"{sum(perm[i])}", size=6.8, color=INK)
    # staircase boundary of the local causal block (j <= i)
    pts = []
    for i in range(len(qs)):
        xr = xs[4 + i] + SW + 0.5
        pts += [(xr, top - i * rh), (xr, top - (i + 1) * rh)]
    cv.line(pts, color=LOC["ink"], lw=1.1, radius=0, z=9)
    # q10 row: the worked example
    i10 = qs.index(d["q"])
    cv.ax.add_patch(Rectangle((xs[0] - 0.8, top - (i10 + 1) * rh - 0.3), xs[-1] + SW - xs[0] + 1.6, rh + 0.6,
                              fc="none", ec=QRY["mark"], lw=1.1, zorder=10))
    # legend
    ly = 56.4
    for n_, r in enumerate((PRE, SUM, LOC)):
        cv.ax.add_patch(Rectangle((xs[0] - 0.5 + n_ * 1.15, ly - 1.4), 1.15, 2.8, fc=r["soft"], ec="none", zorder=6))
    cv.text(xs[0] + 3.8, ly, "$0$  permitted", size=6.4, color=INK, ha="left")
    hatched(cv, xs[3], ly - 1.4, 3.4, 2.8)
    cv.text(xs[3] + 4.3, ly, r"$-\infty$  blocked", size=6.4, color=INK, ha="left")
    cv.line([(xs[6], ly), (xs[6] + 3.4, ly)], color=LOC["ink"], lw=1.1)
    cv.text(xs[6] + 4.3, ly, r"$j\leq i$ edge", size=6.4, color=INK, ha="left")
    # ---- right: shapes of the operator, then the equations
    xR = 116.0
    cv.line([(xR - 3.0, 55.0), (xR - 3.0, 90.6)], color="#E1E5EA", lw=0.5)
    cell, yc = 1.15, 73.0
    roles = [kind(k) for k in keys]
    x = xR + 1.0
    glyphs = []

    def put(lbl, dims, rows, cols, fills, color):
        nonlocal x
        w, h = mini(cv, x, yc - rows * cell / 2, rows, cols, fills, cell)
        cv.text(x + w / 2, yc + h / 2 + 2.0, lbl, size=7.0, color=color)
        cv.text(x + w / 2, yc - h / 2 - 2.0, dims, size=6.5, color=MUTED)
        glyphs.append((x, w))
        x += w

    def gap(sym=None, wid=4.2, arrow=False, lab=None, lab2=None):
        nonlocal x
        if arrow:
            cv.arrow([(x + 0.8, yc), (x + wid - 0.8, yc)], head=1.0, lw=0.6)
            if lab:
                cv.text(x + wid / 2, yc + 1.9, lab, size=6.4, color=INK)
            if lab2:
                cv.text(x + wid / 2, yc - 1.9, lab2, size=6.0, color=INK)
        elif sym:
            cv.op(x + wid / 2, yc, sym, d=2.4, lw=0.5)
        x += wid

    put(r"$\mathbf{Q}$", r"$4\times d_k$", 4, 3, lambda i, j: QRY["soft"] if i != i10 else QRY["mark"], QRY["ink"])
    gap("x")
    put(r"$\mathbf{K}^{\!\top}$", r"$d_k\times 8$", 3, 8, lambda i, j: roles[j]["soft"], BANK["ink"])
    gap(arrow=True, wid=11.4, lab=r"$+\mathbf{M}$", lab2="softmax")
    put(r"$\mathbf{A}$", r"$4\times 8$", 4, 8,
        lambda i, j: (roles[j]["mark"] if i == i10 else roles[j]["soft"]) if perm[i][j] else None, INK)
    gap("x")
    put(r"$\mathbf{V}$", r"$8\times d_v$", 8, 2, lambda i, j: roles[i]["soft"], BANK["ink"])
    gap(arrow=True, wid=4.6)
    put(r"$\mathbf{O}$", r"$4\times d_v$", 4, 2, lambda i, j: QRY["soft"] if i != i10 else QRY["mark"], QRY["ink"])
    xm = (xR + x) / 2
    cv.rich(xm, 87.6, [(r"$\mathbf{A}=\mathrm{rowsoftmax}($", INK), (r"$\mathbf{Q}$", QRY["ink"]),
                       (r"$\mathbf{K}^{\!\top}$", BANK["ink"]), (r"$/\sqrt{d_k}\,+\,$", INK),
                       (r"$\mathbf{M}$", INK), (r"$)$,", INK),
                       (r"$\ \ \mathbf{O}=\mathbf{A}$", INK), (r"$\mathbf{V}$", BANK["ink"])], size=7.4, ha="center")
    cv.rich(xm, 62.2, [(r"$M_{ij}=0$  if  $j\in\{$", INK), (r"$P_0,P_1,$", PRE["ink"]), (r"$S_1,S_2$", SUM["ink"]),
                       (r"$\}$  or  ", INK), (r"$t_j$ with $j\leq i$", LOC["ink"])], size=6.6, ha="center")
    cv.text(xm, 58.0, r"$M_{ij}=-\infty$  otherwise", size=6.6, color=INK)


def panel_d(cv, d, xs):
    card(cv, 2, 2, 174, 47, r"(d) Worked readout for query $q_{10}$")
    keys = d["keys"]
    n = len(d["allowed"])
    cw = SW + 1.0
    yid, yl, base, yv, ya1, ya2 = 41.0, 36.8, 22.2, 18.4, 14.4, 10.8
    k_bar = 9.0 / max(d["a"])
    lx = 4.0
    cv.text(lx, yl, r"$\ell_j+M_{10,j}$", size=6.6, ha="left")
    cv.text(lx, base + 5.0, r"weight $a_j$", size=6.6, ha="left")
    cv.text(lx, yv, r"value $\mathbf{v}_j$", size=6.6, ha="left")
    cv.text(lx, (ya1 + ya2) / 2, r"$a_j\mathbf{v}_j$", size=6.6, ha="left")
    cv.line([(xs[0] - 1.0, base), (xs[-1] + SW + 1.0, base)], color="#9AA0A8", lw=0.5)
    for j, (k, x) in enumerate(zip(keys, xs)):
        r, cx = kind(k), x + SW / 2
        cv.text(cx, yid, sub(k), size=7.0, color=r["ink"])
        if j < n:
            cv.text(cx, yl, f"${d['logits'][j]}$", size=6.8, color=INK)
            hb = d["a"][j] * k_bar
            cv.box(cx - 2.6, base, 5.2, hb, r, fill=r["mark"], stroke=r["ink"], lw=0.4, radius=0.25, z=6)
            cv.text(cx, base + hb + 1.5, f"{d['a'][j]:.4f}", size=6.2, color=r["ink"])
            v = d["vals"][j]
            cv.text(cx, yv, f"$({v[0]},\\,{v[1]})$", size=6.6, color=INK)
            for yy, c in ((ya1, d["contrib"][j][0]), (ya2, d["contrib"][j][1])):
                cv.text(cx, yy, f"${c:.4f}$", size=6.2, color=INK if c else MUTED)
        else:
            hatched(cv, x - 0.5 + 0.15, yl - 2.0, cw - 0.3, 4.0)
            cv.text(cx, yl, r"$-\infty$", size=6.6, color=BLK["ink"], bbox=dict(fc=BLK["fill"], ec="none", pad=0.4))
            cv.text(cx, base + 1.5, "0", size=6.4, color=BLK["ink"])
            for yy in (yv, ya1, ya2):
                cv.text(cx, yy, "–", size=6.4, color=BLK["ink"])
    # column brackets for the value vector pair
    bx0, bx1 = xs[0] - 1.6, xs[-1] + SW + 1.6
    for xx, s in ((bx0, 1), (bx1, -1)):
        cv.line([(xx + s * 0.6, ya1 + 2.0), (xx, ya1 + 2.0), (xx, ya2 - 2.0), (xx + s * 0.6, ya2 - 2.0)],
                color="#9AA0A8", lw=0.5, radius=0)
    # sums
    xS = xs[-1] + SW + 6.0
    cv.text(xS, yid, r"$\Sigma$", size=7.2, color=INK)
    cv.text(xS, base + 1.6, "$1$", size=6.6, color=INK)
    for yy, c in ((ya1, d["out"][0]), (ya2, d["out"][1])):
        cv.text(xS, yy, f"{c:.4f}", size=6.6, color=QRY["ink"], weight="bold")
    cv.rich(lx, 5.2, [(r"$a_j=\exp(\ell_j)/Z,\quad Z=\Sigma_j\exp(\ell_j)=$", INK),
                      (f"${d['Z']:.5f}$", INK)], size=6.6)
    # ---- right: 2-D value space with the hero output vector
    xR = 116.0
    cv.line([(xR - 3.0, 4.0), (xR - 3.0, 42.6)], color="#E1E5EA", lw=0.5)
    cv.rich(145.0, 39.6, [(r"$\mathbf{o}_{10}=\Sigma_j\, a_j\mathbf{v}_j=$", QRY["ink"]),
                          (f"$({d['out'][0]:.6f},\\,{d['out'][1]:.6f})$", QRY["ink"], "bold")], size=7.4, ha="center")
    u, ox, oy = 10.5, 135.0, 9.0
    P = lambda v1, v2: (ox + u * v1, oy + u * v2)  # noqa: E731
    gl = "#E6E9ED"
    for t in (-1, 1, 2):
        cv.line([P(t, -0.05), P(t, 2.25)], color=gl, lw=0.45, z=2)
    for t in (1, 2):
        cv.line([P(-1.3, t), P(2.35, t)], color=gl, lw=0.45, z=2)
    cv.arrow([P(-1.35, 0), P(2.45, 0)], color="#9AA0A8", lw=0.55, head=1.0)
    cv.arrow([P(0, -0.12), P(0, 2.4)], color="#9AA0A8", lw=0.55, head=1.0)
    for t in (-1, 1, 2):
        cv.text(*P(t, -0.2), f"${t}$", size=6.0, color=MUTED, va="top")
    for t in (1, 2):
        cv.text(ox - 1.8, oy + u * t, f"${t}$", size=6.0, color=MUTED, ha="right")
    cv.text(*P(2.55, 0), r"$v_1$", size=6.6, color=MUTED, ha="left")
    cv.text(ox + 1.0, oy + u * 2.4, r"$v_2$", size=6.6, color=MUTED, ha="left")
    off = {"P0": (0.0, 0.17, "center"), "P1": (0.12, 0.0, "left"), "S1": (0.12, 0.0, "left"),
           "S2": (-0.12, 0.0, "right"), "t9": (0.0, 0.17, "center"), "t10": (0.12, 0.0, "left")}
    for k, v, a in zip(d["allowed"], d["vals"], d["a"]):
        r = kind(k)
        cv.line([P(0, 0), P(*v)], color=r["stroke"], lw=0.45, z=4)
        cv.dot(*P(*v), color=r["mark"], d=1.4, z=9)
        dx, dy, ha = off[k]
        cv.text(*P(v[0] + dx, v[1] + dy), sub(k), size=6.6, color=r["ink"], ha=ha,
                va="bottom" if dy else "center")
    o = d["out"]
    cv.arrow([P(0, 0), P(*o)], color=QRY["mark"], lw=1.3, head=1.6, z=10)
    cv.text(*P(0.64, 0.51), r"$\mathbf{o}_{10}$", size=7.2, color=QRY["ink"], ha="left", va="center",
            weight="bold")
    cv.text(*P(2.45, 2.2), r"value space, $d_v=2$", size=6.5, color=MUTED, style="italic", ha="right")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", default=os.path.join(E_DIR, "inputs.json"))
    ap.add_argument("--checks", default=None, help="numerical_checks.json (default: next to --inputs)")
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    inp = json.load(open(a.inputs))
    chk = json.load(open(a.checks or os.path.join(os.path.dirname(a.inputs), "numerical_checks.json")))
    d = compute(inp, chk)
    matplotlib.rcParams["hatch.linewidth"] = 0.35
    cv = Canvas(W, H, family="serif", size=7.0)
    xs = col_x(d["keys"])
    panel_a(cv, d, xs)
    panel_b(cv, d)
    panel_c(cv, d, xs)
    panel_d(cv, d, xs)
    print("\n".join(cv.save(os.path.join(a.out, "causal_cache_attention"))))


if __name__ == "__main__":
    main()
