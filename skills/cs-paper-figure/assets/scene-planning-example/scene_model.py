"""Exact, deterministic fixture rollout and closed-set collision tests.

All coordinates are dimensionless. The point agent follows piecewise-linear
motion between sampled states; an endpoint-only test is deliberately inadequate.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import numpy as np

TOL = 1e-12


def segment_aabb(p, q, bounds):
    """Closed segment/rectangle intersection, with its [t_enter,t_exit]."""
    p, q = np.asarray(p, float), np.asarray(q, float)
    d = q - p
    lo = np.array([bounds[0], bounds[2]], float)
    hi = np.array([bounds[1], bounds[3]], float)
    t0, t1 = 0.0, 1.0
    for j in range(2):
        if abs(d[j]) <= TOL:
            if p[j] < lo[j] - TOL or p[j] > hi[j] + TOL:
                return {"hit": False, "interval": None}
        else:
            a, b = sorted(((lo[j] - p[j]) / d[j], (hi[j] - p[j]) / d[j]))
            t0, t1 = max(t0, a), min(t1, b)
            if t0 > t1 + TOL:
                return {"hit": False, "interval": None}
    return {"hit": True, "interval": [float(t0), float(t1)]}


def segment_circle(p, q, center, radius):
    """Closest-point projection onto a closed segment, including zero length."""
    p, q, center = np.asarray(p, float), np.asarray(q, float), np.asarray(center, float)
    d = q - p
    dd = float(np.dot(d, d))
    t = 0.0 if dd <= TOL else float(np.clip(np.dot(center - p, d) / dd, 0.0, 1.0))
    closest = p + t * d
    distance = float(np.linalg.norm(closest - center))
    return {"hit": bool(distance <= radius + TOL), "t_closest": t,
            "closest": closest.tolist(), "distance_to_center": distance,
            "clearance": distance - radius}


def inside_bounds(p, bounds):
    return bool(bounds[0] - TOL <= p[0] <= bounds[1] + TOL and
                bounds[2] - TOL <= p[1] <= bounds[3] + TOL)


def rollout(fixture):
    scene, dynamics = fixture["scene"], fixture["dynamics"]
    p0, goal = np.asarray(scene["agent"]["position"], float), np.asarray(scene["goal"], float)
    task = fixture["task_template"].format(**{
        f"obstacle_{i}": o["name"] for i, o in enumerate(scene["obstacles"])})
    results = []
    for candidate in fixture["candidates"]:
        actions = np.asarray(candidate["actions"], float)
        if actions.shape != (dynamics["horizon"], 2):
            raise ValueError("Every candidate must have H two-dimensional actions")
        norms = np.linalg.norm(actions, axis=1)
        if np.any(norms > dynamics["max_action_norm"] + TOL):
            raise ValueError(f"Action limit exceeded by {candidate['id']}")
        states = np.vstack([p0, p0 + np.cumsum(actions * dynamics["dt"], axis=0)])
        segments = []
        for k, (p, q) in enumerate(zip(states[:-1], states[1:])):
            tests = []
            for obstacle in scene["obstacles"]:
                if obstacle["type"] == "aabb":
                    test = segment_aabb(p, q, obstacle["bounds"])
                elif obstacle["type"] == "circle":
                    test = segment_circle(p, q, obstacle["center"], obstacle["radius"])
                else:
                    raise ValueError("Unknown obstacle geometry")
                tests.append({"obstacle_id": obstacle["id"], **test})
            # The room is convex, so segment containment is equivalent to both
            # endpoints lying within the closed room bounds.
            within = inside_bounds(p, scene["bounds"]) and inside_bounds(q, scene["bounds"])
            segments.append({"k": k, "from": p.tolist(), "to": q.tolist(),
                             "obstacles": tests, "within_room": within,
                             "collision": bool(any(t["hit"] for t in tests) or not within)})
        E = float(np.sum(actions ** 2))
        terminal_error = float(np.sum((states[-1] - goal) ** 2))
        C = int(any(s["collision"] for s in segments))
        J = terminal_error + fixture["objective"]["effort_weight"] * E + fixture["objective"]["collision_penalty"] * C
        results.append({"id": candidate["id"], "name": candidate["name"],
                        "actions": actions.tolist(), "states": states.tolist(),
                        "action_norms": norms.tolist(), "segments": segments,
                        "terminal_squared_distance": terminal_error,
                        "effort": E, "collision": C, "cost": float(J)})
    selected = min(results, key=lambda r: r["cost"])
    if selected["segments"][0]["collision"]:
        raise ValueError("Selected first action is unsafe; execution is blocked")
    next_state = copy.deepcopy(scene)
    next_state["agent"]["position"] = selected["states"][1]
    return {"fixture_id": fixture["id"], "task": task, "candidates": results,
            "selected_id": selected["id"], "executed_action": selected["actions"][0],
            "initial_state": scene, "next_state": next_state,
            "executed_action_count": 1,
            "unexecuted_selected_actions": selected["actions"][1:]}


def load_fixture(path=None):
    return json.loads(Path(path or Path(__file__).with_name("scene_fixture.json")).read_text())


if __name__ == "__main__":
    print(json.dumps(rollout(load_fixture()), indent=2, allow_nan=False))
