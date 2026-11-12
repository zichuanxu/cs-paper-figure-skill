"""ToolSpace Figure 1: a tool-space layer, one state-aware walk through it, and what the walks buy.

Source: Dong et al., "ToolSpace: Scaling Tool-Centric Environment Synthesis for Long-Horizon Agents",
arXiv:2611.05036v1, Figure 1 (p. 1), Table 1 (p. 12), Table 2 (p. 13), Sections 4.2 and 4.3.

Content kept from the source
  * (a) An agent, a Tool Space layer of tools (Search, Read, Query, Write, Message, Update, chained;
    "tools are atomic units") and the MCP servers and underlying environments below it (GitHub, Slack,
    Notion, Drive, Postgres, SQLite, GitLab, Redis, Brave, Sentry); tool calls go down, observations come up.
  * (b) The global tool graph clustered into environments (Spreadsheets, Files, Mail, Messaging and an
    unnamed one) and one walk of eight calls, in order: values.get, spreadsheets.get, batchUpdate,
    files.list, files.get, mail.list, messages.get, messages.send, from START to END across four
    environments. The background nodes and edges are an illustration of the graph, as in the source.
  * (c) Scores of ToolSpace-744B-A40B against GLM 5.2, GPT 5.6 Sol and Kimi K3, and of ToolSpace-35B-A3B
    against Qwen3.6-35B-A3B, Muse-Glimmer-30B and Qwen3.6-27B, on the seven benchmarks: every value from
    Table 1, plus the reported averages.
  * (d) Scores of frontier models on AutomationBench Pro and tau^3-Bench Banking Pro: every value from
    Table 2.

Design decisions
  * Strengths of the source that are kept: the tool space drawn as a plate floating between the agent and a
    plate of MCP servers, the servers and the models shown by their own marks, and radar charts for the claim
    that one model is ahead on nearly every benchmark (references/toolspace-study-2026-11.md).
  * (a) Two isometric plates. Tools stand on the upper one as tiles in a chain, the ten servers stand on the
    lower one as logo tiles with their names; calls go down and observations come up through the gaps. The
    upper plate opens by zoom rays into (b), the largest panel.
  * One hue per environment (green Spreadsheets, amber Files, coral Mail, purple Messaging, grey for the
    rest of the space). A walk node, its row in the tool chain and its cluster share that hue, so the
    chain reads as 3 + 2 + 1 + 2 calls in four environments without counting arrows.
  * Blue is ToolSpace everywhere: the plate in (a), the walk in (b), the models trained on its tasks
    in (c), the Pro splits built with it in (d).
  * API names are monospace and are listed once, in walk order, in the tool chain beside the graph; the
    graph carries only the step numbers, so no label covers an edge.
  * (c) keeps the two radars and repairs them: the ToolSpace model is blue in both and drawn last, its value
    is printed at every vertex, and on the one axis it does not win (tau^3-Bench Banking at 744B) the
    winner's value is printed beside it. Each axis runs from 0 to its best score, which the card says. The
    backbone each model was trained from is rose in both charts, and the key gives the reported averages.
  * (d) shows the drop the text claims: for each model a pale bar to its Standard score and a blue bar to
    its Pro score, with the Pro score and the difference printed. The source figure drew Pro bars only, for
    six of the seven models in Table 2; the seventh, DeepSeek-V4.1-Flash-1017, has the 38.2-point drop quoted
    in the text. Each row starts with the model's mark and name.
  * Rows keep the order of Table 2. Averages, gains and differences are asserted against the tables.
  * Logos are the marks embedded in the source PDF, unmodified (logos/); --no-logos draws initials instead.
    They are trademarks of their owners and identify the products only.
"""
import argparse
import math
import os
import sys

import numpy as np
from matplotlib import patheffects
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import INK, MUTED, ROLE, Canvas, mix  # noqa: E402

STEM = "toolspace_fig1_overview"
W, H = 178.0, 123.5
B = 54.5  # bottom of the top row
BLUE = ROLE["blue"]
GREY, GREY2 = "#5E6875", "#8E99A8"
MONO = dict(family="monospace")

