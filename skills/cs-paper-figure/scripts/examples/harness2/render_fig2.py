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

Icons in icons/ were generated with scripts/codex_images.py (prompts in icons/manifest_fig2*.json): the frozen
model, the subagent, four group emblems, and one file icon per component (f_c1..f_c8, f_out: the same page with
a role badge); --vector-icons draws paperkit's vector glyphs instead.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, INK, MUTED  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

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
W, H = 178, 93
KEY = 7.0  # legend strip height under the art (the art is drawn in 0..86 and lifted by KEY)
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
NO_ICONS = False


def icon(name):
    p = os.path.join(ICON_DIR, f"{name}.png")
    return p if os.path.exists(p) and not NO_ICONS else None


def lift(cv, dy, since=None):
    """Move every artist drawn after `since` (from mark(cv)) up by dy mm, snapped to whole output pixels so
    placed icons keep their 1:1 pixel grid. Lets a key strip go under art laid out from y = 0."""
    from matplotlib.transforms import Affine2D
    from paperkit import RASTER_DPI
    ppm = RASTER_DPI / 25.4
    dy = round(dy * ppm) / ppm
    since = since or dict(patches=0, texts=0, lines=0, images=0, collections=0, chips=0)
    for kind in ("patches", "texts", "lines", "collections"):
        for a in list(getattr(cv.ax, kind))[since[kind]:]:
            # compose with earlier lifts; a patch's get_transform() also holds its own patch transform
            base = a.get_data_transform() if kind == "patches" else a.get_transform()
            a.set_transform(Affine2D().translate(0, dy) + base)
    for im in list(cv.ax.images)[since["images"]:]:
        x0, x1, y0, y1 = im.get_extent()
        im.set_extent((x0, x1, y0 + dy, y1 + dy))
    cv.chips[since["chips"]:] = [(x, y + dy, w, h, s, reg and (reg[0], reg[1] + dy, reg[2], reg[3] + dy))
                                 for x, y, w, h, s, reg in cv.chips[since["chips"]:]]
    cv.ax.set_xlim(0, cv.w)
    cv.ax.set_ylim(0, cv.h)


def mark(cv):
    return {k: len(getattr(cv.ax, k)) for k in ("patches", "texts", "lines", "images", "collections")} | \
        {"chips": len(cv.chips)}


def card(cv, x, y, w, h, c, title, sub, em=None):
    """Module section: tinted field, dashed border in the module hue, title on a pill tab on the top border."""
    cv.section(x, y, w, h, c, title, tab="top", size=7.4, radius=2.0, lw=0.75)
    if em and icon(em):
        cv.image(icon(em), x + w - 4.2, y + h - 4.6, 4.2)
    cv.text(x + 2.0, y + h - 5.4, sub, size=6.0, color=c["ink"], ha="left", style="italic")


