#!/usr/bin/env python3
"""Ray's end-to-end example as one sequence chart, in one column (84 x 93 mm).

Source: Moritz et al., "Ray: A Distributed Framework for Emerging AI Applications", OSDI 2018,
arXiv:1712.05889v2, Figure 7 and Section 4.3 "Putting Everything Together". Every step, its sender, its
receiver and its plane (solid or dotted in the source) are the paper's and are asserted at the end of
build(); nothing is added, dropped or reordered. Step 1 of (b) follows the text (the driver checks its
local object store); the source figure draws that arc to the local scheduler. Steps 3 and 6 of (a) end on
the Object Table, where the GCS keeps object locations. The verb beside each number is the paper's word.

Register: line art (references/registers.md §1), the timeline family: one lane per component, time running
down, one message per row, both protocols on one set of lifelines.
  * Message: of seventeen steps six move data and only three of those leave a node; the other eleven are
    control messages between schedulers, stores and the Object Table.
  * Hero: the data-plane steps, the only coloured and the only solid arrows. Nothing is thicker.
  * One hue, blue = data plane: the arrow, its step number, and the cell of every object or function held
    in memory. Control-plane messages are black and dotted. Lifelines are grey scaffolding, and one pale
    grey column stands behind the lanes of each node, so an arrow that leaves a column crosses the network.
  * One stroke weight, 0.6 pt, for cells, arrows, rules and lifelines; one arrow head, 1.1 mm.
  * Two text sizes: 7.2 pt for panel heads and cell contents (subscripts then stay at 5.0 pt), 6.0 pt for
    lane heads, verbs, numerals, code and the key. Code is monospace.
  * State is drawn where and when it changes: a cell appears on a lane in the row that creates it, and
    the lifelines are interrupted between the two calls.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import Canvas, ROLE  # noqa: E402

STEM = "ray_fig7_example"
W, H = 84.0, 93.2
LW, HEAD = 0.6, 1.1                     # the one stroke weight (pt) and the one arrow head (mm)
BIG, SMALL = 7.2, 6.0                   # the two text sizes (pt)
BLUE = ROLE["blue"]["mark"]             # data plane
TINT = ROLE["blue"]["soft"]             # a cell held in memory
GREY = "#B3B3B3"                        # lifelines
FIELD = "#F2F2F2"                       # the column of a node
EDGE = 3.0                              # a group reaches this far beyond its outer lanes (mm)
DOTS = (0, (1.3, 1.9))                  # control plane: dotted, in units of the stroke
RP, CH = 3.2, 2.8                       # row pitch and cell height (mm)
SP = 3.3                                # pitch of two stacked table entries (their subscripts need it)
D, L1, S1, FT, OT, GS, S2, L2, WK = range(9)
LANES = ["Driver", "Local\nscheduler", "Object\nstore", "Function\nTable", "Object\nTable",
         "Global\nscheduler", "Object\nstore", "Local\nscheduler", "Worker"]
GROUPS = [("N1", D, S1), ("GCS", FT, OT), ("N2", S2, WK)]
PITCH = [7.2, 7.2, 8.2, 9.4, 9.4, 8.3, 7.2, 7.2]   # the Object Table lane is wider: it holds table rows
XDISC, XVERB = 1.75, 4.0


class Chart:
    def __init__(self):
        self.cv = cv = Canvas(W, H, family="serif", size=SMALL)
        x = W - 0.6 - cv.text_width("Worker", SMALL) / 2
        self.x = [x - sum(PITCH[k:]) for k in range(9)]
        self.cuts = {k: [] for k in range(9)}        # y intervals where a cell interrupts a lifeline
        self.verb_edge = 0.0
        self.log = []                                # (number, sender, receiver, plane) of every step drawn

    # ---- cells: square-cornered, the one stroke; tinted = held in memory, white = a table row ----------
    def cell(self, lane, y, text, **kw):
        cv = self.cv
        size = SMALL if kw.get("family") == "monospace" else BIG     # code keeps the size of the code in the heads
        w = max(CH, cv.text_width(text, size, **kw) + 1.1)
        cv.box(self.x[lane] - w / 2, y - CH / 2, w, CH, "line", radius=0, lw=LW, fill=TINT)
        cv.text(self.x[lane], y - 0.05, text, size=size, color="black", **kw)
        self.cuts[lane].append((y - CH / 2, y + CH / 2))
        return self.x[lane] - w / 2, self.x[lane] + w / 2

    def entry(self, y, key, val, x0=None):
        """One Object Table row: object id | nodes that hold it. Centred on the table's lane unless x0 is given."""
        cv = self.cv
        wk, wv = cv.text_width(key, BIG) + 1.0, cv.text_width(val, BIG) + 1.2
        if x0 is None:
            x0 = self.x[OT] - (wk + wv) / 2
            self.cuts[OT].append((y - CH / 2, y + CH / 2))
        cv.box(x0, y - CH / 2, wk, CH, "line", radius=0, lw=LW)
        cv.box(x0 + wk, y - CH / 2, wv, CH, "line", radius=0, lw=LW)
        cv.text(x0 + wk / 2, y - 0.05, key, size=BIG, color="black")
        cv.text(x0 + wk + wv / 2, y - 0.2, val, size=BIG, color="black")      # capitals: centre the cap height
        return x0, x0 + wk + wv

    # ---- one message -----------------------------------------------------------------------------------
    def wire(self, xa, xb, y, data, both=False, dot=True):
        """Solid blue = data plane, dotted black = control plane. A control wire is a dotted shaft plus solid heads,
        with the pitch DOTS tuned to this chart's 3.2 mm rows; cv.arrow(dotted=True) draws the same thing at
        paperkit's default pitch."""
        cv, c, s = self.cv, BLUE if data else "black", 1 if xb > xa else -1
        if data:
            cv.arrow([(xa, y), (xb, y)], color=c, lw=LW, head=HEAD, radius=0, both=both)
        else:
            stub = s * (HEAD + 0.25)
            cv.line([(xa + (stub if both else 0), y), (xb - stub, y)], color=c, lw=LW, radius=0)
            shaft = cv.ax.patches[-1]
            shaft.set_linestyle(DOTS)
            shaft.set_capstyle("butt")
            cv.arrow([(xb - stub, y), (xb, y)], color=c, lw=LW, head=HEAD, radius=0)
            if both:
                cv.arrow([(xa + stub, y), (xa, y)], color=c, lw=LW, head=HEAD, radius=0)
        if dot and not both:
            cv.dot(xa, y, color=c, d=0.9)

    def step(self, k, verb, y, src, dst, data=False, both=False, xa=None, xb=None):
        cv = self.cv
        self.log.append((k, src, dst, "data" if data else "control"))
        cv.dot(XDISC, y, color=BLUE if data else "black", d=2.8)     # cv.badge adds a white 0.5 pt edge
        cv.text(XDISC, y - 0.1, str(k), size=SMALL, color="white", weight="bold")
        cv.text(XVERB, y, verb, size=SMALL, color="black", ha="left")
        self.verb_edge = max(self.verb_edge, XVERB + cv.text_width(verb, SMALL))
        self.wire(self.x[src] if xa is None else xa, self.x[dst] if xb is None else xb, y, data, both,
                  dot=xa is None)

    def arrive(self, lane, y, text, frm):
        """A cell that a data-plane step creates on `lane`; returns the edge the arrow lands on."""
        x0, x1 = self.cell(lane, y, text)
        return x0 if self.x[frm] < self.x[lane] else x1

    # ---- lanes -------------------------------------------------------------------------------------------
    def heads(self, y):
        """Lane names in two lines; a one-line name takes the first line, which clears "scheduler" beside it."""
        cv, lh = self.cv, 2.3
        for k, name in enumerate(LANES):
            for i, s in enumerate(name.split("\n")):
                cv.text(self.x[k], y - (i + 0.5) * lh, s, size=SMALL, color="black")
        return y - 2 * lh

    def tags(self, y):
        """Node names over their lanes, each with a rule; the global scheduler belongs to no node."""
        cv = self.cv
        for name, a, b in GROUPS:
            cv.text((self.x[a] + self.x[b]) / 2, y, name, size=SMALL, color="black", weight="bold")
            cv.line([(self.x[a] - EDGE, y - 1.6), (self.x[b] + EDGE, y - 1.6)], color="black", lw=LW)

    def nodes(self, spans):
        """A pale column behind the lanes of each node: an arrow that leaves a column crosses the network."""
        for name, a, b in GROUPS:
            if name.startswith("N"):
                for top, bot in spans:
                    self.cv.box(self.x[a] - EDGE, bot, self.x[b] - self.x[a] + 2 * EDGE, top - bot, "line", radius=0,
                                lw=0, fill=FIELD, stroke="none", container=True, z=1)

    def lifelines(self, spans):
        """Grey lifelines over the y spans, broken wherever a cell sits on the lane."""
        for k in range(9):
            for top, bot in spans:
                top_k = top + (2.3 if "\n" not in LANES[k] and top == spans[0][0] else 0.0)
                edges, bot_k = [top_k], bot
                for lo, hi in sorted(self.cuts[k], reverse=True):
                    if bot_k < lo < hi < top_k:
                        edges += [hi, lo]
                edges.append(bot_k)
                for a, b in zip(edges[::2], edges[1::2]):
                    if a - b > 0.05:
                        self.cv.line([(self.x[k], a), (self.x[k], b)], color=GREY, lw=LW, z=2)


