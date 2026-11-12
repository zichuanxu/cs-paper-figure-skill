"""Proactive versus reactive AI agents: a from-scratch design of Figure 1 of
"Proactive AI for Superintelligent Agents" (Yang et al.).

Source. Figure 1 and its caption: "Reactive agents rely on users to identify the work and request action.
Proactive agents can recognize emerging needs and initiate useful work before being asked, learning from
outcomes and feedback."

Content kept from the source
* Reactive agent: the exchange "How is the report going?" / "Here is the latest update", and the rule
  "Act when asked: act to fulfill the goal from the prompt."
* Proactive agent: the six numbered capacities in order, each with the source's definition, word for word:
  continuously monitor context; identify / infer gaps between current progress & intended state; generate
  candidate goals to address gaps (with the five listed goals); decide whether initiative is worthwhile,
  timely, and safe; suggest, assist, or execute before being asked; learn from outcomes and feedback.
* Topology: 1 -> 2 -> 3 -> 4 -> 5 -> outcome -> 6, and 6 back to each of the five ("Adaptation uses outcomes
  and feedback to update the other capacities", Fig. 6 caption).
* Stage names are the paper's six A's (Section 4), as in every other figure of the series; the source figure
  mixes parts of speech (Aware, Anticipate, Agenda, Arbitrate, Act, Adaptation).

Design decisions
* Contrast as a matrix (visual-craft section 13, transposed): two rows (reactive, proactive) over three shared
  columns named once in a header strip: who identifies the work and initiates action, the act, the outcome.
  The reactive row is the narrow, neutral baseline; the proactive row is tall and carries the colour.
* The source's own parallel is made positional: "Act when asked" sits directly above "Action ... before being
  asked", and the two outcomes end on matching pills ("when asked" / "before being asked").
* The four columns that the proactive agent fills with Awareness, Anticipation, Agenda and Arbitration are, in
  the reactive row, the user's turn: her picture, her prompt, and a note that the agent waits until then.
* Each capacity takes its hue from the series palette (sixa.SIXA) on a solid header, the card frame, its
  object panel and its chevron. Grey means reactive, near-black means the proactive agent as a whole, so no
  hue has two meanings.
* Each definition ends in an object made from its own words: a progress bar with the gap left open, the five
  candidate goals as a checklist, three ticked tests, three modes on a lightness ramp. Awareness lists three
  kinds of context the paper names in Section 3.4 (calendar, current task, screen state), marked "e.g.".
* Adaptation is a rail under the row with its vignette standing on the right end, under the outcome: outcomes
  and feedback enter there (solid), and the rail returns to every capacity (dashed, keyed on the rail), so no
  feedback line crosses a card.
* Illustrations are the series' text-free vignettes; every word is vector text.

    python render_overview.py --out DIR   ->  DIR/proactive_overview.{pdf,svg,png}
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle  # noqa: E402

from paperkit import HAIR, MUTED, Canvas, mix  # noqa: E402
from sixa import SIXA  # noqa: E402

VIG = os.path.join(HERE, "vignettes")
STEM = "proactive_overview"

# grey = the reactive baseline; near-black = the proactive agent as a whole (title tab, outcome)
REACT = dict(fill="#F4F5F7", soft="#E6E8EC", stroke="#8C95A1", ink="#3A4250", mark="#5E6875")
PRO = dict(fill="#F4F5F7", soft="#E6E8EC", stroke="#262B33", ink="#262B33", mark="#262B33")

W, M, TABW, G, RAD = 178.0, 1.2, 8.4, 3.0, 1.8
X0 = M + TABW + 1.6
CW = (W - M - X0 - 5 * G) / 6                       # one of six equal columns
COL = [X0 + i * (CW + G) for i in range(6)]
PH, RR, GAP, HEAD, PIC, BODY, RAIL = 4.4, 25.6, 5.2, 6.2, 21.5, 22.8, 12.5
CARD = HEAD + PIC + BODY
Y_RAIL = M
Y_CARD = Y_RAIL + RAIL + GAP
Y_R = Y_CARD + CARD + GAP                           # reactive row bottom
Y_PH = Y_R + RR + 1.6
H = Y_PH + PH + M
T_HEAD, T_BODY, T_SMALL = 9.6, 6.9, 6.0

# name, vignette, focus, definition stem, object kind, object items
STAGES = [
    ("Awareness", "f1_aware", (0.5, 0.45), "Continuously monitor\ncontext, e.g.", "dot",
     ["calendar", "current task", "screen state"]),
    ("Anticipation", "f1_anticipate", (0.5, 0.30), "Identify / infer gaps\nbetween", "gap",
     ["current progress", "intended state"]),
    ("Agenda", "f1_agenda", (0.5, 0.42), "Generate candidate\ngoals to address gaps", "box",
     ["Draft report", "Update charts", "Prepare summary", "Review data", "Schedule meeting"]),
    ("Arbitration", "f1_arbitrate", (0.5, 0.50), "Decide whether\ninitiative is", "tick",
     ["worthwhile", "timely", "safe"]),
    ("Action", "f1_act", (0.5, 0.52), "Before being asked,", "ramp",
     ["suggest", "assist", "or execute"]),
]


def picture(cv, name, x, y, w, h, c, **kw):
    """Full-bleed vignette in the rect (x, y, w, h); a tinted panel with the vector robot if the file is absent."""
    path = os.path.join(VIG, name + ".jpg")
    if os.path.exists(path):
        cv.image(path, x + w / 2, y + h / 2, w, fit="cover", h=h, **kw)
    else:
        cv.ax.add_patch(Rectangle((x, y), w, h, fc=c["soft"], ec="none", zorder=11))
        cv.icon_robot(x + w / 2, y + h / 2, min(w, h) * 0.5, color=c["ink"])


def frame(cv, x, y, w, h, c, lw=0.8):
    """Card outline redrawn above the picture, which otherwise covers the card's own stroke."""
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={RAD}", fc="none",
                                   ec=c["mark"], lw=lw, zorder=13))


