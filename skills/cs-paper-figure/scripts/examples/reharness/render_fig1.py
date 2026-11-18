#!/usr/bin/env python3
"""ReHarness Fig. 1 as a fork: one history, two futures (arXiv:2610.12668), 178 x 63.6 mm.

Source: Xiao et al., "Recurrent Harness for Agentic Continual Learning", Fig. 1 and Sec. 3. The content
(tasks, token values, reflections, step order, notation, Eqs. 2-3 instantiated for i = t-1) is the
paper's. An earlier redesign (in the git history of this file) drew the instance stream between two
framed harnesses; this one departs from it and from the paper's two-panel layout.

Family: ours versus a baseline that share part of the run; plate register, full width.
Model: assets/models/plate_agent_loop.png (this figure).
  * Message: a forward-only memory keeps a wrong lesson and is misled by it twice; going back to revise
    the old lesson with later feedback fixes the next task.
  * The picture: the shared history once, as one left-to-right row (task, notebook, failed task). At the
    failure the write forks. The stateful harness runs straight on (it only writes forward). ReHarness
    drops into the row below and reaches back under the history: the one warm arrow points left, at the
    old line of the same notebook, struck out and rewritten. Both lanes dock on one card for the next
    task, its input between their two answers.
  * Hero: the warm lane, and in it the backward arrow and the revised notebook h'_t. It is made by hue
    and by direction (the only arrow that points left), not by weight.
  * One slot grid for every card: a header, then two slots of 8.2 mm. In a notebook the newer reflection
    is added on top, so slot 1 is what the last task wrote and slot 2 the older lesson. Every arrow then
    ends on the line it writes, reads or rewrites, and none has to cross another.
  * Hue is the agent: slate = decision agent pi_D and its tasks, blue = memory agent pi_M and what it
    wrote, orange = revision agent pi_R and what it rewrote. Green and red only on rewards. The memory is
    one object every time: a ring-bound pad with a cover strip in its writer's hue and a tab on each line.
  * Drawn here because paperkit has no primitive for them: the notebook, the lane tab that sits on its
    tray, the two direction marks inside the next task's card.
  * Type: Times at 8.4 / 7.4 / 6.4 pt. Strokes: outlines 0.7 pt, arrows 1.2 pt (head 2.0 mm). Eight
    arrows. Two numerals, only in the lower lane, where the order (revise, then write) is not the
    reading order; the same numerals name the two equations.

    python render_fig1.py --out DIR  ->  DIR/reharness_fig1.{pdf,svg,png}
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import paperkit as pk  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Polygon, Rectangle  # noqa: E402

STEM = "reharness_fig1"
HEAD, LABEL, FINE = 8.4, 7.4, 6.4       # the three text sizes
LW, AW, AH = 0.7, 1.2, 2.0              # outline weight, arrow weight, arrow head (mm)

# ---- roles: one meaning per hue --------------------------------------------------------------------
SLATE = dict(fill="#F1F3F6", soft="#E3E7ED", stroke="#74859C", ink="#2F3B4D", mark="#5E7088")  # pi_D, tasks
BLUE = dict(fill="#EAF2FC", soft="#D5E4F7", stroke="#3F78C2", ink="#1B467F", mark="#2F6FC0")   # pi_M, memory
WARM = dict(fill="#FFF0DA", soft="#FAD7A2", stroke="#D0822A", ink="#8A4706", mark="#D9730B")   # pi_R, revision
OK = dict(fill="#E4F3E9", ink="#1C5A35", mark="#2E8B57")     # reward: correct
BAD = dict(fill="#FCE9E5", ink="#8C2A18", mark="#CF4530")    # reward: wrong
TRAY_A, TRAY_B = "#EEF0F3", WARM["fill"]
INK, MUTED = pk.INK, pk.MUTED

# ---- the running example (the paper's) -------------------------------------------------------------
R_OLD = ("Put larger", "numbers first")
R_NEW_A = ("Put smaller", "numbers first")
R_REV = ("Larger first", "only if descending")
R_NEW_B = ("Smaller first", "only if ascending")
for xs, ys, desc in (((3, 7, 4), (7, 4, 3), True), ((3, 7, 4), (3, 4, 7), False)):   # the two correct answers
    assert list(ys) == sorted(xs, reverse=desc)
assert [9, 5, 2] == sorted((2, 9, 5), reverse=True)   # tau_t: asked ascending, answered descending
assert [7, 4, 3] == sorted((3, 7, 4), reverse=True)   # tau_{t+1} under the stale lesson: descending again

# ---- column grid (mm): task, notebook, task, notebook, task; the gutter where the write forks is wider ----
W = 178.0
X0, CW, NW = 0.8, 27.0, 34.0
G1, G2, G3, G4 = 6.2, 6.2, 8.2, 6.6
assert abs(X0 + 3 * CW + 2 * NW + G1 + G2 + G3 + G4 + 1.0 - W) < 1e-6
XT0 = X0
XH = XT0 + CW + G1
XT1 = XH + NW + G2
XH1 = XT1 + CW + G3
XT2 = XH1 + NW + G4
XG = XT1 + CW + 3.4                      # where the write forks, in the gutter after tau_t

# ---- slot grid and rows (mm, bottom-up) -------------------------------------------------------------
HDR, PAD, SLOT, SG = 4.4, 1.0, 8.2, 0.6


def card_h(n):
    return HDR + 2 * PAD + n * SLOT + (n - 1) * SG


def slot_c(top, i):
    """Centre line of slot i of a card whose top edge is at `top`."""
    return top - HDR - PAD - SLOT / 2 - i * (SLOT + SG)


ROW, TAB_H = card_h(2), 4.4
B_BOT = 2.6
B_TOP = B_BOT + ROW
TRAYB = (0.0, B_BOT - 2.0, XT2, B_TOP + 1.8)                # x0, y0, x1, y1: reaches back under the history
A_BOT = TRAYB[3] + 5.6
A_TOP = A_BOT + ROW
TRAYA = (XH1 - 1.6, A_BOT - 2.0, XT2, A_TOP + 1.8)          # both lanes dock on the next task's card
H = TRAYA[3] + TAB_H + 0.6
E1A, E2A, E1B, E2B = slot_c(A_TOP, 0), slot_c(A_TOP, 1), slot_c(B_TOP, 0), slot_c(B_TOP, 1)
LINE = 1.9                               # half the distance between the two text lines of a slot


def shade(v):
    """Token fill by magnitude (2..9): larger = darker, so an order is a visible ramp."""
    return dict(soft=pk.mix("#FAFBFC", "#9DA8B7", (v - 2) / 7), stroke="#7F8A99", ink=INK)


def strip(cv, x, cy, w, fc, alpha=1.0):
    cv.ax.add_patch(FancyBboxPatch((x, cy - SLOT / 2), w, SLOT, boxstyle="round,pad=0,rounding_size=0.8", fc=fc,
                                   ec="none", zorder=5.4, alpha=alpha))


def reward(cv, x, cy, good, d=3.2):
    r = OK if good else BAD
    cv.ax.add_patch(Circle((x, cy), d / 2, fc=r["mark"], ec="none", zorder=9))
    (cv.icon_check if good else cv.icon_cross)(x, cy, d * 0.52, color="white", lw=0.9, z=10)


def agent(cv, xr, cy, sym, r, on_cover=False):
    """Who produced the card: the agent glyph in its hue with its symbol, right-aligned at xr."""
    cv.icon_robot(xr - 1.6, cy + 0.1, 3.0, color="white" if on_cover else r["mark"],
                  fill=r["mark"] if on_cover else "white", lw=0.6, z=8)
    cv.text(xr - 3.9, cy, sym, size=LABEL, color="white" if on_cover else r["ink"], ha="right")


def numbers(cv, x, cy, vals):
    cv.tokens(x, cy - 1.6, 3, w=3.6, h=3.2, gap=0.4, labels=[str(v) for v in vals], fills=[shade(v) for v in vals],
              size=LABEL, lw=0.45)
    return x + 3 * 3.6 + 2 * 0.4


def x_slot(cv, x, cy, sub, order, xs, tx):
    strip(cv, x + PAD, cy, CW - 2 * PAD, SLATE["fill"])
    xe = cv.rich(x + 1.9, cy + LINE, [(f"sort {order}", INK)], size=LABEL)
    assert xe <= x + CW - 1.2, (order, xe)
    cv.text(x + 1.9, cy - LINE, rf"$x_{{{sub}}}$", size=LABEL, color=SLATE["ink"], ha="left")
    numbers(cv, x + tx, cy - LINE, xs)


def y_slot(cv, x, cy, sub, ys, good, note, tx):
    r = OK if good else BAD
    strip(cv, x + PAD, cy, CW - 2 * PAD, r["fill"])
    cv.text(x + 1.9, cy + LINE, rf"$y_{{{sub}}}$", size=LABEL, color=SLATE["ink"], ha="left")
    xe = numbers(cv, x + tx, cy + LINE, ys)
    reward(cv, xe + 2.7, cy + LINE, good)
    cv.text(x + tx, cy - LINE, note, size=FINE, color=r["ink"], style="italic", ha="left")
    return xe + 2.7


def task(cv, x, top, sub, order, xs, ys, good, note, tx):
    """A task card tau = (x, y, r): name and decision agent, the input slot, the output slot with its reward."""
    h = card_h(2)
    cv.box(x, top - h, CW, h, SLATE, fill="white", lw=LW, radius=1.3)
    cv.text(x + 1.9, top - HDR / 2 - 0.2, rf"$\tau_{{{sub}}}$", size=HEAD, color=SLATE["ink"], ha="left")
    agent(cv, x + CW - 1.4, top - HDR / 2 - 0.2, r"$\pi_D$", SLATE)
    x_slot(cv, x, slot_c(top, 0), sub, order, xs, tx)
    return y_slot(cv, x, slot_c(top, 1), sub, ys, good, note, tx)


def notebook(cv, x, top, name, who, r, entries, tx):
    """The memory, drawn the same way every time: a ring-bound pad whose lines are reflections, the newest
    on top. Each line carries a tab in the hue of the agent that wrote it. entries = [(label, tab role,
    (line1, line2), opts)]; opts: tag=, or was=(label, lines) for a line rewritten in place, which then takes
    both slots: the old text struck out above the new one, under one tab."""
    n = sum(2 if e[3].get("was") else 1 for e in entries)
    h = card_h(n)
    cv.box(x, top - h, NW, h, r, fill=r["soft"], stroke=r["mark"], lw=LW, radius=1.3)
    cv.ax.add_patch(PathPatch(pk._round_top_rect(x, top - HDR, NW, HDR, 1.3), fc=r["mark"], ec=r["mark"], lw=LW,
                              zorder=5.2))                # the cover strip of the pad, with its binding
    for k in range(5):
        cv.ax.add_patch(FancyBboxPatch((x + NW / 2 - 6.4 + k * 3.0, top - 1.1), 0.8, 2.1,
                                       boxstyle="round,pad=0,rounding_size=0.4", fc=r["ink"], ec="none", zorder=6))
    cv.text(x + 1.9, top - HDR / 2 - 0.1, name, size=HEAD, color="white", ha="left")
    agent(cv, x + NW - 1.4, top - HDR / 2 - 0.1, *who, on_cover=True)

    def lines_at(cy, label, lines, ink, struck=False):
        cv.text(x + 3.5, cy + LINE, label, size=LABEL, color=ink, ha="left")
        for j, s in enumerate(lines):
            yy = cy + LINE - j * 2 * LINE
            xe = cv.rich(x + tx, yy, [(s, MUTED)] if struck else s if isinstance(s, list) else [(s, INK)], size=LABEL)
            assert xe <= x + NW - PAD - 0.4, (s, xe - x)
            if struck:
                cv.ax.plot([x + tx - 0.3, xe + 0.3], [yy - 0.1, yy - 0.1], color=MUTED, lw=LW, zorder=21,
                           solid_capstyle="round")

    i = 0
    for label, tab, lines, opt in entries:
        cy, was = slot_c(top, i), opt.get("was")
        y0 = cy - SLOT / 2 - ((SLOT + SG) if was else 0)                  # a rewritten line spans two slots
        hh = SLOT + ((SLOT + SG) if was else 0)
        cv.ax.add_patch(FancyBboxPatch((x + PAD, y0), NW - 2 * PAD, hh, boxstyle="round,pad=0,rounding_size=0.8",
                                       fc="white", ec="none", zorder=5.4))
        cv.ax.add_patch(Rectangle((x + PAD + 0.7, y0 + 0.9), 0.9, hh - 1.8, fc=tab["mark"], ec="none", zorder=5.6))
        if was:
            lines_at(cy, was[0], was[1], MUTED, struck=True)
            i += 1
            cy = slot_c(top, i)
        lines_at(cy, label, lines, tab["ink"])
        if opt.get("tag"):
            cv.text(x + NW - PAD - 0.9, cy + LINE, opt["tag"], size=FINE, color=opt.get("tag_ink", MUTED),
                    style="italic", ha="right")
        i += 1


def lane(cv, tray, fc, r, title, note=None):
    """A future: a pale borderless tray with its name on a solid tab that sits on the tray."""
    x0, y0, x1, y1 = tray
    cv.box(x0, y0, x1 - x0, y1 - y0, r, fill=fc, stroke="none", lw=0, radius=1.8, container=True, z=1)
    w = cv.text_width(title, HEAD, "bold") + 3.6
    cv.ax.add_patch(PathPatch(pk._round_top_rect(x0, y1, w, TAB_H, 1.3), fc=r["mark"], ec="none", zorder=2))
    cv.text(x0 + w / 2, y1 + TAB_H / 2 - 0.1, title, size=HEAD, color="white", weight="bold")
    if note:
        cv.text(x0 + w + 1.6, y1 + TAB_H / 2 - 0.1, note, size=LABEL, color=r["ink"], style="italic", ha="left")


def wire(cv, pts, r, label=None, radius=1.2):
    cv.arrow(pts, color=r["mark"], lw=AW, head=AH, radius=radius)
    if label:
        (xa, ya), (xb, _) = pts[0], pts[1]
        cv.text((xa + xb) / 2, ya + 1.9, label, size=FINE, color=r["ink"])


def build():
    cv = pk.Canvas(W, H, family="serif", size=LABEL)
    tx = 1.9 + max(cv.text_width(rf"${v}_{{t+1}}$", LABEL) for v in "xy") + 0.9          # token column of a task
    txn = 3.5 + max(cv.text_width(s, LABEL) for s in ("$R_{t-1}$", r"$R^{\prime}_{t-1}$")) + 1.0  # text column
    PI_D, PI_M, PI_R = (r"$\pi_D$", SLATE), (r"$\pi_M$", BLUE), (r"$\pi_R$", WARM)

    # ---- the two futures: trays under the part of the run each one owns ------------------------------
    lane(cv, TRAYA, TRAY_A, SLATE, "(a) Stateful harness", "only writes forward")
    lane(cv, TRAYB, TRAY_B, WARM, "(b) ReHarness")
    yh = TRAYA[3] + TAB_H / 2 - 0.1
    xe = cv.rich(X0, yh, [("Shared history", INK, "bold")], size=HEAD)
    xe = cv.rich(xe + 1.8, yh, [("memory agent ", MUTED), (PI_M[0], BLUE["ink"]), (" writes a reflection, decision agent ",
                                 MUTED), (PI_D[0], SLATE["ink"]), (" reads it", MUTED)], size=LABEL, style="italic")
    assert xe < TRAYA[0] - 2.0, xe

    # ---- shared history: tau_{t-1} -> h_t -> tau_t, one straight line ----------------------------------
    task(cv, XT0, A_TOP, "t-1", "descending", (3, 7, 4), (7, 4, 3), True, "correct", tx)
    notebook(cv, XH, A_TOP, "$h_t$", PI_M, BLUE, [("$R_{t-1}$", BLUE, R_OLD, {})], txn)
    xv = task(cv, XT1, A_TOP, "t", "ascending", (2, 9, 5), (9, 5, 2), False, "misled", tx)
    wire(cv, [(XT0 + CW, E1A), (XH, E1A)], BLUE, "write")
    wire(cv, [(XH + NW, E1A), (XT1, E1A)], SLATE, "read")

    # ---- (a) forward only: a new line on top, the stale one stays --------------------------------------
    notebook(cv, XH1, A_TOP, "$h_{t+1}$", PI_M, BLUE,
             [("$R_t$", BLUE, R_NEW_A, {}), ("$R_{t-1}$", BLUE, R_OLD, dict(tag="stale", tag_ink=BAD["ink"]))], txn)
    wire(cv, [(XT1 + CW, E1A), (XH1, E1A)], BLUE)
    cv.text(XT1 + CW + G3 / 2 + 0.3, E1A + 1.9, "write", size=FINE, color=BLUE["ink"])

    # ---- (b) the same notebook, its old line rewritten in place; then the same write, with it in memory --
    notebook(cv, XH, B_TOP, r"$h^{\prime}_t$", PI_R, WARM,
             [(r"$R^{\prime}_{t-1}$", WARM, ["Larger first", [("only if descending", WARM["ink"], "bold", WARM["soft"])]],
               dict(was=("$R_{t-1}$", R_OLD)))], txn)
    notebook(cv, XH1, B_TOP, "$h_{t+1}$", PI_M, BLUE,
             [("$R_t$", BLUE, ["Smaller first", [("only if ascending", BLUE["ink"])]], {}),
              (r"$R^{\prime}_{t-1}$", WARM, ["Larger first", [("only if descending", WARM["ink"])]], {})], txn)
    for xx in (XH + 1.3, XH + NW - 1.3):                 # h'_t is h_t: construction lines, not a flow
        cv.ax.plot([xx, xx], [A_TOP - card_h(1) - 0.5, B_TOP + 1.3], color=BLUE["stroke"], lw=LW, ls=(0, (2.2, 1.8)),
                   zorder=3)
    cv.text(XH + NW / 2, (A_TOP - card_h(1) + TRAYB[3]) / 2 + 0.2, "the same notebook, revised", size=FINE, color=MUTED,
            style="italic")
    yb = TRAYB[3] + (A_BOT - TRAYB[3]) / 2 - 0.4         # numerals: on the two wires, between the rows
    wire(cv, [(xv, A_BOT), (xv, E1B), (XH + NW, E1B)], WARM, radius=3.2)                    # 1: backward, points left
    cv.badge(xv, yb, 1, WARM, d=3.2, size=FINE, rim=LW)
    wire(cv, [(XT1 + CW, E1A), (XG, E1A), (XG, E1B), (XH1, E1B)], BLUE)                     # 2: the fork, same write
    cv.dot(XG, E1A, BLUE["mark"], d=1.5)
    cv.badge(XG, yb, 2, BLUE, d=3.2, size=FINE, rim=LW)
    wire(cv, [(XH + NW, E2B), (XH1, E2B)], WARM)                                            # the revised line returns
    xl = XH + NW + 2.2
    cv.text(xl, E1B + 2.9, "Backward revision", size=LABEL, color=WARM["ink"], weight="bold", ha="left")
    xe = cv.rich(xl, E1B - 2.7, [("revision agent ", INK), (PI_R[0], WARM["ink"]), (" rewrites ", INK),
                                 ("$R_{t-1}$", BLUE["ink"])], size=LABEL)
    assert xe < XG - 1.0, xe
    xe = cv.rich(xl, E1B - 6.1, [("with the feedback from ", INK), (r"$\tau_t$", SLATE["ink"])], size=LABEL)
    assert xe < XH1 - 3.5, xe
    cv.text((XH + NW + XH1) / 2, E2B - 2.0, "kept as a demonstration", size=FINE, color=WARM["ink"], style="italic")

    # ---- what the lower lane computes: the two numbered steps, as the paper's Eqs. 2-3 for this example --
    xb = 2.4
    cv.text(xb - 0.8, TRAYB[3] - 3.4, "goes back and revises", size=LABEL, color=WARM["ink"], style="italic", ha="left")
    eqs = [(1, WARM, [(r"$R^{\prime}_{t-1}$", WARM["ink"]), (r"$\,=\pi_R($", INK), ("$R_{t-1}$", BLUE["ink"]),
                      (r"$,\tau_{t-1};\,\tau_t)$", INK)]),
           (2, BLUE, [(r"$R_t\,=\pi_M(\tau_t;$", INK), 0.6, (r"$R^{\prime}_{t-1}$", WARM["ink"]), ("$)$", INK)]),
           (None, None, [(r"$h_{t+1}=$", INK), 0.6, (r"$h^{\prime}_t$", WARM["ink"]), (r"$\,\oplus R_t$", INK)])]
    for k, (num, r, segs) in enumerate(eqs):
        yy = E1B + 0.8 - k * 5.0
        if num:
            cv.badge(xb + 0.8, yy, num, r, d=3.2, size=FINE, rim=0)
        xe = xb + 3.4
        for seg in segs:          # a number is a gap in mm: mathtext drops a space at either end of a run
            xe = xe + seg if isinstance(seg, float) else cv.rich(xe, yy, [seg], size=LABEL)
        assert xe < XH - 1.0, (num, xe)

    # ---- the next task, once: its input between the two answers, the three token rows on one vertical ---
    top, bot = E2A + SLOT / 2 + PAD, E2B - SLOT / 2 - PAD
    assert abs(bot - B_BOT) < 1e-6
    cv.box(XT2, bot, CW, top - bot, SLATE, fill="white", lw=LW, radius=1.3)
    cv.text(XT2, top + 6.7, "Next task", size=HEAD, color=INK, weight="bold", ha="left")
    xe = cv.rich(XT2, top + 2.7, [("the numbers of ", MUTED), (r"$\tau_{t-1}$", SLATE["ink"]), (" again", MUTED)],
                 size=LABEL, style="italic")
    assert xe <= W - 0.3, xe
    y_slot(cv, XT2, E2A, "t+1", (7, 4, 3), False, "misled again", tx)
    y_slot(cv, XT2, E2B, "t+1", (3, 4, 7), True, "guided correctly", tx)
    free = ((E2A - SLOT / 2) - (E2B + SLOT / 2) - (HDR + SLOT)) / 2
    yn = E2A - SLOT / 2 - free - HDR / 2
    cv.text(XT2 + 1.9, yn, r"$\tau_{t+1}$", size=HEAD, color=SLATE["ink"], ha="left")
    agent(cv, XT2 + CW - 1.4, yn, *PI_D)
    yx = yn - HDR / 2 - SLOT / 2
    x_slot(cv, XT2, yx, "t+1", "ascending", (3, 7, 4), tx)
    xc = XT2 + tx + 5.8                                   # centre of the token column
    for yc, s in ((E2A - SLOT / 2 - free / 2, 1), (E2B + SLOT / 2 + free / 2, -1)):   # input -> each answer
        cv.ax.add_patch(Polygon([(xc - 1.3, yc - s * 0.75), (xc + 1.3, yc - s * 0.75), (xc, yc + s * 0.75)],
                                fc=SLATE["stroke"], ec="none", zorder=6))
    wire(cv, [(XH1 + NW, E2A), (XT2, E2A)], SLATE, "read")
    wire(cv, [(XH1 + NW, E2B), (XT2, E2B)], SLATE, "read")

    assert not cv.overlaps() and not cv.text_overlaps() and not cv.wire_crossings(), \
        (cv.overlaps(), cv.text_overlaps(), cv.wire_crossings())
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/reharness")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