# ------------------------------------------------------------------ (a), (b): reported structure ---
TOOLS = ["Search", "Read", "Query", "Write", "Message", "Update"]
SERVERS = ["GitHub", "Slack", "Notion", "Drive", "Postgres", "SQLite", "GitLab", "Redis", "Brave", "Sentry"]
LOGO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logos")
USE_LOGOS = True  # --no-logos: initials in the tiles
VENDOR = {"Claude": "claude", "GPT": "openai", "DeepSeek": "deepseek", "GLM": "zai", "Qwen": "qwen"}
ENV = {"Spreadsheets": "memory", "Files": "amber", "Mail": "coral", "Messaging": "purple"}
WALK = [("values.get", "Spreadsheets"), ("spreadsheets.get", "Spreadsheets"), ("batchUpdate", "Spreadsheets"),
        ("files.list", "Files"), ("files.get", "Files"), ("mail.list", "Mail"),
        ("messages.get", "Messaging"), ("messages.send", "Messaging")]
assert len(WALK) == 8 and len(dict.fromkeys(e for _, e in WALK)) == 4

# ------------------------------------------------------------------ (c): Table 1, p. 12 ---
BENCH = ["AutomationBench", "SkillsBench", "JobBench", "τ³-Bench Banking", "BFCL V4", "Harvey LAB",
         "OfficeQA Pro"]
T1 = {  # seven benchmark scores in the order of BENCH, then the reported average
    "ToolSpace-744B-A40B": ([54.7, 67.8, 57.5, 43.3, 78.4, 27.5, 67.1], 56.6),
    "GLM 5.2": ([29.3, 56.7, 43.4, 37.1, 75.6, 13.3, 56.9], 44.6),
    "GPT 5.6 Sol": ([47.1, 62.5, 45.4, 46.9, 68.8, 5.0, 66.4], 48.9),
    "Kimi K3": ([44.8, 51.9, 54.3, 37.1, 69.1, 25.4, 65.4], 49.7),
    "ToolSpace-35B-A3B": ([45.8, 42.4, 40.0, 34.0, 74.3, 1.7, 48.9], 41.0),
    "Qwen3.6-35B-A3B": ([8.2, 30.7, 6.4, 9.3, 60.0, 0.8, 45.9], 23.0),
    "Muse-Glimmer-30B": ([14.2, 32.9, 3.5, 11.3, 55.5, 0.0, 13.5], 18.7),
    "Qwen3.6-27B": ([10.7, 22.1, 5.6, 15.8, 58.5, 0.8, 38.4], 21.7),
}
SCALES = [("ToolSpace-744B-A40B", "GLM 5.2", "GPT 5.6 Sol", "Kimi K3"),       # hero, its backbone, two others
          ("ToolSpace-35B-A3B", "Qwen3.6-35B-A3B", "Muse-Glimmer-30B", "Qwen3.6-27B")]
for _m, (_v, _avg) in T1.items():
    assert len(_v) == 7 and abs(sum(_v) / 7 - _avg) < 0.06, (_m, sum(_v) / 7, _avg)
GAIN = [round(T1[h][1] - T1[b][1], 1) for h, b, *_ in SCALES]
assert GAIN == [12.0, 18.0], GAIN  # 44.6 -> 56.6 and 23.0 -> 41.0 (abstract; "18.0 points" in Sec. 6.2)

# ------------------------------------------------------------------ (d): Table 2, p. 13 ---
T2 = [  # model, AutomationBench (Std, Pro, delta), tau^3-Bench Banking (Std, Pro, delta)
    ("Claude Opus 5.5", (59.2, 26.3, -32.9), (51.5, 35.7, -15.8)),
    ("GPT 6.1 Sol", (50.8, 24.7, -26.1), (46.4, 29.6, -16.8)),
    ("DeepSeek-V4.1-Flash-1017", (60.5, 22.3, -38.2), (51.3, 36.9, -14.4)),
    ("DeepSeek-V4.1-Flash", (54.8, 20.0, -34.8), (50.3, 35.7, -14.6)),
    ("GLM 5.3", (52.5, 22.7, -29.8), (40.2, 20.4, -19.8)),
    ("Qwen 3.8 Max", (49.7, 24.0, -25.7), (55.2, 29.6, -25.6)),
    ("GLM 5.2", (29.3, 18.0, -11.3), (37.1, 12.2, -24.9)),
]
for _m, *_cols in T2:
    for _s, _p, _d in _cols:
        assert round(_p - _s, 1) == _d, (_m, _s, _p, _d)
