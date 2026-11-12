#!/usr/bin/env python3
"""ReAct Fig. 1, part 1 (HotpotQA): four prompting methods on one question, full width (140 x 88 mm).

Source: Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", ICLR 2023,
arXiv:2210.03629v3 (CC BY 4.0), Figure 1 (1a)-(1d). Every word of the question, thoughts, actions,
observations and answers is transcribed from that figure, and every ellipsis is the paper's own; nothing is
elided here. Two things are normalised: the stray spaces around its highlighted runs, and the colon after
each role label, which moves to a gutter. Part 2 of the original (ALFWorld, Act-only versus ReAct) is left
out: at 6.7 pt this part alone needs 88 mm of height, and the same grammar would draw part 2 as a second
figure.

Register: example-led text (references/registers.md §3). The example text is the object.
  * Message: only the method that reasons and acts answers the question. Reasoning alone invents its
    facts; acting alone retrieves the right page and cannot use it.
  * Hero by difference: ReAct is the only trace in which a blue-railed thought precedes every action, the
    only one that ends in a tick, and the largest block (54 % of the width, full height).
  * Skeleton: the question once, across the top; the three baselines stacked in the left column, ReAct in
    the right; both traces end on one line, so the two final actions sit side by side. Role labels stand in
    a gutter, so thought / act / obs can be scanned without reading. Rejected: a method x step grid with
    Act-only and ReAct on shared rows, which narrows ReAct to 40 characters a line and needs about 100 mm.
  * Three hues: blue = reasoning (the rail, the label "Thought", the word "reason" in two heads);
    green band = retrieved and carried forward, and the tick; red band = hallucinated or wrong, and the
    cross. The bands are exactly the spans the original marks. A key sits right of the question.
  * Three voices: what the model wrote is monospace; what the environment returned is the body face in
    grey; the question, heads and role labels are the body face in black.
  * Two sizes: 8.0 pt (question, heads) and 6.7 pt (example text, role labels, key).
  * Strokes: 0.5 pt hairlines under the heads, 1.0 pt verdict glyphs. No frames and no arrows: reading
    order carries the flow.

Run from skills/cs-paper-figure: python scripts/examples/react/render_fig1.py --out figures/react
"""
import argparse
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import Canvas, PT_PER_MM, ROLE  # noqa: E402

STEM = "react_fig1"
W, H = 140.0, 88.0
FS, HS = 6.7, 8.0                       # example text and labels; question and heads (pt)
LH = 1.2 * FS / PT_PER_MM               # line pitch of the example text (mm) = the height of a span band
QLH = 1.25 * HS / PT_PER_MM
BLUE, OK, BAD = ROLE["blue"], "memory", "coral"
BLACK, GREY, RULE = "#000000", "#4D5560", "#AEB5BF"
M, GUT, GAP = 1.0, 5.0, 3.0             # outer margin; gutter between the columns; least gap between panels
LW = 58.0                               # left column width; the right column takes the rest
RX = M + LW + GUT
RW = W - M - RX
RAIL, STEP = 0.8, 0.55 * LH             # rail width; extra space between steps

QUESTION = ("Aside from the Apple Remote, what other device can control the program Apple Remote was "
            "originally designed to interact with?")
STANDARD = [("Answer", [("iPod", None)], "bad")]
COT = [
    ("Thought", [("Let's think step by step. ", None),
                 ("Apple Remote was originally designed to interact with Apple TV. Apple TV can be "
                  "controlled by iPhone, iPad, and iPod Touch.", BAD),
                 (" So the answer is iPhone, iPad, and iPod Touch.", None)], None),
    ("Answer", [("iPhone, iPad, iPod Touch", None)], "bad"),
]
ACT_ONLY = [
    ("Act 1", [("Search[Apple Remote]", None)], None),
    ("Obs 1", [("The Apple Remote is a remote control …", None)], None),
    ("Act 2", [("Search[Front Row]", None)], None),
    ("Obs 2", [("Could not find [Front Row]. Similar: …", None)], None),
    ("Act 3", [("Search[", None), ("Front Row (software)", OK), ("]", None)], None),
    ("Obs 3", [("Front Row is a discontinued media center software …", None)], None),
    ("Act 4", [("Finish[", None), ("yes", BAD), ("]", None)], "bad"),
]
REACT = [
    ("Thought 1", [("I need to search Apple Remote and find the program it was originally designed to "
                    "interact with.", None)], None),
    ("Act 1", [("Search[Apple Remote]", None)], None),
    ("Obs 1", [("The Apple Remote is a remote control introduced in October 2005 by Apple … originally "
                "designed to control the ", None), ("Front Row media center", OK), (" program …", None)], None),
    ("Thought 2", [("Apple Remote was originally designed to control the Front Row media center program. "
                    "I need to search ", None), ("Front Row", OK),
                   (" next and find what other device can control it.", None)], None),
    ("Act 2", [("Search[Front Row]", None)], None),
    ("Obs 2", [("Could not find [Front Row]. Similar: ['Front Row Seat to Earth', 'Front Row "
                "Motorsports', '", None), ("Front Row (software)", OK), ("', …]", None)], None),
    ("Thought 3", [("Front Row is not found. I need to search ", None), ("Front Row (software)", OK),
                   (".", None)], None),
    ("Act 3", [("Search[", None), ("Front Row (software)", OK), ("]", None)], None),
    ("Obs 3", [("Front Row is a discontinued media center software …", None)], None),
    ("Thought 4", [("Front Row (software) is controlled by an Apple Remote or the keyboard function keys.",
                    OK), (" So the answer is keyboard function keys.", None)], None),
    ("Act 4", [("Finish[", None), ("keyboard function keys", OK), ("]", None)], "ok"),
]


