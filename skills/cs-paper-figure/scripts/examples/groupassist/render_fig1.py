"""GroupAssistBench Fig. 1: one thread, two cuts, and the fact that changes sides.

Source: Hu, Zhang et al., "One Assistant, Many Memories: Benchmarking Real-World Group Assistance When
Recall Is Not Enough", arXiv:2611.04867v1 (CC BY 4.0), Fig. 1, with Sec. 3.1 (task and memory axes),
Table 2 (instances per cell), Sec. 3.3 and Table 6 (reference facts, rubric weights), Appendix A.5
(native and authored instances).

Kept from the source: the benchmark totals; the two task levels (L1 memory recall, L2 memory use) crossed
with the three memory dependencies (M1 single, M2 multiple, M3 conflicting) and the six counts of Table 2;
the trip-planning thread with its six messages, speakers, wording and highlighted spans; the two instances
cut from it (L1 x M2 at #104 with two reference facts, L2 x M3 at #452 with four grounding criteria and one
penalty), with every message number.

Design:
* The two task levels are the two bands of the plate. Each band starts in the taxonomy (its row of
  Table 2, one square per cell with area = number of instances) and continues to the right as the worked
  instance of that level, so "A is an L1 x M2 instance" is a position, not a letter to look up.
* The thread is drawn once, above both bands, as a chat window. Under it each instance shows the same
  thread as a strip of ten-message cells with its own cut: at #104 only the two anchors are in view, at
  #452 the strip also holds the revision. The cut is a picture in both rows and they share one x scale.
* The claim of the caption is the red rail on the right: the reference fact of A ("7:30 am on May 1",
  #34) runs down into the penalty row of B, where the same value is superseded.
* Colour: blue = L1, purple = L2; amber = anchor, red = superseded value, green = current value, the same
  as in render_fig2.py (ga_style.py). Words that come from the conversation are monospace.
* A lock marks what the evaluated system never sees (the answer key), as in Fig. 2.
* Labels follow the paper's text where the source figure departs from it: M1-M3 for the grid's D1-D3,
  "memory use" for "L2 serve", "instances" for "Quires"; the six cell names ("Recall for one" ...) are
  replaced by the row and column heads. Counts are Table 2's; 80,299 is the abstract's exact "80K".

    python render_fig1.py --out DIR [--vector-icons]
"""
import argparse
import math
import os
import sys

from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import ga_style as S  # noqa: E402
from ga_style import ANCHOR, CUR, INK, L1, L2, MONO, MUTED, OLD, ROLE, STRUCT, THREAD  # noqa: E402
from paperkit import Canvas  # noqa: E402

STEM = "groupassist_fig1_overview"
W, H = 178, 105.5
COUNTS = {L1: (776, 448, 150), L2: (221, 650, 150)}   # Table 2
assert sum(COUNTS[L1]) == 1374 and sum(COUNTS[L2]) == 1021 and sum(map(sum, COUNTS.values())) == 2395
DEPS = [("M1", "single"), ("M2", "multiple"), ("M3", "conflicting")]


