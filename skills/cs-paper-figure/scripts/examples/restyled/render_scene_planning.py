"""Restyle of the scene-planning example (deterministic illustrative simulation).

Every coordinate, action, collision interval, effort, cost and the executed step is
read from computed_rollouts.json and re-derived from scene_fixture.json with the
example's own scene_model.py (asserted equal). All five scene tiles share one
camera: world (0..10, 0..6) at 3.8 mm/unit.

    python render_scene_planning.py --out <dir>
"""
import argparse
import importlib.util
import json
import os
import sys

import matplotlib
from matplotlib import patheffects as pe
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, ROLE, INK, MUTED, LINE, HAIR  # noqa: E402

EX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "scene-planning")
SEL, COL, EXE, GOAL, NEU = ROLE["teal"], ROLE["coral"], ROLE["blue"], ROLE["amber"], ROLE["neutral"]
REJ = {"D": "#5E6875", "U": "#8E99A8"}          # rejected candidates: two greys
OBS_FILL, OBS_EDGE = "#D3D7DD", "#7A8390"
FLOOR, GRID = "#F6F7F8", "#E3E6EA"
W, H = 178, 98
SC = 3.8                                          # mm per scene unit, every tile


def num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return ("−" + s[1:]) if s.startswith("-") else ("0" if s == "-0" else s)


def pt(p):
    return f"({num(p[0])}, {num(p[1])})"


# ------------------------------------------------------------------ scene ---
class Tile:
    """One registered scene view: world -> mm with a fixed scale."""

    def __init__(self, cv, x0, y0, scene, sc=SC, wx=(0, 10), wy=(0, 6)):
        self.cv, self.x0, self.y0, self.sc, self.wx, self.wy = cv, x0, y0, sc, wx, wy
        self.scene = scene

    def m(self, p):
        return (self.x0 + (p[0] - self.wx[0]) * self.sc, self.y0 + (p[1] - self.wy[0]) * self.sc)

    def draw(self, grid=True, labels=True):
        ax, (x1, y1) = self.cv.ax, self.m((self.wx[1], self.wy[1]))
        w, h = x1 - self.x0, y1 - self.y0
        ax.add_patch(Rectangle((self.x0, self.y0), w, h, fc=FLOOR, ec="none", zorder=3))
        if grid:
            for gx in range(int(self.wx[0]) + 1, int(self.wx[1])):
                ax.plot([self.m((gx, 0))[0]] * 2, [self.y0, y1], color=GRID, lw=0.3, zorder=3.1)
            for gy in range(int(self.wy[0]) + 1, int(self.wy[1])):
                ax.plot([self.x0, x1], [self.m((0, gy))[1]] * 2, color=GRID, lw=0.3, zorder=3.1)
        ax.add_patch(Rectangle((self.x0, self.y0), w, h, fc="none", ec=NEU["stroke"], lw=0.6, zorder=9))
        for o in self.scene["obstacles"]:
            self.obstacle(o, labels)

    def obstacle(self, o, label=True):
        ax = self.cv.ax
        if o["type"] == "aabb":
            x0, x1, y0, y1 = o["bounds"]
            (a, b), (c, d) = self.m((x0, y0)), self.m((x1, y1))
            ax.add_patch(Rectangle((a, b), c - a, d - b, fc=OBS_FILL, ec=OBS_EDGE, lw=0.55, hatch="////",
                                   zorder=4))
            cx, cy = (a + c) / 2, d - 1.6           # label near the top, clear of mid-height paths
        else:
            cx, cy = self.m(o["center"])
            ax.add_patch(Circle((cx, cy), o["radius"] * self.sc, fc=OBS_FILL, ec=OBS_EDGE, lw=0.55, zorder=4))
        if label:
            self.cv.text(cx, cy, o["id"], size=6.4, weight="bold", color=NEU["ink"], z=6,
                         path_effects=[pe.withStroke(linewidth=1.6, foreground=OBS_FILL)])

    def agent(self, p, hollow=False, color=INK, d=1.5):
        x, y = self.m(p)
        self.cv.ax.add_patch(Circle((x, y), d / 2, fc="white" if hollow else color, ec=color,
                                    lw=0.6, zorder=12))
        if not hollow:
            self.cv.ax.add_patch(Circle((x, y), d * 0.18, fc="white", ec="none", zorder=12.1))

    def goal(self, p):
        x, y = self.m(p)
        ax = self.cv.ax
        ax.plot([x, x], [y, y + 3.0], color=GOAL["ink"], lw=0.6, zorder=11, solid_capstyle="round")
        ax.add_patch(Polygon([(x, y + 3.0), (x + 2.0, y + 2.45), (x, y + 1.9)], fc=GOAL["mark"],
                             ec=GOAL["ink"], lw=0.4, zorder=11))
        ax.add_patch(Circle((x, y), 0.45, fc=GOAL["ink"], ec="none", zorder=11))

    def path(self, pts, color, lw=0.9, dashed=True, z=10, alpha=1.0):
        self.cv.line([self.m(p) for p in pts], color=color, lw=lw, dashed=dashed, z=z, radius=0, alpha=alpha)

    def states(self, pts, color, offsets):
        for k, (p, off) in enumerate(zip(pts, offsets)):
            if off is None:
                continue
            x, y = self.m(p)
            self.cv.ax.add_patch(Circle((x, y), 0.55, fc="white", ec=color, lw=0.6, zorder=11))
            self.cv.text(x + off[0], y + off[1], str(k), size=6.0, color=color, z=12)