def trace(cv, x, y, w, gut, items):
    """One trajectory from the top-left (x, y): role labels in a gutter of width `gut`, the text wrapped to
    the rest of the column, a blue rail beside each thought, the verdict after the judged span. What the
    model wrote is monospace; what the environment returned is the body face in grey. Returns the bottom y."""
    for k, (label, segs, verdict) in enumerate(items):
        role = label.split()[0]
        if k and role != "Obs" and not (role == "Act" and items[k - 1][0].startswith("Thought")):
            y -= STEP                                    # a new step starts
        ink, kw = (GREY, {}) if role == "Obs" else (BLACK, {"family": "monospace"})
        bottom, end = cv.para(x + gut, y, w - gut, [(t, ink, "normal", m) for t, m in segs], size=FS, **kw)
        lines = range(round((y - bottom) / LH))
        cv.text(x + RAIL + 1.2, y - LH / 2 - (0.0 if role == "Obs" else 0.1), label, size=FS, ha="left",
                weight="normal" if role == "Obs" else "bold",
                color=GREY if role == "Obs" else BLUE["ink"] if role == "Thought" else BLACK)
        if role == "Thought":
            cv.ax.add_patch(Rectangle((x, y - len(lines) * LH + 0.25), RAIL, len(lines) * LH - 0.5,
                                      fc=BLUE["mark"], ec="none", zorder=6))
        if verdict:
            icon = cv.icon_check if verdict == "ok" else cv.icon_cross
            icon(end + 2.9, y - (len(lines) - 0.5) * LH, 3.0, color=ROLE[OK if verdict == "ok" else BAD]["mark"],
                 lw=1.0)
        y -= len(lines) * LH
    return y


def head(cv, x, y, w, letter, name, note=None, ours=False):
    """Panel head on the page, a hairline under it. Returns the y where the content starts."""
    segs = [(f"({letter}) ", GREY), (name, BLACK, "bold" if ours else "normal")]
    if note:                                            # ("reason", " only"): the word reason takes the blue
        segs += [(" (", BLACK)] + [(t, BLUE["ink"] if t == "reason" else BLACK) for t in note] + [(")", BLACK)]
    cv.rich(x, y - QLH / 2, segs, size=HS)
    cv.line([(x, y - QLH - 0.5), (x + w, y - QLH - 0.5)], color=RULE, lw=0.5)
    return y - QLH - 0.5 - 1.3


def lay(cv, gap):
    """Draw everything above the key; `gap` separates the panels of the left stack. Returns both bottoms."""
    y = H - M                                           # the question, once, across the top
    cv.text(M, y - QLH / 2, "Question", size=HS, weight="bold", ha="left", color=BLACK)
    qx = M + cv.text_width("Question", HS, "bold") + 2.4
    lines = [""]
    for wd in QUESTION.split():
        trial = (lines[-1] + " " + wd).strip()
        if cv.text_width(trial, HS) > W - M - qx:
            lines.append(wd)
        else:
            lines[-1] = trial
    assert len(lines) == 2
    for i, ln in enumerate(lines):
        cv.text(qx, y - (i + 0.5) * QLH, ln, size=HS, ha="left", color=BLACK)
    # key, right of the question's short last line: every mark beside a sample of itself
    ky, x = y - 1.5 * QLH, W - M
    for words, mark in (("hallucinated or wrong", BAD), ("retrieved and carried forward", OK)):
        x -= cv.text_width(words, FS)
        cv.rich(x, ky, [(words, BLACK, "normal", mark)], size=FS)
        x -= 5.0
    x -= cv.text_width("reasoning", FS)
    cv.text(x, ky, "reasoning", size=FS, ha="left", color=BLACK)
    cv.ax.add_patch(Rectangle((x - 1.2 - RAIL, ky - LH / 2 + 0.25), RAIL, LH - 0.5, fc=BLUE["mark"], ec="none",
                              zorder=6))
    assert x - 1.2 - RAIL - (qx + cv.text_width(lines[1], HS)) > 20   # the key stands clear of the question
    top = y - 2 * QLH - 3.7
    gl = RAIL + 1.2 + cv.text_width("Thought", FS, "bold") + 1.6      # left stack: the three baselines
    y = head(cv, M, top, LW, "a", "Standard")
    y = trace(cv, M, y, LW, gl, STANDARD)
    y = head(cv, M, y - gap, LW, "b", "CoT", ("reason", " only"))
    y = trace(cv, M, y, LW, gl, COT)
    y = head(cv, M, y - gap, LW, "c", "Act-only")
    yl = trace(cv, M, y, LW, gl, ACT_ONLY)
    gr = RAIL + 1.2 + cv.text_width("Thought 1", FS, "bold") + 1.6    # right column: ReAct
    y = head(cv, RX, top, RW, "d", "ReAct", ("reason", " + act"), ours=True)
    return yl, trace(cv, RX, y, RW, gr, REACT)


def build():
    probe = Canvas(W, H, family="serif", size=FS)
    yl, yr = lay(probe, GAP)
    plt.close(probe.fig)
    assert abs(yl - yr) <= 3.0, (yl, yr)                # the two columns come out within a line of each other
    cv = Canvas(W, H, family="serif", size=FS)
    yl, yr = lay(cv, GAP + (yl - yr) / 2)               # both traces end on one line: the two final actions
    print(f"bottoms: left {yl:.2f} mm, right {yr:.2f} mm (margin {M})")
    assert abs(yl - yr) < 0.01 and abs(yr - M) < 0.05, (yl, yr)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/react")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
