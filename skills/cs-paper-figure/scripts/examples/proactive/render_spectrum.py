"""Redesign of Fig. 4 of "Proactive AI for Superintelligent Agents": the reactivity-proactivity spectrum.

Content from the source figure: three settings along one axis (reactive -> more proactive), what the agent
provides (reactive response, mixed-initiative assistance, self-initiated agency) and the human's role
(operator, collaborator, reviewer), the printer dialogue, the proposed work plan and the progress update.

Kept from the original: full-colour scenes that fill their panels, one cast, a graded axis, and solid chips
that darken along it. Fixed: the dialogue, work plan and progress update were text baked into the pixels
(unsearchable, uneditable, blurry at print size); here they are vector bubbles and cards over text-free
vignettes (vignettes/, generated with scripts/codex_icons.py, style "vignette", cast reference cast.jpg).

    python render_spectrum.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sixa  # noqa: E402,F401  (puts paperkit on the path)
from paperkit import Canvas, INK, mix  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon  # noqa: E402

LIGHT, DARK = "#7A8599", "#2B2F6E"  # one hue ramp: lightness carries "more initiative"
VIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vignettes")
TICK = "#2E8B57"
W = 178


def rbox(cv, x, y, w, h, fc, ec="none", lw=0.0, r=1.4, z=15, alpha=1.0):
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw,
                                   zorder=z, alpha=alpha))


def card(cv, x, y, title, items, done, accent, foot=None):
    """Vector checklist card laid over a vignette: (x, y) is its top-left corner."""
    lh, size = 2.45, 5.6
    w = max([cv.text_width(s, size) + 5.4 for s in items + ([foot] if foot else [])]
            + [cv.text_width(title, 6.0, "bold") + 2.8])
    h = 4.4 + lh * len(items) + (lh + 0.4 if foot else 0) + 0.8
    rbox(cv, x + 0.25, y - h - 0.25, w, h, "#1A2230", r=1.2, z=14.8, alpha=0.18)  # soft shadow
    rbox(cv, x, y - h, w, h, "white", accent, 0.5, r=1.2)
    cv.text(x + 1.4, y - 2.0, title, size=6.0, weight="bold", color=accent, ha="left", z=16)
    for k, s in enumerate(items):
        yy = y - 4.6 - k * lh
        if done:
            cv.ax.add_patch(Circle((x + 2.2, yy), 0.85, fc=TICK, ec="none", zorder=16))
            cv.icon_check(x + 2.2, yy, 1.0, color="white", lw=0.55, z=17)
        else:
            rbox(cv, x + 1.35, yy - 0.85, 1.7, 1.7, "white", accent, 0.45, r=0.3, z=16)
        cv.text(x + 4.0, yy, s, size=size, color=INK, ha="left", z=16)
    if foot:
        yy = y - 4.6 - len(items) * lh - 0.4
        cv.line([(x + 1.2, yy + 1.3), (x + w - 1.2, yy + 1.3)], color="#D5D9DF", lw=0.35, z=16)
        cv.text(x + 1.4, yy, foot, size=size, color=accent, ha="left", z=16, style="italic")


def person(cv, x, y, s, col):
    cv.ax.add_patch(Circle((x, y + s * 0.22), s * 0.2, fc=col, ec="none", zorder=12))
    cv.ax.add_patch(FancyBboxPatch((x - s * 0.33, y - s * 0.42), s * 0.66, s * 0.4,
                                   boxstyle=f"round,pad=0,rounding_size={s * 0.2}", fc=col, ec="none", zorder=12))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    x0, gap = 21.0, 1.6
    pw = (W - x0 - 1.0 - 2 * gap) / 3
    ph = pw / 1.28
    H = 8.6 + ph + 23.6
    cv = Canvas(W, H, family="sans", size=7.6)
    py = H - 8.6 - ph
    cv.spectrum(x0, W - 1.0, H - 5.4, LIGHT, DARK, labels=(), lw=2.2, head=2.4)
    for xx in (x0 + pw + gap / 2, x0 + 2 * pw + 1.5 * gap):
        cv.dot(xx, H - 5.4, color="white", d=1.0)
    cv.text(x0 + 0.4, H - 2.4, "Reactive", size=8.6, weight="bold", color=mix(LIGHT, "#1F2430", 0.35), ha="left")
    cv.text(W - 1.6, H - 2.4, "More proactive", size=8.6, weight="bold", color=DARK, ha="right")
    cv.text(1.0, H - 5.4, "Initiative", size=8.2, weight="bold", color=INK, ha="left")
    xs = [x0 + k * (pw + gap) for k in range(3)]
    for k, scene in enumerate(("sc_reactive", "sc_mixed", "sc_proactive")):
        cv.image(os.path.join(VIG, scene + ".jpg"), xs[k] + pw / 2, py + ph / 2, pw, fit="cover", h=ph, radius=1.8, z=10)

    def at(k, fx, fy):  # fraction of panel k (from the top-left) -> canvas mm
        return xs[k] + fx * pw, py + ph * (1 - fy)

    # reactive: the user dictates each step
    cv.bubble(*at(0, 0.66, 0.11), "Good! Now close the lid\nand run a test print.", tail=at(0, 0.44, 0.17), size=6.0)
    cv.bubble(*at(0, 0.78, 0.34), "Understood. Preparing\nthe test print…", tail=at(0, 0.70, 0.43), size=6.0)
    # mixed initiative: the agent proposes, the user decides
    bx, by = at(1, 0.03, 0.56)
    card(cv, bx, by, "Proposed work plan", ["Draft Q2 market analysis", "Review competitor updates",
                                           "Prepare budget forecast", "Schedule stakeholder sync"], False, "#4B4F9A")
    # self-initiated: the agent reports work already done
    bx, by = at(2, 0.03, 0.50)
    card(cv, bx, by, "Work progress update", ["Q2 analysis completed", "Competitor report delivered",
                                             "Budget forecast ready", "Stakeholder sync scheduled"], True, DARK,
         foot="Next up: product roadmap review")
    # what the agent provides / the human's role: solid chips darkening along the axis
    rows = (("Agent\nprovides", ("Reactive response", "Mixed-initiative\nassistance", "Self-initiated\nagency"), py - 6.4),
            ("Human's\nrole", ("Operator", "Collaborator", "Reviewer"), py - 17.2))
    shades = [mix(LIGHT, DARK, t) for t in (0.0, 0.5, 1.0)]
    for label, chips, yy in rows:
        cv.text(1.0, yy, label, size=8.2, weight="bold", color=INK, ha="left", linespacing=1.05)
        for k, s in enumerate(chips):
            cx = xs[k] + 11.0
            ic = shades[k]
            if label.startswith("Agent"):
                if k == 0:  # speech bubble = responds
                    rbox(cv, cx - 3.2, yy - 1.6, 6.4, 4.2, ic, r=2.0, z=12)
                    cv.ax.add_patch(Polygon([(cx - 1.8, yy - 1.4), (cx - 2.6, yy - 3.2), (cx - 0.2, yy - 1.4)],
                                            fc=ic, ec="none", zorder=12))
                elif k == 1:  # two people = together
                    person(cv, cx - 1.6, yy + 0.2, 5.0, ic)
                    person(cv, cx + 1.8, yy - 0.4, 5.0, mix(ic, "white", 0.25))
                else:  # clipboard with rising chart = owns the work
                    rbox(cv, cx - 2.6, yy - 3.2, 5.2, 6.4, "white", ic, 0.8, r=0.6, z=12)
                    cv.line([(cx - 1.4, yy - 2.0), (cx - 0.2, yy - 0.6), (cx + 0.6, yy - 1.2), (cx + 1.6, yy + 1.2)],
                            color=ic, lw=0.9, z=13)
                    rbox(cv, cx - 1.2, yy + 2.6, 2.4, 1.1, ic, r=0.3, z=13)
            else:
                person(cv, cx, yy, 6.0, ic)
            rbox(cv, cx + 5.0, yy - 4.2, pw - 17.0, 8.4, ic, r=2.0, z=12)
            cv.text(cx + 5.0 + (pw - 17.0) / 2, yy, s, size=8.0, color="white", weight="bold", z=13, linespacing=1.05)
    for xx in (xs[1] - gap / 2, xs[2] - gap / 2):
        cv.line([(xx, rows[1][2] - 4.6), (xx, rows[0][2] + 4.6)], color="#C9CED6", lw=0.5, dashed=True)
    assert not cv.overlaps() and not cv.text_overlaps(), cv.overlaps() + cv.text_overlaps()
    print("\n".join(cv.save(os.path.join(a.out, "proactive_spectrum"))))


if __name__ == "__main__":
    main()