def card(cv, x, y, w, h, r, title, size=7.6, lw=0.7, fill="white"):
    cv.group(x, y, w, h, r, title, band=True, size=size, radius=2.0, lw=lw, fill=fill)


def shadow(cv, x, y, w, h, radius=1.6):
    cv.ax.add_patch(FancyBboxPatch((x + 0.4, y - 0.4), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                                   lw=0, fc="#1A2230", alpha=0.10, zorder=0.9))


# ------------------------------------------------------------------ data ---
def load(fixture_path, rollouts_path):
    spec = importlib.util.spec_from_file_location("scene_model", os.path.join(EX, "scene_model.py"))
    sm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sm)
    fx = json.load(open(fixture_path))
    ro = json.load(open(rollouts_path))
    fresh = sm.rollout(fx)
    for a, b in zip(ro["candidates"], fresh["candidates"]):      # stored == recomputed
        assert a["id"] == b["id"] and a["states"] == b["states"] and a["collision"] == b["collision"]
        assert abs(a["cost"] - b["cost"]) < 1e-9 and abs(a["effort"] - b["effort"]) < 1e-9
    c = {r["id"]: r for r in ro["candidates"]}
    assert ro["selected_id"] == fresh["selected_id"] == "L"
    assert min(c.values(), key=lambda r: r["cost"])["id"] == "L"
    assert [c[k]["collision"] for k in "DUL"] == [1, 0, 0]
    assert all(abs(c[k]["terminal_squared_distance"]) < 1e-12 for k in "DUL")
    assert [round(c[k]["effort"], 2) for k in "DUL"] == [16.0, 26.36, 21.42]
    assert [round(c[k]["cost"], 3) for k in "DUL"] == [101.6, 2.636, 2.142]
    hit = c["D"]["segments"][1]["obstacles"][0]
    assert c["D"]["segments"][1]["collision"] and hit["obstacle_id"] == "A"
    assert [round(t, 2) for t in hit["interval"]] == [0.2, 0.8]
    assert c["D"]["segments"][1]["from"] == [3.0, 3.0] and c["D"]["segments"][1]["to"] == [5.0, 3.0]
    assert sum(s["collision"] for r in c.values() for s in r["segments"]) == 1
    assert ro["executed_action"] == [1.5, -1.8] and ro["executed_action_count"] == 1
    assert ro["next_state"]["agent"]["position"] == c["L"]["states"][1] == [2.5, 1.2]
    assert not c["L"]["segments"][0]["collision"]
    return fx, ro, c