def header(cv, x, ytop, w, c, name, num=None, size=T_HEAD):
    """Solid header in the role's mark: white bold name, the stage number on a white disc."""
    cv.ax.add_patch(FancyBboxPatch((x, ytop - HEAD - RAD), w, HEAD + RAD, boxstyle=f"round,pad=0,rounding_size={RAD}",
                                   fc=c["mark"], ec="none", zorder=6))  # the picture below hides the lower corners
    tw, d = cv.text_width(name, size, "bold"), (3.8 if num else 0.0)
    x0 = x + (w - tw - d - (0.9 if num else 0.0)) / 2
    yc = ytop - HEAD / 2
    if num:
        cv.ax.add_patch(Circle((x0 + d / 2, yc), d / 2, fc="white", ec="none", zorder=7))
        cv.text(x0 + d / 2, yc - 0.05, str(num), size=7.6, weight="bold", color=c["ink"], z=8)
        x0 += d + 0.9
    cv.text(x0, yc - 0.05, name, size=size, weight="bold", color="white", ha="left", z=8)


def pill(cv, cx, cy, s, c, size=6.6, h=4.0):
    w = cv.text_width(s, size, "bold") + 3.2
    cv.ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                   fc=c["mark"], ec="none", zorder=14))
    cv.text(cx, cy - 0.05, s, size=size, weight="bold", color="white", z=15)


def chevron(cv, xgap, y, c):
    """Stage-to-stage flow: a solid chevron in the gutter, in the colour of the stage it leaves."""
    cv.ax.add_patch(Polygon([(xgap + 0.45, y + 1.9), (xgap + G - 0.45, y), (xgap + 0.45, y - 1.9)], closed=True,
                            fc=c["mark"], ec="none", zorder=9))