def comp(cv, x, y, w, h, cid, c):
    _, name, path, act = COMPONENTS[cid]
    cv.box(x, y, w, h, c, fill="white", lw=0.6, radius=1.3, shadow=True)
    cv.ax.add_patch(Rectangle((x + 0.25, y + 0.6), 0.9, h - 1.2, fc=c["mark"], ec="none", zorder=5.5))
    # an editable component file: generated file icon with a role badge, else the vector file glyph
    png, tx = icon(f"f_{cid.lower()}"), x + 6.6
    if png:
        cv.image(png, x + 4.8, y + h - 4.8 if h > 16 else y + h / 2, 6.8)
        tx = x + 9.4
    else:
        cv.doc(x + 1.8, y + h - 6.6, 3.6, 4.6, c, lines=2, fold=1.2, lw=0.45)
    x0, wc = cv.chip(tx, y + h - 4.3, cid, c, size=6.0, solid=True, ha="left", pad=0.7)
    cv.text(x0 + wc + 1.2, y + h - 4.3, name, size=7.0, color=c["ink"], weight="bold", ha="left")
    cv.text(tx, y + 3.1, path, size=5.4, color="#3F4652", ha="left", family=MONO)
    if act:
        cv.chip(x + w - 1.4, y + 3.1, act, c, size=5.9, ha="right", pad=0.7)


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
    card(cv, 2, 2, 48, 80.6, CTX, "Context construction", "what enters the context, and when", em="context")
    for k, cid in enumerate(("C1", "C2", "C3", "C6")):
        comp(cv, 4.0, 57.4 - k * 18.0, 44, 14.4, cid, CTX)

    # frozen model at the centre: the hero, a soft halo in the context hue fading into the tool hue
    mx, my = 76.5, 50.0
    r = 11.5 if icon("model") else 10.0
    cv.ax.add_patch(Circle((mx, my), r + 1.8, fc=CTX["fill"], ec=CTX["stroke"], lw=0.5, ls=(0, (3, 2)), zorder=3))
    cv.ax.add_patch(Circle((mx, my), r, fc="white", ec=NEU["ink"], lw=1.2, zorder=4))
    if icon("model"):
        cv.text(mx, my + 6.6, "Frozen model", size=7.2, color=NEU["ink"], weight="bold")
        cv.image(icon("model"), mx - 2.2, my - 1.6, 10.2)
        cv.text(mx + 6.0, my - 2.6, r"$\mathcal{M}$", size=10, color=NEU["ink"])
        cv.icon_snow(mx + 6.0, my - 7.0, 2.4, color="#4A90C8")
    else:
        cv.text(mx, my + 3.4, "Frozen model", size=7.2, color=NEU["ink"], weight="bold")
        cv.text(mx, my - 1.6, r"$\mathcal{M}$", size=11, color=NEU["ink"])
        cv.icon_snow(mx, my - 6.6, 2.6, color="#4A90C8")
    cv.rich(mx, 72.6, [("Agent = ", INK, "bold"), ("model", NEU["ink"], "bold"), (" + ", INK, "bold"),
                       ("harness", CTX["mark"], "bold")], size=6.8, ha="center")
    cv.text(mx, 69.4, "8 editable files around a model", size=6.0, color=MUTED, style="italic")
    cv.text(mx, 66.8, "whose weights never change", size=6.0, color=MUTED, style="italic")

    # (1) context in: the window the model reads each call, assembled from the context components + the task
    cv.text(55.4, 62.6, "context", size=6.1, color=CTX["ink"], style="italic")
    for k, (lab, c) in enumerate((("C1", CTX), ("C2", CTX), ("C3", CTX), ("C6", CTX), (r"$q$", NEU))):
        cv.cuboid(52.4, 56.2 - k * 4.4, 5.6, 3.4, d=1.3, r=c, title=lab, size=5.8)
    cv.arrow([(59.4, my), (mx - r - 2.0, my)], color=CTX["mark"], lw=1.0, head=1.2)
    cv.line([(50.0, my), (52.4, my)], color=CTX["mark"], lw=1.0)

    # middleware + tool interface
    card(cv, 98, 37, 78, 45.2, MID, "Middleware", "hooks every tool call, outside the model's discretion", em="plugin")
    comp(cv, 99.6, 41.0, 28.4, 26.0, "C8", MID)
    cv.chip(113.8, 55.4, "inside the tool loop", MID, size=5.9, pad=0.7)
    cv.text(113.8, 51.6, "tool calls + turn", size=5.9, color=MID["ink"])
    cv.text(113.8, 49.0, "boundaries", size=5.9, color=MID["ink"])
    cv.section(129.5, 39.0, 44.5, 31.0, TOOL, "Tool interface", tab="top", size=7.0, radius=1.6, lw=0.7)
    if icon("tools"):
        cv.image(icon("tools"), 129.5 + 44.5 - 4.0, 39.0 + 31.0 - 4.2, 4.0)
    cv.text(131.3, 65.4, "what the model can call, and how", size=5.9, color=TOOL["ink"], ha="left", style="italic")
    comp(cv, 130.8, 51.2, 42.2, 12.2, "C4", TOOL)
    comp(cv, 130.8, 40.2, 42.2, 10.4, "C7", TOOL)
    # (2) call -> plugin hook -> (3) tool ; (4) result back
    cv.arrow([(mx + r + 0.4, my + 4.0), (99.6, my + 4.0)], color=MID["mark"], lw=1.0, head=1.3)
    cv.text(93.6, my + 6.2, "tool call", size=6.1, color=MID["ink"], style="italic")
    cv.arrow([(128.0, 47.6), (130.8, 47.6)], color=TOOL["mark"], lw=0.8, head=1.1)
    cv.arrow([(130.8, 43.0), (128.0, 43.0)], color=TOOL["mark"], lw=0.8, head=1.1)
    cv.icon_cycle(92.4, my, 2.8, color=MID["mark"])
    cv.arrow([(99.6, my - 4.0), (mx + r + 0.4, my - 4.0)], color=MID["mark"], lw=1.0, head=1.3)
    cv.text(93.6, my - 6.4, "result", size=6.1, color=MID["ink"], style="italic")

    # orchestration
    card(cv, 98, 2, 78, 31.4, ORC, "Orchestration", "when work is delegated to a new agent, and how", em="orchestration")
    comp(cv, 100.5, 6.4, 49.0, 14.4, "C5", ORC)
    if icon("subagent"):
        cv.image(icon("subagent"), 163.0, 15.6, 10.0, fit="height")
    else:
        cv.icon_robot(163.0, 15.0, 6.4, color=ORC["mark"])
    cv.text(163.0, 7.8, "new agent", size=6.0, color=ORC["ink"], style="italic")
    cv.arrow([(151.4, 13.6), (157.8, 13.6)], color=ORC["mark"], lw=0.8, head=1.0)
    # delegation from the model
    cv.arrow([(mx + 6.0, my - r + 2.0), (92.0, 26.0), (92.0, 13.6), (100.5, 13.6)], color=ORC["mark"],
             lw=0.9, head=1.2, dashed=True, radius=1.4, both=True)
    cv.text(86.0, 33.4, "delegate", size=6.0, color=ORC["ink"], ha="right", style="italic")

    # output
    cv.arrow([(mx - 7.0, my - (r * r - 49.0) ** 0.5), (mx - 7.0, 24.0)], color=INK, lw=1.0, head=1.3)
    if icon("f_out"):
        cv.image(icon("f_out"), mx - 7.0, 17.4, 9.6)
    else:
        cv.doc(mx - 10.2, 11.0, 6.4, 13.0, NEU, lines=4, fold=2.0)
    cv.text(mx - 0.8, 20.4, r"trajectory $\tau$", size=6.7, color=INK, ha="left")
    cv.text(mx - 0.8, 15.4, r"+ deliverable $y$", size=6.7, color=INK, ha="left")
    cv.text(mx, 5.6, r"output of $\mathcal{A}(q;\,\mathcal{M},\mathcal{H})$", size=6.2, color=MUTED)

    lift(cv, KEY)
    cv.legend(2, 1.2, 174, [("snow", "#4A90C8", "frozen: weights never change"),
                            ("cycle", MID["mark"], "tool loop: call, plugin hook, tool, result"),
                            ("dash", ORC["mark"], "delegation to a subagent"),
                            ("abbr", "C1–C8", "editable harness component files"),
                            ("cuboid", CTX, r"context entry ($q$ = task)")], size=6.0, gap=3.4)
    assert not cv.wire_crossings(), cv.wire_crossings()
    print("\n".join(cv.save(os.path.join(a.out, "harness2_fig2_components"))))
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()


if __name__ == "__main__":
    main()
