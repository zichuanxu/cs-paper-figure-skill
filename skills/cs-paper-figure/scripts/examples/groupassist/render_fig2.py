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
the route feedback -> five failure patterns -> penalty criteria; the instance tuple (c, q, A, K).

Design:
* One row of five numbered step columns, read left to right; a solid header names the step and the line
  under it gives what comes out, with the counts of Appendix A, so the row is also the funnel
  13,782 -> 7,926 requests, 22,843 anchors, 595 -> 338 pairs, 9,542 instances -> 2,395 sampled.
* The source is the thread itself, drawn as the same strip of ten-message cells as in Fig. 1
  (render_fig1.py), with the requests named above it and the anchors below. Every step then works on
  messages of that one thread, so the reader can follow #342 from the strip through the anchor record,
  the conflict pair and the rubric to the gate that checks it.
* Each sub-step carries one glyph for who does it (gear = rules, sparkle = language model, person =
  humans) and a data object: two answers side by side in monospace, the anchor record, chips for memory
  units, instance cards with key rows, check lists.
* Feedback is a side channel, so it is a rail under the row that enters step 4 at the penalty row it
  produces; the M3 branch stays inside step 3, where the pair is verified.
* Colour as in Fig. 1 (ga_style.py): amber = anchor, red = superseded / dropped / penalty, green =
  current / kept, blue = L1, purple = L2, slate = the benchmark's own structure.
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

from matplotlib.patches import Circle, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import ga_style as S  # noqa: E402
from ga_style import ANCHOR, CUR, INK, L1, L2, MUTED, OLD, ROLE, STRUCT  # noqa: E402
from paperkit import Canvas  # noqa: E402

STEM = "groupassist_fig2_pipeline"
W, H = 178, 114.1
P = 5.9 * 0.415                      # mono line pitch (mm)
FUNNEL = dict(points=13782, requests=10191, kept=7926, proposals=22843, rejected=154, pairs=595, accepted=338,
              passed=9542, excluded=440, sampled=2395)                      # Appendix A, Table 2
assert FUNNEL["kept"] == 6772 + 1154
PATTERNS = [("member's current state", -3), ("recalled fact", -2), ("agreement or constraint", -2),
            ("superseded value", -2), ("settled plan", -1)]                 # Table 7
assert 23 + 24 + 21 + 12 + 17 == 97