def rows(cv, x, yc, items, c, kind, pitch):
    """A short list inside an object panel: one glyph per row (dot, checkbox, tick, lightness ramp) and its word."""
    n = len(items)
    for k, s in enumerate(items):
        y = yc + (n - 1) / 2 * pitch - k * pitch
        gx = x + 1.5
        if kind == "dot":
            cv.ax.add_patch(Circle((gx, y), 0.55, fc=c["mark"], ec="none", zorder=9))
        elif kind == "box":
            cv.ax.add_patch(FancyBboxPatch((gx - 0.8, y - 0.8), 1.6, 1.6, boxstyle="round,pad=0,rounding_size=0.3",
                                           fc="white", ec=c["stroke"], lw=0.6, zorder=9))
        elif kind == "tick":
            cv.icon_check(gx, y, 1.8, color=c["mark"], lw=1.0, z=9)
        elif kind == "ramp":  # lighter to darker = more of the work done by the agent
            cv.ax.add_patch(FancyBboxPatch((gx - 0.85, y - 0.85), 1.7, 1.7, boxstyle="round,pad=0,rounding_size=0.3",
                                           fc=mix(c["soft"], c["mark"], k / (n - 1)), ec=c["stroke"], lw=0.5, zorder=9))
        cv.text(x + 3.4, y - 0.05, s, size=T_SMALL, color=c["ink"], ha="left", z=10)


def gap_bar(cv, x0, x1, yc, c, labels):
    """Progress bar whose unfilled, dashed remainder is the gap; the far end is the intended state."""
    xm, hb = x0 + (x1 - x0) * 0.56, 2.9
    cv.ax.add_patch(Rectangle((x0, yc - hb / 2), xm - x0, hb, fc=c["mark"], ec="none", zorder=9))
    cv.ax.add_patch(Rectangle((xm, yc - hb / 2), x1 - xm, hb, fc="white", ec=c["stroke"], lw=0.6,
                              ls=(0, (2.2, 1.4)), zorder=9))
    cv.ax.plot([x1, x1], [yc - hb / 2 - 1.0, yc + hb / 2 + 1.0], color=c["ink"], lw=1.0, zorder=10,
               solid_capstyle="round")
    cv.text((xm + x1) / 2, yc - 0.05, "gap", size=T_SMALL, weight="bold", color=c["ink"], z=10)
    cv.text(x0, yc + 3.7, labels[0], size=T_SMALL, color=c["ink"], ha="left", z=10)
    cv.text(x1, yc - 3.8, labels[1], size=T_SMALL, color=c["ink"], ha="right", z=10)


def stage_card(cv, i, name, vig, focus, stem, kind, items):
    c, x, y, top = SIXA[name], COL[i], Y_CARD, Y_CARD + CARD
    cv.box(x, y, CW, CARD, c, stroke=c["mark"], lw=0.8, radius=RAD)
    header(cv, x, top, CW, c, name, num=i + 1)
    picture(cv, vig, x, top - HEAD - PIC, CW, PIC, c, focus=focus)
    frame(cv, x, y, CW, CARD, c)
    cv.text(x + CW / 2, top - HEAD - PIC - 3.9, stem, size=T_BODY, color=c["ink"], linespacing=1.12, z=10,
            weight="bold" if kind == "ramp" else "normal")
    px, py, pw, ph = x + 1.1, y + 1.0, CW - 2.2, 14.0
    cv.box(px, py, pw, ph, c, fill="white", lw=0.45, radius=1.2, container=True)
    if kind == "gap":
        gap_bar(cv, px + 1.8, px + pw - 1.8, py + ph / 2, c, items)
    else:
        rows(cv, px + 1.2, py + ph / 2, items, c, kind, 2.55 if len(items) > 3 else 3.7)


def say(cv, cx, cy, s, tail, c, **kw):
    """cv.bubble with a side tail, plus a white stroke over the joint: paperkit leaves the tail's closing edge
    visible there as a hairline across the mouth of the tail."""
    x, y, w, h = cv.bubble(cx, cy, s, tail=tail, r=c, size=7.8, **kw)
    bx, by = (x if tail[0] < x else x + w), min(max(tail[1], y + 1.6), y + h - 1.6)
    cv.ax.plot([bx, bx], [by - 0.78, by + 0.78], color="white", lw=1.3, zorder=14.2, solid_capstyle="butt")
    return x, y, w, h


