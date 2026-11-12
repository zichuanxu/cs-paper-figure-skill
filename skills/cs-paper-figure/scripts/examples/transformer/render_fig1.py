#!/usr/bin/env python3
"""Transformer model architecture: Figure 1 of "Attention Is All You Need" (Vaswani et al., arXiv:1706.03762).

Source content kept
  * Encoder: N = 6 identical layers, each multi-head self-attention then a position-wise feed-forward
    network (d_ff = 2048); decoder: N = 6 layers, each masked multi-head self-attention, multi-head
    attention over the encoder output, then feed-forward. Every sub-layer is wrapped as
    LayerNorm(x + Sublayer(x)), d_model = 512 throughout (Sec. 3.1).
  * Input and output embeddings plus sinusoidal positional encodings at the bottom of both stacks;
    outputs shifted right; a linear layer and a softmax give next-token probabilities. The two embedding
    layers and the pre-softmax linear layer share one weight matrix (Sec. 3.4).
  * Scaled dot-product attention softmax(QK^T / sqrt(d_k)) V with the optional mask, and multi-head
    attention with h = 8 heads, d_k = d_v = d_model / h = 64 (Sec. 3.2, the paper's Figure 2).
  * The three uses of attention (Sec. 3.2.3): encoder self-attention, masked decoder self-attention
    (illegal connections set to -inf before the softmax), encoder-decoder attention (queries from the
    previous decoder layer, keys and values from the encoder output z).

Design
  * Claim: one operator, multi-head attention, is wired three ways; everything else is a thin frame around
    it. The three attention blocks are the only saturated blocks and carry the numbers 1-3 that panel (c)
    opens.
  * One hue per stream: blue = encoder states, coral = decoder states, on frames, wires, tokens and the
    Q / K / V ports. Every attention block has the same three ports (K, V, Q); only the colour of what
    enters them changes, and the encoder-decoder block is a blue-to-coral blend. Amber = the shared weight
    matrix (three trapezoids), purple = attention scores and weights, grey = the fixed positional signal.
  * Add & Norm is opened into its parts: a residual wire into a circled +, then a LayerNorm bar.
  * (a) keeps the paper's bottom-to-top flow with a running English-to-German example, so "shifted right"
    is visible as the offset between the decoder's input row and the predicted row. The encoder output z is
    drawn as an object and labelled as feeding every decoder layer, which the original leaves implicit.
  * (b) multi-head wrapper over a worked single head: scores, optional mask, softmax, weights. The weights
    are computed in this script from the printed scores and asserted to sum to 1 per row.
  * (c) the three uses as query-by-key matrices over the example tokens, with the causal mask hatched.
  * The positional-encoding curves are the paper's formula evaluated for d_model = 512 at dimensions
    2i = 0, 48, 96 over positions 0-24. Example sentence, score values, attention patterns and probability
    bars are illustrative; the tokens are whole words for legibility (the paper uses byte-pair / word-piece
    units), and <s> / </s> stand for the start and end symbols implied by "shifted right".

Size: 178 x 125.5 mm (two-column width); smallest text 5.8 pt, math subscripts 4.55 pt.
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from matplotlib import colors as mcolors  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

from paperkit import INK, MUTED, ROLE, Canvas, mix  # noqa: E402

STEM = "transformer_fig1"
W, H = 178.0, 125.5
ENC, DEC, AMB, PUR, NEU = (ROLE[k] for k in ("blue", "coral", "amber", "purple", "neutral"))
PV = mcolors.LinearSegmentedColormap.from_list("pv", ["#FBF9FE", PUR["soft"], PUR["mark"], PUR["ink"]])

T_NODE, T_BODY, T_ANN = 6.8, 6.5, 5.8      # node titles, body and all math (subscripts stay >= 4.5 pt), annotations
SRC = ["I", "like", "green", "tea"]          # x_1..x_n   (illustrative)
TGT_IN = ["<s>", "Ich", "mag", "grünen", "Tee"]   # outputs shifted right
TGT_OUT = ["Ich", "mag", "grünen", "Tee", "</s>"]

# (a) geometry, mm
EX, DX = 20.0, 67.5            # centre lines of the encoder and decoder columns
S0, P = 23.5, 21.6             # bottom of the layer frames; pitch of one sub-layer
BW, BH = 25.0, 7.2             # sub-layer block
RES = 15.5                     # residual corridor, right of the centre line
FL, FR = 17.5, 18.5            # frame extent left / right of the centre line


def softmax(s):
    e = np.exp(s - np.max(s, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def token_row(cv, cx, y, words, r, w=7.2, h=3.6, gap=0.4):
    n = len(words)
    return cv.tokens(cx - (n * w + (n - 1) * gap) / 2, y, n, w=w, h=h, r=r, gap=gap, labels=words, size=5.9)


def masked_cell(cv, x, y, s, z=6):
    cv.ax.add_patch(Rectangle((x, y), s, s, fc="#ECEEF1", ec="white", lw=0.4, zorder=z))
    for a, b in ((0.0, 0.55), (0.45, 1.0)):
        cv.ax.plot([x + a * s + 0.12 * s, x + b * s - 0.12 * s + 0.0], [y + 0.12 * s, y + (b - a) * s + 0.0],
                   color="#A3ABB6", lw=0.45, zorder=z + 0.1, solid_capstyle="round")


def attn_grid(cv, x, y, A, cell, mask=None):
    """Query-by-key weight map: rows = queries (top = first), columns = keys; masked cells hatched."""
    R, C = A.shape
    for i in range(R):
        for j in range(C):
            cx, cy = x + j * cell, y + (R - 1 - i) * cell
            if mask is not None and mask[i, j]:
                masked_cell(cv, cx, cy, cell)
            else:
                cv.ax.add_patch(Rectangle((cx, cy), cell, cell, fc=PV(float(A[i, j])), ec="white", lw=0.4, zorder=6))
    cv.ax.add_patch(Rectangle((x, y), C * cell, R * cell, fc="none", ec=PUR["ink"], lw=0.6, zorder=6.5))


def pill(cv, x, ytop, text, r, solid=False, size=7.4, h=4.2):
    """Title pill sitting on a frame's top border, left-anchored so the centre line stays free."""
    w = cv.text_width(text, size, "bold") + 3.4
    cv.tab(x, ytop - h / 2, w, h, r, text, size=size, solid=solid, radius=h / 2, z=3)
    return w


