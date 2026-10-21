"""Redesign of Figure 1 of "Attention Is All You Need" (arXiv 1706.03762): the Transformer.

Facts used (Sec. 3 of the paper): encoder and decoder are stacks of N = 6 identical layers;
encoder layer = multi-head self-attention + position-wise feed-forward, each wrapped in a
residual connection and layer norm (Add & Norm); the decoder adds a third sub-layer that
attends over the encoder output, and its self-attention is masked so position i only sees
positions < i+1 (outputs are shifted right); embeddings are summed with sinusoidal
positional encodings; a linear layer + softmax gives next-token probabilities.
Base model: d_model = 512, h = 8, d_k = d_v = 64, d_ff = 2048.
The example tokens are illustrative.

    python render_fig1.py --out <dir>
"""
import argparse
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, ROLE, INK, MUTED, LINE  # noqa: E402

# one meaning per hue: the three attention kinds are the only saturated colours
ENC = dict(fill="#EBF2FC", soft="#D2E2F7", stroke="#5A8BCB", ink="#1C4C8C", mark="#2F6FC0")   # self-attention
DEC = dict(fill="#F3EFFB", soft="#E1D6F4", stroke="#8C6CC8", ink="#47297F", mark="#7048BF")   # masked self-attn
CRS = dict(fill="#E7F5F2", soft="#C3E5DD", stroke="#3D9C8B", ink="#0E5A4F", mark="#14897A")   # cross-attention
EMB = dict(fill="#FCEFF3", soft="#F6D7E1", stroke="#C98AA0", ink="#7A2E4A", mark="#C2507F")   # embeddings
NEU = dict(fill="#F3F4F6", soft="#E4E7EB", stroke="#8F98A4", ink="#353C47", mark="#6B7480")   # standard parts
NORM = dict(NEU, fill="#F7F7F2", stroke="#B9BDB0", ink="#4A4F45")
RES = "#9AA2AD"
N, H_HEADS, D_MODEL, D_K, D_FF = 6, 8, 512, 64, 2048
SRC = ["the", "cat", "sat", "."]
TGT_IN = ["<s>", "die", "Katze", "saß"]
TGT_OUT = TGT_IN[1:] + ["</s>"]          # outputs are the inputs shifted by one position
W, H = 178, 104


def card(cv, x, y, w, h, r, title):
    cv.group(x, y, w, h, r, title, band=True, size=7.6, radius=2.0, lw=0.7, fill="white")


def strip(cv, cx, y, words, r, w=7.6, h=3.8, gap=0.7):
    x0 = cx - (len(words) * (w + gap) - gap) / 2
    return cv.tokens(x0, y, len(words), w=w, h=h, gap=gap, r=r, labels=words, size=6.3)


def pe_glyph(cv, x, y, d=3.0):
    """Sinusoid in a circle = positional encoding."""
    from matplotlib.patches import Circle
    cv.ax.add_patch(Circle((x, y), d / 2, fc="white", ec=LINE, lw=0.6, zorder=9))
    t = np.linspace(-1, 1, 40)
    cv.ax.plot(x + t * d * 0.34, y + np.sin(t * math.pi) * d * 0.2, color=LINE, lw=0.6, zorder=10)


def norm_bar(cv, x, y, w):
    cv.box(x, y, w, 2.9, NORM, "Add & Norm", weight="normal", size=6.1, radius=1.0, lw=0.5)


def qkv_entry(cv, cx, y_split, y_box, labels=("Q", "K", "V"), dx=8.0):
    cv.line([(cx - dx, y_split), (cx + dx, y_split)])
    for k, x in enumerate((cx - dx, cx, cx + dx)):
        if labels[k]:
            cv.arrow([(x, y_split), (x, y_box)], head=1.0)
            cv.text(x + 0.9, (y_split + y_box) / 2 + 0.1, labels[k], size=5.8, color=MUTED, ha="left", style="italic")


def residual(cv, x_from, y_branch, x_side, y_target, x_target):
    cv.arrow([(x_from, y_branch), (x_side, y_branch), (x_side, y_target), (x_target, y_target)],
             color=RES, lw=0.5, head=0.9, radius=0.8)