# ---------------------------------------------------------------- panels ---
def panel_a(cv, fx, scene):
    card(cv, 1.5, 42.5, 42.5, 54, "neutral", "(a) Scene state and task")
    cv.text(3.4, 89.4, r"planner reads exact state $s_0$", size=6.0, color=MUTED, style="italic", ha="left")
    cv.group(2.7, 44, 40.1, 43.4, NEU, r"Observation $o_0=R(s_0)$", band=True, size=6.9, radius=1.6, lw=0.55,
             fill="white")
    t = Tile(cv, 3.75, 59.4, scene)
    t.draw()
    p0, g = scene["agent"]["position"], scene["goal"]
    t.agent(p0)
    t.goal(g)
    x, y = t.m(p0)
    cv.text(x, y + 1.9, r"$p_0$", size=6.6)
    x, y = t.m(g)
    cv.text(x - 1.4, y - 1.6, r"$g$", size=6.6, color=GOAL["ink"])
    A, B = scene["obstacles"]
    rows = [(r"$p_0=$" + pt(p0) + r"$\quad g=$" + pt(g), INK),
            (r"A: $[" + num(A["bounds"][0]) + "," + num(A["bounds"][1]) + r"]\times[" + num(A["bounds"][2])
             + "," + num(A["bounds"][3]) + "]$", INK),
            (r"B: $c=$" + pt(B["center"]) + r", $r=$" + num(B["radius"]), INK)]
    for i, (s, col) in enumerate(rows):
        cv.text(4.2, 56.8 - i * 3.3, s, size=6.3, color=col, ha="left")
    cv.text(4.2, 46.1, "Reach $g$; avoid A and B", size=6.3, color=MUTED, style="italic", ha="left")


def candidate(cv, x, y, w, h, r, fx):
    cid, sel = r["id"], r["id"] == "L"
    role = SEL if sel else NEU
    if sel:
        shadow(cv, x, y, w, h)
    cv.group(x, y, w, h, role, f"{cid}   {r['name']}", band=True, size=6.9, radius=1.6,
             lw=1.0 if sel else 0.55, fill="white", stroke=SEL["mark"] if sel else None)
    if sel:
        cv.chip(x + w - 7.5, y + h - 2.15, "selected", SEL, size=6.0, solid=True, h=3.0, pad=0.8, z=12)
    elif r["collision"]:
        cv.chip(x + w - 7.5, y + h - 2.15, "collision", COL, size=6.0, h=3.0, pad=0.8, z=12)
    t = Tile(cv, x + (w - 38) / 2, 59.4, fx["scene"])
    t.draw()
    color = SEL["mark"] if sel else REJ[cid]
    st = r["states"]
    t.path(st, color, lw=1.3 if sel else 0.9)
    if cid == "D":
        seg = r["segments"][1]
        t0, t1 = seg["obstacles"][0]["interval"]
        p, q = seg["from"], seg["to"]
        a = [p[i] + t0 * (q[i] - p[i]) for i in (0, 1)]
        b = [p[i] + t1 * (q[i] - p[i]) for i in (0, 1)]
        t.path([a, b], COL["mark"], lw=1.6, dashed=False, z=10.5)
        (zx0, zy0), (zx1, zy1) = t.m((2.7, 2.55)), t.m((5.3, 3.45))
        cv.ax.add_patch(Rectangle((zx0, zy0), zx1 - zx0, zy1 - zy0, fc="none", ec=COL["stroke"], lw=0.5,
                                  ls=(0, (2, 1.2)), zorder=10.6))
        cv.text(zx1 + 0.4, zy1 + 0.9, "(c)", size=6.0, color=COL["ink"], ha="left", z=12,
                path_effects=[pe.withStroke(linewidth=1.4, foreground=FLOOR)])
        offs = [None, (0, -2.9), (0, -2.9), (0, -1.6), None]
    elif cid == "U":
        offs = [None, (0, 1.5), (0, 1.5), (1.5, 0.5), None]
        clr = min(o["clearance"] for sg in r["segments"] for o in sg["obstacles"] if o["obstacle_id"] == "B")
        assert round(clr, 2) == 0.13 and not r["collision"]
        bx, by = t.m((9.8, 0.35))
        cv.text(bx, by, f"clears B by {clr:.2f}", size=6.0, color=MUTED, style="italic", ha="right", va="bottom",
                z=12)
    else:
        offs = [None, (0, -1.6), (0, -1.6), (1.0, -1.4), None]
    t.states(st, color, offs)
    t.agent(st[0])
    t.goal(fx["scene"]["goal"])
    # action rows a_k, aligned columns
    cols = [x + 12.5 + 8.0 * k for k in range(4)]
    cv.text(x + 2.4, 56.6, "$k$", size=6.2, color=MUTED, ha="left")
    for k, cx in enumerate(cols):
        cv.text(cx, 56.6, str(k), size=6.2, color=MUTED)
    for j, (lab, yy) in enumerate(((r"$a_x$", 53.8), (r"$a_y$", 51))):
        cv.text(x + 2.4, yy, lab, size=6.4, color=INK, ha="left")
        for k, cx in enumerate(cols):
            first = sel and k == 0
            cv.text(cx, yy, num(r["actions"][k][j]), size=6.4, z=21,
                    color=EXE["ink"] if first else INK, weight="bold" if first else "normal")
    if sel:  # a_0 is the executed action
        cv.ax.add_patch(FancyBboxPatch((cols[0] - 3.4, 49.4), 6.8, 6.0, boxstyle="round,pad=0,rounding_size=0.8",
                                       fc=EXE["fill"], ec=EXE["stroke"], lw=0.5, zorder=8))
    cv.ax.plot([x + 1.5, x + w - 1.5], [48.6] * 2, color=HAIR, lw=0.4, zorder=8)
    cv.rich(x + w / 2, 46.3, [(f"$E={r['effort']:.2f}$", INK), (r"$\quad$", INK),
                              (f"$C={r['collision']}$", COL["ink"] if r["collision"] else INK)], size=6.4, ha="center")


