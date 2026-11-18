"""ToolSpace Figure 1, second redesign: one spine from the tool space to the numbers.

Source: Dong et al., "ToolSpace: Scaling Tool-Centric Environment Synthesis for Long-Horizon Agents",
arXiv:2611.05036v1. Figure 1 (p. 1), Figure 2 (p. 6), Sections 4.1 to 4.3 (pp. 5-10), Section 5 (p. 10),
Section 6.1 (p. 11), Table 1 (p. 12), Table 2 (p. 13).

Message
  ToolSpace pools the tools of 804 environments into one graph in which a tool call is the unit, samples
  state-aware random walks over it and turns each walk that replays into a task. The tasks do two things:
  models fine-tuned on them gain on seven benchmarks, and the same pipeline, anchored to two benchmarks
  with longer walks, gives Pro splits on which every frontier model falls.

Picture
  One isometric plate, the tool space, with the tool-composition graph drawn on it: four environments as
  coloured regions, the rest of the space grey, and one eight-call walk as the only saturated path with
  numbered stops. The agent calls a tool on the plate from above; a shelf of ten MCP servers, shown by
  their marks, feeds it from below through risers that come up as nodes. Two dashed leaders drop the walk
  onto a rail, where the same eight numbered stops carry their API names in their environment's hue. The
  rail funnels into one task card (q, V and the three kinds of check a replay must pass), and the card's
  two arrows turn down into the two results: radars on the left, falls on the right.

Hero
  The walk: the one saturated line on a pale plate, continued by the rail, the funnel and the fork in the
  same blue and the same weight.

Content kept from the source (all of Figure 1's facts) and added from the text
  * Agent, Tool Space, ten MCP servers; tool calls down, observations up; "tools are atomic units".
  * The walk of Figure 1(b): values.get, spreadsheets.get, batchUpdate, files.list, files.get, mail.list,
    messages.get, messages.send across Spreadsheets, Files, Mail and Messaging. Background nodes, edges
    and grey regions are a schematic of the rest of the graph, as in the source. The paper reports no
    mapping from the ten servers to the four named environments, so the risers end on grey nodes.
  * Counts from Section 4.3: 2,042 canonical tools, 77,760 tool-call-pattern nodes, 804 environments.
  * A walk becomes a task q with checks V = V_state, V_trace, V_out (final state, key snapshots, returned
    fields) and is kept only if its replay passes (Section 4.2.2).
  * 34,376 SFT samples (Section 6.1); Pro splits of 300 and 98 tasks from walks with larger L and K
    (Section 5).
  * Table 1 for the eight models of Figure 1(c); Table 2 for all seven frontier models (the source figure
    drew six, and Pro scores only).
  * The source's key calls the walk "one depth-first traversal"; Section 4.2.1 and Algorithm 1 define it
    as a state-aware random walk with rollback, which is what the figure says.

Design decisions
  * No panel frames, cards around charts or header bands. The scene, the rail and the two results sit bare
    on the page and are joined by the blue spine. The one card is the task: it bounds one real unit.
  * One hue per environment (green Spreadsheets, amber Files, coral Mail, purple Messaging) on its region,
    its stops and its name chips. Blue is ToolSpace: the plate, the walk, the spine, the ToolSpace
    polygons and the Pro falls. Everything else is grey; vendor colour appears only in the marks.
  * Radars are kept for the envelope claim. Every axis of both radars runs from 0 to 80, so a radius is a
    score and the two scales can be compared (the first redesign ran each axis to its own best score,
    which put 1.7 on Harvey LAB at the rim). ToolSpace's value is printed at every vertex, the rival's
    value and name where ToolSpace loses (tau^3-Bench Banking at 744B), and the average gain over the
    backbone is the bracket between the two averages.
  * The Pro result is drawn as a fall: a wedge from the Standard score down to the Pro score, the vendor's
    mark standing at the Pro score, the change printed under the mark. Filled = AutomationBench,
    open = tau^3-Bench Banking. Models are ordered by their fall on AutomationBench, largest first.
  * Type: Times, 8.0 pt heads and claim numbers, 6.8 pt labels, 6.0 pt notes, values and API names
    (monospace). Strokes: 0.6 pt outlines and thin arrows, 1.8 pt for the spine; hairlines of 0.45 pt in
    the graph and the grid. Radar polygons take cv.radar's own weights (1.25 / 0.85 pt).
  * Primitives defined here because paperkit lacks them: a graph projected onto a plate (Deck, mesh),
    a station rail with a funnel (rail), a fall wedge (falls). Logos are the marks embedded in the source
    PDF (logos/); --no-logos draws initials. They are trademarks of their owners and identify the
    products only.
"""
import argparse
import math
import os
import sys

