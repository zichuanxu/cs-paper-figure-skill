"""GroupAssistBench Fig. 2: five checked steps from a group thread to an evaluation instance.

Source: Hu, Zhang et al., "One Assistant, Many Memories: Benchmarking Real-World Group Assistance When
Recall Is Not Enough", arXiv:2611.04867v1 (CC BY 4.0), Fig. 2, with Sec. 3.2 (the five steps), Appendix A
(A.2-A.6: how each step works and how many candidates survive it), Appendix B and Table 7 (penalty
criteria and the feedback they come from), Appendix C (human validation).

Kept from the source: the five steps and their sub-steps with who performs each (rules, a language model,
humans); the worked requests #397 (kept) and #343 (dropped) with both answers; the anchor of #342 with
its fact, turn and span and the spans of #342 (found) and #431 (not found); the M1 / M2 / M3 rule and the
conflict pair #34 -> #342 with its three votes; the two instances built from the thread (L1 x M2 from the
native request #104, L2 x M3 from an authored request cut at #452) with their reference facts and rubric
rows; the checks of the gates, the model review and the human validation; the feedback quote #1474 and
the route feedback -> five failure patterns -> penalty criteria; the instance tuple (c, q, A, K) and what
its four letters stand for.

Design (plate register, kept light: no header band, no frame, one panel treatment):
* Message: five checked steps turn one real group thread into evaluation instances, and every step
  filters. The hero is the anchor, the one amber thing in a black, white and slate figure: the cell of
  #342 on the thread, the span it puts into the answer of #397, its record in step 2 (the only outlined,
  tinted card), the units of step 3, the rubric rows of step 4. #342 is the only message id set in bold.
* One row of five numbered steps, read left to right. A step is a plain head on the page (numbered disc
  and name, the count of Appendix A, a bar that shows the share kept) above a pale borderless tray, so
  the row is also the funnel 13,782 -> 7,926 requests, 22,843 anchors, 595 -> 338 pairs, 9,542 instances
  -> 2,395 sampled. Things from the thread and things the pipeline makes are white tiles on the tray.
* The source is the thread itself, the same strip of ten-message cells as in Fig. 1 (render_fig1.py),
  with the requests named above it and the memories below.
* Each sub-step carries one glyph for who does it (gear = rules, sparkle = language model, person =
  humans) and works on a message of that thread. What a step drops is the same drawing in grey.
* Feedback is a side channel, so it is a rail under the row, on the page. Its five failure patterns are
  drawn as rubric rows in waiting (outlined weights); the one this thread triggers is solid and rises
  into the penalty row of instance B that it produces.
* Colour, as in Fig. 1 (ga_style.py): amber = anchor, red = superseded / dropped / penalty, green =
  current / kept. The level colours of Fig. 1 are not used here; structure is slate grey.
* Type: 8.4 pt step names, 6.6 pt labels, 5.8 pt notes and the mono words of the conversation.
  Strokes: 0.6 pt outlines, 1.0 pt arrows and ticks. Arrows: grey = next step, red = feedback.
* Where the source figure departs from the paper's text, the text wins: the steps are numbered 1-5 as in
  Sec. 3.2 (the source leaves "Assign dependency type" unnumbered); "M3" for "D3 pairs"; "three annotators,
  120 instances, 95.8% valid by majority" (Sec. 3.2, Appendix C) for "two annotators, agreement kappa";
  the three votes are a language-model step (the source marks them as rules but prints "Model vote");
  the assistant-message check sits under the model review (A.6), not under the gates; "current at the
  cut" for "least value"; #342 and #34 are both Zhou Yue's, as in Fig. 1 (the source prints User A and
  User B); the span is a verbatim substring of #342 as Fig. 1 prints it.

    python render_fig2.py --out DIR [--vector-icons]
"""
import argparse
import os
import sys

from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import ga_style as S  # noqa: E402
from ga_style import ANCHOR, CUR, INK, MUTED, OLD, ROLE, STRUCT  # noqa: E402
from paperkit import Canvas  # noqa: E402