def draw(out, vector=False):
    S.VECTOR = vector
    cv = Canvas(W, H, family="sans", size=6.3)
    T = lambda t: H - t                                             # noqa: E731  (top-down millimetres)
    slate = ROLE[STRUCT]
    cw = S.mono_w(cv, 5.9)

    tight = []

    def fits(s, size, w, weight="normal"):
        if cv.text_width(s, size, weight) > w:
            tight.append(f"'{s}' is {cv.text_width(s, size, weight):.1f} mm, room {w:.1f}")

    # ------------------------------------------------ source: the thread
    S.frame(cv, 1.0, T(1.5), W - 2.0, 12.4)
    cv.ax.add_patch(FancyBboxPatch((1.0, T(13.9)), 50.0, 12.4, boxstyle="round,pad=0,rounding_size=1.8", fc=S.SLATE,
                                   ec="none", zorder=2))
    for k, who in enumerate(("zhou_yue", "lu_ye", "assistant")):   # a cluster; the vector stand-ins need clear discs
        S.avatar(cv, who, 5.8 + k * (4.9 if vector else 4.0), T(7.7), 4.7 if vector else 6.2, z=12 + k)
    cv.text(19.6, T(5.6), "Group conversations", size=7.6, weight="bold", color="white", ha="left")
    cv.text(19.6, T(9.7), "50 groups · 80,299 messages", size=6.0, color="#D5DCE8", ha="left")
    SX, SW = 89.0, 53.0
    cv.text(53.4, T(4.9), "Trip-planning group", size=6.6, weight="bold", color=slate["ink"], ha="left")
    cv.text(53.4, T(7.9), "2,236 turns", size=6.0, color=INK, ha="left")
    cv.text(53.4, T(10.8), "10 messages per cell", size=5.8, color=MUTED, style="italic", ha="left")
    sy = T(9.0)
    fx = S.strip(cv, SX, sy, SW, marks={34: ANCHOR, 326: ANCHOR, 342: ANCHOR, 363: ANCHOR, 104: STRUCT, 397: STRUCT,
                                        452: STRUCT})
    for mid, lab, ha in ((104, "#104", "center"), (343, "#343", "right"), (397, "#397", "center"), (452, "#452", "center")):
        S.strip_label(cv, fx(mid), sy + 2.4, lab, color=slate["ink"], weight="bold", ha=ha)
    amber = ROLE[ANCHOR]["ink"]
    S.strip_label(cv, fx(34), sy, "#34 #35", color=amber, above=False, weight="bold")
    for mid in (326, 363):
        cv.ax.plot([fx(mid)] * 2, [sy, sy - 1.0], color=amber, lw=0.5, zorder=7)
    S.strip_label(cv, fx(342), sy, "#326 #342 #363", color=amber, above=False, weight="bold")
    cv.text(SX - 1.4, sy + 3.55, "requests", size=5.8, color=slate["ink"], style="italic", ha="right")
    cv.text(SX - 1.4, sy - 2.15, "memories", size=5.8, color=amber, style="italic", ha="right")
    for k, s_ in enumerate(("de-identified, real-world", "everyday settings", "Chinese + English translation")):
        cv.ax.add_patch(Circle((145.6, T(4.5 + k * 3.2)), 0.38, fc=slate["stroke"], ec="none", zorder=5))
        cv.text(146.8, T(4.5 + k * 3.2), s_, size=6.0, color=INK, ha="left")
    cv.block_arrow(23.0, T(14.3), 23.0, T(17.9), width=3.6, color=slate["stroke"], head=2.2)

    # ------------------------------------------------ the five step columns
    PT, PH, GUT = 18.2, 67.5, 2.3
    widths = [44.4, 33.0, 27.0, 34.8, 27.6]
    xs = [1.0]
    for w in widths[:-1]:
        xs.append(xs[-1] + w + GUT)
    assert abs(xs[-1] + widths[-1] - (W - 1.0)) < 1e-6
    names = ["Locate requests", "Anchor memories", "Assign type", "Build instances", "Quality control"]
    outs = [f"{FUNNEL['points']:,} candidates → {FUNNEL['kept']:,} kept",
            f"{FUNNEL['proposals']:,} anchors, {FUNNEL['rejected']} rejected",
            f"{FUNNEL['pairs']} pairs → {FUNNEL['accepted']} kept",
            "instance (c, q, A, K)",
            f"{FUNNEL['passed']:,} pass, {FUNNEL['excluded']} fail"]
    for k, (x0, w) in enumerate(zip(xs, widths)):
        S.frame(cv, x0, T(PT), w, PH)
        S.header(cv, x0, T(PT), w, 6.0, names[k], size=7.4, tx=x0 + 6.6)
        cv.ax.add_patch(Circle((x0 + 3.6, T(PT + 3.0)), 1.9, fc="white", ec="none", zorder=5))
        cv.text(x0 + 3.6, T(PT + 3.05), str(k + 1), size=7.4, weight="bold", color=S.SLATE, z=6)
        fits(outs[k], 6.0, w - 2.6)
        cv.text(x0 + w / 2, T(PT + 8.1), outs[k], size=6.0, color=slate["ink"], style="italic")
        cv.ax.plot([x0 + 1.3, x0 + w - 1.3], [T(PT + 10.0)] * 2, color=slate["soft"], lw=0.6, zorder=3)
        if k:
            cv.arrow([(x0 - GUT, T(PT + 3.0)), (x0, T(PT + 3.0))], color=S.SLATE, lw=1.3, head=1.7)
    BOT = PT + PH

    def substep(x0, w, t, letter, doer, label):
        """'a [doer glyph] Label': who does this sub-step. Returns the next top."""
        fits(label, 6.3, w - 3.0 - 5.9, "bold")
        cv.text(x0 + 1.8, T(t + 1.6), letter, size=6.3, weight="bold", color=MUTED, ha="left")
        S.DOER[doer](cv, x0 + 5.0, T(t + 1.6), 2.5, color=slate["ink"])
        cv.text(x0 + 6.9, T(t + 1.6), label, size=6.3, weight="bold", color=slate["ink"], ha="left")
        return t + 3.7

    def card(x, t, w, h, r=STRUCT, fill="white", lw=0.5, name=""):
        c = ROLE[r]
        cv.solids.append((x, T(t + h), w, h, f"card {name}", None))
        cv.ax.add_patch(FancyBboxPatch((x, T(t + h)), w, h, boxstyle="round,pad=0,rounding_size=1.1", fc=fill,
                                       ec=c["stroke"], lw=lw, zorder=4))

    # ---- 1 Locate requests
    x0, w = xs[0], widths[0]
    t = substep(x0, w, PT + 11.0, "a", "rule", "Enumerate candidate requests")
    t = substep(x0, w, t, "b", "model", "Answer with and without history")

    def request(t, mid, query, yp, ym, hl, ok, note):
        cx, cwd = x0 + 1.5, w - 3.0
        ch, ch2 = int((cwd - 2.4) / cw), int((cwd - 2.4 - 5.2) / cw)
        nq, n1, n2 = S.n_lines(query, ch), S.n_lines(yp, ch2), S.n_lines(ym, ch2)
        h = 1.0 + nq * P + 1.0 + n1 * P + 0.6 + n2 * P + 0.9 + 3.2 + 0.8
        card(cx, t, cwd, h, name=f"#{mid}")
        y = S.mono_para(cv, cx + 1.2, T(t + 1.0), query, ch, weight="bold", color=slate["ink"])
        cv.ax.plot([cx + 1.0, cx + cwd - 1.0], [y - 0.5] * 2, color=slate["soft"], lw=0.6, zorder=5)
        for sym, txt, hh in ((r"$\hat{y}^{+}$", yp, hl), (r"$\hat{y}^{-}$", ym, ())):
            cv.text(cx + 1.2, y - 1.0 - P / 2, sym, size=6.6, color=slate["ink"], ha="left")
            y = S.mono_para(cv, cx + 1.2 + 5.2, y - 1.0, txt, ch2, hl=hh) + 0.4
        vy = T(t + h - 2.4)
        S.verdict(cv, cx + cwd - 1.2, vy, ok, "keep" if ok else "drop", ha="right")
        cv.text(cx + 1.2, vy, note, size=5.9, color=MUTED, style="italic", ha="left")
        return t + h + 1.2

    t = request(t, 397, "#397 @Agent check when we can start booking tickets",
                "You have an Apr 30 train and start watching…", "Please confirm the booking time…",
                [("Apr 30 train", ANCHOR)], True, "history changes the answer")
    t = request(t, 343, "#343 @Agent check the rail fare from Chongqing to Chengdu…",
                "About ¥100–200 for second class; check 12306.", "About ¥100–200 for second class, …",
                (), False, "same answer without it")
    assert t - 1.2 <= BOT - 1.0, t

    # ---- 2 Anchor memories
    x0, w = xs[1], widths[1]
    cx, cwd = x0 + 1.5, w - 3.0
    t = substep(x0, w, PT + 11.0, "a", "model", "Extract memories")
    S.seg_line(cv, cx + 0.4, T(t + 1.2), [("for request ", MUTED, "normal"), ("#397", slate["ink"], "bold", None, True)],
               size=6.0)
    t += 3.2
    ac = ROLE[ANCHOR]
    card(cx, t, cwd, 20.4, r=ANCHOR, fill=ac["fill"], lw=0.8, name="anchor")
    cv.text(cx + 1.4, T(t + 2.0), "anchor", size=6.4, weight="bold", color=ac["ink"], ha="left")
    cv.text(cx + cwd - 1.4, T(t + 2.0), "a = (f, t, e)", size=6.2, color=ac["ink"], style="italic", ha="right")
    cv.ax.plot([cx + 1.0, cx + cwd - 1.0], [T(t + 3.9)] * 2, color=ac["soft"], lw=0.6, zorder=5)
    kx, vx = cx + 1.4, cx + 8.0
    cv.text(kx, T(t + 5.7), "fact", size=6.0, weight="bold", color=ac["ink"], ha="left")
    yb = S.sans_para(cv, vx, T(t + 4.4), "departure moved to Apr 30", cwd - 8.0 - 1.2, size=6.2)
    t2 = H - yb + 0.5
    cv.text(kx, T(t2 + 1.6), "turn", size=6.0, weight="bold", color=ac["ink"], ha="left")
    S.seg_line(cv, vx, T(t2 + 1.6), [("#342 ", MUTED, "normal", None, True), ("Zhou Yue", INK, "normal")], size=6.2)
    S.avatar(cv, "zhou_yue", cx + cwd - 3.2, T(t2 + 1.6), 4.0)
    t2 += 3.6
    cv.text(kx, T(t2 + 1.3), "span", size=6.0, weight="bold", color=ac["ink"], ha="left")
    cv.text(cx + cwd - 1.4, T(t2 + 1.3), "verbatim in #342", size=5.8, color=MUTED, style="italic", ha="right")
    S.mono_para(cv, kx, T(t2 + 3.0), "“we leave on Apr 30”", 22, hl=[("“we leave on Apr 30”", ANCHOR)])
    t += 20.4 + 2.0
    for mid, s in ((34, "meet 7:30 am, May 1"), (326, "rail both ways")):
        cv.ax.add_patch(FancyBboxPatch((cx + 0.4, T(t + 2.7)), 2.2, 2.2, boxstyle="round,pad=0,rounding_size=0.5",
                                       fc=S.HL[ANCHOR], ec=ac["stroke"], lw=0.45, zorder=5))
        S.seg_line(cv, cx + 3.6, T(t + 1.6), [(f"#{mid} ", MUTED, "normal", None, True), (s, INK, "normal")], size=6.2)
        t += 3.3
    t = substep(x0, w, t + 1.3, "b", "rule", "Verify evidence spans")
    for mid, s, ok in ((342, "verbatim", True), (431, "not found", False)):
        S.seg_line(cv, cx + 0.4, T(t + 1.7), [(f"#{mid} ", MUTED, "normal", None, True), (s, INK, "normal")], size=6.2)
        S.verdict(cv, cx + cwd - 0.2, T(t + 1.7), ok, "keep" if ok else "drop", ha="right")
        t += 3.9
    cv.ax.plot([cx, cx + cwd], [T(t + 0.6)] * 2, color=slate["soft"], lw=0.6, zorder=3)
    t += 1.6
    t = H - S.sans_para(cv, cx + 0.4, T(t), "Verified anchors go to a per-group inventory.", cwd - 0.8, size=5.9,
                        color=MUTED, style="italic")
    assert t <= BOT - 1.0, t

    # ---- 3 Assign dependency type
    x0, w = xs[2], widths[2]
    cx, cwd = x0 + 1.5, w - 3.0
    t = substep(x0, w, PT + 11.0, "a", "rule", "Count units")

    def chip(px, py, r, struck=False):
        cv.ax.add_patch(FancyBboxPatch((px - 1.4, py - 1.0), 2.8, 2.0, boxstyle="round,pad=0,rounding_size=0.45",
                                       fc=S.HL[r], ec=ROLE[r]["stroke"], lw=0.45, zorder=6))
        if struck:
            cv.ax.plot([px - 1.0, px + 1.0], [py - 0.6, py + 0.6], color=ROLE[r]["ink"], lw=0.6, zorder=7)

    for code, n, lab in (("M1", 1, "one memory unit"), ("M2", 2, "two or more")):
        cv.text(cx + 0.4, T(t + 1.7), code, size=6.6, weight="bold", color=slate["ink"], ha="left")
        for j in range(n):
            chip(cx + 7.4 + j * 3.2, T(t + 1.7), ANCHOR)
        cv.text(cx + 0.4, T(t + 4.7), lab, size=6.0, color=INK, ha="left")
        t += 7.8
    # the M3 branch: a verified conflict pair
    mh = BOT - 1.2 - t
    cv.ax.add_patch(FancyBboxPatch((cx - 0.5, T(t + mh)), cwd + 1.0, mh, boxstyle="round,pad=0,rounding_size=1.3",
                                   fc=ROLE[OLD]["fill"], ec=ROLE[OLD]["stroke"], lw=0.6, ls=(0, (3, 2)), zorder=2))
    cv.text(cx + 0.4, T(t + 2.2), "M3", size=6.6, weight="bold", color=ROLE[OLD]["ink"], ha="left")
    cv.text(cx + 5.4, T(t + 2.2), "M2 + conflict pair", size=6.0, color=INK, ha="left")
    t += 4.4
    old = ROLE[OLD]
    for mid, val, r, struck in ((34, "May 1", OLD, True), (342, "Apr 30", CUR, False)):
        ex = S.seg_line(cv, cx + 0.6, T(t + 1.5), [(f"#{mid} ", MUTED, "normal", None, True),
                                                   (val, INK, "bold", r)], size=6.3)
        if struck:
            cv.ax.plot([ex - cv.text_width(val, 6.3, "bold") - 0.2, ex + 0.2], [T(t + 1.5)] * 2, color=old["ink"], lw=0.6,
                       zorder=22)
        cv.text(cx + cwd - 0.9, T(t + 1.5), "old" if struck else "new", size=5.9, color=ROLE[r]["ink"], style="italic",
                ha="right", weight="bold")
        t += 3.9
    t += 1.2
    t = substep(x0, w, t, "b", "rule", "Detect updates")
    t = substep(x0, w, t, "c", "model", "Three votes")
    cv.text(x0 + 2.0, T(t + 1.0), "same matter?", size=6.0, color=INK, ha="left")
    for j in range(3):
        S.tick(cv, x0 + 2.0 + cv.text_width("same matter?", 6.0) + 2.2 + j * 2.5, T(t + 1.0), True, s=1.7)
    t += 3.6
    t = substep(x0, w, t, "d", "rule", "Current at cut")
    t = H - S.sans_para(cv, x0 + 2.0, T(t - 0.2), "if not, the cut moves before the next change", cwd - 1.2, size=5.9,
                        color=MUTED, style="italic", pitch=2.4)
    assert t <= BOT - 1.6, t

    # ---- 4 Build instances
    x0, w = xs[3], widths[3]
    cx, cwd = x0 + 1.5, w - 3.0
    t = PT + 11.0
    for letter, doer, lab in (("a", "model", "Write authored queries"), ("b", "model", "Derive facts, grounding"),
                              ("c", "rule", "Trigger penalties"), ("d", "model", "Propose service criteria")):
        t = substep(x0, w, t, letter, doer, lab)

    def instance(t, letter, r, title, source, query, rows):
        c = ROLE[r]
        ch = int((cwd - 2.4) / cw)
        h = 4.6 + S.n_lines(query, ch) * P + 1.2 + len(rows) * 3.25 + 0.6
        card(cx, t, cwd, h, r=r, fill=c["fill"], lw=0.8, name=letter)
        S.letter_badge(cv, cx + 2.6, T(t + 2.4), letter, r, d=3.4)
        ex = S.seg_line(cv, cx + 5.0, T(t + 2.4), [(title, c["ink"], "bold")], size=6.6)
        cv.text(ex + 1.0, T(t + 2.45), source, size=5.9, color=MUTED, style="italic", ha="left")
        cv.icon_lock(cx + cwd - 2.2, T(t + 2.3), 2.0, color=MUTED)
        y = S.mono_para(cv, cx + 1.2, T(t + 4.6), query, ch)
        cv.ax.plot([cx + 1.0, cx + cwd - 1.0], [y - 0.5] * 2, color=c["soft"], lw=0.6, zorder=5)
        for k, (kind, segs, mid) in enumerate(rows):
            ry = y - 1.2 - 1.4 - k * 3.25
            S.key_row(cv, cx + 1.2, ry, cwd - 2.4, kind, segs, mid, size=6.0)
        return t + h + 1.3

    t = instance(t + 0.3, "A", L1, "L1 × M2", "native", "#104 @Agent on departure day, remind…",
                 [("fact", [("meet ", INK, "normal"), ("7:30 am, May 1", INK, "normal", ANCHOR)], 34),
                  ("fact", [("no-show ", INK, "normal"), ("pays ¥500", INK, "normal", ANCHOR)], 35)])
    t = instance(t, "B", L2, "L2 × M3", "authored", "#452 @Agent Post a reminder…",
                 [(3, [("window seat", INK, "normal", ANCHOR)], 363),
                  (2, [("leaves ", INK, "normal"), ("Apr 30", INK, "normal", CUR)], 342),
                  (-2, [("uses old ", INK, "normal"), ("May 1", INK, "normal", OLD)], 34)])
    assert t - 1.3 <= BOT - 0.9, t
    b_bottom = t - 1.3

    # ---- 5 Quality control
    x0, w = xs[4], widths[4]
    cx, cwd = x0 + 1.5, w - 3.0

    def checks(t, items):
        for s in items:
            S.tick(cv, cx + 1.3, T(t + 1.25), True, s=1.7)
            t = H - S.sans_para(cv, cx + 3.2, T(t), s, cwd - 3.2, size=6.0, pitch=2.45) + 0.5
        return t + 0.4

    t = substep(x0, w, PT + 11.0, "a", "rule", "Rule gates")
    t = checks(t, ["anchors precede the cut", "spans found verbatim", "query gives no cue of a change"])
    t = substep(x0, w, t, "b", "model", "Model review")
    t = checks(t, ["each anchor is necessary", "query not answerable from its own wording",
                   "assistant turns only relay a member's fact", "M3 values concern one matter"])
    t = substep(x0, w, t, "c", "human", "Human validation")
    t = H - S.sans_para(cv, cx + 0.6, T(t), "3 annotators, 120 instances: 95.8% valid by majority", cwd - 1.0, size=6.0,
                        pitch=2.45)
    assert t <= BOT - 1.0, t

    # ------------------------------------------------ feedback rail -> penalty criteria
    RT, RH = BOT + 3.4, 16.5
    rx1 = xs[3] + widths[3]
    red = ROLE[OLD]
    cv.ax.add_patch(FancyBboxPatch((1.0, T(RT + RH)), rx1 - 1.0, RH, boxstyle="round,pad=0,rounding_size=1.8",
                                   fc=red["fill"], ec=red["stroke"], lw=0.7, zorder=1))
    cv.text(3.0, T(RT + 2.9), "Penalty criteria from real feedback", size=7.0, weight="bold", color=red["ink"], ha="left")
    # the quote
    quote = "#1474 “I asked you to keep the memo. How is it mixed up again?”"
    qx, qt, qch = 3.0, RT + 6.2, 32
    qw, qh = qch * cw + 6.2, 2 * P + 1.8
    assert S.n_lines(quote, qch) == 2
    card(qx, qt, qw, qh, r=OLD, name="quote")
    S.person(cv, qx + 2.5, T(qt + qh / 2), 3.0, color=red["stroke"])
    S.mono_para(cv, qx + 4.8, T(qt + 0.9), quote, qch)
    ym = T(qt + qh / 2)
    cv.arrow([(qx + qw + 0.6, ym), (qx + qw + 3.4, ym)], color=red["mark"], lw=0.9, head=1.3)
    fx0 = qx + qw + 4.2
    cv.text(fx0, ym + 1.5, "423 negative reactions", size=6.0, color=INK, ha="left")
    cv.text(fx0, ym - 1.5, "97 corrections", size=6.0, color=INK, ha="left", weight="bold")
    fx1 = fx0 + cv.text_width("423 negative reactions", 6.0) + 0.8
    cv.arrow([(fx1, ym), (fx1 + 2.8, ym)], color=red["mark"], lw=0.9, head=1.3)
    # five failure patterns, each with its weight (Table 7); the last one is the M3 penalty of instance B
    px0, px1 = fx1 + 3.6, rx1 - 1.4
    cv.text(px0, T(RT + 2.9), "five failure patterns, each with its weight", size=6.0, color=MUTED, style="italic",
            ha="left")
    rows = [PATTERNS[1:2] + PATTERNS[4:5] + PATTERNS[3:4], PATTERNS[2:3] + PATTERNS[0:1]]
    hot = None
    for k, row in enumerate(rows):
        y = T(RT + 7.6 + k * 4.4)
        tws = [cv.text_width(n, 6.0, "bold" if n == "superseded value" else "normal") + 2.0 + 4.8 for n, _ in row]
        x = px0
        assert px0 + sum(tws) + 1.0 * (len(row) - 1) <= px1, "pattern chips leave the rail"
        for (name, wt), tw in zip(row, tws):
            on = name == "superseded value"
            cv.chips.append((x, y - 1.6, tw, 3.2, name, (px0 - 0.1, T(RT + RH), px1 + 0.1, T(RT + 4.6))))
            cv.ax.add_patch(FancyBboxPatch((x, y - 1.6), tw, 3.2, boxstyle="round,pad=0,rounding_size=1.6", fc="white",
                                           ec=red["ink"] if on else red["stroke"], lw=1.0 if on else 0.5, zorder=5))
            cv.text(x + 1.4, y - 0.05, name, size=6.0, color=INK, ha="left", weight="bold" if on else "normal")
            cv.ax.add_patch(FancyBboxPatch((x + tw - 4.5, y - 1.2), 3.9, 2.4, boxstyle="round,pad=0,rounding_size=1.2",
                                           fc=red["mark"], ec="none", zorder=6))
            cv.text(x + tw - 2.55, y - 0.05, f"−{abs(wt)}", size=6.0, color="white", weight="bold")
            if on:
                hot = (x + tw / 2, y + 1.6)
            x += tw + 1.0
    # the rail enters step 4 at the penalty row it produces
    cv.arrow([hot, (hot[0], T(b_bottom))], color=red["mark"], lw=1.1, head=1.5)

    # ------------------------------------------------ output
    x0, w = xs[4], widths[4]
    S.frame(cv, x0, T(RT), w, RH)
    S.header(cv, x0, T(RT), w, 5.4, "Evaluation set", size=7.4)
    cv.text(x0 + w / 2, T(RT + 8.4), f"{FUNNEL['sampled']:,}", size=9.5, weight="bold", color=slate["ink"])
    cv.text(x0 + w / 2, T(RT + 11.6), "instances (c, q, A, K)", size=6.0, color=INK)
    cv.text(x0 + w / 2, T(RT + 14.2), f"sampled from the {FUNNEL['passed']:,}", size=5.8, color=MUTED, style="italic")
    cv.block_arrow(x0 + w / 2, T(BOT + 0.2), x0 + w / 2, T(RT - 0.1), width=3.6, color=slate["stroke"], head=2.2)

    # ------------------------------------------------ key
    S.key(cv, 1.0, 1.0, W - 2.0, [
        (lambda x, y: S.gear(cv, x, y, 2.6, color=slate["ink"]), 2.6, "rules"),
        (lambda x, y: S.sparkle(cv, x, y, 2.6, color=slate["ink"]), 2.6, "language model"),
        (lambda x, y: S.person(cv, x, y, 2.6, color=slate["ink"]), 2.6, "humans"),
        (lambda x, y: cv.text(x, y - 0.1, r"$\hat{y}^{+}$ $\hat{y}^{-}$", size=6.4, color=slate["ink"], z=12), 6.2,
         "answer with / without history"),
        (lambda x, y: S.swatch(cv, x, y, ANCHOR), 3.6, "anchor"),
        (lambda x, y: S.swatch(cv, x, y, OLD), 3.6, "superseded"),
        (lambda x, y: S.swatch(cv, x, y, CUR), 3.6, "current"),
        (lambda x, y: cv.icon_lock(x, y, 2.2, color=MUTED), 2.2, "judge only"),
    ])

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
