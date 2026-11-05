"""Redesign of Figure 1 of "Attention Is All You Need" (arXiv 1706.03762): the Transformer.

Facts used (Sec. 3 of the paper): encoder and decoder are stacks of N = 6 identical layers;
encoder layer = multi-head self-attention + position-wise feed-forward, each wrapped in a
residual connection and layer norm (Add & Norm); the decoder adds a third sub-layer that
attends over the encoder output, and its self-attention is masked so position i only sees
positions < i+1 (outputs are shifted right; illegal scores are set to -inf before the softmax);
embeddings are summed with sinusoidal positional encodings; a linear layer + softmax gives
next-token probabilities. Base model: d_model = 512, h = 8, d_k = d_v = 64, d_ff = 2048.
The example tokens are illustrative.

Plate (architecture register): (a) overview with the encoder and decoder as two lanes of
sub-layer slabs, (b) inside every attention block, (c) the three attention masks with real
tokens and the -inf entries, (d) one head's tensor flow and the base-model sizes; key strip.

    python render_fig1.py --out <dir>
"""
import argparse
import math
import os
import sys

import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, INK, MUTED, LINE, mix  # noqa: E402

# one meaning per hue: the three attention kinds are the only saturated colours
ENC = dict(fill="#EBF2FC", soft="#D2E2F7", stroke="#5A8BCB", ink="#1C4C8C", mark="#2F6FC0")   # self-attention
DEC = dict(fill="#F3EFFB", soft="#E1D6F4", stroke="#8C6CC8", ink="#47297F", mark="#7048BF")   # masked self-attn
CRS = dict(fill="#E7F5F2", soft="#C3E5DD", stroke="#3D9C8B", ink="#0E5A4F", mark="#14897A")   # cross-attention
EMB = dict(fill="#FCEFF3", soft="#F6D7E1", stroke="#C98AA0", ink="#7A2E4A", mark="#C2507F")   # embeddings
NEU = dict(fill="#F3F4F6", soft="#E4E7EB", stroke="#8F98A4", ink="#353C47", mark="#6B7480")   # standard parts
NORM = dict(NEU, fill="#F7F7EE", soft="#EEEFD9", stroke="#AEB39C", ink="#4A4F45")
RES = "#9AA2AD"
NEU2 = dict(NEU)                          # same neutral, drawn with a soft fill (derived tensors)
N, H_HEADS, D_MODEL, D_K, D_FF = 6, 8, 512, 64, 2048
SRC = ["the", "cat", "sat", "."]
TGT_IN = ["<s>", "die", "Katze", "saß"]
TGT_OUT = TGT_IN[1:] + ["</s>"]          # outputs are the inputs shifted by one position
W, H = 178, 124
ANG = math.radians(40)


def ox(d):
    return d * math.cos(ANG)


def oy(d):
    return d * math.sin(ANG)


# ------------------------------------------------------------------ helpers ---
def pill(cv, cx, y, text, c, size=7.0):
    """Title tab sitting on a frame border (section-style, placed by hand so it can avoid wires)."""
    tw, th = cv.text_width(text, size, "bold") + 4.0, size * 0.56
    cv.ax.add_patch(FancyBboxPatch((cx - tw / 2, y - th / 2), tw, th, boxstyle=f"round,pad=0,rounding_size={th / 2}",
                                   fc=c["soft"], ec=c["stroke"], lw=0.6, zorder=4))
    cv.text(cx, y, text, size=size, weight="bold", color=c["ink"], z=5)


def vslab(cv, x, yc, w, h, c, title, sub=None, d=1.2, size=6.5, hero=False, lw=0.6, fill=None):
    """Sub-layer as a tall slab with vertical text, centred on the lane line yc. Returns (x_in, x_out, top)."""
    y = yc - h / 2
    cv.cuboid(x, y, w, h, d=d, r=c, fill=fill or (c["mark"] if hero else c["soft"]), lw=lw)
    tc, sc = ("white", "white") if hero else (c["ink"], INK)
    if sub:
        cv.text(x + w / 2 - 1.15, yc, title, size=size, weight="bold", color=tc, rotation=90, z=8)
        cv.text(x + w / 2 + 1.35, yc, sub, size=size - 0.4, color=sc, rotation=90, z=8)
    else:
        cv.text(x + w / 2, yc, title, size=size, weight="bold" if c is not NORM else "normal", color=tc,
                rotation=90, z=8)
    assert cv.text_width(title, size, "bold") < h - 1.0, title
    return x, x + w + ox(d), y + h + oy(d)