# ------------------------------------------------------------------ (a) ---
def layer_frame(cv, cx, n_sub, r, name):
    c = ROLE[r]
    x, y, w, h = cx - FL, S0 - 0.9, FL + FR, n_sub * P + 5.7
    for k in (2, 1):                       # two more layers behind: the stack of N identical layers
        cv.box(x + k, y + k, w, h, r, container=True, dashed=True, radius=2.4, lw=0.55, z=0.5 - 0.1 * k,
               fill=mix(c["fill"], "#FFFFFF", 0.35))
    cv.section(x, y, w, h, r)
    pill(cv, x + 1.3, y + h, name, r)
    pill(cv, cx + 4.2, y + h, "N = 6", r, solid=True, size=6.6, h=3.8)
    return y + h


def main_wire(cv, cx, y0, y1, c):
    cv.arrow([(cx, y0), (cx, y1)], color=c["mark"], lw=0.95, head=1.5)


def add_norm(cv, cx, s, r):
    c = ROLE[r]
    xr = cx + RES
    cv.arrow([(cx, s + 1.3), (xr, s + 1.3), (xr, s + 15.9), (cx + 1.4, s + 15.9)], color=c["stroke"], lw=0.6,
             head=1.2)
    cv.dot(cx, s + 1.3, color=c["mark"], d=1.0)
    cv.arrow([(cx, s + 6.0 + BH), (cx, s + 14.5)], color=c["mark"], lw=0.95, head=1.2)
    cv.op(cx, s + 15.9, "+", r=r, d=2.8)
    cv.line([(cx, s + 17.3), (cx, s + 18.2)], color=c["mark"], lw=0.95)
    cv.box(cx - 8, s + 18.2, 16, 3.4, r, "LayerNorm", fill="white", size=6.2, weight="normal")


