"""Harness² Fig. 2: the eight components of the execution harness, placed where they act in the agent loop.

Source: Xu et al., "Harness²: Recursive Agent Harnessing for an Open World", arXiv:2610.14224, Fig. 2,
with Table 5 (files, activation, definitions) and Appendix D.1 (always-on files, on-demand components).

Kept from the source: the frozen model M; components C1-C8 with their names and file paths; the four
groups (context construction, tool interface, orchestration, middleware) and their one-line roles; the
activation of each component; the call / result loop through the plugin; delegation to a subagent that
returns only its result; the output, a trajectory tau and a deliverable y.

Design:
* Reading order follows one model call: files -> context -> frozen model -> tool call -> hook -> tools.
  The hero is the frozen model with the context it reads; every component sits where it acts on that loop.
* The context is drawn as an object, a stack of the text present at a call. Band colour = owning group,
  so C4 (tool guidance, an always-on file of the tool-interface group) shows up inside the context
  without a wire across the figure; the on-invoke skill is the dashed band, loaded after the task.
  Band order is illustrative; membership and activation follow Table 5.
* The plugin is a node ON the call and result wires: interposed in the tool loop, not a box beside it.
* Each component is a file card (file icon, C-number, name, path). Its activation is a tag on the card
  border: solid = reaches the model on every call, dashed = on demand.
* One hue per group, slate for the frozen model; the key strip defines the tags and the harness rack
  H = (c1..c8) that Fig. 3 (render_fig3.py) reuses. Palette and objects live in h2_style.py.

    python render_fig2.py --out DIR [--vector-icons]
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import h2_style as S  # noqa: E402
from h2_style import CONTEXT, INK, MID, MODEL, MONO, MUTED, ORCH, ROLE, TOOLS  # noqa: E402
from paperkit import Canvas  # noqa: E402

STEM = "harness2_fig2_components"
W, H = 178, 92
CARD_H = 13.6

# number, name, path, activation tag, on demand?   (Table 5)
COMP = {
    1: ("System prompt", "systemprompt.md", "every call", False),
    2: ("Guardrails", "guardrails.md", "every call", False),
    3: ("Memory", "LongTermMEMORY.md", "every call", False),
    6: ("Skills", "skills/<n>/SKILL.md", "on invoke", True),
    4: ("Tool guidance", "tool_guidance.md", "every call", False),
    7: ("Scripts", "scripts/<name>.py", "via bash", True),
    5: ("Subagents", "sub_agents/<n>/AGENT.md", "task tool", True),
    8: ("Plugin", "plugin/<name>.ts", "in tool loop", False),
}


def frame(cv, x, y, w, h, r, title, sub=None, tx=None, inline=False):
    """Group region: tinted field, dashed border in the group hue, title in its ink, one-line role in italic."""
    cv.section(x, y, w, h, r)
    tx = x + 2.4 if tx is None else tx
    cv.text(tx, y + h - 1.5, title, size=8.2, weight="bold", color=ROLE[r]["ink"], ha="left", va="top", z=4)
    if sub and inline:
        cv.text(tx + cv.text_width(title, 8.2, "bold") + 1.6, y + h - 1.85, sub, size=6.2, style="italic", color=MUTED,
                ha="left", va="top", z=4)
    elif sub:
        cv.text(tx, y + h - 5.2, sub, size=6.2, style="italic", color=MUTED, ha="left", va="top", z=4, linespacing=1.05)


def head(cv, x, y, k, r, ha="left"):
    """'C4 Tool guidance': number badge in the group mark, name in the group ink. (x, y) = left end, centre line."""
    name = COMP[k][0]
    bw = 5.0
    if ha == "center":
        x -= (bw + 1.1 + cv.text_width(name, 7.2, "bold")) / 2
    cv.ax.add_patch(S.FancyBboxPatch((x, y - 1.65), bw, 3.3, boxstyle="round,pad=0,rounding_size=0.8", fc=ROLE[r]["mark"],
                                     ec="none", zorder=8))
    cv.text(x + bw / 2, y - 0.05, f"C{k}", size=5.9, weight="bold", color="white", z=9)
    cv.text(x + bw + 1.1, y - 0.05, name, size=7.2, weight="bold", color=ROLE[r]["ink"], ha="left", z=9)


def file_card(cv, x, y, w, k, h=CARD_H):
    """One component = one editable file: icon, number + name, path; activation tag on the top border."""
    r = S.GROUP[k]
    _, path, act, demand = COMP[k]
    cv.box(x, y, w, h, r, fill="white", lw=0.7, radius=1.5, z=5)
    S.icon(cv, f"f_c{k}", x + 5.9, y + h / 2, 9.2, r, tint=(k == 8))
    head(cv, x + 12.0, y + h / 2 + 2.5, k, r)
    cv.text(x + 12.0, y + h / 2 - 2.5, path, size=5.9, color=INK, ha="left", z=9, **MONO)
    S.tag(cv, x + w - 1.6, y + h, act, r, dashed=demand)
    return (x, y, w, h)


def draw(out, vector=False):
    S.VECTOR = vector
    cv = Canvas(W, H)
    blue, slate = ROLE[CONTEXT], ROLE[MODEL]

    # ---- context construction: three always-on files and the on-invoke skill feed the context ----------------
    frame(cv, 2, 11.5, 64.5, 77.5, CONTEXT, "Context construction", "what enters the context, and when")
    cx, cw = 4.4, 46.0
    ys = [80.0 - CARD_H - i * (CARD_H + 2.9) for i in range(4)]
    for k, y in zip((1, 2, 3, 6), ys):
        file_card(cv, cx, y, cw, k)
    mid = [y + CARD_H / 2 for y in ys]

    # the context at one call: bands in the colour of the group that owns the text
    sx, sw, bh, stop = 56.6, 8.6, 5.0, 75.0
    bands = [("C1", CONTEXT, False), ("C2", CONTEXT, False), ("C3", CONTEXT, False), ("C4", TOOLS, False),
             ("task", "neutral", False), ("C6", CONTEXT, True)]
    sbot = stop - bh * len(bands)
    cv.box(sx - 0.5, sbot - 0.5, sw + 1.0, stop - sbot + 1.0, fill="white", stroke=slate["ink"], lw=0.8, radius=1.0, z=5,
           name="ctx")
    for i, (lab, r, demand) in enumerate(bands):
        c, by = ROLE[r], stop - (i + 1) * bh
        cv.ax.add_patch(S.Rectangle((sx, by), sw, bh, fc="white" if demand else c["soft"], ec=c["stroke"], lw=0.5,
                                    ls=(0, (2.2, 1.4)) if demand else "-", zorder=6))
        cv.text(sx + sw / 2, by + bh / 2 - 0.05, lab, size=6.0, color=c["ink"], weight="normal" if r == "neutral" else "bold",
                z=7)
    cv.text(sx + sw / 2, stop + 2.2, "context", size=6.6, weight="bold", color=slate["ink"])
    always = stop - 2 * bh  # middle of the four always-on bands
    bus = cx + cw + 2.0
    for m in mid[:3]:
        cv.line([(cx + cw, m), (bus, m)], color=blue["mark"], lw=0.8)
    cv.line([(bus, mid[2]), (bus, mid[0])], color=blue["mark"], lw=0.8)
    cv.arrow([(bus, always), (sx - 0.5, always)], color=blue["mark"], lw=0.9, head=1.3, start_dot=True)
    S.darrow(cv, [(cx + cw, mid[3]), (sx + sw / 2, mid[3]), (sx + sw / 2, sbot - 0.5)], color=blue["mark"])

    # ---- hero: the frozen model reads that context on every call ----------------------------------------------
    mx, my, mw, mh = 74.0, 45.0, 24.0, 28.0
    mcy = my + mh / 2
    cv.box(mx, my, mw, mh, MODEL, fill=slate["soft"], stroke=slate["ink"], lw=1.0, radius=2.2, shadow=True, z=5)
    S.icon(cv, "model", mx + mw / 2, my + mh - 9.6, 12.0, MODEL)
    cv.text(mx + mw / 2, my + 8.0, "Frozen model", size=7.8, weight="bold", color=slate["ink"], z=9)
    cv.text(mx + mw / 2, my + 3.6, r"$\mathcal{M}$", size=8.6, color=slate["ink"], z=9)
    cv.icon_snow(mx + mw - 3.0, my + mh - 3.0, 2.8, color=slate["mark"])
    cv.arrow([(sx + sw + 0.5, mcy), (mx, mcy)], color=blue["mark"], lw=1.1, head=1.6)

    # output: the execution record e = (tau, y)
    rx, ry, rw, rh = 70.0, 78.6, 32.0, 10.4
    cv.box(rx, ry, rw, rh, "neutral", fill="white", lw=0.7, radius=1.5, z=5)
    S.record(cv, rx + 2.2, ry + 1.8, MODEL)
    cv.text(rx + 9.2, ry + rh / 2 + 1.9, r"trajectory $\tau$", size=6.8, ha="left", z=9)
    cv.text(rx + 9.2, ry + rh / 2 - 2.0, r"+ deliverable $y$", size=6.8, ha="left", z=9)
    cv.arrow([(mx + mw / 2, my + mh), (mx + mw / 2, ry)], lw=0.8)

    # ---- middleware: the plugin sits on the call and result wires ---------------------------------------------
    ax_, aw = 106.5, 27.0
    frame(cv, ax_, 37.0, aw, 52.0, MID, "Middleware", "hooks every tool call")
    px, pw, py, ph = ax_ + 2.0, aw - 4.0, 50.0, 22.0
    cv.box(px, py, pw, ph, MID, fill="white", lw=0.8, radius=1.5, z=5)
    S.icon(cv, "f_c8", px + pw / 2, py + ph - 6.0, 8.6, MID, tint=True)
    head(cv, px + pw / 2, py + 8.2, 8, MID, ha="center")
    cv.text(px + pw / 2, py + 3.6, COMP[8][1], size=5.9, z=9, **MONO)
    S.tag(cv, px + pw - 1.6, py + ph, COMP[8][2], MID)
    cv.text(ax_ + aw / 2, 46.0, "enforces a behavior,", size=6.2, style="italic", color=MUTED)
    cv.text(ax_ + aw / 2, 43.0, "rather than instructs it", size=6.2, style="italic", color=MUTED)
    ycall, yres = mcy + 2.6, mcy - 2.6

    # ---- tool interface --------------------------------------------------------------------------------------------
    gx, gw = 136.5, 39.5
    frame(cv, gx, 37.0, gw, 52.0, TOOLS, "Tool interface", "what the model can call, and how")
    tx, tw = gx + 2.0, gw - 4.0
    ty, th = mcy - 4.6, 9.2
    c4 = file_card(cv, tx, ty + th + 3.5, tw, 4, h=12.2)
    c7 = file_card(cv, tx, ty - 3.5 - 12.2, tw, 7, h=12.2)
    cv.box(tx, ty, tw, th, TOOLS, fill=ROLE[TOOLS]["soft"], lw=0.8, radius=1.5, z=5)
    S.icon(cv, "tools", tx + 6.0, ty + th / 2, 7.6, TOOLS)
    cv.text(tx + 11.6, ty + th / 2 + 1.9, "Tools", size=7.2, weight="bold", color=ROLE[TOOLS]["ink"], ha="left", z=9)
    cv.text(tx + 11.6, ty + th / 2 - 2.0, "existing tools, bash", size=6.2, color=INK, ha="left", z=9)
    rel = tx + tw * 0.62  # relation arrows: a file configures the node it points at
    cv.arrow([(rel, c4[1]), (rel, ty + th)], color=MUTED, lw=0.6, head=1.1)
    cv.text(rel - 1.2, (c4[1] + ty + th) / 2, "guides use", size=5.9, style="italic", color=MUTED, ha="right")
    cv.arrow([(rel, c7[1] + c7[3]), (rel, ty)], color=MUTED, lw=0.6, head=1.1)
    cv.text(rel - 1.2, (c7[1] + c7[3] + ty) / 2, "adds a capability", size=5.9, style="italic", color=MUTED, ha="right")

    # call goes out through the plugin, the result comes back through it
    cv.arrow([(mx + mw, ycall), (px, ycall)], lw=0.9)
    cv.arrow([(px + pw, ycall), (tx, ycall)], lw=0.9)
    cv.arrow([(tx, yres), (px + pw, yres)], lw=0.9)
    cv.arrow([(px, yres), (mx + mw, yres)], lw=0.9)
    lx = (mx + mw + ax_) / 2
    cv.text(lx, ycall + 1.7, "call", size=6.2, style="italic", color=INK)
    cv.text(lx, yres - 1.8, "result", size=6.2, style="italic", color=INK)

    # ---- orchestration: a subagent is a new context, defined by AGENT.md ----------------------------------------
    ox, oy, ow, oh = 70.5, 11.5, 105.5, 22.5
    frame(cv, ox, oy, ow, oh, ORCH, "Orchestration", "when work is delegated to a new agent, and how", tx=ax_ + 2.4,
          inline=True)
    nx, ny, nw, nh = ox + 2.0, oy + 2.2, 33.0, 14.6
    cv.box(nx, ny, nw, nh, ORCH, fill=ROLE[ORCH]["soft"], lw=0.8, radius=1.5, z=5)
    S.icon(cv, "subagent", nx + 6.4, ny + nh / 2, 11.0, ORCH, fit="height")
    cv.text(nx + 12.6, ny + nh / 2 + 2.2, "Subagent", size=7.2, weight="bold", color=ROLE[ORCH]["ink"], ha="left", z=9)
    cv.text(nx + 12.6, ny + nh / 2 - 2.0, "own context window", size=6.2, color=INK, ha="left", z=9)
    c5 = file_card(cv, ox + ow - 2.0 - 47.0, ny, 47.0, 5, h=CARD_H)
    cv.arrow([(c5[0], ny + nh / 2 - 0.5), (nx + nw, ny + nh / 2 - 0.5)], color=MUTED, lw=0.6, head=1.1)
    cv.text((c5[0] + nx + nw) / 2, ny + nh / 2 + 1.2, "defines", size=5.9, style="italic", color=MUTED)
    dx, ux = mx + 7.0, mx + mw - 7.0
    S.darrow(cv, [(dx, my), (dx, ny + nh)], color=ROLE[ORCH]["mark"], lw=0.9, head=1.4)
    cv.arrow([(ux, ny + nh), (ux, my)], color=ROLE[ORCH]["mark"], lw=0.9)
    ly = (my + oy + oh) / 2 + 0.2
    cv.text(dx - 1.3, ly, "delegates", size=6.2, style="italic", color=ROLE[ORCH]["ink"], ha="right")
    cv.text(ux + 1.3, ly, "result only", size=6.2, style="italic", color=ROLE[ORCH]["ink"], ha="left")

    # ---- key ---------------------------------------------------------------------------------------------------------
    S.key(cv, 2, 1.0, 174, h=8.6, size=6.5, items=[
        (lambda x, y: cv.icon_snow(x, y, 2.8, color=slate["mark"]), 3.0, "frozen weights"),
        (lambda x, y: S.icon(cv, "f_c1", x, y, 5.6, CONTEXT), 5.6, "editable file; an edit is a diff"),
        (lambda x, y: S.tag(cv, x, y, "tag", "neutral", ha="center"), 6.6, "active on every call"),
        (lambda x, y: S.tag(cv, x, y, "tag", "neutral", dashed=True, ha="center"), 6.6, "on demand"),
        (lambda x, y: S.rack(cv, x - 7.3, y - 3.38, groups=True, cell=(3.4, 2.9)), 14.6,
         r"harness $\mathcal{H}=(c_1,\ldots,c_8)$, in group colours"),
    ])

    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=".")
    ap.add_argument("--vector-icons", action="store_true", help="draw vector stand-ins instead of the raster icons")
    a = ap.parse_args()
    print(draw(a.out, a.vector_icons))