def stack_back(cv, x, y, w, h, n=2, d=0.9):
    for i in range(n, 0, -1):
        cv.box(x + i * d, y + i * d, w, h, NEU, fill="#FAFAFB", lw=0.45, radius=1.8, z=1.2 - i * 0.01)


def multihead_inset(cv):
    """Inside every coloured attention block: h parallel scaled dot-product heads."""
    x0, y0 = 6.0, 75.0
    cv.box(x0, y0, 50, 21.5, NEU, fill="#FAFAFB", lw=0.5, radius=1.6, dashed=True, z=1.1)
    cv.text(x0 + 1.8, y0 + 19.2, "Inside each attention block", size=6.5, color=NEU["ink"], weight="bold", ha="left")
    ys = (y0 + 13.4, y0 + 9.0, y0 + 4.6)
    for y, lab in zip(ys, ("Q", "K", "V")):
        cv.text(x0 + 2.4, y, lab, size=6.4, color=INK, style="italic")
        cv.arrow([(x0 + 3.6, y), (x0 + 6.0, y)], head=0.9)
        cv.trap(x0 + 6.0, y - 1.5, 4.2, 3.0, NEU, narrow="right")
        cv.arrow([(x0 + 10.2, y), (x0 + 13.6, y)], head=0.9, lw=0.5)
    cv.text(x0 + 8.1, y0 + 1.4, "linear", size=5.9, color=MUTED)
    cv.stack(x0 + 13.6, y0 + 3.6, 15.4, 11.0, n=3, r=NEU, dx=0.9, dy=0.9, fill="white", lw=0.5, radius=1.2)
    cv.text(x0 + 21.3, y0 + 11.4, "scaled", size=6.2, color=INK)
    cv.text(x0 + 21.3, y0 + 9.1, "dot-product", size=6.2, color=INK)
    cv.text(x0 + 21.3, y0 + 6.8, "attention", size=6.2, color=INK)
    cv.text(x0 + 22.2, y0 + 1.4, r"$h=%d$ heads" % H_HEADS, size=5.9, color=MUTED)
    cv.arrow([(x0 + 31.0, y0 + 9.0), (x0 + 33.0, y0 + 9.0)], head=0.9)
    cv.box(x0 + 33.0, y0 + 6.2, 8.4, 5.6, NEU, "Concat", weight="normal", size=6.0, fill="white", lw=0.5)
    cv.arrow([(x0 + 41.4, y0 + 9.0), (x0 + 43.0, y0 + 9.0)], head=0.9)
    cv.trap(x0 + 43.0, y0 + 6.2, 4.2, 5.6, NEU, narrow="left")
    cv.text(x0 + 45.1, y0 + 4.4, r"$W^O$", size=6.0, color=MUTED)
    cv.arrow([(x0 + 47.2, y0 + 9.0), (x0 + 49.2, y0 + 9.0)], head=0.9)