def attention(cv, cx, s, r, sub, k, cross=False):
    """Hero block with the same three ports on every use: K, V (left) and Q (centre line)."""
    c, x, y = ROLE[r], cx - BW / 2, s + 6.0
    if cross:
        cv.box(x, y, BW, BH, r, fill=DEC["mark"], stroke=INK, lw=0.8, shadow=True, radius=1.15)
        cv.gradient_rect(x + 0.1, y + 0.1, BW - 0.2, BH - 0.2, ENC["mark"], DEC["mark"], z=5.05, radius=1.05)
    else:
        cv.box(x, y, BW, BH, r, fill=c["mark"], stroke=c["ink"], lw=0.8, shadow=True, radius=1.15)
    cv.text(cx + 0.6, y + BH / 2 + 1.5, "Multi-Head Attention", size=T_NODE, weight="bold", color="white", z=7)
    cv.text(cx + 0.6, y + BH / 2 - 1.55, sub, size=6.0, style="italic", color="white", z=7)
    cv.badge(x + 0.2, y + BH - 0.2, k, r={"mark": INK}, d=3.1)
    kv = ENC if cross else c
    for px, lab, col in ((cx - 8, "K", kv), (cx - 4, "V", kv), (cx, "Q", c)):
        cv.text(px + 1.25, s + 4.8, lab, size=T_ANN, style="italic", color=col["ink"], ha="left")
    if not cross:                           # self-attention: all three ports fed by the layer below
        cv.arrow([(cx, s + 3.0), (cx - 8, s + 3.0), (cx - 8, y)], color=c["mark"], lw=0.8, head=1.2)
        cv.arrow([(cx - 4, s + 3.0), (cx - 4, y)], color=c["mark"], lw=0.8, head=1.2)
        cv.dot(cx, s + 3.0, color=c["mark"], d=1.0)
        cv.dot(cx - 4, s + 3.0, color=c["mark"], d=0.9)


def feed_forward(cv, cx, s, r):
    c = ROLE[r]
    cv.box(cx - BW / 2, s + 6.0, BW, BH, r, "Feed Forward", r"position-wise, $d_{\mathrm{ff}}=2048$",
           fill=c["soft"], size=T_NODE, gap=1.5)