assert len(T2) == 7 and min(a[2] for _, a, _ in T2) == -38.2  # "seven frontier models drop by up to 38.2 points"


# ------------------------------------------------------------------------------ helpers ---
def tw(cv, s, size, **kw):
    t = cv.ax.text(0, 0, s, fontsize=size, **kw)
    bb = t.get_window_extent(cv._renderer())
    t.remove()
    return bb.width / cv.fig.dpi * 25.4


def seg_dist(p, a, b):
    p, a, b = (np.asarray(v, float) for v in (p, a, b))
    t = np.clip(np.dot(p - a, b - a) / np.dot(b - a, b - a), 0, 1)
    return float(np.linalg.norm(p - (a + t * (b - a))))


def crosses(a, b, c, d):
    """True if segments ab and cd properly intersect (shared endpoints do not count)."""
    def o(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    if {tuple(a), tuple(b)} & {tuple(c), tuple(d)}:
        return False
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def gabriel(pts):
    """Edges (i, j) with no third point inside the circle on diameter ij: a planar, organic-looking net."""
    P = np.asarray(pts, float)
    E = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            d2 = ((P - (P[i] + P[j]) / 2) ** 2).sum(1)
            d2[[i, j]] = np.inf
            if (d2 > ((P[i] - P[j]) ** 2).sum() / 4 * 0.999).all():
                E.append((i, j))
    return E


def mark(cv, kind, x, y, s, fc, ec="white", lw=0.5, z=9):
    """Chart mark centred at (x, y), s mm across: dot, ring, diamond or triangle."""
    if kind in ("dot", "ring"):
        cv.ax.add_patch(Circle((x, y), s / 2, fc=fc, ec=ec, lw=lw, zorder=z))
    elif kind == "diamond":
        cv.ax.add_patch(Polygon([(x - s / 2, y), (x, y + s / 2), (x + s / 2, y), (x, y - s / 2)], closed=True, fc=fc,
                                ec=ec, lw=lw, zorder=z, joinstyle="miter"))
    else:
        cv.ax.add_patch(Polygon([(x - s / 2, y - s * 0.42), (x + s / 2, y - s * 0.42), (x, y + s * 0.5)], closed=True,
                                fc=fc, ec=ec, lw=lw, zorder=z, joinstyle="miter"))


def tool_glyph(cv, name, x, y, s, col, z=11):
    """Generic pictogram for a tool kind, drawn inside its node."""
    ax = cv.ax
    if name == "Search":
        ax.add_patch(Circle((x - s * 0.1, y + s * 0.1), s * 0.27, fc="none", ec=col, lw=0.8, zorder=z))
        ax.plot([x + s * 0.11, x + s * 0.4], [y - s * 0.11, y - s * 0.4], color=col, lw=1.1, zorder=z,
                solid_capstyle="round")
    elif name == "Read":
        w, h, f = s * 0.62, s * 0.8, s * 0.2
        ax.add_patch(Polygon([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2 - f),
                              (x + w / 2 - f, y + h / 2), (x - w / 2, y + h / 2)], closed=True, fc="white", ec=col,
                             lw=0.7, zorder=z, joinstyle="round"))
        for k in range(3):
            yy = y + h * 0.18 - k * h * 0.2
            ax.plot([x - w * 0.28, x + w * (0.28 if k < 2 else 0.05)], [yy, yy], color=col, lw=0.6, zorder=z)
    elif name == "Query":
        w, h, e = s * 0.66, s * 0.74, s * 0.2
        for k in (2, 1, 0):
            yy = y - h / 2 + e / 2 + k * (h - e) / 2
            ax.add_patch(Ellipse((x, yy), w, e, fc=BLUE["soft"] if k < 2 else "white", ec=col, lw=0.7, zorder=z))
        for xx in (x - w / 2, x + w / 2):
            ax.plot([xx, xx], [y - h / 2 + e / 2, y + h / 2 - e / 2], color=col, lw=0.7, zorder=z)
    elif name == "Write":
        u, n = np.array([1, 1]) / math.sqrt(2), np.array([-1, 1]) / math.sqrt(2)
        c, hw = np.array([x, y]), s * 0.11
        a, b = c - u * s * 0.2, c + u * s * 0.42
        ax.add_patch(Polygon([a + n * hw, b + n * hw, b - n * hw, a - n * hw], closed=True, fc="white", ec=col, lw=0.7,
                             zorder=z, joinstyle="round"))
        ax.add_patch(Polygon([a + n * hw, a - n * hw, c - u * s * 0.44], closed=True, fc=col, ec=col, lw=0.7,
                             zorder=z, joinstyle="round"))
    elif name == "Message":
        w, h = s * 0.82, s * 0.56
        ax.add_patch(Polygon([(x - w * 0.22, y - h / 2 + s * 0.08), (x - w * 0.3, y - h / 2 - s * 0.14),
                              (x + w * 0.02, y - h / 2 + s * 0.08)], closed=True, fc="white", ec=col, lw=0.7, zorder=z))
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2 + s * 0.08), w, h, fc="white", ec=col, lw=0.7, zorder=z + 0.1,
                                    boxstyle=f"round,pad=0,rounding_size={h * 0.3}"))
        ax.plot([x - w * 0.14, x + w * 0.05], [y - h / 2 + s * 0.08] * 2, color="white", lw=1.0, zorder=z + 0.2)
        for k in (-1, 0, 1):
            ax.add_patch(Circle((x + k * w * 0.22, y + s * 0.08), s * 0.05, fc=col, ec="none", zorder=z + 0.3))
    else:
        cv.icon_cycle(x, y, s * 0.95, color=col, z=z, lw=0.8)