def panel_b(cv, fx, c):
    card(cv, 46, 42.5, 130.5, 54, "neutral", "(b) Candidate rollouts in one scene")
    d = fx["dynamics"]
    cv.text(48.0, 89.4, r"$p_{k+1}=p_k+a_k\Delta t,\ \ \Delta t=%s,\ \ \|a_k\|_2\leq %s,\ \ H=%d$;  dashed = simulated"
            % (num(d["dt"]), num(d["max_action_norm"]), d["horizon"]), size=6.0, color=MUTED, style="italic",
            ha="left")
    w = (130.5 - 2.4 - 4) / 3
    for i, k in enumerate("DUL"):
        candidate(cv, 47.2 + i * (w + 2), 44, w, 43.4, c[k], fx)


def panel_c(cv, c):
    card(cv, 1.5, 1.5, 56, 39, "coral", "(c) Swept collision test")
    seg = c["D"]["segments"][1]
    p, q = seg["from"], seg["to"]
    t0, t1 = seg["obstacles"][0]["interval"]
    cv.text(3.4, 33.6, r"D, segment $k=1$: " + pt(p) + r" $\rightarrow$ " + pt(q), size=6.0, color=MUTED,
            style="italic", ha="left")
    sc, wx, wy = 19.0, (2.7, 5.3), (2.55, 3.45)
    t = Tile(cv, 4.8, 14, {"obstacles": []}, sc=sc, wx=wx, wy=wy)
    ax = cv.ax
    x1, y1 = t.m((wx[1], wy[1]))
    ax.add_patch(Rectangle((t.x0, t.y0), x1 - t.x0, y1 - t.y0, fc=FLOOR, ec=NEU["stroke"], lw=0.5, zorder=3))
    (a0, _), (a1, _) = t.m((3.4, 0)), t.m((4.6, 0))
    ax.add_patch(Rectangle((a0, t.y0), a1 - a0, y1 - t.y0, fc=OBS_FILL, ec=OBS_EDGE, lw=0.55, hatch="////",
                           zorder=4))
    cv.text((a0 + a1) / 2, y1 - 2.4, "A", size=6.6, weight="bold", color=NEU["ink"], z=6,
            path_effects=[pe.withStroke(linewidth=1.6, foreground=OBS_FILL)])
    P, Q = t.m(p), t.m(q)
    ca = [p[i] + t0 * (q[i] - p[i]) for i in (0, 1)]
    cb = [p[i] + t1 * (q[i] - p[i]) for i in (0, 1)]
    cv.line([P, Q], color=REJ["D"], lw=0.9, dashed=True, z=8, radius=0)
    cv.line([t.m(ca), t.m(cb)], color=COL["mark"], lw=2.2, dashed=False, z=9, radius=0)
    for pp, lab, k in ((P, r"$p_1$", 1), (Q, r"$p_2$", 2)):
        ax.add_patch(Circle(pp, 0.75, fc="white", ec=REJ["D"], lw=0.7, zorder=10))
        cv.text(pp[0], pp[1] + 2.4, lab, size=6.6, color=INK)
        cv.text(pp[0], pp[1] - 2.4, "free", size=6.0, color=MUTED, style="italic")
    # segment parameter axis t in [0, 1]
    ya = 9.5
    cv.line([(P[0], ya), (Q[0], ya)], color=LINE, lw=0.5, z=8, radius=0)
    for tv in (0.0, t0, t1, 1.0):
        xx = P[0] + tv * (Q[0] - P[0])
        hot = tv in (t0, t1)
        ax.plot([xx, xx], [ya - 0.6, ya + 0.6], color=COL["mark"] if hot else LINE, lw=0.6, zorder=8)
        cv.text(xx, ya - 2.1, f"{tv:.2f}", size=6.0, color=COL["ink"] if hot else MUTED)
        if hot:
            cv.line([(xx, ya + 0.6), (xx, t.y0)], color=COL["stroke"], lw=0.4, dashed=True, z=7, radius=0)
    ax.add_patch(Rectangle((P[0] + t0 * (Q[0] - P[0]), ya - 0.35), (t1 - t0) * (Q[0] - P[0]), 0.7,
                           fc=COL["mark"], ec="none", zorder=8.5))
    cv.text(P[0] - 2.8, ya, "$t$", size=6.6, color=INK, ha="right")
    cv.text((a0 + a1) / 2, 3.3, r"inside A for $t\in[%.2f,\,%.2f]\ \Rightarrow\ C=1$" % (t0, t1), size=6.4,
            color=COL["ink"])