import numpy as np
from matplotlib import patheffects
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import INK, ROLE, Canvas, mix  # noqa: E402

STEM = "toolspace_fig1_overview"
W, H = 178.0, 125.0
HEAD, LABEL, FINE = 8.0, 6.8, 6.0          # the three text sizes
LW, SPINE, HAIR = 0.6, 1.8, 0.45           # outline and thin arrow; the spine; graph and grid hairlines
BLUE = ROLE["blue"]
GREY, GREY2 = "#3A4250", "#7D8794"
MONO = dict(family="monospace")
LOGO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logos")
USE_LOGOS = True

# ------------------------------------------------------------------ reported structure (Figure 1) ---
SERVERS = ["GitHub", "Slack", "Notion", "Drive", "Postgres", "SQLite", "GitLab", "Redis", "Brave", "Sentry"]
ENV = {"Spreadsheets": "memory", "Files": "amber", "Mail": "coral", "Messaging": "purple"}
WALK = [("values.get", "Spreadsheets"), ("spreadsheets.get", "Spreadsheets"), ("batchUpdate", "Spreadsheets"),
        ("files.list", "Files"), ("files.get", "Files"), ("mail.list", "Mail"),
        ("messages.get", "Messaging"), ("messages.send", "Messaging")]
assert len(WALK) == 8 and list(dict.fromkeys(e for _, e in WALK)) == list(ENV)
N_TOOLS, N_NODES, N_ENVS = 2042, 77760, 804          # Section 4.3 (A), (B), pp. 9-10
N_SFT, N_PRO = 34376, (300, 98)                      # Section 6.1, p. 11; Section 5, p. 10

# ------------------------------------------------------------------ Table 1, p. 12 ---
BENCH = ["AutomationBench", "SkillsBench", "JobBench", "τ³-Bench Banking", "BFCL V4", "Harvey LAB",
         "OfficeQA Pro"]