def reactive_row(cv):
    c, y, top = REACT, Y_R, Y_R + RR
    # the user's turn: columns 1-4
    uw, pw = 2 * CW + G, 31.0
    cv.box(COL[0], y, uw, RR, c, radius=RAD)
    picture(cv, "f1_reactive", COL[0] + uw - pw - 0.5, y + 0.5, pw, RR - 1.0, c, radius=1.4,
            focus=(0.30, 0.42), zoom=1.67)
    tx = COL[0] + 1.9
    cv.text(tx, y + RR / 2 + 3.6, "The user", size=7.6, weight="bold", color=c["ink"], ha="left")
    cv.text(tx, y + RR / 2 - 1.4, "identifies the work\nand requests action", size=T_BODY, color=c["ink"],
            ha="left", linespacing=1.15)
    ask_y, pr = top - 4.6, COL[1] + CW - 0.5      # her bubble overlaps the picture's corner, the tail ends at her face
    bx, _, bw, _ = say(cv, 0, ask_y, "How is the report going?", (pr - 9.6, top - 10.2), c, left=pr - 6.6)
    cv.arrow([(bx + bw, ask_y), (COL[4], ask_y)], color=c["mark"], lw=0.8)
    cv.text((bx + bw + COL[4]) / 2, ask_y - 1.9, "prompt", size=T_SMALL, style="italic", color=MUTED)
    cv.icon_clock(pr + 4.6, y + 7.6, 3.0, color=c["mark"])
    cv.text(pr + 7.2, y + 7.6, "until then,\nthe agent waits", size=T_SMALL, style="italic", color=MUTED, ha="left",
            linespacing=1.1)
    # the agent's turn: column 5, aligned with Action below
    x = COL[4]
    cv.box(x, y, CW, RR, c, stroke=c["mark"], lw=0.8, radius=RAD)
    header(cv, x, top, CW, c, "Act when asked", size=9.0)
    rp = 12.0
    picture(cv, "f1_reactive", x, top - HEAD - rp, CW, rp, c, focus=(0.80, 0.29), zoom=2.0)
    frame(cv, x, y, CW, RR, c)
    cv.text(x + CW / 2, y + (RR - HEAD - rp) / 2, "Act to fulfill the goal\nfrom the prompt.", size=T_BODY,
            color=c["ink"], linespacing=1.12)
    rw = cv.text_width("Here is the latest update", 7.8) + 3.2
    say(cv, x - 1.6 - rw / 2, y + 7.6, "Here is the latest update", (x + 6.4, y + 12.6), c)
    # what the user gets: column 6
    dw, dh = 9.5, 11.5
    dx, dy = COL[5] + (CW - dw) / 2, top - 1.4 - dh
    cv.doc(dx, dy, dw, dh, c, lines=5)
    cv.arrow([(x + CW, dy + dh / 2), (dx, dy + dh / 2)], color=c["mark"], lw=0.8)
    cv.text(COL[5] + CW / 2, dy - 2.4, "The latest update", size=T_BODY, color=c["ink"])
    pill(cv, COL[5] + CW / 2, y + 3.0, "when asked", c)


ADAPT_PIC = 22.0            # height of the Adaptation vignette at the rail's right end
OUT_H = HEAD + PIC + 11.4   # the outcome card is shorter than a stage card: the feedback edge leaves below it


def outcome_card(cv):
    c, x, top, ph = PRO, COL[5], Y_CARD + CARD, HEAD + PIC
    y = top - OUT_H
    cv.box(x, y, CW, OUT_H, c, stroke=c["mark"], lw=0.8, radius=RAD)
    picture(cv, "f1_outcome", x, top - ph, CW, ph, c, radius=RAD, focus=(0.5, 0.5))
    frame(cv, x, y, CW, OUT_H, c)
    cv.text(x + CW / 2, top - ph - 3.4, "Useful work arrives", size=T_BODY, color=c["ink"])
    pill(cv, x + CW / 2, top - ph - 8.3, "before being asked", c)