def panel_a(cv):
    cv.label(2.5, H - 0.9, "a", "Model architecture", size=8.0)

    # inputs, embeddings (one shared weight matrix: amber), positional encoding
    for cx, r, words, lab, emb in ((EX, "blue", SRC, "Inputs", "Input Embedding"),
                                   (DX, "coral", TGT_IN, "Outputs (shifted right)", "Output Embedding")):
        c = ROLE[r]
        token_row(cv, cx, 5.4, words, r)
        cv.text(cx, 3.2, lab, size=T_BODY, weight="bold", color=c["ink"])
        cv.arrow([(cx, 9.0), (cx, 11.0)], color=c["mark"], lw=0.95, head=1.2)
        cv.trap(cx - 11, 11.0, 22, 4.8, "amber", narrow="top", ratio=0.84, title=emb, size=6.5)
        cv.arrow([(cx, 15.8), (cx, 17.6)], color=c["mark"], lw=0.95, head=1.2)
        cv.op(cx, 19.0, "+", r=r, d=2.8)
    mx = (EX + DX) / 2                  # PE(pos, 2i) = sin(pos / 10000^(2i / d_model)), d_model = 512
    cv.box(mx - 5.5, 16.4, 11, 5.2, "neutral", fill="white", radius=0.8, lw=0.55)
    pos = np.linspace(0, 24, 200)
    for two_i, col, lw in ((0, "#B9C0CA", 0.6), (48, NEU["stroke"], 0.75), (96, NEU["ink"], 0.9)):
        cv.ax.plot(mx - 4.9 + 9.8 * pos / 24, 19.0 + 2.0 * np.sin(pos / 10000 ** (two_i / 512.0)), color=col, lw=lw,
                   zorder=6, solid_capstyle="round")
    cv.arrow([(mx - 5.5, 19.0), (EX + 1.4, 19.0)], color=MUTED, lw=0.7, head=1.2)
    cv.arrow([(mx + 5.5, 19.0), (DX - 1.4, 19.0)], color=MUTED, lw=0.7, head=1.2)
    cv.text(mx, 14.3, "Positional encoding", size=T_BODY, weight="bold", color=NEU["ink"])
    cv.text(mx, 11.9, "fixed sinusoids", size=T_ANN, style="italic", color=MUTED)
    cv.text(EX - 2.9, 19.0, r"$d_{\mathrm{model}}=512$", size=T_BODY, color=MUTED, ha="right")

    # encoder: self-attention, feed-forward
    etop = layer_frame(cv, EX, 2, "blue", "Encoder")
    main_wire(cv, EX, 20.4, S0 + 6.0, ENC)
    attention(cv, EX, S0, "blue", "self-attention", 1)
    add_norm(cv, EX, S0, "blue")
    main_wire(cv, EX, S0 + P, S0 + P + 6.0, ENC)
    feed_forward(cv, EX, S0 + P, "blue")
    add_norm(cv, EX, S0 + P, "blue")

    # encoder output z, drawn as an object, feeds K and V of every decoder layer
    zx, zy, zs = 41.5, etop + 1.5, 7.2
    cv.arrow([(EX, S0 + 2 * P), (EX, zy + zs / 2), (zx, zy + zs / 2)], color=ENC["mark"], lw=0.95, head=1.5)
    cv.matrix(zx, zy, zs, zs, rows=5, cols=4, r="blue", seed=3)
    cv.rich((EX + zx) / 2 + 0.6, zy + zs / 2 + 2.1, [("encoder output ", ENC["ink"]), (r"$\mathbf{z}$", ENC["ink"])],
            size=T_BODY, ha="center")
    s2 = S0 + P
    kx = zx + zs / 2
    cv.arrow([(kx, zy), (kx, s2 + 3.0), (DX - 4, s2 + 3.0), (DX - 4, s2 + 6.0)], color=ENC["mark"], lw=0.95,
             head=1.3)
    cv.arrow([(DX - 8, s2 + 3.0), (DX - 8, s2 + 6.0)], color=ENC["mark"], lw=0.95, head=1.3)
    cv.dot(DX - 8, s2 + 3.0, color=ENC["mark"], d=1.0)
    cv.text(kx + 2.3, (zy + s2 + 3.0) / 2, "to every decoder layer", size=T_ANN, style="italic",
            color=ENC["ink"], rotation=90)

    # decoder: masked self-attention, encoder-decoder attention, feed-forward
    dtop = layer_frame(cv, DX, 3, "coral", "Decoder")
    main_wire(cv, DX, 20.4, S0 + 6.0, DEC)
    attention(cv, DX, S0, "coral", "masked self-attention", 2)
    add_norm(cv, DX, S0, "coral")
    main_wire(cv, DX, s2, s2 + 6.0, DEC)
    attention(cv, DX, s2, "coral", "encoder–decoder attention", 3, cross=True)
    add_norm(cv, DX, s2, "coral")
    main_wire(cv, DX, s2 + P, s2 + P + 6.0, DEC)
    feed_forward(cv, DX, s2 + P, "coral")
    add_norm(cv, DX, s2 + P, "coral")

    # output head: linear (the shared matrix again) and softmax, one distribution per position
    y = dtop + 3.9
    main_wire(cv, DX, S0 + 3 * P, y, DEC)
    cv.trap(DX - 10, y, 20, 4.6, "amber", narrow="bottom", ratio=0.84, title="Linear", size=6.5)
    cv.arrow([(DX, y + 4.6), (DX, y + 6.8)], color=DEC["mark"], lw=0.95, head=1.2)
    cv.box(DX - 10, y + 6.8, 20, 4.2, "neutral", "Softmax", size=6.5, fill="white")
    cv.arrow([(DX, y + 11.0), (DX, y + 13.2)], color=DEC["mark"], lw=0.95, head=1.2)
    yb = y + 13.2
    cs = token_row(cv, DX, yb + 7.6, TGT_OUT, "coral")
    cv.box(cs[0][0] - 4.1, yb, cs[-1][0] - cs[0][0] + 8.2, 6.4, "coral", fill="white", radius=1.0, lw=0.55)
    rng = np.random.default_rng(7)
    for k, (tx, _) in enumerate(cs):        # illustrative next-token distributions; the tallest bar is the word above
        p = rng.uniform(0.06, 0.3, 5)
        win = (2 * k + 1) % 5
        p[win] = 1.0
        for j, v in enumerate(p):
            cv.ax.add_patch(Rectangle((tx - 2.75 + j * 1.15, yb + 0.7), 0.9, 4.9 * v,
                                      fc=DEC["mark"] if j == win else DEC["soft"], ec="none", zorder=6))
    cv.text(DX, yb + 12.7, "Output probabilities (next token)", size=T_BODY, weight="bold", color=DEC["ink"])
    return etop