# ---------------------------------------------------------------- (a) the layer ---
def logo_tile(cv, key, cx, cy, s, label=None, **kw):
    """A product or model mark in a white tile; initials when the mark is unavailable."""
    path = os.path.join(LOGO_DIR, key + ".png")
    if USE_LOGOS and os.path.exists(path):
        return cv.tile(cx, cy, s, image=path, label=label, **kw)
    return cv.tile(cx, cy, s, label=label, glyph=lambda x, y, z: cv.text(x, y, (label or key)[:1].upper(), size=6.0,
                                                                         weight="bold", color=GREY, z=12), **kw)


def panel_a(cv):
    cv.label(1.5, B + 65.3, "a", "The philosophy of Tool Space")
    nb = ROLE["neutral"]
    PX, PW_, SK = 3.0, 45.5, 5.0
    # agent
    cv.box(14.5, B + 53.2, 20.0, 7.3, "neutral", fill="white", stroke=nb["ink"], lw=0.8, radius=1.6, name="agent",
           shadow=True)
    cv.icon_robot(19.6, B + 56.95, 5.0, color=nb["ink"], lw=0.8)
    cv.text(27.6, B + 56.8, "Agent", size=7.2, weight="bold", color=nb["ink"])
    cv.block_arrow(18.0, B + 53.0, 18.0, B + 47.0, width=1.3, color=BLUE["stroke"])
    cv.block_arrow(31.0, B + 47.0, 31.0, B + 53.0, width=1.3, color=GREY2)
    cv.text(16.2, B + 50.2, "Tool calls", size=6.0, style="italic", color=BLUE["ink"], ha="right")
    cv.text(32.8, B + 50.2, "Observations", size=6.0, style="italic", color=nb["ink"], ha="left")

    # the Tool Space plate (hero of this panel; it opens into panel b): tools stand on it as tiles
    y0, d, t = B + 31.0, 15.5, 3.2
    up = cv.plate(PX, y0, PW_, d, skew=SK, t=t, r="blue", label="Tool Space", size=7.2)
    s = 4.4
    pos = []
    for k in range(6):
        v = 0.64 if k % 2 == 0 else 0.33
        pos.append(up.at((11.8 + 6.7 * k - PX - v * SK) / PW_, v))
    for (x0, y0_), (x1, y1) in zip(pos, pos[1:]):
        L = math.hypot(x1 - x0, y1 - y0_)
        ux, uy = (x1 - x0) / L, (y1 - y0_) / L
        e = s / 2 / max(abs(ux), abs(uy)) + 0.3
        cv.arrow([(x0 + ux * e, y0_ + uy * e), (x1 - ux * e, y1 - uy * e)], color=BLUE["ink"], lw=0.8, head=1.2)
    for k, ((x, y), name) in enumerate(zip(pos, TOOLS)):
        cv.tile(x, y, s, r="blue", z=10, glyph=lambda cx, cy, z, n=name: tool_glyph(cv, n, cx, cy, z, BLUE["ink"], z=12))
        cv.text(x, y + (s / 2 + 1.35 if k % 2 == 0 else -s / 2 - 1.3), name, size=6.0, color=BLUE["ink"])

    # calls and observations continue to the servers through the gap between the plates
    yb, d2 = B + 4.2, 19.0
    for xa in (11.5, 43.5):
        cv.block_arrow(xa, y0 - t - 0.3, xa, yb + d2 + 0.5, width=1.3, color=BLUE["stroke"])
        cv.block_arrow(xa + 2.3, yb + d2 + 0.5, xa + 2.3, y0 - t - 0.3, width=1.3, color=GREY2)
    cv.text(28.2, (y0 - t + yb + d2) / 2, "tools are atomic units", size=6.0, style="italic", color=BLUE["ink"])

    # MCP servers and the environments behind them: ten marks on the lower plate
    cv.plate(PX, yb, PW_, d2, skew=SK, t=2.8, r="frozen", label="MCP servers and underlying environments", size=5.8,
             grad=("#F8FAFD", "#DDE5F0"))
    for i, name in enumerate(SERVERS):
        v = 0.72 if i < 5 else 0.29
        logo_tile(cv, name.lower(), PX + PW_ / 2 + v * SK + 8.4 * (i % 5 - 2), yb + v * d2, 4.6, label=name, size=5.8,
                  r="frozen", weight="normal")
    return (PX + PW_ + SK, y0 + d), (PX + PW_ + SK, y0 + d - t)   # the back edge of the plate's right face


