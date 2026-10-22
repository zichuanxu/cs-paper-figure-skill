"""Redesign of Fig. 5 of "Proactive AI for Superintelligent Agents": historical foundations.

Content from the source figure: seven traditions with their decades and one-sentence summaries, ending in
proactive AI agents and the six capacities. Changes: a proportional time axis (the source spaces decades
evenly and zig-zags), each era drawn as a span on its own lane with a leader line to its card, and a
legacy chip per era coloured like the capacity it prepared. The era -> capacity reading follows the
caption's four themes (future consequences -> Anticipation, persistent goals -> Agenda, changing
context -> Awareness, value of intervention -> Arbitration); feedback control -> Adaptation and
foundation models -> all six are our reading, stated in the notes.

    python render_history.py --out <dir>
"""
import argparse
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sixa import NAMES, SIXA  # noqa: E402
from paperkit import Canvas, INK, MUTED  # noqa: E402

ART = os.path.join(HERE, "art")
NEU = dict(fill="#F3F4F6", soft="#E4E7EB", stroke="#8F98A4", ink="#353C47", mark="#5B6577")
ERAS = [  # key, decades, (start, end), title, summary, legacy text, capacity, row, slot
    ("control", "1940s–1950s", (1940, 1960), "Control and Cybernetics",
     "Feedback control and cybernetic principles laid the foundation for self-regulating systems.", "feedback", "Adaptation", "top", 0),
    ("planning", "1960s–1970s", (1960, 1980), "Planning and World Models",
     "Planning and world models let machines reason about future states and actions.", "future states", "Anticipation", "bottom", 0),
    ("bdi", "1980s–1990s", (1980, 2000), "BDI and Agent Theory",
     "Belief-desire-intention models formalized how agents reason and act toward goals.", "goals & intentions", "Agenda", "top", 1),
    ("ubiquitous", "1990s–2000s", (1990, 2010), "Ubiquitous and Context-Aware Computing",
     "Computing embedded in everyday life: systems that sense context and adapt.", "context", "Awareness", "bottom", 1),
    ("mixed", "2000s–2010s", (2000, 2020), "Mixed-Initiative Interaction",
     "User input combined with agent suggestions and actions for better decisions.", "when to step in", "Arbitration", "top", 2),
    ("goals", "2000s–2010s", (2000, 2020), "Goal Reasoning and Intrinsic Motivation",
     "How agents generate goals, prioritize, and pursue what matters.", "self-set goals", "Agenda", "bottom", 2),
    ("foundation", "2010s–2020s", (2010, 2025), "Foundation Models and Tool-Using Agents",
     "LLMs and tools enabled flexible reasoning and execution across real-world tasks.", "all six", None, "top", 3),
]
W, H = 178, 100
AX0, AX1, Y0, Y1 = 6.0, 150.0, 1940, 2025


def xs(year):
    return AX0 + (year - Y0) * (AX1 - AX0) / (Y1 - Y0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.0)
    axis_y = 52.0
    cv.line([(AX0, axis_y), (AX1 + 2.0, axis_y)], color="#4B5563", lw=0.9)
    for yr in range(1940, 2030, 10):
        cv.line([(xs(yr), axis_y - 0.9), (xs(yr), axis_y + 0.9)], color="#4B5563", lw=0.6)
        cv.text(xs(yr), axis_y - 7.6, str(yr), size=5.9, color=MUTED)
    # top-row eras draw their spans above the axis, bottom-row eras below, so leaders never cross a bar;
    # each leader lands at a year inside its span, clear of the decade labels
    lane = {"control": 0, "bdi": 0, "mixed": 0, "foundation": 1, "planning": 0, "ubiquitous": 0, "goals": 1}
    land = {"control": 1948, "bdi": 1988, "mixed": 2005, "foundation": 2018, "planning": 1968, "ubiquitous": 1994,
            "goals": 2014}
    card_w, card_h, gap = 34.0, 31.0, 2.67
    for key, dec, (s, e), title, summary, legacy, cap, row, slot in ERAS:
        c = SIXA[cap] if cap else NEU
        top = row == "top"
        ly = axis_y + (2.4 + lane[key] * 2.4) * (1 if top else -1)
        cv.ax.plot([xs(s) + 0.6, xs(e) - 0.6], [ly, ly], color=c["mark"], lw=4.0, solid_capstyle="round", zorder=7)
        x = AX0 + slot * (card_w + gap) + (0 if top else 17.0)
        y = 66.0 if top else 4.0
        cv.box(x, y, card_w, card_h, "neutral", fill="white", stroke=c["stroke"], lw=0.7, radius=1.8)
        p = os.path.join(ART, f"era_{key}.png")
        if os.path.exists(p):
            cv.image(p, x + 4.8, y + card_h - 5.2, 7.4, fit="box")
        cv.text(x + 9.8, y + card_h - 2.8, dec, size=5.9, color=MUTED, ha="left")
        tl = textwrap.wrap(title, 19)
        for j, t in enumerate(tl):
            cv.text(x + 9.8, y + card_h - 5.8 - j * 2.8, t, size=6.7, weight="bold", color=c["ink"], ha="left")
        sy = y + card_h - 5.8 - max(len(tl), 2) * 2.8 - 1.8
        for j, t in enumerate(textwrap.wrap(summary, 34)):
            cv.text(x + 1.8, sy - j * 2.6, t, size=5.9, color=INK, ha="left")
        cv.chip(x + 1.8, y + 3.2, "→ " + legacy, c, size=6.0, ha="left", pad=0.9)
        lx, cx = xs(land[key]), x + card_w / 2
        if top:
            cv.line([(cx, y), (cx, 62.5), (lx, 62.5), (lx, ly + 1.0)], color=c["stroke"], lw=0.55, radius=0.8)
        else:
            cv.line([(cx, y + card_h), (cx, 39.0), (lx, 39.0), (lx, ly - 1.0)], color=c["stroke"], lw=0.55, radius=0.8)
    # hero: what these traditions add up to
    hx, hw = 154.0, 22.0
    cv.arrow([(AX1 + 2.0, axis_y), (hx - 0.6, axis_y)], color="#4B5563", lw=0.9, head=1.3)
    cv.box(hx, 4.0, hw, 93.0, "neutral", fill="#F7F8FB", stroke="#5A5FA8", lw=0.9, radius=2.2)
    cv.text(hx + hw / 2, 8.6, "chip colour =", size=5.9, color=MUTED, style="italic")
    cv.text(hx + hw / 2, 6.2, "capacity it prepared", size=5.9, color=MUTED, style="italic")
    cv.text(hx + hw / 2, 91.0, "Proactive", size=8.0, weight="bold", color="#2B2F6E")
    cv.text(hx + hw / 2, 87.4, "AI agents", size=8.0, weight="bold", color="#2B2F6E")
    cv.text(hx + hw / 2, 83.6, "2020s", size=6.0, color=MUTED)
    for k, name in enumerate(NAMES):
        c = SIXA[name]
        yy = 77.0 - k * 11.6
        icon = {"Awareness": "aware", "Anticipation": "anticipate", "Agenda": "agenda", "Arbitration": "arbitrate",
                "Action": "act", "Adaptation": "adapt"}[name]
        p = os.path.join(ART, icon + ".png")
        if os.path.exists(p):
            cv.image(p, hx + hw / 2, yy + 1.8, 6.4, fit="box")
        cv.chip(hx + hw / 2, yy - 3.6, name, c, size=6.2, pad=0.9)
    print("\n".join(cv.save(os.path.join(a.out, "proactive_history"))))


if __name__ == "__main__":
    main()