def token_column(cv, cx, yc, words, c, w=8.6, h=3.4, gap=0.6):
    y0 = yc + (len(words) * (h + gap) - gap) / 2 - h
    for k, t in enumerate(words):
        cv.tokens(cx - w / 2, y0 - k * (h + gap), 1, w=w, h=h, r=c, labels=[t], size=6.2)
    return yc - (len(words) * (h + gap) - gap) / 2, yc + (len(words) * (h + gap) - gap) / 2


def pe_glyph(cv, x, y, d=3.0, z=9):
    """Sinusoid in a circle = positional encoding."""
    cv.ax.add_patch(Circle((x, y), d / 2, fc="white", ec=LINE, lw=0.6, zorder=z))
    t = np.linspace(-1, 1, 40)
    cv.ax.plot(x + t * d * 0.34, y + np.sin(t * math.pi) * d * 0.2, color=LINE, lw=0.6, zorder=z + 1)


def hatch_cell(cv, x, y, s, z=6):
    cv.ax.add_patch(Rectangle((x, y), s, s, fc="white", ec="#B3BAC4", lw=0.4, hatch="//////", zorder=z))


def stack_frame(cv, x, y, w, h, c, n=2, d=0.9):
    """N identical layers: dashed section in the stack's hue with two offset copies behind it."""
    for i in range(n, 0, -1):
        cv.box(x + i * d, y + i * d, w, h, c, fill=mix(c["fill"], "#FFFFFF", 0.4), lw=0.45, radius=2.0,
               z=1.2 - i * 0.01)
    cv.section(x, y, w, h, c, fill=c["fill"], radius=2.0, z=1.3)


# ------------------------------------------------------------------ (a) overview ---
def lane(cv, yc, words, emb_title, c, subs, x_frame, frame_w, pill_x, pill_y_top):
    """One stack lane: token column -> embedding slab -> (+) PE -> N x [sub-layers] frame.
    subs = [(kind, role, title, sub, w)] with kind 'attn' | 'ffn' | 'norm'. Returns slab extents."""
    t0, t1 = token_column(cv, 7.2, yc, words, NEU)
    cv.arrow([(11.5, yc), (14.6, yc)], color=c["mark"], lw=0.8, head=1.1)
    _, xo, _ = vslab(cv, 14.6, yc, 5.6, 22, EMB, emb_title, r"$d_{\mathrm{model}}=%d$" % D_MODEL, d=1.0, size=6.3)
    cv.arrow([(xo, yc), (24.1, yc)], color=c["mark"], lw=0.8, head=1.0)
    cv.op(25.5, yc, "+", d=2.8)
    pe_glyph(cv, 25.5, yc - 8.0)
    cv.line([(25.5, yc - 6.5), (25.5, yc - 1.4)])
    stack_frame(cv, x_frame, yc - 14.5, frame_w, 29.0, c)
    pill(cv, pill_x, pill_y_top, f"{'Encoder' if c is ENC else 'Decoder'}  ×{N}", c)
    x, prev_out, ext = x_frame + 4.0, 26.9, []
    yr = yc - 13.0                                         # residual runs under the slabs
    junction = None
    for kind, rr, title, sub, w in subs:
        if kind != "norm":
            junction = (prev_out + x) / 2 if prev_out > x_frame else x_frame + 2.0
        cv.arrow([(prev_out, yc), (x, yc)], color=c["mark"], lw=0.8, head=1.0)
        d = {"attn": 1.2, "ffn": 1.0, "norm": 0.6}[kind]
        x_in, x_out, top = vslab(cv, x, yc, w, 22, rr, title, sub, d=d, hero=kind == "attn",
                                 size=6.5 if kind != "norm" else 6.1, lw=0.9 if kind == "attn" else 0.5,
                                 fill="white" if kind == "ffn" else None)
        ext.append((kind, x_in, x_out, top, w))
        if kind == "norm":
            cv.dot(junction, yc, color=RES, d=0.8)
            cv.arrow([(junction, yc), (junction, yr), (x + w / 2, yr), (x + w / 2, yc - 11.0)], color=RES, lw=0.5,
                     head=0.9, radius=0.8)
        prev_out, x = x_out, x_out + 4.2
    return prev_out, ext


