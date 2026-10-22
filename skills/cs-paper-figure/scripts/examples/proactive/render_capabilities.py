"""Redesign of Fig. 3 of "Proactive AI for Superintelligent Agents": from complementary capabilities to earned
autonomy.

Content from the source figure: three examples of acting before being asked (coding agent: unreported bug ->
discovered and fixed without being asked; risk detection: smoke detected (overheating) -> risk resolved and
safe; household robot: supply low, need restock -> items ordered and delivered); a low / high grid for
intelligence, alignment and proactiveness with the paper's first-person lines; "Trust earned?" leading to
autonomy, from "need permission before acting" to "act independently within guardrails".

Kept from the original: the hero scene, current -> goal pairs, solid Low / High headers, one robot per cell
with its line in a speech bubble, the autonomy row. Fixed: every cell is a full-bleed scene of one cast
(the original mixed cut-out robots, photos and icons), the lines are vector text, the example states carry
no baked-in text, and all labels are at least 6.2 pt.

    python render_capabilities.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sixa  # noqa: E402,F401  (puts paperkit on the path)
from paperkit import Canvas, INK, MUTED, mix  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Polygon  # noqa: E402

VIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vignettes")
# Low / High in neutral warm grey and the proactive indigo, so they never read as a capacity colour
LOW = dict(mark="#8C7B70", fill="#F5F1EE", stroke="#CDBFB5", ink="#5A4A40")
HIGH = dict(mark="#2B2F6E", fill="#EEEFF8", stroke="#A3A6CF", ink="#2B2F6E")
SLATE = "#3F4A5A"
EXAMPLES = [  # (title, current vignette, current label, goal vignette, goal label)
    ("Example 1 · Coding agent", "s_bug", "Unreported\nbug", "s_fixed", "Found & fixed\nwithout being\nasked"),
    ("Example 2 · Risk detection", "s_smoke", "Smoke detected\n(overheating)", "s_safe", "Risk resolved\n& safe"),
    ("Example 3 · Household robot", "s_low", "Supply low,\nneed restock", "s_delivered", "Items ordered\n& delivered"),
]
ROWS = [  # (capability, gloss, low vignette, low line, high vignette, high line)
    ("Intelligence", "understanding and\nreasoning", "r_int_low", "Wait – what\nshould I do?", "r_int_high", "I've got this."),
    ("Alignment", "aligning actions with the\nuser's intents, values\nand constraints", "r_ali_low",
     "Get the result.\nHowever it takes.", "r_ali_high", "I'll succeed, and\nsucceed cleanly."),
    ("Proactiveness", "taking the initiative\nto act", "r_pro_low", "Plans broken.\nWaiting for your call\non what to do next.",
     "r_pro_high", "Plan shifted, so I started\nworking a way around it,\nopen to your steer."),
]
W, H = 178, 136


def rbox(cv, x, y, w, h, fc, ec="none", lw=0.0, r=1.4, z=5):
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.4)
    # ---- top: hero + three examples of acting unasked -------------------------------------------------
    ty, th = 99.0, H - 1.0 - 99.0
    hw = 44.0
    cv.image(os.path.join(VIG, "hero.jpg"), 1.0 + hw / 2, ty + th / 2, hw, fit="cover", h=th, radius=1.8,
             focus=(0.5, 0.45), z=5)
    ew = (W - 1.0 - (1.0 + hw + 2.4) - 2 * 1.8) / 3
    for k, (title, cur, cl, goal, gl) in enumerate(EXAMPLES):
        x = 1.0 + hw + 2.4 + k * (ew + 1.8)
        rbox(cv, x, ty, ew, th, "#F4F6F9", "#C3CAD4", 0.6, r=1.8, z=3)
        rbox(cv, x + 1.2, ty + th - 5.6, ew - 2.4, 4.4, SLATE, r=2.2, z=4)
        cv.text(x + ew / 2, ty + th - 3.4, title, size=6.8, weight="bold", color="white", z=6)
        s = 15.0
        for j, (vig, lab, hdr) in enumerate(((cur, cl, "current"), (goal, gl, "goal"))):
            cx = x + 1.4 + s / 2 + j * (ew - 2.8 - s)
            cy = ty + th - 9.0 - s / 2 - 1.6
            cv.text(cx, ty + th - 8.4, hdr, size=6.2, color=MUTED, style="italic")
            cv.image(os.path.join(VIG, vig + ".jpg"), cx, cy, s, fit="cover", h=s, radius=1.2, z=5)
            cv.text(cx, ty + 4.6, lab, size=6.2, weight="bold", color=LOW["ink"] if j == 0 else HIGH["ink"],
                    linespacing=1.05)
        mx, my = x + ew / 2, ty + th - 9.0 - 1.6 - s / 2
        cv.arrow([(mx - 3.0, my), (mx + 3.0, my)], color=SLATE, lw=1.0, head=1.2)
        cv.text(mx, my + 2.4, "unasked", size=5.9, color=SLATE, style="italic")
    # ---- low / high grid -------------------------------------------------------------------------------
    hx, hw2 = 1.0, 35.0
    gx = hx + hw2 + 1.6
    cw = (W - 1.0 - gx - 1.6) / 2
    rh, rg = 20.0, 1.4
    hy = 91.6
    for j, (lab, c) in enumerate((("Low", LOW), ("High", HIGH))):
        x = gx + j * (cw + 1.6)
        rbox(cv, x, hy, cw, 5.6, c["mark"], r=2.0, z=4)
        cv.text(x + cw / 2, hy + 2.8, lab, size=9.0, weight="bold", color="white", z=6)
    for i, (cap, gloss, lv, ll, hv, hl) in enumerate(ROWS):
        y = hy - 1.4 - (i + 1) * rh - i * rg
        rbox(cv, hx, y, hw2, rh, "#EEF1F6", "#C3CAD4", 0.5, r=1.6, z=3)
        cv.text(hx + 2.4, y + rh - 4.4, cap, size=9.0, weight="bold", color=SLATE, ha="left")
        cv.text(hx + 2.4, y + rh - 8.0, gloss, size=6.9, color=INK, ha="left", va="top", linespacing=1.08)
        for j, (vig, line, c) in enumerate(((lv, ll, LOW), (hv, hl, HIGH))):
            x = gx + j * (cw + 1.6)
            rbox(cv, x, y, cw, rh, c["fill"], c["stroke"], 0.5, r=1.6, z=3)
            s = rh - 2.0
            cv.image(os.path.join(VIG, vig + ".jpg"), x + 1.0 + s / 2, y + rh / 2, s, fit="cover", h=s, radius=1.2,
                     focus=(0.5, 0.45), zoom=1.45, z=5)
            # bubble next to the robot with a short tail (a long tail across empty space reads as a pointer)
            cv.bubble(0, y + rh / 2, line, tail=(x + s - 1.0, y + rh / 2 + 3.0), left=x + s + 3.4, r=c, size=7.6)
    # ---- trust earned -> autonomy ------------------------------------------------------------------------
    ay, ah = 1.0, 20.0
    tyy = ay + ah + 3.2
    cv.text(hx + 2.4, tyy, "Trust earned?", size=9.4, weight="bold", color=HIGH["mark"], ha="left")
    cv.ax.add_patch(Polygon([(hx + 29.4, tyy + 3.0), (hx + 33.0, tyy + 3.0), (hx + 33.0, tyy - 0.4), (hx + 35.0, tyy - 0.4),
                             (hx + 31.2, tyy - 3.2), (hx + 27.4, tyy - 0.4), (hx + 29.4, tyy - 0.4)], closed=True,
                            fc=HIGH["mark"], ec="none", zorder=5))
    for j, (lab, c) in enumerate((("Low", LOW), ("High", HIGH))):  # repeat the column headers for the autonomy row
        x = gx + j * (cw + 1.6)
        rbox(cv, x, ay + ah + 1.0, cw, 4.2, c["mark"], r=2.0, z=4)
        cv.text(x + cw / 2, ay + ah + 3.1, lab, size=7.6, weight="bold", color="white", z=6)
    rbox(cv, hx, ay, hw2, ah, "#EEF1F6", "#C3CAD4", 0.5, r=1.6, z=3)
    cv.text(hx + 2.4, ay + ah - 4.4, "Autonomy", size=9.0, weight="bold", color=SLATE, ha="left")
    cv.text(hx + 2.4, ay + ah - 8.0, "how independently it\nis allowed to act", size=6.9, color=INK, ha="left",
            va="top", linespacing=1.08)
    for j, (vig, line, c) in enumerate((("a_low", "Needs permission\nbefore acting", LOW),
                                         ("a_high", "Acts independently\nwithin guardrails", HIGH))):
        x = gx + j * (cw + 1.6)
        rbox(cv, x, ay, cw, ah, c["fill"], c["stroke"], 0.5, r=1.6, z=3)
        s = ah - 2.0
        cv.image(os.path.join(VIG, vig + ".jpg"), x + 1.0 + s / 2, ay + ah / 2, s, fit="cover", h=s, radius=1.2,
                 focus=(0.5, 0.45), z=5)
        cv.text((x + s + 1.0 + x + cw - 7.0) / 2, ay + ah / 2, line, size=8.6, weight="bold", color=c["ink"], linespacing=1.1)
    cv.arrow([(gx + cw - 6.0, ay + ah / 2), (gx + cw + 1.6 + 0.6, ay + ah / 2)], color=HIGH["mark"], lw=1.4, head=1.6, z=9)
    assert not cv.overlaps() and not cv.text_overlaps(), cv.overlaps() + cv.text_overlaps()
    print("\n".join(cv.save(os.path.join(a.out, "proactive_capabilities"))))


if __name__ == "__main__":
    main()
