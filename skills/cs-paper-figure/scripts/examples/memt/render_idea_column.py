#!/usr/bin/env python3
"""MemT-1.0 in one column: the idea schematic (84 mm wide).

Source: MemT-1.0, arXiv:2610.26825v2, Section 2: the local memory M_t is read by every token of a turn
and rewritten once, at the turn end, from that turn's hidden states (M_{t+1}).

Register: idea schematic (references/registers.md §2). It complements the full-width plate in
render_fig4.py; it does not replace it.
  * Message: read at every token, written once per turn.
  * One drawing (a token row over a state grid) repeated for two turns; the only thing that changes is the
    state, whose rewritten row is the darker one in M_{t+1}.
  * Three hues, the paper's own from Fig. 4: green = the state, blue = read, purple = write. Tokens and
    labels are grey and black. Each hue is defined by a sample in the key row.
  * No frames, no tints: the page is the ground, and the gap between the turns is the separator.
  * Two stroke weights: 0.6 pt for shapes and the per-token reads, 0.9 pt for the state and the write.
    Three text sizes: 7.6 pt turn names, 7.0 pt symbols and the write node, 6.2 pt everything else.
The grid cells are an illustrative texture, not data.
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import Canvas, ROLE  # noqa: E402

STEM = "memt_idea_column"
G, B, P = (ROLE[k] for k in ("memory", "blue", "purple"))
IN = dict(fill="#F1F2F4", soft="#F1F2F4", stroke="#8C95A1", ink="#000000", mark="#8C95A1")    # input tokens
OUT = dict(fill="#BFC6D0", soft="#BFC6D0", stroke="#6B7480", ink="#000000", mark="#6B7480")   # generated tokens
N, TW, GAP = 8, 2.6, 0.7           # tokens per turn, token size and gap (mm)
ROWY, MY, MW, MH = 29.5, 10.0, 11.0, 8.8


def turn(cv, x0, name, values, label):
    """One turn: token row, state grid under its centre, a read arrow from the state to every token."""
    xs = cv.tokens(x0, ROWY, N, w=TW, h=TW, gap=GAP, fills=[IN] * 4 + [OUT] * 4, lw=0.6)
    cx = x0 + (N * TW + (N - 1) * GAP) / 2
    cv.text(cx, ROWY + TW + 5.2, name, size=7.6)
    cv.text((xs[0][0] + xs[3][0]) / 2, ROWY + TW + 1.7, "input", size=6.2, color="#5A626D")
    cv.text((xs[4][0] + xs[7][0]) / 2, ROWY + TW + 1.7, "response", size=6.2, color="#5A626D")
    cv.matrix(cx - MW / 2, MY, MW, MH, rows=4, cols=5, r="memory", values=values, lw=0.6)
    cv.text(cx, MY - 2.2, label, size=7.0)
    for k, (tx, _) in enumerate(xs):  # read at every token: one arrow per token, fanned from the state's top edge
        cv.arrow([(cx - MW / 2 + (k + 0.5) * MW / N, MY + MH), (tx, ROWY)], color=B["mark"], lw=0.6, head=1.0,
                 radius=0)
    return cx, xs


def build():
    cv = Canvas(84, 40.5, family="serif", size=7.0)
    rng = np.random.default_rng(3)
    m0 = rng.uniform(0.05, 0.55, (4, 5))
    m1 = m0.copy()
    m1[2] = [0.95, 0.7, 0.85, 0.6, 0.9]          # the one row this turn's write changed
    c0, x0s = turn(cv, 3.5, "turn $t$", m0, r"$\mathbf{M}_t$")
    c1, _ = turn(cv, 54.5, "turn $t{+}1$", m1, r"$\mathbf{M}_{t+1}$")
    wx, wy = (c0 + c1) / 2, MY + MH / 2            # the write, in the gap between the turns
    cv.box(wx - 5.0, wy - 2.3, 10.0, 4.6, "purple", "write", fill=P["soft"], stroke=P["soft"], size=7.0)  # flat, no outline
    cv.arrow([(c0 + MW / 2, wy), (wx - 5.0, wy)], color=G["mark"], lw=0.9, head=1.5)
    cv.arrow([(wx + 5.0, wy), (c1 - MW / 2, wy)], color=G["mark"], lw=0.9, head=1.5)
    end = x0s[-1][0] + TW / 2                      # right edge of the turn's last token
    cv.arrow([(end, ROWY + TW / 2), (wx, ROWY + TW / 2), (wx, wy + 2.3)], color=P["mark"], lw=0.9, head=1.5,
             radius=1.0)
    cv.text(wx + 1.2, ROWY - 4.2, "once, at\nturn end", size=6.2, style="italic", color=P["ink"], ha="left",
            linespacing=1.05)
    # key row: every hue beside a sample of itself
    ky = 2.2
    cv.arrow([(3.5, ky), (8.5, ky)], color=B["mark"], lw=0.6, head=1.0)
    cv.text(9.5, ky, "read, at every token", size=6.2, ha="left")
    cv.arrow([(33.0, ky), (38.0, ky)], color=P["mark"], lw=0.9, head=1.5)
    cv.text(39.0, ky, "write", size=6.2, ha="left")
    cv.arrow([(49.0, ky), (54.0, ky)], color=G["mark"], lw=0.9, head=1.5)
    cv.text(55.0, ky, "state $\\mathbf{M}$, carried forward", size=6.2, ha="left")
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/memt")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