def panel_a(cv):
    cv.text(2.5, 122.6, "(a) Overview", size=7.6, weight="bold", color=NEU["ink"], ha="left", va="top")
    yE, yD = 103.5, 67.5
    enc = [("attn", ENC, "Self-attention", r"multi-head, $h=%d$" % H_HEADS, 7.0),
           ("norm", NORM, "Add & Norm", None, 3.4),
           ("ffn", NEU, "Feed-forward", r"$d_{ff}=%d$" % D_FF, 6.4),
           ("norm", NORM, "Add & Norm", None, 3.4)]
    dec = [("attn", DEC, "Masked self-attn.", "multi-head, causal", 7.0),
           ("norm", NORM, "Add & Norm", None, 3.4),
           ("attn", CRS, "Cross-attention", "multi-head", 7.0),
           ("norm", NORM, "Add & Norm", None, 3.4),
           ("ffn", NEU, "Feed-forward", r"$d_{ff}=%d$" % D_FF, 6.4),
           ("norm", NORM, "Add & Norm", None, 3.4)]
    e_out, _ = lane(cv, yE, SRC, "Input embedding", ENC, enc, 29.0, 49.5, 53.75, yE + 15.4)
    d_out, dext = lane(cv, yD, TGT_IN, "Output embedding", DEC, dec, 29.0, 63.5, 80.0, yD + 15.4)
    cv.text(7.2, yE + 10.4, "source", size=6.1, color=MUTED, style="italic")
    cv.text(7.2, yD + 11.4, "shifted\nright", size=6.1, color=MUTED, style="italic", linespacing=0.95)
    # encoder output tensor -> K, V of cross-attention in every decoder layer
    cv.arrow([(e_out, yE), (85.0, yE)], color=ENC["mark"], lw=0.8, head=1.0)
    cv.cuboid(85.0, yE - 5.0, 6.0, 10.0, d=2.4, r=ENC, fill=ENC["soft"], lw=0.6)
    cv.text(88.0, yE, r"$\mathbf{Z}$", size=7.2, color=ENC["ink"], z=8)
    cv.text(95.4, yE + 4.6, "encoder output", size=6.6, color=ENC["ink"], weight="bold", ha="left")
    cv.text(95.4, yE + 1.5, r"$n_{\mathrm{src}}\times d_{\mathrm{model}}=%d\times%d$" % (len(SRC), D_MODEL), size=6.2,
            color=INK, ha="left")
    cv.text(95.4, yE - 2.4, "keys and values of", size=6.1, color=CRS["ink"], style="italic", ha="left")
    cv.text(95.4, yE - 5.0, f"cross-attention, all {N} layers", size=6.1, color=CRS["ink"], style="italic", ha="left")
    _, ca_in, ca_out, ca_top, ca_w = dext[2]
    xk, xv, ycor = ca_in + 2.0, ca_in + 5.0, 86.6
    cv.line([(88.0, yE - 5.0), (88.0, ycor), (xv, ycor)], color=CRS["mark"], lw=1.0)
    cv.line([(xv, ycor), (xk, ycor)], color=CRS["mark"], lw=1.0)
    for x_, lab, ha, dx in ((xk, "K", "right", -0.8), (xv, "V", "left", 0.8)):
        cv.arrow([(x_, ycor), (x_, ca_top - 0.3)], color=CRS["mark"], lw=0.9, head=1.0)
        cv.text(x_ + dx, 80.7, lab, size=6.2, color=CRS["ink"], style="italic", ha=ha)
    cv.dot(xv, ycor, color=CRS["mark"], d=0.8)
    cv.text(ca_in - 2.1, yD + 1.6, "Q", size=6.0, color=DEC["ink"], style="italic")
    # output head
    cv.arrow([(d_out, yD), (97.0, yD)], color=DEC["mark"], lw=0.8, head=1.0)
    _, lo, _ = vslab(cv, 97.0, yD, 4.4, 18, NEU, "Linear", d=0.8, fill="white", lw=0.5)
    cv.arrow([(lo, yD), (105.0, yD)], color=DEC["mark"], lw=0.8, head=1.0)
    _, so, _ = vslab(cv, 105.0, yD, 4.4, 18, NEU, "Softmax", d=0.8, fill="white", lw=0.5)
    cv.arrow([(so, yD), (113.0, yD)], color=DEC["mark"], lw=0.8, head=1.0)
    token_column(cv, 117.6, yD, TGT_OUT, DEC)
    cv.text(117.6, yD + 11.4, "next\ntoken", size=6.1, color=MUTED, style="italic", linespacing=0.95)
    return dext


