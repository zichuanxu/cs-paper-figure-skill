# Recent Google, Meta and NVIDIA figure studies

**12 new papers/reports; 26 actual inspected figure anchors; 8 papers from 2025 and 4 from 2026.**

This is a design study, not a venue ranking. Dates use first arXiv submission. Source point sizes are observations, not recommendations. Raw transparent fills retain their alpha. Type 3 identifiers, outlined glyphs, and hidden search text are not promoted to identified visible font families.

## Contents

- [Gemma 3 Technical Report](#gemma3)
- [Gemma 4 Technical Report](#gemma4)
- [AlphaEvolve: A coding agent for scientific and algorithmic discovery](#alphaevolve)
- [Gemini Robotics: Bringing AI into the Physical World](#gemini-robotics)
- [DINOv3](#dinov3)
- [SAM 3: Segment Anything with Concepts](#sam3)
- [Perception Encoder: The best visual embeddings are not at the output of the network](#perception-encoder)
- [Efficient Universal Perception Encoder](#eupe)
- [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](#gr00t-n1)
- [Cosmos-Reason1: From Physical Common Sense To Embodied Reasoning](#cosmos-reason1)
- [Nemotron 3 Super: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning](#nemotron3-super)
- [Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding](#nemotron-diffusion)
- [Transferable design recipes](#transferable-design-recipes)

<a id="gemma3"></a>
## Gemma 3 Technical Report

**Google / DeepMind | 2025 | arXiv:2503.19786v1**

[Primary PDF](https://arxiv.org/pdf/2503.19786v1) · [Record](https://arxiv.org/abs/2503.19786v1)

PDF p1 names Gemma Team, Google DeepMind. Header report date 2025-03-12; arXiv submission 2025-03-25.

PDF SHA-256: `b2793d288d6672f8d6a03f65370bb4a48d607f54937a22fc7d9f727435795305`

### Figure 2 — Paired model-family capability radars

**PDF page 6; family: paired small multiples.** Actual crop inspected at 216 dpi.

**Color roles.**
- Gemma 2 comparison trace: `#E94335`, alpha 1; raster_sampled.
- Gemma 3 comparison trace: `#4267D1`, alpha 1; raster_sampled.

**Typography.**
- Figure labels: unidentified, size unverified, regular; visual_estimate. All three panels are embedded raster images. Visible labels are sans serif; no font family or point size is established by PDF text extraction.

**Layout.** Three equal radar panels in one row; each contains one model-size comparison. Six semantic axes are held in the same order. The small legends sit to the left of each radar, leaving the polygon interiors readable.

**Geometry and strokes.** The three raster placements are each 150.57 × 107.15 pt, with 11.96 pt horizontal gaps (measured image placements). The complete figure extends slightly beyond the nominal text column width.

**Routing.** No dataflow arrows. Circular and triangular markers add a second encoding beyond red/blue color.

**Transferable rules.**
- Repeat axis order and model color across size-specific panels.
- Pair comparable models within each panel; use marker shape in addition to hue.
- Place comparisons in small multiples rather than overlaying many model polygons.

**Do not copy blindly.**
- Radar area is not an aggregate performance measure. Axis ranges differ and must remain explicit.
- The source is raster and has tiny radial tick labels; produce editable vector marks and larger labels for a new figure.

### Figure 5 — Model versus KV-cache memory

**PDF page 7; family: stacked resource decomposition.** Actual crop inspected at 216 dpi.

**Color roles.**
- Model memory: `#E94335`, alpha 1; vector_measured.
- KV-cache memory: `#FABB04`, alpha 1; vector_measured.

**Typography.**
- Figure labels: unidentified, size unverified, regular; visual_estimate. Visible lettering is outlined. The nominal DejaVuSans 4.494 pt text is rendering-mode-3 search metadata and is not evidence of a visible embedded font.

**Layout.** A low, wide single-axis stacked bar chart. The red lower component is constant while the gold upper component changes, directly explaining where the resource saving comes from. A compact two-item legend occupies unused upper-right space.

**Geometry and strokes.** Selected crop 234 × 85 pt; bars use uniform widths and uniform categorical spacing. Source axis strokes are about 0.360 pt, with a 0.449 pt legend border.

**Routing.** No arrows. Shared bar baseline and component order carry the comparison.

**Transferable rules.**
- Use a fixed base component plus changing increment when the claim concerns a cost decomposition.
- Keep the component color and stack order constant.
- Write units in the axis title and include the controlled context condition in the caption.

**Do not copy blindly.**
- Do not stack incomparable quantities or conceal a changed denominator.
- The final source labels are small; simplify category labels or increase height instead of reproducing the source size.

<a id="gemma4"></a>
## Gemma 4 Technical Report

**Google / DeepMind | 2026 | arXiv:2607.02770v2**

[Primary PDF](https://arxiv.org/pdf/2607.02770v2) · [Record](https://arxiv.org/abs/2607.02770v2)

PDF p1 names Gemma Team, Google DeepMind. The inspected arXiv v2 was revised 2026-07-24; report header says 2026-06-19.

PDF SHA-256: `b20b25f18d76217d0c49c89f9ed1ffe3cf1912cd8ce710e1a325977653c7bfa6`

### Figure 1 — Multi-token-prediction drafter beside the main model

**PDF page 3; family: aligned architectural comparison.** Actual crop inspected at 216 dpi.

**Color roles.**
- Shared embeddings and output projection: `#D8EAD2`, alpha 1; raster_sampled. Representative dominant rendered green sample; JPEG/raster variation is present.
- MTP drafter layers: `#C9D9FA`, alpha 1; raster_sampled. Representative rendered blue sample; this is not a recovered authoring token.

**Typography.**
- Figure labels: unidentified, size unverified, regular; visual_estimate. The figure is rasterized. The visible labels are sans serif, mostly regular. Exact family, original size, and original stroke widths cannot be recovered from this PDF crop.

**Layout.** Three aligned bottom-to-top columns: one main model and two consecutive drafter steps. Identical embeddings, MTP levels and output layers align horizontally. Ellipses compress repeated backbone layers; compact trapezoids distinguish projection operations from rectangular repeated layers.

**Geometry and strokes.** The selected figure region is approximately 253 × 203 pt. Main-model gray, drafter blue and embedding green separate roles; red attention routes cross between columns and blue dashed activation paths run along their margins.

**Routing.** Black arrows show the main vertical path; blue dashed arrows show the drafter path; red dotted cross-column attention links are labeled. Repeated drafter steps share corresponding ports.

**Transferable rules.**
- Align repeated steps and corresponding operators so visual differences correspond to method differences.
- Use shape to distinguish projection/unembedding from repeated layers.
- Show exactly which state is reused through colored, labeled cross-column routes.

**Do not copy blindly.**
- The source has several diagonal attention crossings. Reserve a distinct cross-column corridor in a new diagram.
- Do not infer missing connections or freeze/train state from a color.
- Do not reuse the raster artwork when editable vector source can be built.

<a id="alphaevolve"></a>
## AlphaEvolve: A coding agent for scientific and algorithmic discovery

**Google / DeepMind | 2025 | arXiv:2506.13131v1**

[Primary PDF](https://arxiv.org/pdf/2506.13131v1) · [Record](https://arxiv.org/abs/2506.13131v1)

PDF p1 names Google DeepMind beneath the author list.

PDF SHA-256: `f092c8cbd65da89951ee6496374da9a54963f9035758c25ac6e4625f506df9ad`

### Figure 2 — Human configuration and distributed controller loop

**PDF page 4; family: code-linked system architecture.** Actual crop inspected at 216 dpi.

**Color roles.**
- Prompt sampler: `#4285F4`, alpha 1; vector_measured.
- LLM ensemble: `#EA4335`, alpha 1; vector_measured.
- Evaluators pool: `#FBBC04`, alpha 1; vector_measured.
- Program database: `#34A853`, alpha 1; vector_measured.
- Human setup background: `#E6F4EA`, alpha 1; vector_measured.
- System background: `#E8F0FE`, alpha 1; vector_measured.
- Neutral ink and routes: `#3C4043`, alpha 1; vector_measured.

**Typography.**
- Module labels and prose: GoogleSans-Regular, 8.783 pt, regular; vector_measured.
- Module labels and controller heading: GoogleSans-Bold, 8.783 pt, bold; vector_measured.
- Group headings: GoogleSans-Bold, 11.293 pt, bold; vector_measured.
- Controller pseudocode: GoogleSansMono-Regular, 8.783 pt, regular; vector_measured.
- Role-colored code identifiers: GoogleSansMono-Bold, 8.783 pt, bold; vector_measured.

**Layout.** A green-tinted human setup band sits above a blue-tinted system group. Four equal module columns connect vertically to their corresponding setup items. A wide pseudocode box below spans the modules. The module colors recur on matching identifiers inside the pseudocode; the final output sits outside the system group at the right.

**Geometry and strokes.** Primary module/routing strokes measure 0.941 pt; secondary dashed boundaries measure 0.511 pt. The controller occupies roughly the lower half of the system area (visual estimate). Module boxes are dashed; actual direction arrows are solid.

**Routing.** Vertical setup arrows descend into each module. Short bidirectional colored arrows join modules to the controller. Only the database has the right-facing export arrow to the final program.

**Transferable rules.**
- Bind pseudocode identifiers to diagram roles with exactly the same semantic palette.
- Separate human-provided configuration from automated execution through aligned spatial bands.
- Give code a real monospace companion with a matching x-height; keep prose and code hierarchy coherent.
- Place the final artifact outside the execution boundary.

**Do not copy blindly.**
- Yellow labels have low contrast on pale blue at small size; darken the label ink while keeping a yellow accent or fill.
- Bidirectional arrows should only represent genuinely bidirectional interfaces.
- Do not assume Google Sans is licensed or installed; use a verified substitute such as Arial or an installed open sans.

### Figure 3 — Input program, sampled prompt, and proposed code modification

**PDF page 6; family: asymmetric code storyboard.** Actual crop inspected at 216 dpi.

**Color roles.**
- Code card background: `#F7F7F7`, alpha 1; vector_measured.
- Function/class names: `#0000FF`, alpha 1; vector_measured.
- Python keywords: `#008000`, alpha 1; vector_measured.
- Comments: `#3D7A7A`, alpha 1; vector_measured.
- Strings: `#BA2121`, alpha 1; vector_measured.
- Ellipses and values: `#666666`, alpha 1; vector_measured.

**Typography.**
- Code: LMMono8-Regular, 6.575 pt, regular; vector_measured.
- Highlighted code: LMMonoLt10-Bold, 6.575 pt, bold; vector_measured.
- Code comments: LMMono10-Italic, 6.575 pt, italic; vector_measured.
- Panel letters: XCharter-Bold, 10.909 pt, bold; vector_measured.

**Layout.** Two columns use unequal vertical subdivision: two shorter code cards on the left, one tall prompt card on the right. The panel order is explicitly labeled (a), (b), (c), since spatial order alone would be ambiguous. Consistent neutral backgrounds and syntax colors distinguish code from the surrounding paper.

**Geometry and strokes.** Three borderless pale-gray rectangles carry the code. Large panel letters and small role icons sit below each card. Real line breaks, indentation, and ellipses preserve program structure.

**Routing.** No connecting arrows; panel labels and caption establish the input → prompt → edit sequence.

**Transferable rules.**
- Use unequal panel heights to fit actual content, while aligning column edges.
- Keep enough literal code to make the operation concrete, then elide irrelevant lines explicitly.
- Use panel labels when reading order differs from ordinary row-major order.

**Do not copy blindly.**
- The source code is only 6.575 pt at placement; a new figure should show fewer lines or more space.
- Avoid decorative role icons if the same distinction is already obvious from headings.
- Never let colored syntax substitute for an explanation of which lines changed.

### Figure 8 — Ablation trajectories over compute budget

**PDF page 18; family: paired step plots with uncertainty.** Actual crop inspected at 216 dpi.

**Color roles.**
- Full method: `#1A991A`, alpha 1; vector_measured.
- No evolution: `#0066CC`, alpha 1; vector_measured.
- No context: `#CC1A1A`, alpha 1; vector_measured.
- No full-file evolution: `#801ACC`, alpha 1; vector_measured.
- No meta-prompt evolution: `#FF8000`, alpha 1; vector_measured.
- Full-method band: `#99E599`, alpha 0.3; vector_measured. Raw band color at alpha 0.3 over white, not opaque displayed green. Background: White plotting field; overlapping uncertainty bands produce additional composites.
- Grid: `#B0B0B0`, alpha 0.6; vector_measured. Background: White plotting field; overlapping uncertainty bands produce additional composites.

**Typography.**
- Figure labels: unidentified, size unverified, regular; visual_estimate. The visible labels are vector outlines. DejaVuSans sizes in the hidden search layer are not used as visible font evidence.

**Layout.** Two equal-width plots share the normalized 0–100% compute-budget axis. The second panel includes only the relevant subset of ablations. Step-like mean trajectories sit on translucent standard-deviation bands. Titles name the problem, while axis labels name the measured quantity.

**Geometry and strokes.** Curve strokes measure about 0.748 pt; grid 0.498 pt; axis/tick strokes 0.199 pt. Bands have alpha 0.3. Legends are placed within low-occupancy lower-right regions. Y ranges intentionally differ between tasks.

**Routing.** No topology arrows. Legends maintain consistent method colors across panels, including methods omitted from one panel.

**Transferable rules.**
- Normalize the budget when comparing training/search trajectories across tasks.
- Keep uncertainty behind the mean, with explicitly documented interval meaning and run count.
- Match legend colors across panels even when a panel contains only a subset.

**Do not copy blindly.**
- Do not copy the source standard-deviation band into a new figure without its correct statistical meaning.
- Overlapping colored ribbons can become muddy; use fewer emphasized methods, lighter bands, or separate panels.
- The y ranges differ; do not imply equal magnitudes from aligned panel heights.

<a id="gemini-robotics"></a>
## Gemini Robotics: Bringing AI into the Physical World

**Google / DeepMind | 2025 | arXiv:2503.20020v1**

[Primary PDF](https://arxiv.org/pdf/2503.20020v1) · [Record](https://arxiv.org/abs/2503.20020v1)

PDF p1 names Gemini Robotics Team, Google DeepMind.

PDF SHA-256: `f2c1ab4e73a76013b9ebf5a4ff90bb3d291eee0730304d3ebf4531256a204b78`

### Figure 1 — Capabilities, training, and specialization overview

**PDF page 2; family: evidence-framed method overview.** Actual crop inspected at 216 dpi.

**Color roles.**
- Model blocks: `#1B6EF3`, alpha 1; vector_measured.
- Capability-chip surround: `#D0E4FF`, alpha 1; vector_measured.
- Process-group background: `#F2F2F2`, alpha 1; vector_measured.
- Photo caption bars: `#5E5E5E`, alpha 1; vector_measured.
- Main ink: `#202124`, alpha 1; vector_measured.

**Typography.**
- Visible figure text: embedded Type 3; family unidentified, 6.862 pt, regular; vector_measured. The PDF font is named Unnamed-T3. Its underlying commercial font family is not established.
- Small image captions: embedded Type 3; family unidentified, 5.392 pt, regular; vector_measured.
- Larger labels: embedded Type 3; family unidentified, 8.823 pt, regular; vector_measured.

**Layout.** A compact central training pipeline is framed by real task examples above and below. A narrower right column shows specialization outcomes. Photo cards use aligned crops and dark caption strips. Blue model blocks are visually heavier than the pale capability chips above them.

**Geometry and strokes.** The main evidence area is roughly four-fifths of the total width and the specialization column one-fifth (visual estimate). Thin, pale container boundaries group panels without competing with the photographs.

**Routing.** A single central left-to-right arrow sequence links base model, robotics training, adaptation and specialization. Photo grids are evidence groups rather than extra dataflow nodes.

**Transferable rules.**
- Use real outputs around a compact mechanism to connect abstract stages to observable capabilities.
- Keep photographic panels aligned and give all captions a stable contrast surface.
- Use saturated color for the model identities and pale tints for subordinate capabilities.

**Do not copy blindly.**
- A large montage can turn into a promotional overview; label example selection and distinguish examples from aggregate evidence.
- Do not reproduce corporate logos to imply authority.
- Source captions below 6 pt need enlargement or reduced text in a new paper figure.

### Figure 2 — Object, point, correspondence, and 3D grounding examples

**PDF page 3; family: qualitative capability grid.** Actual crop inspected at 216 dpi.

**Color roles.**
- Caption-strip overlay: `#000000`, alpha 0.6; vector_measured. Translucent overlay on photographs; observed background varies with image pixels. Background: Variable photograph pixels; no single opaque equivalent exists.
- Caption text: `#FFFFFF`, alpha 1; vector_measured.

**Typography.**
- Panel captions: GoogleSans-Regular, 7.173 pt, regular; vector_measured.

**Layout.** Three upper panels show distinct 2D tasks. The lower row contains one wide two-view correspondence example and one narrower 3D detection example. Each image has a bottom caption bar. The correspondence lines encode matched points directly; the 3D panel uses boxes with attached labels.

**Geometry and strokes.** White gutters separate image panels. The wider lower-left panel spans the first two columns, preserving the two-view relation without shrinking both views into one ordinary tile.

**Routing.** Correspondence connectors stay within their dedicated photographic panel. Detection boxes and point markers are data overlays, not process arrows.

**Transferable rules.**
- Allow a panel to span columns when the scientific relation requires multiple views.
- Keep captions outside the visually important image region or on an explicit contrast strip.
- Use point halos or outlines so markers remain visible on both dark and light imagery.

**Do not copy blindly.**
- Do not treat qualitative successes as representative without a stated selection rule.
- Avoid overlaying tiny labels everywhere; use numbered keys or an enlarged inset for dense scenes.
- The photo annotations are raster content; their source font identity is unavailable.

<a id="dinov3"></a>
## DINOv3

**Meta / FAIR | 2025 | arXiv:2508.10104v1**

[Primary PDF](https://arxiv.org/pdf/2508.10104v1) · [Record](https://arxiv.org/abs/2508.10104v1)

PDF p1 names Meta AI Research, WRI and Inria.

PDF SHA-256: `c68dc50b1f73e1641a592f777984fc360759e84b7fe65ac4f6e1377927f20b2e`

### Figure 5 — Dense-feature degradation beside task trajectories

**PDF page 10; family: qualitative-quantitative diagnostic pairing.** Actual crop inspected at 216 dpi.

**Color roles.**
- VOC trajectory: `#645FAA`, alpha 1; vector_measured.
- ImageNet trajectory: `#F05A93`, alpha 1; vector_measured.
- Grid: `#BFBFBF`, alpha 1; vector_measured.

**Typography.**
- Axes, legend and panel labels: LMRoman9-Regular, 8.966 pt, regular; vector_measured.
- Panel letters: LMRoman9-Bold, 8.966 pt, bold; vector_measured.

**Layout.** The left portion is a two-row grid of an input image and two training-time similarity maps. The right portion stacks two compact line plots, one per model size. The diagnostic images occupy about 60% of the width and the plots about 30%, with a generous gap for vertical model labels (visual estimate).

**Geometry and strokes.** Plot curves measure about 0.797 pt, major axes/grid about 0.399 pt, and thin ticks about 0.199 pt. The image grid uses almost no gutter so exact spatial correspondence remains obvious.

**Routing.** No process connectors. Panel labels and shared iteration values connect qualitative degradation to the training trajectories.

**Transferable rules.**
- Pair a diagnostic visualization with the metric that reveals its consequence.
- Align image variants tightly when the comparison is pixelwise.
- Use a serif figure family intentionally when the manuscript math and labels benefit from it.

**Do not copy blindly.**
- The source similarity panels have no visible common colorbar; add one when quantitative color comparison is claimed.
- Never imply that visually noisier maps alone establish a performance claim.
- Do not force identical y limits when the relevant trajectories have different meaningful ranges; label the distinction.

### Figure 9 — Qualitative resolution comparison with an ablation table

**PDF page 14; family: image-grid and exact-lookup pairing.** Actual crop inspected at 216 dpi.

**Color roles.**
- Table rules and labels: `#000000`, alpha 1; vector_measured.

**Typography.**
- Table and image labels: LMRoman9-Regular, 8.966 pt, regular; vector_measured.
- Best values: LMRoman9-Bold, 8.966 pt, bold; vector_measured.
- Panel captions: LMRoman10-Regular, 9.963 pt, regular; vector_measured.

**Layout.** A four-column, two-row image comparison sits beside a compact exact-value ablation table. The table has top, header and bottom rules but no vertical rules or cell shading. Best values are bold. Both sides share one overall top alignment and paired bottom captions.

**Geometry and strokes.** The left grid and right table each occupy nearly half the figure width (visual estimate). Table outer rules are 0.797 pt and the inner header rule 0.498 pt.

**Routing.** No arrows. The column labels establish resolution/downsampling conditions and the table gives precise consequences.

**Transferable rules.**
- Use a table alongside imagery when the reader needs exact values rather than a visual trend.
- Give boldface a precise meaning such as best measured value, and declare metric direction.
- Use a few horizontal rules to create a quiet table that does not compete with images.

**Do not copy blindly.**
- Do not use a multicolor table when there is no meaningful grouping.
- Avoid interpreting feature colors as semantic classes; these are visualizations of learned representations.
- Declare how similarity maps are normalized if comparing across rows or resolutions.

<a id="sam3"></a>
## SAM 3: Segment Anything with Concepts

**Meta / FAIR | 2025 | arXiv:2511.16719v1**

[Primary PDF](https://arxiv.org/pdf/2511.16719v1) · [Record](https://arxiv.org/abs/2511.16719v1)

PDF p1 names Meta Superintelligence Labs. Counted as 2025 by original arXiv submission; later revision is 2026.

PDF SHA-256: `876e138b0e07c57aaa251e1eea9fcaf0008a44987ebc48a075806bacc43894bc`

### Figure 4 — Detector, tracker, and memory overview

**PDF page 4; family: novelty-coded recurrent architecture.** Actual crop inspected at 216 dpi.

**Color roles.**
- New components fill: `#FDF5AD`, alpha 1; vector_measured.
- New components outline: `#FCDC30`, alpha 1; vector_measured.
- Inherited SAM 2 fill: `#CDE5F7`, alpha 1; vector_measured.
- Inherited SAM 2 outline: `#6C9FD5`, alpha 1; vector_measured.
- Perception Encoder fill: `#C6E8E8`, alpha 1; vector_measured.
- Perception Encoder outline: `#42BFB4`, alpha 1; vector_measured.
- Routes and scope boundaries: `#A7B3BF`, alpha 1; vector_measured.
- Label ink: `#1B2B33`, alpha 1; vector_measured.

**Typography.**
- Figure labels: unidentified, size unverified, regular; visual_estimate. Labels are outlined vector glyphs, not live text. They are visually sans serif; the original font family and point sizes are not established.

**Layout.** Parallel detection and tracking lanes meet at an explicit circled-plus merge. Text and image encoders are trapezoids, detector/tracker are rectangles, outputs are real frames with masks, and the memory bank is a repeated-card stack. A small legend explains component provenance.

**Geometry and strokes.** The diagram is wide and shallow. Primary routes and selected outlines measure about 1.304 pt; other outlines about 1.003 pt. A separate lower corridor carries the memory feedback edge.

**Routing.** Detection and propagated masks merge before output and memory update. A clean lower return path brings memory back to the tracker. Additional prompt input enters the tracker from below, with a distinct arrow endpoint.

**Transferable rules.**
- Encode new versus reused components with a source-specific provenance palette and an explicit legend.
- Use a distinct shape for stored state and a junction for actual combination.
- Reserve the return corridor before placing nodes and labels.

**Do not copy blindly.**
- The exact yellow/cyan/blue assignment belongs to this figure; do not invent a universal company style.
- A color used for novelty must not simultaneously mean modality or training state.
- Do not infer a merge or memory update that is absent from the described method.

### Figure 10 — System overview plus detector expansion

**PDF page 19; family: overview and scoped mechanism detail.** Actual crop inspected at 216 dpi.

**Color roles.**
- New components fill: `#FDF5AD`, alpha 1; vector_measured.
- New components outline: `#FCDC30`, alpha 1; vector_measured.
- Inherited SAM 2 fill: `#CDE5F7`, alpha 1; vector_measured.
- Inherited SAM 2 outline: `#6C9FD5`, alpha 1; vector_measured.
- Perception Encoder fill: `#C6E8E8`, alpha 1; vector_measured.
- Perception Encoder outline: `#42BFB4`, alpha 1; vector_measured.
- Routes and scope boundaries: `#A7B3BF`, alpha 1; vector_measured.
- Label ink: `#1B2B33`, alpha 1; vector_measured.

**Typography.**
- Figure labels: unidentified, size unverified, regular; visual_estimate. Outlined glyphs are visually sans serif. No visible text spans establish a font family or size.

**Layout.** The left section gives the recurrent system while the right, larger dashed rounded region expands detector internals. A consistent yellow new-module grammar links both scales. Repeated circular tokens express queries and hidden states; the memory bank remains a stacked object. The legend is tucked into unused lower-left space.

**Geometry and strokes.** Overview is about 45% and expanded detail about 55% of the width (visual estimate). Most route strokes are 1.305 pt, with about 1.004 pt boundaries. Dashed groups distinguish a set of tokens from a scoped subsystem.

**Routing.** Expansion is communicated through scope and corresponding labels, not a mass of zoom leader lines. Right-side feature inputs fan into decoder blocks using shared straight/curved lanes. The output route exits through a separate lower port.

**Transferable rules.**
- Give a novel operation more area than familiar context.
- Carry the same color, shapes and terminology from overview into expansion.
- Use compact token rows to expose hidden-state structure without listing dimensions everywhere.

**Do not copy blindly.**
- Do not let a dashed token group be mistaken for an execution boundary; label its role.
- Multiple curved routes still need edge-by-edge endpoint checks.
- Outlined source text should be recreated as editable text, not copied as paths.

<a id="perception-encoder"></a>
## Perception Encoder: The best visual embeddings are not at the output of the network

**Meta / FAIR | 2025 | arXiv:2504.13181v1**

[Primary PDF](https://arxiv.org/pdf/2504.13181v1) · [Record](https://arxiv.org/abs/2504.13181v1)

PDF p1 explicitly lists the five organizations and notes internships at Meta.

PDF SHA-256: `e2447fdcf48da2fe717bb7795adb4a902b0b939d9ca9f79feff95d222b6f16a1`

### Figure 5 — Caption fusion data engine

**PDF page 5; family: typed-data fan-in workflow.** Actual crop inspected at 216 dpi.

**Color roles.**
- Video branch fill: `#E6EFEC`, alpha 1; vector_measured.
- Video branch ink: `#005853`, alpha 1; vector_measured.
- Frame branch fill: `#E1EAF2`, alpha 1; vector_measured.
- Frame branch ink: `#3B7190`, alpha 1; vector_measured.
- Metadata and LLM fill: `#E5E1F6`, alpha 1; vector_measured.
- Metadata ink: `#66629B`, alpha 1; vector_measured.
- LLM outline: `#4F3A7B`, alpha 1; vector_measured.
- Routing ink: `#134F5C`, alpha 1; vector_measured.

**Typography.**
- Row contents: OptimisticText-Regular, 4.936 pt, regular; vector_measured.
- Branch headings: OptimisticText-Regular, 5.595 pt, regular; vector_measured.
- Captioner blocks: OptimisticText-Bold, 5.924 pt, bold; vector_measured.
- LLM: OptimisticText-Bold, 8.557 pt, bold; vector_measured.
- Input/output labels: OptimisticText-Regular, 4.278 pt, regular; vector_measured.

**Layout.** Video frames enter two captioners and a metadata path. The middle column presents actual record-shaped content: a video caption, expandable frame-caption rows, and title/description metadata. These feed a tall LLM block, which emits a dashed text artifact. Teal, blue and lavender families persist from branch to record.

**Geometry and strokes.** The chosen half-page region is 309 × 124 pt. Fine routes are about 0.494 pt with lighter strokes around 0.247 pt. Narrow repeated plus-glyph cells form a separate column from record text.

**Routing.** Curved routes diverge after the input stack, then converge at the LLM input edge. Routes remain outside the contents of the record rows. The final output is a single arrow to a separate artifact.

**Transferable rules.**
- Replace generic data boxes with miniature records when the data structure explains the method.
- Keep branch color stable from producing operation to its data object.
- Use a visually distinct output-artifact boundary and a short final connector.

**Do not copy blindly.**
- The source uses 4–6 pt labels; enlarge the figure or reduce record count in a new design.
- Do not add a plus icon if it can be misread as arithmetic rather than expandable list structure.
- The exact proprietary font may be unavailable; preserve hierarchy with a verified installed family.

### Figure 8 — Layer-by-task diagnostic matrix

**PDF page 11; family: semantically grouped small multiples.** Actual crop inspected at 216 dpi.

**Color roles.**
- Classification heading fill: `#E6EFEC`, alpha 1; vector_measured.
- Classification curve/text: `#038790`, alpha 1; vector_measured.
- Language heading fill: `#E1EAF2`, alpha 1; vector_measured.
- Language dark/mid/light traces: `#35528A`, alpha 1; vector_measured.
- Language middle trace: `#3D71BE`, alpha 1; vector_measured.
- Language light trace: `#84B5DF`, alpha 1; vector_measured.
- Spatial heading fill: `#E5E1F6`, alpha 1; vector_measured.
- Spatial dark trace: `#693A87`, alpha 1; vector_measured.
- Spatial middle trace: `#8F50BA`, alpha 1; vector_measured.
- Spatial light trace: `#B1A3EA`, alpha 1; vector_measured.

**Typography.**
- Domain headings: OptimisticText-Bold, 7.516 pt, bold; vector_measured.
- Task names: OptimisticDisplay-Bold, 8.052 pt, bold; vector_measured.
- Task datasets: OptimisticDisplay-Light, 8.052 pt, regular; vector_measured.
- Model labels and best values: OptimisticDisplay-Bold, 4.831 pt, bold; vector_measured.
- Small annotation text: OptimisticDisplay-Light, 4.831 pt, regular; vector_measured.

**Layout.** Three model columns cross seven task rows, grouped into classification, language modeling and spatial tasks. Each group has a tinted capsule heading, a very pale body background and a related hue family. Task labels occupy a dedicated left rail. Dashed best-value reference lines cross each task row, while vertical dashed guides mark selected layers.

**Geometry and strokes.** The region is portrait-shaped, approximately 285 × 396 pt. The 21 miniature curve panels are embedded raster images; surrounding headings, model labels, endpoint values and dashed guides include visible vector text/shapes. Figure-level font metrics must therefore be assigned by role rather than to all chart pixels.

**Routing.** No system arrows. Horizontal best-value references and vertical best-layer guides create the comparison structure.

**Transferable rules.**
- Use a model × task matrix when a single radar chart would mix too many comparisons.
- Group task families with pale backgrounds and consistent color hierarchies.
- Label key optima directly in panels, while retaining a common row reference.
- Keep task names and units in a stable left rail.

**Do not copy blindly.**
- The figure is very dense: many source labels are below 5 pt. Split panels or increase page allocation for a new figure.
- The best-value line must be defined consistently across models.
- A shared column width does not mean equal layer counts; retain layer indices and model-specific maxima.

<a id="eupe"></a>
## Efficient Universal Perception Encoder

**Meta / FAIR | 2026 | arXiv:2603.22387v2**

[Primary PDF](https://arxiv.org/pdf/2603.22387v2) · [Record](https://arxiv.org/abs/2603.22387v2)

PDF p1 lists Meta Reality Labs and FAIR at Meta.

PDF SHA-256: `f1d91b91820967e8b4aee3f34b563c1de2507cd2d53ee7492fb98cfd252d9481`

### Figure 1 — Multi-benchmark radar and feature examples

**PDF page 2; family: capability summary with qualitative evidence.** Actual crop inspected at 216 dpi.

**Color roles.**
- Proposed model: `#E41A1C`, alpha 1; vector_measured.
- Comparators blue/green/purple: `#377EB8`, alpha 1; vector_measured.
- Comparator green: `#4DAF4A`, alpha 1; vector_measured.
- Comparator purple: `#984EA3`, alpha 1; vector_measured.
- Comparator orange: `#FF7F00`, alpha 1; vector_measured.
- Comparator yellow: `#FFFF33`, alpha 1; vector_measured.
- Grid: `#E6E2DF`, alpha 1; vector_measured.

**Typography.**
- Figure labels: unidentified, size unverified, regular; visual_estimate. All lettering is outlined with hidden LiberationSans/Helvetica search text. Hidden family names and sizes are not used as proof of visible typography.

**Layout.** A large radar consumes roughly three-quarters of the horizontal space; a two-column strip of image/PCA pairs fills the right. The proposed model has the thick red outline, while several comparator polygons overlap at lower opacity. Numeric boxes are placed directly on vertices.

**Geometry and strokes.** Seven model traces and nine benchmark axes create many overlaps. Source numeric labels visibly collide at several vertices. The right qualitative strip keeps all paired crops square and aligns rows.

**Routing.** No arrows. Polygon vertices and numeric labels encode benchmark values; image pairs encode feature visualizations.

**Transferable rules.**
- Use a stronger line weight for the focal model when a compact overview is essential.
- Keep paired qualitative crops the same size and alignment.
- Treat this figure as evidence for a radar-density limit: once labels overlap, change the structure.

**Do not copy blindly.**
- Do not copy seven translucent polygons and dense vertex labels; use small multiples or a task-by-model matrix.
- Yellow lines and text on white have weak contrast.
- Polygon area is not a valid aggregate score, and normalized axis ranges must be stated.

### Figure 2 — Scale-up then scale-down distillation stages

**PDF page 4; family: multi-stage training storyboard.** Actual crop inspected at 216 dpi.

**Color roles.**
- First expert fill: `#FFF2CC`, alpha 1; vector_measured.
- Second expert fill: `#D5E8D4`, alpha 1; vector_measured.
- Third expert fill: `#F8CECC`, alpha 1; vector_measured.
- Proxy fill: `#E1D5E7`, alpha 1; vector_measured.
- Proxy outline: `#9673A6`, alpha 1; vector_measured.
- Efficient student fill: `#BAC8D3`, alpha 1; vector_measured.
- Student outline: `#23445D`, alpha 1; vector_measured.

**Typography.**
- Proxy labels: LiberationSans, 5.814 pt, regular; vector_measured.
- Student labels: LiberationSans, 4.845 pt, regular; vector_measured.
- Edge labels: LiberationSans, 5.330 pt, regular; vector_measured.
- Stage labels: LiberationSans, 6.784 pt, regular; vector_measured.

**Layout.** A three-part left-to-right storyboard is separated by thin vertical dashed rules. Stage 1 is wider because it contains three teachers; stages 2 and 3 are compact matched pairs of proxy/student. The proxy preserves the same lavender color as it changes from trainable to frozen. Multi-resolution inputs are shown as a stack of different image sizes.

**Geometry and strokes.** Most source node and route strokes measure about 0.485 pt. The stages allocate approximately 42:28:30 width (visual estimate). Fire and snowflake glyphs carry trainable/frozen state independently of model color.

**Routing.** Teacher outputs converge on one explicit distillation edge. Subsequent stages each have one horizontal teacher-to-student edge plus separate image-input branches.

**Transferable rules.**
- Allocate width according to stage complexity rather than forcing equal panels.
- Preserve model identity colors while showing training state with a separate symbol or textual badge.
- Represent multiresolution augmentation with a concrete image stack.

**Do not copy blindly.**
- Snowflake/fire icons need a legend or adjacent text; they are not universally self-explanatory.
- The 4.845 pt student labels are too small to adopt as a production default.
- Do not imply simultaneous execution when the figure shows sequential training stages.

### Figure 3 — Per-teacher patch and CLS distillation flow

**PDF page 5; family: two-lane loss diagram.** Actual crop inspected at 216 dpi.

**Color roles.**
- Student patch representation: `#CCE5FF`, alpha 0.6; vector_measured. Raw transparent fill; rendered blue is lighter than this hexadecimal color. Background: White page and overlapping translucent tensor faces; overlapping faces have different displayed colors.
- Teacher representation: `#FFCCCC`, alpha 0.6; vector_measured. Background: White page and overlapping translucent tensor faces; overlapping faces have different displayed colors.
- Trainable adapters: `#FFF2CC`, alpha 1; vector_measured.
- Loss boxes: `#F5F5F5`, alpha 1; vector_measured.
- Main line ink: `#36393D`, alpha 1; vector_measured.

**Typography.**
- Interpolation edge label: LiberationSans, 5.179 pt, regular; vector_measured.
- Normalization edge label: LiberationSans, 6.330 pt, regular; vector_measured.
- Mathematical labels: unidentified, size unverified, regular; visual_estimate. Large serif mathematical labels are outlined; their font family and exact point size are not established.

**Layout.** A student on the left splits into patch-token and CLS-token lanes. A teacher on the right supplies matched targets. Each lane meets at a loss box near the center. Patch tokens are an extruded grid, while a CLS token is a single flat tile. A dotted rounded scope identifies repetition for each teacher.

**Geometry and strokes.** The source uses about 0.575 pt nonzero strokes; many zero-width paths belong to outlined artwork, not intended production lines. The upper and lower lanes have aligned adapters, losses and teacher representations.

**Routing.** Student paths travel right; teacher targets travel left. Interpolation appears only in the patch lane and normalization appears on both target lanes. This is a two-sided loss computation, not a unidirectional inference chain.

**Transferable rules.**
- Show data tensor structure through a small token grid when it explains why two losses differ.
- Mirror student and teacher lanes around the actual loss junction.
- Place a repeat boundary around precisely the repeated per-teacher operations.

**Do not copy blindly.**
- Do not reverse loss-target directions to make all arrows point right.
- Dotted scope outlines must not be confused with gradient flow.
- Do not represent every tensor dimension if it adds clutter without explaining the method.

<a id="gr00t-n1"></a>
## GR00T N1: An Open Foundation Model for Generalist Humanoid Robots

**NVIDIA | 2025 | arXiv:2503.14734v2**

[Primary PDF](https://arxiv.org/pdf/2503.14734v2) · [Record](https://arxiv.org/abs/2503.14734v2)

PDF p1 names NVIDIA as authoring organization.

PDF SHA-256: `76e38cf679637b816b16edf7170340883dd09175bf334aeeaed49392777731b9`

### Figure 2 — Dual-system VLA model overview

**PDF page 3; family: multimodal token-lane architecture.** Actual crop inspected at 216 dpi.

**Color roles.**
- Image tokens: `#9C2FE5`, alpha 0.5176; vector_measured. Raw source fill; pale visible violet results from alpha compositing. Background: White input/output field or pale-gray model interior; displayed color depends on placement.
- Text tokens: `#0365C0`, alpha 1; vector_measured.
- State tokens: `#E06666`, alpha 1; vector_measured.
- Clean action tokens: `#FF9900`, alpha 1; vector_measured.
- Noisy action tokens: `#FF9900`, alpha 0.1569; vector_measured. Background: White input/output field or pale-gray model interior; displayed color depends on placement.
- Model modules: `#F2F2F2`, alpha 1; vector_measured.
- System 2 label: `#E82884`, alpha 1; vector_measured.
- System 1 label: `#50ABC0`, alpha 1; vector_measured.

**Typography.**
- Regular labels: ArialMT, 7.244 pt, regular; vector_measured.
- Major module titles: HelveticaNeue-Bold, 9.338 pt, bold; vector_measured.
- System labels: Optima-Bold, 10.357 pt, bold; vector_measured.
- Literal instruction: AndaleMono, 7.244 pt, regular; vector_measured.
- Small state labels: ArialMT, 5.207 pt, regular; vector_measured.

**Layout.** Three left input lanes carry an image, a literal instruction and a robot-state schematic. Narrow colored token strips bridge inputs and tall model modules. The vision-language model occupies the upper middle while the diffusion block spans the token and action lanes. A token-opacity progression inside the latter exposes denoising.

**Geometry and strokes.** Tall rounded modules give labels room and align with their consumed token strips. Primary strokes are about 0.584 pt; selected boundaries about 0.778 pt. The final motor action is illustrated by a separate robot image.

**Routing.** Image/text enter the VLM; state bypasses it into the diffusion block. Denoising is shown by a separate dotted horizontal direction arrow below the action-token progression.

**Transferable rules.**
- Represent modalities with stable token-strip colors, not just a list of input names.
- Use a concrete instruction and representative state labels to explain what enters the model.
- Separate semantic module identity from repeated token/data representations.

**Do not copy blindly.**
- Raw alpha-encoded token colors must be composited or converted to opaque tints when reused.
- An overview may hide precise block connections; pair it with a mechanism detail when those edges matter.
- Avoid adding robot imagery to a non-robotic system merely for decoration.

### Figure 3 — Embodiment-aware encoders, diffusion blocks, and decoding

**PDF page 4; family: expanded recurrent model mechanism.** Actual crop inspected at 216 dpi.

**Color roles.**
- Embodiment-specific modules: `#D9EAD3`, alpha 1; vector_measured.
- Repeated attention blocks: `#D9D9D9`, alpha 1; vector_measured.
- Shared modules: `#F2F2F2`, alpha 1; vector_measured.
- Routes: `#53585F`, alpha 1; vector_measured.
- Image tokens: `#9C2FE5`, alpha 0.5137; vector_measured. Background: White page or pale-gray grouped module fields; displayed color depends on placement.
- Text tokens: `#0365C0`, alpha 1; vector_measured.
- State tokens: `#E06666`, alpha 1; vector_measured.
- Clean action tokens: `#FF9900`, alpha 1; vector_measured.

**Typography.**
- Module labels: ArialMT, 7.018 pt, regular; vector_measured.
- Repetition label: ArialMT, 6.031 pt, regular; vector_measured.
- Literal instruction: AndaleMono, 6.031 pt, regular; vector_measured.
- Mathematical state/action labels: CambriaMath, 8.059 pt, regular; vector_measured.

**Layout.** The upper path handles image/text context; the lower path handles robot state and noisy action. Embodiment-specific encoders and decoder are pale green. Cross/self-attention repeat inside one gray rounded block; action sequences use dashed list containers. A legend decodes the green modules and snowflake symbol.

**Geometry and strokes.** Two stroke tiers measure about 0.565 and 0.754 pt. The lower edge of the figure reserves a wide return corridor, and the repeat count is placed directly below the DiT block.

**Routing.** Context branches enter cross-attention at top ports. Noisy actions enter the horizontal block lane. A dotted outer loop returns decoded action to the noisy-action input for K iterations without crossing the model interior.

**Transferable rules.**
- Expand a high-level module by preserving its modality colors and exposing actual operator types.
- Reserve the feedback corridor before laying out the lower labels.
- Separate repeat-count annotations for layer repetition and iterative inference.

**Do not copy blindly.**
- The source mixes vertical attention labels with horizontal module labels; rotate only when the block aspect requires it.
- Freeze/train state requires a textual legend; color alone means embodiment specificity here.
- Route the outer iteration loop to the correct state input, not to an arbitrary nearby node.

<a id="cosmos-reason1"></a>
## Cosmos-Reason1: From Physical Common Sense To Embodied Reasoning

**NVIDIA | 2025 | arXiv:2503.15558v1**

[Primary PDF](https://arxiv.org/pdf/2503.15558v1) · [Record](https://arxiv.org/abs/2503.15558v1)

PDF p1 names NVIDIA as authoring organization.

PDF SHA-256: `f0721fecb78a726cb5648a44958f65f2a8f70bd8032e36c24c5cd26ee57064a8`

### Figure 1 — Model, training, ontology, and benchmark inventory

**PDF page 2; family: parallel scope inventory.** Actual crop inspected at 216 dpi.

**Color roles.**
- Title accent: `#76B900`, alpha 1; vector_measured.
- Group and item borders: `#000000`, alpha 1; vector_measured.

**Typography.**
- Items: ArialMT, 8.453 pt, regular; vector_measured.
- Group headings: Arial-BoldMT, 9.660 pt, bold; vector_measured.
- Figure title: Arial-BoldMT, 10.868 pt, bold; vector_measured.

**Layout.** Four equal-height columns list different aspects of the project. Model has three cards, training four, and ontology/benchmark two each. Thin inner outlines contrast with heavier outer column borders. The layout deliberately has no arrows: it is a scope inventory rather than a causal pipeline.

**Geometry and strokes.** Outer borders measure 0.906 pt; inner borders 0.453 pt. Consistent group widths and top-aligned headings organize unequal numbers of items. The green accent is confined to the title.

**Routing.** No connectors; adding arrows would falsely imply a single computational chain.

**Transferable rules.**
- Use equal boxes when the scientific task is an inventory of parallel dimensions.
- Make border-weight hierarchy carry grouping when color is unnecessary.
- State whether a diagram explains scope, computation, or chronology before selecting arrows.

**Do not copy blindly.**
- This is not an adequate template for a mechanism figure.
- Do not copy the product logo or use its accent as an assumed corporate house style.
- Avoid a generic four-box summary when specific data or operation structure is the contribution.

### Figure 6 — Embodied-reasoning SFT data curation

**PDF page 11; family: concrete-example workflow.** Actual crop inspected at 216 dpi.

**Color roles.**
- Processing modules: `#76B900`, alpha 0.5; vector_measured. Raw vector color at alpha 0.5; visible pale green is a composite over its background, not opaque #76B900. Background: White page background under processing-node interiors.
- Subtask labels: `#C9DAF8`, alpha 1; vector_measured.
- Data artifacts/background: `#F3F3F3`, alpha 1; vector_measured.
- Routes and outlines: `#434343`, alpha 1; vector_measured.
- De-emphasized context text: `#B7B7B7`, alpha 1; vector_measured.

**Typography.**
- Node and example labels: embedded font000000002d8a2408; family unidentified, 7.533 pt, regular; vector_measured.
- Main goal: embedded font000000002d8a2408; family unidentified, 8.789 pt, regular; vector_measured.
- Small example text: embedded font000000002d8a2408; family unidentified, 6.905 pt, regular; vector_measured.

**Layout.** A concrete three-subtask video sequence occupies the top-left. The current subtask has a rounded enclosure and dark text, while adjacent subtasks are muted context. Green processing modules run along the bottom then upward at right. Gray rectangular artifacts distinguish questions, object-action lists and the final SFT tuple.

**Geometry and strokes.** Main connectors and module outlines measure 0.942 pt; secondary boundaries 0.471 pt. Stacked frames indicate clips. A bottom corridor carries the state-action context into the later reasoning stage.

**Routing.** A single selected current clip feeds captioning, while paired current/next information feeds QA curation. Distinct branches become a reasoning extraction input; subsequent cleaning points upward to the final record.

**Transferable rules.**
- Anchor an abstract data-generation pipeline with one concrete input and one final output record.
- Use stronger enclosure and text contrast for the active temporal slice.
- Separate operations from intermediate data artifacts through shape/fill vocabulary.

**Do not copy blindly.**
- Muted text still needs adequate contrast in the actual print size.
- Do not call the embedded arbitrary font identifier Arial without independent evidence.
- No raw transparent fill should be reused as an opaque palette token.

<a id="nemotron3-super"></a>
## Nemotron 3 Super: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning

**NVIDIA | 2026 | arXiv:2604.12374v1**

[Primary PDF](https://arxiv.org/pdf/2604.12374v1) · [Record](https://arxiv.org/abs/2604.12374v1)

PDF p1 names NVIDIA.

PDF SHA-256: `fa7e8a9a1a8f9f716e38e46170371d4bc67c3f6d1ac3e4857c574e911f0e107f`

### Figure 1 — Accuracy and throughput benchmark comparison

**PDF page 2; family: split-metric grouped bars.** Actual crop inspected at 216 dpi.

**Color roles.**
- Proposed BF16 model: `#6AA84F`, alpha 1; vector_measured.
- Proposed NVFP4 model: `#96C880`, alpha 1; vector_measured.
- First comparator: `#848484`, alpha 1; vector_measured.
- Second comparator: `#4285F4`, alpha 1; vector_measured.

**Typography.**
- Figure labels: unidentified, size unverified, regular; visual_estimate. Visible labels are outlined. Hidden DejaVuSans overlays exist at several tiny sizes, but do not establish visible font identity or production-size recommendations.

**Layout.** A wide benchmark strip uses grouped bars and direct numeric labels. A dashed vertical divider separates accuracy tasks from throughput. Headings name the metric regions; the left and right y axes have explicit different units. Two green shades identify precision variants within one model family.

**Geometry and strokes.** The accuracy section occupies roughly four-fifths of the width and throughput the remainder (visual estimate). Thin grid/axis strokes are about 0.327 pt. The short two-line category labels carry task family context.

**Routing.** No arrows. The divider and heading hierarchy are essential because unlike units share one visual frame.

**Transferable rules.**
- Use hue families to group related precision variants and unrelated hues for different model families.
- Give each unit regime its own title, axis and explicit scope.
- Use direct values when exact benchmark lookup matters.

**Do not copy blindly.**
- Prefer physically separate panels when a dual-axis composition could imply a common scale.
- Dense labels, long model names and tiny footnotes should move to the caption or an external legend.
- Keep throughput hardware, batching, sequence length and precision conditions visible.

### Figure 3 — Standard MoE versus LatentMoE

**PDF page 5; family: matched architecture comparison.** Actual crop inspected at 216 dpi.

**Color roles.**
- New latent projection fill: `#D7E7CF`, alpha 1; raster_sampled. Representative rendered pale-green sample; the low-resolution raster has interpolation/alpha variation.
- New latent projection outline: `#82B366`, alpha 1; raster_sampled.

**Typography.**
- Architecture node text: unidentified, size unverified, regular; visual_estimate. Node lettering is raster; family and source size are unknown.
- Panel captions: LMRoman10-Regular, 9.963 pt, regular; vector_measured.

**Layout.** Two vertically oriented architectures align the previous-layer input, residual addition, self-attention, routing/expert section, combine operation and next-layer output. New down/up projections are the only colored nodes. Selected experts use hatching; the router is a small bar-profile object.

**Geometry and strokes.** The left architecture is a 414 × 535 px raster placed at 230.58 × 297.97 pt (~129 px/in at source placement); the right is 518 × 615 px at 230.57 × 273.74 pt (~162 px/in). No exact vector node font or stroke width can be recovered.

**Routing.** Main state travels bottom-to-top. Residuals use an outer left return-style bypass. Dotted router lines indicate expert weighting, while solid arrows indicate data transport. Explicit plus and multiply junctions show operations.

**Transferable rules.**
- Keep unchanged architecture neutral and highlight only the new mechanism.
- Use identical landmark positions in before/after comparisons.
- Differentiate routing/weights from token transport with a documented edge style.

**Do not copy blindly.**
- The source has dense crossing routes and visibly rasterized labels; rebuild as vector and separate routing corridors.
- Do not silently equate number of drawn experts with actual model expert count.
- Hatching needs a legend when it indicates active rather than removed experts.

<a id="nemotron-diffusion"></a>
## Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding

**NVIDIA | 2026 | arXiv:2607.05722v1**

[Primary PDF](https://arxiv.org/pdf/2607.05722v1) · [Record](https://arxiv.org/abs/2607.05722v1)

PDF p1 has NVIDIA branding/copyright and explicitly lists additional university affiliations and NVIDIA internships.

PDF SHA-256: `59dbe4282e085a0606298647de5b6fab650da86d9525b0d67e69d14a5ac61739`

### Figure 1 — Three inference modes and two performance tradeoffs

**PDF page 1; family: mechanism-plus-evidence triptych.** Actual crop inspected at 216 dpi.

**Color roles.**
- AR mode: `#006FE8`, alpha 1; vector_measured.
- Diffusion mode: `#FF6700`, alpha 1; vector_measured.
- Self-speculation mode: `#48A027`, alpha 1; vector_measured.
- Model-family highlight: `#2E7D32`, alpha 1; vector_measured.
- Comparator label blue: `#1F5FA0`, alpha 1; vector_measured.

**Typography.**
- Mode titles: LiberationSans-Bold, 6.636 pt, bold; vector_measured.
- Mode descriptions: LiberationSans-BoldItali, 4.404 pt, bold italic; vector_measured.
- Plot labels and annotations: LiberationSerif, 4.629 pt, regular; vector_measured.
- Plot headings/axes: LiberationSerif-Bold, 5.603 pt, bold; vector_measured.

**Layout.** A three-panel first-page summary pairs a mode diagram with accuracy-throughput and system-throughput/per-user-throughput plots. Plot points are directly labeled and marker shape separates models or modes. The first panel uses saturated colored cards and simple token icons; the plot panels use a quiet white field.

**Geometry and strokes.** The diagram and two plots occupy comparable widths. Several labels are 3–5 pt. The PDF combines graphics with distinct internal transformations, so unnormalized raw path widths are not treated as effective painted strokes.

**Routing.** Only the mechanism panel contains arrows. Plot direction annotations state which region is preferable; concurrency and block-size parameters are attached to measured points.

**Transferable rules.**
- Pair a new decoding mechanism with both quality-speed and serving-efficiency evidence.
- Keep mechanism iconography separate from quantitative axes.
- Encode operating condition with marker style and explicit point annotation.

**Do not copy blindly.**
- The first-page triptych is too dense for its original small lettering; expand or split it in a new paper.
- Avoid drop shadows and saturated orange/green cards when they compete with the measurements.
- Do not connect operating points into an implied universal frontier without controlled hardware and workload conditions.

### Figure 3 — Joint losses and attention pattern

**PDF page 3; family: token diagram paired with a block mask.** Actual crop inspected at 216 dpi.

**Color roles.**
- Diffusion targets and noisy-token attention: `#D4E1F5`, alpha 1; vector_measured.
- Autoregressive targets and causal attention: `#FFCCCC`, alpha 1; vector_measured.
- Clean context tokens: `#D5E8D4`, alpha 1; vector_measured.
- Noisy-to-clean attention block: `#FFE6CC`, alpha 1; vector_measured.
- Masked tokens: `#CCCCCC`, alpha 1; vector_measured.
- Model block: `#F5F5F5`, alpha 1; vector_measured.

**Typography.**
- Loss headings: LiberationSans-Bold, 5.453 pt, bold; vector_measured.
- Model label: LiberationSerif-Bold, 6.543 pt, bold; vector_measured.
- Masking label: LiberationSans, 5.453 pt, regular; vector_measured.

**Layout.** The left half depicts masked and clean token streams entering one model, with diffusion and AR targets above. The right half is an attention matrix whose rows and columns repeat the same token symbols. Pastel cells distinguish attention subsets while white cells denote absence.

**Geometry and strokes.** Source nonzero cell/model outlines are about 0.818 pt. The matrix has a deliberate block gap separating noisy and clean contexts. Rounded token squares maintain identity between sequence and matrix.

**Routing.** Masking has an explicit branch indicator. Attention is represented by filled cells rather than dozens of arrows, avoiding combinatorial edge clutter.

**Transferable rules.**
- Show sparse or patterned interactions as an adjacency/mask matrix instead of a dense arrow graph.
- Reuse identical token glyphs and color roles in the sequence and matrix.
- Separate block partitions with spacing, then explain each cell class in a legend.

**Do not copy blindly.**
- This matrix encodes a categorical mask, not a numerical heatmap; do not attach a continuous colorbar.
- The source colors alone are insufficient for grayscale; add pattern or letter labels to distinguish subsets.
- State row/column orientation and causal convention explicitly.

### Figure 5 — AR, diffusion, and self-speculation inference

**PDF page 7; family: matched token storyboard.** Actual crop inspected at 216 dpi.

**Color roles.**
- Model strip: `#DCEAF7`, alpha 1; vector_measured.
- Accepted/predicted tokens: `#D9F2D0`, alpha 1; vector_measured.
- Context tokens: `#D9D9D9`, alpha 0.6; vector_measured. Background: White field with shadowed token cards; shadow and layered rendering are not normalized into an opaque authoring token.
- Rejected token: `#FFCECE`, alpha 1; vector_measured.
- Rejection marker: `#C00000`, alpha 1; vector_measured.
- Single shared model: `#4EA72E`, alpha 1; vector_measured.
- Cache brace and annotation: `#084F6A`, alpha 1; vector_measured.

**Typography.**
- Token text: TimesNewRomanPSMT, 5.960 pt, regular; vector_measured.
- Mode/panel labels: TimesNewRomanPSMT, 7.477 pt, regular; vector_measured.
- Larger model labels: TimesNewRomanPSMT, 8.452 pt, regular; vector_measured.
- Cache annotation: TimesNewRomanPS-BoldItal, 7.910 pt, bold italic; vector_measured.

**Layout.** Two equal top panels contrast sequential AR and parallel diffusion. A wider lower panel shows draft and verification as two uses of one shared model. Uniform token cells make sequential, parallel, accepted and rejected states concrete. The cacheable region is bracketed under the verified sequence.

**Geometry and strokes.** Most source outlines measure 0.745 pt. A consistent token pitch aligns rows. Model strips are long pale-blue rectangles; token states use gray, pale green and pale red.

**Routing.** Dashed blue arrows connect sequential generation steps. The lower draft route travels through a dedicated middle gap into verification. Green versus red dashed alignments show accepted and rejected candidate tokens; a brace marks the reuse span.

**Transferable rules.**
- Use an actual short token sequence to explain inference-time concurrency and validation.
- Align token positions across before/after or draft/verify views.
- Make one shared parameter set explicit so duplicate drawings do not imply duplicate models.
- Use a brace to mark a reusable contiguous span rather than enclosing the whole model.

**Do not copy blindly.**
- Drop shadows add little and should usually be removed in a new scientific figure.
- A snowflake beside verification can be misread as a training statement; explain the intended state.
- Preserve token order and rejection semantics exactly; typography cannot repair an incorrect sequence.

## Transferable design recipes

### Diagram-code correspondence

Sources: alphaevolve Figure 2, alphaevolve Figure 3.

For a harness or agent method, allocate a human setup band, a row of typed operations, and one readable controller excerpt. Repeat role colors on module labels and the corresponding code identifiers. Keep the final artifact outside the system boundary.

The source role mappings and mechanism are observed; all tokens in recommended_tokens are new production recommendations, not copied source measurements.

```json
{
  "body_pt": 8.5,
  "group_pt": 10.5,
  "code_pt": 8.2,
  "route_pt": 1.0,
  "scope_pt": 0.65,
  "gutter_mm": 3.5,
  "font": "verified installed sans + compatible monospace",
  "ink": "#263238",
  "prompt_accent": "#2C64B7",
  "model_accent": "#B9453D",
  "evaluator_accent": "#8A6500",
  "memory_accent": "#287A48",
  "group_fill": "#EEF3FB"
}
```

### Provenance overview with a mechanism expansion

Sources: sam3 Figure 4, sam3 Figure 10, perception-encoder Figure 5.

Keep familiar inherited modules neutral or cool-toned, use a distinct pale accent for the new operation, and give the new operation a larger detail panel. Encode data/state with token rows, record cards or a memory stack. Include a small provenance legend. Reserve one outer feedback corridor and use explicit merge nodes.

Source-specific palette roles and object vocabulary are observed. These adjusted opaque tokens and clearances are recommendations.

```json
{
  "body_pt": 8.5,
  "heading_pt": 10,
  "route_pt": 1.0,
  "border_pt": 0.8,
  "feedback_gap_mm": 4,
  "new_fill": "#FFF2B8",
  "new_ink": "#6D5300",
  "inherited_fill": "#DCEBFA",
  "state_fill": "#D7ECE8",
  "ink": "#26333D"
}
```

### Task-by-model diagnostic matrix

Sources: perception-encoder Figure 8, dinov3 Figure 5, eupe Figure 1.

For many evaluation dimensions, use model columns and task rows, with a left label rail and group headings. Color families encode task domains, while line/marker styles encode models if necessary. Share reference lines only when the baseline definition matches. Pair selected rows with qualitative diagnostics rather than adding more radar polygons.

The matrix grammar comes from PE; EUPE radar label collisions serve as a negative example. Recommended values intentionally exceed the source microtype sizes.

```json
{
  "body_pt": 8,
  "group_pt": 9.5,
  "curve_pt": 1.1,
  "grid_pt": 0.4,
  "row_gap_mm": 3,
  "main_palette": [
    "#147A82",
    "#315F9A",
    "#75469A"
  ]
}
```

### Concrete tokens and typed multimodal lanes

Sources: gr00t-n1 Figure 2, gr00t-n1 Figure 3, nemotron-diffusion Figure 5.

Give each modality a lane and stable token color. Show one literal input/example, an explicit state representation and a concrete output sequence. Use an overview/detail pair for repeated operators. In inference storyboards, align token positions, separate draft from verification, and bracket the reused state.

Modality roles and token/storyboard grammar are observed. Recommended colors are opaque, adjusted for new figures; they are not raw transparent source colors.

```json
{
  "body_pt": 8.5,
  "heading_pt": 10,
  "route_pt": 0.95,
  "loop_clearance_mm": 4,
  "token_gap_mm": 0.7,
  "image_token": "#C59AE3",
  "text_token": "#3B74AF",
  "state_token": "#D77771",
  "action_token": "#E79A35",
  "context_fill": "#EEEEEE",
  "module_fill": "#F3F4F5"
}
```

### Select source features, not whole source styles

Sources: eupe Figure 1, nemotron3-super Figure 1, nemotron3-super Figure 3, cosmos-reason1 Figure 1.

Audit an admired figure for type size, overlaps, axis semantics and rasterization before adopting it. Keep a high-value structural idea while rejecting tiny type, excessive radar overlaps, ambiguous mixed units or blurry raster diagram labels. Treat inventory layouts as inventories and mechanism layouts as mechanisms.

Direct inspection found both transferable strengths and practical defects in current major-company figures.

