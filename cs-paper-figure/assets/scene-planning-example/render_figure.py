#!/usr/bin/env python3
"""Reproduce the original scene-planning plate and its deterministic observations.

Run from any working directory:
  python render_figure.py --out .

No source-paper artwork is copied. All scene positions, actions, collision
annotations, numbers, and the executed transition come from scene_fixture.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Respect an explicit output directory before Matplotlib initializes its cache;
# the source can therefore reside in a read-only installed skill directory.
_bootstrap=argparse.ArgumentParser(add_help=False)
_bootstrap.add_argument("--out",type=Path,default=HERE)
_boot_args,_boot_rest=_bootstrap.parse_known_args()
os.environ.setdefault("MPLCONFIGDIR", str(_boot_args.out.resolve() / "_work" / "mplconfig"))
import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle
from matplotlib.text import Text
import numpy as np

from figure_style import export_figure, style_context
from scene_model import load_fixture, rollout

W, H = 178.0, 203.0
COL = {
    "ink": "#233746", "muted": "#536572", "rule": "#BBC5CB",
    "grid": "#E4E4DF", "floor": "#F7F6F0", "wall": "#8E9AA1",
    "obstacle": "#C7CDD0", "obstacle_edge": "#6A7780",
    "D": "#AE403B", "U": "#7255A1", "L": "#087C78",
    "D_pale": "#FBEFEC", "U_pale": "#F3EFF9", "L_pale": "#E8F5F1",
    "goal": "#A96C0C", "goal_fill": "#F8D988", "white": "#FFFFFF",
}
REGULAR = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="normal"))
BOLD = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))
MONO = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans Mono", weight="normal"))


def star_vertices(cx, cy, radius):
    angles = np.arange(10) * np.pi / 5 - np.pi / 2
    radii = np.where(np.arange(10) % 2 == 0, radius, radius * .43)
    return [(cx + r * np.cos(t), cy + r * np.sin(t)) for t, r in zip(angles, radii)]


class Plate:
    def __init__(self, width=W, height=H):
        self.width, self.height = width, height
        self.fig = plt.figure(figsize=(width / 25.4, height / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set(xlim=(0, width), ylim=(height, 0))
        self.ax.axis("off")
        self.text_items, self.maps, self.connectors = [], [], []

    def text(self, x, y, s, size=7.6, color="ink", bold=False, ha="left", mono=False, owner=None, z=9):
        fp = font_manager.FontProperties(fname=MONO if mono else BOLD if bold else REGULAR, size=size)
        item = self.ax.text(x, y, s, fontsize=size, color=COL.get(color, color), ha=ha, va="center",
                            fontproperties=fp, zorder=z, linespacing=1.25)
        self.text_items.append({"artist": item, "owner": owner, "text": s, "size_pt": size})
        return item

    def rect(self, x, y, w, h, fill="white", edge=None, lw=.7, z=1, **kw):
        obj = Rectangle((x, y), w, h, facecolor=COL.get(fill, fill),
                        edgecolor=COL.get(edge, edge) if edge else "none", linewidth=lw, zorder=z, **kw)
        self.ax.add_patch(obj)
        return obj

    def line(self, points, color="rule", lw=.6, style="-", z=2):
        a = np.asarray(points, float)
        return self.ax.plot(a[:, 0], a[:, 1], color=COL.get(color, color), lw=lw, linestyle=style,
                            solid_capstyle="round", zorder=z)[0]

    def arrow(self, a, b, color="muted", lw=.95, scale=7.5, label=None):
        self.ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", color=COL.get(color, color),
                                         lw=lw, mutation_scale=scale, shrinkA=0, shrinkB=0, zorder=6))
        self.connectors.append({"from_mm": a, "to_mm": b, "label": label})

    def heading(self, x, y, letter, title):
        self.text(x, y, letter, 9.3, bold=True)
        self.text(x + 5.4, y, title, 9.0, bold=True)

    def scene(self, x, y, w, h, scene, *, candidate=None, panel_id="scene", labels=True,
              indices=False, axes=False, transition=None, raw=False):
        bounds = scene["bounds"]
        xmin, xmax, ymin, ymax = bounds
        sx, sy = w / (xmax - xmin), h / (ymax - ymin)
        assert abs(sx - sy) < 1e-9, "Spatial geometry must use isotropic scale"
        def world(p):
            return (x + (p[0] - xmin) * sx, y + (ymax - p[1]) * sy)
        self.rect(x, y, w, h, "floor", "wall", .65)
        for gx in np.arange(xmin + 1, xmax, 1):
            self.line([world((gx, ymin)), world((gx, ymax))], "grid", .28)
        for gy in np.arange(ymin + 1, ymax, 1):
            self.line([world((xmin, gy)), world((xmax, gy))], "grid", .28)
        obstacle_drawings = []
        for o in scene["obstacles"]:
            if o["type"] == "aabb":
                bx0, bx1, by0, by1 = o["bounds"]
                px, py = world((bx0, by1))
                self.rect(px, py, (bx1 - bx0) * sx, (by1 - by0) * sy,
                          "obstacle", "obstacle_edge", .65, z=3, hatch="///")
                label_at = world(((bx0 + bx1) / 2, by1 - .42))
                obstacle_drawings.append({"id": o["id"], "type": "aabb", "bounds_mm": [px, py, (bx1-bx0)*sx, (by1-by0)*sy]})
            else:
                center = world(o["center"])
                self.ax.add_patch(Circle(center, o["radius"] * sx, facecolor=COL["obstacle"],
                                         edgecolor=COL["obstacle_edge"], lw=.65, zorder=3))
                label_at = center
                obstacle_drawings.append({"id": o["id"], "type": "circle", "center_mm": center,
                                          "radius_mm": o["radius"] * sx})
            if labels and not raw:
                self.text(*label_at, o["id"], 7.2, bold=True, ha="center", owner=panel_id)
        goal = world(scene["goal"])
        # Fixed scene-space glyph dimensions keep the raw observations and
        # their scaled vector depictions registered. Glyph radii do not give
        # the point agent or point goal a physical collision radius.
        self.ax.add_patch(Polygon(star_vertices(*goal, .23*sx), closed=True,
                                  facecolor=COL["goal_fill"], edgecolor=COL["goal"], lw=.7, zorder=7))
        if candidate:
            cid = candidate["id"]
            states = candidate["states"]
            painted = [world(p) for p in states]
            self.line(painted, cid, 1.25 if cid == "L" else 1.05, (0, (3.0, 2.0)), z=5)
            for i, p in enumerate(painted):
                if i == len(painted) - 1:
                    continue
                self.ax.add_patch(Circle(p, .73, facecolor=COL["white"], edgecolor=COL[cid], lw=1, zorder=7))
            # This cross is generated from the actual AABB intersection interval.
            for segment in candidate["segments"]:
                for test in segment["obstacles"]:
                    if test["hit"] and test.get("interval") is not None:
                        a, b = np.asarray(segment["from"]), np.asarray(segment["to"])
                        mid_t = sum(test["interval"]) / 2
                        cx, cy = world(a + mid_t * (b - a))
                        self.line([(cx-.95, cy-.95), (cx+.95, cy+.95)], cid, 1.6, z=8)
                        self.line([(cx-.95, cy+.95), (cx+.95, cy-.95)], cid, 1.6, z=8)
            if indices:
                offsets = {
                    "D": [(0, -2.8), (0, 2.8), (0, 2.8), (0, 2.8), (0, -2.8)],
                    "U": [(0, 2.8), (-.4, -2.8), (0, -2.8), (3, .1), (0, -2.8)],
                    "L": [(0, -2.8), (-.4, 3), (0, 3), (0, 3), (0, -2.8)],
                }
                for i, ((px, py), (dx, dy)) in enumerate(zip(painted, offsets[cid])):
                    self.text(px+dx, py+dy, str(i), 7.2, cid, ha="center", owner=panel_id)
        agent = world(scene["agent"]["position"])
        if transition:
            old = world(transition["from"])
            self.ax.add_patch(Circle(old, .8, facecolor=COL["white"], edgecolor=COL["muted"], lw=.75, zorder=7))
            self.arrow(old, agent, "L", lw=1.6, scale=8, label="executed first action")
            self.text(old[0]-.4, old[1]-2.9, "p₀", 7.2, ha="center", owner=panel_id)
            self.text(agent[0]+2.6, agent[1]-.2, "p₁", 7.2, "L", bold=True, ha="center", owner=panel_id)
        else:
            self.ax.add_patch(Circle(agent, .14*sx, facecolor=COL["ink"], edgecolor=COL["white"], lw=.65, zorder=8))
        if transition:
            self.ax.add_patch(Circle(agent, .95, facecolor=COL["L"], edgecolor=COL["white"], lw=.7, zorder=8))
        if labels and not candidate and not transition and not raw:
            self.text(agent[0], agent[1]-3.2, "p₀", 7.6, bold=True, ha="center", owner=panel_id)
            self.text(goal[0], goal[1]-3.2, "g", 7.6, "goal", bold=True, ha="center", owner=panel_id)
        if axes:
            for vx in (xmin, (xmin+xmax)/2, xmax):
                tx, ty = world((vx, ymin))
                self.line([(tx, ty), (tx, ty+.7)], "wall", .5)
                self.text(tx, ty+2.9, f"{vx:g}", 7.2, "muted", ha="center", owner=panel_id)
            for vy in (ymin, (ymin+ymax)/2, ymax):
                tx, ty = world((xmin, vy))
                self.line([(tx, ty), (tx-.6, ty)], "wall", .5)
                self.text(tx-1.3, ty, f"{vy:g}", 7.2, "muted", ha="right", owner=panel_id)
        self.maps.append({"id": panel_id, "rect_mm": [x,y,w,h], "world_bounds": bounds,
                          "scale_mm_per_unit": [sx,sy], "agent_world": scene["agent"]["position"],
                          "agent_mm": agent, "obstacles": obstacle_drawings,
                          "trajectory_world": candidate["states"] if candidate else None,
                          "trajectory_mm": [world(p) for p in candidate["states"]] if candidate else None})
        return world

    def geometry_report(self):
        self.fig.canvas.draw()
        renderer = self.fig.canvas.get_renderer()
        boxes = []
        for i, item in enumerate(self.text_items):
            b = item["artist"].get_window_extent(renderer)
            mm = self.ax.transData.inverted().transform([[b.x0,b.y0], [b.x1,b.y1]])
            x0, x1 = sorted(mm[:,0]); y0, y1 = sorted(mm[:,1])
            boxes.append({"id":i, "text":item["text"], "font_pt":item["size_pt"], "owner":item["owner"],
                          "bounds_mm":[float(x0),float(y0),float(x1),float(y1)]})
        overlap = []
        for i, a in enumerate(boxes):
            for b in boxes[i+1:]:
                a0,a1,a2,a3=a["bounds_mm"]; b0,b1,b2,b3=b["bounds_mm"]
                dx=min(a2,b2)-max(a0,b0); dy=min(a3,b3)-max(a1,b1)
                if dx > .08 and dy > .08:
                    overlap.append({"a":a["text"],"b":b["text"],"overlap_mm":[dx,dy]})
        outside = [b for b in boxes if b["bounds_mm"][0] < 0 or b["bounds_mm"][1] < 0 or
                   b["bounds_mm"][2] > self.width or b["bounds_mm"][3] > self.height]
        return {"text_bounds":boxes, "pairwise_text_overlap":overlap, "outside_canvas":outside,
                "maps":self.maps,"connectors":self.connectors,
                "limits":"Text rectangles are conservative. Spatial labels intentionally annotate scene objects. Arbitrary mark occlusion requires visual review."}


def fmt(x):
    return f"{x:g}".replace("-", "−")


def make_observation(out, scene, name):
    # Actual raster observation, without labels or trajectories. The plate adds
    # vector annotations using the same scene renderer and exactly the same state.
    p = Plate(100,60)
    p.scene(0,0,100,60,scene,labels=False,raw=True,panel_id=name)
    p.fig.savefig(out / f"{name}.png", dpi=152.4, facecolor="white", metadata={"Software":"deterministic scene renderer"})
    plt.close(p.fig)


def render(out, fixture_path=None):
    out.mkdir(parents=True, exist_ok=True)
    fixture_path=Path(fixture_path or HERE/"scene_fixture.json")
    fixture=load_fixture(fixture_path)
    data=rollout(fixture)
    results={r["id"]:r for r in data["candidates"]}
    (out / "computed_rollouts.json").write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    with style_context(7.6):
        p=Plate()
        p.text(4,6.8,"Scene-grounded planning with swept-path checks",10.7,bold=True)
        p.text(4,12.6,"DETERMINISTIC ILLUSTRATIVE SIMULATION  ·  point agent  ·  exact scene state",7.5,"muted")
        p.line([(4,16),(174,16)],lw=.8)
        p.heading(4,21,"a","One fixture binds the observation, task, and planner input")
        p.text(7,26,"Rendered observation o₀ = R(s₀)",7.6,bold=True)
        p.scene(7,30,60,36,fixture["scene"],panel_id="a_observation",axes=True)
        p.text(7,73,"Same coordinates in every scene view",7.2,"muted")

        # Literal scene record with a strong left rule, rather than another box.
        p.line([(79,28),(79,50)],"ink",1.3)
        p.text(82,29.8,"Explicit state s₀",8.3,bold=True)
        origin,goal=fixture["scene"]["agent"]["position"],fixture["scene"]["goal"]
        p.text(82,36.1,f"p₀ = ({fmt(origin[0])}, {fmt(origin[1])})      g = ({fmt(goal[0])}, {fmt(goal[1])})",7.8,mono=False)
        A,B=fixture["scene"]["obstacles"]
        p.text(82,42.2,f"{A['name']} A: [{A['bounds'][0]:g}, {A['bounds'][1]:g}] × [{A['bounds'][2]:g}, {A['bounds'][3]:g}]",7.5)
        p.text(82,48.3,f"{B['name']} B: center ({B['center'][0]:g}, {B['center'][1]:g}), r = {B['radius']:g}",7.5)
        p.arrow((77,36.1),(69,36.1),"muted",label="state to deterministic rendering")
        p.text(73,31.8,"R",7.5,"muted",ha="center")
        p.line([(82,53),(174,53)],lw=.5)
        p.text(82,57.8,"Task from the same fixture",8.0,bold=True)
        p.text(82,63.8,data["task"],7.6)
        p.text(82,72.2,"Planner reads s₀ directly; no learned perception.",7.2,"muted")
        p.line([(4,76),(174,76)],lw=.6)

        p.heading(4,81,"b","Roll out three candidate action sequences")
        p.text(4,87.1,f"pₖ₊₁ = pₖ + aₖ   ·   Δt = {fixture['dynamics']['dt']:g}   ·   ‖aₖ‖₂ ≤ {fixture['dynamics']['max_action_norm']:g}   ·   H = {fixture['dynamics']['horizon']}",7.8)
        p.text(174,87.1,"Dashes: simulated motion",7.2,"muted",ha="right")

        for idx,cid in enumerate(("D","U","L")):
            left=4+58*idx
            r=results[cid]
            p.rect(left,92.1,54,3.7,f"{cid}_pale")
            p.text(left+1,94,cid,8.5,cid,bold=True)
            p.text(left+7.2,94,r["name"],8.0,cid,bold=True)
            p.scene(left+2,99,50,30,fixture["scene"],candidate=r,indices=True,panel_id=f"b_{cid}")
            p.text(left+2,133.7,"k",7.2,"muted")
            p.text(left+2,138.7,"aₓ",7.3,"muted")
            p.text(left+2,143.7,"aᵧ",7.3,"muted")
            for k,a in enumerate(r["actions"]):
                xx=left+15+10.5*k
                p.text(xx,133.7,str(k),7.2,"muted",ha="center")
                p.text(xx,138.7,fmt(a[0]),7.3,ha="center")
                p.text(xx,143.7,fmt(a[1]),7.3,ha="center")
            p.rect(left,147,54,7.3,f"{cid}_pale")
            p.text(left+2,150.6,f"C={r['collision']}   E={r['effort']:.2f}   J={r['cost']:.3f}",7.35,cid,bold=(cid==data["selected_id"]))

        p.heading(4,160,"c","Test the swept path and minimize J")
        horizon_sub=str(fixture['dynamics']['horizon']).translate(str.maketrans('0123456789','₀₁₂₃₄₅₆₇₈₉'))
        p.text(4,166.4,f"J = ‖p{horizon_sub} − g‖₂² + {fixture['objective']['effort_weight']:.2f}E + {fixture['objective']['collision_penalty']:g}C",7.8)
        p.text(4,172,"E = Σₖ‖aₖ‖₂²; C = 1 for any swept collision.",7.4)

        # Exact magnification of the direct candidate's colliding segment. The
        # obstacle and all interval endpoints are derived from the numeric test.
        hit_segment=next(s for s in results["D"]["segments"] if s["collision"])
        hit_test=next(t for t in hit_segment["obstacles"] if t["hit"])
        pp,qq=np.asarray(hit_segment["from"]),np.asarray(hit_segment["to"])
        t0,t1=hit_test["interval"]
        lo,hi=pp+t0*(qq-pp),pp+t1*(qq-pp)
        zoom_x,zoom_y,zoom_w,zoom_h=6,178,48,13
        p.rect(zoom_x,zoom_y,zoom_w,zoom_h,"floor")
        zx=lambda xx: zoom_x+(xx-(pp[0]-.2))/(qq[0]-pp[0]+.4)*zoom_w
        zy=zoom_y+zoom_h/2
        p.rect(zx(lo[0]),zoom_y,zx(hi[0])-zx(lo[0]),zoom_h,"obstacle","obstacle_edge",.6,z=3,hatch="///")
        p.line([(zx(pp[0]),zy),(zx(qq[0]),zy)],"D",1.2,(0,(3,2)),z=5)
        p.line([(zx(lo[0]),zy),(zx(hi[0]),zy)],"D",2.8,z=6)
        for endpoint,label in ((pp,"p₁"),(qq,"p₂")):
            xx=zx(endpoint[0])
            p.ax.add_patch(Circle((xx,zy),.8,facecolor="white",edgecolor=COL["D"],lw=1,zorder=7))
            p.text(xx,zy+4.6,label,7.2,"D",ha="center")
        p.text((zx(lo[0])+zx(hi[0]))/2,zoom_y+2.3,"A",7.2,bold=True,ha="center")
        p.text(62,180.0,f"D: ({pp[0]:g}, {pp[1]:g}) → ({qq[0]:g}, {qq[1]:g})",7.4,"D",bold=True)
        p.text(62,185.5,f"t ∈ [{t0:.2f}, {t1:.2f}] lies inside A.",7.2)
        p.text(62,191.0,"Free endpoints; colliding segment.",7.2)
        p.rect(4,195.5,111,5.8,"L_pale")
        selected=results[data["selected_id"]]
        terminal_errors=[r['terminal_squared_distance'] for r in data['candidates']]
        if not np.allclose(terminal_errors,terminal_errors[0],atol=1e-12,rtol=0):
            raise ValueError('This composition requires a shared terminal-error summary; revise the label for this fixture.')
        p.text(6,198.4,f"argmin J = {selected['id']} ({selected['cost']:.3f}); all terminal errors = {terminal_errors[0]:g}.",7.5,"L",bold=True)

        p.line([(118,159),(118,201)],"rule",.55)
        p.heading(122,160,"d","Execute one step")
        a=data["executed_action"]; q=data["next_state"]["agent"]["position"]
        p.text(122,166.3,f"L: a₀ = ({fmt(a[0])}, {fmt(a[1])})",7.5,"L",bold=True)
        p.text(122,171.5,f"p₁ = ({fmt(q[0])}, {fmt(q[1])})",7.5)
        p.scene(125,176,43,25.8,data["next_state"],panel_id="d_observation",transition={"from":fixture['scene']['agent']['position']})
        # The footer is intentionally placed above the mini-map: it labels the
        # observation as the available input to a new planning cycle.
        # Replanning is not simulated a second time in this fixture.
        p.text(174,171.5,"o₁ → replan",7.2,"muted",ha="right")

        report=p.geometry_report()
        (out / "geometry_audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
        if report["outside_canvas"]:
            raise ValueError(f"Text outside canvas: {report['outside_canvas']}")
        files=export_figure(p.fig,out/"scene_planning_figure",source_files=[fixture_path,HERE/"scene_model.py",HERE/"render_figure.py",HERE/"figure_style.py"],
                            metadata={"data_status":"deterministic illustrative simulation", "claim":"Exactly tested finite-candidate planning and execution of one action",
                                      "minimum_authored_font_pt":7.2,"scene_coordinates":"dimensionless", "horizon":fixture["dynamics"]["horizon"],
                                      "font_programs":{"regular":REGULAR,"bold":BOLD,"monospace":MONO},
                                      "scene_fixture_sha256":hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
                                      "scope":"No learned perception, model training, empirical benchmark, or real-agent evaluation claim."},dpi=300)
        plt.close(p.fig)
        make_observation(out,fixture["scene"],"observation_o0")
        make_observation(out,data["next_state"],"observation_o1")
    print(json.dumps({"files":files,"selected":data["selected_id"],
                      "costs":{k:r["cost"] for k,r in results.items()},
                      "text_overlap_count":len(report["pairwise_text_overlap"])},indent=2))


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=HERE)
    parser.add_argument("--fixture",type=Path,default=HERE/"scene_fixture.json")
    args=parser.parse_args()
    render(args.out.resolve(),args.fixture.resolve())