# ------------------------------------------------------------------ (b) multi-head ---
def panel_b(cv):
    x0, y0, w, h = 130.0, 53.0, 46.0, 66.0
    m = x0 + w / 2
    cv.section(x0, y0, w, h, NEU, "Multi-head attention", letter="b", tab="corner", size=7.2, fill=NEU["fill"])
    cxs = (m - 11.5, m, m + 11.5)
    for cx, lab, c in zip(cxs, ("Q", "K", "V"), (DEC, CRS, CRS)):
        cv.cuboid(cx - 2.6, y0 + 3.0, 5.2, 4.4, d=1.4, r=NEU, fill="white", lw=0.5)
        cv.text(cx, y0 + 5.2, rf"$\mathbf{{{lab}}}$", size=6.6, color=INK, z=8)
        cv.arrow([(cx, y0 + 8.3), (cx, y0 + 11.0)], head=0.9)
        cv.trap(cx - 3.2, y0 + 11.0, 6.4, 4.6, NEU, narrow="top", lw=0.5)
        cv.arrow([(cx, y0 + 15.6), (cx, y0 + 19.6)], head=0.9)
    cv.text(m - 17.5, y0 + 13.3, "linear", size=5.9, color=MUTED, ha="left", rotation=90)
    cv.stack(m - 17.0, y0 + 19.6, 32.2, 12.6, n=3, r=NEU, dx=0.9, dy=0.9, fill="white", lw=0.5, radius=1.2)
    for k, (s, col, sz) in enumerate((("scaled dot-product", INK, 6.3), ("attention", INK, 6.3),
                                      (rf"$h={H_HEADS}$ heads in parallel", MUTED, 5.9))):
        cv.text(m - 0.9, y0 + 29.0 - 3.0 * k, s, size=sz, color=col)
    cv.arrow([(m, y0 + 34.0), (m, y0 + 35.6)], head=0.9)
    cv.cuboid(m - 12.5, y0 + 35.6, 25.0, 3.8, d=0.8, r=NEU, fill=NEU["soft"], lw=0.5)
    cv.text(m, y0 + 37.5, "Concat", size=6.3, color=NEU["ink"], z=8)
    cv.arrow([(m, y0 + 39.9), (m, y0 + 42.4)], head=0.9)
    cv.trap(m - 4.5, y0 + 42.4, 9.0, 4.6, NEU, narrow="top", lw=0.5)
    cv.text(m + 6.5, y0 + 44.7, r"$W^{O}$", size=6.4, color=INK, ha="left")
    cv.arrow([(m, y0 + 47.0), (m, y0 + 50.0)], head=0.9)
    cv.text(m, y0 + 55.8, r"$\mathrm{MultiHead}(Q,K,V)=$", size=6.4, color=INK)
    cv.text(m, y0 + 52.4, r"$\mathrm{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)\,W^{O}$", size=6.4,
            color=INK)
    return (x0, y0, w, h)


# ------------------------------------------------------------------ (c) masks ---
def mask_block(cv, x, ytop, kind, rows, cols, c, title, l1, l2, cell=4.0):
    n = len(rows)
    allowed = np.ones((n, n)) if kind != "causal" else np.tril(np.ones((n, n)))
    for i in range(n):
        for j in range(n):
            xx, yy = x + j * cell, ytop - (i + 1) * cell
            if allowed[i, j] > 0:
                cv.ax.add_patch(Rectangle((xx, yy), cell, cell, fc=c["soft"], ec=c["stroke"], lw=0.4, zorder=6))
                cv.text(xx + cell / 2, yy + cell / 2, "0", size=5.8, color=c["ink"], z=7)
            else:
                hatch_cell(cv, xx, yy, cell)          # = -inf, defined in the key strip
    cv.ax.add_patch(Rectangle((x, ytop - n * cell), n * cell, n * cell, fc="none", ec=c["ink"], lw=0.7, zorder=7))
    for i, t in enumerate(rows):
        cv.text(x - 0.8, ytop - (i + 0.5) * cell, t, size=5.8, color=MUTED, ha="right")
    for j, t in enumerate(cols):
        cv.text(x + (j + 0.5) * cell, ytop + 0.7, t, size=5.8, color=MUTED, rotation=90, va="bottom")
    yb = ytop - n * cell
    cv.text(x - 5.0, yb - 2.6, title, size=6.7, color=c["ink"], weight="bold", ha="left")
    cv.text(x - 5.0, yb - 5.6, l1, size=6.1, color=INK, ha="left")
    cv.text(x - 5.0, yb - 8.9, l2, size=6.1, color=INK, ha="left")
    return allowed


