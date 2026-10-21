# Visual objects inside rich method figures

Use this reference when a figure combines scenes, frames, spatial relations, token structures or persistent visual memory with a method overview. Six already-catalogued figures were visually reinspected on 2026-10-21; this deepens their design evidence without increasing the corpus count. Source artwork is not included in the skill.

## Contents

- Evidence and scope
- Six close readings: Cosmos Policy, WorldPlay, GR00T N1, Wan-Animate-2, Gemini Robotics, SAM 3
- Reusable rules for original visual objects
- Two full-width composition patterns
- Implementation and delivery contract

## Evidence and scope

**Observed** describes the reopened crop. **Catalog-measured** identifies the existing PDF inspection record returned by `scripts/reference_catalog.py show <paper-id> --figure <n>`; these measurements were not independently re-extracted here. **Estimated** describes approximate visual proportions, not segmented artwork area. **Recommended** describes choices for an original figure, not measurements of a source.

| Source anchor | Catalog-measured selected crop | Strongest lesson |
|---|---|---|
| [Cosmos Policy, Fig. 2, PDF p. 4](https://arxiv.org/pdf/2601.16163v1) | 398 × 159 pt; aspect 2.503 | Align concrete views with representation slots through successive transformations. |
| [WorldPlay, Fig. 2, PDF p. 4](https://arxiv.org/pdf/2512.14614v1) | 496 × 198 pt; aspect 2.505 | Repeated scene views connect transient calls with persistent history. |
| [GR00T N1, Fig. 2, PDF p. 3](https://arxiv.org/pdf/2503.14734v2) | 487 × 260 pt; aspect 1.873 | Modalities have both concrete input exemplars and persistent token identities. |
| [Wan-Animate-2, Fig. 1, PDF p. 5](https://arxiv.org/pdf/2608.06009v1) | 473 × 313.2 pt; aspect 1.510 | Let the overview, representation, and operator use different spatial grammars. |
| [Gemini Robotics, Fig. 1, PDF p. 2](https://arxiv.org/pdf/2503.20020v1) | 475 × 282 pt; aspect 1.684 | Observable task examples can frame a compact system story. |
| [SAM 3, Fig. 10, PDF p. 19](https://arxiv.org/pdf/2511.16719v1) | 473 × 228 pt; aspect 2.075 | Repeated token objects and memory stacks connect overview and mechanism. |

These are manually selected source regions, not automatic artwork bounds. Reopened raster sizes, directly read from image metadata, are respectively 1194 × 477, 1488 × 594, 1461 × 780, 1419 × 940, 1425 × 846, and 1419 × 684 pixels. The sources and figure records are already in `dense-expansion-index.json` or `recent-expansion-index.json`.

## Six close readings

### 1. Cosmos Policy: a visual ledger whose columns remain stable

**Observed.** The dominant objects are square camera crops, short diagonal frame stacks, and synthetic modality tiles. The top row presents multiview images; the middle row inserts proprioception, action, and value slots; the bottom row exposes which slots receive noise. Within each colored field, camera identities stay in their columns. The wrist view remains tightly centered on the manipulated object; external views retain the robot and supporting surface. Changes between present and future are therefore legible without a new viewing convention.

**Estimated area and hierarchy.** The conditioning field takes about two-fifths and the target field about three-fifths of the colored content width, consistent with four versus six displayed slots. A slim left margin holds transformation labels. This is a data-object-led composition: labels and arrows occupy gaps around a large aligned object grid, rather than placing the objects inside oversized model boxes.

**Color and typography.** Two pale backgrounds encode conditioning versus target status. A dark red outline and red labels identify injected modalities. The stronger red does not fill every slot. Catalog-rendered samples are `#F1FFE8`, `#F8E1DB`, and `#A62C17`; the original alpha is unknown. Sans-serif prose and italic mathematical group labels are visible, but the figure is raster and exact fonts and point sizes are not established.

**Original vector transfer.** Draw a reusable scene once and render a wrist crop plus two fixed external views from it. Use those same view objects across rows. Make added action/state/value content visibly nonphotographic: a small numeric vector, joint-angle glyph, or scalar tile can explain representation without impersonating an image. Draw brackets, column labels, noising texture, and injection routes as precise vector elements. Keep the same coordinates before and after a transformation. The source does not justify implying that proprioception is literally a photograph.

### 2. WorldPlay: scene recurrence makes memory visible

**Observed.** Two near-identical temporal-call compositions sit over one long memory ribbon. Road images retain the same horizon and scene family, while viewpoint changes provide the temporal signal. Two enlarged retrieved views sit inside a red dashed selection group in each call. The small thumbnails in memory use the same landscape aspect ratio. Repetition is explanatory: a reader can see which old visual content is recovered and where a decoded result is written back.

**Estimated area and hierarchy.** The shared model strip is only about one-tenth of crop height. The memory ribbon takes roughly one-sixth at the bottom. Most remaining area belongs to view selections, action-conditioning objects, and the two repeated calls. The title bar is wide, but is not the largest area-consuming component.

**Orientation, detail, and routes.** Thumbnails face the page; mild perspective is inside the depicted scene. A simple planar arrow and a wireframe spatial icon communicate the two action representations without detailed equipment illustration. Blue update paths descend outside the local objects; red retrieval paths rise from memory. Direct labels provide a local key. The color samples in the catalog are rendered `#5480AD` for the model spine and `#C25759` for memory/reconstitution; native opacity and lettering metrics are unavailable.

**Original vector transfer.** Build a sparse road or room from a ground plane, a few landmarks, a camera position, and a trajectory. Render two or three matched view frames with stable camera framing. Place the same selected frames in both the cache and the retrieval group. Use separate read and write routes. If calls are sequential, label that fact; a shared horizontal model bar alone can otherwise suggest simultaneous computation.

### 3. GR00T N1: concrete modalities become token objects

**Observed.** A landscape observation, a literal language instruction, and a compact annotated body schematic form three input lanes. The first two become colored token columns before entering a tall vision-language module. State tokens bypass that module and enter the diffusion module. Action-token columns change from very pale to saturated orange along a separate denoising direction. The final humanoid figure is a standalone output object on white, rather than another card.

**Estimated area and hierarchy.** The concrete input objects occupy roughly the left quarter of the width. The two model modules are large, but token strips sit at their boundaries and the state bypass remains visually open. The figure spends considerable space on module interiors; a denser new figure can shorten those modules while preserving the three modality lanes.

**Sparse detail and typography.** Four state callouts identify joints, base position, velocity, and end-effector pose. They explain what the body contributes; they do not attempt a complete anatomy. Catalog-measured source labels include approximately 7.24 pt Arial, 9.34 pt bold module text, 10.36 pt system labels, and 5.21 pt small state labels. These describe the source, not recommended production minima. The literal instruction uses a monospaced face.

**Opacity matters.** Image-token fill is catalog-measured as raw `#9C2FE5` at alpha 0.5176. Clean action tokens use `#FF9900` at alpha 1; the noisy action variant uses the same raw orange at alpha 0.1569. These are not interchangeable with opaque raw hex colors. A new figure should use verified composites or deliberate opaque tints on a known background, and retain a denoising label because pale color alone is ambiguous.

**Original vector transfer.** A simple original articulated figure with a few labeled joints is sufficient. Repeated, aligned token rectangles can carry modality identity through the whole architecture. Use a small set of state marks and a short control vector rather than adding a decorative robot rendering. Do not copy the source robot, input photograph, or typography as artwork.

### 4. Wan-Animate-2: three levels of explanation, three kinds of geometry

**Observed.** The left overview runs from reference/target frames through a dual-branch model to output frames. The top-right explanation is a spatial-temporal arrangement of rounded token tiles; the bottom-right is a sparse-access matrix. A vertical divider and a horizontal divider establish separate reading scales. The top panels show explicit references and target frames before any abstract tensor geometry appears.

**Estimated proportion.** The left overview occupies a little over half the crop width; the right-hand mechanisms occupy the remainder in roughly equal-height panels. This corrects an overstrong reading of the existing prose that the right mechanisms are intrinsically wider than the left overview. The useful rule is asymmetric sizing by explanatory need, not a fixed left/right ratio.

**Object orientation and sparse detail.** The token arrangement uses front-facing rounded squares with consistent diagonal offsets for depth. It does not require photorealistic cubes. Horizontal, vertical, and diagonal dimension arrows establish W, H, and T. Ellipses compress repeated positions. The attention matrix has named query and key/value directions, visible computed cells, explicit blank cells, and a two-state legend. Only the example windows needed to reveal the pattern are drawn.

**Color and lettering.** Render-sampled colors include denoising yellow `#FFE699`, reference-video blue `#9DC3E6`, reference-image green `#A9D18E`, and computed-attention green `#97D34F`; their native alpha is unknown. The raster combines serif operator labels, italic mathematics, and bold sans-serif panel headings. It does not establish exact font families.

**A source limitation to improve.** Cross-panel color is not a perfect one-to-one identifier: green represents a reference-image token above and attention computation below; both ordinary and reference x labels use yellow circles in the matrix. Do not claim that every color carries identical semantics across panels. In an original figure, keep modality colors stable and use a separate neutral or patterned fill for computed edges, or explicitly scope the local matrix legend.

**Original vector transfer.** Draw token tiles from one parameterized primitive, with a shared depth vector and repeat spacing. Derive the attention matrix from an explicit Boolean relation, then label its row and column objects. Match operator names between the overview and detail. Preserve exact counts only when supplied by the method; schematic repeats and ellipses are not measured tensor dimensions.

### 5. Gemini Robotics: example objects frame a compact method

**Observed.** Four equal photo cards above and four below frame a central training/adaptation chain. A narrower right column shows specialization outcomes. Top cards pair instructions with robot-task views. Bottom cards contain concrete point, box, and orientation overlays on varied scenes. Those overlays, rather than extra paragraphs, communicate the different output types.

**Estimated proportion and crop discipline.** The main area occupies about four-fifths of total width; the outcome column about one-fifth. Upper and lower evidence bands are each roughly one-third of crop height, with the compact method band between them. Equal card widths, stable image heights, and matched caption bars keep heterogeneous scenes comparable. Camera viewpoints differ across capabilities, so the figure does not imply that all cards are matched experimental trials.

**Color and typography.** Saturated blue model blocks (`#1B6EF3`, catalog-measured opaque source fill) carry the main identity. Pale blue capability surrounds and gray process grounds remain subordinate. Dark gray caption bars supply stable contrast over photographic material. The underlying family of the source's Type 3 font is unidentified; source captions around 5.39 pt are a warning to shorten or enlarge new captions.

**Original vector transfer.** Replace the montage with a smaller set of original schematic scenes tied to actual method outputs: a camera view with projected points, a second view with corresponding landmarks, and a plan view with a path. Keep every small scene's crop and caption placement consistent. A new full-width method figure generally needs fewer examples than this source: the examples must explain inputs or outputs, not make an unmeasured capability claim. Logos and source photos contribute no reusable geometry.

### 6. SAM 3: token rows and stacked memory inside a scoped expansion

**Observed.** A smaller recurrent system on the left expands into a larger detector region on the right. Repeated circular query tokens and hidden states share positions and shapes. A separate presence token uses another color. The memory bank is a small stack with offset sheets. These compact objects make hidden structure visible without turning every state into another large text box.

**Estimated proportion and legend.** The expanded region takes a little over half the total width. The left-bottom whitespace houses a three-item component-provenance legend. The legend explains fill categories, while token labels and grouping boundaries explain the local objects; these are separate roles.

**Visual hierarchy.** Pale yellow novel modules, pale blue inherited modules, and teal encoder modules sit under dark lettering. Gray routes recede relative to the objects. The catalog records opaque yellow fill `#FDF5AD`, blue fill `#CDE5F7`, teal fill `#C6E8E8`, and route gray `#A7B3BF`. Lettering is outlined, so visible typeface and point size are unknown. Repeated token counts are schematic unless the paper explicitly gives their mapping.

**Original vector transfer.** Reuse a query-token primitive and a memory-stack primitive. Name the same operation in the overview and the expanded panel. Give the novel mechanism enough room for its actual ports and internal relations. Use scope boundaries rather than a fan of zoom leaders. Keep component provenance, modality identity, and runtime status as separate encodings; one color legend cannot silently mean all three.

## Reusable rules for original visual objects

1. **Make one scene yield several representations.** A room plan, a perspective camera frame, a path, a patch grid, and a latent strip can share object identifiers. This creates semantic density without adding prose. Cosmos Policy and WorldPlay are the strongest precedents.
2. **Choose the viewpoint that explains the relation.** Use an oblique scene for camera/trajectory geometry, front-facing cards for correspondences, and orthographic token arrays for tensor indexing. Avoid decorative perspective in every object.
3. **Preserve landmarks and crop composition.** A landmark repeated across views must retain its identifier, shape, and relative scene role. Background texture is expendable; the object that makes correspondence inspectable is not.
4. **Use detail sparsely and precisely.** A few projected points, a short labeled trajectory, one camera frustum, three displayed time steps, or a small attention window can explain an operation. Tiny unlabeled meshes and random matrices only create texture.
5. **Use tints for grouping and strong ink for relations.** The sources often keep large fields pale, then reserve saturated color for token roles, model identity, or selected operations. Specify which one a color means. Source alpha must not be guessed from a rendered RGB sample.
6. **Render all new labels and geometry as vector.** Original scenes can be built from polygons, polylines, paths, and repeated primitives. Use real user-provided raster frames only when they are actual evidence. Keep schematic examples explicitly labeled and distinguish them from results.

## Two strong full-width composition patterns

### Pattern A — scene overview, token representation, operator detail

**Recommended starting geometry:** a 178 × 108 mm canvas, with about 46% width for a full-height overview and 54% for two stacked detail panels. These are new design recommendations, not source measurements.

The overview starts with an original oblique room or road scene containing a short trajectory, two labeled camera poses, and two or three landmarks. Immediately below it, matched front-facing view cards show what those cameras observe. Compact encoding and prediction stages lead to future-view cards. Keep the original spatial scene large enough to see the camera-to-object relation; the model itself can be a short band with named ports.

The upper-right panel turns those same views into a time-by-view token arrangement and a separate action/state strip. Reuse view identifiers and timestamps. Show only enough repeated tiles to establish indexing, with dimensional annotations for any omitted extent. The lower-right panel expands one named operation as an exact attention/access mask or a projection-and-gather construction. Its rows and columns reuse the same object identifiers. A local legend states computed/blocked or observed/predicted semantics.

This combines Wan-Animate-2's explanatory scales, Cosmos Policy's aligned representation, and GR00T's stable modality tokens. It is strongest when the scientific contribution lies in representation construction or a novel multimodal operator. The final dimensions and dependencies must come from the actual method; label a demonstration as schematic if no empirical instance is supplied.

### Pattern B — repeated world-model calls above a scene-linked memory ribbon

**Recommended starting geometry:** a 178 × 96 mm canvas. Reserve roughly 76% width for two temporal calls and 24% for a compact mechanism detail. Give the bottom fifth of the main area to persistent memory. These are starting allocations, not source statistics.

Each call uses the same internal layout: a current scene frame, a short action/pose glyph, selected past-view cards, a compact model band, and a decoded future frame. Label the calls with consecutive time intervals and state that they use shared weights. A thin spatial trajectory above the calls places their camera poses in one common scene. The trajectory should identify which pose produced each displayed frame.

The bottom ribbon contains a few meaningful stored views, with time gaps shown explicitly. Reuse the exact same original vector scene crops when a memory item is enlarged above. Retrieval paths rise from selected cells; update paths return outside the call interiors to new cells. A right-side inset shows the actual retrieval relation: a small pose-distance sketch, a view-overlap test, or an explicit token window, depending on the method. That inset must add mechanism, rather than repeat the architecture.

This combines WorldPlay's separation of calls and persistence, Gemini Robotics' concrete scene evidence, and SAM 3's compact state objects. It is strongest when the contribution concerns long-horizon consistency, state reuse, or world-model control. A clear sequential-call label and separate read/write routes prevent the large model or memory bands from introducing incorrect execution semantics.

## Implementation and delivery contract

Preserve a single scene or case fixture behind the visible objects. For scenes, record geometry, units, object IDs, fixed viewport/camera, candidate controls and sampling times. Derive predicted states, collisions, costs, selected candidates and the executed transition from that fixture. Keep compared views registered; do not change camera, crop or object scale to make the selected candidate appear better. For an artifact update, record the matched case outputs, the update rule, the context diff and the proposal that consumes it.

Distinguish the status of each object: supplied observation, simulator-rendered observation, hypothetical rollout, executed step, literal record or schematic latent. Colored tiles do not establish actual token counts or a learned encoding. An original rendered scene can illustrate a method, but it must not impersonate photographic results or measured generalization.

Treat line semantics separately. A trajectory crossing an obstacle may be an intentional failed candidate; a control-flow connector cutting through an unrelated module is a layout defect. Record and check the intended data intersection, while still reviewing arrow attachment and routing. Draw rejected rollouts beyond collision only if their counterfactual continuation is part of the stated rule.

Check painted scene bounds as well as text bounds. A map border whose centerline sits on the page edge loses half its stroke even when every label is inside the page; include half the border width in containment checks. Audit point/state labels against obstacle labels and neighboring path labels in each view. Move the annotation while preserving the scientific point coordinate. A clean panel grid does not detect an ambiguous in-scene label overlap.

For small frame sequences, keep essential labels outside the images, use a shared camera and explicit timestamps, and show a few meaningful states. If frames cannot be read at the final physical width, show fewer larger frames or a larger linked detail. Decorative texture and undocumented ellipses cannot substitute for a visible transition.

## Packaging boundary

Transfer the composition rules, source citations, and newly authored vector primitives. Do not package any source screenshot, source crop, paper photograph, logo, outlined source lettering, or traced source-specific illustration. An original scene may share generic geometry such as a ground plane, camera frustum, or token lattice, but should be authored to explain the new method and retain its own editable construction.