def panel_d(cv, fx, c):
    card(cv, 59.5, 1.5, 58, 39, "neutral", "(d) Cost per candidate")
    ob = fx["objective"]
    cv.rich(61.4, 33.6, [(r"$J=\|p_4-g\|_2^2$", MUTED), (r"$\,+\,%s\,E$" % num(ob["effort_weight"]), MUTED),
                         (r"$\,+\,%d\,C$" % ob["collision_penalty"], COL["ink"])], size=6.4, ha="left")
    cv.text(61.4, 29.8, r"$\|p_4-g\|_2^2=0$ for all three", size=6.0, color=MUTED, style="italic", ha="left")
    x0, s, bh = 66.5, 10.0, 3.6                     # bar origin, mm per cost unit (linear from 0)
    ys = {"D": 24.4, "U": 18.4, "L": 12.4}
    ax = cv.ax
    for k in "DUL":
        r, y = c[k], ys[k]
        sel = k == "L"
        eff = ob["effort_weight"] * r["effort"]
        col = SEL["mark"] if sel else REJ[k]
        cv.text(x0 - 1.6, y, k, size=7.0, weight="bold", color=SEL["ink"] if sel else INK, ha="right")
        ax.add_patch(Rectangle((x0, y - bh / 2), eff * s, bh, fc=col, ec="none", zorder=6))
        if r["collision"]:                          # penalty segment, axis broken at 3.0 -> 101.6
            xb0, xb1 = x0 + eff * s, x0 + 3.55 * s
            ax.add_patch(Rectangle((xb0, y - bh / 2), xb1 - xb0, bh, fc=COL["soft"], ec=COL["mark"],
                                   lw=0.6, zorder=6))
            bx = x0 + 3.05 * s
            ax.add_patch(Rectangle((bx - 0.5, y - bh / 2 - 0.6), 1.0, bh + 1.2, fc="white", ec="none", zorder=7))
            for dx in (-0.5, 0.5):
                ax.plot([bx + dx - 0.45, bx + dx + 0.45], [y - bh / 2 - 0.6, y + bh / 2 + 0.6],
                        color=LINE, lw=0.5, zorder=7.1)
            cv.text((xb0 + bx - 0.5) / 2, y, r"$+100C$", size=6.0, color=COL["ink"], z=8)
            end = xb1
        else:
            end = x0 + eff * s
        cv.text(end + 1.2, y, f"{r['cost']:.3f}", size=6.8 if sel else 6.4, ha="left",
                color=SEL["ink"] if sel else INK, weight="bold" if sel else "normal")
        if sel:
            cv.chip(end + 13.2, y, "argmin", SEL, size=6.0, solid=True, h=3.0, pad=0.8)
    # linear axis 0..3 (D continues past the break)
    ya = 7.9
    ax.plot([x0, x0 + 3.0 * s], [ya, ya], color="#9AA0A8", lw=0.5, zorder=5)
    for v in range(4):
        ax.plot([x0 + v * s] * 2, [ya, ya - 0.8], color="#9AA0A8", lw=0.5, zorder=5)
        cv.text(x0 + v * s, ya - 2.1, str(v), size=6.0, color=MUTED)
    ax.plot([x0, x0], [ya, 27], color="#9AA0A8", lw=0.5, zorder=5)
    cv.text(x0 + 3.0 * s + 1.5, ya - 2.1, "$J$", size=6.4, color=MUTED, ha="left")


