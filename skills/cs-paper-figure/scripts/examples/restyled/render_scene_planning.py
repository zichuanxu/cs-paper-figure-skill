#!/usr/bin/env python3
"""Scene-grounded planning with swept-path checks: one scene, three rollouts, one executed step.

Source: gallery/before/scene-planning.png (a deterministic illustrative simulation, not a
benchmark) and the bundled data/scene-planning/scene_fixture.json, computed_rollouts.json and
scene_model.py, the model that produced the rollouts.

Content kept from the source
  * the explicit state s0 (point agent p0, goal g, Barrier A, Pier B), the task generated from
    the same fixture, the rendered observation o0 = R(s0) and the fact that the planner reads s0
    directly;
  * the rollout model p[k+1] = p[k] + dt a[k] with dt = 1, H = 4, ||a|| <= 3.5 and the three
    candidates D, U, L with every action component;
  * the cost J = ||p4 - g||^2 + 0.1 E + 100 C with E, C and J per candidate, and argmin J = L;
  * the swept test on D's segment (3, 3) -> (5, 3): both endpoints are free, t in [0.20, 0.80]
    lies inside A;
  * execution of the selected first action only: a0 = (1.5, -1.8), p1 = (2.5, 1.2), then replan.

Design
  * Five-second message: the straight path looks free at its sampled states but its swept segment
    cuts the barrier; the lower detour is the cheapest collision-free rollout and only its first
    step is executed. The hero is one large scene in which all three rollouts share coordinates,
    so the comparison is on the object instead of across three small maps.
  * One hue per candidate on its path, state badges, name chip and cost card: coral = D,
    purple = U, teal = L. Amber is the goal only, blue the given fixture only, grey the obstacles.
    Dashed = simulated rollout, solid arrow = the executed step, thick solid = inside an obstacle.
  * The fixture is a data object (window with one row per scene entity), the swept test is drawn
    on the segment's own parameter axis, and each cost card instantiates J term by term.
  * Added from computed_rollouts.json (not in the source figure): the upper detour's smallest
    clearance to Pier B, 0.13, drawn at its closest point.
  * Every number is read from the fixture or recomputed with scene_model.rollout and asserted
    against computed_rollouts.json. The candidate paths are data marks; D crossing A is the
    displayed failure and is asserted numerically, while the executed-step arrow is audited as a
    wire against both obstacles.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from matplotlib.patches import Circle, PathPatch, Polygon, Rectangle  # noqa: E402
from paperkit import INK, MUTED, ROLE, Canvas, _round_top_rect  # noqa: E402

DATA = HERE / "data" / "scene-planning"
HUE = {"D": "coral", "U": "purple", "L": "teal"}
FIX, GOAL = "blue", "amber"
OBST_FC, OBST_EC = "#D3D8DF", "#5E6875"
DASH = (0, (3.4, 2.0))


# ------------------------------------------------------------------ data ---
def g(x):
    """2, 1.5, -1.8 with a true minus."""
    return f"{x:g}".replace("-", "−")


def pt(p):
    return f"({g(p[0])}, {g(p[1])})"


def derive(fixture, rollouts):
    """Load the fixture and the stored rollouts; re-run the bundled model and assert they agree."""
    F, R = json.loads(Path(fixture).read_text()), json.loads(Path(rollouts).read_text())
    spec = importlib.util.spec_from_file_location("scene_model", DATA / "scene_model.py")
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    again = model.rollout(F)
    obj, close = F["objective"], lambda a, b: abs(a - b) < 1e-9  # noqa: E731
    assert again["selected_id"] == R["selected_id"] and again["task"] == R["task"]
    for c, c2, cf in zip(R["candidates"], again["candidates"], F["candidates"]):
        assert c["id"] == c2["id"] == cf["id"] and c["actions"] == cf["actions"] and c["collision"] == c2["collision"]
        assert all(close(a, b) for p, q in zip(c["states"], c2["states"]) for a, b in zip(p, q))
        assert close(c["cost"], c2["cost"]) and close(c["effort"], c2["effort"])
        c["terms"] = (c["terminal_squared_distance"], obj["effort_weight"] * c["effort"],
                      obj["collision_penalty"] * c["collision"])
        assert close(sum(c["terms"]), c["cost"])
        assert c["collision"] == int(any(s["collision"] for s in c["segments"]))
        assert max(c["action_norms"]) <= F["dynamics"]["max_action_norm"]
        assert len(c["actions"]) == F["dynamics"]["horizon"]
    best = min(R["candidates"], key=lambda c: c["cost"])
    assert best["id"] == R["selected_id"] and best["collision"] == 0
    assert R["executed_action"] == best["actions"][0] and R["executed_action_count"] == 1
    assert R["next_state"]["agent"]["position"] == best["states"][1]
    # the displayed failure: a segment whose two endpoints are free but whose interior is inside an obstacle
    hits = [(c, s, o) for c in R["candidates"] for s in c["segments"] for o in s["obstacles"] if o["hit"]]
    assert len(hits) == 1
    hc, hs, ho = hits[0]
    ob = {o["id"]: o for o in F["scene"]["obstacles"]}
    b = ob[ho["obstacle_id"]]["bounds"]
    assert not any(b[0] <= p[0] <= b[1] and b[2] <= p[1] <= b[3] for p in (hs["from"], hs["to"]))
    # the tightest collision-free pass of a circle obstacle
    near = min(((c, s, o) for c in R["candidates"] for s in c["segments"] for o in s["obstacles"]
                if "clearance" in o and not c["collision"]), key=lambda t: t[2]["clearance"])
    return dict(F=F, R=R, best=best, hit=dict(cand=hc, seg=hs, obs=ho), near=dict(cand=near[0], seg=near[1], obs=near[2]),
                obstacles=ob)


# --------------------------------------------------------------- helpers ---
def star(cv, x, y, r, c, z=9.0, lw=0.6):
    pts = [(x + (r if i % 2 == 0 else r * 0.42) * math.sin(i * math.pi / 5),
            y + (r if i % 2 == 0 else r * 0.42) * math.cos(i * math.pi / 5)) for i in range(10)]
    cv.ax.add_patch(Polygon(pts, closed=True, fc=c["mark"], ec=c["ink"], lw=lw, zorder=z, joinstyle="round"))


def obstacle(cv, o, M, s, z=3.0, labels=True):
    if o["type"] == "aabb":
        x0, x1, y0, y1 = o["bounds"]
        (a, b), (c, d) = M(x0, y0), M(x1, y1)
        cv.solids.append((a, b, c - a, d - b, f"obstacle {o['id']}", None))
        cv.ax.add_patch(Rectangle((a, b), c - a, d - b, fc=OBST_FC, ec=OBST_EC, lw=0.8, zorder=z))
        cx, cy = (a + c) / 2, d - 5.6
    else:
        cx, cy = M(*o["center"])
        r = o["radius"] * s
        cv.solids.append((cx - r * 0.7, cy - r * 0.7, r * 1.4, r * 1.4, f"obstacle {o['id']}", None))
        cv.ax.add_patch(Circle((cx, cy), r, fc=OBST_FC, ec=OBST_EC, lw=0.8, zorder=z))
        cy -= 0.3
    if labels:
        cv.text(cx, cy + 1.5, o["id"], size=7.2, weight="bold", color="#2F3743", z=4)
        cv.text(cx, cy - 1.5, o["name"], size=6.0, style="italic", color="#2F3743", z=4)


def lerp(p, q, t):
    return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))


# ------------------------------------------------------------------ draw ---
def draw(d):
    F, R = d["F"], d["R"]
    scene, dyn, obj = F["scene"], F["dynamics"], F["objective"]
    W, H = 178.0, 130.0
    cv = Canvas(W, H)
    LX, LW, RX, RW = 1.5, 55.0, 59.5, 117.0
    TY, TH, BY, BH = 50.5, 76.5, 1.5, 44.0
    fix = ROLE[FIX]
    p0, goal = scene["agent"]["position"], scene["goal"]

    # ============================== (b) scene and rollouts (hero) ===============================
    cv.section(RX, TY, RW, TH, "neutral", "Scene and candidate rollouts", letter="b", fill="#FBFBFC")
    S, MX, MY = 10.8, 65.6, 55.8
    bx0, bx1, by0, by1 = scene["bounds"]
    M = lambda x, y: (MX + (x - bx0) * S, MY + (y - by0) * S)  # noqa: E731
    (mx0, my0), (mx1, my1) = M(bx0, by0), M(bx1, by1)
    cv.ax.add_patch(Rectangle((mx0, my0), mx1 - mx0, my1 - my0, fc="#F8F7F2", ec="none", zorder=2))
    for i in range(int(bx0) + 1, int(bx1)):
        cv.ax.plot([M(i, 0)[0]] * 2, [my0, my1], color="#E6E3D9", lw=0.4, zorder=2.1)
    for j in range(int(by0) + 1, int(by1)):
        cv.ax.plot([mx0, mx1], [M(0, j)[1]] * 2, color="#E6E3D9", lw=0.4, zorder=2.1)
    cv.ax.add_patch(Rectangle((mx0, my0), mx1 - mx0, my1 - my0, fc="none", ec="#4A5260", lw=1.1, zorder=4.5))
    for v in (bx0, (bx0 + bx1) / 2, bx1):
        cv.ax.plot([M(v, 0)[0]] * 2, [my0, my0 - 1.0], color="#4A5260", lw=0.6, zorder=4)
        cv.text(M(v, 0)[0], my0 - 2.5, g(v), size=6.2, color="#4A5059")
    for v in (by0, (by0 + by1) / 2, by1):
        cv.ax.plot([mx0, mx0 - 1.0], [M(0, v)[1]] * 2, color="#4A5260", lw=0.6, zorder=4)
        cv.text(mx0 - 1.7, M(0, v)[1], g(v), size=6.2, color="#4A5059", ha="right")
    cv.text(mx0, my1 + 1.9, r"rendered scene $o_0 = R(s_0)$, dimensionless units", size=6.5, color=MUTED, ha="left")
    cv.chip(mx1, my1 + 1.9, "ILLUSTRATIVE SIMULATION", "neutral", size=5.8, ha="right")
    for o in scene["obstacles"]:
        obstacle(cv, o, M, S)

    for c in R["candidates"]:
        col, sel = ROLE[HUE[c["id"]]], c["id"] == R["selected_id"]
        P = [M(*p) for p in c["states"]]
        first = 1 if sel else 0  # the selected first step is drawn as the executed arrow instead
        cv.ax.plot([p[0] for p in P[first:]], [p[1] for p in P[first:]], color=col["mark"], lw=1.25, ls=DASH,
                   zorder=6, dash_capstyle="butt", solid_joinstyle="round")
        for sgm in c["segments"]:
            for o in sgm["obstacles"]:
                if o["hit"]:  # swept collision: the part of the segment inside the obstacle
                    a, b = (M(*lerp(sgm["from"], sgm["to"], t)) for t in o["interval"])
                    cv.ax.plot([a[0], b[0]], [a[1], b[1]], color=col["mark"], lw=2.8, zorder=6.2, solid_capstyle="butt")
                    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
                    cv.ax.add_patch(Circle(mid, 1.75, fc="white", ec=col["mark"], lw=0.8, zorder=7))
                    cv.icon_cross(mid[0], mid[1], 2.0, color=col["mark"], lw=1.1, z=7.5)
        for k, p in enumerate(P[1:-1], start=1):
            cv.badge(p[0], p[1], k, HUE[c["id"]], d=3.2, z=8)
        if sel:
            u = (P[1][0] - P[0][0], P[1][1] - P[0][1])
            n = math.hypot(*u)
            u = (u[0] / n, u[1] / n)
            cv.arrow([(P[0][0] + u[0] * 1.3, P[0][1] + u[1] * 1.3), (P[1][0] - u[0] * 1.6, P[1][1] - u[1] * 1.6)],
                     color=col["mark"], lw=1.9, head=2.4, z=7)
    a0, p1 = R["executed_action"], R["next_state"]["agent"]["position"]
    tl = ROLE[HUE[R["selected_id"]]]
    x, y = M(0.2, 2.12)
    cv.text(x, y, "executed", size=6.8, weight="bold", color=tl["ink"], ha="left")
    cv.text(x, y - 3.1, f"$a_0$ = {pt(a0)}", size=6.6, color=tl["ink"], ha="left")
    x, y = M(p1[0] - 0.24, p1[1])
    cv.text(x, y, f"$p_1$ = {pt(p1)}", size=6.6, color=tl["ink"], ha="right")
    cv.text(x, y - 3.5, r"then replan from $o_1$", size=6.5, style="italic", color=MUTED, ha="right")
    x, y = M(*p0)
    cv.ax.add_patch(Circle((x, y), 1.3, fc="#1F2530", ec="white", lw=0.6, zorder=9))
    cv.text(x - 2.4, y, "$p_0$", size=7.2, weight="bold", ha="right")
    x, y = M(*goal)
    star(cv, x, y, 2.7, ROLE[GOAL])
    cv.text(x + 3.6, y, "$g$", size=7.6, weight="bold", color=ROLE[GOAL]["ink"], ha="left")
    for cid, (ux, uy) in {"D": (6.0, 3.38), "U": (3.65, 5.2), "L": (3.65, 0.79)}.items():
        c = next(c for c in R["candidates"] if c["id"] == cid)
        cv.chip(*M(ux, uy), f"{cid}  {c['name']}", HUE[cid], size=6.2, solid=True, z=10)
    # tightest free pass: the gap between the path and the pier at the closest point
    nr = d["near"]
    oc = d["obstacles"][nr["obs"]["obstacle_id"]]
    cp, cc, rr = nr["obs"]["closest"], oc["center"], oc["radius"]
    dist = nr["obs"]["distance_to_center"]
    edge = (cc[0] + (cp[0] - cc[0]) * rr / dist, cc[1] + (cp[1] - cc[1]) * rr / dist)
    assert abs(math.dist(cp, edge) - nr["obs"]["clearance"]) < 1e-9
    nc = ROLE[HUE[nr["cand"]["id"]]]
    (ax_, ay_), (bx_, by_) = M(*edge), M(*cp)
    cv.ax.plot([ax_, bx_], [ay_, by_], color=nc["ink"], lw=1.0, zorder=7, solid_capstyle="butt")
    lx, ly = M(cp[0] + 0.55, cp[1] + 0.42)
    cv.ax.plot([bx_ + 0.5, lx - 0.6], [by_ + 0.4, ly - 0.5], color=nc["ink"], lw=0.45, zorder=7)
    cv.text(lx, ly, f"clears {oc['id']} by {nr['obs']['clearance']:.2f}", size=6.0, style="italic", color=nc["ink"], ha="left")

    # map key (line styles and marks)
    kx, ky, kw, row = M(7.05, 0)[0], my0 + 1.3, 31.2, 3.05
    cv.ax.add_patch(Rectangle((kx, ky), kw, 4 * row + 1.2, fc="white", ec="#B7BDC6", lw=0.5, zorder=5))
    yy = ky + 4 * row + 0.6 - row / 2
    cv.ax.plot([kx + 1.4, kx + 7.4], [yy, yy], color="#59616D", lw=1.2, ls=DASH, zorder=6, dash_capstyle="butt")
    cv.text(kx + 9.0, yy, "simulated rollout", size=6.0, ha="left")
    yy -= row
    cv.arrow([(kx + 1.4, yy), (kx + 7.4, yy)], color=tl["mark"], lw=1.7, head=2.0, z=6)
    cv.text(kx + 9.0, yy, "executed step", size=6.0, ha="left")
    yy -= row
    cv.ax.plot([kx + 1.4, kx + 7.4], [yy, yy], color=ROLE[HUE[d["hit"]["cand"]["id"]]]["mark"], lw=2.8, zorder=6,
               solid_capstyle="butt")
    cv.text(kx + 9.0, yy, "inside an obstacle", size=6.0, ha="left")
    yy -= row
    cv.badge(kx + 4.4, yy, "k", "neutral", d=2.9, z=6)
    cv.text(kx + 9.0, yy, r"predicted state $p_k$", size=6.5, ha="left")

    # ============================== (a) fixture ==================================================
    cv.section(LX, TY, LW, TH, FIX, "Scene fixture", letter="a")
    wx, ww, wt, bar, rh = 4.0, 50.5, 122.4, 4.4, 5.0
    ents = [("p0", pt(p0), f"agent ({scene['agent']['geometry']})"), ("g", pt(goal), "goal")]
    for o in scene["obstacles"]:
        if o["type"] == "aabb":
            b = o["bounds"]
            ents.append((o["id"], f"[{g(b[0])}, {g(b[1])}]×[{g(b[2])}, {g(b[3])}]", o["name"]))
        else:
            ents.append((o["id"], f"c {pt(o['center'])}, r {g(o['radius'])}", o["name"]))
    wh = bar + len(ents) * rh + 1.0
    cv.box(wx, wt - wh, ww, wh, FIX, fill="white", radius=1.2, lw=0.7, shadow=True)
    cv.ax.add_patch(PathPatch(_round_top_rect(wx, wt - bar, ww, bar, 1.2), fc=fix["soft"], ec=fix["stroke"], lw=0.7, zorder=5.2))
    for k, colr in enumerate(("#E0645A", "#E8B23A", "#5DB86A")):
        cv.ax.add_patch(Circle((wx + 2.3 + k * 1.9, wt - bar / 2), 0.6, fc=colr, ec="none", zorder=6))
    cv.text(wx + 8.6, wt - bar / 2, "scene_fixture.json", size=6.0, family="monospace", weight="bold", color=fix["ink"],
            ha="left", z=7)
    cv.text(wx + ww - 1.6, wt - bar / 2, "state $s_0$", size=6.5, color=fix["ink"], ha="right", z=7)
    for i, (name, val, tag) in enumerate(ents):
        cy = wt - bar - (i + 0.5) * rh - 0.2
        if name == "p0":
            cv.ax.add_patch(Circle((wx + 2.6, cy), 0.95, fc="#1F2530", ec="none", zorder=7))
        elif name == "g":
            star(cv, wx + 2.6, cy, 1.5, ROLE[GOAL], z=7, lw=0.4)
        elif "×" in val:
            cv.ax.add_patch(Rectangle((wx + 1.9, cy - 1.2), 1.4, 2.4, fc=OBST_FC, ec=OBST_EC, lw=0.5, zorder=7))
        else:
            cv.ax.add_patch(Circle((wx + 2.6, cy), 1.05, fc=OBST_FC, ec=OBST_EC, lw=0.5, zorder=7))
        cv.text(wx + 5.0, cy, name, size=6.0, family="monospace", weight="bold", ha="left", z=7)
        cv.text(wx + 9.2, cy, val, size=6.0, family="monospace", ha="left", z=7)
        cv.text(wx + ww - 1.6, cy, tag, size=6.0, style="italic", color=fix["ink"], ha="right", z=7)
        if i:
            cv.ax.plot([wx + 1.2, wx + ww - 1.2], [cy + rh / 2] * 2, color="#E3E7EE", lw=0.4, zorder=6)
    ry = wt - wh / 2 - 1.0
    cv.arrow([(wx + ww, ry), (mx0 - 0.55, ry)], lw=0.8, head=1.5)
    cv.text(RX + 3.0, ry + 2.1, "$R$", size=6.8)

    ty = wt - wh - 4.4
    cv.text(wx, ty, "Task", size=6.8, weight="bold", color=fix["ink"], ha="left")
    cv.text(wx + ww, ty, "from the same fixture", size=5.9, style="italic", color=MUTED, ha="right")
    cv.box(wx, ty - 9.2, ww, 6.6, FIX, fill="white", radius=1.2, lw=0.6)
    cv.text(wx + ww / 2, ty - 5.9, R["task"], size=6.6, style="italic", z=7)

    my = ty - 14.2
    cv.text(wx, my, "Rollout model", size=6.8, weight="bold", color=fix["ink"], ha="left")
    gy = my - 6.4
    cv.ax.add_patch(Circle((wx + 4.5, gy), 0.95, fc="#1F2530", ec="none", zorder=7))
    cv.ax.add_patch(Circle((wx + 19.5, gy), 0.95, fc="white", ec="#1F2530", lw=0.7, zorder=7))
    cv.arrow([(wx + 5.7, gy), (wx + 18.3, gy)], lw=0.8, head=1.5)
    cv.text(wx + 12.0, gy + 2.0, "$a_k$", size=6.6)
    cv.text(wx + 4.5, gy - 2.9, "$p_k$", size=6.6)
    cv.text(wx + 19.5, gy - 2.9, "$p_{k+1}$", size=6.6)
    cv.text(wx + ww - 0.5, gy - 0.4, r"$p_{k+1} = p_k + \Delta t\,a_k$", size=7.0, ha="right")
    cv.flow_chips([f"$\\Delta t$ = {g(dyn['dt'])}", f"$H$ = {dyn['horizon']}",
                   f"$\\|a_k\\|_2 \\leq$ {g(dyn['max_action_norm'])}"], wx, wx + ww, gy - 6.2, "neutral", size=6.5, gap=2.0)
    cv.text(wx + ww / 2, TY + 6.6, "planner reads $s_0$ directly;", size=6.5, style="italic", color=MUTED)
    cv.text(wx + ww / 2, TY + 3.8, "no learned perception", size=6.5, style="italic", color=MUTED)

    # ============================== (c) swept-segment test ======================================
    hit = d["hit"]
    hid, hk = hit["cand"]["id"], hit["seg"]["k"]
    hc = ROLE[HUE[hid]]
    oid = hit["obs"]["obstacle_id"]
    t0, t1 = hit["obs"]["interval"]
    cv.section(LX, BY, LW, BH, HUE[hid], "Swept-segment test", letter="c")
    cv.rich(4.2, 39.4, [(f"{hid}", hc["ink"], "bold"), (f", segment $p_{hk} \\rightarrow p_{hk + 1}$", INK)], size=6.8)
    X = lambda t: 9.5 + 38.0 * t  # noqa: E731
    sy, ay0, ay1 = 28.6, 22.6, 34.6
    cv.ax.add_patch(Rectangle((X(t0), ay0), X(t1) - X(t0), ay1 - ay0, fc=OBST_FC, ec=OBST_EC, lw=0.8, zorder=3))
    cv.text((X(t0) + X(t1)) / 2, ay1 - 2.1, oid, size=7.2, weight="bold", color="#2F3743", z=4)
    cv.ax.plot([X(0), X(1)], [sy, sy], color=hc["mark"], lw=1.25, ls=DASH, zorder=6, dash_capstyle="butt")
    cv.ax.plot([X(t0), X(t1)], [sy, sy], color=hc["mark"], lw=2.8, zorder=6.2, solid_capstyle="butt")
    for t, p, ha in ((0, hit["seg"]["from"], "left"), (1, hit["seg"]["to"], "right")):
        cv.badge(X(t), sy, hk + t, HUE[hid], d=3.2, z=8)
        cv.text(X(t) + (-2.0 if t == 0 else 2.0), sy + 3.6, pt(p), size=6.4, color=hc["ink"], ha=ha)
    ty0 = 19.4
    cv.ax.plot([X(0), X(1)], [ty0, ty0], color="#59616D", lw=0.6, zorder=5)
    cv.ax.plot([X(t0), X(t1)], [ty0, ty0], color=hc["mark"], lw=2.0, zorder=5.5, solid_capstyle="butt")
    for t in (0, t0, t1, 1):
        cv.ax.plot([X(t), X(t)], [ty0 - 0.9, ty0 + 0.9], color="#59616D", lw=0.6, zorder=6)
        cv.text(X(t), ty0 - 2.5, "0" if t == 0 else "1" if t == 1 else f"{t:.2f}", size=6.2, color="#4A5059")
        if 0 < t < 1:
            cv.ax.plot([X(t), X(t)], [ty0 + 0.9, ay0], color=OBST_EC, lw=0.4, ls=(0, (1.5, 1.2)), zorder=4)
    cv.text(X(1) + 3.4, ty0, "$t$", size=6.6)
    cv.box(4.0, 8.9, 50.5, 4.4, "neutral", fill="white", radius=1.2, lw=0.5)
    cv.icon_check(7.0, 11.1, 2.2, color="#3A4250", lw=1.0)
    cv.text(10.0, 11.05, f"endpoints $p_{hk}$, $p_{hk + 1}$ are outside {oid}", size=6.5, ha="left", z=7)
    cv.box(4.0, 3.5, 50.5, 4.4, HUE[hid], fill=hc["soft"], radius=1.2, lw=0.6)
    cv.icon_cross(7.0, 5.7, 2.0, color=hc["mark"], lw=1.2)
    cv.text(10.0, 5.65, f"inside {oid} for $t \\in$ [{t0:.2f}, {t1:.2f}]:  $C$ = 1", size=6.4, weight="bold",
            color=hc["ink"], ha="left", z=7)

    # ============================== (d) cost and selection ======================================
    cv.section(RX, BY, RW, BH, "neutral", "Cost and selection", letter="d", fill="#FBFBFC")
    ew, pen = obj["effort_weight"], obj["collision_penalty"]
    cv.text(RX + 2.6, 40.0, f"$J = \\|p_{dyn['horizon']} - g\\|_2^2 + {g(ew)}\\,E + {g(pen)}\\,C$,"
            r"    $E = \Sigma_k\,\|a_k\|_2^2$", size=6.9, ha="left")
    cv.text(RX + RW - 2.6, 40.0, "$C$ = 1 if any swept segment collides", size=6.2, style="italic", color=MUTED, ha="right")
    n = len(R["candidates"])
    cw_ = (RW - 4.0 - 2.0 * (n - 1)) / n
    cy0, chh, hb = 3.5, 33.0, 5.0
    for i, c in enumerate(R["candidates"]):
        r_, col, sel = HUE[c["id"]], ROLE[HUE[c["id"]]], c["id"] == R["selected_id"]
        x = RX + 2.0 + i * (cw_ + 2.0)
        cv.box(x, cy0, cw_, chh, r_, fill="white", radius=1.4, lw=1.2 if sel else 0.7, shadow=sel,
               stroke=col["mark"] if sel else None)
        cv.ax.add_patch(PathPatch(_round_top_rect(x, cy0 + chh - hb, cw_, hb, 1.4), fc=col["mark"] if sel else col["soft"],
                                  ec=col["mark"] if sel else col["stroke"], lw=1.2 if sel else 0.7, zorder=5.2))
        hy, on = cy0 + chh - hb / 2, "white" if sel else col["ink"]
        cv.ax.add_patch(Circle((x + 3.4, hy), 1.75, fc="white" if sel else col["mark"], ec="none", zorder=6))
        cv.text(x + 3.4, hy - 0.05, c["id"], size=6.6, weight="bold", color=col["ink"] if sel else "white", z=7)
        cv.text(x + 6.2, hy, c["name"], size=6.9, weight="bold", color=on, ha="left", z=7)
        verdict = "collides" if c["collision"] else "selected" if sel else "free"
        tw = cv.text_width(verdict, 6.4, "bold")
        (cv.icon_cross if c["collision"] else cv.icon_check)(x + cw_ - 3.6 - tw, hy, 1.9, color=on, lw=1.0)
        cv.text(x + cw_ - 1.8, hy, verdict, size=6.4, weight="bold", color=on, ha="right", z=7)
        # action sequence a_0 .. a_3
        cell, ch_ = 5.7, 3.7
        gx, gy0 = x + (cw_ - 4 * cell) / 2 + 2.2, cy0 + chh - hb - 3.6 - 2 * ch_
        cv.text(gx - 1.2, gy0 + 2 * ch_ + 1.5, "$k$", size=6.2, color=MUTED, ha="right")
        for k, a in enumerate(c["actions"]):
            cv.text(gx + (k + 0.5) * cell, gy0 + 2 * ch_ + 1.5, str(k), size=6.2, color=MUTED)
            for j in range(2):
                cv.ax.add_patch(Rectangle((gx + k * cell, gy0 + (1 - j) * ch_), cell, ch_, fc=col["fill"], ec=col["stroke"],
                                          lw=0.45, zorder=6))
                cv.text(gx + (k + 0.5) * cell, gy0 + (1.5 - j) * ch_ - 0.05, g(a[j]), size=6.3, color=col["ink"], z=7)
        for j, lab in enumerate(("$a_x$", "$a_y$")):
            cv.text(gx - 1.2, gy0 + (1.5 - j) * ch_, lab, size=6.5, ha="right")
        # J, term by term
        term, eff, coll = c["terms"]
        rows = [(f"$\\|p_{dyn['horizon']} - g\\|_2^2$", "", g(term)),
                (f"${g(ew)}\\,E$", f"$E$ = {c['effort']:.2f}", f"{eff:.3f}"),
                (f"${g(pen)}\\,C$", f"$C$ = {c['collision']}", g(coll))]
        ly = gy0 - 3.0
        for lab, note, val in rows:
            bad = c["collision"] and lab.endswith("C$")
            cv.text(x + 2.4, ly, lab, size=6.5, ha="left", z=7)
            if note:
                cv.text(x + 12.4, ly, note, size=6.0, color=MUTED, ha="left", z=7)
            cv.text(x + cw_ - 2.4, ly, val, size=6.4, ha="right", z=7, weight="bold" if bad else "normal",
                    color=col["ink"] if bad else INK)
            ly -= 3.05
        cv.ax.plot([x + 2.2, x + cw_ - 2.2], [ly + 1.35] * 2, color=col["stroke"], lw=0.5, zorder=6)
        cv.text(x + 2.4, ly - 1.0, "$J$", size=7.0, weight="bold", ha="left", z=7)
        if sel:
            cv.text(x + 6.0, ly - 1.0, "minimum", size=6.0, style="italic", color=col["ink"], ha="left", z=7)
        cv.text(x + cw_ - 2.4, ly - 1.0, f"{c['cost']:.3f}", size=7.4, weight="bold", color=col["ink"], ha="right", z=7)
    return cv


def build(fixture=DATA / "scene_fixture.json", rollouts=DATA / "computed_rollouts.json"):
    return draw(derive(fixture, rollouts))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="figures/scene")
    ap.add_argument("--fixture", default=str(DATA / "scene_fixture.json"))
    ap.add_argument("--rollouts", default=str(DATA / "computed_rollouts.json"))
    a = ap.parse_args()
    cv = build(a.fixture, a.rollouts)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    print("\n".join(cv.save(os.path.join(a.out, "scene-planning"))))


if __name__ == "__main__":
    main()