# ---------------------------------------------------------------- (b) graph and walk ---
CLUSTERS = [  # name, role, centre x, centre y (above B), rx, ry, title position (above B) or None
    ("Spreadsheets", "memory", 80.0, 45.5, 14.8, 10.8, 58.4),
    ("Messaging", "purple", 123.5, 46.5, 15.5, 10.3, 58.9),
    (None, "neutral", 76.5, 18.5, 10.5, 8.2, None),
    ("Files", "amber", 104.5, 23.0, 13.8, 10.2, 10.6),
    ("Mail", "coral", 131.5, 19.5, 11.5, 8.6, 8.7),
]
NODES = [(71.5, 50.0), (85.0, 47.8), (86.5, 38.7), (98.5, 27.3), (111.0, 19.5), (129.5, 18.5), (132.0, 40.5),
         (118.5, 49.5)]  # walk nodes 1..8, y above B
BRIDGES = [(0, 2), (2, 3), (0, 1), (3, 1)]  # cluster pairs joined by one grey edge (the walk joins the others)


def panel_b(cv):
    X0, PW, PH = 62.5, 114.0, 67.5
    cv.section(X0, B, PW, PH, "blue", fill="white", lw=0.8)
    cv.label(X0 + 2.0, B + 65.3, "b", "Tool-composition graph and state-aware walks")
    rng = np.random.default_rng(7)
    walk = [(x, B + y) for x, y in NODES]
    segs = list(zip(walk, walk[1:]))
    tags = [(walk[0][0], walk[0][1] - 3.5, "START"), (walk[7][0], walk[7][1] + 3.5, "END")]

    def on_tag(p, mx=5.4, my=1.9):
        return any(abs(p[0] - tx) < mx and abs(p[1] - ty) < my for tx, ty, _ in tags)

    def keep_out(p):
        return any(seg_dist(p, a, b) < 2.5 for a, b in segs) or on_tag(p)

    def clear(p, q):  # an edge may not cross the walk or run under START / END
        return (not any(crosses(p, q, a, b) for a, b in segs)
                and not any(on_tag((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t), 4.6, 1.3)
                            for t in np.linspace(0, 1, 15)))

    nets = []
    for name, r, cx, cy, rx, ry, ty in CLUSTERS:
        c, cy = ROLE[r], B + cy
        inside = [p for p in walk if ((p[0] - cx) / rx) ** 2 + ((p[1] - cy) / ry) ** 2 < 1]
        assert len(inside) == sum(e == name for _, e in WALK), (name, inside)
        pts = list(inside)
        for _ in range(6000):
            a, q = rng.uniform(0, 2 * math.pi), math.sqrt(rng.uniform(0, 1))
            p = (cx + rx * 0.9 * q * math.cos(a), cy + ry * 0.9 * q * math.sin(a))
            if all(math.hypot(p[0] - u[0], p[1] - u[1]) >= 3.0 for u in pts) and not keep_out(p):
                pts.append(p)
        cv.ax.add_patch(Ellipse((cx, cy), 2 * rx, 2 * ry, fc=c["fill"] if name else "#F1F2F4",
                                ec=mix(c["stroke"], "#FFFFFF", 0.45), lw=0.5, zorder=2))
        ecol = mix(c["stroke"], "#FFFFFF", 0.15)
        for i, j in gabriel(pts):
            if clear(pts[i], pts[j]) and (pts[i], pts[j]) not in segs:
                cv.ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], color=ecol, lw=0.45, zorder=3)
        for p in pts[len(inside):]:
            cv.ax.add_patch(Circle(p, 0.48, fc=c["stroke"], ec="none", zorder=4))
        if name:
            cv.text(cx, B + ty, name, size=7.2, weight="bold", color=c["ink"])
        nets.append(pts[len(inside):])
    for i, j in BRIDGES:  # the space is one graph: clusters are linked
        p, q = min(((p, q) for p in nets[i] for q in nets[j]), key=lambda e: math.dist(*e))
        if clear(p, q):
            cv.ax.plot([p[0], q[0]], [p[1], q[1]], color="#AEB5BF", lw=0.45, zorder=2.5)

    # the walk
    Rb = 1.75
    for (x0, y0), (x1, y1) in segs:
        L = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        cv.arrow([(x0 + ux * (Rb + 0.2), y0 + uy * (Rb + 0.2)), (x1 - ux * (Rb + 0.25), y1 - uy * (Rb + 0.25))],
                 color=BLUE["mark"], lw=1.25, head=1.9, halo=True, z=9)
    for k, ((x, y), (_, env)) in enumerate(zip(walk, WALK)):
        cv.badge(x, y, k + 1, ENV[env], d=2 * Rb, size=6.0)
    for tx, ty, s in tags:
        cv.text(tx, ty, s, size=5.8, weight="bold", color=INK,
                path_effects=[patheffects.withStroke(linewidth=1.6, foreground="white")])

    # key
    ky, kx = B + 3.6, X0 + 3.0
    cv.ax.plot([kx, kx + 4.6], [ky, ky], color=GREY2, lw=0.5, zorder=5)
    for xx in (kx, kx + 4.6):
        cv.ax.add_patch(Circle((xx, ky), 0.48, fc=GREY2, ec="none", zorder=6))
    cv.text(kx + 6.0, ky, "global tool space: 2,042 tools in 804 environments", size=6.0, ha="left")
    kx2 = kx + 6.0 + tw(cv, "global tool space: 2,042 tools in 804 environments", 6.0) + 5.0
    cv.arrow([(kx2, ky), (kx2 + 5.6, ky)], color=BLUE["mark"], lw=1.25, head=1.9)
    cv.text(kx2 + 7.0, ky, "one state-aware walk (a depth-first traversal)", size=6.0, ha="left")

    # the same walk as a tool chain
    x, w, top, rh = 147.6, 27.0, B + 61.2, 3.9
    Hc = 4.4 + 0.5 + 8 * rh + 0.8
    cv.box(x, top - Hc, w, Hc, "neutral", fill="white", stroke=ROLE["neutral"]["stroke"], lw=0.6, radius=1.2,
           container=True)
    cv.text(x + 1.8, top - 2.3, "Tool chain", size=7.2, weight="bold", ha="left")
    cv.text(x + w - 1.8, top - 2.3, "in walk order", size=5.8, style="italic", color=MUTED, ha="right")
    k = 0
    for env, r in ENV.items():
        n = sum(e == env for _, e in WALK)
        c = ROLE[r]
        yb = top - 4.4 - 0.5 - (k + n) * rh
        cv.ax.add_patch(FancyBboxPatch((x + 0.8, yb + 0.25), w - 1.6, n * rh - 0.5, fc=c["fill"], ec=c["stroke"],
                                       lw=0.4, boxstyle="round,pad=0,rounding_size=0.8", zorder=6))
        for i in range(n):
            y = top - 4.4 - 0.5 - (k + i + 0.5) * rh
            cv.badge(x + 3.2, y, k + i + 1, r, d=2.9, size=5.8)
            cv.text(x + 5.4, y - 0.05, WALK[k + i][0], size=5.8, color=c["ink"], ha="left", **MONO)
            assert x + 5.4 + tw(cv, WALK[k + i][0], 5.8, **MONO) < x + w - 1.0
        k += n
    cb = top - Hc
    cv.arrow([(152.0, cb), (152.0, B + 13.3)], lw=0.8)
    cv.text(155.0, cb - 3.3, "8 calls across", size=7.2, weight="bold", color=BLUE["ink"], ha="left")
    cv.text(155.0, cb - 6.1, "4 environments", size=7.2, weight="bold", color=BLUE["ink"], ha="left")
    cv.doc(149.6, B + 6.4, 4.8, 6.6, "blue", lines=3)
    cv.text(155.9, B + 11.0, "task $q$ + checks $V$,", size=6.0, ha="left")
    cv.text(155.9, B + 8.3, "kept if replay passes", size=6.0, ha="left")
    for s in ("task $q$ + checks $V$,", "kept if replay passes"):
        assert 155.9 + tw(cv, s, 6.0) < X0 + PW - 1.0, s
    return (X0, B, PW, PH)


