"""Redesign of Fig. 5 of "Proactive AI for Superintelligent Agents": historical foundations.

Content from the source figure: seven traditions with their decades and one-sentence summaries, ending in
proactive AI agents and the six capacities.

Kept from the original: one illustrated card per tradition (the pictures carry each era: a control
console, a 1970s terminal, a phone in the street), numbered titles, and the hero card with the six
capacities, read in one pass. Fixed: the zig-zag spine spaced decades evenly and repeated "2000s-2010s"
twice with no sign that the eras overlap; here a span chart on a proportional axis shows when each tradition
was active (numbers match the cards, which stay in reading order), and every card ends in a legacy chip
coloured like the capacity it prepared. The era -> capacity reading follows the caption's four themes
(future consequences -> Anticipation, persistent goals -> Agenda, changing context -> Awareness, value of
intervention -> Arbitration); feedback control -> Adaptation and foundation models -> all six are our
reading, stated in the notes.

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
from matplotlib.patches import FancyBboxPatch  # noqa: E402

VIG = os.path.join(HERE, "vignettes")
NEU = dict(fill="#F3F4F6", soft="#E4E7EB", stroke="#8F98A4", ink="#353C47", mark="#5B6577")
PRO = "#2B2F6E"
ERAS = [  # vignette, decades, (start, end), title, summary, legacy text, capacity, (unused)
    ("e_control", "1940s–1950s", (1940, 1960), "Control and Cybernetics",
     "Feedback control and cybernetic principles laid the foundation for self-regulating systems.", "feedback", "Adaptation", "top"),
    ("e_planning", "1960s–1970s", (1960, 1980), "Planning and World Models",
     "Planning and world models let machines reason about future states and actions.", "future states", "Anticipation", "bottom"),
    ("e_bdi", "1980s–1990s", (1980, 2000), "BDI and Agent Theory",
     "Belief-desire-intention models formalized how agents reason and act toward goals.", "goals & intentions", "Agenda", "top"),
    ("e_ubiquitous", "1990s–2000s", (1990, 2010), "Ubiquitous and Context-Aware Computing",
     "Computing embedded in everyday life: systems that sense context and adapt.", "context", "Awareness", "bottom"),
    ("e_mixed", "2000s–2010s", (2000, 2020), "Mixed-Initiative Interaction",
     "User input combined with agent suggestions and actions for better decisions.", "when to step in", "Arbitration", "top"),
    ("e_goals", "2000s–2010s", (2000, 2020), "Goal Reasoning and Intrinsic Motivation",
     "How agents generate goals, prioritize, and pursue what matters.", "self-set goals", "Agenda", "bottom"),
    ("e_foundation", "2010s–2020s", (2010, 2025), "Foundation Models and Tool-Using Agents",
     "LLMs and tools enabled flexible reasoning and execution across real-world tasks.", "all six", None, "top"),
]
SHORT = ["Control & cybernetics", "Planning & world models", "BDI & agent theory", "Ubiquitous & context-aware",
         "Mixed-initiative interaction", "Goal reasoning & motivation", "Foundation models"]
LANE = [0, 0, 0, 1, 0, 2, 1]
FOCUS = {"e_planning": (0.5, 0.2), "e_ubiquitous": (0.5, 0.18)}  # keep the people's heads in the crop  # span-chart lane per era, so overlapping eras never share a lane
CW, CH, GH = 42.5, 44.0, 22.0
W, H = 178, 1.0 + GH + 3.0 + 2 * CH + 2.0 + 1.0
Y0, Y1, TX0, TX1 = 1940, 2032, 5.0, 176.0


def xs(year):
    return TX0 + (year - Y0) / (Y1 - Y0) * (TX1 - TX0)


def rbox(cv, x, y, w, h, fc, ec="none", lw=0.0, r=1.4, z=5):
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))


def era_card(cv, x, y, k, era):
    vig, dec, _, title, summ, leg, cap, _ = era
    c = SIXA[cap] if cap else NEU
    rbox(cv, x, y, CW, CH, "white", c["stroke"], 0.6, r=1.8, z=3)
    vh = 19.0
    cv.image(os.path.join(VIG, vig + ".jpg"), x + CW / 2, y + CH - 0.8 - vh / 2, CW - 1.6, fit="cover", h=vh,
             radius=1.2, focus=FOCUS.get(vig, (0.5, 0.5)), z=5)
    x0, _ = cv.chip(x + 1.6, y + CH - 3.4, f"{k}  ·  {dec}", c, size=6.6, h=3.8, pad=1.0, solid=True, z=8, ha="left")
    ty = y + CH - vh - 2.8
    lines = textwrap.wrap(title, 28, break_on_hyphens=False)
    cv.text(x + 1.6, ty, "\n".join(lines), size=7.6, weight="bold", color=c["ink"], ha="left", va="top", linespacing=1.05)
    sy = ty - len(lines) * 3.1 - 0.9
    cv.text(x + 1.6, sy, "\n".join(textwrap.wrap(summ, 37, break_on_hyphens=False)), size=6.5, color=INK, ha="left", va="top", linespacing=1.12)
    cv.chip(x + 1.6, y + 3.0, "→ " + leg, c, size=6.6, h=3.8, pad=1.0, solid=True, z=8, ha="left")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.2)
    # ---- span chart: when each tradition was active (overlaps read directly, no leaders) ----------------
    gy = H - 1.0 - GH
    rbox(cv, 1.0, gy, W - 2.0, GH, "#F6F7F9", "#D5D9DF", 0.5, r=1.8, z=1)
    base = gy + 4.6
    for yr in range(1940, 2031, 10):
        cv.line([(xs(yr), base - 0.6), (xs(yr), gy + GH - 1.2)], color="#DDE1E6", lw=0.4, z=2)
        cv.text(xs(yr), base - 2.2, str(yr), size=6.2, color=MUTED)
    lh = 5.0
    for k, (era, short, lane) in enumerate(zip(ERAS, SHORT, LANE)):
        c = SIXA[era[6]] if era[6] else NEU
        s, e = era[2]
        y = base + 0.6 + (2 - lane) * (lh + 0.6)
        rbox(cv, xs(s) + 0.3, y, xs(e) - xs(s) - 0.6, lh, c["mark"], r=lh / 2, z=4)
        cv.text(xs(s) + 2.0, y + lh / 2, f"{k + 1}  {short}", size=6.4, weight="bold", color="white", ha="left", z=6)
    y = base + 0.6 + 2 * (lh + 0.6)
    rbox(cv, xs(2021) + 0.3, y, xs(2032) - xs(2021) - 0.9, lh, PRO, r=lh / 2, z=4)
    cv.text((xs(2021) + xs(2032)) / 2, y + lh / 2, "8  Proactive AI", size=6.4, weight="bold", color="white", z=6)
    # ---- cards in reading order 1-7, then the hero ---------------------------------------------------
    gap = (W - 2.0 - 4 * CW) / 3
    for k, era in enumerate(ERAS):
        r, col = divmod(k, 4)
        x = 1.0 + col * (CW + gap)
        y = gy - 3.0 - (r + 1) * CH - r * 2.0
        era_card(cv, x, y, k + 1, era)
    x, y = 1.0 + 3 * (CW + gap), gy - 3.0 - 2 * CH - 2.0
    rbox(cv, x, y, CW, CH, "#EEEEF7", "#9EA1CC", 0.7, r=1.8, z=3)
    vh = 19.0
    cv.image(os.path.join(VIG, "e_hero.jpg"), x + CW / 2, y + CH - 0.8 - vh / 2, CW - 1.6, fit="cover", h=vh,
             radius=1.2, focus=(0.5, 0.4), z=5)
    cv.chip(x + 1.6, y + CH - 3.4, "8  ·  2020s", dict(mark=PRO, stroke=PRO, soft=PRO, ink=PRO), size=6.6, h=3.8, pad=1.0,
            solid=True, z=8, ha="left")
    cv.text(x + 1.6, y + CH - vh - 2.8, "Proactive AI agents", size=7.6, weight="bold", color=PRO, ha="left", va="top")
    cv.text(x + 1.6, y + CH - vh - 6.6, "inherit all six capacities:", size=6.5, color=INK, ha="left", va="top")
    cw2 = (CW - 4.2) / 2
    for i, n in enumerate(NAMES):
        cx = x + 1.6 + (i % 2) * (cw2 + 1.0)
        cy = y + 13.4 - (i // 2) * 4.6
        rbox(cv, cx, cy - 1.9, cw2, 3.8, SIXA[n]["mark"], r=1.9, z=5)
        cv.text(cx + cw2 / 2, cy, n, size=6.4, weight="bold", color="white", z=6)
    assert not cv.overlaps() and not cv.text_overlaps(), cv.overlaps() + cv.text_overlaps()
    print("\n".join(cv.save(os.path.join(a.out, "proactive_history"))))


if __name__ == "__main__":
    main()