def panel_c(cv):
    x0, y0, w, h = 2.0, 10.5, 86.0, 39.5
    cv.section(x0, y0, w, h, NEU, "Who attends to whom", letter="c", tab="corner", size=7.2, fill="white")
    cv.text(x0 + w - 2.0, y0 + h - 2.9, "rows: queries · columns: keys", size=6.0, color=MUTED, style="italic",
            ha="right")
    yt = 38.2
    a = mask_block(cv, 11.0, yt, "full", SRC, SRC, ENC, "Encoder self-attn.", "every source token", "sees all of them")
    b = mask_block(cv, 40.0, yt, "causal", TGT_IN, TGT_IN, DEC, "Masked self-attn.", r"target token $i$ sees",
                   r"only tokens $\leq i$")
    c = mask_block(cv, 69.0, yt, "full", TGT_IN, SRC, CRS, "Cross-attention", "target queries read", "all source keys")
    assert a.sum() == 16 and b.sum() == 10 and c.sum() == 16 and np.all(np.triu(b, 1) == 0)


# ------------------------------------------------------------------ (d) one head ---
def tensor(cv, x, y, w, h, lab, dims, c=NEU, d=1.4):
    cv.cuboid(x, y, w, h, d=d, r=c, fill="white" if c is NEU else c["soft"], lw=0.5)
    cv.text(x + w / 2, y + h / 2, lab, size=6.6, color=c["ink"], z=8)
    cv.text(x + w / 2, y - 1.7, dims, size=5.9, color=MUTED)


def panel_d(cv):
    x0, y0, w, h = 91.0, 10.5, 85.0, 39.5
    cv.section(x0, y0, w, h, NEU, "Scaled dot-product attention, per head", letter="d", tab="corner", size=7.2,
               fill="white")
    yc = 37.0
    tensor(cv, 94.5, yc + 0.6, 6.0, 4.2, r"$\mathbf{Q}$", "")
    tensor(cv, 94.5, yc - 5.6, 6.0, 4.2, r"$\mathbf{K}$", r"$n\times d_k$")
    cv.line([(101.6, yc + 2.7), (103.6, yc + 2.7), (103.6, yc - 3.5), (101.6, yc - 3.5)], radius=0.8)
    cv.arrow([(103.6, yc - 0.4), (107.0, yc - 0.4)], head=0.9)
    cv.text(104.7, yc + 6.0, r"$\frac{QK^{\top}}{\sqrt{d_k}}$", size=6.4, color=INK)
    tensor(cv, 107.0, yc - 4.0, 7.2, 7.2, r"$\mathbf{S}$", r"$n\times n$", c=NEU2, d=1.6)
    cv.arrow([(115.4, yc - 0.4), (126.6, yc - 0.4)], head=0.9)
    cv.chip(121.0, yc + 2.2, "softmax", NEU, size=6.0, pad=0.7)
    cv.text(121.0, yc - 2.6, r"(mask: $-\infty$)", size=5.3, color=DEC["ink"], style="italic")
    tensor(cv, 126.6, yc - 4.0, 7.2, 7.2, r"$\mathbf{A}$", r"$n\times n$", c=NEU2, d=1.6)
    tensor(cv, 139.0, yc - 4.0, 6.0, 7.2, r"$\mathbf{V}$", r"$n\times d_v$")
    cv.text(137.3, yc - 0.4, r"$\cdot$", size=10, color=INK)
    cv.arrow([(146.6, yc - 0.4), (151.4, yc - 0.4)], head=0.9)
    tensor(cv, 151.4, yc - 4.0, 6.0, 7.2, r"$\mathrm{head}$", r"$n\times d_v$", c=NEU2)
    cv.text(161.0, yc + 2.2, "to Concat", size=5.9, color=MUTED, ha="left", style="italic")
    cv.text(161.0, yc - 0.6, "in (b)", size=5.9, color=MUTED, ha="left", style="italic")
    cv.text(133.5, 24.4, r"$\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V$",
            size=7.2, color=INK)
    spec_strip(cv, 107.0, 11.8, 67.0, 8.4)
    cv.text(94.0, 16.0, "base\nmodel", size=6.1, color=MUTED, style="italic", ha="left", linespacing=0.95)


