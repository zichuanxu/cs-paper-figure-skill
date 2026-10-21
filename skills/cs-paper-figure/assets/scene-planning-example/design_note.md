# Design note

## Claim, scope, and panel contract

**Claim:** this deterministic fixture makes finite-candidate planning auditable: shared scene state, explicit actions, swept collision tests, a declared cost, and a single executed transition agree numerically and visually. It is an illustration of computation, not evidence of perception accuracy, learned dynamics, real-agent performance, or general planning optimality.

| Panel | Reader's question | Concrete object and conclusion | Cross-panel identity |
|---|---|---|---|
| a | What exactly is observed and supplied to the planner? | A rendered 2D scene sits beside the literal geometric state and a task generated from it. The planner reads exact state. | `s₀`, `o₀`, `p₀`, `g`, Barrier A, Pier B |
| b | What do the three proposals do? | Registered scene views show actual computed trajectories, with every action component in aligned indexed rows. | Candidates D, U, L; states 0–4; identical A/B/g |
| c | Why is the chosen proposal preferred? | The cost is declared, and one collision is enlarged with its exact segment parameter interval. L has the smallest displayed cost. | D's segment 1→2; C, E, J; selected L |
| d | What changes in the environment now? | Exactly the first selected action moves the agent. The new scene observation is available to begin another cycle. | L's action 0; `p₁`; `o₁` |

The overall computation is state/task → three nominal rollouts → swept tests and score → finite-set argmin → first-action collision guard → one transition → render/replan. Only the first iteration is simulated. The first-segment guard does not claim to certify all possible future horizons.

## Original composition

Two materially different compositions were considered: a central planner node surrounded by input/output objects, and a vertically read scene-and-proof plate. The chosen plate gives each kind of explanation its appropriate geometry: an asymmetric scene/record pairing, three truly parallel candidate views, a local spatial magnification, and a compact executed-state view. The largest repeated objects are scenes, not empty computational boxes. Literal controls, cost values, and the interval proof supply the mechanism detail.

The 178 × 203 mm artwork uses a 4 mm primary outer grid, 4 mm candidate gutters, and a narrow divider between the proof and execution panels. The three compared candidate scenes are each 50 × 30 mm, with identical 10 × 6 coordinate bounds and isotropic 5 mm/unit scale. The initial scene is larger; the executed-state scene is smaller. Those views explain different roles rather than a controlled size comparison; their extents and spatial proportions remain identical.

Cross-panel identifiers carry computation without long leader arrows cutting through scenes. The actual state-to-render dependency has a short leftward R arrow. The only solid motion arrow is the executed first step. Dashed trajectories are explicitly defined as simulated motion. The crossing of D through A is intended scientific geometry, not an accidental connector collision.

## Visual system

| Role | Ink / mark | Pale fill or geometry |
|---|---|---|
| Primary text / exact state | `#233746` | White background; literal record marked by a left rule |
| Secondary text | `#536572` | Thin neutral rules `#BBC5CB` |
| Direct candidate D | `#AE403B` | `#FBEFEC`; collision cross and explicit C=1 |
| Upper candidate U | `#7255A1` | `#F3EFF9`; explicit U label |
| Lower candidate L | `#087C78` | `#E8F5F1`; bold cost and selected statement |
| Obstacles | `#6A7780` outline | `#C7CDD0`; rectangle hatching and circular geometry remain distinct in grayscale |
| Goal | `#A96C0C` outline | `#F8D988`; star glyph is separate from trajectory state markers |
| Scene floor | Neutral grid `#E4E4DF` | `#F7F6F0` |

Color identifies candidate identity consistently; it is not a quantitative scale. Direct labels, letter IDs, collision flags, hatching, shapes, and a textual selection statement provide redundancy. The palette has been inspected in grayscale. A dedicated color-vision simulation was not run.

DejaVu Sans uses real regular and bold TrueType programs. Title: 10.7 pt; panel letters/headings: 9.3/9.0 pt; object headings: 8.0–8.5 pt; ordinary labels: 7.4–7.8 pt; minimum details: 7.2 pt. The PDF embeds the subset font programs. The SVG retains editable text and therefore depends on an available DejaVu Sans font for faithful editing. No synthetic bold or CFF-as-TrueType mismatch is used.

