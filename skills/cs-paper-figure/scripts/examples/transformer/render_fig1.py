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
    it. The three attention blocks are the only saturated blocks and carry the numbers 1-3 that (c) opens.
  * Palette, four hues: blue = encoder states, coral = decoder states (frames, wires, tokens, ports),
    amber = the one shared weight matrix (three trapezoids), purple = attention scores and weights.
    Greys are scaffolding. Text is near-black; the only coloured words are the two frame tabs.
  * Type, three sizes (T_HEAD, T_LABEL, T_FINE). Everything with a subscript is set at T_LABEL so that
    subscripts stay at 5 pt. Bold: panel letters, the two frame tabs, the hero titles, badge numerals and
    the winning weights.
  * Strokes, two weights: LW for every outline, operator, residual and auxiliary arrow; LW_FLOW for the
    token stream only. One dash pattern (a scope, an option, a zoom ray).
  * One panel treatment: bare panels under a plain head, separated by white gutters. The only frames are
    the dashed layer scopes (one of N identical layers) and the solid zoom box of one head.
  * Every attention block has the same three ports (K, V, Q); only the colour of what enters them changes,
    and the encoder-decoder block is a blue-to-coral blend. Add & Norm is opened into a residual wire, a
    circled + and a LayerNorm bar.
  * (a) keeps the paper's bottom-to-top flow with a running English-to-German example, so "shifted right"
    is the one-column offset between the decoder's input row and the predicted row. The encoder output z
    is drawn as an object, one d_model vector per input token.
  * (b) multi-head wrapper over a worked single head: scores, optional mask, softmax, weights. The weights
    are computed in this script from the printed scores and asserted to sum to 1 per row.
  * (c) the three uses as query-by-key matrices whose rows and columns are the example's own token chips,
    in the colour of the stream they come from; the causal mask is hatched.
  * The positional-encoding curves are the paper's formula evaluated for d_model = 512 at dimensions
    2i = 0, 48, 96 over positions 0-24. Example sentence, score values, attention patterns, the texture of
    z and the probability bars are illustrative; the tokens are whole words for legibility (the paper uses
    byte-pair / word-piece units), and <s> / </s> stand for the start and end symbols implied by
    "shifted right".

Size: 178 x 129 mm (two-column width); text 6.0 / 7.2 / 8.5 pt, math subscripts 5.04 pt.
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from matplotlib import colors as mcolors  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

from paperkit import HAIR, INK, LINE, MUTED, ROLE, Canvas, mix  # noqa: E402

STEM = "transformer_fig1"
W, H = 178.0, 129.0
ENC, DEC, AMB, PUR, NEU = (ROLE[k] for k in ("blue", "coral", "amber", "purple", "neutral"))
PV = mcolors.LinearSegmentedColormap.from_list("pv", ["#FBF9FE", PUR["soft"], PUR["mark"], PUR["ink"]])

# ---- the visual system: every size, stroke and radius in the figure comes from these ------------------
T_HEAD, T_LABEL, T_FINE = 8.5, 7.2, 6.0     # panel heads; labels and all math; fine print, tokens, cell values
LW, LW_FLOW = 0.6, 1.0                       # outlines, operators, residual and auxiliary arrows; the token stream
HEAD, HEAD_FLOW = 1.2, 1.6                   # arrow-head length in mm, one per weight
DASH = (0, (3, 2))                           # a scope, an option or a zoom ray: never a concrete flow
D_OP, D_BADGE = 3.0, 3.2                     # operator circle; numbered disc
R_CHIP, R_NODE, R_FRAME = 0.8, 1.2, 2.4      # corner radius per size class
TOK_W, TOK_H, TOK_GAP = 7.6, 3.6, 0.4        # one token chip, the same in (a) and (c)

SRC = ["I", "like", "green", "tea"]          # x_1..x_n   (illustrative)
TGT_IN = ["<s>", "Ich", "mag", "grünen", "Tee"]   # outputs shifted right
TGT_OUT = ["Ich", "mag", "grünen", "Tee", "</s>"]

# layout, mm
Y0 = 8.0                       # bottom of the panels; the key strip sits below
BASE = H - 3.4                 # shared baseline of the three panel heads' top row
EX, DX = 18.5, 65.5            # centre lines of the encoder and decoder columns
S0, P = 29.5, 22.2             # first sub-layer base; pitch of one sub-layer
BW, BH = 28.0, 7.2             # sub-layer block
PORT = 4.8                     # spacing of the K, V, Q ports
RES = 16.5                     # residual corridor, right of the centre line
FL, FR = 17.0, 19.0            # frame extent left / right of the centre line
RAIL = 44.0                    # encoder output runs down the gutter between the two stacks
RX, RW = 93.0, 83.5            # right column: panels (b) and (c)


