"""Harness² Fig. 3: the pipeline as two nested recursions around one persistent library.

Source: Xu et al., "Harness²: Recursive Agent Harnessing for an Open World", arXiv:2610.14224, Fig. 3,
with Sec. 2.2.1 (Propose / Probe / Compose), Sec. 2.3 and Eq. 4 (Reflect, Update), Appendix D.2 (library
entries) and Prompt 6 (reflector verdicts).

Kept from the source: the four sessions (agent executor, harness editor, harness composer, experience
reflector); initial harness H0, reference execution e0, invariant and domain candidates and their probes,
the successor H' and its execution e'; the improvement record D_t; the improvement harness R_t with its
library of adopted harnesses and EXPERIENCE.md files; the two levels and the notation of Eqs. 1 and 4.

Design:
* Nesting states the claim: the task-level frame (one task, R_t fixed) sits inside the harnessing-level
  frame (across tasks). The improvement harness is a shelf above the task: sessions read it downwards
  (dashed), the record of the task is written back along the bottom and up the right (solid). The loop
  the source labels "move to the next task" is that circuit.
* A harness is drawn as the rack of its eight files C1-C8 (the components of Fig. 2, render_fig2.py):
  grey = inherited from H0, teal = edited by the invariant candidate, coral = edited by the domain
  candidate. The successor rack carries both colours, so "compose merges supported edits" is visible
  on the object. The edited files follow the paper's JobBench case study (Fig. 9): invariant edits to
  guardrails C2 and scripts C7, domain edits to skills C6 and tool guidance C4, all four retained.
* Each probe ends in a contrast with the same reference record e0, drawn once between the two lanes.
* Library entries of earlier tasks carry illustrative edit patterns; only the task-t entry follows the case.
* Purple marks everything that belongs to the improver, slate everything that executes; the two
  candidates keep their hue from the editor to the composer. Palette and objects live in h2_style.py.
* The source draws no edge from the improvement harness into the task; Sec. 2.3 says it guides Propose
  and Compose, so the two read arrows are added from the text.

    python render_fig3.py --out DIR [--vector-icons]
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import h2_style as S  # noqa: E402
from h2_style import DOM, IMPROVER, INK, INV, MODEL, MONO, MUTED, ROLE  # noqa: E402
from paperkit import Canvas  # noqa: E402

STEM = "harness2_fig3_pipeline"
W, H = 178, 102
EDITS = {INV: {2: INV, 7: INV}, DOM: {4: DOM, 6: DOM}}  # paper Fig. 9: which files each candidate edited
MERGED = {**EDITS[INV], **EDITS[DOM]}


def agent(cv, name, x, y, s, r, label=None, side="below", tint=False):
    """A session = the robot of the icon family in its role colour, with its role name."""
    S.icon(cv, name, x, y, s, r, tint=tint, fit="height")
    if label and side == "below":
        cv.text(x, y - s / 2 - 0.6, label, size=6.6, weight="bold", color=ROLE[r]["ink"], va="top", linespacing=1.08)
    elif label:
        cv.text(x + s / 2 + 1.4, y, label, size=6.6, weight="bold", color=ROLE[r]["ink"], ha="left", linespacing=1.15)


def entry(cv, x, y, edits=None, new=False):
    """Library entry: an adopted harness (rack) with its EXPERIENCE.md (page). (x, y) = bottom-left."""
    w, h = 16.4, 7.6
    c = ROLE[IMPROVER]
    cv.box(x, y, w, h, IMPROVER, fill="white", stroke=c["mark"] if new else c["stroke"], lw=0.9 if new else 0.5,
           radius=1.0, dashed=new, z=5, container=True)
    S.rack(cv, x + 1.2, y + 1.55, edits, cell=(2.0, 1.95), labels=False, z=6)
    cv.doc(x + w - 5.0, y + 1.2, 3.8, 5.2, IMPROVER, lines=3, z=6, lw=0.5)
    return (x, y, w, h)


def draw(out, vector=False):
    S.VECTOR = vector
    cv = Canvas(W, H)
    pur, slate = ROLE[IMPROVER], ROLE[MODEL]
    B = 9.6  # bottom of the outer frame; the key strip sits below it

    # ---- frames: task-level recursion inside harnessing-level recursion ---------------------------------------
    cv.section(1.2, B, 175.6, 88.4, IMPROVER, r"Harnessing-level recursion: $\mathcal{R}_t \rightarrow \mathcal{R}_{t+1}$ after each task",
               size=8.2, lw=0.9)
    ix, iy, iw, ih = 4.5, B + 17.5, 131.5, 47.5
    cv.section(ix, iy, iw, ih, MODEL, r"Task-level recursion: task $q_t$ starts from $\mathcal{H}_0$", size=8.2,
               fill="white", lw=0.9)

    # ---- the shelf: improvement harness R_t --------------------------------------------------------------------
    sx, sy, sw, sh = 4.5, iy + ih + 5.5, 169.0, 14.5
    cv.box(sx, sy, sw, sh, IMPROVER, fill="white", stroke=pur["mark"], lw=0.9, radius=1.8, z=3, shadow=True)
    cv.text(sx + 2.4, sy + sh - 3.3, r"Improvement harness $\mathcal{R}_t$", size=7.8, weight="bold", color=pur["ink"], ha="left")
    cv.icon_lock(sx + 3.8, sy + 7.3, 2.5, color=pur["stroke"])
    cv.text(sx + 6.2, sy + 7.2, "stage instructions, decision rule:", size=6.2, ha="left")
    cv.text(sx + 6.2 + cv.text_width("stage instructions, decision rule: ", 6.2), sy + 7.2, "fixed", size=6.2, ha="left",
            style="italic", color=pur["ink"])
    cv.icon_cycle(sx + 3.8, sy + 3.5, 2.7, color=pur["mark"])
    cv.text(sx + 6.2, sy + 3.4, "harness improvement library:", size=6.2, ha="left")
    cv.text(sx + 6.2 + cv.text_width("harness improvement library: ", 6.2), sy + 3.4, "evolves", size=6.2, ha="left",
            style="italic", color=pur["ink"])
    # library: an index, then one entry per finished task
    ey = sy + 1.6
    cv.doc(sx + 51.0, ey + 0.6, 5.0, 6.4, IMPROVER, lines=4, z=6, lw=0.5)
    cv.text(sx + 53.5, sy + sh - 2.6, "index", size=6.0, color=pur["ink"])
    past = [(sx + 63.0, "task 1", {2: INV}), (sx + 84.0, "task 2", {6: DOM, 3: INV}), (sx + 113.0, r"task $t-1$", {7: INV, 4: DOM})]
    for x, lab, ed in past:
        e = entry(cv, x, ey, ed)
        cv.text(x + e[2] / 2, sy + sh - 2.6, lab, size=6.0, color=pur["ink"])
    cv.text(sx + 106.7, ey + 3.8, r"$\cdots$", size=8, color=pur["ink"])
    rcx = 156.5  # axis of the reflect column: record up, update up
    entry(cv, rcx - 8.2, ey, MERGED, new=True)
    cv.text(rcx, sy + sh - 2.6, r"task $t$: $\mathcal{H}_t^\star$ + lessons", size=6.5, color=pur["ink"])

    # ---- task level -------------------------------------------------------------------------------------------------
    cv.phase_bar(iy + 1.2, [(ix + 1.5, 64.5, MODEL, "Propose"), (64.5, 99.5, MODEL, "Probe"), (99.5, ix + iw - 1.5, MODEL, "Compose")],
                 h=3.4, size=7.0)
    dom_y, lane_h, gap = iy + 6.6, 14.0, 8.4
    inv_y = dom_y + lane_h + gap
    midy = dom_y + lane_h + gap / 2
    lx0, lx1 = 44.0, 99.0

    # executor: the initial harness runs the task once, giving the reference record
    c1 = 17.3
    cv.text(c1, inv_y + lane_h - 1.4, "Agent executor", size=6.6, weight="bold", color=slate["ink"])
    r0 = S.rack(cv, c1 - 7.5, inv_y + 2.6, name="H0")
    cv.text(r0[0] - 0.9, r0[1] + r0[3] / 2, r"$\mathcal{H}_0$", size=7.2, ha="right")
    agent(cv, "executor", c1, midy - 0.6, 9.0, MODEL, tint=True)
    e0 = S.record(cv, c1 - 2.6, dom_y + 1.2, MODEL)
    cv.text(e0[0] - 0.9, e0[1] + e0[3] / 2, r"$e_0$", size=7.2, ha="right")
    cv.arrow([(c1, r0[1]), (c1, midy + 4.2)], lw=0.8)
    cv.arrow([(c1, midy - 5.4), (c1, e0[1] + e0[3])], lw=0.8)
    tip = cv.brace(26.2, e0[1], inv_y + lane_h - 0.2, side="right", color=slate["ink"], lw=0.7)

    # editor: reads harness + reference (and the library), proposes one candidate per scope
    ed_x = 35.6
    agent(cv, "editor", ed_x, midy, 9.6, IMPROVER, "Harness\neditor", tint=True)
    cv.arrow([tip, (ed_x - 5.0, midy)], lw=0.8)
    S.darrow(cv, [(ed_x, sy), (ed_x, midy + 5.2)], color=pur["mark"], lw=0.9)
    cv.text(ed_x - 1.4, sy - 2.4, "components, lessons", size=6.0, style="italic", color=pur["ink"], ha="right")

    yc = {}
    for r, y, title, what in ((INV, inv_y, "Invariant", "agentic deficiencies"), (DOM, dom_y, "Domain", "domain knowledge, procedures")):
        c = ROLE[r]
        cv.box(lx0, y, lx1 - lx0, lane_h, r, lw=0.7, radius=1.6, z=2, container=True)
        cv.text(lx0 + 2.0, y + lane_h - 2.4, title, size=6.8, weight="bold", color=c["ink"], ha="left")
        cv.text(lx0 + 2.0 + cv.text_width(title + " ", 6.8, "bold"), y + lane_h - 2.4, what, size=6.0, style="italic",
                color=c["ink"], ha="left")
        cy = yc[r] = y + 5.0
        rk = S.rack(cv, 46.2, cy - 3.79, EDITS[r], name=title)
        agent(cv, "executor", 71.8, cy, 8.2, MODEL, tint=True)
        rec = S.record(cv, 82.6, cy - 3.3, r)
        cv.op(95.6, cy, r"$\Delta$", r=r, d=3.6)
        cv.arrow([(42.0, midy), (42.0, cy), (rk[0], cy)], color=c["mark"], lw=0.9)
        cv.arrow([(rk[0] + rk[2], cy), (66.6, cy)], lw=0.8)
        cv.arrow([(77.0, cy), (rec[0], cy)], lw=0.8)
        cv.arrow([(rec[0] + rec[2], cy), (95.6 - 1.8, cy)], color=c["mark"], lw=0.8)
    cv.line([(ed_x + 5.2, midy), (42.0, midy)], color=S.LINE, lw=0.9)
    cv.dot(42.0, midy, color=S.LINE, d=1.0)

    # the same reference record is contrasted with both probes
    g0 = S.record(cv, 95.6 - 2.6, midy - 3.3, MODEL, ghost=True)
    cv.text(g0[0] - 0.9, midy, r"$e_0$", size=7.2, ha="right")
    cv.arrow([(95.6, g0[1] + g0[3]), (95.6, yc[INV] - 1.8)], color=slate["mark"], lw=0.7, head=1.1)
    cv.arrow([(95.6, g0[1]), (95.6, yc[DOM] + 1.8)], color=slate["mark"], lw=0.7, head=1.1)
    cv.icon_snow(lx0 + 3.2, midy, 2.5, color=slate["mark"])
    cv.text(lx0 + 5.6, midy, r"same task $q_t$, model $\mathcal{M}$, environment", size=6.5, style="italic", color=slate["ink"],
            ha="left")

    # composer: reads both contrasts (and the library), writes the successor, which is executed
    co_x, co_y = 109.0, yc[INV] + 1.5
    agent(cv, "editor", co_x, co_y, 9.6, IMPROVER, "Harness\ncomposer", tint=True)
    cv.arrow([(95.6 + 1.8, yc[INV]), (co_x - 4.6, yc[INV])], color=ROLE[INV]["mark"], lw=0.9)
    cv.arrow([(95.6 + 1.8, yc[DOM]), (101.6, yc[DOM]), (101.6, co_y - 4.2), (co_x - 4.6, co_y - 4.2)], color=ROLE[DOM]["mark"], lw=0.9)
    S.darrow(cv, [(co_x, sy), (co_x, co_y + 5.2)], color=pur["mark"], lw=0.9)
    cv.text(co_x + 1.4, sy - 2.4, "lessons", size=6.0, style="italic", color=pur["ink"], ha="left")
    hp = S.rack(cv, 118.2, co_y - 3.79, MERGED, name="H'")
    cv.arrow([(co_x + 5.2, co_y), (hp[0], co_y)], color=pur["mark"], lw=0.9)
    cv.text(hp[0] + hp[2] / 2, hp[1] + hp[3] + 1.9, r"successor $\mathcal{H}'$", size=6.6, color=INK)
    hx = hp[0] + hp[2] / 2
    agent(cv, "executor", hx, midy - 1.4, 8.2, MODEL, tint=True)
    e1 = S.record(cv, hx - 2.6, dom_y + 1.2, MODEL)
    cv.text(e1[0] + e1[2] + 0.9, e1[1] + e1[3] / 2, r"$e'$", size=7.2, ha="left")
    cv.arrow([(hx, hp[1]), (hx, midy + 3.0)], lw=0.8)
    cv.arrow([(hx, midy - 5.8), (hx, e1[1] + e1[3])], lw=0.8)
    cv.flow_chips(["merge", "revise", "adopt one", "keep"], 103.4, 119.6, co_y - 12.8, IMPROVER, size=5.8, h=3.1, pad=0.8,
                  gap=0.8, row_gap=0.7, align="left")

    # ---- harnessing level: record -> reflect -> update ----------------------------------------------------------
    dy, dh = B + 3.0, 9.5
    cv.box(ix, dy, iw, dh, IMPROVER, fill="white", stroke=pur["stroke"], lw=0.7, radius=1.6, z=3)
    cv.text(ix + 2.4, dy + dh / 2, r"Improvement record $\mathcal{D}_t$", size=7.2, weight="bold", color=pur["ink"], ha="left")
    cv.flow_chips(["reference executions", "candidate harnesses + probes", "composition decisions", "selected result"],
                  ix + 34.0, ix + iw - 1.5, dy + dh / 2 + 1.7, IMPROVER, size=5.9, h=3.4, gap=4.0, align="center")
    for x in (c1, 71.8, hx):
        cv.arrow([(x, iy), (x, dy + dh)], color=pur["mark"], lw=0.8, head=1.2)

    kx, kw = 139.5, 34.0
    cv.box(kx, iy, kw, ih, IMPROVER, fill="white", stroke=pur["stroke"], lw=0.7, radius=1.8, z=3)
    # read upwards, with the flow: reflector -> verdict per edit -> lesson -> EXPERIENCE.md -> Update
    agent(cv, "reflector", kx + 7.0, iy + 7.6, 10.4, IMPROVER, "Experience\nreflector", side="right")
    cv.text(kx + 2.2, iy + 24.4, "verdict per edited file", size=6.0, style="italic", color=MUTED, ha="left")
    cv.flow_chips(["helped", "hurt", "confounded", "no observed effect"], kx + 2.2, kx + kw - 2.0, iy + 22.4, IMPROVER,
                  size=5.9, h=3.3, gap=1.0, row_gap=0.8, align="left")
    cv.text(kx + 2.2, iy + 29.6, "lesson, if a contrast supports it", size=6.0, style="italic", color=MUTED, ha="left")
    cv.doc(kx + 3.0, iy + 33.0, 8.4, 10.6, IMPROVER, lines=4, z=6)
    cv.text(kx + 13.4, iy + 42.0, "EXPERIENCE.md", size=5.8, weight="bold", color=pur["ink"], ha="left", **MONO)
    for i, f in enumerate(("situation", "lesson", "evidence")):
        cv.text(kx + 13.4, iy + 39.0 - i * 2.7, f, size=6.0, ha="left")
    cv.arrow([(ix + iw, dy + dh / 2), (rcx, dy + dh / 2), (rcx, iy)], color=pur["mark"], lw=1.1, head=1.5)
    cv.text((ix + iw + rcx) / 2 - 0.5, dy + dh / 2 + 1.8, "after the task", size=6.0, style="italic", color=pur["ink"])
    cv.arrow([(rcx, iy + ih), (rcx, sy)], color=pur["mark"], lw=1.1, head=1.5)
    cv.text(rcx - 1.5, (iy + ih + sy) / 2, "Update", size=6.6, weight="bold", color=pur["ink"], ha="right")

    # ---- key ---------------------------------------------------------------------------------------------------------
    def cells(roles):
        def f(x, y):
            for i, r in enumerate(roles):
                fc = ROLE[r]["mark"] if r else "#E3E6EB"
                cv.ax.add_patch(S.Rectangle((x - len(roles) * 1.75 + i * 3.5, y - 1.5), 3.3, 3.0, fc=fc, ec="none", zorder=11))
        return f

    S.key(cv, 1.2, 1.0, 175.6, h=6.6, items=[
        (cells([None]), 3.5, "inherited file"),
        (cells([INV, DOM]), 7.0, "file edited by that candidate (C1–C8 as in Fig. 2)"),
        (lambda x, y: S.record(cv, x - 2.0, y - 2.5, MODEL, w=4.0, h=5.0, z=11), 4.0, r"execution record $e=(\tau,y)$"),
        (lambda x, y: cv.op(x, y, r"$\Delta$", d=3.4, z=11), 3.4, r"behavioral contrast"),
        (lambda x, y: S.darrow(cv, [(x - 3.2, y), (x + 3.2, y)], color=pur["mark"], lw=0.9, head=1.2), 6.4, "library read"),
        (lambda x, y: cv.arrow([(x - 3.2, y), (x + 3.2, y)], color=pur["mark"], lw=1.1, head=1.3), 6.4, "library write"),
    ])

    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=".")
    ap.add_argument("--vector-icons", action="store_true", help="draw vector stand-ins instead of the raster icons")
    a = ap.parse_args()
    print(draw(a.out, a.vector_icons))