T1 = {  # seven scores in the order of BENCH, then the reported average
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
assert GAIN == [12.0, 18.0], GAIN            # 44.6 -> 56.6 and 23.0 -> 41.0 (abstract; Section 6.2)
LOST = [[BENCH[i] for i in range(7) if max(T1[m][0][i] for m in ms[1:]) > T1[ms[0]][0][i]] for ms in SCALES]
assert LOST == [["τ³-Bench Banking"], []], LOST   # the one axis a drawn rival wins

# ------------------------------------------------------------------ Table 2, p. 13 ---
T2 = [  # model, AutomationBench (Std, Pro, delta), tau^3-Bench Banking (Std, Pro, delta), mark, name lines
    ("Claude Opus 5.5", (59.2, 26.3, -32.9), (51.5, 35.7, -15.8), "claude", ("Claude", "Opus 5.5")),
    ("GPT 6.1 Sol", (50.8, 24.7, -26.1), (46.4, 29.6, -16.8), "openai", ("GPT", "6.1 Sol")),
    ("DeepSeek-V4.1-Flash-1017", (60.5, 22.3, -38.2), (51.3, 36.9, -14.4), "deepseek",
     ("DeepSeek-", "V4.1-Flash", "-1017")),
    ("DeepSeek-V4.1-Flash", (54.8, 20.0, -34.8), (50.3, 35.7, -14.6), "deepseek", ("DeepSeek-", "V4.1-Flash")),
    ("GLM 5.3", (52.5, 22.7, -29.8), (40.2, 20.4, -19.8), "zai", ("GLM", "5.3")),
    ("Qwen 3.8 Max", (49.7, 24.0, -25.7), (55.2, 29.6, -25.6), "qwen", ("Qwen", "3.8 Max")),
    ("GLM 5.2", (29.3, 18.0, -11.3), (37.1, 12.2, -24.9), "zai", ("GLM", "5.2")),
]
for _m, _a, _b, _k, _lines in T2:
    for _s, _p, _d in (_a, _b):
        assert round(_p - _s, 1) == _d, (_m, _s, _p, _d)
    assert "".join(_lines).replace(" ", "") == _m.replace(" ", ""), _m
assert len(T2) == 7 and min(r[1][2] for r in T2) == -38.2     # "seven frontier models drop by up to 38.2 points"
assert all(d < 0 for r in T2 for d in (r[1][2], r[2][2]))     # every model falls on both
assert T2[6][1][0] == T1["GLM 5.2"][0][0] and T2[6][2][0] == T1["GLM 5.2"][0][3]   # the two tables agree


# ------------------------------------------------------------------------------ geometry helpers ---
class Deck:
    """A paperkit plate plus the map from its plane to the page. Plane coordinates are (p, r) in mm: p along
    the front edge, r into the plate; depth r is foreshortened to the plate's page depth and sheared by its
    skew, so anything laid out in the plane lies on the plate."""

    def __init__(self, cv, x, y, w, d, skew, depth, **kw):
        self.x, self.y, self.w, self.d, self.skew, self.depth = x, y, w, d, skew, depth
        self.plate = cv.plate(x, y, w, d, skew=skew, **kw)

    def at(self, p, r):
        q = r * self.d / self.depth
        return (self.x + p + q * self.skew / self.d, self.y + q)

    def plane(self, X, Y):
        q = Y - self.y
        return (X - self.x - q * self.skew / self.d, q * self.depth / self.d)


def seg_dist(p, a, b):
    p, a, b = (np.asarray(v, float) for v in (p, a, b))
    t = np.clip(np.dot(p - a, b - a) / np.dot(b - a, b - a), 0, 1)
    return float(np.linalg.norm(p - (a + t * (b - a))))


def cuts(a, b, c, d):
    """Do the open segments ab and cd intersect?"""
    def side(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return side(a, b, c) * side(a, b, d) < 0 and side(c, d, a) * side(c, d, b) < 0


def mesh(P, longest):
    """Gabriel graph of the points P, without edges longer than `longest`: (i, j) is kept when the circle on
    ij as diameter holds no third point. Planar, and it leaves no node without a neighbour."""
    P = np.asarray(P, float)
    out = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            d2 = float(((P[i] - P[j]) ** 2).sum())
            if d2 > longest ** 2:
                continue
            near = ((P - (P[i] + P[j]) / 2) ** 2).sum(1)
            near[[i, j]] = np.inf
            if near.min() > d2 / 4 * 0.999:
                out.append((i, j))
    return out


def halo(w=1.5):
    return [patheffects.withStroke(linewidth=w, foreground="white")]


def logo_tile(cv, key, cx, cy, s, label=None, **kw):
    """A product or model mark in a white tile; the initial when the mark is unavailable."""
    path = os.path.join(LOGO_DIR, key + ".png")
    if USE_LOGOS and os.path.exists(path):
        return cv.tile(cx, cy, s, image=path, label=label, size=FINE, **kw)
    return cv.tile(cx, cy, s, label=label, size=FINE, glyph=lambda x, y, z: cv.text(
        x, y, (label or key)[:1].upper(), size=FINE, weight="bold", color=GREY, z=12), **kw)


# ---------------------------------------------------------------- the scene: agent, space, servers ---
REGIONS = [  # name, role, centre (p, r), radii (p, r), label (p, r); plane mm on a 137 x 46 plate
    ("Spreadsheets", "memory", (24.0, 29.0), (15.0, 12.5), (24.0, 38.0)),
    ("Files", "amber", (56.0, 20.5), (14.5, 12.0), (56.0, 12.3)),
    ("Mail", "coral", (86.5, 30.0), (12.5, 11.5), (86.5, 38.2)),
    ("Messaging", "purple", (117.0, 21.0), (15.0, 12.5), (116.0, 12.3)),
    (None, None, (27.0, 8.0), (13.0, 5.2), None),      # the rest of the 804 environments, unnamed as in
    (None, None, (57.5, 40.0), (12.5, 4.8), None),     # the source figure
    (None, None, (87.5, 10.0), (11.5, 6.0), None),
    (None, None, (119.5, 40.2), (12.5, 4.6), None),
]
STOPS = [(13.5, 27.0), (24.0, 31.0), (33.5, 22.5), (48.0, 17.5), (63.0, 23.5), (86.0, 28.5), (108.0, 27.0),
         (124.0, 19.5)]                                 # the eight calls of the walk, plane mm
for (_p, _r), (_, _e) in zip(STOPS, WALK):             # every stop lies in its environment's region
    _c, _rad = next((c, rad) for n, _, c, rad, _ in REGIONS if n == _e)
    assert ((_p - _c[0]) / _rad[0]) ** 2 + ((_r - _c[1]) / _rad[1]) ** 2 < 0.8, (_e, _p, _r)


def scene(cv):
    """Returns the page positions of the eight stops."""
    PX, PY, PW, PD, PS, PT = 12.0, 92.5, 137.0, 29.0, 23.2, 3.8
    SX, SY, SW, SD, ST = 33.0, 73.4, 104.0, 10.5, 3.0
    rng = np.random.default_rng(11)

    # the shelf of servers and its marks
    shelf = cv.plate(SX, SY, SW, SD, skew=SD * PS / PD, t=ST, r="frozen", lw=LW, size=FINE,
                     label="MCP servers and underlying environments", grad=("#F8FAFD", "#DDE5F0"))
    tiles = []
    for i, name in enumerate(SERVERS):
        x, y = shelf.at(0.01 + 0.92 * (i + 0.5) / len(SERVERS), 0.62)   # names stay on the shelf
        logo_tile(cv, name.lower(), x, y, 5.2, label=name, r="frozen", weight="normal", lw=LW)
        tiles.append((x, y + 2.6))

    # the tool space
    deck = Deck(cv, PX, PY, PW, PD, PS, 46.0, t=PT, r="blue", lw=LW, grad=("#FBFDFF", "#D6E4F6"))
    fy = PY - PT / 2
    cv.text(PX + 25.0, fy, "Tool Space", size=LABEL, weight="bold", color="white", ha="left", z=5)
    x1 = PX + 25.0 + cv.text_width("Tool Space", LABEL, "bold") + 2.4
    cv.text(x1, fy, "tools are atomic units", size=FINE, style="italic", color="white", ha="left", z=5)
    cv.text(PX + PW - 9.0, fy, "node: a tool-call pattern  ·  edge: a dependency seen in real traces",
            size=FINE, color="white", ha="right", z=5)

    # risers: every server's tools come up through the plate and are nodes of the graph (ports). The paper
    # reports no server-to-environment mapping, so every riser is the same and none ends in a named region.
    ports = []
    for x, y in tiles:
        cv.arrow([(x, y + 0.5), (x, PY - PT)], color=GREY2, lw=LW, head=1.3)
        ports.append(deck.plane(x, PY + 1.7))

    stops = [deck.at(*s) for s in STOPS]
    segs = list(zip(stops, stops[1:]))
    tags = [(stops[0][0] - 5.2, stops[0][1] - 2.6, "START"), (stops[7][0] + 4.6, stops[7][1] - 2.6, "END")]
    boxes = [(x - 4.2, y - 1.4, x + 4.2, y + 1.4) for x, y, _ in tags]     # page rectangles kept free of nodes
    for name, _, _, _, lab in REGIONS:
        if name:
            x, y = deck.at(*lab)
            hw = cv.text_width(name, LABEL, "bold") / 2 + 1.0
            boxes.append((x - hw, y - 1.6, x + hw, y + 1.6))
    # the agent calls one tool: a node at the back-left corner of the plate
    ax_, ay = 8.4, 116.2
    called = (PX + (ay - PY) * PS / PD + 7.0, ay)
    boxes.append((called[0] - 6.0, ay - 2.2, called[0] - 0.8, ay + 2.2))

    def free(pt):
        X, Y = deck.at(*pt)
        return (all(seg_dist((X, Y), a, b) > 3.3 for a, b in segs)
                and not any(a - 0.6 < X < c + 0.6 and b - 0.6 < Y < d + 0.6 for a, b, c, d in boxes))

    def inside(pt, c, rad, f=1.0):
        return ((pt[0] - c[0]) / rad[0]) ** 2 + ((pt[1] - c[1]) / rad[1]) ** 2 < f * f

    def home(pt):  # index of the region a point lies in, or None
        return next((k for k, (_, _, c, rad, _) in enumerate(REGIONS) if inside(pt, c, rad)), None)

    fixed = list(STOPS) + ports + [deck.plane(*called)]
    pts = list(fixed)
    owner = [next(k for k, r in enumerate(REGIONS) if r[0] == e) for _, e in WALK] + [home(p) for p in fixed[8:]]
    assert all(k is None or REGIONS[k][0] is None for k in owner[8:])    # no port lies in a named environment

    def throw(draw, ok, dmin, who, tries):
        for _ in range(tries):
            c = draw()
            if ok(c) and free(c) and all(math.hypot(c[0] - u[0], c[1] - u[1]) >= dmin for u in pts):
                pts.append(c)
                owner.append(who if who is not None else home(c))

    for k, (name, _, c, rad, _) in enumerate(REGIONS):
        def draw(c=c, rad=rad):
            a, q = rng.uniform(0, 2 * math.pi), math.sqrt(rng.uniform(0, 1))
            return (c[0] + rad[0] * 0.9 * q * math.cos(a), c[1] + rad[1] * 0.9 * q * math.sin(a))
        throw(draw, lambda c_: True, 3.3 if name else 3.6, k, 2500)
    throw(lambda: (rng.uniform(2.5, PW - 2.5), rng.uniform(2.5, 43.5)), lambda c_: home(c_) is None, 5.2, None, 2500)

    # regions, edges, nodes
    for name, r, c, rad, lab in REGIONS:
        ring = [deck.at(c[0] + rad[0] * math.cos(t), c[1] + rad[1] * math.sin(t))
                for t in np.linspace(0, 2 * math.pi, 72, endpoint=False)]
        col = ROLE[r] if name else None
        cv.ax.add_patch(Polygon(ring, closed=True, fc=mix(col["soft"], col["fill"], 0.35) if name else "#E9EDF3",
                                ec=mix(col["stroke"], "#FFFFFF", 0.25) if name else "#B9C2CE", lw=LW, zorder=4.5))
        if name:
            x, y = deck.at(*lab)
            cv.text(x, y, name, size=LABEL, weight="bold", color=col["ink"], z=12)
    page = [deck.at(*p) for p in pts]
    for i, j in mesh(pts, 9.5):
        a, b = page[i], page[j]
        if (a, b) in segs or any(cuts(a, b, c, d) for c, d in segs):
            continue
        if any(x0 < a[0] + (b[0] - a[0]) * t < x1 and y0 < a[1] + (b[1] - a[1]) * t < y1
               for x0, y0, x1, y1 in boxes for t in np.linspace(0, 1, 9)):
            continue
        same = owner[i] == owner[j] and owner[i] is not None and REGIONS[owner[i]][0]
        col = mix(ROLE[REGIONS[owner[i]][1]]["stroke"], "#FFFFFF", 0.12) if same else "#9AA5B4"
        cv.ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=HAIR, zorder=5, solid_capstyle="round")
    for n, ((x, y), k) in enumerate(zip(page, owner)):
        if n < 8:
            continue
        named = k is not None and REGIONS[k][0]
        port = n < len(fixed)                # a server's tools, or the tool the agent calls: ringed
        cv.ax.add_patch(Circle((x, y), 0.72 if port else 0.5, fc=ROLE[REGIONS[k][1]]["stroke"] if named else GREY2,
                               ec="white" if port else "none", lw=0.5, zorder=6.5 if port else 6))

    # the walk: the one saturated path
    R = 2.0
    for (xa, ya), (xb, yb) in segs:
        L = math.hypot(xb - xa, yb - ya)
        ux, uy = (xb - xa) / L, (yb - ya) / L
        cv.arrow([(xa + ux * (R + 0.2), ya + uy * (R + 0.2)), (xb - ux * (R + 0.3), yb - uy * (R + 0.3))],
                 color=BLUE["mark"], lw=SPINE, head=2.5, halo=True, z=9)
    for k, ((x, y), (_, env)) in enumerate(zip(stops, WALK)):
        cv.badge(x, y, k + 1, ENV[env], d=2 * R, size=FINE, rim=0.6)
    for x, y, s in tags:
        cv.text(x, y, s, size=FINE, weight="bold", color=INK, z=13, path_effects=halo())

    # the agent: a call goes to the tool, an observation comes back
    cv.tile(ax_, ay, 7.6, glyph=lambda x, y, s: cv.icon_robot(x, y, s, color=GREY, lw=0.8), r="neutral", lw=LW)
    cv.text(ax_, ay + 5.6, "Agent", size=LABEL, weight="bold")
    cv.arrow([(ax_ + 4.4, ay + 1.1), (called[0] - 1.0, ay + 0.45)], color=BLUE["mark"], lw=LW, head=1.5, z=9)
    cv.arrow([(called[0] - 1.0, ay - 0.45), (ax_ + 4.4, ay - 1.1)], color=GREY2, lw=LW, head=1.5, z=9)
    cv.text(ax_ + 5.2, ay + 2.7, "tool calls", size=FINE, style="italic", color=BLUE["ink"], ha="left")
    cv.text(ax_ + 5.2, ay - 2.8, "observations", size=FINE, style="italic", color=GREY, ha="left")

    # what the space holds (under the plate's left corner) and what the blue line is (under its right corner)
    for k, (n, noun) in enumerate(((N_TOOLS, "tools"), (N_NODES, "graph nodes"), (N_ENVS, "environments"))):
        y = 85.4 - 3.8 * k
        end = cv.rich(3.0, y, [(f"{n:,}", BLUE["ink"], "bold")], size=HEAD)
        cv.text(end + 1.0, y - 0.1, noun, size=FINE, ha="left")
    bx = 154.5
    cv.arrow([(bx, 85.4), (bx + 5.2, 85.4)], color=BLUE["mark"], lw=SPINE, head=2.5)
    cv.text(bx + 6.4, 85.4, "one state-aware", size=FINE, ha="left")
    cv.text(bx, 82.7, "random walk: 8 calls", size=FINE, ha="left")
    cv.text(bx, 80.0, "across 4 environments", size=FINE, ha="left")
    return stops


# ---------------------------------------------------------------- the walk laid flat, the task, the fork ---
def rail(cv, stops, drops):
    """The same eight stops on a straight rail, each under its API name; the whole rail funnels into the task
    card; the card's two arrows turn down into the two results at x = drops."""
    y, top, ch = 60.4, 62.9, 4.2
    tw = [cv.text_width(n, FINE, **MONO) + 2.2 for n, _ in WALK]
    gap = [1.0 if WALK[k][1] == WALK[k + 1][1] else 2.4 for k in range(7)]
    x = (W - sum(tw) - sum(gap)) / 2
    assert x > 2.0, x
    xs = []
    for k, ((name, env), w) in enumerate(zip(WALK, tw)):
        c = ROLE[ENV[env]]
        cv.chips.append((x, top, w, ch, name, (1.0, top - 0.1, W - 1.0, top + ch + 0.1)))
        cv.ax.add_patch(FancyBboxPatch((x, top), w, ch, boxstyle="round,pad=0,rounding_size=1.0", fc=c["soft"],
                                       ec=c["stroke"], lw=LW, zorder=8))
        cv.text(x + w / 2, top + ch / 2 - 0.05, name, size=FINE, color=c["ink"], z=9, **MONO)
        xs.append(x + w / 2)
        x += w + (gap[k] if k < 7 else 0)
    r0, r1 = xs[0] - 4.0, xs[-1] + 4.0
    # leaders: stop 1 and stop 8 on the plate are stop 1 and stop 8 on the rail
    for k in (0, 7):
        cv.ax.plot([stops[k][0], xs[k]], [stops[k][1] - 2.3, top + ch + 0.3], color=BLUE["stroke"], lw=LW,
                   ls=(0, (2.6, 1.8)), zorder=7.5)

    # the task: one card holding q, V and the three kinds of check a replay must pass (Section 4.2.2)
    cw, chh, yf = 52.0, 7.8, 52.3
    cx = (r0 + r1) / 2
    cl, cr, ct = cx - cw / 2, cx + cw / 2, yf + chh / 2
    cv.ax.add_patch(Polygon([(r0, y), (r1, y), (cr - 1.5, ct), (cl + 1.5, ct)], closed=True, fc=BLUE["soft"], ec="none",
                            alpha=0.75, zorder=3))                        # the whole chain becomes one task
    cv.line([(r0, y), (r1, y)], color=BLUE["mark"], lw=SPINE, z=7)
    for k, (xc, (_, env)) in enumerate(zip(xs, WALK)):
        cv.badge(xc, y, k + 1, ENV[env], d=3.6, size=FINE, rim=0.6)
    cv.box(cl, yf - chh / 2, cw, chh, "blue", fill="white", stroke=BLUE["mark"], lw=LW, radius=1.4, name="task")
    cv.doc(cl + 1.6, yf - 2.7, 4.4, 5.4, "blue", lines=3, lw=LW)
    tx = cl + 7.4
    end = cv.rich(tx, yf + 1.55, [("task $q$ + checks $V$", "black", "bold")], size=LABEL)
    cv.text(cr - 1.6, yf + 1.5, "kept if the replay passes", size=FINE, style="italic", color=GREY, ha="right")
    assert end + 1.0 < cr - 1.6 - cv.text_width("kept if the replay passes", FINE, style="italic")
    x = tx
    for s in ("final state", "snapshots", "outputs"):
        cv.icon_check(x + 1.0, yf - 1.75, 1.9, color=ROLE["memory"]["mark"], lw=0.9)
        cv.text(x + 2.6, yf - 1.8, s, size=FINE, ha="left")
        x += 2.6 + cv.text_width(s, FINE) + 2.6
    assert x - 2.6 < cr - 1.0, (x, cr)

    # the fork: one arrow into each result, named for what is done with the tasks
    (lx, rx), tip = drops, 47.2
    assert lx < cl - 12 and rx > cr + 12
    cv.arrow([(cl, yf), (lx, yf), (lx, tip)], color=BLUE["mark"], lw=SPINE, head=2.5, radius=1.6, z=7)
    cv.arrow([(cr, yf), (rx, yf), (rx, tip)], color=BLUE["mark"], lw=SPINE, head=2.5, radius=1.6, z=7)
    cv.text(lx - 2.4, yf, "Train on the tasks", size=HEAD, weight="bold", color="black", ha="right")
    cv.text(rx + 2.4, yf, "Extend two benchmarks", size=HEAD, weight="bold", color="black", ha="left")
    assert rx + 2.4 + cv.text_width("Extend two benchmarks", HEAD, "bold") < W - 1.0
    for xa, xb, s in ((lx, cl, f"{N_SFT:,} samples"), (cr, rx, "longer walks")):
        cv.text((xa + xb) / 2, yf + 2.2, s, size=FINE, style="italic", color=BLUE["ink"])
        assert cv.text_width(s, FINE, style="italic") < xb - xa - 1.0, s


# ---------------------------------------------------------------- left result: generalisation ---
RADAR_AXES = [b.replace("Harvey LAB", "Harvey\nLAB").replace("OfficeQA Pro", "OfficeQA\nPro") for b in BENCH]
DARK = dict(ROLE["neutral"], mark="#2F3742", ink="#2F3742")       # the backbone
MID = dict(ROLE["neutral"], mark="#7D8794", ink="#3A4250")        # two other models of that scale
PALE = dict(ROLE["neutral"], mark="#9AA3AF", ink="#3A4250")
NOTE = "#3A4250"
VMAX = 80.0
assert max(max(v) for v, _ in T1.values()) < VMAX


def radars(cv, centres, cy, R, note_x, note_y):
    cv.text(note_x, note_y, f"every axis runs from 0 to {VMAX:.0f}, a ring every 20; higher is better", size=FINE,
            color=NOTE)
    for cx, models, gain in zip(centres, SCALES, GAIN):
        hero, base, o1, o2 = models
        n0 = len(cv.ax.patches)
        cv.radar(cx, cy, R, RADAR_AXES, [(m, T1[m][0], r) for m, r in zip(models, ("blue", DARK, MID, PALE))],
                 size=FINE, scale="shared", vmax=VMAX, fill=0.2)
        for p in cv.ax.patches[n0:]:      # the fourth model is dashed, so the two greys differ in print
            if isinstance(p, Polygon) and p.get_linewidth() == 0.85 and \
                    np.allclose(p.get_edgecolor()[:3], np.array([0x9A, 0xA3, 0xAF]) / 255, atol=0.01):
                p.set_linestyle((0, (2.2, 1.4)))
        for i in range(7):                # name the rival on an axis ToolSpace does not win
            best = max(models, key=lambda m: T1[m][0][i])
            if best != hero:
                a = math.radians(90.0 - 360.0 * i / 7)
                assert math.cos(a) > 0.25 and math.sin(a) < -0.25      # value set left-aligned, hanging
                px, py = cx + (R + 1.3) * math.cos(a), cy + (R + 1.3) * math.sin(a)
                w = cv.text_width(f"{T1[hero][0][i]:.1f}", FINE, "bold") + cv.text_width(f"00{T1[best][0][i]:.1f}", FINE)
                cv.text(px + w + 0.3, py, best, size=FINE, color=MID["ink"], ha="left", va="top")
        x0, xv = cx - 19.5, cx + 17.5
        ys = [cy - (R + 1.3) * 0.901 - 7.6 - 2.7 * k for k in range(3)]

        def key(x, y, m, r, bold=False, tail="", dash=False):
            c = r if isinstance(r, dict) else ROLE[r]
            cv.ax.plot([x, x + 3.0], [y, y], color=c["mark"], lw=1.25 if bold else 0.85, zorder=6,
                       solid_capstyle="butt", ls=(0, (2.2, 1.4)) if dash else "-")
            cv.text(x + 3.9, y, m + tail, size=FINE, ha="left", weight="bold" if bold else "normal",
                    color=BLUE["ink"] if bold else INK)
            return x + 3.9 + cv.text_width(m + tail, FINE, "bold" if bold else "normal")

        e1 = key(x0, ys[0], hero, "blue", bold=True)
        cv.text(xv, ys[0], f"avg. {T1[hero][1]:.1f}", size=FINE, weight="bold", color=BLUE["ink"], ha="right")
        e2 = key(x0, ys[1], base, DARK, tail=", backbone")
        cv.text(xv, ys[1], f"{T1[base][1]:.1f}", size=FINE, ha="right")
        assert e1 < xv - 9.5 and e2 < xv - 5.0, (hero, e1, e2, xv)
        e3 = key(x0, ys[2], o1, MID)
        assert key(e3 + 2.4, ys[2], o2, PALE, dash=True) < cx + 25.5
        # the gain is the bracket between the two averages
        bx = xv + 1.0
        cv.ax.plot([bx, bx + 0.9, bx + 0.9, bx], [ys[0], ys[0], ys[1], ys[1]], color=BLUE["mark"], lw=LW, zorder=6)
        cv.text(bx + 1.6, (ys[0] + ys[1]) / 2, f"+{gain:.1f}", size=HEAD, weight="bold", color=BLUE["ink"], ha="left")
        assert bx + 1.6 + cv.text_width(f"+{gain:.1f}", HEAD, "bold") < cx + 27.5


# ---------------------------------------------------------------- right result: the fall ---
FALLS = sorted(T2, key=lambda r: r[1][2])       # largest fall on AutomationBench first
assert FALLS[0][0] == "DeepSeek-V4.1-Flash-1017" and FALLS[-1][0] == "GLM 5.2"


def falls(cv, x0, y0, mm, pitch, note_x, note_y):
    """One group per model: a wedge from its Standard score down to its Pro score on each benchmark, the
    vendor's mark at the Pro score, the change under the mark. y0 is score 0, mm the millimetres per point."""
    xe = x0 + 1.0 + pitch * len(FALLS)
    for t in (0, 20, 40, 60):
        cv.ax.plot([x0, xe], [y0 + t * mm] * 2, color="#9AA0A8" if t == 0 else "#E3E6EA", lw=HAIR if t else LW,
                   zorder=2)
        cv.text(x0 - 0.9, y0 + t * mm, str(t), size=FINE, color=NOTE, ha="right")
    cv.text(x0 - 4.6, y0 + 32 * mm, "score: Standard (top) to Pro (mark)", size=FINE, color=NOTE, rotation=90)
    sep, wt, wb, ts = 5.3, 2.5, 1.0, 3.5

    def wedge(x, ya, yb, solid, z=5):
        cv.ax.add_patch(Polygon([(x - wt / 2, ya), (x + wt / 2, ya), (x + wb / 2, yb), (x - wb / 2, yb)], closed=True,
                                fc=BLUE["mark"] if solid else BLUE["soft"], ec=BLUE["mark"], lw=LW, zorder=z,
                                joinstyle="miter"))

    worst = min(r[1][2] for r in FALLS)
    for g, (model, a, b, mark, lines) in enumerate(FALLS):
        gx = x0 + 1.0 + pitch * (g + 0.5)
        for x, (std, pro, d), solid in ((gx - sep / 2, a, True), (gx + sep / 2, b, False)):
            wedge(x, y0 + std * mm, y0 + pro * mm, solid)
            logo_tile(cv, mark, x, y0 + pro * mm, ts, r="neutral", shadow=False, lw=LW, pad=0.14, z=9)
            cv.text(x, y0 + pro * mm - ts / 2 - 1.45, f"−{-d:.1f}", size=FINE, weight="bold" if d == worst else "normal",
                    color=BLUE["ink"])
        for k, s in enumerate(lines):
            cv.text(gx, y0 - 1.9 - 2.5 * k, s, size=FINE)
            assert cv.text_width(s, FINE) < pitch - 0.6, s

    # key: a sample of each mark with its meaning, centred under the fork's arrow
    items = ((f"AutomationBench Pro, {N_PRO[0]} tasks", True), (f"τ³-Bench Banking Pro, {N_PRO[1]} tasks", False))
    wkey = sum(3.0 + cv.text_width(n, FINE) + 2.6 for n, _ in items) - 2.6
    x, y = note_x - wkey / 2, note_y
    assert x > x0 - 6.5 and x + wkey < W - 0.8, (x, x + wkey)
    for name, solid in items:
        wedge(x + 1.25, y + 1.2, y - 1.2, solid)
        cv.text(x + 3.0, y, name, size=FINE, ha="left")
        x += 3.0 + cv.text_width(name, FINE) + 2.6


def build():
    cv = Canvas(W, H)
    stops = scene(cv)
    LX, RX, FX, PITCH = 21.5, 70.0, 101.0, 10.8           # radar centres; left edge and group pitch of the falls
    drops = ((LX + RX) / 2, FX + 1.0 + PITCH * 3.5)       # each arrow lands on the middle of its result
    rail(cv, stops, drops)
    radars(cv, (LX, RX), 26.0, 11.0, drops[0], 45.3)
    falls(cv, FX, 10.6, 0.54, PITCH, drops[1], 45.3)
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