# ---------------------------------------------------------------- chart scaffolding ---
def chart_card(cv, x, w, letter, title, note):
    cv.group(x, 1.5, w, 50.0, "neutral", f"({letter}) {title}", band=True, fill="white", size=8.0, color=INK)
    cv.text(x + w - 2.0, 1.5 + 50.0 - 2.48, note, size=6.0, style="italic", color=MUTED, ha="right", z=3)


def value_axis(cv, x0, mm, vmax, ticks, y0, y1):
    """Zero-based value axis from x0, mm per score point, with light verticals up to y1."""
    for t in ticks:
        cv.ax.plot([x0 + t * mm] * 2, [y0, y1], color="#E3E6EA", lw=0.5, zorder=2)
        cv.text(x0 + t * mm, y0 - 1.9, str(t), size=5.8, color="#4A5059")
    cv.ax.plot([x0, x0 + vmax * mm], [y0, y0], color="#9AA0A8", lw=0.6, zorder=3)


# ---------------------------------------------------------------- (c) generalization ---
RADAR_AXES = [b.replace("Harvey LAB", "Harvey\nLAB").replace("OfficeQA Pro", "OfficeQA\nPro") for b in BENCH]
RADAR_ROLES = ("blue", "rose", "teal", "neutral")   # ToolSpace, its backbone, two other models of that scale