def panel_a(cv):
    card(cv, 2, 2, 111, 100, NEU, "(a) Transformer: encoder and decoder")
    # ---------------- encoder ----------------
    ce, xe, we = 32.0, 16.0, 32.0
    strip(cv, ce, 6.0, SRC, NEU)
    cv.text(xe - 1.0, 7.9, "source", size=6.0, color=MUTED, ha="right", style="italic")
    cv.arrow([(ce, 9.8), (ce, 13.0)])
    cv.box(xe + 2, 13.0, we - 4, 5.4, EMB, "Input embedding", weight="normal", size=6.6)
    cv.arrow([(ce, 18.4), (ce, 20.6)])
    cv.op(ce, 22.0, "+", d=2.8)
    pe_glyph(cv, ce - 8.0, 22.0)
    cv.line([(ce - 6.5, 22.0), (ce - 1.4, 22.0)])
    cv.text(ce - 10.2, 22.0, "positional\nencoding", size=6.0, color=MUTED, ha="right", linespacing=0.95)
    cv.arrow([(ce, 23.4), (ce, 27.0)])
    stack_back(cv, 13, 27, 38, 34)
    cv.box(13, 27, 38, 34, NEU, fill="white", lw=0.7, radius=1.8, z=1.3)
    cv.chip(17.6, 61.0, f"N = {N}", NEU, size=6.0)
    cv.line([(ce, 27.0), (ce, 29.6)])
    qkv_entry(cv, ce, 29.6, 32.0)
    cv.box(xe, 32.0, we, 8.0, ENC, "Self-attention", r"multi-head, $h={}$".format(H_HEADS), size=6.7, lw=0.9,
           shadow=True, gap=1.6)
    residual(cv, ce - 8.0, 29.6, 14.4, 42.9, xe)
    norm_bar(cv, xe, 41.5, we)
    cv.arrow([(ce, 44.4), (ce, 47.2)])
    cv.box(xe, 47.2, we, 6.4, NEU, "Feed-forward", r"$d_{ff}=%d$" % D_FF, size=6.5, gap=1.35)
    residual(cv, ce, 45.6, 14.4, 56.9, xe)
    cv.dot(ce, 45.6, color=RES, d=0.7)
    norm_bar(cv, xe, 55.5, we)
    # encoder output -> K, V of cross-attention in every decoder layer
    cv.arrow([(ce, 58.4), (ce, 66.0), (58.6, 66.0), (58.6, 46.0), (70.5, 46.0), (70.5, 47.6)],
             color=CRS["mark"], lw=1.0, head=1.3)
    cv.text(45.0, 70.4, r"encoder output $\rightarrow$ keys, values", size=6.1, color=CRS["ink"])
    cv.text(45.0, 67.6, f"for all {N} decoder layers", size=6.0, color=CRS["ink"], style="italic")
    multihead_inset(cv)
    # ---------------- decoder ----------------
    cd, xd, wd = 84.0, 67.0, 34.0
    strip(cv, cd, 6.0, TGT_IN, NEU)
    cv.text(xd - 0.6, 7.9, "shifted\nright", size=6.0, color=MUTED, ha="right", style="italic", linespacing=0.95)
    cv.arrow([(cd, 9.8), (cd, 13.0)])
    cv.box(xd + 2, 13.0, wd - 4, 5.4, EMB, "Output embedding", weight="normal", size=6.6)
    cv.arrow([(cd, 18.4), (cd, 20.6)])
    cv.op(cd, 22.0, "+", d=2.8)
    pe_glyph(cv, cd + 8.0, 22.0)
    cv.line([(cd + 1.4, 22.0), (cd + 6.5, 22.0)])
    cv.text(cd + 10.2, 22.0, "positional\nencoding", size=6.0, color=MUTED, ha="left", linespacing=0.95)
    cv.arrow([(cd, 23.4), (cd, 27.0)])
    stack_back(cv, 64, 27, 40, 49.6)
    cv.box(64, 27, 40, 49.6, NEU, fill="white", lw=0.7, radius=1.8, z=1.3)
    cv.chip(68.6, 76.6, f"N = {N}", NEU, size=6.0)
    cv.line([(cd, 27.0), (cd, 29.6)])
    qkv_entry(cv, cd, 29.6, 32.0)
    cv.box(xd, 32.0, wd, 8.0, DEC, "Masked self-attention", "multi-head, causal", size=6.7, lw=0.9,
           shadow=True, gap=1.6)
    residual(cv, cd + 8.0, 29.6, 102.6, 42.9, xd + wd)
    norm_bar(cv, xd, 41.5, wd)
    cv.arrow([(cd, 44.4), (cd, 47.6)])
    cv.text(cd + 0.9, 46.1, "Q", size=5.8, color=MUTED, ha="left", style="italic")
    cv.text(72.0, 46.9, "K, V", size=5.8, color=CRS["ink"], ha="left", style="italic")
    cv.box(xd, 47.6, wd, 8.0, CRS, "Cross-attention", "multi-head", size=6.7, lw=0.9, shadow=True, gap=1.6)
    residual(cv, cd, 45.6, 102.6, 58.4, xd + wd)
    cv.dot(cd, 45.6, color=RES, d=0.7)
    norm_bar(cv, xd, 57.0, wd)
    cv.arrow([(cd, 59.9), (cd, 62.6)])
    cv.box(xd, 62.6, wd, 6.4, NEU, "Feed-forward", r"$d_{ff}=%d$" % D_FF, size=6.5, gap=1.35)
    residual(cv, cd, 61.2, 102.6, 72.4, xd + wd)
    cv.dot(cd, 61.2, color=RES, d=0.7)
    norm_bar(cv, xd, 71.0, wd)
    cv.arrow([(cd, 73.9), (cd, 80.0)])
    cv.box(xd + 2, 80.0, wd - 4, 5.4, NEU, "Linear + softmax", weight="normal", size=6.6)
    cv.arrow([(cd, 85.4), (cd, 88.6)])
    strip(cv, cd, 88.6, TGT_OUT, DEC)
    cv.text(cd, 94.9, "next-token probabilities", size=6.0, color=MUTED, style="italic")


