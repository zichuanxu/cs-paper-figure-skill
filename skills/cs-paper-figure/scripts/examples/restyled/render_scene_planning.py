"""Restyle of the scene-planning example (deterministic illustrative simulation).

Every coordinate, action, collision interval, effort, cost and the executed step is
read from computed_rollouts.json and re-derived from scene_fixture.json with the
example's own scene_model.py (asserted equal). Scene tiles keep one aspect (world
0..10 x 0..6); the rollout overview is drawn largest.

Layout: planner pipeline across the top (observe -> simulate -> score -> execute) with a
phase bar, a detail row (per-candidate action sequences; swept collision test) and a key strip.
Candidate hues: D purple, U amber, L teal (selected), carried into paths, cost bars and labels.

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
CAND = {"D": ROLE["purple"], "U": ROLE["amber"], "L": ROLE["teal"]}   # one hue per candidate
SEL, COL, EXE, NEU = ROLE["teal"], ROLE["coral"], ROLE["blue"], ROLE["neutral"]
GOALC = ("#3A4250", "#5E6875")                    # goal flag: neutral ink (amber is candidate U)
OBS_FILL, OBS_EDGE = "#D3D7DD", "#7A8390"
FLOOR, GRID = "#F6F7F8", "#E3E6EA"
W, H = 178, 101
TS = 7.6                                          # panel title size
TH = TS * 0.56                                    # pill tab height (paperkit.section)


def num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return ("−" + s[1:]) if s.startswith("-") else ("0" if s == "-0" else s)


def pt(p):
    return f"({num(p[0])}, {num(p[1])})"


# ------------------------------------------------------------------ scene ---
class Tile:
    """One scene view: world -> mm with a fixed scale."""

    def __init__(self, cv, x0, y0, scene, sc=3.8, wx=(0, 10), wy=(0, 6)):
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
            cx, cy = (a + c) / 2, d - 1.6
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
        ax.plot([x, x], [y, y + 3.0], color=GOALC[0], lw=0.6, zorder=11, solid_capstyle="round")
        ax.add_patch(Polygon([(x, y + 3.0), (x + 2.0, y + 2.45), (x, y + 1.9)], fc=GOALC[1],
                             ec=GOALC[0], lw=0.4, zorder=11))
        ax.add_patch(Circle((x, y), 0.45, fc=GOALC[0], ec="none", zorder=11))

    def path(self, pts, color, lw=0.9, dashed=True, z=10, alpha=1.0):
        self.cv.line([self.m(p) for p in pts], color=color, lw=lw, dashed=dashed, z=z, radius=0, alpha=alpha)

    def states(self, pts, color, offsets):
        for k, (p, off) in enumerate(zip(pts, offsets)):
            if off is None:
                continue
            x, y = self.m(p)
            self.cv.ax.add_patch(Circle((x, y), 0.55, fc="white", ec=color, lw=0.6, zorder=11))
            self.cv.text(x + off[0], y + off[1], str(k), size=6.0, color=color, z=12)


def panel(cv, x, y, w, h, r, title):
    """Section frame in the stage hue, title on a pill tab; returns the y just under the tab."""
    cv.section(x, y, w, h, r, title, tab="top", size=TS, radius=2.0)
    return y + h - TH / 2


def sub(cv, x, y, s, ha="left", **kw):
    cv.text(x, y, s, size=6.0, color=MUTED, style="italic", ha=ha, va="top", **kw)


def flow(cv, x0, x1, y):
    cv.arrow([(x0, y), (x1, y)], color=LINE, lw=0.8, head=1.4)


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
    for k in "DUL":                                   # key-strip definition E = sum_k ||a_k||^2
        assert abs(sum(ax * ax + ay * ay for ax, ay in c[k]["actions"]) - c[k]["effort"]) < 1e-9
    return fx, ro, c


# ------------------------------------------------------- overview (top row) ---
TOP_Y, TOP_H = 52.0, 46.0
XA, XB, XC, XD = (1.5, 30.0), (35.5, 54.0), (93.5, 47.0), (144.5, 32.0)   # (x, w) per stage


def panel_a(cv, scene):
    x, w = XA
    yt = panel(cv, x, TOP_Y, w, TOP_H, "neutral", "(a) Observe")
    sub(cv, x + w / 2, yt - 1.0, r"$o_0=R(s_0)$, exact state", ha="center")
    t = Tile(cv, x + (w - 26) / 2, 72.0, scene, sc=2.6)
    t.draw()
    p0, g = scene["agent"]["position"], scene["goal"]
    t.agent(p0, d=1.3)
    t.goal(g)
    px, py = t.m(p0)
    cv.text(px, py + 1.9, r"$p_0$", size=6.4)
    gx, gy = t.m(g)
    cv.text(gx - 1.3, gy - 1.5, r"$g$", size=6.4, color=GOALC[0])
    A, B = scene["obstacles"]
    rows = [r"$p_0=$" + pt(p0) + r"$\ \ g=$" + pt(g),
            r"A: $[" + num(A["bounds"][0]) + "," + num(A["bounds"][1]) + r"]\times[" + num(A["bounds"][2])
            + "," + num(A["bounds"][3]) + "]$",
            r"B: $c=$" + pt(B["center"]) + r", $r=$" + num(B["radius"])]
    for i, s in enumerate(rows):
        cv.text(x + 1.6, 68.4 - i * 3.3, s, size=6.1, ha="left")
    cv.text(x + w / 2, 56.0, "Reach $g$; avoid A and B", size=6.1, color=MUTED, style="italic")


def panel_b(cv, fx, c):
    x, w = XB
    yt = panel(cv, x, TOP_Y, w, TOP_H, "frozen", "(b) Simulate candidate rollouts")
    d = fx["dynamics"]
    sub(cv, x + w / 2, yt - 1.0, r"$p_{k+1}=p_k+a_k\Delta t,\ \Delta t=%s,\ \|a_k\|_2\leq %s,\ H=%d$"
        % (num(d["dt"]), num(d["max_action_norm"]), d["horizon"]), ha="center")
    t = Tile(cv, x + 2.0, 57.0, fx["scene"], sc=5.0)
    t.draw()
    offs = {"D": [None, (-1.2, 3.9), (1.2, 3.9), (0, 1.5), None],
            "U": [None, (0, 1.6), (0, 1.6), (1.8, 0.6), None],
            "L": [None, (0, -1.8), (0, -1.8), (1.3, -1.8), None]}
    for k in "DUL":
        r, hue = c[k], CAND[k]
        sel = k == "L"
        t.path(r["states"], hue["mark"], lw=1.4 if sel else 1.0, z=10.2 if sel else 10)
        t.states(r["states"], hue["mark"], offs[k])
    seg = c["D"]["segments"][1]
    t0, t1 = seg["obstacles"][0]["interval"]
    p, q = seg["from"], seg["to"]
    t.path([[p[i] + t0 * (q[i] - p[i]) for i in (0, 1)], [p[i] + t1 * (q[i] - p[i]) for i in (0, 1)]],
           COL["mark"], lw=1.8, dashed=False, z=10.5)
    (zx0, zy0), (zx1, zy1) = t.m((2.7, 2.55)), t.m((5.3, 3.45))
    cv.ax.add_patch(Rectangle((zx0, zy0), zx1 - zx0, zy1 - zy0, fc="none", ec=COL["stroke"], lw=0.5,
                              ls=(0, (2, 1.2)), zorder=10.6))
    cv.text(zx0 - 0.4, zy0 - 0.3, "(f)", size=6.0, color=COL["ink"], ha="right", va="top", z=12, weight="bold",
            path_effects=[pe.withStroke(linewidth=1.4, foreground=FLOOR)])
    # direct labels: candidate letter at its last segment, in its hue
    for k, wp, dxy in (("D", (8.0, 3.0), (0, 1.6)), ("U", (8.1, 4.3), (1.5, 0.9)), ("L", (8.1, 2.2), (1.4, -1.0))):
        lx, ly = t.m(wp)
        cv.text(lx + dxy[0], ly + dxy[1], k, size=7.2, weight="bold", color=CAND[k]["ink"], z=12,
                path_effects=[pe.withStroke(linewidth=1.6, foreground=FLOOR)])
    clr = min(o["clearance"] for sg in c["U"]["segments"] for o in sg["obstacles"] if o["obstacle_id"] == "B")
    assert round(clr, 2) == 0.13 and not c["U"]["collision"]
    bx, by = t.m((9.8, 0.25))
    cv.text(bx, by, f"U clears B by {clr:.2f}", size=6.0, color=CAND["U"]["ink"], style="italic", ha="right",
            va="bottom", z=12)
    t.agent(fx["scene"]["agent"]["position"])
    t.goal(fx["scene"]["goal"])


def panel_c(cv, fx, c):
    x, w = XC
    yt = panel(cv, x, TOP_Y, w, TOP_H, "rose", "(c) Score and select")
    ob = fx["objective"]
    cv.rich(x + w / 2, yt - 2.6, [(r"$J=\|p_4-g\|_2^2$", INK), (r"$\,+\,%s\,E$" % num(ob["effort_weight"]), INK),
                                  (r"$\,+\,%d\,C$" % ob["collision_penalty"], COL["ink"])], size=6.6, ha="center")
    sub(cv, x + w / 2, yt - 5.0, r"$\|p_4-g\|_2^2=0$ for all three", ha="center")
    x0, s, bh = x + 6.0, 8.0, 4.4                   # bar origin, mm per cost unit (linear from 0)
    ys = {"D": 79.5, "U": 72.5, "L": 65.5}
    ax = cv.ax
    ax.add_patch(FancyBboxPatch((x + 1.2, ys["L"] - 3.2), w - 2.4, 6.4, boxstyle="round,pad=0,rounding_size=1.0",
                                fc="white", ec=SEL["stroke"], lw=0.5, zorder=5))     # hero row
    for k in "DUL":
        r, y, hue = c[k], ys[k], CAND[k]
        sel = k == "L"
        eff = ob["effort_weight"] * r["effort"]
        cv.text(x0 - 1.6, y, k, size=7.4, weight="bold", color=hue["ink"], ha="right")
        ax.add_patch(Rectangle((x0, y - bh / 2), eff * s, bh, fc=hue["mark"], ec="none", zorder=6))
        if r["collision"]:                          # penalty segment, axis broken at 3.0 -> 101.6
            xb0, xb1 = x0 + eff * s, x0 + 3.55 * s
            ax.add_patch(Rectangle((xb0, y - bh / 2), xb1 - xb0, bh, fc=COL["soft"], ec=COL["mark"],
                                   lw=0.6, zorder=6))
            bx = x0 + 3.05 * s
            ax.add_patch(Rectangle((bx - 0.5, y - bh / 2 - 0.6), 1.0, bh + 1.2, fc=ROLE["rose"]["fill"], ec="none",
                                   zorder=7))
            for dx in (-0.5, 0.5):
                ax.plot([bx + dx - 0.45, bx + dx + 0.45], [y - bh / 2 - 0.6, y + bh / 2 + 0.6],
                        color=LINE, lw=0.5, zorder=7.1)
            cv.text((xb0 + bx - 0.5) / 2, y, r"$+100C$", size=6.0, color=COL["ink"], z=8)
            end = xb1
        else:
            end = x0 + eff * s
        cv.text(end + 1.0, y, f"{r['cost']:.3f}", size=7.4 if sel else 6.4, ha="left",
                color=hue["ink"] if sel else INK, weight="bold" if sel else "normal")
        if sel:
            cv.chip(x + w - 2.0, y, "argmin", SEL, size=6.0, solid=True, h=3.0, pad=0.8, ha="right")
    ya = 59.6
    ax.plot([x0, x0 + 3.0 * s], [ya, ya], color="#9AA0A8", lw=0.5, zorder=5)
    for v in range(4):
        ax.plot([x0 + v * s] * 2, [ya, ya - 0.8], color="#9AA0A8", lw=0.5, zorder=5)
        cv.text(x0 + v * s, ya - 2.1, str(v), size=6.0, color=MUTED)
    ax.plot([x0, x0], [ya, 83.2], color="#9AA0A8", lw=0.5, zorder=5)
    cv.text(x0 + 3.0 * s + 1.5, ya - 2.1, "$J$", size=6.4, color=MUTED, ha="left")


def panel_d(cv, fx, ro, c):
    x, w = XD
    yt = panel(cv, x, TOP_Y, w, TOP_H, "blue", "(d) Execute")
    sub(cv, x + w / 2, yt - 1.0, "only $a_0$ of L is applied", ha="center")
    L = c["L"]
    a0, p0, p1 = ro["executed_action"], L["states"][0], L["states"][1]
    t = Tile(cv, x + (w - 28) / 2, 70.0, ro["next_state"], sc=2.8)
    t.draw()
    t.path(L["states"][1:], SEL["mark"], lw=0.8, alpha=0.45)
    t.goal(fx["scene"]["goal"])
    t.agent(p0, hollow=True, color=INK, d=1.3)
    cv.arrow([t.m(p0), t.m(p1)], color=EXE["mark"], lw=1.3, head=1.4, z=11)
    t.agent(p1, color=EXE["ink"], d=1.3)
    px, py = t.m(p0)
    cv.text(px, py + 1.8, r"$p_0$", size=6.2)
    px, py = t.m(p1)
    cv.text(px + 1.0, py - 1.4, r"$p_1$", size=6.2, color=EXE["ink"], ha="left", weight="bold")
    xl = x + 2.0
    cv.text(xl, 66.6, r"$a_0=$" + pt(a0), size=6.4, color=EXE["ink"], ha="left", weight="bold")
    cv.text(xl, 63.3, r"$p_1=$" + pt(p1) + ", swept: free", size=6.1, color=INK, ha="left")
    cv.text(xl, 60.0, r"$a_{1:3}$ not run", size=6.1, color=SEL["ink"], style="italic", ha="left")
    cv.text(xl, 56.0, r"$o_1=R(s_1)$", size=6.2, color=INK, ha="left")
    cv.chip(x + w - 2.0, 56.0, "replan", EXE, size=6.0, h=3.0, pad=0.8, ha="right")


# -------------------------------------------------------- detail (bottom) ---
BOT_Y, BOT_H = 9.5, 34.5


def candidate(cv, x, y, w, h, r, ob):
    cid, sel = r["id"], r["id"] == "L"
    hue = CAND[cid]
    if sel:
        cv.ax.add_patch(FancyBboxPatch((x + 0.4, y - 0.4), w, h, boxstyle="round,pad=0,rounding_size=1.6",
                                       lw=0, fc="#1A2230", alpha=0.10, zorder=1.4))
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.6", fc="white",
                                   ec=hue["mark"] if sel else hue["stroke"], lw=1.0 if sel else 0.6, zorder=1.5))
    ty = y + h - 2.6
    cv.text(x + 1.8, ty, f"{cid}  {r['name']}", size=6.8, weight="bold", color=hue["ink"], ha="left")
    if sel:
        cv.chip(x + w - 1.4, ty, "selected", SEL, size=6.0, solid=True, h=3.0, pad=0.7, ha="right")
    elif r["collision"]:
        cv.chip(x + w - 1.4, ty, "collision", COL, size=6.0, h=3.0, pad=0.7, ha="right")
    cols = [x + 11.0 + 6.9 * k for k in range(4)]
    yk, yx, yy = ty - 5.0, ty - 8.4, ty - 11.6
    cv.text(x + 2.2, yk, "$k$", size=6.1, color=MUTED, ha="left")
    for k, cx in enumerate(cols):
        cv.text(cx, yk, str(k), size=6.1, color=MUTED)
    if sel:  # a_0 is the executed action
        cv.ax.add_patch(FancyBboxPatch((cols[0] - 3.2, yy - 1.7), 6.4, yx - yy + 3.4,
                                       boxstyle="round,pad=0,rounding_size=0.8",
                                       fc=EXE["fill"], ec=EXE["stroke"], lw=0.5, zorder=8))
    for j, (lab, yv) in enumerate(((r"$a_x$", yx), (r"$a_y$", yy))):
        cv.text(x + 2.2, yv, lab, size=6.3, color=INK, ha="left")
        for k, cx in enumerate(cols):
            first = sel and k == 0
            cv.text(cx, yv, num(r["actions"][k][j]), size=6.3, z=21,
                    color=EXE["ink"] if first else INK, weight="bold" if first else "normal")
    yl = yy - 2.6
    cv.ax.plot([x + 1.5, x + w - 1.5], [yl] * 2, color=HAIR, lw=0.4, zorder=8)
    cv.rich(x + w / 2, yl - 2.6, [(f"$E={r['effort']:.2f}$", INK), (r"$\quad$", INK),
                                  (f"$C={r['collision']}$", COL["ink"] if r["collision"] else INK)], size=6.3,
            ha="center")
    cv.text(x + w / 2, yl - 6.0, r"$J=%s\cdot%.2f+%d\cdot%d=%.3f$" % (num(ob["effort_weight"]), r["effort"],
            ob["collision_penalty"], r["collision"], r["cost"]), size=6.1, color=hue["ink"],
            weight="bold" if sel else "normal")


def panel_e(cv, fx, c):
    x, w = 1.5, 115.5
    panel(cv, x, BOT_Y, w, BOT_H, "frozen", "(e) Candidate action sequences")
    cw = (w - 4.0 - 5.0) / 3
    for i, k in enumerate("DUL"):
        candidate(cv, x + 2.0 + i * (cw + 2.5), BOT_Y + 2.0, cw, 28.4, c[k], fx["objective"])


def panel_f(cv, c):
    x, w = 120.5, 56.0
    yt = panel(cv, x, BOT_Y, w, BOT_H, "coral", "(f) Swept collision test")
    seg = c["D"]["segments"][1]
    p, q = seg["from"], seg["to"]
    t0, t1 = seg["obstacles"][0]["interval"]
    sub(cv, x + w / 2, yt - 0.8, r"D, segment $k=1$: " + pt(p) + r" $\rightarrow$ " + pt(q), ha="center")
    sc, wx, wy = 17.0, (2.7, 5.3), (2.55, 3.45)
    t = Tile(cv, x + (w - 2.6 * sc) / 2, 21.5, {"obstacles": []}, sc=sc, wx=wx, wy=wy)
    ax = cv.ax
    x1, y1 = t.m((wx[1], wy[1]))
    ax.add_patch(Rectangle((t.x0, t.y0), x1 - t.x0, y1 - t.y0, fc=FLOOR, ec=NEU["stroke"], lw=0.5, zorder=3))
    (a0, _), (a1, _) = t.m((3.4, 0)), t.m((4.6, 0))
    ax.add_patch(Rectangle((a0, t.y0), a1 - a0, y1 - t.y0, fc=OBS_FILL, ec=OBS_EDGE, lw=0.55, hatch="////",
                           zorder=4))
    cv.text((a0 + a1) / 2, y1 - 2.2, "A", size=6.6, weight="bold", color=NEU["ink"], z=6,
            path_effects=[pe.withStroke(linewidth=1.6, foreground=OBS_FILL)])
    P, Q = t.m(p), t.m(q)
    ca = [p[i] + t0 * (q[i] - p[i]) for i in (0, 1)]
    cb = [p[i] + t1 * (q[i] - p[i]) for i in (0, 1)]
    cv.line([P, Q], color=CAND["D"]["mark"], lw=0.9, dashed=True, z=8, radius=0)
    cv.line([t.m(ca), t.m(cb)], color=COL["mark"], lw=2.2, dashed=False, z=9, radius=0)
    for pp, lab in ((P, r"$p_1$"), (Q, r"$p_2$")):
        ax.add_patch(Circle(pp, 0.75, fc="white", ec=CAND["D"]["mark"], lw=0.7, zorder=10))
        cv.text(pp[0], pp[1] + 2.4, lab, size=6.4, color=INK)
        cv.text(pp[0], pp[1] - 2.4, "free", size=6.0, color=MUTED, style="italic")
    ya = 17.6
    cv.line([(P[0], ya), (Q[0], ya)], color=LINE, lw=0.5, z=8, radius=0)
    for tv in (0.0, t0, t1, 1.0):
        xx = P[0] + tv * (Q[0] - P[0])
        hot = tv in (t0, t1)
        ax.plot([xx, xx], [ya - 0.6, ya + 0.6], color=COL["mark"] if hot else LINE, lw=0.6, zorder=8)
        cv.text(xx, ya - 2.0, f"{tv:.2f}", size=6.0, color=COL["ink"] if hot else MUTED)
        if hot:
            cv.line([(xx, ya + 0.6), (xx, t.y0)], color=COL["stroke"], lw=0.4, dashed=True, z=7, radius=0)
    ax.add_patch(Rectangle((P[0] + t0 * (Q[0] - P[0]), ya - 0.35), (t1 - t0) * (Q[0] - P[0]), 0.7,
                           fc=COL["mark"], ec="none", zorder=8.5))
    cv.text(P[0] - 2.8, ya, "$t$", size=6.4, color=INK, ha="right")
    cv.text(x + w / 2, 11.6, r"inside A for $t\in[%.2f,\,%.2f]\ \Rightarrow\ C=1$" % (t0, t1), size=6.3,
            color=COL["ink"])


def key(cv, x0, y0, x1, y1):
    """Key strip: every glyph the tiles use, defined once."""
    cv.ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=1.6", fc="white",
                                   ec=NEU["stroke"], lw=0.6, ls=(0, (3, 2)), zorder=1))
    g = Tile(cv, 0, 0, {"obstacles": []}, sc=1.0)
    yc, sz = (y0 + y1) / 2, 6.1
    items = [("agent", "agent $p_k$"), ("goal", "goal $g$"), ("state", "simulated state $k$"),
             ("obs", "obstacle"), ("sim", "simulated path"), ("hit", "inside obstacle"),
             ("exe", "executed $a_0$"), ("txt", r"$E=\Sigma_k\|a_k\|_2^2$ effort,  $C$ collision flag,  $J$ cost")]
    widths = [5.0 + cv.text_width(lab, sz) if kind != "txt" else cv.text_width(lab, sz) for kind, lab in items]
    gap = (x1 - x0 - 4.0 - sum(widths)) / (len(items) - 1)
    x = x0 + 2.0
    for (kind, lab), iw in zip(items, widths):
        gx = x + 2.0
        if kind == "agent":
            g.agent((gx, yc), d=1.3)
        elif kind == "goal":
            g.goal((gx - 0.6, yc - 1.4))
        elif kind == "state":
            cv.ax.add_patch(Circle((gx, yc), 0.55, fc="white", ec=LINE, lw=0.6, zorder=11))
        elif kind == "obs":
            cv.ax.add_patch(Rectangle((gx - 1.6, yc - 1.3), 3.2, 2.6, fc=OBS_FILL, ec=OBS_EDGE, lw=0.55,
                                      hatch="////", zorder=4))
        elif kind == "sim":
            cv.line([(gx - 2.0, yc), (gx + 2.0, yc)], color=LINE, lw=0.9, dashed=True, z=10, radius=0)
        elif kind == "hit":
            cv.line([(gx - 2.0, yc), (gx + 2.0, yc)], color=COL["mark"], lw=1.8, z=10, radius=0)
        elif kind == "exe":
            cv.arrow([(gx - 2.0, yc), (gx + 2.2, yc)], color=EXE["mark"], lw=1.2, head=1.3, z=11)
        cv.text(x if kind == "txt" else x + 5.0, yc, lab, size=sz, ha="left", color=INK)
        x += iw + gap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default=os.path.join(EX, "scene_fixture.json"))
    ap.add_argument("--rollouts", default=os.path.join(EX, "computed_rollouts.json"))
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    fx, ro, c = load(a.fixture, a.rollouts)
    matplotlib.rcParams["hatch.linewidth"] = 0.35
    cv = Canvas(W, H, family="serif", size=7.0)
    panel_a(cv, fx["scene"])
    panel_b(cv, fx, c)
    panel_c(cv, fx, c)
    panel_d(cv, fx, ro, c)
    ym = 74.0
    for (xa, wa), (xb, _) in zip((XA, XB, XC), (XB, XC, XD)):
        flow(cv, xa + wa + 0.3, xb - 0.3, ym)
    cv.phase_bar(47.6, [(XA[0], XA[0] + XA[1], "neutral", "observe"),
                        (XB[0], XB[0] + XB[1], "frozen", "simulate $H=4$ steps per candidate"),
                        (XC[0], XC[0] + XC[1], "rose", r"score $J$, take argmin"),
                        (XD[0], XD[0] + XD[1], "blue", "execute, replan")], h=3.2, size=6.4, gap=0.0)
    panel_e(cv, fx, c)
    panel_f(cv, c)
    key(cv, 1.5, 0.6, 176.5, 7.4)
    small = [t for t in cv.ax.texts if t.get_fontsize() < 6.0]
    assert not small, [t.get_text() for t in small]
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    print("\n".join(cv.save(os.path.join(a.out, "scene_planning_figure"))))


if __name__ == "__main__":
    main()