def panel_e(cv, fx, ro, c):
    card(cv, 119.5, 1.5, 57, 39, "blue", "(e) Executed first step")
    L = c["L"]
    a0, p0, p1 = ro["executed_action"], L["states"][0], L["states"][1]
    cv.text(121.4, 33.6, "only $a_0$ of L is applied", size=6.0, color=MUTED, style="italic", ha="left")
    t = Tile(cv, 121.0, 7.8, ro["next_state"])
    t.draw()
    t.path(L["states"][1:], SEL["mark"], lw=0.8, alpha=0.45)
    t.goal(fx["scene"]["goal"])
    t.agent(p0, hollow=True, color=INK)
    cv.arrow([t.m(p0), t.m(p1)], color=EXE["mark"], lw=1.3, head=1.6, z=11)
    t.agent(p1, color=EXE["ink"])
    x, y = t.m(p0)
    cv.text(x, y + 1.9, r"$p_0$", size=6.6)
    x, y = t.m(p1)
    cv.text(x + 1.2, y - 1.6, r"$p_1$", size=6.6, color=EXE["ink"], ha="left", weight="bold")
    x2, y2 = t.m((6.2, 0.25))
    cv.text(x2, y2, r"$a_{1:3}$ not run", size=6.0, color=SEL["ink"], style="italic", va="bottom", z=12)
    xr = 160.6
    cv.text(xr, 27.2, r"$a_0=$" + pt(a0), size=6.4, color=EXE["ink"], ha="left", weight="bold")
    cv.text(xr, 23.6, r"$p_1=$" + pt(p1), size=6.4, color=INK, ha="left")
    cv.text(xr, 20.0, "swept: free", size=6.0, color=MUTED, style="italic", ha="left")
    cv.arrow([(xr + 0.5, 15.6), (xr + 0.5, 11.2)], color=LINE, lw=0.6, head=1.1)
    cv.text(xr + 2.0, 13.4, r"$o_1=R(s_1)$", size=6.4, color=INK, ha="left")
    cv.chip(xr + 7.0, 8.8, "replan", EXE, size=6.0, h=3.0, pad=0.8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default=os.path.join(EX, "scene_fixture.json"))
    ap.add_argument("--rollouts", default=os.path.join(EX, "computed_rollouts.json"))
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    fx, ro, c = load(a.fixture, a.rollouts)
    matplotlib.rcParams["hatch.linewidth"] = 0.35
    cv = Canvas(W, H, family="serif", size=7.0)
    panel_a(cv, fx, fx["scene"])
    panel_b(cv, fx, c)
    panel_c(cv, c)
    panel_d(cv, fx, c)
    panel_e(cv, fx, ro, c)
    small = [t for t in cv.ax.texts if t.get_fontsize() < 6.0]
    assert not small, [t.get_text() for t in small]
    print("\n".join(cv.save(os.path.join(a.out, "scene_planning_figure"))))


if __name__ == "__main__":
    main()