Scene walls/obstacles use 0.65 pt strokes; grid lines use 0.28 pt; candidate trajectories use 1.05–1.25 pt; the executed arrow uses 1.6 pt. Marker and goal glyph sizes are visual annotations for point locations, not physical collision radii.

## Inspected source principles

Only transferable composition principles were adapted. No source artwork, photographs, logos, traced lettering, model architecture, or empirical numbers are reproduced.

1. **[DreamDojo, version 1, Figure 1, PDF page 3](https://arxiv.org/pdf/2602.06949v1):** the actual figure crop was inspected. Its asymmetric areas give different explanatory levels different visual scales, and concrete scene imagery carries the application story. This informed the unequal observation/record/proof/execution regions here. The source uses many photographic objects and training stages; those are not part of this deterministic simulation.
2. **[Cosmos Policy, version 1, Figure 2, PDF page 4](https://arxiv.org/pdf/2601.16163v1):** the actual figure crop was inspected. Registered visual slots remain aligned with representation rows. Here, each candidate's scene is tied to exact action-component rows, and all candidate scenes use the same world-to-canvas transform. The source's latent-frame architecture and conditioning/noising semantics are not borrowed.

The skill's supplementary `visual-objects.md` study was read after the initial composition was selected. It reinforced shared fixtures, repeated landmarks, and distinct observation/prediction/execution status. The color tokens, fonts, dimensions, and layout of this plate are new design choices; they are not claims of measured source style.

## Scientific integrity and checks

All scene geometry, state positions, action values, collision marks, objective values, and selection labels are generated from `scene_fixture.json`. `computed_rollouts.json` preserves every swept segment and obstacle test. The initial and next observations are actual 600 × 360 deterministic renderings. Their pixel difference is confined to the old and new point-agent glyphs; landmarks and goal remain unchanged.

The rectangle uses a slab intersection algorithm. The circle uses closest-point projection. Validation independently checks all 24 segment/obstacle pairs using segment/rectangle-edge intersection and line/circle quadratic roots, respectively. Boundary and zero-length tests cover inclusive collision semantics. The direct collision's interval is [0.20,0.80], while both segment endpoints are free. The nominal direct rollout continues past that collision only for scoring and display.

E means **quadratic control effort**, not physical energy. The finite cost penalty selects L for this fixture; it does not imply a hard feasibility constraint in general. Validation includes a separate low-penalty counterexample that selects a nominally colliding horizon while its first segment is still safe. A second guard check verifies that an unsafe first action is blocked. Those validation fixtures do not enter the displayed result.

Export checks confirm one 178 × 203 mm vector PDF page, no embedded raster images, two embedded TrueType font programs, minimum nominal label size 7.2 pt, 123 editable SVG text elements, and a 2102 × 2397 PNG at nominal 300 dpi. All plotted world coordinates are invertibly checked against the fixture; every map uses isotropic scale. Measured text boxes have zero pairwise overlaps and zero canvas escapes. Scene bounds include their border stroke footprint. A second renderer, Poppler, generates the reviewed PDF preview.

## Caption budget and remaining limits

The artwork remains at 178 mm width and 203 mm height. The separate short caption is intended for manuscript placement; the extended caption is companion explanation, not a mandatory page footprint. `manuscript_placement_preview.png` places the artwork and short caption on a 210 × 250 mm review page with 3 mm caption gap, 8 pt caption text, and 10 pt leading. `placement_report.json` records the measured line count and total vertical budget. This proof does not claim conformance with a particular venue template.

The repeated candidate views use the same scale, but the initial and executed observation views have different display sizes. Labels and point glyphs are annotation, not camera measurements. The geometry tests establish consistency of this exact fixture; they do not establish real-world dynamics or safety. No unmodeled sensing error, uncertainty, control noise, or collision avoidance beyond the tested first action is asserted.
