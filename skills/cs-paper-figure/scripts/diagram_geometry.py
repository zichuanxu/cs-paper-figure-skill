"""Check explicit orthogonal diagram routes before drawing them.

Coordinates are Cartesian: x grows rightward and y grows upward.  ``Rect``
bounds, route points, label bounds, and ``clearance`` must use the same unit.
Use the *visible* node boundary (including any drawing-library box padding).
Only register real nodes as obstacles; a group enclosure that intentionally
contains a route is not an obstacle node.

Example::

    nodes = [Node("agent", Rect(20, 20, 50, 40)),
             Node("tool", Rect(70, 20, 90, 40))]
    source = Port("tool", "top", .5, kind="observation")
    target = Port("agent", "top", .8, kind="observation")
    route = Route("return", source, target,
                  (port_point(source, nodes), (80, 50), (44, 50),
                   port_point(target, nodes)), kind="observation")
    report = validate_diagram(nodes, [route], clearance=1, units="mm")
    assert report.passed, report.to_dict()

This checks the declared geometry, not a rendered image.  It does not measure
text, inspect glyphs, reserve arrowhead footprints, or prove that every visual
collision is absent.  Supply measured label rectangles and then inspect the
actual final-size export.  Curved or diagonal routes need another checker.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Iterable, Literal, Mapping, Sequence

Point = tuple[float, float]
Side = Literal["left", "right", "bottom", "top"]


@dataclass(frozen=True)
class Rect:
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    def expanded(self, amount: float) -> "Rect":
        return Rect(self.x0 - amount, self.y0 - amount,
                    self.x1 + amount, self.y1 + amount)


@dataclass(frozen=True)
class Node:
    id: str
    rect: Rect


@dataclass(frozen=True)
class Port:
    node_id: str
    side: Side
    offset: float = .5
    kind: str = "data"


@dataclass(frozen=True)
class Route:
    id: str
    source: Port
    target: Port
    points: Sequence[Point]
    kind: str = "data"
    # Prefer an allowed_junctions point for a single intentional junction.
    # A pair permission is broader: all intersections for the named pair.
    allow_crossings_with: Sequence[str] = ()


@dataclass(frozen=True)
class Label:
    id: str
    rect: Rect


@dataclass(frozen=True)
class GeometryIssue:
    code: str
    message: str
    route_id: str | None = None
    segment_index: int | None = None
    node_id: str | None = None
    label_id: str | None = None
    other_route_id: str | None = None
    location: object | None = None
    details: dict = field(default_factory=dict)


@dataclass
class GeometryReport:
    issues: list[GeometryIssue]
    allowed_contacts: list[dict]
    units: str
    clearance: float
    tolerance: float

    @property
    def passed(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "issue_count": len(self.issues),
            "issues": [asdict(x) for x in self.issues],
            "allowed_contacts": self.allowed_contacts,
            "coordinate_system": "Cartesian: x rightward, y upward",
            "units": self.units,
            "label_route_clearance": self.clearance,
            "tolerance": self.tolerance,
            "limitations": (
                "Checks declared axis-aligned rectangles and orthogonal polyline "
                "centerlines only. Does not measure text or rendered box padding, "
                "arrowheads, stroke footprints, curves, clipping, color contrast, "
                "scientific semantics, or all possible visual collisions. The "
                "actual final-size export still requires visual inspection."
            ),
        }


def _valid_rect(r: Rect) -> bool:
    return (all(isfinite(x) for x in (r.x0, r.y0, r.x1, r.y1))
            and r.x0 < r.x1 and r.y0 < r.y1)


def _node_map(nodes: Iterable[Node] | Mapping[str, Rect | Node]) -> dict[str, Node]:
    if isinstance(nodes, Mapping):
        return {key: value if isinstance(value, Node) else Node(key, value)
                for key, value in nodes.items()}
    return {node.id: node for node in nodes}


def port_point(port: Port,
               nodes: Iterable[Node] | Mapping[str, Rect | Node]) -> Point:
    """Resolve a port; offset runs low-to-high along the selected boundary.

    For left/right, offset 0 is bottom and 1 is top.  For top/bottom,
    offset 0 is left and 1 is right.  Invalid declarations raise ValueError
    (or KeyError for an unknown node); validate_diagram reports them instead.
    """
    r = _node_map(nodes)[port.node_id].rect
    if not _valid_rect(r) or not isfinite(port.offset) or not 0 <= port.offset <= 1:
        raise ValueError("Port needs a valid node rectangle and offset in [0, 1].")
    if port.side == "left":
        return (r.x0, r.y0 + port.offset * r.height)
    if port.side == "right":
        return (r.x1, r.y0 + port.offset * r.height)
    if port.side == "bottom":
        return (r.x0 + port.offset * r.width, r.y0)
    if port.side == "top":
        return (r.x0 + port.offset * r.width, r.y1)
    raise ValueError(f"Unknown port side: {port.side!r}")


def _close(a: Point, b: Point, tol: float) -> bool:
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


def _orientation(a: Point, b: Point, tol: float) -> str | None:
    if _close(a, b, tol):
        return "zero"
    if abs(a[1] - b[1]) <= tol:
        return "horizontal"
    if abs(a[0] - b[0]) <= tol:
        return "vertical"
    return None


def _segment_rect(a: Point, b: Point, r: Rect, tol: float):
    """Return (contact kind, contact endpoints) for an orthogonal segment."""
    orient = _orientation(a, b, tol)
    if orient == "horizontal":
        y = (a[1] + b[1]) / 2
        lo, hi = max(min(a[0], b[0]), r.x0), min(max(a[0], b[0]), r.x1)
        if y < r.y0 - tol or y > r.y1 + tol or lo > hi + tol:
            return None
        endpoints = ((lo, y), (hi, y))
        boundary = abs(y - r.y0) <= tol or abs(y - r.y1) <= tol
    elif orient == "vertical":
        x = (a[0] + b[0]) / 2
        lo, hi = max(min(a[1], b[1]), r.y0), min(max(a[1], b[1]), r.y1)
        if x < r.x0 - tol or x > r.x1 + tol or lo > hi + tol:
            return None
        endpoints = ((x, lo), (x, hi))
        boundary = abs(x - r.x0) <= tol or abs(x - r.x1) <= tol
    else:
        return None
    if hi - lo <= tol:
        return ("touch", endpoints)
    return ("border" if boundary else "interior", endpoints)


def _segment_intersection(a: Point, b: Point, c: Point, d: Point, tol: float):
    o1, o2 = _orientation(a, b, tol), _orientation(c, d, tol)
    if o1 not in ("horizontal", "vertical") or o2 not in ("horizontal", "vertical"):
        return None
    if o1 != o2:
        h0, h1, v0, v1 = (a, b, c, d) if o1 == "horizontal" else (c, d, a, b)
        p = ((v0[0] + v1[0]) / 2, (h0[1] + h1[1]) / 2)
        if (min(h0[0], h1[0]) - tol <= p[0] <= max(h0[0], h1[0]) + tol
                and min(v0[1], v1[1]) - tol <= p[1] <= max(v0[1], v1[1]) + tol):
            return ("point", (p,))
        return None
    fixed, varying = (1, 0) if o1 == "horizontal" else (0, 1)
    if abs(a[fixed] - c[fixed]) > tol:
        return None
    lo = max(min(a[varying], b[varying]), min(c[varying], d[varying]))
    hi = min(max(a[varying], b[varying]), max(c[varying], d[varying]))
    if lo > hi + tol:
        return None
    p, q = list(a), list(a)
    p[varying], q[varying] = lo, hi
    return ("point", (tuple(p),)) if hi - lo <= tol else ("overlap", (tuple(p), tuple(q)))


def _normal_ok(a: Point, b: Point, side: Side, outward: bool, tol: float) -> bool:
    dx, dy = b[0] - a[0], b[1] - a[1]
    normal = {"left": (-1, 0), "right": (1, 0),
              "bottom": (0, -1), "top": (0, 1)}[side]
    dot = dx * normal[0] + dy * normal[1]
    tangential = abs(dy) if normal[0] else abs(dx)
    return tangential <= tol and (dot > tol if outward else dot < -tol)


def validate_diagram(
    nodes: Iterable[Node] | Mapping[str, Rect | Node],
    routes: Sequence[Route],
    labels: Sequence[Label] = (),
    allowed_junctions: Sequence[Point] = (),
    clearance: float = 1.0,
    tolerance: float = 1e-6,
    units: str = "diagram units",
) -> GeometryReport:
    """Report port, route, node, label-clearance, and crossing defects.

    Clearance is a conservative axis-aligned padding around label rectangles.
    It applies to route centerlines; callers must include visible stroke and
    arrowhead space when choosing it. Shared endpoint ports are accepted;
    collinear shared segments are not accepted implicitly. Intentional point
    junctions may be listed explicitly. A route-pair permission is broader and
    should be used sparingly; all accepted contacts remain in the report.
    """
    if not isfinite(clearance) or clearance < 0:
        raise ValueError("clearance must be a finite nonnegative number")
    if not isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be a finite positive number")
    issues: list[GeometryIssue] = []
    contacts: list[dict] = []
    report = GeometryReport(issues, contacts, units, clearance, tolerance)
    raw_nodes = list(nodes.values()) if isinstance(nodes, Mapping) else list(nodes)
    node_map = _node_map(nodes if isinstance(nodes, Mapping) else raw_nodes)
    if len(raw_nodes) != len(node_map):
        issues.append(GeometryIssue("duplicate_node_id", "Node IDs must be unique."))
    for node in node_map.values():
        if not _valid_rect(node.rect):
            issues.append(GeometryIssue("invalid_node_rect", "Node rectangle must be finite with positive width and height.", node_id=node.id, details={"rect": asdict(node.rect)}))
    if len({r.id for r in routes}) != len(routes):
        issues.append(GeometryIssue("duplicate_route_id", "Route IDs must be unique."))
    if len({label.id for label in labels}) != len(labels):
        issues.append(GeometryIssue("duplicate_label_id", "Label IDs must be unique."))
    good_labels = []
    for label in labels:
        if _valid_rect(label.rect):
            good_labels.append(label)
        else:
            issues.append(GeometryIssue("invalid_label_rect", "Label rectangle must be finite with positive width and height.", label_id=label.id, details={"rect": asdict(label.rect)}))
    junctions = []
    for p in allowed_junctions:
        if len(p) == 2 and all(isfinite(x) for x in p):
            junctions.append(tuple(p))
        else:
            issues.append(GeometryIssue("invalid_junction", "Allowed junctions must be finite coordinate pairs.", location=p))
    segments = []
    resolved: dict[tuple[int, str], Point] = {}
    for route_index, route in enumerate(routes):
        points = route.points
        if len(points) < 2 or any(len(p) != 2 or not all(isfinite(x) for x in p) for p in points):
            issues.append(GeometryIssue("invalid_route_points", "Route needs at least two finite coordinate pairs.", route_id=route.id))
            continue
        for role, port, actual in (("source", route.source, points[0]), ("target", route.target, points[-1])):
            try:
                expected = port_point(port, node_map)
                resolved[(route_index, role)] = expected
            except (KeyError, ValueError) as exc:
                issues.append(GeometryIssue("invalid_port", f"Invalid {role} port: {exc}", route_id=route.id, node_id=port.node_id, details={"role": role, "port": asdict(port)}))
                continue
            if port.kind != route.kind:
                issues.append(GeometryIssue("port_kind_mismatch", f"{role} port kind and route kind differ.", route_id=route.id, node_id=port.node_id, details={"role": role, "port_kind": port.kind, "route_kind": route.kind}))
            if not _close(actual, expected, tolerance):
                issues.append(GeometryIssue("endpoint_off_port", f"Route {role} does not meet its declared boundary port.", route_id=route.id, node_id=port.node_id, location=tuple(actual), details={"role": role, "expected": expected, "offset": (actual[0]-expected[0], actual[1]-expected[1])}))
            a, b = (points[0], points[1]) if role == "source" else (points[-2], points[-1])
            if not _normal_ok(a, b, port.side, role == "source", tolerance):
                issues.append(GeometryIssue("source_not_outward_normal" if role == "source" else "target_not_inward_normal", f"The {role} segment must be perpendicular to the declared boundary and point {'outward' if role == 'source' else 'inward'}.", route_id=route.id, node_id=port.node_id, location=(tuple(a), tuple(b)), details={"side": port.side}))
        for i, (a, b) in enumerate(zip(points, points[1:])):
            orient = _orientation(a, b, tolerance)
            if orient is None or orient == "zero":
                issues.append(GeometryIssue("nonorthogonal_segment" if orient is None else "zero_length_segment", "Every route segment must be nonzero and horizontal or vertical.", route_id=route.id, segment_index=i, location=(tuple(a), tuple(b))))
                continue
            segments.append((route_index, i, tuple(a), tuple(b)))
            for node in node_map.values():
                if not _valid_rect(node.rect):
                    continue
                hit = _segment_rect(a, b, node.rect, tolerance)
                if hit is None:
                    continue
                kind, pts = hit
                legitimate_source = (kind == "touch" and i == 0 and node.id == route.source.node_id and (route_index, "source") in resolved and _close(pts[0], resolved[(route_index, "source")], tolerance))
                legitimate_target = (kind == "touch" and i == len(points)-2 and node.id == route.target.node_id and (route_index, "target") in resolved and _close(pts[0], resolved[(route_index, "target")], tolerance))
                if legitimate_source or legitimate_target:
                    continue
                code = {"border": "route_rides_node_border", "interior": "route_enters_node", "touch": "unexpected_node_touch"}[kind]
                issues.append(GeometryIssue(code, "A route must use its declared endpoint ports and must not ride or pass through another node boundary/interior.", route_id=route.id, segment_index=i, node_id=node.id, location=pts, details={"node_is_endpoint": node.id in (route.source.node_id, route.target.node_id), "contact": kind}))
            for label in good_labels:
                hit = _segment_rect(a, b, label.rect.expanded(clearance), tolerance)
                if hit is not None:
                    issues.append(GeometryIssue("label_route_clearance", "Route intersects the label box or its requested clearance margin.", route_id=route.id, segment_index=i, label_id=label.id, location=hit[1], details={"label_rect": asdict(label.rect), "clearance": clearance}))
    seen_contacts = set()
    for index, (ri, si, a, b) in enumerate(segments):
        r1 = routes[ri]
        for rj, sj, c, d in segments[index+1:]:
            r2 = routes[rj]
            hit = _segment_intersection(a, b, c, d, tolerance)
            if hit is None:
                continue
            kind, pts = hit
            if ri == rj and abs(si-sj) == 1 and kind == "point":
                continue  # Ordinary bend in one polyline.
            key = (ri, rj, kind, tuple(tuple(round(v / tolerance) for v in p) for p in pts))
            if key in seen_contacts:
                continue
            seen_contacts.add(key)
            reason = None
            if ri != rj and (r2.id in r1.allow_crossings_with or r1.id in r2.allow_crossings_with):
                reason = "explicit route-pair permission"
            elif kind == "point" and any(_close(pts[0], p, tolerance) for p in junctions):
                reason = "explicit junction"
            elif ri != rj and kind == "point":
                for role1, port1 in (("source", r1.source), ("target", r1.target)):
                    for role2, port2 in (("source", r2.source), ("target", r2.target)):
                        if (port1 == port2 and (ri,role1) in resolved and (rj,role2) in resolved
                                and _close(pts[0], resolved[(ri,role1)], tolerance)
                                and _close(pts[0], resolved[(rj,role2)], tolerance)):
                            reason = "shared declared endpoint port"
            if reason:
                contacts.append({"routes": [r1.id, r2.id], "segments": [si,sj], "kind": kind, "location": pts, "permission": reason})
            else:
                issues.append(GeometryIssue("route_self_intersection" if ri == rj else "unexpected_route_intersection", "Route contact needs an explicit junction or allowed route pair; collinear overlap is not implicitly a junction.", route_id=r1.id, segment_index=si, other_route_id=r2.id, location=pts, details={"other_segment": sj, "contact": kind}))
    return report