def adaptation_rail(cv):
    c, x, y, w = SIXA["Adaptation"], COL[0], Y_RAIL, COL[5] + CW - COL[0]
    cv.box(x, y, w, RAIL, c, stroke=c["mark"], lw=0.8, radius=RAD)
    bw = 31.0
    cv.ax.add_patch(FancyBboxPatch((x, y), bw, RAIL, boxstyle=f"round,pad=0,rounding_size={RAD}", fc=c["mark"],
                                   ec="none", zorder=6))
    tw, d, yc = cv.text_width("Adaptation", T_HEAD, "bold"), 3.8, y + RAIL / 2
    hx = x + (bw - tw - d - 0.9) / 2
    cv.ax.add_patch(Circle((hx + d / 2, yc), d / 2, fc="white", ec="none", zorder=7))
    cv.text(hx + d / 2, yc - 0.05, "6", size=7.6, weight="bold", color=c["ink"], z=8)
    cv.text(hx + d + 0.9, yc - 0.05, "Adaptation", size=T_HEAD, weight="bold", color="white", ha="left", z=8)
    cv.text(x + bw + 3.0, yc, "Learn from outcomes and feedback", size=7.6, color=c["ink"], ha="left")
    lx = COL[3] + 9.0   # key for the dashed returns
    cv.arrow([(lx, yc - 2.0), (lx, yc + 2.0)], color=c["mark"], lw=0.8, head=1.2, dashed=True)
    cv.text(lx + 1.8, yc, "updates the other capacities", size=T_SMALL, style="italic", color=c["ink"], ha="left")
    # the agent reviewing what worked: a full vignette standing on the rail's end, under the outcome it learns from
    picture(cv, "f1_adapt", COL[5], y, CW, ADAPT_PIC, c, radius=RAD, focus=(0.5, 0.47))
    frame(cv, COL[5], y, CW, ADAPT_PIC, c)
    for i in range(5):  # Adaptation -> every capacity
        xc = COL[i] + CW / 2
        cv.arrow([(xc, y + RAIL), (xc, Y_CARD)], color=c["mark"], lw=0.8, head=1.3, dashed=True)
    xa, ya = COL[5] + 5.0, Y_CARD + CARD - OUT_H  # outcome -> Adaptation
    cv.arrow([(xa, ya), (xa, y + ADAPT_PIC)], color=c["mark"], lw=1.1, head=1.6)
    cv.text(xa + 1.9, (ya + y + ADAPT_PIC) / 2 + 0.3, "outcomes\nand feedback", size=T_SMALL, style="italic", color=c["ink"],
            ha="left", linespacing=1.1)


def draw(out):
    cv = Canvas(W, H, size=T_BODY)
    # shared columns, named once
    for x0, x1, s in ((COL[0], COL[3] + CW, "Identify the work and initiate action"), (COL[4], COL[4] + CW, "Act"),
                      (COL[5], COL[5] + CW, "Outcome")):
        cv.box(x0, Y_PH, x1 - x0, PH, REACT, s, fill=REACT["soft"], lw=0, stroke="none", radius=PH / 2, size=7.6,
               container=True)
    # row titles
    for y, h, c, big, s in ((Y_R, RR, REACT, 10.5, "Reactive"), (Y_RAIL, Y_CARD + CARD - Y_RAIL, PRO, 12.5, "Proactive")):
        cv.tab(M, y, TABW, h, c, "", solid=True, radius=RAD)
        cv.text(M + TABW * 0.38, y + h / 2, s, size=big, weight="bold", color="white", rotation=90)
        cv.text(M + TABW * 0.80, y + h / 2, "AI agent", size=7.2, color="white", rotation=90)
    cv.line([(M, Y_R - GAP / 2), (W - M, Y_R - GAP / 2)], color=HAIR, lw=0.7, dashed=True)

    reactive_row(cv)
    for i, st in enumerate(STAGES):
        stage_card(cv, i, *st)
        chevron(cv, COL[i] + CW, Y_CARD + CARD - HEAD - PIC / 2, SIXA[st[0]])
    outcome_card(cv)
    adaptation_rail(cv)

    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=".")
    print(f"{W:.0f} x {H:.1f} mm", draw(ap.parse_args().out))