def key(cv, x, y, w, h):
    """Colour and glyph key, in the free corner above the encoder."""
    cv.box(x, y, w, h, "neutral", fill="white", dashed=True, container=True, radius=1.6, lw=0.6, z=2)
    rows = ["encoder states", "decoder states", "multi-head attention (b, c)", "one shared weight matrix",
            r"$\mathrm{LayerNorm}(x+\mathrm{Sublayer}(x))$", "attention scores, weights",
            r"masked: $-\infty$ before softmax"]
    step = (h - 2.4) / len(rows)
    for k, lab in enumerate(rows):
        gy, gx = y + h - 1.2 - (k + 0.5) * step, x + 4.6
        if k == 0:
            cv.box(gx - 2.2, gy - 1.3, 4.4, 2.6, "blue", fill=ENC["soft"], radius=0.6, lw=0.5, container=True)
        elif k == 1:
            cv.box(gx - 2.2, gy - 1.3, 4.4, 2.6, "coral", fill=DEC["soft"], radius=0.6, lw=0.5, container=True)
        elif k == 2:
            cv.box(gx - 2.5, gy - 1.3, 2.4, 2.6, "blue", fill=ENC["mark"], stroke=ENC["ink"], radius=0.5, lw=0.5,
                   container=True)
            cv.box(gx + 0.1, gy - 1.3, 2.4, 2.6, "coral", fill=DEC["mark"], stroke=DEC["ink"], radius=0.5, lw=0.5,
                   container=True)
        elif k == 3:
            cv.trap(gx - 2.3, gy - 1.2, 4.6, 2.4, "amber", narrow="top", ratio=0.7)
        elif k == 4:
            cv.line([(gx - 2.6, gy), (gx - 0.2, gy)], color=ENC["stroke"], lw=0.6)
            cv.op(gx + 1.2, gy, "+", r="blue", d=2.6)
        elif k == 5:
            cv.gradient_rect(gx - 2.4, gy - 1.1, 4.8, 2.2, PV(0.02), PV(1.0), z=6)
            cv.ax.add_patch(Rectangle((gx - 2.4, gy - 1.1), 4.8, 2.2, fc="none", ec=PUR["ink"], lw=0.5, zorder=6.2))
        else:
            masked_cell(cv, gx - 1.3, gy - 1.3, 2.6)
            cv.ax.add_patch(Rectangle((gx - 1.3, gy - 1.3), 2.6, 2.6, fc="none", ec="#A3ABB6", lw=0.4, zorder=6.3))
        cv.text(x + 8.6, gy, lab, size=T_BODY, ha="left")