def title(cv, y, letter, text, code):
    cv.text(0.4, y, f"({letter})", size=BIG, color="black", weight="bold", ha="left")
    cv.text(0.4 + cv.text_width(f"({letter})", BIG, "bold") + 0.9, y, text, size=BIG, color="black", ha="left")
    cv.text(W - 0.4, y, code, size=SMALL, color="black", ha="right", family="monospace")


def note(cv, y, text):
    """A state row, not a message: italic, no number."""
    cv.text(XVERB, y, text, size=SMALL, color="black", ha="left", style="italic")


def build():
    ch = Chart()
    cv, x = ch.cv, ch.x

    # (a): head, lanes, state at the start
    y = H - 1.8
    title(cv, y, "a", "Executing a task remotely", "id_c = add.remote(a, b)")
    ch.tags(y - 3.4)
    life_top = ch.heads(y - 5.9) - 0.4
    s2 = life_top - 0.7 - CH / 2 - SP                 # two state rows; the Object Table's are its two entries
    ch.entry(s2 + SP, "$id_a$", "N1")
    ch.entry(s2, "$id_b$", "N2")
    ch.cell(S1, s2 + SP / 2, "$a$")
    ch.cell(S2, s2 + SP / 2, "$b$")
    note(cv, s2 + SP / 2, "at start")

    ya = [s2 - CH / 2 - 0.8 - RP / 2 - k * RP for k in range(10)]
    # 0: add() is registered with the GCS at initialisation and distributed to every worker
    _, d1 = ch.cell(D, ya[0], "add", family="monospace")
    f0, f1 = ch.cell(FT, ya[0], "add", family="monospace")
    w0, _ = ch.cell(WK, ya[0], "add", family="monospace")
    ch.step(0, "register", ya[0], D, FT, data=True, xa=d1, xb=f0)
    ch.wire(f1, w0, ya[0], data=True, dot=False)
    ch.step(1, "submit", ya[1], D, L1)                      # driver submits add(a, b) to its local scheduler
    ch.step(2, "forward", ya[2], L1, GS)                    # which forwards it to the global scheduler
    ch.step(3, "look up", ya[3], GS, OT, both=True)         # locations of the arguments
    ch.step(4, "schedule", ya[4], GS, L2)                   # on N2, which stores b
    ch.step(5, "check", ya[5], L2, S2)                      # are the arguments in the local store?
    ch.step(6, "look up", ya[6], S2, OT, both=True)         # a is missing: where is it?
    ch.step(7, "replicate", ya[7], S1, S2, data=True, xb=ch.arrive(S2, ya[7], "$a$", S1))
    ch.step(8, "invoke", ya[8], L2, WK)                     # add() at a local worker
    ch.step(9, "read", ya[9], S2, WK, data=True)            # arguments, through shared memory

    # (b): the same lanes continue; the break in the lifelines is the time between the two calls
    a_bot = ya[9] - RP / 2 - 0.3
    yt = a_bot - 2.4
    title(cv, yt, "b", "Returning the result of a remote task", "c = ray.get(id_c)")
    b_top = yt - 2.1
    yb = [None] + [b_top - 0.3 - RP / 2 - k * RP for k in range(6)]
    yu = yb[6] - RP                                         # a state row: the entry after step 6
    yb.append(yu - RP)
    ch.step(1, "check", yb[1], D, S1)                       # driver asks its local store for c
    ch.step(2, "register", yb[2], S1, OT)                   # no entry for c yet: a callback is registered
    ch.step(3, "store", yb[3], WK, S2, data=True, xb=ch.arrive(S2, yb[3], "$c$", WK))
    e0, e1 = ch.entry(yb[4], "$id_c$", "N2")
    ch.step(4, "add entry", yb[4], S2, OT, xb=e1)
    ch.step(5, "callback", yb[5], OT, S1)                   # with c's entry
    ch.step(6, "replicate", yb[6], S2, S1, data=True, xb=ch.arrive(S1, yb[6], "$c$", S2))
    ch.entry(yu, "$id_c$", "N2, N1")                        # updated in step 6, once the copy is on N1
    note(cv, yu, "updated")
    ch.step(7, "return", yb[7], S1, D, data=True)
    b_bot = yb[7] - RP / 2 - 0.3
    foot = ch.heads(b_bot - 0.4)
    ch.lifelines([(life_top, a_bot), (b_top, b_bot)])
    ch.nodes([(life_top, a_bot), (b_top, b_bot)])

    # key: every encoding beside a sample of itself
    ky = foot - 3.2
    labels = ["data plane", "control plane", "object or function", "table entry"]
    samples = [5.0, 5.0, CH, cv.text_width("$id_a$", BIG) + cv.text_width("N1", BIG) + 2.2]
    used = sum(samples) + sum(0.9 + cv.text_width(t, SMALL) for t in labels)
    kx, gap = 0.5, (W - 1.0 - used) / 3                     # the key spans the column
    for i, t in enumerate(labels):
        if i < 2:
            ch.wire(kx, kx + 5.0, ky, data=i == 0, dot=False)
            kx += 5.0
        elif i == 2:
            cv.box(kx, ky - CH / 2, CH, CH, "line", radius=0, lw=LW, fill=TINT)
            kx += CH
        else:
            kx = ch.entry(ky, "$id_a$", "N1", x0=kx)[1]
        cv.text(kx + 0.9, ky, t, size=SMALL, color="black", ha="left")
        kx += 0.9 + cv.text_width(t, SMALL) + gap
    assert abs(kx - gap - (W - 0.5)) < 0.3, kx

    # the paper's sequence (Section 4.3): sender, receiver and plane of steps 0-9 of (a) and 1-7 of (b)
    c, d = "control", "data"
    assert ch.log == [(0, D, FT, d), (1, D, L1, c), (2, L1, GS, c), (3, GS, OT, c), (4, GS, L2, c), (5, L2, S2, c),
                      (6, S2, OT, c), (7, S1, S2, d), (8, L2, WK, c), (9, S2, WK, d),
                      (1, D, S1, c), (2, S1, OT, c), (3, WK, S2, d), (4, S2, OT, c), (5, OT, S1, c), (6, S2, S1, d),
                      (7, S1, D, d)], ch.log
    assert ch.verb_edge < x[D] - 2.6, (ch.verb_edge, x[D])     # the verb column clears the first lane's cell
    assert 0.3 < ky - CH / 2 < 0.8, ky                         # the key closes the canvas
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/ray")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