def spec_strip(cv, x, y, w, h):
    """Base-model hyperparameters as a strip: bold value over its symbol, hairline dividers."""
    cells = [(str(N), r"$N$ layers"), (str(H_HEADS), r"$h$ heads"), (str(D_MODEL), r"$d_{\mathrm{model}}$"),
             (str(D_K), r"$d_k=d_v$"), (str(D_FF), r"$d_{\mathrm{ff}}$")]
    cv.box(x, y, w, h, NEU, fill="#F7F8FA", lw=0.5, radius=1.4)
    cw = w / len(cells)
    for i, (val, sym) in enumerate(cells):
        cx = x + (i + 0.5) * cw
        cv.text(cx, y + h * 0.68, val, size=8.2, color=INK, weight="bold")
        cv.text(cx, y + h * 0.26, sym, size=6.1, color=MUTED)
        if i:
            cv.ax.plot([x + i * cw] * 2, [y + 1.4, y + h - 1.4], color="#D5DAE1", lw=0.5, zorder=6)


# ------------------------------------------------------------------ key strip ---
def key_strip(cv, x, y, w, h=6.2, size=6.3):
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.6", fc="white",
                                   ec=NEU["stroke"], lw=0.6, ls=(0, (3, 2)), zorder=3))
    yc = y + h / 2

    def g_op(gx):
        cv.op(gx, yc, "+", d=2.8)

    def g_pe(gx):
        pe_glyph(cv, gx, yc, d=2.9)

    def g_res(gx):
        cv.arrow([(gx - 2.4, yc), (gx + 2.4, yc)], color=RES, lw=0.5, head=0.9)

    def g_norm(gx):
        cv.cuboid(gx - 2.3, yc - 1.2, 4.0, 2.2, d=0.6, r=NORM, fill=NORM["soft"], lw=0.45)

    def g_mask(gx):
        hatch_cell(cv, gx - 1.3, yc - 1.3, 2.6, z=6)

    def g_slab(gx):
        cv.cuboid(gx - 1.4, yc - 1.8, 2.2, 3.4, d=0.8, r=ENC, fill=ENC["mark"], lw=0.45)

    def g_tensor(gx):
        cv.cuboid(gx - 1.6, yc - 1.4, 2.6, 2.6, d=1.0, r=NEU, fill="white", lw=0.45)

    items = [(g_op, "sum"), (g_pe, "positional encoding"), (g_res, "residual connection"),
             (g_norm, "Add & Norm = sum + layer norm"), (g_slab, "attention sub-layer"),
             (g_tensor, "tensor"), (g_mask, r"masked score ($-\infty$)")]
    widths = [5.0 + 1.0 + cv.text_width(lab, size) for _, lab in items]
    gap = (w - 4.0 - sum(widths)) / (len(items) - 1)
    assert gap > 2.0, gap
    xx = x + 2.0
    for (fn, lab), iw in zip(items, widths):
        fn(xx + 2.5)
        cv.text(xx + 6.0, yc, lab, size=size, ha="left")
        xx += iw + gap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    assert D_K == D_MODEL // H_HEADS and TGT_OUT[:-1] == TGT_IN[1:]
    cv = Canvas(W, H, family="serif", size=7.0)
    panel_a(cv)
    panel_b(cv)
    panel_c(cv)
    panel_d(cv)
    key_strip(cv, 2.0, 2.0, 174.0)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    print("\n".join(cv.save(os.path.join(a.out, "transformer_fig1"))))


if __name__ == "__main__":
    main()