# ------------------------------------------------------------------ (b) ---
def panel_b(cv, x, y, w, h):
    cv.section(x, y, w, h, "purple")
    pill(cv, x + 3.0, y + h, "(b) Multi-head attention", "purple")

    # wrapper: three projections per head, h heads in parallel, concatenate, project
    yq = (y + h - 7.6, y + h - 12.6, y + h - 17.6)
    cx0, cw = x + 26.5, 32.0
    cy0, chh = yq[2] - 2.0, yq[0] - yq[2] + 4.0
    for k, (lab, yy) in enumerate(zip("QKV", yq)):
        cv.text(x + 3.2, yy, f"${lab}$", size=7.0, color=INK)
        cv.matrix(x + 5.0, yy - 1.7, 6.0, 3.4, rows=3, cols=5, r="neutral", seed=11 + k)
        cv.arrow([(x + 11.0, yy), (x + 14.0, yy)], lw=0.7, head=1.2)
        cv.trap(x + 14.0, yy - 2.0, 9.0, 4.0, "neutral", narrow="right", ratio=0.62, title="Linear", size=5.9)
        cv.arrow([(x + 23.0, yy), (cx0, yy)], lw=0.7, head=1.2)
    cv.stack(cx0, cy0, cw, chh, 3, "purple", dx=1.0, dy=1.0, title="Scaled Dot-Product Attention",
             sub=r"$\mathrm{softmax}\!\left(QK^{\top}\!/\sqrt{d_k}\right)V$", size=T_NODE, tsize=6.6, gap=2.4, lw=0.7)
    cv.chip(cx0 + cw - 6.5, cy0 + chh + 2.6, r"$h=8$ heads", "purple", size=5.9, solid=True, h=3.2)
    xa = cx0 + cw + 2.0
    cv.arrow([(xa, yq[1]), (xa + 3.0, yq[1])], lw=0.7, head=1.2)
    cv.box(xa + 3.0, yq[1] - 6.0, 4.0, 12.0, "neutral", fill=NEU["soft"], radius=1.0)
    cv.text(xa + 5.0, yq[1], "Concat", size=6.2, weight="bold", color=NEU["ink"], rotation=90)
    cv.arrow([(xa + 7.0, yq[1]), (xa + 10.0, yq[1])], lw=0.7, head=1.2)
    cv.trap(xa + 10.0, yq[1] - 2.0, 9.0, 4.0, "neutral", narrow="right", ratio=0.62, title="Linear", size=5.9)
    cv.arrow([(xa + 19.0, yq[1]), (x + w - 1.6, yq[1])], lw=0.7, head=1.2)

    # one head, worked: scores -> (mask) -> softmax -> weights -> weighted sum of the values
    bx, by, bw, bh = x + 2.5, y + 2.6, w - 5.0, 26.6
    cv.zoom((cx0, cy0, cw, chh), (bx, by, bw, bh), color=PUR["stroke"], fill=PUR["soft"], alpha=0.4)
    cv.box(bx, by, bw, bh, "purple", fill="white", container=True, radius=1.6, lw=0.6)
    cv.rich(bx + 2.0, by + bh - 2.6, [("One head  ", PUR["ink"], "bold"),
                                      (r"$d_k=d_v=d_{\mathrm{model}}/h=64$", INK)], size=T_BODY)
    S = np.array([[2.1, 0.4, 0.2], [0.3, 1.8, 0.9], [0.1, 0.7, 2.4]])     # illustrative scaled scores
    A = softmax(S)
    assert np.allclose(A.sum(axis=1), 1.0) and np.all(np.round(A, 2).sum(axis=1).round(2) == 1.0), A
    cell, ch = 4.0, 3.8
    yc = by + 11.6
    my = yc - 1.5 * ch
    x1 = bx + 2.2
    cv.text(x1, yc + 3.6, "$Q$", size=7.0)
    cv.text(x1, yc - 3.6, "$K$", size=7.0)
    ox = x1 + 5.2
    cv.arrow([(x1 + 1.5, yc + 3.6), (ox, yc + 3.6), (ox, yc + 1.5)], lw=0.7, head=1.1, radius=0.8)
    cv.arrow([(x1 + 1.5, yc - 3.6), (ox, yc - 3.6), (ox, yc - 1.5)], lw=0.7, head=1.1, radius=0.8)
    cv.op(ox, yc, "x", d=3.0)
    cv.text(ox, yc + 7.0, "MatMul", size=T_ANN, style="italic", color=MUTED)
    m1 = ox + 7.4
    cv.arrow([(ox + 1.5, yc), (m1 - 3.8, yc)], lw=0.7, head=1.1)

    def headers(mx, c):                    # rows = queries, columns = keys
        for i in range(3):
            cv.text(mx - 0.9, my + (2.5 - i) * ch, f"$q_{i + 1}$", size=T_BODY, color=MUTED, ha="right")
            cv.text(mx + (i + 0.5) * c, my + 3 * ch + 1.4, f"$k_{i + 1}$", size=T_BODY, color=MUTED)
    cv.num_matrix(m1, my, S, cell=cell, ch=ch, r="purple", fmt="{:.1f}", size=T_ANN, vmin=0, vmax=3.2)
    headers(m1, cell)
    cv.text(m1 + 1.5 * cell - 1.5, my - 2.2, r"scores $QK^{\top}\!/\sqrt{d_k}$", size=T_BODY, color=PUR["ink"])
    xm = m1 + 3 * cell + 2.2
    cv.arrow([(m1 + 3 * cell, yc), (xm, yc)], lw=0.7, head=1.1)
    cv.box(xm, yc - 2.1, 10.4, 4.2, "neutral", "mask (opt.)", fill="white", dashed=True, size=5.9, weight="normal",
           radius=1.0)
    cv.arrow([(xm + 10.4, yc), (xm + 12.4, yc)], lw=0.7, head=1.1)
    cv.box(xm + 12.4, yc - 2.1, 9.8, 4.2, "purple", "softmax", fill=PUR["soft"], size=6.2, radius=1.0)
    m2 = xm + 22.2 + 5.8
    c2 = 4.5
    cv.arrow([(xm + 22.2, yc), (m2 - 3.8, yc)], lw=0.7, head=1.1)
    cv.num_matrix(m2, my, A, cell=c2, ch=ch, r="purple", fmt="{:.2f}", size=T_ANN, vmin=0, vmax=1,
                  hi=[(0, 0), (1, 1), (2, 2)])
    headers(m2, c2)
    cv.text(m2 + 1.5 * c2 - 1.5, my - 2.2, "weights, rows sum to 1", size=T_BODY, color=PUR["ink"])
    o2 = m2 + 3 * c2 + 4.6
    cv.arrow([(m2 + 3 * c2, yc), (o2 - 1.5, yc)], lw=0.7, head=1.1)
    cv.op(o2, yc, "x", d=3.0)
    cv.text(o2, yc - 3.4, "MatMul", size=T_ANN, style="italic", color=MUTED)
    cv.text(o2, yc + 5.6, "$V$", size=7.0)
    cv.arrow([(o2, yc + 4.3), (o2, yc + 1.5)], lw=0.7, head=1.1)
    cv.arrow([(o2 + 1.5, yc), (bx + bw - 0.8, yc)], lw=0.7, head=1.1)