def stat_glyph(cv, kind, x, y):
    """Small drawn noun for a benchmark total: stacked chat windows, speech bubbles, instance cards."""
    c = ROLE[STRUCT]
    if kind == "groups":
        for k in (2, 1, 0):
            x0, y0 = x - 4.6 + k * 1.1, y - 3.6 + k * 1.1
            cv.ax.add_patch(FancyBboxPatch((x0, y0), 7.0, 5.4, boxstyle="round,pad=0,rounding_size=0.7", fc="white",
                                           ec=c["stroke"], lw=0.5, zorder=5 - k * 0.1))
            cv.ax.add_patch(Rectangle((x0 + 0.25, y0 + 3.9), 6.5, 1.25, fc=S.SLATE if k == 0 else c["soft"], ec="none",
                                      zorder=5.05 - k * 0.1))
        for j, wd in enumerate((4.2, 3.0)):
            cv.ax.plot([x - 3.7, x - 3.7 + wd], [y - 1.0 - j * 1.3] * 2, color=c["stroke"], lw=0.8, zorder=6,
                       solid_capstyle="round")
    elif kind == "messages":
        for (bx, by, bw, fc, tail) in ((x - 4.4, y + 0.2, 6.2, c["soft"], -1), (x - 1.6, y - 3.6, 6.2, "white", 1)):
            cv.ax.add_patch(FancyBboxPatch((bx, by), bw, 3.2, boxstyle="round,pad=0,rounding_size=1.0", fc=fc,
                                           ec=c["stroke"], lw=0.5, zorder=5))
            tx = bx + (1.2 if tail < 0 else bw - 1.2)
            cv.ax.add_patch(Polygon([(tx - 0.6, by + 0.05), (tx + 0.6, by + 0.05), (tx + tail * 1.0, by - 1.0)], fc=fc,
                                    ec=c["stroke"], lw=0.5, zorder=4.9))
            cv.ax.add_patch(Rectangle((tx - 0.62, by + 0.05), 1.24, 0.3, fc=fc, ec="none", zorder=5.1))
            for j in range(3):
                cv.ax.plot([bx + 1.5 + j * 1.6] * 2, [by + 1.6] * 2, marker="o", ms=1.1, color=c["ink"], zorder=6)
    else:
        for k, r in ((1, L2), (0, L1)):
            x0, y0 = x - 4.0 + k * 1.7, y - 3.4 + k * 1.3
            cv.ax.add_patch(FancyBboxPatch((x0, y0), 6.4, 5.6, boxstyle="round,pad=0,rounding_size=0.7",
                                           fc=ROLE[r]["soft"], ec=ROLE[r]["stroke"], lw=0.5, zorder=5 - k * 0.1))
        for j, wd in enumerate((3.4, 2.6)):
            yy = y + 0.6 - j * 1.7
            cv.ax.add_patch(Rectangle((x - 3.3, yy - 0.55), 1.1, 1.1, fc=S.HL[ANCHOR], ec=ROLE[ANCHOR]["stroke"], lw=0.35,
                                      zorder=6))
            cv.ax.plot([x - 1.6, x - 1.6 + wd], [yy, yy], color=ROLE[L1]["stroke"], lw=0.8, zorder=6,
                       solid_capstyle="round")


def dep_glyph(cv, k, x, y):
    """Memory dependency as chips: one unit, two units, two units of which one supersedes another."""
    def chip(cx, r, struck=False):
        cv.ax.add_patch(FancyBboxPatch((cx - 1.35, y - 0.95), 2.7, 1.9, boxstyle="round,pad=0,rounding_size=0.45",
                                       fc=S.HL[r], ec=ROLE[r]["stroke"], lw=0.45, zorder=6))
        if struck:
            cv.ax.plot([cx - 1.0, cx + 1.0], [y - 0.6, y + 0.6], color=ROLE[r]["ink"], lw=0.6, zorder=7)
    if k == 0:
        chip(x, ANCHOR)
    elif k == 1:
        chip(x - 1.7, ANCHOR)
        chip(x + 1.7, ANCHOR)
    else:
        chip(x - 4.0, ANCHOR)
        chip(x - 0.3, OLD, struck=True)
        cv.arrow([(x + 1.25, y), (x + 2.75, y)], lw=0.5, head=0.9)
        chip(x + 4.2, CUR)