STEM = "groupassist_fig2_pipeline"
W, H = 178, 103.0
T1, T2, T3 = 8.4, 6.6, 5.8          # step names; labels; notes and the conversation's own words (mono)
LW, AW = 0.6, 1.0                    # outlines and rules; arrows
P = T3 * 0.415                       # mono line pitch (mm)
FUNNEL = dict(points=13782, requests=10191, kept=7926, proposals=22843, rejected=154, pairs=595, accepted=338,
              passed=9542, excluded=440, sampled=2395)                      # Appendix A, Table 2
assert FUNNEL["kept"] == 6772 + 1154
PATTERNS = [("member's current state", -3), ("recalled fact", -2), ("agreement or constraint", -2),
            ("superseded value", -2), ("settled plan", -1)]                 # Table 7
assert 23 + 24 + 21 + 12 + 17 == 97
HOT = "superseded value"            # the pattern this thread triggers


def draw(out, vector=False):
    S.VECTOR = vector
    cv = Canvas(W, H, family="sans", size=T2)
    T = lambda t: H - t                                             # noqa: E731  (top-down millimetres)
    slate, amb, red = ROLE[STRUCT], ROLE[ANCHOR], ROLE[OLD]
    cw = S.mono_w(cv, T3)
    tight = []

    def fits(s, size, w, weight="normal", **kw):
        if cv.text_width(s, size, weight, **kw) > w:
            tight.append(f"'{s}' is {cv.text_width(s, size, weight, **kw):.1f} mm, room {w:.1f}")

    def seg(x, y, segs, size=T2):
        return S.seg_line(cv, x, y, segs, size=size, mono_size=T3)

    def mid_seg(mid):
        """A message id in mono; #342, the anchor the figure follows, is the only bold one."""
        hot = mid == 342
        return (f"#{mid} ", INK if hot else MUTED, "bold" if hot else "normal", None, True)

    def rule(x0, x1, t, color=None):
        cv.ax.plot([x0, x1], [T(t)] * 2, color=color or slate["soft"], lw=LW, zorder=3, solid_capstyle="butt")

    def card(x, t, w, h, fill="white", edge="none", name=""):
        """An object from the thread or made by the pipeline (a message, the anchor record, an instance): a
        white tile on the step's tray, borderless; only the anchor record, the hero, keeps an outline."""
        cv.solids.append((x, T(t + h), w, h, f"card {name}", None))
        cv.ax.add_patch(FancyBboxPatch((x, T(t + h)), w, h, boxstyle="round,pad=0,rounding_size=1.1", fc=fill,
                                       ec=edge, lw=LW, zorder=4))

    # ------------------------------------------------ source: the thread
    for k, who in enumerate(("zhou_yue", "lu_ye", "assistant")):   # a cluster; the vector stand-ins need clear discs
        S.avatar(cv, who, 4.1 + k * (4.9 if vector else 4.0), T(6.4), 4.7 if vector else 6.2, z=12 + k)
    cv.text(17.4, T(4.5), "Group conversations", size=T1, weight="bold", ha="left")
    cv.text(17.4, T(8.5), "50 groups · 80,299 messages", size=T2, ha="left")
    for k, s_ in enumerate(("de-identified, real-world", "everyday settings", "Chinese + English translation")):
        cv.text(52.0, T(3.6 + k * 2.8), s_, size=T3, color=MUTED, ha="left")
    cv.text(86.0, T(3.6), "Trip-planning group", size=T2, ha="left")
    cv.text(86.0, T(6.5), "2,236 turns", size=T2, ha="left")
    cv.text(86.0, T(9.3), "10 messages per cell", size=T3, color=MUTED, style="italic", ha="left")
    SX, SW = 121.0, 56.0
    sy = T(7.7)
    fx = S.strip(cv, SX, sy, SW, marks={34: ANCHOR, 326: ANCHOR, 342: ANCHOR, 363: ANCHOR, 104: STRUCT, 397: STRUCT,
                                        452: STRUCT})
    for mid in (104, 343, 397, 452):                                # #343 is the request that step 1 drops
        S.strip_label(cv, fx(mid), sy + 2.4, f"#{mid}", color=MUTED if mid == 343 else INK, size=T3)
    S.strip_label(cv, fx(34), sy, "#34 #35", color=amb["ink"], above=False, size=T3)
    for mid in (326, 363):
        cv.ax.plot([fx(mid)] * 2, [sy, sy - 1.0], color=amb["ink"], lw=LW, zorder=7)
    S.strip_label(cv, fx(342), sy, "#326 #342 #363", color=amb["ink"], above=False, size=T3)
    cv.text(SX - 1.4, sy + 4.55, "requests", size=T3, color=MUTED, style="italic", ha="right")
    cv.text(SX - 1.4, sy - 2.15, "memories", size=T3, color=amb["ink"], style="italic", ha="right")

    # ------------------------------------------------ the five steps: number, name, count, share kept
    COL_T, PAD, GAP, EDGE = 13.2, 1.3, 0.8, 0.9       # trays: inner padding, white gap between two, outer margin
    GUT = 2 * PAD + GAP
    widths = [40.4, 33.6, 24.5, 35.3, 26.2]
    xs = [EDGE + PAD]
    for w in widths[:-1]:
        xs.append(xs[-1] + w + GUT)
    assert abs(xs[-1] + widths[-1] - (W - EDGE - PAD)) < 1e-6
    names = ["Locate requests", "Anchor memories", "Assign type", "Build instances", "Quality control"]
    outs = [f"{FUNNEL['points']:,} candidates → {FUNNEL['kept']:,} kept",
            f"{FUNNEL['proposals']:,} anchors, {FUNNEL['rejected']} rejected",
            f"{FUNNEL['pairs']} pairs → {FUNNEL['accepted']} kept",
            "instance (c, q, A, K)",
            f"{FUNNEL['passed']:,} pass, {FUNNEL['excluded']} fail"]
    shares = [(FUNNEL["kept"], FUNNEL["points"] - FUNNEL["kept"]),          # (kept, dropped) at this step
              (FUNNEL["proposals"] - FUNNEL["rejected"], FUNNEL["rejected"]),
              (FUNNEL["accepted"], FUNNEL["pairs"] - FUNNEL["accepted"]),
              None,
              (FUNNEL["passed"], FUNNEL["excluded"])]
    cv.arrow([(EDGE + 2.3, T(10.1)), (EDGE + 2.3, T(COL_T))], color=slate["stroke"], lw=AW, head=1.5)
    for k, (x0, w) in enumerate(zip(xs, widths)):                   # a plain head above each tray, as wide as the tray
        hx, hw = x0 - PAD, w + 2 * PAD
        y = T(COL_T + 2.3)
        cv.ax.add_patch(Circle((hx + 2.3, y), 2.3, fc=slate["ink"], ec="none", zorder=5))
        cv.text(hx + 2.3, y - 0.05, str(k + 1), size=T1, weight="bold", color="white", z=6)
        fits(names[k], T1, hw - 5.7 - (4.2 if k < 4 else 0), "bold")
        cv.text(hx + 5.7, y - 0.05, names[k], size=T1, weight="bold", ha="left")
        fits(outs[k], T2, hw)
        cv.text(hx, T(COL_T + 7.0), outs[k], size=T2, ha="left", style="normal" if shares[k] else "italic")
        by, bh = T(COL_T + 9.9), 0.9
        if shares[k]:
            f = shares[k][0] / sum(shares[k])
            cv.ax.add_patch(Rectangle((hx, by), hw * f, bh, fc=slate["stroke"], ec="none", zorder=3))
            cv.ax.add_patch(Rectangle((hx + hw * f, by), hw * (1 - f), bh, fc=red["soft"], ec="none", zorder=3))
        else:
            rule(hx, hx + hw, COL_T + 9.9 - bh / 2, slate["soft"])
        if k:
            cv.arrow([(hx - GAP - 2.6, y), (hx - 0.1, y)], color=slate["stroke"], lw=AW, head=1.5)
    BT = COL_T + 12.6                                               # top of the step bodies

    def substep(x0, t, letter, doer, label, w):
        """'a [doer glyph] Label': who does this sub-step. label is a string or seg_line segments."""
        y = T(t + 1.5)
        cv.text(x0, y, letter, size=T2, weight="bold", color=MUTED, ha="left")
        S.DOER[doer](cv, x0 + 3.9, y, 2.5, color=slate["ink"])
        ex = seg(x0 + 5.8, y, [(label, INK, "normal")] if isinstance(label, str) else label)
        if ex > x0 + w + 0.05:
            tight.append(f"sub-step {letter} of the column at {x0} ends at {ex:.1f}, edge {x0 + w:.1f}")
        return t + 3.4

    ends = []
    G = [3.8, 2.8, 7.6, 1.4, 2.0]                                   # the group gap of each column

    # ---- 1 Locate requests
    x0, w = xs[0], widths[0]
    t = substep(x0, BT, "a", "rule", "Enumerate candidate requests", w)
    t = substep(x0, t, "b", "model", "Answer with and without history", w)

    def request(t, query, yp, ym, hl, ok, note):
        """One candidate request (a white message bubble) with both answers; the dropped one is the same
        drawing in grey."""
        col = INK if ok else MUTED
        ch, ch2 = int((w - 2.0) / cw), int((w - 1.0 - 7.8) / cw)
        qh = S.n_lines(query, ch) * P + 1.4
        card(x0, t, w, qh, name=query[:4])
        S.mono_para(cv, x0 + 1.0, T(t + 0.7), query, ch, size=T3, color=col, weight="bold")
        y = T(t + qh + 0.3)
        for how, txt, hh in (("with", yp, hl), ("without", ym, ())):
            assert S.n_lines(txt, ch2) == 2, (txt, ch2)
            cv.text(x0 + 1.0, y - 0.5 - P / 2, how, size=T3, color=MUTED, style="italic", ha="left")
            y = S.mono_para(cv, x0 + 1.0 + 7.8, y - 0.5, txt, ch2, size=T3, hl=hh, color=col)
        vy = y - 2.5
        S.verdict(cv, x0 + w, vy, ok, "keep" if ok else "drop", ha="right", size=T2)
        cv.text(x0 + 1.0, vy, note, size=T3, color=MUTED, style="italic", ha="left")
        return H - vy + 1.5

    t = request(t + 1.2, "#397 @Agent check when we can start booking tickets",
                "You have an Apr 30 train and start watching…", "Please confirm the booking time…",
                [("Apr 30 train", ANCHOR)], True, "history changes the answer")
    t = request(t + G[0], "#343 @Agent check the rail fare from Chongqing to Chengdu…",
                "About ¥100–200 for second class; check 12306.", "About ¥100–200 for second class, …",
                (), False, "same answer without it")
    ends.append(t)

    # ---- 2 Anchor memories
    x0, w = xs[1], widths[1]
    t = substep(x0, BT, "a", "model", "Extract memories", w)
    seg(x0 + 5.8, T(t + 1.0), [("for request ", MUTED, "normal"), ("#397", INK, "normal", None, True)], size=T3)
    t += 3.9
    rec_t = t
    kx, vx = x0 + 1.4, x0 + 7.4
    cv.text(kx, T(t + 2.0), "anchor", size=T2, weight="bold", color=amb["ink"], ha="left", z=21)
    cv.text(x0 + w - 1.4, T(t + 2.0), "a = (f, t, e)", size=T2, color=amb["ink"], style="italic", ha="right", z=21)
    rule(x0 + 1.0, x0 + w - 1.0, t + 3.9, amb["soft"])
    cv.text(kx, T(t + 5.9), "fact", size=T3, color=amb["ink"], ha="left")
    yb = S.sans_para(cv, vx, T(t + 4.6), "departure moved to Apr 30", 22.0, size=T2)
    t = H - yb + 0.7
    cv.text(kx, T(t + 1.5), "turn", size=T3, color=amb["ink"], ha="left")
    seg(vx, T(t + 1.5), [mid_seg(342), ("Zhou Yue", INK, "normal")])
    S.avatar(cv, "zhou_yue", x0 + w - 3.3, T(t + 1.5), 4.0)
    t += 3.6
    span = "“we leave on Apr 30”"
    assert vx + len(span) * cw <= x0 + w - 1.0, "the span leaves the anchor record"
    cv.text(kx, T(t + 1.5), "span", size=T3, color=amb["ink"], ha="left")
    S.mono_para(cv, vx, T(t + 1.5) + P / 2, span, len(span), size=T3, hl=[(span, ANCHOR)])
    t += 3.9
    card(x0, rec_t, w, t - rec_t, fill=amb["fill"], edge=amb["stroke"], name="anchor")
    t += 2.4
    for mid, s in ((34, "meet 7:30 am, May 1"), (326, "rail both ways")):          # the request's other anchors
        cv.ax.add_patch(FancyBboxPatch((x0 + 1.4, T(t + 2.6)), 2.2, 2.2, boxstyle="round,pad=0,rounding_size=0.5",
                                       fc=S.HL[ANCHOR], ec=amb["stroke"], lw=LW, zorder=5))
        seg(x0 + 4.8, T(t + 1.5), [mid_seg(mid), (s, INK, "normal")])
        t += 3.2
    t = substep(x0, t + G[1], "b", "rule", "Verify evidence spans", w)
    for mid, s, ok in ((342, "verbatim", True), (431, "not found", False)):
        seg(x0 + 1.4, T(t + 1.7), [mid_seg(mid), (s, INK if ok else MUTED, "normal")])
        S.verdict(cv, x0 + w, T(t + 1.7), ok, "keep" if ok else "drop", ha="right", size=T2)
        t += 4.0
    t = H - S.sans_para(cv, x0 + 1.4, T(t + 1.1), "Verified anchors go to a per-group inventory.", w - 1.4, size=T3,
                        color=MUTED, style="italic")
    ends.append(t)

    # ---- 3 Assign dependency type
    x0, w = xs[2], widths[2]
    t = substep(x0, BT, "a", "rule", "Count units", w)

    def unit(px, py):
        cv.ax.add_patch(FancyBboxPatch((px - 1.4, py - 1.0), 2.8, 2.0, boxstyle="round,pad=0,rounding_size=0.45",
                                       fc=S.HL[ANCHOR], ec=amb["stroke"], lw=LW, zorder=6))

    for code, n, lab in (("M1", 1, "one memory unit"), ("M2", 2, "two or more")):
        cv.text(x0 + 1.4, T(t + 1.6), code, size=T2, weight="bold", ha="left")
        for j in range(n):
            unit(x0 + 8.0 + j * 3.3, T(t + 1.6))
        fits(lab, T3, w - 1.4)
        cv.text(x0 + 1.4, T(t + 4.4), lab, size=T3, color=MUTED, ha="left")
        t += G[2]
    # the M3 branch: its sub-steps work on a verified conflict pair only, so they share one dashed scope
    t += 0.9
    m3_t = t
    cv.text(x0 + 1.4, T(t + 2.2), "M3", size=T2, weight="bold", ha="left")
    fits("M2 + conflict pair", T3, w - 6.6 - 1.0)
    cv.text(x0 + 6.6, T(t + 2.2), "M2 + conflict pair", size=T3, color=MUTED, ha="left")
    t += 4.8
    for mid, val, r, struck in ((34, "May 1", OLD, True), (342, "Apr 30", CUR, False)):
        ex = seg(x0 + 1.4, T(t + 1.5), [mid_seg(mid), (val, INK, "normal", r)])
        if struck:
            cv.ax.plot([ex - cv.text_width(val, T2) - 0.2, ex + 0.2], [T(t + 1.5)] * 2, color=red["ink"], lw=LW,
                       zorder=22)
        cv.text(x0 + w - 1.2, T(t + 1.5), "old" if struck else "new", size=T3, color=ROLE[r]["ink"], style="italic",
                ha="right")
        t += 3.9
    t = substep(x0 + 1.4, t + 1.5, "b", "rule", "Detect updates", w - 2.4)
    t = substep(x0 + 1.4, t + 0.5, "c", "model", "Three votes", w - 2.4)
    cv.text(x0 + 1.4, T(t + 0.9), "same matter?", size=T3, color=MUTED, ha="left")
    for j in range(3):
        S.tick(cv, x0 + 1.4 + cv.text_width("same matter?", T3) + 2.2 + j * 2.5, T(t + 0.9), True, s=1.7)
    t += 3.5
    t = substep(x0 + 1.4, t + 0.5, "d", "rule", "Current at cut", w - 2.4)
    t = H - S.sans_para(cv, x0 + 1.4, T(t - 0.3), "if not, the cut moves before the next change", w - 2.6, size=T3,
                        color=MUTED, style="italic")
    t += 1.3
    cv.ax.add_patch(FancyBboxPatch((x0, T(t)), w, t - m3_t, boxstyle="round,pad=0,rounding_size=1.1", fc="none",
                                   ec=slate["stroke"], lw=LW, ls=(0, (3, 2)), zorder=2))
    ends.append(t)

    # ---- 4 Build instances
    x0, w = xs[3], widths[3]
    t = BT
    for letter, doer, lab in (("a", "model", "Write authored queries"), ("b", "model", "Derive facts, grounding"),
                              ("c", "rule", "Trigger penalties"), ("d", "model", "Propose service criteria")):
        t = substep(x0, t, letter, doer, lab, w)

    def weight_chip(x, y, wt, solid=True, z=9):
        r = ROLE[CUR if wt > 0 else OLD]
        cv.ax.add_patch(FancyBboxPatch((x, y - 1.3), 4.3, 2.6, boxstyle="round,pad=0,rounding_size=0.6",
                                       fc=r["mark"] if solid else "white", ec=r["mark"], lw=LW, zorder=z))
        cv.text(x + 2.15, y - 0.05, f"{'+' if wt > 0 else '−'}{abs(wt)}", size=T3, weight="bold",
                color="white" if solid else r["ink"], z=z + 1)

    def key_row(x, y, wd, kind, segs, mid):
        """One line of an answer key: a ticked reference fact, or a rubric criterion with its signed weight."""
        if kind == "fact":
            cv.ax.add_patch(FancyBboxPatch((x, y - 1.2), 2.4, 2.4, boxstyle="round,pad=0,rounding_size=0.5",
                                           fc=S.HL[ANCHOR], ec=amb["stroke"], lw=LW, zorder=9))
            cv.icon_check(x + 1.2, y, 1.5, color=amb["ink"], lw=AW, z=10)
            tx = x + 3.5
        else:
            weight_chip(x, y, kind)
            tx = x + 5.3
        ex = seg(tx, y, segs)
        mx = x + wd - len(f"#{mid}") * cw
        if ex > mx - 0.6:
            tight.append(f"key row #{mid}: text ends at {ex:.1f}, id starts at {mx:.1f}")
        seg(mx, y, [(f"#{mid}", INK if mid == 342 else MUTED, "bold" if mid == 342 else "normal", None, True)])

    def instance(t, letter, title, source, query, who, rows):
        ax_ = 5.2 if who else 0.0
        ch = int((w - 2.4 - ax_) / cw)
        nq = S.n_lines(query, ch)
        h = 4.6 + max(nq * P, 4.4 if who else 0) + 1.2 + len(rows) * 3.3 + 0.5
        card(x0, t, w, h, name=letter)
        cv.ax.add_patch(Circle((x0 + 2.7, T(t + 2.5)), 1.8, fc=slate["ink"], ec="none", zorder=12))
        cv.text(x0 + 2.7, T(t + 2.55), letter, size=T2, color="white", weight="bold", z=13)
        ex = seg(x0 + 5.3, T(t + 2.5), [(title, INK, "bold")])
        cv.text(ex + 1.2, T(t + 2.5), source, size=T3, color=MUTED, style="italic", ha="left")
        cv.icon_lock(x0 + w - 2.3, T(t + 2.4), 2.0, color=MUTED)
        qh = max(nq * P, 4.4 if who else 0)
        if who:
            S.avatar(cv, who, x0 + 3.4, T(t + 4.6 + qh / 2), 4.2)
        S.mono_para(cv, x0 + 1.2 + ax_, T(t + 4.6 + (qh - nq * P) / 2), query, ch, size=T3)
        rule(x0 + 1.0, x0 + w - 1.0, t + 4.6 + qh + 0.5)
        for k, (kind, segs, mid) in enumerate(rows):
            key_row(x0 + 1.2, T(t + 4.6 + qh + 1.2 + 1.5 + k * 3.3), w - 2.4, kind, segs, mid)
        return t + h

    t = instance(t + 0.4, "A", "L1 × M2", "native", "#104 @Agent on departure day, remind…", "li_lei",
                 [("fact", [("meet ", INK, "normal"), ("7:30 am, May 1", INK, "normal", ANCHOR)], 34),
                  ("fact", [("no-show ", INK, "normal"), ("pays ¥500", INK, "normal", ANCHOR)], 35)])
    t = instance(t + G[3], "B", "L2 × M3", "authored", "#452 @Agent Post a reminder…", None,
                 [(3, [("window seat", INK, "normal", ANCHOR)], 363),
                  (2, [("leaves ", INK, "normal"), ("Apr 30", INK, "normal", CUR)], 342),
                  (-2, [("uses old ", INK, "normal"), ("May 1", INK, "normal", OLD)], 34)])
    b_bottom = t
    ends.append(b_bottom)

    # ---- 5 Quality control
    x0, w = xs[4], widths[4]

    def checks(t, items):
        for s in items:
            cv.icon_check(x0 + 2.2, T(t + 1.25), 1.6, color=slate["ink"], lw=AW)
            t = H - S.sans_para(cv, x0 + 4.2, T(t), s, w - 4.2, size=T3) + 0.7
        return t + G[4]

    t = substep(x0, BT, "a", "rule", "Rule gates", w)
    t = checks(t, ["anchors precede the cut", "spans found verbatim", "query gives no cue of a change"])
    t = substep(x0, t, "b", "model", "Model review", w)
    t = checks(t, ["each anchor is necessary", "query not answerable from its own wording",
                   "assistant turns only relay a member's fact", "M3 values concern one matter"])
    t = substep(x0, t, "c", "human", "Human validation", w)
    t = H - S.sans_para(cv, x0 + 1.4, T(t), "3 annotators, 120 instances: 95.8% valid by majority", w - 1.4, size=T3)
    ends.append(t)
    BOT = max(ends)
    for x0, w in zip(xs, widths):                                   # the step's tray: a pale field, no frame
        S.tray(cv, x0 - PAD, T(BT - 1.4), w + 2 * PAD, BOT + PAD - (BT - 1.4))
    assert BOT - min(ends) < 0.5, f"uneven columns: {[round(e - BT, 1) for e in ends]}"

    # ------------------------------------------------ feedback rail -> the penalty row it produces
    LT = BOT + PAD + 2.4
    LX = EDGE
    cv.text(LX, T(LT + 1.5), "Penalty criteria from real feedback", size=T2, weight="bold", color=red["ink"], ha="left")
    quote = "#1474 “I asked you to keep the memo. How is it mixed up again?”"
    qch = 32
    assert S.n_lines(quote, qch) == 2
    S.person(cv, LX + 1.4, T(LT + 6.5), 2.8, color=red["stroke"])
    cv.ax.add_patch(FancyBboxPatch((LX + 3.4, T(LT + 9.2)), qch * cw + 2.0, 5.4, fc=slate["fill"], ec="none",
                                   boxstyle="round,pad=0,rounding_size=1.1", zorder=2))
    S.mono_para(cv, LX + 4.4, T(LT + 4.1), quote, qch, size=T3)
    seg(LX, T(LT + 11.6), [("423 negative reactions, ", INK, "normal"), ("97 corrections", INK, "bold")])
    px0, px1 = 53.0, xs[3] + widths[3]
    hx = xs[3] + 1.2                                                # under the weight column of instance B
    cv.arrow([(LX + 3.4 + qch * cw + 2.0 + 1.0, T(LT + 6.5)), (px0 - 1.2, T(LT + 6.5))], color=red["mark"], lw=AW, head=1.5)

    def pattern(x, y, name, wt, on=False):
        """A failure pattern drawn as a rubric row in waiting: outlined weight; solid for the one triggered here."""
        size = T2 if on else T3
        tw = 5.3 + cv.text_width(name, size, "bold" if on else "normal")
        cv.chips.append((x, y - 1.6, tw, 3.2, name, (px0 - 0.1, T(LT + 12.4), px1 + 0.1, T(LT + 2.6))))
        weight_chip(x, y, wt, solid=on)
        cv.text(x + 5.3, y, name, size=size, ha="left", weight="bold" if on else "normal")
        return x + tw

    y1, y2 = T(LT + 4.6), T(LT + 9.2)
    cv.text(px0, y1, "five failure patterns, each with its weight", size=T3, color=MUTED, style="italic", ha="left")
    hot = next(p for p in PATTERNS if p[0] == HOT)
    pattern(hx, y1, *hot, on=True)
    x = px0
    for name, wt in (PATTERNS[1], PATTERNS[4], PATTERNS[2], PATTERNS[0]):
        x = pattern(x, y2, name, wt) + 2.6
    assert x - 2.6 <= px1, f"pattern rows leave the rail by {x - 2.6 - px1:.1f} mm"
    cv.arrow([(hx + 2.15, y1 + 1.3), (hx + 2.15, T(b_bottom))], color=red["mark"], lw=AW, head=1.5)

    # ------------------------------------------------ output
    x0, w = xs[4] - PAD, widths[4] + 2 * PAD
    cv.arrow([(x0 + 2.3, T(ends[4] + 1.2)), (x0 + 2.3, T(LT + 0.1))], color=slate["stroke"], lw=AW, head=1.5)
    cv.text(x0 + 5.7, T(LT + 2.3), "Evaluation set", size=T1, weight="bold", ha="left")
    for k in (2, 1, 0):                                             # a stack of cards: many instances
        cv.ax.add_patch(FancyBboxPatch((x0 + 0.3 + k * 0.7, T(LT + 3.9) + k * 0.7), 3.2, 2.6,
                                       boxstyle="round,pad=0,rounding_size=0.5", fc="white", ec=slate["ink"], lw=LW,
                                       zorder=5 - k * 0.1))
    seg(x0 + 5.7, T(LT + 6.8), [(f"{FUNNEL['sampled']:,}", INK, "bold"), (" instances", INK, "normal")])
    cv.text(x0 + 5.7, T(LT + 9.8), f"sampled from the {FUNNEL['passed']:,}", size=T3, color=MUTED, style="italic",
            ha="left")

    # ------------------------------------------------ key
    def share(x, y):
        cv.ax.add_patch(Rectangle((x - 2.7, y - 0.45), 3.6, 0.9, fc=slate["stroke"], ec="none", zorder=11))
        cv.ax.add_patch(Rectangle((x + 0.9, y - 0.45), 1.8, 0.9, fc=red["soft"], ec="none", zorder=11))

    KT = LT + 14.2
    S.key(cv, EDGE, T(KT + 4.6), W - 2 * EDGE, [
        (lambda x, y: S.gear(cv, x, y, 2.5, color=slate["ink"]), 2.5, "rules"),
        (lambda x, y: S.sparkle(cv, x, y, 2.5, color=slate["ink"]), 2.5, "language model"),
        (lambda x, y: S.person(cv, x, y, 2.5, color=slate["ink"]), 2.5, "humans"),
        (share, 5.4, "kept / dropped"),
        (lambda x, y: S.swatch(cv, x, y, ANCHOR), 3.6, "anchor = required memory"),
        (lambda x, y: cv.icon_lock(x, y, 2.0, color=MUTED), 2.0, "judge only"),
        (lambda x, y: cv.text(x, y, "(c, q, A, K)", size=T3, style="italic", z=12), cv.text_width("(c, q, A, K)", T3,
                                                                                               style="italic"),
         "cutoff, query, required memories, answer key"),
    ], h=4.6, size=T3, frame=False)
    assert abs(KT + 4.6 + 0.6 - H) < 0.8, f"canvas height should be {KT + 5.2:.1f}"

    assert not tight, tight
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
