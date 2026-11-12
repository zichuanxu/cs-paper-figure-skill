"""ReHarness Fig. 1, "From stateful agent harnesses to ReHarness" (arXiv:2610.12668).

Source: Xiao et al., "Recurrent Harness for Agentic Continual Learning", Fig. 1 and Sec. 3.

Content kept from the source
* The toy stream: tau_{t-1} = (sort descending {3,7,4} -> {7,4,3}, correct), tau_t = (sort ascending
  {2,9,5} -> {9,5,2}, wrong), tau_{t+1} = (sort ascending {3,7,4}); the stateful harness answers
  {7,4,3} (wrong), ReHarness answers {3,4,7} (correct).
* The states and reflections, verbatim: h_t = {R_{t-1}: "Put larger numbers first"}; stateful
  h_{t+1} adds R_t "Put smaller numbers first"; ReHarness h'_t holds R'_{t-1} "Larger first only if
  descending" and its h_{t+1} adds R_t "Smaller first only if ascending".
* The numbered edges of both panels, in the source's order and with the source's endpoints:
  (a) 1 write R_{t-1}, 2 read R_{t-1}, 3 write R_t, 4 read R_{t-1} again;
  (b) 1 write R_{t-1}, 2 read R_{t-1}, 3 backward revision tau_t -> h'_t, 4 write R_t, 5 read R'_{t-1}.
* The agents docked on their cards (decision pi_D, memory pi_M, revision pi_R), the incoming states
  h_{t-1} / h'_{t-1}, and Eqs. (2)-(3) instantiated for the example (i = t-1).

Design
* One instance stream, two harnesses. Steps t-1 and t are identical under both harnesses, so the
  trajectories are drawn once in the middle; the stateful harness sits above the stream and ReHarness
  below it on the same column grid. The two outcomes meet in the tau_{t+1} card, one row each.
* A state h_t exists between instance t-1 and instance t, so the state cards are staggered half a
  column from the trajectories. Every write and read is then a short straight vertical edge.
* The added layer has its own row and its own hue: backward revision (orange) hangs under the forward
  state row (blue). The hero is the h'_t card, which shows the edit itself: the old reflection struck
  out, the revised one with its new condition highlighted.
* Edge type = colour (blue forward, orange backward); edge order = the numbered badge inside a label
  chip that sits on the edge, so no detached legend box is needed.
* Numbers are tokens shaded by magnitude, so "descending" and "ascending" are visible as a gradient.
* Green and red appear only on reward marks and the two verdicts.

python render_fig1.py --out DIR  ->  DIR/reharness_fig1.{pdf,svg,png}
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import paperkit as pk  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Rectangle  # noqa: E402

STEM = "reharness_fig1"
W, H = 178.0, 99.0

# ---- roles: one meaning per hue ------------------------------------------------------------------
FWD = dict(fill="#EAF2FC", soft="#B6D6F4", stroke="#3F78C2", ink="#1B467F", mark="#2F6FC0")   # forward state, write, read
REV = dict(fill="#FFF8EC", soft="#FAD7A2", stroke="#D0822A", ink="#8A4706", mark="#D9730B")   # backward revision (the new layer)
ENV = dict(fill="#F5F6F8", soft="#E3E7ED", stroke="#74859C", ink="#2F3B4D", mark="#5E7088")   # instance stream / baseline frame
OK = dict(fill="#E7F4EB", soft="#CFE9D7", stroke="#3E9160", ink="#1C5A35", mark="#2E8B57")    # reward: correct
BAD = dict(fill="#FCEBE7", soft="#F6CFC6", stroke="#C9553E", ink="#8C2A18", mark="#CF4530")   # reward: wrong
INK, MUTED = pk.INK, pk.MUTED

# ---- column grid (mm): trajectories on the columns, states half a column later -------------------
PITCH, TW, SW = 57.0, 46.0, 44.0
TAU_X = [9.0 + i * PITCH for i in range(3)]                    # left edges of tau_{t-1}, tau_t, tau_{t+1}
ST_X = [TAU_X[0] + TW / 2 + PITCH / 2 - SW / 2 + i * PITCH for i in range(2)]   # h_t, h_{t+1}
X_W1 = (ST_X[0] + TAU_X[0] + TW) / 2      # tau_{t-1} <-> h_t
X_R1 = (TAU_X[1] + ST_X[0] + SW) / 2      # h_t <-> tau_t
X_W2 = (ST_X[1] + TAU_X[1] + TW) / 2      # tau_t <-> h_{t+1}
X_R2 = (TAU_X[2] + ST_X[1] + SW) / 2      # h_{t+1} <-> tau_{t+1}
X_MID = TAU_X[1] + TW / 2                 # tau_t centre = gap between the two states

# ---- rows (mm, bottom-up) ------------------------------------------------------------------------
HH, NOTE, NGAP, NPAD = 4.2, 3.3, 0.6, 0.8      # state card: header, note strip, gap, padding


def state_h(n):
    return HH + 2 * NPAD + n * NOTE + (n - 1) * NGAP


KEY_Y, KEY_H = 1.0, 5.0
SB_Y0 = KEY_Y + KEY_H + 2.0                    # section (b) bottom
REV_Y0 = SB_Y0 + 2.2                           # revision row
REV_Y1 = REV_Y0 + state_h(2)
STB_Y0 = REV_Y1 + 9.0                          # state row of (b): cards hang from STB_Y1
STB_Y1 = STB_Y0 + state_h(2)
TROW, TH = 4.2, 4.4                            # trajectory card: row pitch, header
TAU_Y0 = STB_Y1 + 10.0
TAU_H2 = TH + 2 * TROW + 1.4
TAU_Y1 = TAU_Y0 + TAU_H2
TAU_YM = (TAU_Y0 + TAU_Y1) / 2
TAU_H3 = TAU_H2 + TROW
SB_Y1 = TAU_Y0 - 3.0                           # section (b) top
SA_Y0 = TAU_Y1 + 3.0                           # section (a) bottom
STA_Y0 = TAU_Y1 + 10.0                         # state row of (a): cards stand on STA_Y0
SA_Y1 = STA_Y0 + state_h(2) + 3.4
CHIP_OFF = 6.2                                 # edge-label chips: distance from the stream


def card(cv, x, y, w, h, r, left, right, hh, *, body=None, lw=0.7, shadow=False, lsize=7.6, rsize=6.4):
    """Data card: role-tinted body, solid header with the symbol left and the agent that produces it right."""
    cv.box(x, y, w, h, r, fill=body or r["fill"], stroke=r["stroke"], lw=lw, radius=1.4, shadow=shadow)
    cv.ax.add_patch(PathPatch(pk._round_top_rect(x, y + h - hh, w, hh, 1.4), fc=r["mark"], ec=r["mark"], lw=lw,
                              zorder=5.2))
    cv.text(x + 1.8, y + h - hh / 2, left, size=lsize, color="white", weight="bold", ha="left", z=6)
    cv.text(x + w - 1.8, y + h - hh / 2 - 0.05, right, size=rsize, color="white", ha="right", z=6)


def note(cv, x, y, w, label, segs, tick, *, size=6.5, label_color=None, struck=False):
    """One reflection as a note strip: tick in the colour of the edge that produced it, R label, text."""
    cv.ax.add_patch(FancyBboxPatch((x, y), w, NOTE, boxstyle="round,pad=0,rounding_size=0.7", fc="white",
                                   ec="none", zorder=5.4, alpha=0.55 if struck else 1.0))
    cv.ax.add_patch(Rectangle((x + 0.8, y + 0.6), 0.75, NOTE - 1.2, fc=tick, ec="none", zorder=5.6))
    cy = y + NOTE / 2 - 0.05
    cv.text(x + 2.3, cy, label, size=size, color=label_color or INK, ha="left", z=6)
    x0 = x + 10.2
    x1 = cv.rich(x0, cy, segs, size=size, z=6)
    assert x1 <= x + w - 0.5, (label, x1, x + w)
    if struck:
        cv.ax.plot([x0 - 0.3, x1 + 0.3], [cy - 0.1, cy - 0.1], color=MUTED, lw=0.6, zorder=7, solid_capstyle="round")
    return x0, x1


def state(cv, x, y, sym, agent, notes, r=FWD, **kw):
    """Harness state = a card holding its reflections. y is the bottom edge."""
    h = state_h(len(notes))
    card(cv, x, y, SW if "w" not in kw else kw.pop("w"), h, r, sym, agent, HH, body=r["soft"], **kw)
    for i, (label, segs, tick, lc) in enumerate(notes):
        note(cv, x + 1.1, y + h - HH - NPAD - (i + 1) * NOTE - i * NGAP, SW - 2.2, label, segs, tick, label_color=lc)
    return h


def shade(v):
    """Token fill by magnitude (2..9): larger = darker."""
    return dict(soft=pk.mix("#FAFBFC", "#9DA8B7", (v - 2) / 7), stroke="#7F8A99", ink=INK)


def numbers(cv, x, cy, vals):
    cv.tokens(x, cy - 1.5, 3, w=3.3, h=3.0, gap=0.4, labels=[str(v) for v in vals], fills=[shade(v) for v in vals],
              size=6.4)
    return x + 3 * 3.3 + 2 * 0.4


def reward(cv, x, cy, good, d=3.0):
    r = OK if good else BAD
    cv.ax.add_patch(Circle((x, cy), d / 2, fc=r["mark"], ec="white", lw=0.4, zorder=9))
    (cv.icon_check if good else cv.icon_cross)(x, cy, d * 0.52, color="white", lw=0.9, z=10)


def trajectory(cv, x, sub, order, xs, outcomes, hero=False):
    """tau = (x, y, r). outcomes = [(y tokens, correct?, tag, tag role, note)], one row per harness."""
    h = TH + 1.4 + (1 + len(outcomes)) * TROW
    y = TAU_YM - h / 2
    card(cv, x, y, TW, h, ENV, rf"$\tau_{{{sub}}}$", r"Decision agent $\pi_D$", TH, body="white",
         lw=0.9 if hero else 0.7, shadow=hero)
    cy = y + h - TH - 0.7 - TROW / 2
    cv.text(x + 1.8, cy, rf"$x_{{{sub}}}$", size=6.8, color=ENV["ink"], ha="left")
    xe = numbers(cv, x + 9.2, cy, xs)
    cv.text(xe + 1.8, cy, f"sort {order}", size=6.5, ha="left")
    for ys, good, tag, tr, msg in outcomes:
        cy -= TROW
        cv.ax.add_patch(FancyBboxPatch((x + 0.9, cy - TROW / 2 + 0.25), TW - 1.8, TROW - 0.5,
                                       boxstyle="round,pad=0,rounding_size=0.8", fc=(OK if good else BAD)["fill"],
                                       ec="none", zorder=5.3))
        cv.text(x + 1.8, cy, rf"$y_{{{sub}}}$", size=6.8, color=ENV["ink"], ha="left")
        xe = numbers(cv, x + 9.2, cy, ys)
        cv.text(xe + 1.8, cy, rf"$r_{{{sub}}}$", size=6.8, color=ENV["ink"], ha="left")
        reward(cv, x + 31.2, cy, good)
        if tag:
            cv.chip(x + 34.0, cy, tag, tr, size=6.0, h=3.0, pad=0.8, solid=True, ha="left",
                    region=(x, y, x + TW, y + h))
        elif msg:
            cv.text(x + 33.8, cy, msg, size=6.2, color=(OK if good else BAD)["ink"], style="italic", ha="left")
    return y, y + h


def edge(cv, x, y0, y1, yc, k, label, r, lw=0.9):
    """Numbered, typed vertical edge: the label chip (badge + what moves) sits on the wire."""
    size, hc = 6.4, 3.6
    verb, what, wr = label
    w = 3.9 + cv.text_width(verb, size) + cv.text_width(what, size) + 1.3
    s = 1 if y1 > y0 else -1
    cv.line([(x, y0), (x, yc - s * hc / 2)], color=r["mark"], lw=lw)
    cv.arrow([(x, yc + s * hc / 2), (x, y1)], color=r["mark"], lw=lw, head=1.5)
    cv.ax.add_patch(FancyBboxPatch((x - w / 2, yc - hc / 2), w, hc, boxstyle=f"round,pad=0,rounding_size={hc / 2}",
                                   fc="white", ec=r["mark"], lw=0.6, zorder=11))
    cv.badge(x - w / 2 + 1.8, yc, k, r, d=3.0, size=6.0)
    cv.rich(x - w / 2 + 3.9, yc - 0.05, [(verb, r["ink"]), (what, wr["ink"])], size=size, z=13)


def verdict(cv, x, y, w, h, good, lines, size=6.7):
    r = OK if good else BAD
    cv.box(x, y, w, h, r, fill=r["soft"], stroke=r["stroke"], lw=0.8, radius=h / 2)
    reward(cv, x + h / 2 + 0.2, y + h / 2, good, d=4.0)
    for i, s in enumerate(lines):
        cv.text(x + h + 0.6, y + h / 2 + (len(lines) - 1 - 2 * i) * 1.7, s, size=size, color=r["ink"], ha="left",
                weight="bold" if i == 0 else "normal")


def title_tab(cv, x, yc, text, r):
    w = cv.text_width(text, 7.8, "bold") + 4.4
    cv.tab(x, yc - 2.2, w, 4.4, r, text, size=7.8, solid=True, radius=1.3)
    return x + w


def key(cv, x, y, w, h):
    """Glyph key: one entry per colour or mark the panels use without words."""
    cv.box(x, y, w, h, ENV, fill="white", stroke=ENV["stroke"], lw=0.5, radius=1.4, dashed=True, container=True, z=1)
    cy, s = y + h / 2, 6.3

    def wire(r):
        def f(xx):
            cv.arrow([(xx, cy), (xx + 5.0, cy)], color=r["mark"], lw=0.9, head=1.4, z=9)
            return 5.0
        return f

    def badge(xx):
        cv.badge(xx + 1.5, cy, 1, FWD, d=3.0, size=6.0)
        cv.badge(xx + 4.9, cy, 3, REV, d=3.0, size=6.0)
        return 6.4

    def ticks(xx):
        for i, r in enumerate((FWD, REV)):
            cv.ax.add_patch(FancyBboxPatch((xx + i * 3.4, cy - 1.5), 2.8, 3.0, boxstyle="round,pad=0,rounding_size=0.6",
                                           fc=r["soft"], ec="none", zorder=8))
            cv.ax.add_patch(Rectangle((xx + i * 3.4 + 1.02, cy - 0.95), 0.75, 1.9, fc=r["mark"], ec="none", zorder=9))
        return 6.2

    def toks(xx):
        for i, v in enumerate((2, 5, 9)):
            c = shade(v)
            cv.ax.add_patch(FancyBboxPatch((xx + i * 2.6, cy - 1.1), 2.2, 2.2, boxstyle="round,pad=0,rounding_size=0.45",
                                           fc=c["soft"], ec=c["stroke"], lw=0.4, zorder=8))
        return 7.4

    def marks(xx):
        reward(cv, xx + 1.4, cy, True, d=2.8)
        reward(cv, xx + 4.6, cy, False, d=2.8)
        return 6.0

    items = [(wire(FWD), "forward write / read"), (wire(REV), "backward revision"), (badge, "order of events"),
             (ticks, "reflection: written / revised"), (toks, "shade = magnitude"), (marks, r"reward $r$")]
    widths = [{0: 5.0, 1: 5.0, 2: 6.4, 3: 6.2, 4: 7.4, 5: 6.0}[i] + 1.1 + cv.text_width(lab, s)
              for i, (_, lab) in enumerate(items)]
    gap = (w - 5.0 - sum(widths)) / (len(items) - 1)
    assert gap > 2.5, gap
    xx = x + 2.5
    for (draw, lab), iw in zip(items, widths):
        gw = draw(xx)
        cv.text(xx + gw + 1.1, cy - 0.05, lab, size=s, color=INK, ha="left")
        xx += iw + gap


def render(out):
    cv = pk.Canvas(W, H, size=6.8)

    # ---- frames: baseline above the stream, ours below, the new layer as its own lane ------------
    cv.section(1.5, SA_Y0, W - 3.0, SA_Y1 - SA_Y0, ENV)
    cv.section(1.5, SB_Y0, W - 3.0, SB_Y1 - SB_Y0, REV)
    cv.box(3.0, REV_Y0 - 1.3, W - 6.0, REV_Y1 - REV_Y0 + 2.7, REV, fill="#FDEBCB", stroke="none", lw=0, radius=1.8,
           container=True, z=1.5)
    title_tab(cv, 5.0, SA_Y1, "(a) Stateful harness", ENV)
    title_tab(cv, 5.0, SB_Y1 - 1.0, "(b) ReHarness", REV)
    cv.text(5.2, SA_Y1 - 4.3, "forward write and read only", size=6.2, color=MUTED, style="italic", ha="left")

    # ---- the shared instance stream ----------------------------------------------------------------
    trajectory(cv, TAU_X[0], "t-1", "descending", (3, 7, 4), [((7, 4, 3), True, None, None, None)])
    trajectory(cv, TAU_X[1], "t", "ascending", (2, 9, 5), [((9, 5, 2), False, None, None, "misled")])
    y30, y31 = trajectory(cv, TAU_X[2], "t+1", "ascending", (3, 7, 4),
                          [((7, 4, 3), False, "(a)", ENV, None), ((3, 4, 7), True, "(b)", REV, None)], hero=True)
    for i in range(2):
        cv.block_arrow(TAU_X[i] + TW + 1.6, TAU_YM, TAU_X[i + 1] - 1.6, TAU_YM, width=2.8, color="#C3C9D2")
    cv.text(TAU_X[2] + TW + 3.8, TAU_YM, r"$\cdots$", size=8.0, color=MUTED)
    cv.text(4.9, TAU_YM, "shared stream", size=6.2, color=MUTED, style="italic", rotation=90)

    # ---- (a) stateful harness: the state only grows ------------------------------------------------
    r_old = ("$R_{t-1}$", [("Put larger numbers first", INK)], FWD["mark"], FWD["ink"])
    ha1 = state(cv, ST_X[0], STA_Y0, "$h_t$", r"Memory agent $\pi_M$", [r_old])
    state(cv, ST_X[1], STA_Y0, "$h_{t+1}$", r"Memory agent $\pi_M$",
          [r_old, ("$R_t$", [("Put smaller numbers first", INK)], FWD["mark"], FWD["ink"])])
    ya = STA_Y0 + ha1 / 2
    cv.arrow([(ST_X[0] - 11.0, ya), (ST_X[0], ya)], color=FWD["mark"], lw=0.7, head=1.3)
    cv.text(ST_X[0] - 12.0, ya, "$h_{t-1}$", size=6.8, color=FWD["ink"], ha="right")
    cv.arrow([(ST_X[0] + SW, ya), (ST_X[1], ya)], color=FWD["mark"], lw=0.7, head=1.3)
    yc = TAU_Y1 + CHIP_OFF
    edge(cv, X_W1, TAU_Y1, STA_Y0, yc, 1, ("write ", "$R_{t-1}$", FWD), FWD)
    edge(cv, X_R1, STA_Y0, TAU_Y1, yc, 2, ("read ", "$R_{t-1}$", FWD), FWD)
    edge(cv, X_W2, TAU_Y1, STA_Y0, yc, 3, ("write ", "$R_t$", FWD), FWD)
    edge(cv, X_R2, STA_Y0, y31, yc, 4, ("read ", "$R_{t-1}$", FWD), FWD)
    px = ST_X[1] + SW + 2.4
    verdict(cv, px, STA_Y0 + 1.9, W - 3.6 - px, 9.2, False, ["$R_{t-1}$ persists,", r"misleads $\pi_D$ again"])

    # ---- (b) ReHarness: same forward row, plus the revision row ------------------------------------
    hb1 = state_h(1)
    state(cv, ST_X[0], STB_Y1 - hb1, "$h_t$", r"Memory agent $\pi_M$", [r_old])
    r_new = (r"$R^{\prime}_{t-1}$", [("Larger first ", INK), ("only if descending", REV["ink"])], REV["mark"], REV["ink"])
    state(cv, ST_X[1], STB_Y0, "$h_{t+1}$", r"Memory agent $\pi_M$",
          [r_new, ("$R_t$", [("Smaller first ", INK), ("only if ascending", FWD["ink"])], FWD["mark"], FWD["ink"])])
    yb = STB_Y1 - hb1 / 2
    cv.arrow([(ST_X[0] - 11.0, yb), (ST_X[0], yb)], color=REV["mark"], lw=0.7, head=1.3)
    cv.text(ST_X[0] - 12.0, yb, r"$h^{\prime}_{t-1}$", size=6.8, color=REV["ink"], ha="right")
    cv.text(5.2, SB_Y1 - 5.3, "adds backward revision", size=6.2, color=REV["ink"], style="italic", ha="left")
    yc = TAU_Y0 - CHIP_OFF
    edge(cv, X_W1, TAU_Y0, STB_Y1, yc, 1, ("write ", "$R_{t-1}$", FWD), FWD)
    edge(cv, X_R1, STB_Y1, TAU_Y0, yc, 2, ("read ", "$R_{t-1}$", FWD), FWD)
    edge(cv, X_W2, TAU_Y0, STB_Y1, yc, 4, ("write ", "$R_t$", FWD), FWD)
    edge(cv, X_R2, STB_Y1, y30, yc, 5, ("read ", r"$R^{\prime}_{t-1}$", REV), FWD)

    # the hero: h'_t shows the edit
    hx = X_MID - TW / 2
    card(cv, hx, REV_Y0, TW, REV_Y1 - REV_Y0, REV, r"$h^{\prime}_t$", r"Revision agent $\pi_R$", HH, body=REV["soft"],
         lw=1.0, shadow=True)
    ny = REV_Y1 - HH - NPAD - NOTE
    note(cv, hx + 1.1, ny, TW - 2.2, "$R_{t-1}$", [("Put larger numbers first", MUTED)], "#B9C0CA",
         label_color=MUTED, struck=True)
    ny -= NOTE + NGAP
    q0 = hx + 1.1 + 10.2 + cv.text_width("Larger first ", 6.5)
    qw = cv.text_width("only if descending", 6.5, "bold")
    cv.ax.add_patch(FancyBboxPatch((q0 - 0.25, ny + 0.45), qw + 0.75, NOTE - 0.9, boxstyle="round,pad=0,rounding_size=0.6",
                                   fc=REV["soft"], ec="none", zorder=5.5))
    note(cv, hx + 1.1, ny, TW - 2.2, r"$R^{\prime}_{t-1}$", [("Larger first ", INK), ("only if descending", REV["ink"], "bold")],
         REV["mark"], label_color=REV["ink"])
    edge(cv, X_MID, TAU_Y0, REV_Y1, REV_Y1 + 4.9, 3, ("revise ", "$R_{t-1}$", FWD), REV, lw=1.0)
    cv.arrow([(X_R1, STB_Y1 - hb1), (X_R1, REV_Y1)], color=REV["mark"], lw=0.8, head=1.4)
    cv.arrow([(X_W2, REV_Y1), (X_W2, STB_Y0)], color=REV["mark"], lw=0.8, head=1.4)

    # governing equations, instantiated for the example (Eqs. 2-3 with i = t-1)
    lx, ly = 5.4, (REV_Y0 + REV_Y1) / 2
    cv.text(lx, ly + 2.5, "Backward revision", size=7.4, weight="bold", color=REV["ink"], ha="left")
    cv.rich(lx, ly - 2.3, [(r"$R^{\prime}_{t-1}$", REV["ink"]), (r"$\,=\,\pi_R\,($", INK), (r"$R_{t-1}$", FWD["ink"]),
                           (r"$,\,\tau_{t-1};\ \tau_t)$", INK)], size=7.0)
    ex = ST_X[1] + SW + 3.0
    cv.rich(ex, STB_Y0 + 9.0, [(r"$R_t=\pi_M(\tau_t;\ $", INK), (r"$R^{\prime}_{t-1}$", REV["ink"]), ("$)$", INK)], size=6.8)
    cv.rich(ex, STB_Y0 + 4.2, [(r"$h_{t+1}=\,$", INK), (r"$h^{\prime}_t$", REV["ink"]), (r"$\,\oplus R_t$", INK)], size=6.8)
    px = hx + TW + 13.0
    verdict(cv, px, ly - 4.6, W - 5.0 - px, 9.2, True, [r"Revised $R^{\prime}_{t-1}$", r"guides $\pi_D$ correctly"])

    key(cv, 1.5, KEY_Y, W - 3.0, KEY_H)

    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=".")
    for p in render(ap.parse_args().out):
        print(p)