def draw(out, vector=False):
    S.VECTOR = vector
    cv = Canvas(W, H, family="sans", size=6.4)
    T = lambda t: H - t                                             # noqa: E731  (top-down millimetres)
    slate = ROLE[STRUCT]

    # ------------------------------------------------ benchmark card (top left)
    LX, LW = 1.0, 51.5
    S.tray(cv, LX, T(1.5), LW, 32.5)
    S.header(cv, LX, T(1.5), LW, 6.2, "GroupAssistBench", size=8.4)
    for k, (kind, num, lab) in enumerate((("groups", "50", "group chats"), ("messages", "80,299", "messages"),
                                          ("instances", "2,395", "instances"))):
        cx = LX + LW * (2 * k + 1) / 6
        stat_glyph(cv, kind, cx, T(13.6))
        cv.text(cx, T(21.4), num, size=10.0, weight="bold", color=slate["ink"])
        cv.text(cx, T(24.9), lab, size=6.4, color=INK)
    cv.ax.plot([LX + 2, LX + LW - 2], [T(27.4)] * 2, color=slate["soft"], lw=0.6, zorder=3)
    S.avatar(cv, "assistant", LX + 5.2, T(30.7), 4.8)
    cv.text(LX + 8.6, T(30.7), "real chats with a deployed assistant", size=6.2, color=slate["ink"], ha="left",
            style="italic")

    # ------------------------------------------------ taxonomy headers
    GX, CW, CG = 14.6, 12.3, 0.5
    cv.text(GX + (3 * CW + 2 * CG) / 2, T(35.9), "memory dependency", size=6.0, color=MUTED, style="italic")
    for k, (code, name) in enumerate(DEPS):
        x0 = GX + k * (CW + CG)
        cv.ax.add_patch(FancyBboxPatch((x0, T(49.3)), CW, 11.9, boxstyle="round,pad=0,rounding_size=1.2",
                                       fc=slate["fill"], ec="none", zorder=1))
        dep_glyph(cv, k, x0 + CW / 2, T(40.2))
        cv.text(x0 + CW / 2, T(43.8), code, size=7.6, weight="bold", color=slate["ink"])
        cv.text(x0 + CW / 2, T(47.0), name, size=6.2, color=INK)
    cv.text(7.8, T(47.0), "task level", size=6.0, color=MUTED, style="italic")

    # ------------------------------------------------ the thread (top right)
    TX, TW, TTOP, TH = 55.0, 122.0, 1.5, 47.4
    S.tray(cv, TX, T(TTOP), TW, TH)
    S.header(cv, TX, T(TTOP), TW, 8.0, "Trip-planning group", "9 members · 2,236 turns · April 15–24", size=8.4)
    ax = TX + TW - 4.4
    S.avatar(cv, "assistant", ax, T(TTOP + 4.0), 5.4)
    cv.text(ax - 5.2, T(TTOP + 4.05), "+4", size=6.4, color=INK, weight="bold")
    for k, who in enumerate(("lin_xi", "jiang_chen", "li_lei", "lu_ye", "zhou_yue")):
        S.avatar(cv, who, ax - 10.2 - k * 5.9, T(TTOP + 4.0), 5.4)
    COLW = 58.5
    cols = (TX + 1.5, TX + TW - 1.5 - COLW)
    for x0, day in zip(cols, ("Apr 15 · the plan is set", "Apr 16 · the plan changes")):
        cv.text(x0 + 0.4, T(TTOP + 10.5), day, size=6.8, weight="bold", color=slate["ink"], ha="left")
        cv.ax.plot([x0, x0 + COLW], [T(TTOP + 12.4)] * 2, color=slate["soft"], lw=0.7, zorder=3)
    cv.text(cols[1] + COLW - 0.4, T(TTOP + 10.5), "235 messages later", size=6.0, color=MUTED, style="italic", ha="right")

    def cut_line(x0, y, mid, r, letter):
        c = ROLE[r]
        lab = f"cut #{mid}"
        tw = S.mono_w(cv, 5.9) * len(lab) + 2.4
        cv.ax.add_patch(FancyBboxPatch((x0, y - 1.3), tw, 2.6, boxstyle="round,pad=0,rounding_size=1.3", fc=c["mark"],
                                       ec="none", zorder=7))
        cv.text(x0 + tw / 2, y - 0.05, lab, size=5.9, color="white", weight="bold", z=8, **MONO)
        cv.line([(x0 + tw + 0.6, y), (x0 + COLW - 4.6, y)], color=c["mark"], lw=0.8, dashed=True)
        S.letter_badge(cv, x0 + COLW - 2.2, y, letter, r, d=3.4)

    y = T(TTOP + 13.6)
    for mid in (34, 35):
        who, text, hl = THREAD[mid]
        y = S.message(cv, cols[0], y, COLW, mid, who, text, hl) - 1.0
    cut_line(cols[0], y - 0.9, 104, L1, "A")
    who, text, hl = THREAD[104]
    S.message(cv, cols[0], y - 2.9, COLW, 104, who, text, hl, r=L1, tag="request of A", fill=ROLE[L1]["fill"])
    y = T(TTOP + 13.6)
    for mid in ("proposal", 342, 363):
        who, text, hl = THREAD[mid]
        y = S.message(cv, cols[1], y, COLW, mid if isinstance(mid, int) else None, who, text, hl) - 1.0
    cut_line(cols[1], y - 0.9, 452, L2, "B")

    # ------------------------------------------------ the two bands: taxonomy row + worked instance
    SX, SW = 57.0, 56.0            # strip
    KX, KW = 117.5, 52.0           # answer-key card
    rail = {}

    def band(top, h, r, code, name, total, letter, hi, title, source, cut, marks, labels, query, who, key_title,
             key_note, rows):
        c = ROLE[r]
        S.tray(cv, 1.0, T(top), W - 2.0, h, r=r, z=1)
        # row tab
        cv.ax.add_patch(FancyBboxPatch((2.0, T(top + h - 1.0)), 11.6, h - 2.0, boxstyle="round,pad=0,rounding_size=1.4",
                                       fc=c["mark"], ec="none", zorder=2))
        ym = T(top + h / 2)
        cv.text(7.8, ym + 5.2, code, size=10.5, weight="bold", color="white")
        cv.text(7.8, ym + 1.2, "memory", size=6.4, color="white")
        cv.text(7.8, ym - 1.5, name, size=6.4, color="white", weight="bold")
        cv.text(7.8, ym - 5.4, total, size=6.4, color="white")
        # cells: one square per cell, area = instances
        for k, n in enumerate(COUNTS[r]):
            x0 = GX + k * (CW + CG)
            on = k == hi
            cv.ax.add_patch(FancyBboxPatch((x0, T(top + h - 1.0)), CW, h - 2.0, boxstyle="round,pad=0,rounding_size=1.2",
                                           fc="white", ec=c["ink"] if on else c["stroke"], lw=1.2 if on else 0.45,
                                           zorder=2))
            s = 9.2 * math.sqrt(n / 776)
            cy = T(top + 1.0 + (h - 2.0 - 4.2) / 2 + 0.4)
            cv.ax.add_patch(FancyBboxPatch((x0 + CW / 2 - s / 2, cy - s / 2), s, s,
                                           boxstyle="round,pad=0,rounding_size=0.5", fc=c["mark"], ec="none", zorder=3))
            cv.text(x0 + CW / 2, T(top + h - 3.3), f"{n:,}", size=7.4, weight="bold", color=c["ink"])
            if on:
                S.letter_badge(cv, x0 + CW - 0.6, T(top + 1.6), letter, r, d=3.6)
        # instance header
        S.letter_badge(cv, 58.6, T(top + 3.0), letter, r, d=4.0)
        ex = S.seg_line(cv, 61.6, T(top + 3.0), [(title, c["ink"], "bold")], size=7.2)
        cv.text(ex + 1.6, T(top + 3.05), source, size=6.0, color=MUTED, style="italic", ha="left")
        # the thread strip with this instance's cut
        sy = T(top + 11.2)
        fx = S.strip(cv, SX, sy, SW, cut=cut, marks=marks, accent=r)
        for mid, text, col, above, wt, ha in labels:
            S.strip_label(cv, fx(mid), sy + (2.4 if above else 0), text, color=col, above=above, weight=wt, ha=ha)
        # the query at the cut
        qy = top + (12.4 if all(a for _, _, _, a, _, _ in labels) else 15.4)
        qw = SW
        chars = int((qw - (6.2 if who else 0) - 2.8) / S.mono_w(cv, 5.9))
        qh = S.n_lines(query, chars) * 5.9 * 0.415 + 1.6
        bx = SX + (6.2 if who else 0)
        cv.solids.append((bx, T(qy + qh), qw - (bx - SX), qh, f"query {letter}", None))
        cv.ax.add_patch(FancyBboxPatch((bx, T(qy + qh)), qw - (bx - SX), qh, boxstyle="round,pad=0,rounding_size=1.1",
                                       fc="white", ec=c["stroke"], lw=0.9, zorder=5))
        if who:
            S.avatar(cv, who, SX + 2.6, T(qy + qh / 2), 5.0)
        S.mono_para(cv, bx + 1.4, T(qy + 0.8), query, chars)
        # answer key
        S.frame(cv, KX, T(top + 1.2), KW, h - 2.4, r=r, radius=1.4, lw=0, z=2)
        cv.text(KX + 1.8, T(top + 3.7), key_title, size=6.9, weight="bold", color=c["ink"], ha="left")
        S.lock_tag(cv, KX + KW - 1.6, T(top + 3.7))
        cv.ax.plot([KX + 1.4, KX + KW - 1.4], [T(top + 5.6)] * 2, color=c["soft"], lw=0.6, zorder=3)
        for k, (kind, segs, mid) in enumerate(rows):
            ry = T(top + 8.0 + k * 3.35)
            S.key_row(cv, KX + 1.8, ry, KW - 3.6, kind, segs, mid)
            rail[(letter, mid)] = ry
        if key_note:
            cv.text(KX + 1.8, T(top + h - 3.2), key_note, size=5.9, color=MUTED, style="italic", ha="left")
        cv.arrow([(SX + SW + 0.4, T(qy + qh / 2)), (KX, T(qy + qh / 2))], color=c["mark"], lw=0.9, head=1.3)

    amber, red, green = ROLE[ANCHOR]["ink"], ROLE[OLD]["ink"], ROLE[CUR]["ink"]
    A_TOP, A_H, B_TOP, B_H = 50.6, 20.4, 73.0, 24.6
    band(A_TOP, A_H, L1, "L1", "recall", "1,374", "A", 1, "L1 × M2", "native request, cut at #104", 104,
         {34: ANCHOR}, [(34, "#34 #35", amber, True, "bold", "center"), (104, "cut #104", ROLE[L1]["ink"], True, "bold", "left")],
         "#104 " + THREAD[104][1], "li_lei", "Reference facts", "Atom Recall: share of the facts recovered",
         [("fact", [("meet at ", INK, "normal"), ("7:30 am on May 1", INK, "normal", ANCHOR)], 34),
          ("fact", [("no-show ", INK, "normal"), ("pays the group ¥500", INK, "normal", ANCHOR)], 35)])
    band(B_TOP, B_H, L2, "L2", "use", "1,021", "B", 2, "L2 × M3", "authored request, cut at #452", 452,
         {34: OLD, 342: CUR, 363: ANCHOR, 372: ANCHOR},
         [(34, "#34", red, True, "bold", "center"), (342, "#342", green, True, "bold", "right"),
          (452, "cut #452", ROLE[L2]["ink"], True, "bold", "right"),
          (363, "#343 #363 #372", amber, False, "bold", "center")],
         "#452 " + S.QUERY_B, None, "Rubric", None,
         [(3, [("Lin Xi wants a ", INK, "normal"), ("window seat", INK, "normal", ANCHOR)], 363),
          (3, [("costs count all nine travellers", INK, "normal")], 372),
          (2, [("leaves on ", INK, "normal"), ("Apr 30", INK, "normal", CUR)], 342),
          (2, [("Chongqing→Chengdu by railway", INK, "normal")], 343),
          (-2, [("answers with the superseded ", INK, "normal"), ("May 1", INK, "normal", OLD)], 34)])
    cv.text(SX + SW, T(A_TOP + 8.0), "later messages: not visible", size=5.9, color=MUTED, style="italic", ha="right")

    # ------------------------------------------------ the claim: A's answer is B's superseded value
    ya, yb, rx = rail[("A", 34)], rail[("B", 34)], KX + KW + 3.6
    cv.arrow([(KX + KW, ya), (rx, ya), (rx, yb), (KX + KW, yb)], color=ROLE[OLD]["mark"], lw=1.1, head=1.5,
             start_dot=True)
    # the label is a chip on the rail, so the band borders it spans pass behind it and not through the words
    cv.text(rx, (ya + yb) / 2, "same fact, now superseded", size=6.0, color=red, style="italic", rotation=90,
            weight="bold", z=30, bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=ROLE[OLD]["mark"], lw=0.6))

    # ------------------------------------------------ key
    def cells(x, y):
        for i, fc in enumerate((slate["soft"], ROLE[L1]["mark"], ROLE[L2]["mark"], "#E4E4E4")):
            cv.ax.add_patch(Rectangle((x - 3.3 + i * 1.7, y - 1.2), 1.5, 2.4, fc=fc, ec="#B9C0CB", lw=0.25, zorder=11))

    S.key(cv, 1.0, 1.0, W - 2.0, [
        (lambda x, y: S.swatch(cv, x, y, ANCHOR), 3.6, "anchor (a required memory)"),
        (lambda x, y: S.swatch(cv, x, y, OLD), 3.6, "superseded value"),
        (lambda x, y: S.swatch(cv, x, y, CUR), 3.6, "current value"),
        (cells, 6.8, "seen history, the cut (L1 / L2), not visible; 10 messages per cell"),
        (lambda x, y: cv.ax.add_patch(Rectangle((x - 1.3, y - 1.3), 2.6, 2.6, fc=slate["mark"], ec="none", zorder=11)),
         2.6, "area = instances"),
    ], frame=False)

    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=".")
    ap.add_argument("--vector-icons", action="store_true", help="draw vector stand-ins instead of the raster avatars")
    a = ap.parse_args()
    print(draw(a.out, a.vector_icons))
