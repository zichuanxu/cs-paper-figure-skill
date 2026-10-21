# Diagram routing and geometry review

## The concrete failure this prevents

The earlier demonstration sent a dashed observation path from near the Tools top edge to a point above the controller's upper-right corner. The automatically chosen bend ran almost along the Tools border; the target was not a declared controller port. The path's direction was visible, but its attachment and route were ambiguous. A no-overflow PDF check could not detect this.

Use explicit typed ports and reserve a corridor. For a tool-feedback loop, place call ports on the lower horizontal lane; leave Tools through a north port, rise into a free outer corridor, turn toward the controller, and enter its north or upper-east port normally. Place the observation label beside the free corridor. Do not use a hand-tuned arc whose bend depends on near-collinear endpoints.

## Geometry contract

- Store node rectangles in final-size coordinates. Separate semantic nodes from visual group containers; edges can legitimately cross a group boundary.
- Define each port by node ID, side, fractional offset, and edge kind. Port offsets refer to the actual painted bounds, including any box padding.
- Make the first segment point outward from the source and the last segment point inward to the target.
- Keep arrowhead tips at the target boundary and long enough to show direction. Avoid excessive automatic endpoint shrink that makes arrows float.
- Route orthogonal polylines in free corridors. A curve can be appropriate, but then inspect/control its extrema, endpoint tangents, and clearance; the bundled checker covers orthogonal segments only.
- Never ride along a node border. An edge may touch its own endpoint at one intended point; it must not travel along that boundary.
- Avoid nonendpoint node intersections and unintended route crossings. Declare an intended junction explicitly. A route crossing exception is documentation, not permission to make an ambiguous picture.
- Keep labels and their white backing away from all unrelated routes. Check label rectangles after text rendering, not from character-count guesses.
- Distinguish source/target direction, data/control/feedback/update meaning, and train/inference scope. A missing or extra arrow changes the scientific model.

## Bundled helper

Use `scripts/diagram_geometry.py` to validate declared rectangle/port/polyline geometry. It does not depend on Matplotlib. It reports concrete coordinates for bad ports, non-normal entry/exit, border riding, nonendpoint intersections, label clearance, overlapping routes, and undeclared crossings.

Read the module's dataclass definitions before constructing inputs. The coordinate system is Cartesian with y increasing upward; use the same final-size unit for every rectangle, route, label and clearance. Only semantic nodes should enter its node list, not background group regions that contain the nodes. The actual renderer must use those same bounds and points; validating one geometry and rendering another proves nothing.

Validation is a targeted safeguard, not a complete layout solver. Curves, round-corner tangencies, stroke widths, arrowhead extents, occlusion, rasterized content, and scientific semantics still need inspection. The checker is most useful when the renderer preserves the declared geometry and reports measured text bounds.

## Visual acceptance

Inspect the exported vector PDF at final size and zoom the densest route region. Trace every edge in the adjacency list with your eyes. Confirm that labels attach to the intended route, arrowheads do not hide under fills, and the routing remains understandable in grayscale. Check that the fixed return path is separated from both the call path and the node outline.