def panel_c(cv):
    X, PW = 1.5, 88.5
    chart_card(cv, X, PW, "c", "Generalization across seven benchmarks", "each axis: 0 to its best score")
    for cx, models, gain in zip((X + 22.3, X + 65.6), SCALES, GAIN):
        hero, base, o1, o2 = models
        cv.radar(cx, 28.9, 11.0, RADAR_AXES, [(m, T1[m][0], r) for m, r in zip(models, RADAR_ROLES)], size=5.8)
        xl, xr = cx - 20.3, cx + 21.0

        def key(x, y, m, r, bold=False, tail=""):
            c = ROLE[r]
            cv.ax.plot([x, x + 3.0], [y, y], color=c["mark"], lw=1.6 if bold else 1.1, zorder=6, solid_capstyle="round")
            cv.text(x + 4.0, y, m + tail, size=5.8, ha="left", weight="bold" if bold else "normal",
                    color=c["ink"] if bold else INK)
            return x + 4.0 + tw(cv, m + tail, 5.8, weight="bold" if bold else "normal")

        key(xl, 9.3, hero, "blue", bold=True)
        cv.text(xr, 9.3, f"avg. {T1[hero][1]:.1f} (+{gain:.1f})", size=5.8, weight="bold", color=BLUE["ink"], ha="right")
        key(xl, 6.7, base, "rose", tail=", its backbone")
        cv.text(xr, 6.7, f"avg. {T1[base][1]:.1f}", size=5.8, ha="right")
        x2 = key(xl, 4.1, o1, "teal")
        assert key(x2 + 2.5, 4.1, o2, "neutral") < xr


