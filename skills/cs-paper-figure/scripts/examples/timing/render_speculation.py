#!/usr/bin/env python3
"""A timing diagram for a latency claim: a ReAct baseline above, a speculative agent below (140 x 67 mm).

The method ("SPECTRA") and its step times are ILLUSTRATIVE, made up to show the family. This script was
written by a fresh agent from a one-paragraph brief and the skill alone; it is kept as the model for the
family. Devices are taken from JetSpec++ Fig. 1 (references/trending-study-2026-11.md).

Family: timing diagram (references/registers.md section 2, visual-craft.md section 5).
Model: assets/models/idea_timing_diagram.png.
  * Message: planning the next step while the tool runs removes the wait when the prediction is right.
  * The picture: one time axis, the baseline's rows above and ours below at one scale. Where the baseline
    has a hatched idle block ours has the one saturated block; the saving is a dimension arrow between the
    two dashed end lines.
  * Every block's position and width is computed from the step times below; nothing is placed by hand,
    and the end times are asserted.
  * A hit and a miss are both drawn: the kept plan saturated, the discarded one ghosted and struck out,
    followed by the re-plan. The pale band marks a prediction awaiting its verdict.
  * Type: Times at 8.0 / 7.2 / 6.0 pt. One stroke weight, 0.6 pt. Orange is speculation, blue is tool
    calls, grey is the main model's ordinary work.

    python render_speculation.py --out DIR
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import LINE, MUTED, ROLE, Canvas  # noqa: E402

STEM = "timing_speculation"
# ------------------------------------------------------------------ inputs: the running example ---
TASK = "Find the cheapest direct flight SFO$\\rightarrow$NRT\nnext Friday and add it to my calendar."
STEPS = [("search_flights", 2.1), ("get_fare_details", 1.4), ("calendar.add_event", 0.9)]  # tool, seconds
HIT = [True, False, True]         # does the draft model's prediction of call k's result match the real one
PLAN, DRAFT, VERIFY = 1.2, 0.3, 0.1   # main-model planning per step, draft prediction, verification (s)


# ------------------------------------------------------------------ schedules, derived ---
def baseline():
    """(row, t0, t1, kind, label) of every interval, and the end time. Plan, wait for the tool, repeat."""
    t, ev = 0.0, []
    for k, (_, d) in enumerate(STEPS, 1):
        ev += [("model", t, t + PLAN, "plan", f"plan {k}"), ("model", t + PLAN, t + PLAN + d, "idle", None),
               ("tool", t + PLAN, t + PLAN + d, "tool", k)]
        t += PLAN + d
    return ev, round(t, 6)


def spectra():
    """While call k runs: draft predicts its result, main model plans step k+1 on the prediction; when the
    real result is back the verifier commits the plan (hit) or it is discarded and re-planned (miss).
    The last call has no step after it, so nothing is speculated there and HIT[-1] does not change the
    wall time."""
    ev, t, busy = [("model", 0.0, PLAN, "plan", "plan 1")], PLAN, PLAN   # busy = main model occupied until
    for k, (_, d) in enumerate(STEPS, 1):
        ret = t + d
        ev.append(("tool", t, ret, "tool", k))
        if k == len(STEPS):
            ev.append(("model", busy, ret, "idle", None))
            return ev, round(ret, 6)
        s0, s1, v1 = t + DRAFT, t + DRAFT + PLAN, ret + VERIFY
        ev += [("model", busy, s0, "idle", None), ("draft", t, s0, "predict", k), ("draft", ret, v1, "verify", k)]
        if HIT[k - 1]:
            ev.append(("model", s0, s1, "commit", f"plan {k + 1}"))
            busy, t = s1, max(v1, s1)
        else:
            cut = min(s1, v1)
            ev += [("model", s0, cut, "discard", f"plan {k + 1}"), ("model", cut, v1, "idle", None),
                   ("model", v1, v1 + PLAN, "plan", f"re-plan {k + 1}")]
            busy = t = v1 + PLAN


EV_A, END_A = baseline()
EV_B, END_B = spectra()
SAVED = round(END_A - END_B, 6)
PCT = 100 * SAVED / END_A
assert (END_A, END_B, SAVED, PCT) == (8.0, 7.0, 1.0, 12.5), (END_A, END_B, SAVED, PCT)   # derived, then printed

# ------------------------------------------------------------------ visual system ---
HEAD, LABEL, FINE = 8.0, 7.2, 6.0     # pt: heads and the claim number / labels / ticks and tool names
LW = 0.6                              # the one stroke weight
W, H = 140.0, 67.0                    # mm
X0, S = 19.5, 15.0                    # x of t = 0 and mm per second: 8 s ends 0.5 mm from the edge
BH, RG = 5.8, 1.3                     # block height, gap between rows
AM, NE, BL = ROLE["amber"], ROLE["neutral"], ROLE["blue"]   # speculation / the main model's work / tool calls
GREEN, RED, DARK = ROLE["memory"]["mark"], ROLE["coral"]["mark"], NE["ink"]


def X(t):
    return X0 + S * t


def build():
    cv = Canvas(W, H, family="serif", size=LABEL)

    def block(y, t0, t1, kind, label=None):
        if t1 - t0 < 1e-9:
            return
        x, w = X(t0), S * (t1 - t0)
        cx, cy = x + w / 2, y + BH / 2
        if kind == "idle":       # the main model has nothing to do
            cv.box(x, y, w, BH, fill="white", stroke=NE["stroke"], lw=LW, radius=0, hatch="/////")
            if w > 9:
                cv.text(cx, cy, "idle", size=LABEL, color=MUTED, style="italic",
                        bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))
        elif kind == "plan":
            cv.box(x, y, w, BH, fill=NE["soft"], stroke=NE["stroke"], lw=LW, radius=0, title=label, size=LABEL,
                   weight="normal", title_color="black")
        elif kind == "tool":     # numeral of the call, defined in the trajectory strip, and its duration
            cv.box(x, y, w, BH, fill=BL["soft"], stroke=BL["stroke"], lw=LW, radius=0)
            d = f"{t1 - t0:.1f} s"
            tw = 3.0 + 0.9 + cv.text_width(d, LABEL)
            cv.badge(cx - tw / 2 + 1.5, cy, label, "blue", d=3.0, size=FINE, rim=0)
            cv.text(cx - tw / 2 + 3.9, cy, d, size=LABEL, color="black", ha="left")
        elif kind == "commit":   # the hero: a plan made on the predicted result, kept
            cv.box(x, y, w, BH, fill=AM["mark"], stroke=AM["mark"], lw=LW, radius=0, title=label, size=LABEL,
                   weight="bold", title_color="white")
        elif kind == "discard":  # the same plan, thrown away: ghosted and struck out
            cv.box(x, y, w, BH, fill=AM["fill"], stroke=AM["stroke"], lw=LW, radius=0, title=label, size=LABEL,
                   weight="normal", title_color=AM["ink"])
            tw = cv.text_width(label, LABEL)
            cv.ax.plot([cx - tw / 2 - 0.6, cx + tw / 2 + 0.6], [cy, cy], color=AM["ink"], lw=LW, zorder=25)
        elif kind == "predict":
            cv.box(x, y, w, BH, fill=AM["soft"], stroke=AM["stroke"], lw=LW, radius=0,
                   title=f"$\\hat{{r}}_{label}$", size=LABEL, weight="normal", title_color="black")
        elif kind == "verify":   # 0.1 s: a sliver, with the comparison and its verdict set before it
            cv.box(x, y, w, BH, fill=DARK, stroke=DARK, lw=LW, radius=0)
            hit = HIT[label - 1]
            (cv.icon_check if hit else cv.icon_cross)(x - 2.4, cy, 3.0, color=GREEN if hit else RED, lw=1.0)
            cv.text(x - 4.6, cy, f"$\\hat{{r}}_{label} {'=' if hit else chr(92) + 'neq'} r_{label}$", size=LABEL,
                    color="black", ha="right")

    def rows(events, ys):
        for row, t0, t1, kind, label in events:
            block(ys[row], t0, t1, kind, label)

    def head(y, segs, note):
        base = y - 0.72 * HEAD / 2.835
        end = cv.rich(1.0, base, segs, size=HEAD, va="baseline")
        cv.text(end + 2.0, base, note, size=LABEL, color=MUTED, style="italic", ha="left", va="baseline")

    def row_label(y, s):
        cv.text(X0 - 1.3, y + BH / 2, s, size=LABEL, color="black", ha="right")

    # ---- the task, said once, and the trajectory both agents follow ----
    yb = H - 0.6 - 4.0
    cv.icon_user(3.3, yb - 0.3, 4.4, color=LINE, lw=LW)
    bx, _, bw, _ = cv.bubble(0, yb, TASK, tail=(5.9, yb), size=LABEL, left=8.0, lw=LW)
    names = [n for n, _ in STEPS]
    wn = [cv.text_width(n, FINE, family="monospace") for n in names]
    sep = 2.2                                                        # between two calls
    x = X(END_A) - sum(wn) - len(names) * 3.9 - (len(names) - 1) * sep
    assert x - (bx + bw) >= 6.0, x - (bx + bw)                       # room for the one arrow from the request
    yc = yb - 1.6
    cv.arrow([(bx + bw + 1.0, yc), (x - 1.0, yc)], color=LINE, lw=LW, head=1.4)
    cv.text(x, yb + 2.2, "the same three tool calls in both agents", size=LABEL, color=MUTED, style="italic",
            ha="left")
    for k, (n, w) in enumerate(zip(names, wn), 1):
        cv.badge(x + 1.5, yc, k, "blue", d=3.0, size=FINE, rim=0)
        cv.text(x + 3.9, yc, n, size=FINE, color="black", ha="left", family="monospace")
        x += 3.9 + w + sep

    # ---- baseline ----
    ya = H - 11.5
    head(ya, [("ReAct baseline", "black"), (f"   {END_A:.1f} s", "black", "bold")],
         "the model is idle while every tool runs")
    a = {"model": ya - 4.6 - BH}
    a["tool"] = a["model"] - RG - BH
    row_label(a["model"], "Main model")
    row_label(a["tool"], "Tool")
    rows(EV_A, a)

    # ---- SPECTRA: the same two rows, and one added lane between them ----
    yh = a["tool"] - 3.2
    head(yh, [("SPECTRA", AM["ink"], "bold"), (f"   {END_B:.1f} s", "black", "bold")],
         "plans the next step on a predicted result while the tool runs")
    b = {"model": yh - 4.6 - BH}
    b["draft"] = b["model"] - RG - BH
    b["tool"] = b["draft"] - RG - BH
    row_label(b["model"], "Main model")
    row_label(b["draft"], "Draft, verifier")
    row_label(b["tool"], "Tool")
    start = {k: t0 for row, t0, _, kind, k in EV_B if kind == "predict"}
    for row, _, t1, kind, k in EV_B:
        if kind == "verify":     # tint = a prediction is outstanding, from the call to its verdict
            cv.box(X(start[k]), b["draft"], S * (t1 - start[k]), BH, fill=AM["fill"], stroke="none", lw=0,
                   radius=0, z=1, container=True)
    rows(EV_B, b)
    for row, _, t1, kind, k in EV_B:
        if kind == "predict":    # the prediction feeds the plan made on it
            cv.arrow([(X(t1), b["draft"] + BH / 2), (X(t1) + 2.2, b["draft"] + BH / 2),
                      (X(t1) + 2.2, b["model"])], color=AM["mark"], lw=LW, head=1.3, radius=0.8)

    # ---- one time axis ----
    yx = b["tool"] - 1.0
    cv.ax.plot([X(0), X(END_A)], [yx, yx], color=LINE, lw=LW, zorder=3, solid_capstyle="butt")
    for s in range(int(END_A) + 1):
        cv.ax.plot([X(s), X(s)], [yx, yx - 1.0], color=LINE, lw=LW, zorder=3, solid_capstyle="butt")
        cv.text(X(s), yx - 2.5, str(s), size=FINE, color="black")
    cv.text(X0 - 1.3, yx - 2.5, "time (s)", size=FINE, color="black", ha="right")

    # ---- the claim: the gap between the two end times ----
    for t in (END_A, END_B):     # two end lines of one height, so the arrow reads as a dimension
        cv.line([(X(t), a["tool"]), (X(t), yx)], color=LINE, lw=LW, dashed=True, z=2)
    ym = b["model"] + BH / 2
    cv.arrow([(X(END_B) + 0.3, ym), (X(END_A) - 0.3, ym)], color="black", lw=LW, head=1.5, both=True)
    xm = (X(END_A) + X(END_B)) / 2
    cv.text(xm, ym - 4.6, f"{SAVED:.1f} s", size=HEAD, weight="bold", color="black")
    cv.text(xm, ym - 7.9, "saved", size=LABEL, color="black")
    cv.text(xm, ym - 11.0, f"({PCT:.1f} %)", size=LABEL, color="black")

    # ---- key: a sample of each new mark ----
    yk, kh, x = 2.3, 3.2, 1.0

    def key(w, draw, label, gap=3.8):
        nonlocal x
        draw(x)
        x += w + 1.0
        cv.text(x, yk, label, size=LABEL, color="black", ha="left")
        x += cv.text_width(label, LABEL) + gap

    key(4.5, lambda x: cv.box(x, yk - kh / 2, 4.5, kh, fill=AM["soft"], stroke=AM["stroke"], lw=LW, radius=0),
        "draft predicts result $\\hat{r}_t$")
    key(4.5, lambda x: cv.box(x, yk - kh / 2, 4.5, kh, fill=AM["mark"], stroke=AM["mark"], lw=LW, radius=0),
        "speculative plan on $\\hat{r}_t$")
    key(1.5, lambda x: cv.box(x, yk - kh / 2, 1.5, kh, fill=DARK, stroke=DARK, lw=LW, radius=0),
        "verify against the real $r_t$")
    key(2.4, lambda x: cv.icon_check(x + 1.2, yk, 2.4, color=GREEN, lw=1.0), "hit: commit")
    key(2.4, lambda x: cv.icon_cross(x + 1.2, yk, 2.4, color=RED, lw=1.0), "miss: discard, re-plan", gap=0)
    assert x <= W - 0.5, x

    assert not cv.overlaps() and not cv.text_overlaps() and not cv.wire_crossings(), \
        (cv.overlaps(), cv.text_overlaps(), cv.wire_crossings())
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/timing")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