def mask_row(cv, x, ytop, kind, c, title, l1, l2):
    n, cell = 4, 2.7
    allowed = np.ones((n, n)) if kind != "causal" else np.tril(np.ones((n, n)))
    from matplotlib.patches import Rectangle
    for i in range(n):
        for j in range(n):
            ok = allowed[i, j] > 0
            cv.ax.add_patch(Rectangle((x + j * cell, ytop - (i + 1) * cell), cell, cell,
                                      fc=c["soft"] if ok else "white", ec=c["stroke"] if ok else "#B3BAC4",
                                      lw=0.4, zorder=6, hatch=None if ok else "//////"))
    cv.ax.add_patch(Rectangle((x, ytop - n * cell), n * cell, n * cell, fc="none", ec=c["ink"], lw=0.6, zorder=7))
    tx = x + n * cell + 3.0
    cv.text(tx, ytop - 1.4, title, size=6.9, color=c["ink"], weight="bold", ha="left")
    cv.text(tx, ytop - 5.0, l1, size=6.2, color=INK, ha="left")
    cv.text(tx, ytop - 8.2, l2, size=6.2, color=INK, ha="left")
    return allowed


def panel_b(cv):
    card(cv, 116, 38, 60, 64, NEU, "(b) Who attends to whom")
    x = 119.5
    cv.text(x + 5.4, 94.2, r"keys $\rightarrow$", size=5.8, color=MUTED)
    from matplotlib.patches import Rectangle
    cv.ax.add_patch(Rectangle((150.0, 93.2), 2.2, 2.2, fc="white", ec="#B3BAC4", lw=0.4, hatch="//////", zorder=6))
    cv.text(153.0, 94.2, r"masked: score $=-\infty$", size=5.9, color=MUTED, ha="left")
    cv.text(x - 1.3, 88.0, r"queries $\downarrow$", size=5.8, color=MUTED, rotation=90)
    a = mask_row(cv, x, 92.4, "full", ENC, "Encoder self-attention", "every source token sees", "all source tokens")
    b = mask_row(cv, x, 73.6, "causal", DEC, "Masked self-attention", r"target token $i$ sees only", r"tokens $\leq i$")
    c = mask_row(cv, x, 54.8, "full", CRS, "Cross-attention", "target queries read the", "encoder's keys and values")
    assert a.sum() == 16 and b.sum() == 10 and c.sum() == 16 and np.all(np.triu(b, 1) == 0)


def panel_c(cv):
    card(cv, 116, 2, 60, 33, NEU, "(c) Attention, per head")
    cv.text(146.0, 24.2, r"$\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V$",
            size=7.2, color=INK)
    cv.text(146.0, 15.8, r"$\mathrm{MultiHead}(Q,K,V)=\mathrm{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)\,W^{O}$",
            size=6.6, color=INK)
    x = 119.0
    for s in (f"N = {N}", f"h = {H_HEADS}", r"$d_{model}$ = %d" % D_MODEL):
        x0, w = cv.chip(x, 8.6, s, NEU, size=6.1, ha="left")
        x = x0 + w + 1.2
    x = 119.0
    for s in (r"$d_k = d_v$ = %d" % D_K, r"$d_{ff}$ = %d" % D_FF):
        x0, w = cv.chip(x, 4.6, s, NEU, size=6.1, ha="left")
        x = x0 + w + 1.2
    cv.text(174.0, 4.6, "base model", size=6.0, color=MUTED, ha="right", style="italic")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    assert D_K == D_MODEL // H_HEADS and TGT_OUT[:-1] == TGT_IN[1:]
    cv = Canvas(W, H, family="serif", size=7.0)
    panel_a(cv)
    panel_b(cv)
    panel_c(cv)
    print("\n".join(cv.save(os.path.join(a.out, "transformer_fig1"))))


if __name__ == "__main__":
    main()