def softmax(s):
    e = np.exp(s - np.max(s, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


# ------------------------------------------------------------- primitives ---
def node(cv, x, y, w, h, fill, stroke, radius=R_NODE, dashed=False, container=False, z=5):
    return cv.box(x, y, w, h, "neutral", fill=fill, stroke=stroke, lw=LW, radius=radius, dashed=dashed,
                  container=container, z=z)


def flow(cv, pts, c):
    """The token stream: the only heavy stroke."""
    cv.arrow(pts, color=c["mark"], lw=LW_FLOW, head=HEAD_FLOW)


def thin(cv, pts, color=LINE, **kw):
    cv.arrow(pts, color=color, lw=LW, head=HEAD, **kw)


def head(cv, x, letter, title):
    """Panel head: bold letter, regular title. Returns the end x."""
    return cv.rich(x, BASE, [(f"({letter}) ", INK, "bold"), (title, INK)], size=T_HEAD, va="baseline")


def badge(cv, x, y, k, z=12):
    cv.ax.add_patch(Circle((x, y), D_BADGE / 2, fc=INK, ec="white", lw=LW, zorder=z))
    cv.text(x, y - 0.05, str(k), size=T_FINE, color="white", weight="bold", z=z + 1)


def chips(cv, x, y, words, r, vertical=False, upright=False, fills=None, w=TOK_W, h=TOK_H, gap=TOK_GAP,
          size=T_FINE, style="normal"):
    """Token chips with near-black text. Row (default), column of rows (vertical) or a row of upright chips
    with the text turned (upright), for the column heads of a matrix. Returns the chip centres."""
    n = len(words)
    if upright:
        w, h = h, w
    out = []
    for i, t in enumerate(words):
        xx, yy = (x, y - i * (h + gap)) if vertical else (x + i * (w + gap), y)
        cv.tokens(xx, yy, 1, w=w, h=h, r=fills[i] if fills else r, lw=LW)
        cv.text(xx + w / 2, yy + h / 2, t, size=size, color=INK, rotation=90 if upright else 0, style=style, z=9)
        out.append((xx + w / 2, yy + h / 2))
    assert n == len(out)
    return out


def chip_row(cv, cx, y, words, r):
    return chips(cv, cx - (len(words) * TOK_W + (len(words) - 1) * TOK_GAP) / 2, y, words, r)


def hatch(cv, x, y, w, h, z=6):
    """A masked cell: grey field with two diagonal strokes."""
    for a, b in ((0.0, 0.55), (0.45, 1.0)):
        cv.ax.plot([x + (a + 0.12) * w, x + (b - 0.12) * w], [y + 0.14 * h, y + (b - a + 0.0) * h],
                   color="#A3ABB6", lw=LW, zorder=z + 0.1, solid_capstyle="round")


def cells(cv, x, y, fills, cw, ch, edge, texts=None, bold=(), z=6):
    """Matrix drawn as flat cells: white dividers and one outline, both at LW. fills[i][j] is a colour or
    None (masked: hatched). texts[i][j] are the cell values, bold and bordered on `bold`. Row 0 is the top."""
    R, C = len(fills), len(fills[0])
    cv.solids.append((x, y, C * cw, R * ch, "matrix", None))
    for i in range(R):
        for j in range(C):
            cx, cy = x + j * cw, y + (R - 1 - i) * ch
            fc = fills[i][j]
            cv.ax.add_patch(Rectangle((cx, cy), cw, ch, fc="#ECEEF1" if fc is None else fc, ec="white", lw=LW,
                                      zorder=z))
            if fc is None:
                hatch(cv, cx, cy, cw, ch, z)
            elif texts is not None:
                rgb = mcolors.to_rgb(fc)
                dark = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2] < 0.55
                cv.text(cx + cw / 2, cy + ch / 2, texts[i][j], size=T_FINE, color="white" if dark else INK,
                        weight="bold" if (i, j) in bold else "normal", z=z + 1)
    for i, j in bold:
        cv.ax.add_patch(Rectangle((x + j * cw, y + (R - 1 - i) * ch), cw, ch, fc="none", ec=edge, lw=LW,
                                  zorder=z + 0.5))
    cv.ax.add_patch(Rectangle((x, y), C * cw, R * ch, fc="none", ec=edge, lw=LW, zorder=z + 0.6))


def texture(r, rows, cols, seed):
    """Illustrative cell fills on one role's ramp (a tensor whose values are not the point)."""
    c = ROLE[r]
    cm = mcolors.LinearSegmentedColormap.from_list("t", [c["fill"], c["soft"], c["mark"]])
    v = np.random.default_rng(seed).uniform(0.05, 0.8, (rows, cols))
    return [[cm(float(v[i, j])) for j in range(cols)] for i in range(rows)]


def trapezoid(cv, x, y, w, h, r, narrow, title, size=T_LABEL, ratio=0.84):
    cv.trap(x, y, w, h, r, narrow=narrow, ratio=ratio, lw=LW)
    cv.text(x + w / 2, y + h / 2, title, size=size, color=INK, z=8)


# ------------------------------------------------------------------ (a) ---
def layer_frame(cv, cx, n_sub, r, name):
    """One of N identical layers: a dashed scope, two more behind it, the name on a tab on the border."""
    c = ROLE[r]
    x, y, w, h = cx - FL, S0 - 0.9, FL + FR, n_sub * P + 5.7
    for k in (2, 1):
        node(cv, x + k, y + k, w, h, mix(c["fill"], "#FFFFFF", 0.35), c["stroke"], radius=R_FRAME, dashed=True,
             container=True, z=0.5 - 0.1 * k)
    node(cv, x, y, w, h, "white", c["stroke"], radius=R_FRAME, dashed=True, container=True, z=1)
    top, th = y + h, 4.2
    tw = cv.text_width(name, T_LABEL, "bold") + 3.2
    node(cv, x + 1.2, top - th / 2, tw, th, c["soft"], c["stroke"], radius=th / 2, container=True, z=3)
    cv.text(x + 1.2 + tw / 2, top, name, size=T_LABEL, weight="bold", color=c["ink"], z=4)
    cv.text(x + w - 1.6, top - 2.4, "$N=6$ layers", size=T_LABEL, color=INK, ha="right", z=4)
    return top


def add_norm(cv, cx, s, r):
    """LayerNorm(x + Sublayer(x)): residual wire, circled +, LayerNorm bar. Returns the top of the bar."""
    c = ROLE[r]
    yo = s + 14.9 + D_OP / 2
    thin(cv, [(cx, s + 1.4), (cx + RES, s + 1.4), (cx + RES, yo), (cx + D_OP / 2, yo)], color=c["stroke"])
    cv.dot(cx, s + 1.4, color=c["mark"], d=1.0)
    flow(cv, [(cx, s + 6.0 + BH), (cx, yo - D_OP / 2)], c)
    cv.op(cx, yo, "+", r=r, d=D_OP, lw=LW)
    cv.line([(cx, yo + D_OP / 2), (cx, s + 18.4)], color=c["mark"], lw=LW_FLOW)
    node(cv, cx - 8.5, s + 18.4, 17.0, P - 18.4, "white", c["stroke"], radius=R_CHIP)
    cv.text(cx, s + 18.4 + (P - 18.4) / 2, "LayerNorm", size=T_LABEL, color=INK, z=6)
    return s + P


def attention(cv, cx, s, r, sub, k, cross=False):
    """Hero block with the same three ports on every use: K, V (left) and Q (centre line)."""
    c, x, y = ROLE[r], cx - BW / 2, s + 6.0
    if cross:
        node(cv, x, y, BW, BH, DEC["mark"], mix(ENC["ink"], DEC["ink"], 0.5))
        cv.gradient_rect(x + 0.1, y + 0.1, BW - 0.2, BH - 0.2, ENC["mark"], DEC["mark"], z=5.05, radius=R_NODE - 0.1)
    else:
        node(cv, x, y, BW, BH, c["mark"], c["ink"])
    cv.text(cx + 0.7, y + BH / 2 + 1.5, "Multi-Head Attention", size=T_LABEL, weight="bold", color="white", z=7)
    cv.text(cx + 0.7, y + BH / 2 - 1.6, sub, size=T_FINE, style="italic", color="white", z=7)
    badge(cv, x + 0.3, y + BH - 0.3, k)
    for i, lab in enumerate("KVQ"):
        cv.text(cx - (2 - i) * PORT + 1.1, s + 4.6, f"${lab}$", size=T_LABEL, color=INK, ha="left")
    if not cross:                           # self-attention: all three ports fed by the layer below
        flow(cv, [(cx, s + 3.0), (cx - 2 * PORT, s + 3.0), (cx - 2 * PORT, y)], c)
        flow(cv, [(cx - PORT, s + 3.0), (cx - PORT, y)], c)
        cv.dot(cx, s + 3.0, color=c["mark"], d=1.0)
        cv.dot(cx - PORT, s + 3.0, color=c["mark"], d=1.0)


def feed_forward(cv, cx, s, r):
    c = ROLE[r]
    node(cv, cx - BW / 2, s + 6.0, BW, BH, c["soft"], c["stroke"])
    cv.text(cx, s + 6.0 + BH / 2 + 1.55, "Feed Forward", size=T_LABEL, color=INK, z=6)
    cv.text(cx, s + 6.0 + BH / 2 - 1.6, r"position-wise, $d_{\mathrm{ff}}=2048$", size=T_LABEL, color=INK, z=6)


def panel_a(cv):
    head(cv, 1.5, "a", "Model architecture")

    # inputs, embeddings (one shared weight matrix: amber), positional encoding
    yt = Y0 + 3.6
    yo = yt + TOK_H + 2.0 + 4.8 + 2.0 + D_OP / 2
    for cx, r, words, lab, emb in ((EX, "blue", SRC, "Inputs", "Input Embedding"),
                                   (DX, "coral", TGT_IN, "Outputs (shifted right)", "Output Embedding")):
        c = ROLE[r]
        chip_row(cv, cx, yt, words, r)
        cv.text(cx, Y0 + 0.5, lab, size=T_LABEL, color=INK, va="baseline")
        flow(cv, [(cx, yt + TOK_H), (cx, yt + TOK_H + 2.0)], c)
        trapezoid(cv, cx - 12, yt + TOK_H + 2.0, 24, 4.8, "amber", "top", emb)
        flow(cv, [(cx, yt + TOK_H + 6.8), (cx, yo - D_OP / 2)], c)
        cv.op(cx, yo, "+", r=r, d=D_OP, lw=LW)
        flow(cv, [(cx, yo + D_OP / 2), (cx, S0 + 6.0)], c)
    mx = (EX + DX) / 2                  # PE(pos, 2i) = sin(pos / 10000^(2i / d_model)), d_model = 512
    node(cv, mx - 5.0, yo - 2.3, 10.0, 4.6, "white", NEU["stroke"], radius=R_CHIP)
    pos = np.linspace(0, 24, 200)
    for two_i, col in ((0, "#B9C0CA"), (48, NEU["stroke"]), (96, NEU["ink"])):
        cv.ax.plot(mx - 4.4 + 8.8 * pos / 24, yo + 1.75 * np.sin(pos / 10000 ** (two_i / 512.0)), color=col, lw=LW,
                   zorder=6, solid_capstyle="round")
    thin(cv, [(mx - 5.0, yo), (EX + D_OP / 2, yo)])
    thin(cv, [(mx + 5.0, yo), (DX - D_OP / 2, yo)])
    cv.text(mx, yo - 4.6, "Positional encoding", size=T_LABEL, color=INK)
    cv.text(mx, yo - 7.4, "fixed sinusoids", size=T_FINE, style="italic", color=MUTED)

    # encoder: self-attention, feed-forward
    etop = layer_frame(cv, EX, 2, "blue", "Encoder")
    attention(cv, EX, S0, "blue", "self-attention", 1)
    s = add_norm(cv, EX, S0, "blue")
    flow(cv, [(EX, s), (EX, s + 6.0)], ENC)
    feed_forward(cv, EX, s, "blue")
    s = add_norm(cv, EX, s, "blue")

    # encoder output z: one d_model vector per input token, read as K and V by every decoder layer
    zx, zy, zr = EX - BW / 2, etop + 4.6, TOK_H + TOK_GAP
    zh = len(SRC) * zr - TOK_GAP
    chips(cv, zx, zy + zh - TOK_H, SRC, "blue", vertical=True)
    mxz, mwz = zx + TOK_W + 0.6, BW - TOK_W - 0.6
    cells(cv, mxz, zy - TOK_GAP / 2, texture("blue", len(SRC), 12, 3), mwz / 12, zr, ENC["ink"])
    flow(cv, [(EX, s), (EX, zy - TOK_GAP / 2)], ENC)
    ym, dm = zy + zh + 2.0, r"$d_{\mathrm{model}}=512$"       # the width of every state, said once, as a measure
    hw = cv.text_width(dm, T_LABEL) / 2 + 0.7
    cv.text(mxz + mwz / 2, ym, dm, size=T_LABEL, color=INK)
    thin(cv, [(mxz + mwz / 2 - hw, ym), (mxz, ym)])
    thin(cv, [(mxz + mwz / 2 + hw, ym), (mxz + mwz, ym)])
    cv.text(zx, ym + 5.9, r"Encoder output $\mathbf{z}$", size=T_LABEL, color=INK, ha="left")
    cv.text(zx, ym + 3.1, "K and V, to every decoder layer", size=T_FINE, style="italic", color=INK,
            ha="left")
    s2 = S0 + P
    flow(cv, [(mxz + mwz, zy + zh / 2), (RAIL, zy + zh / 2), (RAIL, s2 + 3.0), (DX - PORT, s2 + 3.0),
              (DX - PORT, s2 + 6.0)], ENC)
    flow(cv, [(DX - 2 * PORT, s2 + 3.0), (DX - 2 * PORT, s2 + 6.0)], ENC)
    cv.dot(DX - 2 * PORT, s2 + 3.0, color=ENC["mark"], d=1.0)

    # decoder: masked self-attention, encoder-decoder attention, feed-forward
    dtop = layer_frame(cv, DX, 3, "coral", "Decoder")
    attention(cv, DX, S0, "coral", "masked self-attention", 2)
    s = add_norm(cv, DX, S0, "coral")
    flow(cv, [(DX, s), (DX, s + 6.0)], DEC)
    attention(cv, DX, s, "coral", "encoder–decoder attention", 3, cross=True)
    s = add_norm(cv, DX, s, "coral")
    flow(cv, [(DX, s), (DX, s + 6.0)], DEC)
    feed_forward(cv, DX, s, "coral")
    s = add_norm(cv, DX, s, "coral")

    # output head: linear (the shared matrix again) and softmax, one distribution per position
    y = dtop + 3.3
    flow(cv, [(DX, s), (DX, y)], DEC)
    trapezoid(cv, DX - 10, y, 20, 4.8, "amber", "bottom", "Linear")
    flow(cv, [(DX, y + 4.8), (DX, y + 6.8)], DEC)
    node(cv, DX - 10, y + 6.8, 20, 3.8, "white", NEU["stroke"], radius=R_CHIP)
    cv.text(DX, y + 8.7, "Softmax", size=T_LABEL, color=INK, z=6)
    flow(cv, [(DX, y + 10.6), (DX, y + 12.6)], DEC)
    yb = y + 12.6
    cs = chip_row(cv, DX, yb + 7.0, TGT_OUT, "coral")
    node(cv, cs[0][0] - TOK_W / 2, yb, cs[-1][0] - cs[0][0] + TOK_W, 6.0, "white", DEC["stroke"], radius=R_CHIP)
    rng = np.random.default_rng(7)
    for k, (tx, _) in enumerate(cs):        # illustrative next-token distributions; the tallest bar is the word above
        p = rng.uniform(0.06, 0.3, 5)
        win = (2 * k + 1) % 5
        p[win] = 1.0
        for j, v in enumerate(p):
            cv.ax.add_patch(Rectangle((tx - 2.75 + j * 1.15, yb + 0.6), 0.9, 4.7 * v,
                                      fc=DEC["mark"] if j == win else DEC["soft"], ec="none", zorder=6))
    assert yb + 7.0 + TOK_H + 1.0 < H, "output head leaves the canvas"
    for i, t in enumerate(("Output probabilities", "(next token)")):
        cv.text(cs[0][0] - TOK_W / 2 - 1.6, yb + 4.5 - 3.0 * i, t, size=T_LABEL, color=INK, ha="right")


def key(cv, y):
    """Key strip along the bottom: every colour and glyph the panels do not label, each beside its sample."""
    cv.line([(1.5, y + 2.9), (W - 1.5, y + 2.9)], color=HAIR, lw=LW)

    def g_states(r):
        return lambda x: chips(cv, x, y - TOK_H / 2, [""], r, w=4.4)

    def g_shared(x):
        cv.trap(x, y - 1.5, 5.0, 3.0, "amber", narrow="top", ratio=0.7, lw=LW)

    def g_addnorm(x):
        thin(cv, [(x, y), (x + 3.4, y)], color=ENC["stroke"])
        cv.op(x + 3.4 + D_OP / 2, y, "+", r="blue", d=D_OP, lw=LW)
        cv.line([(x + 3.4 + D_OP, y), (x + 7.2, y)], color=ENC["mark"], lw=LW_FLOW)
        node(cv, x + 7.2, y - 1.5, 4.4, 3.0, "white", ENC["stroke"], radius=R_CHIP)

    def g_weight(x):
        cv.text(x, y, "0", size=T_FINE, color=INK, ha="left")
        cv.gradient_rect(x + 1.7, y - 1.3, 8.0, 2.6, PV(0.0), PV(1.0), z=6)
        cv.ax.add_patch(Rectangle((x + 1.7, y - 1.3), 8.0, 2.6, fc="none", ec=PUR["ink"], lw=LW, zorder=6.2))
        cv.text(x + 10.4, y, "1", size=T_FINE, color=INK, ha="left")

    items = [(4.4, g_states("blue"), "encoder states"), (4.4, g_states("coral"), "decoder states"),
             (5.0, g_shared, "one shared weight matrix"),
             (11.6, g_addnorm, r"Add & Norm: $\mathrm{LayerNorm}(x+\mathrm{Sublayer}(x))$"),
             (11.6, g_weight, "attention weight")]
    widths = [gw + 1.2 + cv.text_width(lab, T_FINE) for gw, _, lab in items]
    gap = (W - 3.0 - sum(widths)) / (len(items) - 1)
    assert gap >= 4.0, f"key strip does not fit: gap {gap:.1f} mm"
    x = 1.5
    for (gw, draw, lab), wd in zip(items, widths):
        draw(x)
        cv.text(x + gw + 1.2, y, lab, size=T_FINE, color=INK, ha="left")
        x += wd + gap


# ------------------------------------------------------------------ (b) ---
def panel_b(cv, ybot):
    """Multi-head wrapper, then one head worked with numbers. Returns nothing; occupies ybot .. the head row."""
    x = RX
    xe = head(cv, x, "b", "Multi-head attention")
    cv.text(xe + 2.0, BASE, "inside blocks", size=T_FINE, color=MUTED, ha="left", va="baseline")
    bx0 = xe + 2.0 + cv.text_width("inside blocks", T_FINE) + 1.0 + D_BADGE / 2
    for k in (1, 2, 3):
        badge(cv, bx0 + (k - 1) * (D_BADGE + 0.5), BASE + 1.0, k)

    # one head, worked: scores -> (mask) -> softmax -> weights -> weighted sum of the values
    bx, by, bw, bh = x, ybot, RW, 27.0
    yq0 = by + bh + 7.0 + 2.2 + 10.0
    yq = (yq0, yq0 - 5.0, yq0 - 10.0)

    # wrapper: three projections per head, h heads in parallel, concatenate, project
    cx0, cw = x + 23.8, 33.5
    cy0, chh = yq[2] - 2.2, 14.4
    for k, (lab, yy) in enumerate(zip("QKV", yq)):
        cv.text(x + 1.4, yy, f"${lab}$", size=T_LABEL, color=INK)
        cells(cv, x + 3.4, yy - 1.7, texture("neutral", 3, 5, 11 + k), 1.2, 3.4 / 3, NEU["ink"])
        thin(cv, [(x + 9.4, yy), (x + 12.0, yy)])
        trapezoid(cv, x + 12.0, yy - 2.0, 9.0, 4.0, "neutral", "right", "Linear", size=T_FINE, ratio=0.62)
        thin(cv, [(x + 21.0, yy), (cx0, yy)])
    cv.stack(cx0, cy0, cw, chh, 3, "purple", dx=1.0, dy=1.0, lw=LW, radius=R_NODE, fill=PUR["fill"])
    cv.text(cx0 + cw / 2, cy0 + chh / 2 + 2.5, "Scaled Dot-Product Attention", size=T_LABEL, color=INK, z=7)
    cv.text(cx0 + cw / 2, cy0 + chh / 2 - 2.3, r"$\mathrm{softmax}(QK^{\top}\!/\sqrt{d_k}\,)\,V$",
            size=T_LABEL, color=INK, z=7)
    ylab = cy0 + chh + 2.0 + 1.9
    cv.text(cx0 + cw / 2 + 1.0, ylab, "$h=8$ heads in parallel", size=T_FINE, color=INK)
    xa = cx0 + cw + 2.0
    thin(cv, [(xa, yq[1]), (xa + 2.7, yq[1])])
    node(cv, xa + 2.7, cy0, 4.0, chh + 2.0, NEU["soft"], NEU["stroke"], radius=R_CHIP)
    cv.text(xa + 4.7, ylab, "Concat", size=T_FINE, color=INK)
    thin(cv, [(xa + 6.7, yq[1]), (xa + 9.5, yq[1])])
    trapezoid(cv, xa + 9.5, yq[1] - 2.0, 9.0, 4.0, "neutral", "right", "Linear", size=T_FINE, ratio=0.62)
    thin(cv, [(xa + 18.5, yq[1]), (x + RW - 0.5, yq[1])])

    # zoom: one of the h heads, opened
    a, b, c, d = (cx0, cy0), (cx0 + cw, cy0), (bx + R_FRAME, by + bh), (bx + bw - R_FRAME, by + bh)
    cv.ax.add_patch(Polygon([a, c, d, b], fc=PUR["soft"], ec="none", alpha=0.4, zorder=1.9))
    for p, q in ((a, c), (b, d)):
        cv.ax.plot([p[0], q[0]], [p[1], q[1]], color=PUR["stroke"], lw=LW, ls=DASH, zorder=2)
    node(cv, bx, by, bw, bh, "white", PUR["stroke"], radius=R_FRAME, container=True, z=2.1)
    cv.rich(bx + 2.2, by + bh - 3.1, [("One head   ", INK), (r"$d_k=d_v=d_{\mathrm{model}}/h=64$", INK)],
            size=T_LABEL)

    S = np.array([[2.1, 0.4, 0.2], [0.3, 1.8, 0.9], [0.1, 0.7, 2.4]])     # illustrative scaled scores
    A = softmax(S)
    assert np.allclose(A.sum(axis=1), 1.0) and np.all(np.round(A, 2).sum(axis=1).round(2) == 1.0), A
    ch = 3.8
    yc = by + 11.3
    my = yc - 1.5 * ch

    def matmul(ox, lab):                   # second operand enters from above, the name sits under the operator
        cv.op(ox, yc, "x", d=D_OP, lw=LW)
        cv.text(ox, yc + 5.6, f"${lab}$", size=T_LABEL, color=INK)
        thin(cv, [(ox, yc + 4.2), (ox, yc + D_OP / 2)])
        cv.text(ox, yc - D_OP / 2 - 1.9, "MatMul", size=T_FINE, style="italic", color=MUTED)

    def headers(mx, c):                    # rows = queries, columns = keys
        for i in range(3):
            cv.text(mx - 0.9, my + (2.5 - i) * ch, f"$q_{i + 1}$", size=T_LABEL, color=MUTED, ha="right")
            cv.text(mx + (i + 0.5) * c, my + 3 * ch + 1.5, f"$k_{i + 1}$", size=T_LABEL, color=MUTED)

    x1 = bx + 2.6
    cv.text(x1, yc, "$Q$", size=T_LABEL, color=INK)
    ox = x1 + 5.2
    thin(cv, [(x1 + 1.5, yc), (ox - D_OP / 2, yc)])
    matmul(ox, "K")
    c1 = 4.2
    m1 = ox + 7.8
    thin(cv, [(ox + D_OP / 2, yc), (m1 - 4.0, yc)])
    cells(cv, m1, my, [[PV(v / 3.2) for v in row] for row in S], c1, ch, PUR["ink"],
          texts=[[f"{v:.1f}" for v in row] for row in S])
    headers(m1, c1)
    cv.text(m1 + 1.5 * c1 - 1.6, my - 2.4, r"scores $QK^{\top}\!/\sqrt{d_k}$", size=T_LABEL, color=INK)
    xm = m1 + 3 * c1 + 2.3
    thin(cv, [(m1 + 3 * c1, yc), (xm, yc)])
    node(cv, xm, yc - 2.1, 11.0, 4.2, "white", NEU["stroke"], radius=R_CHIP, dashed=True)
    cv.text(xm + 5.5, yc, "mask (opt.)", size=T_FINE, color=INK, z=6)
    thin(cv, [(xm + 11.0, yc), (xm + 13.2, yc)])
    node(cv, xm + 13.2, yc - 2.1, 9.6, 4.2, "white", NEU["stroke"], radius=R_CHIP)
    cv.text(xm + 18.0, yc, "softmax", size=T_FINE, color=INK, z=6)
    c2 = 4.8
    m2 = xm + 22.8 + 6.2
    thin(cv, [(xm + 22.8, yc), (m2 - 4.0, yc)])
    cells(cv, m2, my, [[PV(float(v)) for v in row] for row in A], c2, ch, PUR["ink"],
          texts=[[f"{v:.2f}" for v in row] for row in A], bold=[(0, 0), (1, 1), (2, 2)])
    headers(m2, c2)
    cv.text(m2 + 1.5 * c2 - 1.6, my - 2.4, "weights, rows sum to 1", size=T_LABEL, color=INK)
    o2 = m2 + 3 * c2 + 2.4 + D_OP / 2
    thin(cv, [(m2 + 3 * c2, yc), (o2 - D_OP / 2, yc)])
    matmul(o2, "V")
    assert o2 + D_OP / 2 + 2.4 <= bx + bw - 0.8, "one-head row leaves its box"
    thin(cv, [(o2 + D_OP / 2, yc), (bx + bw - 0.8, yc)])
    return yq0


# ------------------------------------------------------------------ (c) ---
def use(cv, x, ytop, k, title, rows, cols, rrole, crole, qkv, note, foot, A, cell, mask=None):
    """One use of attention: head, the three ports in the colour of their source, the weight map over the
    example's own tokens (rows = queries, columns = keys), and what the pattern means."""
    badge(cv, x + D_BADGE / 2, ytop - 1.5, k)
    for i, t in enumerate(title):
        cv.text(x + D_BADGE + 1.0, ytop - 3.0 * i, t, size=T_LABEL, color=INK, ha="left", weight="bold")
    yk = ytop - 3.0 - 2.4 - TOK_H
    chips(cv, x, yk, ["$Q$", "$K$", "$V$"], None, fills=qkv, w=TOK_H, gap=0.5, size=T_LABEL)
    cv.text(x, yk - 2.0, note, size=T_FINE, style="italic", color=INK, ha="left")
    mx, mtop = x + TOK_W + 0.5, yk - 4.6 - TOK_W - 0.4
    R, C = A.shape
    cells(cv, mx, mtop - R * cell, [[None if mask is not None and mask[i, j] else PV(float(A[i, j]))
                                     for j in range(C)] for i in range(R)], cell, cell, PUR["ink"])
    chips(cv, x, mtop - cell + (cell - TOK_H) / 2, rows, rrole, vertical=True, gap=cell - TOK_H)
    chips(cv, mx + (cell - TOK_H) / 2, mtop + 0.4, cols, crole, upright=True, gap=cell - TOK_H)
    cv.text(mx - 0.7, mtop + 5.6, r"$K\rightarrow$", size=T_LABEL, ha="right", color=INK)
    cv.text(mx - 0.7, mtop + 2.1, r"$Q\downarrow$", size=T_LABEL, ha="right", color=INK)
    fy = mtop - 5 * cell - 2.6
    for i, t in enumerate(foot):
        if t.startswith("#"):               # a masked-cell swatch before the text
            cv.ax.add_patch(Rectangle((x, fy - 2.9 * i - 1.2), 2.4, 2.4, fc="#ECEEF1", ec="none", zorder=6))
            hatch(cv, x, fy - 2.9 * i - 1.2, 2.4, 2.4)
            cv.text(x + 3.2, fy - 2.9 * i, t[1:], size=T_FINE, style="italic", color=INK, ha="left")
        else:
            cv.text(x, fy - 2.9 * i, t, size=T_FINE, style="italic", color=INK, ha="left")
    return fy - 2.9 * (len(foot) - 1)


def panel_c(cv, ytop):
    x = RX
    cv.rich(x, ytop, [("(c) ", INK, "bold"), ("Three uses of attention", INK)], size=T_HEAD, va="baseline")
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
    cell = 4.0
    ws = [TOK_W + 0.5 + c * cell for c in (n, m, n)]
    gut = (RW - sum(ws)) / 2
    assert gut >= 2.5, gut
    yt = ytop - 5.6
    xs = [x, x + ws[0] + gut, x + ws[0] + ws[1] + 2 * gut]
    use(cv, xs[0], yt, 1, ("Encoder", "self-attention"), SRC, SRC, "blue", "blue", ["blue"] * 3,
        "previous encoder layer", ("each position attends", "to all positions"), A1, cell)
    use(cv, xs[1], yt, 2, ("Masked decoder", "self-attention"), TGT_IN, TGT_IN, "coral", "coral", ["coral"] * 3,
        "previous decoder layer", ("position i attends to ≤ i", "#masked: −∞ before softmax"), A2, cell, mask)
    return use(cv, xs[2], yt, 3, ("Encoder–decoder", "attention"), TGT_IN, SRC, "coral", "blue",
               ["coral", "blue", "blue"], r"$K, V$: encoder output $\mathbf{z}$",
               ("every output position", "attends over all inputs"), A3, cell)


def render(out):
    cv = Canvas(W, H, family="serif", size=T_LABEL)
    panel_a(cv)
    key(cv, 3.3)
    ctop = 61.9
    panel_c(cv, ctop)
    panel_b(cv, ctop + 7.7)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/transformer")
    print("\n".join(render(ap.parse_args().out)))