# ---------------------------------------------------------------- (d) Standard -> Pro ---
def panel_d(cv):
    X, PW = 92.5, 84.0
    chart_card(cv, X, PW, "d", "Frontier models on Pro benchmarks", "score on each split")
    mm, nx, bh = 0.26, X + 26.2, 2.9
    rows = [37.3 - 4.55 * k for k in range(7)]
    ghost = dict(fc="#EDF0F4", ec="#A9B2BF", lw=0.45)
    for (m, *_), y in zip(T2, rows):
        cv.text(nx, y, m, size=6.0, ha="right")
        assert nx - tw(cv, m, 6.0) > X + 1.0, m
        logo_tile(cv, VENDOR[m.replace("-", " ").split()[0]], nx + 3.0, y, 3.5, shadow=False, pad=0.13, lw=0.35)
    cv.ax.add_patch(FancyBboxPatch((X + 2.2, 44.3 - 0.9), 4.0, 1.8, boxstyle="round,pad=0,rounding_size=0.4", zorder=5,
                                   **ghost))
    cv.text(X + 7.2, 44.3, "Standard split", size=5.8, ha="left")
    cv.gradient_rect(X + 2.2, 41.5 - 0.9, 4.0, 1.8, mix(BLUE["mark"], "#FFFFFF", 0.5), BLUE["mark"], z=5, radius=0.4)
    cv.text(X + 7.2, 41.5, "Pro split, by ToolSpace", size=5.8, ha="left", color=BLUE["ink"], weight="bold")
    assert X + 7.2 + tw(cv, "Pro split, by ToolSpace", 5.8, weight="bold") < nx + 5.5
    for x0, col, name in ((X + 32.1, 1, "AutomationBench"), (X + 59.1, 2, "τ³-Bench Banking")):
        value_axis(cv, x0, mm, 62, (0, 20, 40, 60), 6.6, 39.7)
        cv.text(x0 + 31 * mm, 43.0, name, size=6.0, weight="bold")
        dx = x0 + 62 * mm + 7.7
        cv.text(dx, 43.0, "Δ", size=6.0, weight="bold", ha="right")
        worst = min(r[col][2] for r in T2)
        for r, y in zip(T2, rows):
            std, pro, d = r[col]
            cv.ax.add_patch(FancyBboxPatch((x0, y - bh / 2), std * mm, bh, boxstyle="round,pad=0,rounding_size=0.5",
                                           zorder=4, **ghost))
            cv.gradient_rect(x0, y - bh / 2, pro * mm, bh, mix(BLUE["mark"], "#FFFFFF", 0.45), BLUE["mark"], z=6,
                             radius=0.5)
            lab = f"{pro:.1f}"
            if pro * mm >= tw(cv, lab, 5.8, weight="bold") + 1.1:   # inside the bar when it fits
                cv.text(x0 + pro * mm - 0.6, y - 0.05, lab, size=5.8, weight="bold", color="white", ha="right")
            else:
                cv.text(x0 + pro * mm + 0.7, y - 0.05, lab, size=5.8, weight="bold", color=BLUE["ink"], ha="left")
            cv.text(dx, y, f"−{-d:.1f}", size=6.0, ha="right", weight="bold" if d == worst else "normal")
        assert dx < X + PW - 0.8, dx


def build():
    cv = Canvas(W, H)
    p, q = panel_a(cv)
    fx, fy, _, fh = panel_b(cv)
    # the plate opens into (b): rays from the back edge of its right face to the frame
    cv.ax.add_patch(Polygon([p, (fx, fy + fh), (fx, fy), q], fc=BLUE["soft"], ec="none", alpha=0.45, zorder=1.9))
    for a, b in ((p, (fx, fy + fh)), (q, (fx, fy))):
        cv.ax.plot([a[0], b[0]], [a[1], b[1]], color=BLUE["stroke"], lw=0.5, ls=(0, (2.5, 1.6)), zorder=2)
    cv.block_arrow(56.2, B + 36.6, 61.6, B + 36.6, width=2.4, color=BLUE["stroke"])
    cv.text(58.3, B + 40.6, "Expand", size=6.0, style="italic", color=BLUE["ink"])
    panel_c(cv)
    panel_d(cv)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/toolspace")
    ap.add_argument("--no-logos", action="store_true", help="draw initials instead of the product and model marks")
    args = ap.parse_args()
    USE_LOGOS = not args.no_logos
    print(build().save(os.path.join(args.out, STEM)))
