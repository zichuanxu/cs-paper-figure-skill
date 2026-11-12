#!/usr/bin/env python3
"""LoRA Fig. 1 redesigned in one column: train a low-rank bypass, then fold it into the weight (84 mm).

Source: Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", ICLR 2022, arXiv:2106.09685v2,
Figure 1 and Section 4.1. Every symbol is the paper's: W0 in R^{d x k} frozen, B in R^{d x r} and A in
R^{r x k} trainable with r << min(d, k); h = W0 x + B A x (Eq. 3); A Gaussian and B zero at initialisation;
when deployed W0 + BA is computed and stored, so inference has no additional latency.

Register: idea schematic (references/registers.md §2), as the source is.
  * Message: train only a thin low-rank pair beside the frozen weight, then merge it: one matrix again.
  * One drawing (x, a weight square, h) twice. The only thing that changes is the pair: a live orange
    bypass in training; at inference a ghost at 20 % strength, its orange now striped into the square.
  * Kept from the source: bottom-to-top reading, the trapezoid pair whose narrow side is the rank, blue =
    frozen and orange = trainable, the initial values beside A and B. The waist is drawn at r/d = 1/8, not
    the source's 0.4, so "r << d" is a shape and not only a letter.
  * Two hues: blue = the frozen pretrained weight, orange = the trainable low-rank pair; each keeps its hue
    in its shape, in the stripes and in its term of the equations. Vectors are grey; wires and text black.
  * Flat borderless shapes on the white page; no frames, no tints, no key.
  * One stroke weight, 0.8 pt: wires, the sum node and the merge stripes.
    Two arrow styles: black = data flow, light grey without a head = the path that no longer exists.
    Three text sizes: 8.0 pt heads and the names A and B, 7.2 pt math (scripts stay at 5 pt), 6.4 pt words.
The stripes are a schematic texture for "BA added in", not data; trapezoid area is not a parameter count.
"""
import argparse
import os
import sys

from matplotlib.patches import Rectangle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import Canvas, mix  # noqa: E402

STEM = "lora_fig1"
BLUE, BLUE_INK = "#9CC1EC", "#1F4E8C"        # frozen: the pretrained weight
ORANGE, ORANGE_INK = "#EE8233", "#B24A0A"    # trainable: the low-rank pair
GHOST, GHOST_WIRE = mix(ORANGE, "#FFFFFF", 0.80), "#D0D0D0"   # what is no longer there, at 20 % strength
VEC, K, NOTE = "#C3C8D0", "#000000", "#5A626D"
HEAD, MATH, WORD = 8.0, 7.2, 6.4            # the type scale (pt)
LW, AH = 0.8, 1.5                            # the one wire weight (pt) and its head (mm)

W = 84.0
S, GAP, R = 14.0, 4.0, 1.75                  # weight square = d = k (mm); gap to the pair; waist = r = d / 8
YB, BH = 1.6, 1.8                            # input bar: bottom and height
YJ = YB + BH + 2.7                           # where the bypass leaves the main path
Y0 = YJ + 2.9                                # bottom of the weight
Y1 = Y0 + S
YP = Y1 + 3.9                                # the sum node
YH = YP + 4.3                                # output bar
D = 3.0                                      # sum node diameter


def flat(color):
    """A role for a flat borderless shape with black text."""
    return dict(fill=color, soft=color, stroke=color, ink=K, mark=color)


def stripes(cv, x, y, w, h, color, skip, pitch=1.5, lw=LW, z=5.5):
    """Local helper (paperkit has no fill hatched in a second hue): 45 degree lines clipped to a rectangle.
    skip=(y0, y1) leaves a clear band for the label; the lines keep their phase across it."""
    for b0, b1 in ((y, skip[0]), (skip[1], y + h)):
        clip = Rectangle((x, b0), w, b1 - b0, transform=cv.ax.transData)
        k = -h + pitch / 2
        while k < w:
            (ln,) = cv.ax.plot([x + k, x + k + h], [y, y + h], color=color, lw=lw, zorder=z, solid_capstyle="butt")
            ln.set_clip_path(clip)
            k += pitch


def eq(cv, x, y, parts, size=MATH, gap=0.15, ha="left"):
    """Local helper: an equation whose terms take the hue of the thing they name. cv.rich sets its segments
    flush, which closes the space around an operator; the gap between terms is set here (mm)."""
    ws = [cv.text_width(s, size) for s, _ in parts]
    x -= (sum(ws) + gap * (len(parts) - 1)) / 2 if ha == "center" else 0
    for (s, c), w in zip(parts, ws):
        cv.text(x, y, s, size=size, color=c, ha="left")
        x += w + gap


