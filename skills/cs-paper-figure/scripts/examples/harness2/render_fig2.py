"""Redesign of Harness^2 (arXiv 2610.14224) Figure 2: the eight harness components and their runtime roles.

Facts (Sec. 2.1 and the original Figure 2): a harness H = (c1..c8) of editable files composes with a
frozen model M to form an agent; components are grouped by runtime role:
  context construction: C1 system prompt (systemprompt.md, every call), C2 guardrails (guardrails.md,
  every call), C3 memory (LongTermMEMORY.md, every call), C6 skills (skills/<n>/SKILL.md, on invoke);
  middleware: C8 plugin (plugin/<name>.ts) hooks every tool call, outside the model's discretion;
  tool interface: C4 tool guidance (tool_guidance.md, every call), C7 scripts (scripts/<name>.py, via bash);
  orchestration: C5 subagents (sub_agents/<n>/AGENT.md, task tool) delegate work to a new agent.
The agent produces a trajectory and a deliverable.

    python render_fig2.py --out <dir> [--vector-icons]

Icons in icons/ (model, subagent and four group emblems) were generated with scripts/codex_icons.py,
using the Fig. 3 executor icon as a style reference; --vector-icons draws paperkit's vector glyphs instead.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, INK, MUTED  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402

CTX = dict(fill="#EBF2FC", soft="#D2E2F7", stroke="#5A8BCB", ink="#1C4C8C", mark="#2F5FA8")
MID = dict(fill="#F3EFFB", soft="#E1D6F4", stroke="#8C6CC8", ink="#47297F", mark="#6A45B0")
TOOL = dict(fill="#ECF5EC", soft="#CFE6CF", stroke="#5E9E62", ink="#25592A", mark="#3F7F44")
ORC = dict(fill="#FBEFF3", soft="#F3D5E0", stroke="#C27896", ink="#7A2E4A", mark="#A84C72")
NEU = dict(fill="#F3F4F6", soft="#E4E7EB", stroke="#8F98A4", ink="#353C47", mark="#6B7480")
MONO = "DejaVu Sans Mono"
COMPONENTS = {  # id: (group, name, file, activation)
    "C1": ("ctx", "System prompt", "systemprompt.md", "every call"),
    "C2": ("ctx", "Guardrails", "guardrails.md", "every call"),
    "C3": ("ctx", "Memory", "LongTermMEMORY.md", "every call"),
    "C6": ("ctx", "Skills", "skills/<n>/SKILL.md", "on invoke"),
    "C8": ("mid", "Plugin", "plugin/<name>.ts", None),
    "C4": ("tool", "Tool guidance", "tool_guidance.md", "every call"),
    "C7": ("tool", "Scripts", "scripts/<name>.py", "via bash"),
    "C5": ("orc", "Subagents", "sub_agents/<n>/AGENT.md", "task tool"),
}
W, H = 178, 86
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
NO_ICONS = False


def icon(name):
    p = os.path.join(ICON_DIR, f"{name}.png")
    return p if os.path.exists(p) and not NO_ICONS else None


def emblem(cv, x, y, w, h, name, size=7.4):
    """Generated group emblem at the right end of a header band (band height = 0.62 * size)."""
    p = icon(name)
    if p:
        cv.image(p, x + w - 4.8, y + h - size * 0.31, 4.2)


def card(cv, x, y, w, h, c, title, sub, em=None):
    cv.group(x, y, w, h, c, title, band=True, size=7.4, radius=2.0, lw=0.7, fill="white")
    if em:
        emblem(cv, x, y, w, h, em)
    cv.text(x + 2.0, y + h - 7.6, sub, size=6.0, color=MUTED, ha="left", style="italic")


def comp(cv, x, y, w, h, cid, c):
    _, name, path, act = COMPONENTS[cid]
    cv.box(x, y, w, h, c, fill="white", lw=0.55, radius=1.3)
    # folded-corner file glyph = an editable component file
    cv.doc(x + 1.4, y + h - 6.6, 3.6, 4.6, c, lines=2, fold=1.2, lw=0.45)
    x0, wc = cv.chip(x + 6.6, y + h - 4.3, cid, c, size=6.0, solid=True, ha="left", pad=0.7)
    cv.text(x0 + wc + 1.2, y + h - 4.3, name, size=7.0, color=INK, weight="bold", ha="left")
    cv.text(x + 6.6, y + 3.1, path, size=5.9, color="#3F4652", ha="left", family=MONO)
    if act:
        cv.chip(x + w - 1.4, y + 3.1, act, c, size=5.9, ha="right", pad=0.7)


def step(cv, x, y, k):
    cv.ax.add_patch(Circle((x, y), 1.35, fc=INK, ec="white", lw=0.4, zorder=12))
    cv.text(x, y - 0.05, str(k), size=5.8, color="white", weight="bold", z=13)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    ap.add_argument("--vector-icons", action="store_true", help="ignore icons/*.png and draw vector glyphs")
    a = ap.parse_args()
    global NO_ICONS
    NO_ICONS = a.vector_icons
    assert len(COMPONENTS) == 8 and sorted(COMPONENTS) == [f"C{i}" for i in range(1, 9)]
    cv = Canvas(W, H, family="serif", size=7.0)

    # context construction
    card(cv, 2, 2, 52, 82, CTX, "Context construction", "what enters the context, and when", em="context")
    for k, cid in enumerate(("C1", "C2", "C3", "C6")):
        comp(cv, 4.0, 58.6 - k * 18.0, 48, 14.4, cid, CTX)

    # frozen model at the centre
    mx, my = 76.5, 50.0
    r = 11.5 if icon("model") else 10.0
    cv.ax.add_patch(Circle((mx, my), r + 1.6, fc="#F4F6F9", ec="#C9D2DE", lw=0.5, zorder=3))
    cv.ax.add_patch(Circle((mx, my), r, fc="white", ec=NEU["ink"], lw=1.1, zorder=4))
    if icon("model"):
        cv.text(mx, my + 6.6, "Frozen model", size=7.2, color=NEU["ink"], weight="bold")
        cv.image(icon("model"), mx - 2.4, my - 2.0, 11.6)
        cv.text(mx + 6.0, my - 2.6, r"$\mathcal{M}$", size=10, color=NEU["ink"])
    else:
        cv.text(mx, my + 3.4, "Frozen model", size=7.2, color=NEU["ink"], weight="bold")
        cv.text(mx, my - 1.6, r"$\mathcal{M}$", size=11, color=NEU["ink"])
        cv.icon_snow(mx, my - 6.6, 2.6, color=NEU["stroke"])
    cv.text(mx, 72.2, "Agent = model + harness", size=6.6, color=INK, weight="bold")
    cv.text(mx, 69.2, "8 editable files around a model", size=6.0, color=MUTED, style="italic")
    cv.text(mx, 66.6, "whose weights never change", size=6.0, color=MUTED, style="italic")

    # (1) context in
    cv.arrow([(54.0, my), (mx - r - 1.8, my)], color=CTX["mark"], lw=0.9, head=1.3)
    cv.text(60.0, my + 2.6, "context", size=6.1, color=CTX["ink"])

    # middleware + tool interface
    card(cv, 98, 37, 78, 47, MID, "Middleware", "hooks every tool call, outside the model's discretion", em="plugin")
    comp(cv, 99.6, 43.0, 28.4, 26.0, "C8", MID)
    cv.chip(113.8, 58.6, "inside the tool loop", MID, size=5.9, pad=0.7)
    cv.text(113.8, 54.6, "tool calls + turn", size=5.9, color=MID["ink"])
    cv.text(113.8, 52.0, "boundaries", size=5.9, color=MID["ink"])
    cv.group(129.5, 39.5, 44.5, 33.0, TOOL, "Tool interface", size=7.0, radius=1.6, lw=0.6, band=True)
    emblem(cv, 129.5, 39.5, 44.5, 33.0, "tools", size=7.0)
    cv.text(131.3, 66.0, "what the model can call, and how", size=5.9, color=MUTED, ha="left", style="italic")
    comp(cv, 131.0, 52.0, 41.5, 12.2, "C4", TOOL)
    comp(cv, 131.0, 40.8, 41.5, 10.6, "C7", TOOL)
    # (2) call -> plugin hook -> (3) tool ; (4) result back
    cv.arrow([(mx + r + 0.4, my + 4.0), (99.6, my + 4.0)], color=MID["mark"], lw=0.9, head=1.3)
    cv.text(92.4, my + 6.2, "tool call", size=6.1, color=MID["ink"])
    cv.arrow([(128.0, 48.4), (131.0, 48.4)], color=TOOL["mark"], lw=0.8, head=1.1)
    cv.arrow([(131.0, 43.6), (128.0, 43.6)], color=TOOL["mark"], lw=0.8, head=1.1)
    cv.icon_cycle(92.4, my, 2.8, color=MID["mark"])
    cv.arrow([(99.6, my - 4.0), (mx + r + 0.4, my - 4.0)], color=MID["mark"], lw=0.9, head=1.3)
    cv.text(92.4, my - 6.4, "result", size=6.1, color=MID["ink"])

    # orchestration
    card(cv, 98, 2, 78, 32, ORC, "Orchestration", "when work is delegated to a new agent, and how", em="orchestration")
    comp(cv, 100.5, 7.0, 46.0, 14.4, "C5", ORC)
    if icon("subagent"):
        cv.image(icon("subagent"), 160.0, 16.2, 9.0)
    else:
        cv.icon_robot(160.0, 15.6, 6.4, color=ORC["mark"])
    cv.text(160.0, 8.4, "new agent", size=6.0, color=ORC["ink"], style="italic")
    cv.arrow([(148.6, 14.2), (155.6, 14.2)], color=ORC["mark"], lw=0.7, head=1.0)
    # delegation from the model
    cv.arrow([(mx + 6.0, my - r + 2.0), (92.0, 26.0), (92.0, 14.2), (100.5, 14.2)], color=ORC["mark"],
             lw=0.8, head=1.2, dashed=True, radius=1.4, both=True)
    cv.text(86.0, 33.4, "delegate", size=6.0, color=ORC["ink"], ha="right", style="italic")

    # output
    cv.arrow([(mx - 7.0, my - (r * r - 49.0) ** 0.5), (mx - 7.0, 24.0)], color=INK, lw=0.9, head=1.3)
    cv.doc(mx - 10.2, 11.0, 6.4, 13.0, NEU, lines=4, fold=2.0)
    cv.text(mx - 2.0, 20.4, r"trajectory $\tau$", size=6.7, color=INK, ha="left")
    cv.text(mx - 2.0, 15.4, r"+ deliverable $y$", size=6.7, color=INK, ha="left")
    cv.text(mx, 5.6, r"output of $\mathcal{A}(q;\,\mathcal{M},\mathcal{H})$", size=6.2, color=MUTED)
    print("\n".join(cv.save(os.path.join(a.out, "harness2_fig2_components"))))


if __name__ == "__main__":
    main()
