"""Redesign of Fig. 3 of "Proactive AI for Superintelligent Agents": from complementary capabilities
to earned autonomy.

Content from the source figure: three examples (coding agent: unreported bug -> discovered & fixed
without being asked; risk detection: smoke detected (overheating) -> risk resolved & safe; household
robot: supply low, need restock -> items ordered & delivered); a low/high grid for intelligence,
alignment and proactiveness with the agent's own words; autonomy (need permission before acting -> act
independently within guardrails), granted when trust is earned. Robot poses and state icons in art/
were generated with scripts/codex_icons.py; every word is vector text.

    python render_capabilities.py --out <dir>
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sixa  # noqa: E402,F401
from paperkit import Canvas, INK, MUTED, ROLE  # noqa: E402

ART = os.path.join(HERE, "art")
LOW, HIGH, NEU = ROLE["rose"], ROLE["teal"], ROLE["neutral"]
EXAMPLES = [("Coding agent", "ex_bug", "Unreported bug", "ex_fixed", "Found and fixed\nwithout being asked"),
            ("Risk detection", "ex_smoke", "Smoke detected\n(overheating)", "ex_safe", "Risk resolved\nand safe"),
            ("Household robot", "ex_low", "Supply low,\nneed restock", "ex_delivered", "Items ordered\nand delivered")]
ROWS = [("Intelligence", "understanding and reasoning",
         ("r_int_low", "Wait – what\nshould I do?"), ("r_int_high", "I've got this.")),
        ("Alignment", "aligning actions with the user's\nintents, values and constraints",
         ("r_ali_low", "Get the result.\nHowever it takes."), ("r_ali_high", "I'll succeed, and\nsucceed cleanly.")),
        ("Proactiveness", "taking the initiative to act",
         ("r_pro_low", "Plans broken. Waiting\nfor your call on\nwhat to do next."),
         ("r_pro_high", "Plan shifted, so I started\nworking a way around it,\nopen to your steer."))]
W, H = 178, 118


def img(cv, name, cx, cy, w, fit="box"):
    p = os.path.join(ART, name + ".png")
    return cv.image(p, cx, cy, w, fit=fit) if os.path.exists(p) else w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.0)
    # 1. examples: current state -> goal state, reached without a request
    ew, eg, ey, eh = 56.6, 2.1, 89.0, 27.0
    for k, (title, cur, cur_t, goal, goal_t) in enumerate(EXAMPLES):
        x = 2.0 + k * (ew + eg)
        cv.box(x, ey, ew, eh, "neutral", fill="white", stroke=NEU["stroke"], lw=0.6, radius=2.0)
        cv.tab(x + 2.0, ey + eh - 3.0, cv.text_width(f"Example {k + 1} · {title}", 6.6) + 4.0, 5.0, NEU,
               f"Example {k + 1} · {title}", size=6.6, solid=True)
        for j, (icon, label, c, cap) in enumerate(((cur, cur_t, LOW, "current state"), (goal, goal_t, HIGH, "goal state"))):
            cx = x + 14.0 + j * 28.6
            cv.text(cx, ey + eh - 6.6, cap, size=5.9, color=MUTED, style="italic")
            img(cv, icon, cx, ey + 11.8, 9.6)
            cv.text(cx, ey + 3.6, label, size=6.2, color=c["ink"], weight="bold", linespacing=1.05)
        cv.arrow([(x + 21.2, ey + 11.8), (x + 35.4, ey + 11.8)], color="#4B5563", lw=0.9, head=1.2)
        cv.text(x + 28.3, ey + 14.0, "unasked", size=5.9, color=MUTED, style="italic")
    # 2. capability grid: low vs high, in the agent's own words
    lx, lw_, cx0, cw = 2.0, 40.0, 44.0, 65.0
    top = 84.0
    cv.tab(cx0, top - 5.0, cw, 5.0, LOW, "Low", size=7.6, solid=True)
    cv.tab(cx0 + cw + 2.0, top - 5.0, cw, 5.0, HIGH, "High", size=7.6, solid=True)
    rh = 17.4
    for r, (name, desc, low, high) in enumerate(ROWS):
        y = top - 6.0 - (r + 1) * rh
        cv.box(lx, y + 0.6, lw_, rh - 1.2, "neutral", fill="#F7F8FA", stroke=NEU["soft"], lw=0.5, radius=1.6)
        cv.text(lx + 2.4, y + rh - 5.2, name, size=8.0, weight="bold", color=INK, ha="left")
        cv.text(lx + 2.4, y + rh - 9.0, desc, size=6.0, color=MUTED, ha="left", va="top", linespacing=1.1)
        for j, ((icon, quote), c) in enumerate(((low, LOW), (high, HIGH))):
            x = cx0 + j * (cw + 2.0)
            cv.box(x, y + 0.6, cw, rh - 1.2, "neutral", fill=c["fill"], stroke=c["soft"], lw=0.5, radius=1.6)
            img(cv, icon, x + 8.4, y + rh / 2, rh - 3.4, fit="height")
            cv.bubble(0, y + rh / 2 + 1.0, quote, tail=(x + 14.0, y + rh / 2 + 2.6), r=c, size=6.3, left=x + 18.0)
    # 3. a reliable track record earns trust, trust earns autonomy
    gy = top - 6.0 - 3 * rh
    cv.arrow([(lx + lw_ / 2, gy + 0.4), (lx + lw_ / 2, 21.0)], color="#4B5563", lw=1.0, head=1.3)
    cv.text(lx + lw_ / 2 + 1.6, gy - 2.6, "a reliable track record earns trust …", size=6.2, color=INK, ha="left",
            style="italic")
    ay, ah = 3.0, 17.0
    cv.box(lx, ay, lw_, ah, "neutral", fill="#EEF0F8", stroke="#5A5FA8", lw=0.7, radius=1.6)
    cv.text(lx + 2.4, ay + ah - 5.0, "Autonomy", size=8.0, weight="bold", color="#2B2F6E", ha="left")
    cv.text(lx + 2.4, ay + ah - 8.8, "… and trust earns autonomy:\nhow independently it is\nallowed to act", size=6.0,
            color=MUTED, ha="left", va="top", linespacing=1.1)
    cv.box(cx0, ay, cw - 6.0, ah, "neutral", fill=LOW["fill"], stroke=LOW["stroke"], lw=0.7, radius=1.6)
    cv.text(cx0 + (cw - 6.0) / 2, ay + ah / 2, "Needs permission\nbefore acting", size=7.6, weight="bold",
            color=LOW["ink"], linespacing=1.1)
    cv.box(cx0 + cw + 8.0, ay, cw - 6.0, ah, "neutral", fill=HIGH["fill"], stroke=HIGH["stroke"], lw=0.7, radius=1.6)
    cv.text(cx0 + cw + 8.0 + (cw - 6.0) / 2, ay + ah / 2, "Acts independently\nwithin guardrails", size=7.6,
            weight="bold", color=HIGH["ink"], linespacing=1.1)
    cv.spectrum(cx0 + cw - 5.0, cx0 + cw + 7.0, ay + ah / 2, LOW["mark"], HIGH["mark"], lw=1.6, head=1.5)
    print("\n".join(cv.save(os.path.join(a.out, "proactive_capabilities"))))


if __name__ == "__main__":
    main()