def layer(cv, x0, merged):
    """One dense layer, bottom to top: x, the weight, h; the low-rank pair to its right, live or ghosted."""
    cx, px = x0 + S / 2, x0 + S + GAP          # centre of the main path; left edge of the pair
    pc, ym = px + S / 2, (Y0 + Y1) / 2
    th = (S - 0.7) / 2                         # height of one trapezoid; a 0.7 mm slit separates A from B
    pair = flat(GHOST if merged else ORANGE)
    cv.box(x0, YB, S, BH, flat(VEC), radius=0.5, lw=0)
    cv.box(x0, YH, S, BH, flat(VEC), radius=0.5, lw=0)
    cv.box(x0, Y0, S, S, flat(BLUE), radius=0, lw=0)
    cv.trap(px, Y0, S, th, pair, narrow="top", ratio=R / S, lw=0)
    cv.trap(px, Y1 - th, S, th, pair, narrow="bottom", ratio=R / S, lw=0)
    cv.text(x0 + S + 1.2, YB + BH / 2, "$x$", size=MATH, ha="left", color=K)
    cv.arrow([(cx, YB + BH), (cx, Y0)], color=K, lw=LW, head=AH)
    if merged:
        stripes(cv, x0, Y0, S, S, ORANGE, skip=(ym - 2.2, ym + 2.2))
        eq(cv, cx, ym, [("$W_0 +$", K), ("$BA$", ORANGE_INK)], ha="center")
        cv.arrow([(cx, Y1), (cx, YH)], color=K, lw=LW, head=AH)
        cv.text(x0 + S + 1.2, YH + BH / 2, "$h$", size=MATH, ha="left", color=K)
        cv.line([(cx + 0.9, YJ), (pc, YJ), (pc, Y0 - 0.5)], color=GHOST_WIRE, lw=LW, radius=1.0)
        cv.line([(pc, Y1 + 0.5), (pc, YP), (cx + 0.9, YP)], color=GHOST_WIRE, lw=LW, radius=1.0)
        return
    cv.text(cx, ym + 3.0, r"$W_0 \in \mathbb{R}^{d \times k}$", size=MATH, color=K)
    cv.text(cx, ym + 0.7, "pretrained,\nfrozen", size=WORD, color=K, va="top", linespacing=1.1)
    cv.text(pc, Y0 + 2.4, "$A$", size=HEAD, color=K)
    cv.text(pc, Y1 - 2.4, "$B$", size=HEAD, color=K)
    cv.dot(cx, YJ, color=K, d=1.0)
    cv.arrow([(cx, YJ), (pc, YJ), (pc, Y0)], color=K, lw=LW, head=AH, radius=1.0)
    cv.line([(cx, Y1), (cx, YP - D / 2)], color=K, lw=LW)
    cv.arrow([(pc, Y1), (pc, YP), (cx + D / 2, YP)], color=K, lw=LW, head=AH, radius=1.0)
    cv.op(cx, YP, "+", flat(K), d=D, lw=LW)
    cv.arrow([(cx, YP + D / 2), (cx, YH)], color=K, lw=LW, head=AH)
    eq(cv, x0 + S + 1.2, YH + BH / 2, [("$h =$", K), ("$W_0x$", BLUE_INK), ("$+$", K), ("$BAx$", ORANGE_INK)])
    lx = px + S + 1.0                          # the initial values, beside the pair
    cv.text(lx, Y1 - 2.4, "$B = 0$", size=MATH, ha="left", color=K)
    cv.text(lx, Y0 + 2.4, r"$A = \mathcal{N}(0, \sigma^2)$", size=MATH, ha="left", color=K)
    cv.text(pc + R / 2 + 1.2, ym, r"$r \ll \min(d, k)$", size=MATH, ha="left", color=K)   # at the waist it names


def build():
    cv = Canvas(W, YH + BH + 5.4, family="serif", size=MATH)
    xa, xb = 0.8, W - 0.8 - (2 * S + GAP)
    layer(cv, xa, merged=False)
    layer(cv, xb, merged=True)
    yt = YH + BH + 3.0
    for x, head, note in ((xa, "Training", "only $A$ and $B$ are trained, from $BA = 0$"), (xb, "Inference", "no added latency")):
        cv.text(x, yt, head, size=HEAD, ha="left", color=K)
        cv.text(x + cv.text_width(head, HEAD) + 1.6, yt - 0.15, note, size=WORD, ha="left", style="italic",
                color=NOTE)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/lora")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