# ------------------------------------------------------------------ (c) ---
def use_card(cv, x, y, w, h, k, title, r, rows, cols, rrole, crole, qkv, note, foot, A, mask=None, cell=3.7,
             grad=False):
    c = ROLE[r]
    if grad:
        cv.gradient_rect(x, y, w, h, ENC["fill"], DEC["fill"], z=1.4, radius=1.8)
        cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.8", fc="none",
                                       ec=mix(ENC["stroke"], DEC["stroke"], 0.5), lw=0.6, zorder=1.5))
    else:
        cv.box(x, y, w, h, r, container=True, radius=1.8, lw=0.6, z=1.4)
    top = y + h
    cv.badge(x + 3.0, top - 3.6, k, r={"mark": INK}, d=3.2)
    ink = INK if grad else c["ink"]
    for i, t in enumerate(title):
        cv.text(x + 5.4, top - 2.4 - 2.5 * i, t, size=6.5, weight="bold", color=ink, ha="left")
    cv.tokens(x + w / 2 - 5.3, top - 11.3, 3, w=3.2, h=3.2, gap=0.5, fills=qkv, labels=["Q", "K", "V"], size=5.9)
    cv.text(x + w / 2, top - 13.5, note, size=T_ANN, style="italic", color=INK)
    R, C = A.shape
    gw = 6.9 + C * cell
    mx, mtop = x + (w - gw) / 2 + 6.9, top - 22.4 - (5 - R) * cell / 2     # centred in a five-row slot
    my = mtop - R * cell
    attn_grid(cv, mx, my, A, cell, mask)
    for i, t in enumerate(rows):
        cv.text(mx - 0.7, mtop - (i + 0.5) * cell, t, size=T_ANN, ha="right", color=ROLE[rrole]["ink"])
    for j, t in enumerate(cols):
        cv.text(mx + (j + 0.5) * cell, mtop + 0.6, t, size=T_ANN, va="bottom", rotation=90, color=ROLE[crole]["ink"])
    cv.text(mx - 0.8, mtop + 4.7, r"$K\rightarrow$", size=T_ANN, ha="right", color=ROLE[crole]["ink"])
    cv.text(mx - 0.8, mtop + 1.5, r"$Q\downarrow$", size=T_ANN, ha="right", color=ROLE[rrole]["ink"])
    fy = top - 22.4 - 5 * cell - 2.6
    for i, t in enumerate(foot):
        if t.startswith("#"):               # a masked-cell swatch before the text
            tw = cv.text_width(t[1:], T_ANN) + 3.4
            masked_cell(cv, x + w / 2 - tw / 2, fy - 3.0 * i - 1.2, 2.4)
            cv.text(x + w / 2 - tw / 2 + 3.4, fy - 3.0 * i, t[1:], size=T_ANN, style="italic", ha="left")
        else:
            cv.text(x + w / 2, fy - 3.0 * i, t, size=T_ANN, style="italic")


def panel_c(cv, x, y, w, h):
    cv.section(x, y, w, h, "neutral")
    pill(cv, x + 3.0, y + h, "(c) Three uses of attention", "neutral")
    n, m = len(SRC), len(TGT_IN)
    A1 = softmax(np.array([[2.0, 0.6, 0.1, 0.0], [0.5, 2.0, 0.4, 0.8], [0.1, 0.3, 1.6, 1.5], [0.0, 0.9, 1.4, 1.8]]))
    S2 = np.array([[1.0, 0, 0, 0, 0], [0.9, 1.6, 0, 0, 0], [0.3, 1.1, 1.7, 0, 0], [0.2, 0.4, 1.2, 1.8, 0],
                   [0.1, 0.3, 0.5, 1.5, 1.7]])
    mask = np.triu(np.ones((m, m), bool), 1)          # position i may not attend to positions after i
    A2 = softmax(np.where(mask, -np.inf, S2))
    A3 = softmax(np.array([[0.9, 0.5, 0.3, 0.4], [2.2, 0.6, 0.1, 0.1], [0.5, 2.3, 0.3, 0.2], [0.1, 0.4, 2.2, 0.9],
                           [0.1, 0.2, 0.9, 2.4]]))
    assert A1.shape == (n, n) and A2.shape == (m, m) and A3.shape == (m, n)
    assert np.allclose(A2[mask], 0) and all(np.allclose(a.sum(axis=1), 1) for a in (A1, A2, A3))
    cy, chh = y + 1.5, h - 5.6
    w1, w2 = 25.0, 29.0
    w3 = w - 3.0 - w1 - w2 - 3.0
    use_card(cv, x + 1.5, cy, w1, chh, 1, ("Encoder", "self-attention"), "blue", SRC, SRC, "blue", "blue",
             ["blue"] * 3, "previous encoder layer", ("each position attends", "to all positions"), A1)
    use_card(cv, x + 3.0 + w1, cy, w2, chh, 2, ("Masked decoder", "self-attention"), "coral", TGT_IN, TGT_IN,
             "coral", "coral", ["coral"] * 3, "previous decoder layer",
             ("position i attends to ≤ i", "#masked: −∞ before softmax"), A2, mask)
    use_card(cv, x + 4.5 + w1 + w2, cy, w3, chh, 3, ("Encoder–decoder", "attention"), "purple", TGT_IN, SRC,
             "coral", "blue", ["coral", "blue", "blue"], r"$K, V$: encoder output $\mathbf{z}$",
             ("every output position", "attends over all inputs"), A3, grad=True)


def render(out):
    cv = Canvas(W, H, family="serif", size=T_NODE)
    etop = panel_a(cv)
    key(cv, 2.5, etop + 12.6, 41.0, H - 6.0 - (etop + 12.6))
    panel_b(cv, 90.5, 63.5, 85.5, H - 3.7 - 63.5)
    panel_c(cv, 90.5, 2.0, 85.5, 56.5)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/transformer")
    print("\n".join(render(ap.parse_args().out)))
