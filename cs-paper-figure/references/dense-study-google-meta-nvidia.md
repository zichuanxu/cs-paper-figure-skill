# Sophisticated figure studies: Google/DeepMind, Meta, and NVIDIA

**14 distinct papers; 28 actually inspected figure crops.** Twelve papers were first submitted in 2025–2026. Thirteen inspected revisions are from 2025–2026. Titans is honestly recorded as first submitted in December 2024; Movie Gen is a 2024 report inspected in its February 2025 revision.

The study emphasizes meaningful internal objects, multi-scale explanations, matched evidence, and scientific comparison. It does not rank papers by prestige or claim that a generated figure objectively beats them.

| Company group | New papers | Figure crops |
|---|---:|---:|
| Google / DeepMind | 5 | 10 |
| Meta / FAIR | 4 | 8 |
| NVIDIA | 5 | 10 |

## Four reusable compositions

### Mechanism, closeup, and exact relation matrix

Use a small whole-system locator, a large component closeup, and one exact relation view such as an attention mask, dependency table, or state-transition matrix.

Sources: fast-blt:Figure 5, miras:Figure 2, nested-learning:Figure 2.

- Choose one short, concrete sequence or artifact and preserve its labels throughout.
- Number the two or three operations that deserve closeups.
- Repeat the same tokens on matrix axes.
- Use one connector style for execution and another for explanatory zoom.
- Size the matrix so its headers remain readable at final print size.

**Verification question:** A reader should be able to trace one object from the overview through the closeup and verify one permitted or blocked relation in the matrix.

**Avoid:** A closeup must expose a mechanism; it cannot be another enlarged generic box. Do not copy the source sub-5-point type or excessive accent count.

### Fixed schema with changing conditioning or training state

Show one canonical multimodal object sequence, then vertically aligned variants with the same slots, camera views, token groups, or state fields.

Sources: cosmos-policy:Figure 2, cosmos-policy:Figure 12, titans:Figure 2.

- Keep column positions and widths identical.
- Use quiet background bands for supplied versus predicted content.
- Use a redundant mark such as noise texture, a mask badge, or an outline for the changed state.
- Put objective formulas and sample weights above each row.
- Use a shared column header if repeated labels would become tiny.

**Verification question:** A reader should see the single changed boundary or state without re-reading every object label.

**Avoid:** Do not imply that a learned latent slot is literally a photograph of its semantic quantity. Do not reorder the schema to make individual rows fit.

### Physical mechanism grounded by matched evidence

Pair a compact mechanism with a larger grid of matched scene evidence; repeat one scene or frame-pair throughout the explanation.

Sources: cosmos-transfer1:Figure 6, dreamgen:Figure 2, dreamdojo:Figure 3, perception-lm:Figure 5.

- Define the comparison unit: same frame, same ROI, same time pair, or same camera view.
- Keep that unit aligned across modalities or methods.
- Place masks, intervals, or action objects next to the visual evidence they describe.
- Give results and failure regions enough area for inspection.
- Add timestamps, numeric mask keys, or explicit generated/observed labels.

**Verification question:** A reader should identify what was held constant, what changed, and where the claimed effect is visible.

**Avoid:** A photographic mosaic alone does not establish generalization. Avoid unlabeled diagonal before/after crops when exact spatial comparison matters.

### Systems comparison with an implementation ledger

Combine a before/after computational topology with an aligned ledger of tensor dimensions, communication counts, resource use, or uncertainty-bearing performance.

Sources: movie-gen:Figure 8, pe-av:Figure 13, agent-scaling:Figure 3, cosmos25:Figure 1.

- Preserve the same input/output ordering across variants.
- Expose the repeated operation that is removed, shared, or moved.
- Keep numerical details in a dedicated aligned panel rather than scattering tuples over every edge.
- Reserve route corridors before placing dense containers.
- Show cost and performance uncertainty where both vary.

**Verification question:** A reader should be able to count the relevant operations and connect the structural change to a stated resource or performance consequence.

**Avoid:** Do not claim a causal resource improvement from an unlabeled topology alone. Keep differing axis ranges and aggregation scopes explicit.

## Paper-level inspection records

<a id="nested-learning"></a>
### Nested Learning: The Illusion of Deep Learning Architectures

**Google / DeepMind; first submitted 2025-12-31; inspected v1 dated 2025-12-31.** [Versioned PDF](https://arxiv.org/pdf/2512.24695v1) · [Organization evidence](https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/)

PDF p1 correspondence identifies three google.com authors and Peilin Zhong at Columbia; the official Google Research article attributes this work to Google Research. The arXiv landing title uses Architectures; the inspected PDF title uses Architecture.

PDF SHA-256: `e87a9ce82ff24e96f55b83fb9713a5d6fc9e4a1a232c12d42da49c10022ed891`.

#### Figure 2 — Architecture flattened, unfolded, and expanded into learning levels

PDF page 4; crop `[70, 65, 570, 265]`; family: nested mechanism with conceptual closeups.

**Layout.** A wide two-part composition: the left half relates a flat hybrid stack to an unfolded depth view, while the right half arranges three optimization levels vertically. A dashed vertical divider separates the two explanations.

**Information layers.** Whole hybrid architecture → Depth of internal learning rather than layer count → Nested learning modules → Memory and update-rule closeups.

**Detail devices.** Aligned repeated attention/recurrent blocks; Isometric blocks to expose otherwise hidden depth; Dashed guides from parent modules to subordinate modules; Three colored oval closeups containing a memory object and its equation.

**Density and composition.** Dense but hierarchically navigable: two large regions, three numbered levels, and repeated object grammar organize many details. The paragraph embedded inside the left region consumes substantial space. The top flat architecture is deliberately translucent relative to the foreground depth view. Each right-side closeup repeats the same cube but changes accent hue; the viewer can compare the level-specific equations without relearning the icon. Cream and muted rose grounds carry hierarchy while black arrows remain visible.

**Color.** Training/outer-level ground: #B78383 (raster_sampled_composited); Neural block face: #8A8495 (raster_sampled_composited); Deep block face: #65657E (raster_sampled_composited).

**Typography.** All artwork is one embedded raster. Serif labels, bold headings, and mathematical lettering are visible, but neither font family nor point size can be established from this PDF crop.

**Routing.** Black arrows show the main gradient direction; pale dashed branches indicate decomposition; colored dashed ovals indicate explanation, not additional execution stages.

**Transfer.** Separate execution flow from explanatory decomposition with different connector grammar. Repeat a semantic object inside its closeup and place the governing equation directly beside it. Use depth only when it reveals an additional scientific dimension.

**Do not copy.** Do not add volumetric cubes just to make a flat pipeline look sophisticated. Replace the long embedded paragraph with a concise claim and a caption. Raster serif lettering and shaded edges should be rebuilt as editable elements for new artwork.

#### Figure 5 — Paired architectural views of HOPE and a Transformer

PDF page 30; crop `[80, 65, 560, 242]`; family: matched multilevel architecture comparison.

**Layout.** Four columns form two matched pairs: a nested-memory view and a conventional block view for each architecture. The divider is placed between the architectures, while each pair is linked by adjacency.

**Information layers.** Architecture identity → Equivalent representation views → Memory-update frequencies → Per-level context and truncation parameters.

**Detail devices.** Repeated memory cubes; Aligned annotation cards with the same three parameter fields; Shared query/key/value fan-out at the base; Vertically ordered frequency tiers.

**Density and composition.** High information density is earned by keeping the two representations aligned. The parameter cards make the extra levels inspectable rather than decorative. The two cream memory containers have comparable width and similar object scale. Sage distinguishes feed-forward levels; mauve identifies attention or self-modification. Whitespace between a cube and its parameter card acts as a consistent association channel.

**Color.** Nested-memory container: #FFF8E3 (raster_sampled_composited); Parameter card: #FFFCF3 (raster_sampled_composited); Attention/self-modifying block: #65657E (raster_sampled_composited); Feed-forward block: #6C7869 (raster_sampled_composited); Projection block: #9B5353 (raster_sampled_composited).

**Typography.** One embedded raster; visible serif type and math cannot be attributed to an exact font family or size.

**Routing.** Bottom-to-top computation with a shared input fan-out. Curved query/key/value routes converge on the same anchor line; thin vertical arrows connect successive memory levels.

**Transfer.** When comparing mechanisms, align the counterpart components and hold object size constant. Put actual parameter fields next to the repeated structures. Keep an explicit mapping between abstract levels and ordinary blocks.

**Do not copy.** Do not assume the same apparent block height means the same compute or capacity. Tiny frequency annotations need more space at final paper size.

<a id="miras"></a>
### It's All Connected: A Journey Through Test-Time Memorization, Attentional Bias, Retention, and Online Optimization

**Google / DeepMind; first submitted 2025-04-17; inspected v1 dated 2025-04-17.** [Versioned PDF](https://arxiv.org/pdf/2504.13173v1) · [Organization evidence](https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/)

PDF p1 explicitly identifies all four authors with Google Research and google.com addresses.

PDF SHA-256: `faceb861d46d65fd7098cbdb97aa400081c7b5cb7e048ac8d010f01537915ab2`.

#### Figure 1 — Design-space taxonomy connected to the memory objective

PDF page 3; crop `[70, 70, 570, 320]`; family: taxonomy plus equation-grounded mechanism.

**Layout.** Four equal taxonomy columns occupy the upper half. A lower left-to-right mechanism connects an input strip, memory cube, two magnified objective terms, an update operation, and two resulting strips.

**Information layers.** Four independent design decisions → Candidate choices under each decision → Memory as a concrete object → Decomposed objective and its effect on output.

**Detail devices.** Equal taxonomy cards; Numbered option lists; Two dashed circular closeups; A plus sign between objective terms; Repeated token strips before and after learning.

**Density and composition.** Very dense: the upper matrix supports lookup while the lower mechanism explains how its choices act together. One strong title and strict four-column alignment prevent the page from becoming a pile of unrelated annotations. Warm cream backgrounds are almost white; rose carries the explanatory baseline and closeup strokes. The memory cube connects the conceptual taxonomy to an actual operation. The lower labels sit on a shared baseline, distinct from the mathematical labels in the closeups.

**Color.** Outer taxonomy panel: #FFF8E3 (raster_sampled_composited); Individual taxonomy cards: #FFFCF3 (raster_sampled_composited); Explanatory routes: #9B5353 (raster_sampled_composited).

**Typography.** Raster-only artwork. Serif family and mathematical glyphs are visible but exact typeface and point size remain unknown.

**Routing.** A horizontal black execution arrow is separate from a rose explanatory baseline; a dashed leader connects the memory object to its magnified objective.

**Transfer.** Combine a compact design-space matrix with one worked mechanism. Decompose an objective visually only when each term has a distinct scientific role. Keep every column governed by the same heading/definition/options hierarchy.

**Do not copy.** Do not fill taxonomy columns with arbitrary bullets to create visual density. The dense raster prose should be shortened or enlarged in a new figure.

#### Figure 2 — Architecture variants beside an expanded memory block

PDF page 14; crop `[100, 70, 560, 285]`; family: architecture alternatives with component closeup.

**Layout.** Two narrow vertical architecture columns share a left-side scale. A substantially wider right panel expands the common memory module into projections, normalization, convolution, gates, and a residual route.

**Information layers.** Two backbone alternatives → Common memory module → Internal projections and gates → Residual versus main computation.

**Detail devices.** Repeated module color in all views; Residual plus symbols; Dashed bypass routes; Input token strip; Small typed operators instead of identical rectangles.

**Density and composition.** The unequal panel widths correctly allocate space to the detailed block. The two overview columns are concise enough that the closeup can be dense without making every region equally demanding. Pale lavender backgrounds group variants; pale cream groups the detailed block. Sage rounded convolution blocks and rose trapezoidal projections create shape distinctions. The repeated mauve memory block is the visual hinge between overview and detail.

**Color.** Detailed-block ground: #FFF8E3 (raster_sampled_composited); Memory block: #757488 (raster_sampled_composited); MLP block: #85647B (raster_sampled_composited); Projection and residual route: #9B5353 (raster_sampled_composited); Normalization: #F2BC99 (raster_sampled_composited).

**Typography.** One embedded raster: serif labels and mathematical variables are visible; exact family and point sizes are unknown.

**Routing.** Main flow is vertical. Residual paths use dashed side corridors in the overview; the expanded gate takes a long outer route around the block instead of crossing its interior.

**Transfer.** Use a common color/object as the bridge from overview to closeup. Reserve a dedicated outside corridor for bypass paths. Give more width to the scientifically informative closeup than to repeated overview columns.

**Do not copy.** Do not rely on hue alone to distinguish operator types. Avoid faint duplicate routes that might be mistaken for additional signals.

<a id="alphageometry2"></a>
### Gold-medalist Performance in Solving Olympiad Geometry with AlphaGeometry2

**Google / DeepMind; first submitted 2025-02-05; inspected v3 dated 2025-12-08.** [Versioned PDF](https://arxiv.org/pdf/2502.03544v3) · [Organization evidence](https://arxiv.org/abs/2502.03544v3)

PDF p1 gives numbered affiliations and explicitly states that all authors conducted this work at Google DeepMind. PDF cover date 2025-12-10 differs from arXiv v3 submission date 2025-12-08.

PDF SHA-256: `5d481741941713c3203b73ec8f4503d5ae489e9e8ecfd5b1ce52b27f0651ac9f`.

#### Figure 4 — Shared knowledge across heterogeneous proof searches

PDF page 10; crop `[60, 82, 540, 540]`; family: search topology with shared artifact.

**Layout.** A top-down problem/formalization pipeline expands into three distinct search trees inside offset blue containers. A broad brace leads to a shared-facts database below.

**Information layers.** Input and formalization → Multiple language-model instances → Three search procedures → Knowledge shared across procedures.

**Detail devices.** Explicit trees rather than generic agent icons; Stacked containers for repeated model instances; Brace for common scope; Database cylinder with a local definition callout.

**Density and composition.** Moderate density with clear hierarchy. The topology explains which entities are repeated and what they share, but large unused interiors and partially hidden back-card labels could be improved. One pale blue fill distinguishes the search domain from the two white preprocessing cards. Bold headings create a readable three-level hierarchy. The shared database is centered under all trees rather than attached to a single branch.

**Color.** Search-instance containers: #CFE2F3 (vector_measured); Topology and labels: #000000 (vector_measured).

**Typography.** Visible ArialMT and Arial-BoldMT at approximately 9.411 pt. These are figure labels, not page body fonts.

**Routing.** A centered vertical trunk splits into three tree roots. The bottom brace expresses common access; it is a scope relation rather than a directed data-transfer edge.

**Transfer.** Draw a miniature real topology when the claim concerns search or parallel instances. Place shared artifacts outside individual worker containers. Explain unfamiliar shared-state semantics next to the artifact.

**Do not copy.** Do not hide labels behind offset cards; use a count badge or shallow stack tab instead. Do not interpret the raw 381-point stroke width as a physical stroke. It is inconsistent with the render; 82 additional paths are flagged by the inspector as transformed-width failures.

#### Figure 14 — Geometric construction with highlighted proof relationships

PDF page 27; crop `[60, 80, 540, 348]`; family: dense mathematical construction with emphasis layers.

**Layout.** One geometric coordinate field keeps all construction landmarks in place. Gray construction lines form the context; colored circles, translucent polygons, and red auxiliary-point labels identify selected proof relationships.

**Information layers.** Original problem geometry → Auxiliary construction points → Cyclic relationships → Selected similar-triangle relationships.

**Detail devices.** Shared geometric landmarks; Thin context strokes; Translucent filled polygons; Colored point markers and short labels.

**Density and composition.** High legitimate geometric density: many lines encode actual construction relations. The central cluster remains difficult at source scale, so a new figure should add a local zoom or progressive subpanels. A common coordinate field makes the colored relationships directly comparable. Colored fills remain near 0.098 opacity, allowing the underlying construction to stay visible. Red auxiliary markers distinguish added points from the original black-labeled vertices.

**Color.** Context construction lines: #616161 at alpha 0.800 (vector_measured); Cyclic/green relation outline: #2E7D32 at alpha 0.800 (vector_measured); Auxiliary points: #D32F2F (vector_measured); Orange highlighted polygon: #C75000 at alpha 0.098 (vector_measured); Blue highlighted polygon: #1565C0 at alpha 0.098 (vector_measured).

**Typography.** Visible Helvetica labels measured at 3.4396 and 4.12752 pt. The small source size is evidence of a legibility limitation, not a recommended setting.

**Routing.** No process arrows. Exact geometric incidence carries the relation; line crossings must not be rerouted as though this were a flowchart.

**Transfer.** Keep the true coordinate system when geometry is the evidence. Fade the complete construction and emphasize only the relationships used in the argument. Add an anchored magnification for a dense central region rather than redrawing it arbitrarily.

**Do not copy.** Do not treat colored area as a quantitative value. Source labels around 3.44–4.13 pt are too small to adopt as a production target. Do not copy transparent fill hex values as opaque colors.

<a id="agent-scaling"></a>
### Towards a Science of Scaling Agent Systems

**Google / DeepMind; first submitted 2025-12-09; inspected v3 dated 2026-04-08.** [Versioned PDF](https://arxiv.org/pdf/2512.08296v3) · [Organization evidence](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)

PDF p1 lists Google Research, Google DeepMind, and MIT as numbered affiliations.

PDF SHA-256: `028f329010d95143915db8db6ce1ad26a4e844b66e4abd6b36fdb39651aff7fd`.

#### Figure 1 — Architecture scaling across three model families

PDF page 1; crop `[60, 460, 535, 638]`; family: aligned analytical small multiples with direct annotations.

**Layout.** Three equal plotting panels share a performance axis. Each family has its own x-range; five marker shapes encode architectures. A shared legend sits in one row below the panels.

**Information layers.** Model family → Base-model capability → Agent architecture → Relative change at the high-capability endpoint.

**Detail devices.** Shape redundancy for architecture; Direct model labels at selected x positions; One dashed baseline; Endpoint arrows and signed annotations.

**Density and composition.** Moderate analytical density: the figure combines categorical architecture, continuous capability, and family comparison. Its discipline comes from separating color by family and shape by architecture. Thin gray connections are subordinate to colored marks. Only the endpoint comparison receives a saturated annotation. The common y-axis supports comparison, but differing x ranges must remain visible.

**Color.** OpenAI-family marks: #F390C9 (vector_measured); Google-family marks: #367DFE (vector_measured); Anthropic-family marks: #D97757 (vector_measured); Grid: #B0B0B0 at alpha 0.300 (vector_measured); Connecting lines: #808080 at alpha 0.550 (vector_measured).

**Typography.** Visible Aptos and Aptos-Bold text includes model annotations around 5.984 pt and axis/title text around 8.229–8.603 pt. Some symbols and branding are raster images.

**Routing.** Line connections show the progression of models within each architecture; dashed baseline differs from solid multi-agent traces. Annotation arrows stay near the compared endpoint.

**Transfer.** Assign one channel to each comparison dimension. Use a shared legend once for all small multiples. Directly label the few landmarks needed to read the trend.

**Do not copy.** Do not imply identical x-axis ranges across panels. An aggregate across benchmarks can conceal task dependence; disclose the aggregation. Company logos are not required for a scientific comparison.

#### Figure 3 — Cost and performance with uncertainty in both dimensions

PDF page 16; crop `[56, 82, 545, 260]`; family: small-multiple bivariate error-bar comparison.

**Layout.** Three panels place architecture means on cost-versus-performance axes, with both horizontal and vertical uncertainty. The shared legend is below the plots.

**Information layers.** Family-specific cost scale → Mean performance → Mean cost → Uncertainty on both quantities → Architecture identity.

**Detail devices.** Two-dimensional error bars; Five consistent shapes; Muted architecture palette; Shared legend and panel titles.

**Density and composition.** The mark count is modest, but each mark carries several measurements. This is a useful companion to a dense mechanism because it answers an operational question without extra ornamental panels. Markers and error bars share their color. A zero baseline makes the range explicit. Pale lavender/gray marks have weak contrast and several intervals overlap.

**Color.** Gray baseline, lavender decentralized/independent marks, and blue centralized/hybrid marks: exact value not established (visual_estimate).

**Typography.** Four raster occurrences contain the visible plotted labels and marks. No embedded figure font is established; visual sans-serif appearance does not establish Aptos for this separate figure.

**Routing.** No causal or execution arrows. Horizontal and vertical whiskers are uncertainty, not directional movement.

**Transfer.** Show cost uncertainty when its variability matters, instead of treating cost as exact. Keep architecture symbols consistent with adjacent figures. State the uncertainty statistic and averaging population in the caption.

**Do not copy.** Do not copy the pale contrast at reduced size. The three x scales differ substantially; compare numeric ticks rather than panel position. Do not infer a Pareto frontier from noisy aggregated means alone.

<a id="titans"></a>
### Titans: Learning to Memorize at Test Time

**Google / DeepMind; first submitted 2024-12-31; inspected v1 dated 2024-12-31.** [Versioned PDF](https://arxiv.org/pdf/2501.00663v1) · [Organization evidence](https://research.google/pubs/titans-learning-to-memorize-at-test-time-2/)

PDF p1 explicitly lists Google Research for all authors. The 2501 arXiv identifier must not be interpreted as first-submission year: this PDF was submitted 2024-12-31. The official Google page separately identifies a NeurIPS 2025 publication.

PDF SHA-256: `a65e4a7d02784df1a040b487127e6dd09fff4474e5caf94d93263af3d50cfbc2`.

#### Figure 1 — From sequential memory updates to parallelizable operations

PDF page 7; crop `[120, 74, 520, 158]`; family: compact algorithm strip with concrete sequence objects.

**Layout.** A low, wide strip is divided into within/cross-chunk behavior, momentum computation, and weight decay. Repeated short token strips anchor each operation.

**Information layers.** Chunk-local versus cross-chunk dependencies → Parallel computation of updates → Equivalent implementation forms → Effect of decay on the update expression.

**Detail devices.** Repeated colored token cells; Solid versus dotted dependency arcs; Operator symbols beside tensor strips; Equations in a separate rounded inset.

**Density and composition.** The wide aspect ratio compresses three computational ideas into a caption-height strip. Richness comes from repeated objects and small operator diagrams, although source type is tiny. Dashed vertical rules establish module boundaries without large boxes. Amber and sage routes distinguish the two dependency types. Muted rose identifies the updated endpoint cell consistently.

**Color.** Sequence cells: #65657E (raster_sampled_composited); Updated cell and momentum routes: #9B5353 (raster_sampled_composited); Within-chunk route: #DF9F3D (raster_sampled_composited); Cross-chunk route: #6C7869 (raster_sampled_composited).

**Typography.** All visible artwork is raster. Serif labels and math are visible, but exact family, size, and vector stroke widths cannot be recovered.

**Routing.** Short dependency arcs terminate on actual token cells. A compact curved arrow in the decay inset indicates a local transformation of the expression.

**Transfer.** Use token-level objects to explain a parallelization claim. Keep an updated cell visually identifiable across equivalent operations. Separate dependency type from implementation primitive.

**Do not copy.** Do not use a tiny strip if the equations are central to the argument. Avoid implying exact sequence length from schematic cell counts unless stated.

#### Figure 2 — Memory as context with three state lifetimes

PDF page 8; crop `[90, 70, 550, 213]`; family: swimlane architecture with explicit token composition.

**Layout.** Three colored horizontal bands distinguish contextual memory, core computation, and persistent memory. A narrow right-side column states the corresponding test-time status.

**Information layers.** State lifetime → Retrieval and update paths → Composition of the attention input → Readout gating → Training status at test time.

**Detail devices.** Neural memory cubes; Token strip assembled from three sources; Dashed token-correspondence leaders; Distinct retrieval and update blocks; Frozen-state symbol and status column.

**Density and composition.** A rich architecture remains readable because the lane system gives each object a stable home. The actual token concatenation is the mechanism-bearing detail. Pale cream, blue, and rose bands map semantics rather than visual decoration. The status column mirrors lane heights exactly. Retrieval and update share sage blocks and the memory object is repeated at each end.

**Color.** Contextual-memory band: #FFF8E3 (raster_sampled_composited); Core band: #E5EDF1 (raster_sampled_composited); Persistent-memory band: #F8E3E3 (raster_sampled_composited); Retrieval/update block: #989E8E (raster_sampled_composited); Attention block: #9393A5 (raster_sampled_composited); Computation routes: #9B5353 (raster_sampled_composited).

**Typography.** One raster occurrence contains the complete diagram; exact typeface and point size are unknown.

**Routing.** Left-to-right main path; contextual memory branches upward; persistent tokens enter from below. Dashed diagonal leaders specify token correspondence, while solid rose arrows carry computation.

**Transfer.** Use lanes for state lifetime or ownership, not arbitrary grouping. Show how objects concatenate into a downstream input. Mirror state status in a compact aligned side column.

**Do not copy.** Do not add diagonal correspondence leaders without explicit source/target cells. Rebuild raster labels as vector text and avoid relying on the frozen icon alone.

<a id="fast-blt"></a>
### Fast Byte Latent Transformer

**Meta / FAIR; first submitted 2026-05-08; inspected v1 dated 2026-05-08.** [Versioned PDF](https://arxiv.org/pdf/2605.08044v1) · [Organization evidence](https://arxiv.org/abs/2605.08044v1)

PDF p1 lists FAIR at Meta, Stanford University, and University of Washington as numbered affiliations.

PDF SHA-256: `7957dd70eb7175a86bdcb1f8e8fca2f1444a348c0058dc924633f892d7efc8a2`.

#### Figure 1 — Three successive states of block-diffusion byte generation

PDF page 2; crop `[70, 63, 570, 295]`; family: worked token execution trace.

**Layout.** Three side-by-side time snapshots repeat the same encoder/global-model/decoder structure. Concrete byte cells accumulate across the snapshots and masked cells show the pending block.

**Information layers.** Encoder/global/decoder hierarchy → Byte-to-patch grouping → Generated versus masked content → State progression across calls.

**Detail devices.** Literal byte cells; Larger latent-patch boxes; Dashed masked-block enclosures; Dotted inter-snapshot transitions; Consistent three-tier module placement.

**Density and composition.** High but intelligible density: a reader can follow the same short example across three states. The objects carry the explanation more effectively than prose inside generic blocks. Yellow byte cells remain visually distinct from green encoder and blue decoder representations. The middle global model is orange/red, with broader whitespace around it. The same masked-block outline reappears in the legend and in each state.

**Color.** Byte cell: #FFF2CD (vector_measured); Byte-cell border: #DEC36F (vector_measured); Encoder representation: #D9EAD3 (vector_measured); Decoder representation: #C9DAF8 (vector_measured); Latent/global representation: #FFE8DB (vector_measured); Masked-block routes: #FF6393 (vector_measured).

**Typography.** Visible embedded text has opaque font000... aliases; the exact family is unidentified. Source sizes include roughly 6.78–8.49 pt for ordinary labels, with larger operator symbols. Three raster occurrences also occur in the crop.

**Routing.** Local computation runs bottom-to-top. Dotted pink curves represent progression between snapshots; solid gray edges map bytes and patches within a snapshot.

**Transfer.** Use a concrete short sequence to expose the algorithm. Keep module positions identical across execution snapshots. Distinguish time progression from within-step computation using line style.

**Do not copy.** Add explicit step numbers when the generation order could be ambiguous. Do not depend on red/green distinctions alone; retain shape, labels, and dashed boundaries. The source PDF font names are opaque aliases and must not be presented as a known typeface.

#### Figure 5 — Decoder closeup linked to two attention-mask matrices

PDF page 9; crop `[70, 62, 570, 250]`; family: multiscale architecture plus explicit incidence matrices.

**Layout.** A miniature full model on the left expands into the decoder internals at center. Two matrices on the right use the same byte/patch objects as row and column headers.

**Information layers.** Whole-model location → Decoder sublayers → Clean and corrupted sequences → Cross-attention permissions → Self-attention permissions → Two prediction objectives.

**Detail devices.** Numbered callout badges; Dashed zoom connectors; Repeated literal byte cells; Rotated patch-header cells; Attention matrices with explicit index labels; Matching pink/green boundaries in sequence and matrix views.

**Density and composition.** Very high density with a strong cross-scale mapping. It is one of the clearest sources for adding technical richness, but the inspected source placement has many labels near 3–5 pt. The central detail panel is larger than the model thumbnail. Darker purple matrix cells encode a discrete state; pale purple cells preserve the complete matrix grid. Object identity remains stable from input through output and into the matrix axes.

**Color.** Inactive/light matrix cells: #D9D2E9 (vector_measured); Active/dark matrix cells: #674EA7 (vector_measured); Matrix grid: #351C75 (vector_measured); Byte cells: #FFF2CD (vector_measured); Masked/corrupted objects: #FF6393 (vector_measured); Clean-object annotation: #38761D (vector_measured).

**Typography.** Visible text uses opaque embedded font aliases rather than a recoverable family name. Many ordinary labels are measured at 3.20–4.89 pt, a concrete legibility risk at source placement.

**Routing.** Blue dashed lines connect the overview to the enlarged decoder. Pink dotted guides connect internal operations to the appropriate matrix. Internal attention curves are confined to their sublayer.

**Transfer.** Use matrices when they expose exact permitted interactions. Repeat real token labels on both the schematic and matrix axes. Associate each matrix with one numbered operation and one clear connector. Allocate enough final width for matrix headers rather than shrinking every element.

**Do not copy.** Provide an explicit allowed/blocked-cell legend in a new figure. Do not adopt the source 3–5 pt lettering as acceptable output size. Limit arbitrary accent colors; the diagram already uses many categorical channels.

<a id="perception-lm"></a>
### PerceptionLM: Open-Access Data and Models for Detailed Visual Understanding

**Meta / FAIR; first submitted 2025-04-17; inspected v3 dated 2025-07-23.** [Versioned PDF](https://arxiv.org/pdf/2504.13180v3) · [Organization evidence](https://arxiv.org/abs/2504.13180v3)

PDF p1 lists Meta FAIR and Meta Reality Labs plus academic collaborators; the internship footnote explicitly names Meta.

PDF SHA-256: `af62f17abd55e038860539940b41ca082becb250dbdc5d3ab8bd1db75f2ce130`.

#### Figure 5 — Spatial masks tied to temporal caption intervals

PDF page 6; crop `[106, 442, 506, 570]`; family: qualitative triptychs with temporal grounding.

**Layout.** Three equal example cards each contain a three-frame filmstrip and caption intervals underneath. A shared lavender title bar spans the complete row.

**Information layers.** Video example → Spatially selected entity → Time interval → Language description → Explicit out-of-frame intervals.

**Detail devices.** Mask overlay maintained across frames; Short timeline bars beneath the strip; Color-associated interval text; Three-frame temporal sampling; Equal-size example cards.

**Density and composition.** High semantic density in a compact row: each card answers who/where, when, and what. The visible small text is the limiting factor, not the organization. The saturated blue mask is the only strong color on each photograph. Subtle card backgrounds keep natural-image color from becoming the grouping system. Intervals and captions stay directly beneath the corresponding frames.

**Color.** Title strip: #D3D5ED (vector_measured); Timeline background: #D7DBE7 (vector_measured); Interval accent: #B1AFD0 (vector_measured); Stronger interval accent: #596B95 (vector_measured); Card ground: #D2D5EC at alpha 0.150 (vector_measured).

**Typography.** Visible Montserrat-Regular at 4.9527 pt and Montserrat-Bold at 5.77815 pt; photographic frames are raster. These exact measurements are source observations, not recommended label sizes.

**Routing.** No arrows are needed: spatial alignment and repeated card grammar provide the correspondence. Timeline bars encode intervals, not measured model performance.

**Transfer.** Pair spatial evidence with a synchronized temporal annotation. Keep frame crops and their timelines aligned. Show absent/out-of-frame states explicitly when they matter.

**Do not copy.** Do not use tiny caption paragraphs; choose fewer examples or enlarge the panel. Do not let a decorative video-control bar imply an interactive artifact. Preserve exact interval semantics when remaking the figure.

#### Figure 6 — Five task definitions shown through matched worked examples

PDF page 7; crop `[106, 178, 506, 309]`; family: task taxonomy as visual example cards.

**Layout.** Five narrow cards share title bars, image placement, and text hierarchy. The last card includes a paired temporal view to represent its denser task.

**Information layers.** Task family → Observed visual evidence → Question format → Expected answer structure → Spatial/temporal grounding where needed.

**Detail devices.** Consistent question/answer typographic hierarchy; Mask-highlighted target regions; Task-specific answer format; One aligned row of visual examples.

**Density and composition.** The card grammar supports rapid comparison across five task types, but the 4.19 pt body text is too small to reproduce. A new figure should use fewer columns or place detailed wording in the caption. Lavender headings unify the cards without assigning five unrelated colors. Images occupy a consistent top band; questions and answers align below it. Task differences are communicated by the content and mask/interval objects rather than by decorative icon changes.

**Color.** Card title strips: #D3D5ED (vector_measured); Card ground: #D2D5EC at alpha 0.150 (vector_measured); Media frame: #F3F3F3 (vector_measured).

**Typography.** Visible Montserrat-Regular at 4.18725 pt; bold labels at 4.74555 and 5.86215 pt. Eighteen raster placements provide the visual examples and related media fragments.

**Routing.** No process arrows. Parallel layout expresses taxonomy; it must not be read as a sequential pipeline.

**Transfer.** Show a concrete input/output example for every claimed task family. Use identical card anatomy to make differences comparable. Vary the evidence object only when the task requires it.

**Do not copy.** Avoid five columns of tiny prose in a new figure. Do not turn taxonomy cards into a pipeline with unjustified arrows.

<a id="pe-av"></a>
### Pushing the Frontier of Audiovisual Perception with Large-Scale Multimodal Correspondence Learning

**Meta / FAIR; first submitted 2025-12-22; inspected v1 dated 2025-12-22.** [Versioned PDF](https://arxiv.org/pdf/2512.19687v1) · [Organization evidence](https://ai.meta.com/research/publications/pushing-the-frontier-of-audiovisual-perception-with-large-scale-multimodal-correspondence-learning/)

PDF p1 places the author team under Meta Superintelligence Labs.

PDF SHA-256: `e3f717d0c8c1111cb6c8b07e24390efdf936913d19d0cae3e1967b98402842fd`.

#### Figure 2 — Multimodal encoders with an explicit alignment-loss inventory

PDF page 3; crop `[160, 60, 455, 214]`; family: modality architecture with aligned relationship key.

**Layout.** The encoder hierarchy occupies the left two-thirds; a narrow right column enumerates single-modality, fused-modality, and fine-tuning-only alignment relations.

**Information layers.** Raw modality input → Encoder hierarchy → Fused representation → Text representation → Pairwise learning objectives → Stage-specific objectives.

**Detail devices.** Waveform and film input glyphs; Stacked frame encoder; Named pooled output tokens; Bidirectional relation list; Dashed enclosure for fine-tuning-only objectives.

**Density and composition.** Moderately rich without overcrowding: the loss inventory removes many crossing edges from the architecture while retaining exact pairwise relationships. Teal, blue, and purple consistently distinguish audio, video, and text. Pale tinted blocks support darker outlines and labels. The relationship inventory is visually a key, not a second disconnected architecture.

**Color.** Audio ground: #E8EFEC (vector_measured); Video ground: #E1EAF2 (vector_measured); Text ground: #D1D7ED (vector_measured); Audio/video route: #00546A (vector_measured); Text outline: #613F8B (vector_measured).

**Typography.** Visible labels have an opaque font000... name and cannot be assigned an exact human-readable family. Measured label sizes span approximately 4.54–7.75 pt; italic sans-serif role labels are visually evident.

**Routing.** Main modality streams move upward. The loss inventory uses bidirectional arrows to denote alignment relations; these are not dataflow arrows.

**Transfer.** Move a dense set of pairwise learning relationships into an aligned relation key. Distinguish representation fusion from loss alignment. Use a dashed subregion for stage-specific objectives.

**Do not copy.** Keep abbreviations close to their full definitions. Do not imply a bidirectional runtime communication path from a contrastive-loss arrow.

#### Figure 13 — Repeated collectives replaced by a batched communication structure

PDF page 27; crop `[68, 120, 545, 230]`; family: before-and-after distributed-computation topology.

**Layout.** Two side-by-side diagrams retain six modality objects and three loss objects. The left repeats a communication primitive per input; the right groups modalities into two batched operations.

**Information layers.** Input modalities → Communication collectives → Batch concatenation/splitting → Loss-pair relationships → Before/after equivalence.

**Detail devices.** Identical modality ordering; Repeated loss cards; Explicit operation-count change; Consistent modality palettes; Two shared batched-operation bars.

**Density and composition.** The diagram is information-dense because its topology is the claim: the viewer can count the communication objects and trace unchanged loss endpoints. Curved edge crossings remain a readability weakness. Purple highlights the operation being optimized. Input cards preserve semantic color across the two panels. The optimized side has a deeper hierarchy but fewer communication bars.

**Color.** Audio/video modality ground: #E6EFEC (vector_measured); Text-associated modality ground: #C3D8F0 (vector_measured); Collective-operation ground: #E3E4F6 (vector_measured); Collective outline: #8F50BB (vector_measured); Routes: #134F5C (vector_measured).

**Typography.** Main diagram text is visibly embedded at about 4.467 pt under opaque font aliases. SFRM0900 near 8.97–9.00 pt belongs to the subcaptions, not the small operation labels.

**Routing.** Curved edges connect specific modality pairs to losses. The batched operation is an explicit intermediate node, so bundling is a computation rather than an unexplained visual junction.

**Transfer.** When claiming a systems optimization, show exactly which repeated operation is removed or shared. Hold inputs and outputs in the same order before and after. Make batch/communication boundaries visible as named objects.

**Do not copy.** Do not hide topology in unlabeled edge bundles. Reduce or separate crossings in a new version. Use larger than the source approximately 4.47 pt labels.

<a id="movie-gen"></a>
### Movie Gen: A Cast of Media Foundation Models

**Meta / FAIR; first submitted 2024-10-17; inspected v2 dated 2025-02-26.** [Versioned PDF](https://arxiv.org/pdf/2410.13720v2) · [Organization evidence](https://ai.meta.com/research/publications/movie-gen-a-cast-of-media-foundation-models/)

PDF p1 credits the Movie Gen team at Meta and gives the official Meta project link. The inspected arXiv revision is dated 2025-02-26; the report cover date remains 2024-10-04 and first arXiv submission is 2024-10-17.

PDF SHA-256: `60fd60a970245ec8e8fda77f04cf6ca0322b8eff5174da8faf28477a035075e5`.

#### Figure 8 — Parallelization semantics attached to a transformer and its tensor dimensions

PDF page 11; crop `[70, 62, 545, 354]`; family: architecture plus dimension ledger.

**Layout.** A color key at far left maps parallelization strategies. A central vertical transformer block shares colors with a right-hand dimension ledger, separated by a dashed rule.

**Information layers.** Layer sequence → Parallelization strategy → External context inputs → Feature dimensions at selected points → Fixed training configuration.

**Detail devices.** Color-matched strategy legend; Explicit query/key/value objects; Side-entry conditioning routes; Repeated objects in a dimension ledger; Aligned numeric tuple column.

**Density and composition.** High technical density remains organized because numerical details live in a dedicated panel. The ledger adds reproducibility value without placing long tuples on every architecture edge. One pale blue-gray container groups the transformer and another groups the ledger. The same colored objects reappear beside their dimensions, creating direct lookup. A wide gap and dashed divider separate computation from annotation.

**Color.** Sequence-parallel blocks: #A4D8FF (vector_measured); Data-parallel/context blocks: #D2D2FF (vector_measured); Key/value strategy: #FAB9E6 (vector_measured); Query strategy: #C42F8F at alpha 0.749 (vector_measured); Feed-forward tensor strategy: #00D6BE (vector_measured); Structural containers: #F0F4F7 (vector_measured); Routes: #156082 (vector_measured).

**Typography.** Visible Optimistic-Regular at about 6.210–7.097 pt and Optimistic-Bold at 8.772 pt; a few ArialMT characters occur. Font identity is observed in the source, not a production dependency.

**Routing.** Main computation runs upward; external context and positional inputs enter from the side. The right panel has no execution arrows because it is a property table.

**Transfer.** Attach tensor shapes to selected landmarks through an aligned ledger. Reuse the identical color/object between architecture and shape annotation. Keep the hardware strategy key separate from the functional layer labels.

**Do not copy.** Do not assume a color describes only one concept unless the legend makes it explicit. The magenta source fill has approximately 0.749–0.753 opacity; retain that transparency when interpreting its appearance. Do not copy a proprietary font requirement into the skill; use a licensed available substitute.

#### Figure 17 — Matched image crops separated by diagonal before/after seams

PDF page 27; crop `[75, 520, 540, 637]`; family: qualitative detail comparison strip.

**Layout.** Four equally sized close crops form one row. A thin diagonal white seam divides each crop into pre- and post-upsampling regions.

**Information layers.** Four different visual textures → Before/after rendering detail → Shared scene landmarks.

**Detail devices.** Matched spatial crops; Consistent seam angle; Equal panel sizes; Edge, fur, petal, and vehicle-detail examples.

**Density and composition.** Low textual density but high image-detail density. The fixed closeup scale makes fine texture visible; the missing local before/after labels and absent parent image constrain interpretation. White gutters keep strong photographic colors from merging. The comparison boundary is thinner than any scene edge. All four panels use the same visual rule, so the viewer does not learn a new comparison format per image.

**Color.** Comparison seam: #FFFFFF (vector_measured).

**Typography.** No visible text occurs in the inspected artwork region. Eight raster placements and four white seam strokes form the strip; photographic colors are content, not a reusable palette.

**Routing.** No arrows. The diagonal seam is a comparison boundary, not a geometric feature in the scene.

**Transfer.** Keep matched crop locations and the same output size for qualitative comparisons. Choose examples that expose different relevant failure modes. Add a parent-image ROI inset and explicit before/after labels in a new figure.

**Do not copy.** Do not rely entirely on the caption to identify sides. A diagonal split compares different spatial locations across most of the image; provide a full matched pair for exact pixel-level assessment. Do not use this format as proof of quantitative improvement.

<a id="cosmos-transfer1"></a>
### Cosmos-Transfer1: Conditional World Generation with Adaptive Multimodal Control

**NVIDIA; first submitted 2025-03-18; inspected v2 dated 2025-04-01.** [Versioned PDF](https://arxiv.org/pdf/2503.14492v2) · [Organization evidence](https://arxiv.org/abs/2503.14492v2)

PDF p1 identifies NVIDIA as the author organization. PDF cover date 2025-04-03 differs from arXiv v2 submission date 2025-04-01.

PDF SHA-256: `c9d0256d1a066ed7a165cb1f62b1fee097f15e776a7f792d1998379c6fb0a6d9`.

#### Figure 2 — Layer-matched multimodal control branches

PDF page 3; crop `[65, 88, 530, 330]`; family: control architecture with repeated aligned branches.

**Layout.** A main denoising trunk at left is aligned with two displayed modality branches. An ellipsis represents intervening modalities. Corresponding layers share horizontal ranks.

**Information layers.** Base denoising model → Conditioning modalities → Layerwise control features → Spatial/temporal weighting → Injection into the common trunk.

**Detail devices.** Repeated transformer ranks; Explicit linear projection nodes; Multiplication and summation operators; Indexed feature and weight notation; Collapsed repeated depth.

**Density and composition.** Rich in topology even though monochrome: the drawing exposes where every control contribution enters and how it is weighted. The distinct operations matter more than added color. White rectangles and black outlines keep the weight equations and layer matching dominant. All displayed branches use the same block widths and layer spacing. The main trunk extends below the controlled layers, making scope explicit.

**Color.** Visible structure: #000000 (vector_measured); Blocks: #FFFFFF (vector_measured).

**Typography.** Visible Calibri labels are about 7.764–7.767 pt; CambriaMath provides indexed variables around 5.667–7.767 pt. The inspected region contains no raster images.

**Routing.** Downward trunk and branch flows; horizontal/orthogonal connectors merge corresponding control ranks. Junctions use explicit sum/product symbols rather than ambiguous intersections.

**Transfer.** Align repeated computational ranks across parallel branches. Put weighting and merge operators at the actual connection point. Use ellipses only for truly repeated, specified structure.

**Do not copy.** Do not color every branch merely to add polish. Some overlapping horizontal routes could be separated into dedicated channels. Zero-opacity black strokes in the extracted PDF are not visible line evidence.

#### Figure 6 — Spatial control masks connected to a generated scene

PDF page 10; crop `[66, 324, 533, 588]`; family: mechanism grounded in a physical-scene example.

**Layout.** Four aligned input-modality rows at left are paired with four binary control maps. They merge into one generated scene at right, with the text prompt above it.

**Information layers.** Same physical scene under four modalities → Foreground/background weighting regions → Combination of control branches → Prompt conditioning → Generated result.

**Detail devices.** Matched scene geometry across modalities; Binary spatial masks; Shared merge operator; Prompt inset; One large output panel.

**Density and composition.** High visual density is purposeful: the viewer can see exactly which pixels each modality controls. The repeated scene is a shared landmark across all rows. Natural image color is confined to the input/output evidence. Black and white masks expose the weighting partition. The output is substantially larger than one input thumbnail, allowing retained and changed details to be inspected.

**Color.** Routing and mask dark state: #000000 (vector_measured); Mask light state: #FFFFFF (vector_measured).

**Typography.** Visible Charter-Roman labels include about 8.842 pt for modality headings and 6.920 pt for prompt text; the sum glyph uses CambriaMath. Nine raster occurrences provide scene and mask content.

**Routing.** Each modality feeds its matching mask, then the rows merge through an explicit sum operator. A separate top-down prompt arrow enters the output path.

**Transfer.** Place the actual control map next to the input it weights. Keep the scene framing identical across modalities. Make the generated result large enough to inspect the claimed preservation/change.

**Do not copy.** Do not call white a weight of one here: the source caption specifies white as 0.5 and black as 0.0. Add a local numeric mask key in a new version. Do not treat arbitrary segmentation colors as the figure palette.

<a id="cosmos25"></a>
### World Simulation with Video Foundation Models for Physical AI

**NVIDIA; first submitted 2025-10-28; inspected v2 dated 2026-02-24.** [Versioned PDF](https://arxiv.org/pdf/2511.00062v2) · [Organization evidence](https://research.nvidia.com/labs/dir/cosmos-predict2.5/)

PDF p1 identifies NVIDIA as the author organization. Cosmos-Predict2.5 and Cosmos-Transfer2.5 are covered in this ONE paper and count once. First submission is 2025-10-28 despite a 2511 identifier; v2 is 2026-02-24 and PDF cover date 2026-02-26.

PDF SHA-256: `2597170ef9e8128c1ec3c87aa1eaf321cd599268451da1f61aead325eca576fe`.

#### Figure 1 — Dataset construction with explicit filtering and deduplication internals

PDF page 5; crop `[63, 82, 535, 348]`; family: three-column data-engine decomposition.

**Layout.** A left acquisition/preparation column feeds a tall central filter stack, then a right captioning/deduplication/sharding column. Distinct artifact shapes show source collections, a database, and final datasets.

**Information layers.** Source-domain coverage → Preparation stages → Seven filtering criteria → Captioning and semantic deduplication → Sharded training output.

**Detail devices.** Stacked document glyphs for datasets; Database cylinder; Dashed inner filter cards; Two internal deduplication operators; Three aligned columns with one reserved transit corridor.

**Density and composition.** Moderately high density: one pipeline is decomposed only where choices matter. The tall filter container makes its internal checks visible without requiring a long single-row flow. A limited green/gray palette keeps the filter hierarchy clear. Stage outlines are stronger than dashed internal-card outlines. Source and output artifacts use matching stacked-sheet vocabulary.

**Color.** Stage outline: #76B900 (vector_measured); Stage fill: #E7FFBE at alpha 0.502 (vector_measured); Artifact and inner-card outline: #404040 (vector_measured); Route arrowheads: #595959 (vector_measured).

**Typography.** Visible Calibri: stage labels roughly 7.724–8.550 pt; source-domain labels around 4.47–4.89 pt. The source objects are vector, with no raster occurrences in this crop.

**Routing.** Main flow bends through three vertical columns. The long database-to-filter connector occupies a clear gap, keeping it away from labels and internal cards.

**Transfer.** Use a tall grouped stage to expose a meaningful sequence of checks. Differentiate datasets, persistent stores, and transformations by shape. Reserve a visible route corridor before placing densely populated containers.

**Do not copy.** Do not imply the filters are sequential if the implementation uses a different relation; state ordering semantics. The pale source fill is #E7FFBE at about 0.502 opacity, not an opaque pale-green token.

#### Figure 2 — Multimodal embedding extraction connected to a denoising block

PDF page 10; crop `[65, 82, 535, 318]`; family: system overview with tensor objects and internal block expansion.

**Layout.** The left half traces text/image/video inputs through a language/vision system into a text embedding. The right half expands the repeated denoising block, with three conditioning cases above and output tokens below.

**Information layers.** Modal inputs → Intermediate representation extraction → Projected embedding → Alternative conditioning masks → Repeated denoising sublayers → Time modulation → Denoised output.

**Detail devices.** Filmstrip input; Intermediate hidden-state strips; Concatenation/projection object; Three 3D token volumes with different conditioned slices; Nested normalization/attention/MLP stages; Side-entry time modulation.

**Density and composition.** Very high density with a clear two-system division. The tensor objects carry dimensional and conditioning information rather than acting as decoration. One green semantic family links the text-conditioning interface across the central divider. Distinct slice colors make alternative conditioning cases comparable. Internal operations are white on progressively darker green containers, creating depth without shadows.

**Color.** Model/interface outline: #76B900 (vector_measured); Inner green block fill: #B0E873 at alpha 0.502 (vector_measured); Internal operation boxes: #FFFFFF (vector_measured); Route/context gray: #7F7F7F (vector_measured).

**Typography.** Visible Calibri and Calibri-Bold labels around 4.860–6.309 pt coexist with 61 raster occurrences in the selected region. The raster token textures do not establish separate font or palette measurements.

**Routing.** The left path mostly descends then crosses right through a single embedding interface. Time modulation runs in an outside vertical corridor and enters the corresponding internal rows.

**Transfer.** Show where a representation is sampled, combined, and injected. Use matched tensor objects to compare conditioning patterns. Expand one repeated block and label its multiplicity rather than duplicating every layer.

**Do not copy.** Keep small inner labels readable; several source labels are near 4.86 pt. Do not imitate the 3D volume unless its slices have an explicit scientific meaning. The source contains mixed raster/vector components and semi-transparent fills; do not infer all colors from path counts.

<a id="dreamgen"></a>
### DreamGen: Unlocking Generalization in Robot Learning through Video World Models

**NVIDIA; first submitted 2025-05-19; inspected v2 dated 2025-06-17.** [Versioned PDF](https://arxiv.org/pdf/2505.12705v2) · [Organization evidence](https://research.nvidia.com/labs/gear/dreamgen/)

PDF p1 gives NVIDIA as affiliation 1 with numbered academic collaborators.

PDF SHA-256: `e4e2c5c9e664d9331adb49c230053a76cf5bb4c3501341f4d9b372ecc585684c`.

#### Figure 2 — From demonstrations to generated trajectories and policy training

PDF page 2; crop `[72, 54, 538, 318]`; family: four-stage overview with repeated concrete artifacts.

**Layout.** A 2×2 composition uses numbered horizontal stage bars. The same flower-watering scene appears in generation, pseudo-action labeling, and policy-training examples.

**Information layers.** Real demonstration input → Generated future video → Pseudo-action extraction → Synthetic trajectory dataset → Policy output.

**Detail devices.** Two actual scene examples; Initial-frame red emphasis; Temporal filmstrip; Action-chunk brackets; Stacked trajectory artifact; Small model/output glyphs.

**Density and composition.** Rich yet approachable: each of four stages contains a specific evidence object, and repetition of the same scene creates continuity. The stage labels supply reading order without long crossing arrows. Four muted header colors organize stages while photographic content provides the detail. The novel pseudo-action step gets a warm accent label. The generated video panel uses one initial frame and a compact two-frame future.

**Color.** Demonstration stage: #E3DACC (vector_measured); Generation stage: #BCD1CA (vector_measured); Pseudo-action stage: #CCCADC (vector_measured); Policy stage: #FCE1B8 (vector_measured); Pseudo-action accent: #D97857 (vector_measured); Initial-frame emphasis: #E40000 (vector_measured).

**Typography.** Visible Verdana stage labels at 10.40416 pt and italic explanatory text at 8.12825 pt; STIXGeneral supplies math. Eighteen raster occurrences provide scene imagery.

**Routing.** Short local arrows explain input-to-rollout and dataset-to-policy. Numbered headers carry global order, so the overall 2×2 layout does not need a large serpentine connector.

**Transfer.** Repeat one worked example through the pipeline. Use a local artifact to make each stage concrete. When the global order is numbered, keep arrows local and meaningful.

**Do not copy.** Label generated and observed imagery explicitly in a new figure. A generic neural-network icon is less informative than a compact policy input/output specification. Do not use the four pastel headers as an excuse for unrelated color categories.

#### Figure 3 — Two pseudo-action models with common frame-pair input

PDF page 4; crop `[130, 55, 480, 256]`; family: matched architecture pair with representation strips.

**Layout.** A wider inverse-dynamics model at left and a compact latent-action model at right use the same two scene frames. Both flow upward from paired inputs, but their internal representation types differ.

**Information layers.** Common frame-pair input → Vision/action encoders → Intermediate token groups → Action decoder or vector-quantized bottleneck → Predicted action or reconstructed frame.

**Detail devices.** Same input frames in both panels; Repeated token strips aligned with the corresponding encoder; Action-time sequence in a dashed enclosure; VQ codebook object; Outer skip/iteration routes.

**Density and composition.** Moderately dense and strongly comparative: the differing internal structures are visible because input examples and vertical orientation are controlled. Beige marks visual information, sage marks actions, and lavender marks the latent encoder/decoder path. The large warm transformer block forms the left panel center. Trapezoids make the right encoder/decoder pair visually distinct from transformer blocks.

**Color.** Visual representation: #E2DACB (vector_measured); Action representation: #BCD1CA (vector_measured); Latent-code model: #CBCADB (vector_measured); Transformer center: #DA7958 (vector_measured).

**Typography.** Visible Verdana labels around 7.654 pt, STIXGeneral for math around 4.67–6.94 pt, and serif subcaptions around 8.966 pt. Five raster occurrences contain the paired frames.

**Routing.** Bottom-to-top main paths. An iteration/conditioning path uses the outside edge of the left model; a skip path travels outside the right encoder/decoder body.

**Transfer.** Compare methods with the same concrete input and matching orientation. Use token strips to reveal what is concatenated or quantized. Place recurrence or skip routes outside the primary operator stack.

**Do not copy.** Explain the iteration index and action horizon in the caption. Do not infer equal model capacity from equal-looking panels.

<a id="dreamdojo"></a>
### DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos

**NVIDIA; first submitted 2026-02-06; inspected v1 dated 2026-02-06.** [Versioned PDF](https://arxiv.org/pdf/2602.06949v1) · [Organization evidence](https://github.com/NVIDIA/DreamDojo)

PDF p1 gives NVIDIA as affiliation 1 with numbered academic collaborators. PDF cover date 2026-02-09 differs from arXiv first submission 2026-02-06.

PDF SHA-256: `c8f02e22c8fbe98e0b50215e10e1f6baf2f589b1987e5c6dc07175bfe6fe8587`.

#### Figure 1 — Pretraining, embodiment transfer, distillation, and applications

PDF page 3; crop `[60, 82, 535, 285]`; family: dense system atlas with four named regions.

**Layout.** An asymmetric composition dedicates a left column to human-video sources, a top center to the base model and robot embodiments, a lower center to autoregressive distillation, and a right column to applications.

**Information layers.** Data diversity → General model training → Robot embodiment adaptation → Distilled temporal rollout → Downstream use cases.

**Detail devices.** Grouped thumbnail mosaics; A broad data-funnel shape; Named robot cutouts; Repeated clean/noisy frame slots; Gradient of temporal-state blocks; Application image cards with local labels.

**Density and composition.** Very high content density with a clear four-region story. Meaningful imagery and repeated temporal slots supply detail, while numbered stage tabs prevent the mosaic from becoming an unstructured gallery. Green is reserved for the model and its update path. Thin gray panel borders maintain separate scopes. Application labels are white on black strips over the image edge, maintaining contrast. The large center distillation region earns extra area because it carries the novel mechanism.

**Color.** Model and primary accents: #76B900 (vector_measured); Secondary green tint: #76B900 at alpha 0.500 (vector_measured); Funnel/pale state tint: #76B900 at alpha 0.200 (vector_measured); Panel structure: #CECECE (vector_measured); Image label ground: #000000 (vector_measured).

**Typography.** Visible text uses an Unnamed-T3 embedded font, so the exact family is unknown. Measured sizes include 7.279, 9.099, and 11.828 pt. Seventy-three raster occurrences supply the scientific imagery.

**Routing.** Local arrows connect noisy inputs, model outputs, and autoregressive frame groups. A broad source funnel shows aggregation rather than a numeric flow volume.

**Transfer.** Allocate area by explanatory importance rather than equal card sizes. Show data, mechanism, and applications at distinct visual scales. Use repeated temporal slots and frame landmarks to make distillation tangible.

**Do not copy.** Do not treat a collage of attractive pictures as evidence of breadth without labels and selection criteria. The light gray robot names are weak at reduced size. A varying green tint must not be interpreted as a numeric scale unless a scale is provided.

#### Figure 3 — Latent-action bottleneck paired with cross-domain frame examples

PDF page 6; crop `[70, 80, 525, 292]`; family: mechanism plus qualitative correspondence grid.

**Layout.** A narrow left architecture uses a frame pair to produce a latent action and reconstruct the next frame. The wider right region shows two groups of paired frames from different settings.

**Information layers.** Action bottleneck mechanism → Input/output temporal relationship → Cross-scene action correspondence → Different human/robot embodiments.

**Detail devices.** Repeated time-index badges; Fixed paired-frame grammar; Two visual groups with multiple examples; A visible single-vector bottleneck; Shared frame used in skip and encoded paths.

**Density and composition.** High visual density is justified by the correspondence claim. The grid is organized by paired transitions, so the evidence is motion-related rather than an unordered set of scenes. The green mechanism occupies about one-third of the width. Black time badges stay at the same top-left position on every frame. Image crops are matched within each pair; object and embodiment diversity are allowed across pairs.

**Color.** Latent-action modules: #76B900 (vector_measured); Latent-vector ground: #76B900 at alpha 0.200 (vector_measured); Temporal badges: #000000 (vector_measured); Bypass/context routes: #CECECE (vector_measured).

**Typography.** Visible labels use Unnamed-T3 with exact family unidentified; source sizes include 5.496, 7.328, and 9.160 pt. Eleven raster occurrences form the scene examples.

**Routing.** Downward encoder/bottleneck/decoder path on the left, with a pale outer skip route. The right is a comparison grid and does not imply flow between different examples.

**Transfer.** Give a correspondence grid one stable unit, such as a before/after frame pair. Keep temporal badges consistent across every example. Place a compact mechanism next to the evidence it predicts or explains.

**Do not copy.** Add action-group labels or captions so visual similarity is not the only evidence. A static pair does not fully establish motion quality; link a video or report an appropriate metric.

<a id="cosmos-policy"></a>
### Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning

**NVIDIA; first submitted 2026-01-22; inspected v1 dated 2026-01-22.** [Versioned PDF](https://arxiv.org/pdf/2601.16163v1) · [Organization evidence](https://research.nvidia.com/labs/cosmos-lab/cosmos-policy/)

PDF p1 gives numbered NVIDIA and Stanford University affiliations.

PDF SHA-256: `05696475c9b5481afbf88673a65f80a46cf3fb87a5755c1410e83d0f468cc6e0`.

#### Figure 2 — Video slots extended with actions, state, and value

PDF page 4; crop `[107, 82, 505, 241]`; family: aligned multimodal sequence transformation.

**Layout.** Three horizontal rows show raw image groups, an expanded latent sequence, and the partially noised target sequence. Green conditioning and rose target regions span all rows.

**Information layers.** Input images → Additional non-image modalities → Latent-frame positions → Conditioning/target split → Noising operation → Grouped state/action/future/value variables.

**Detail devices.** Fixed-position latent tiles; Actual multiview robot imagery; Red outlined injected modalities; A spanning injection annotation; Brackets matching mathematical variables; Noise texture only on target slots.

**Density and composition.** Very high information density is carried by exact alignment: the same slot position can be tracked through the transformation. This is an excellent template for explaining multimodal packing. Two quiet background colors encode the split, while red is reserved for newly injected objects. The left vertical labels explain row transformations. Camera-view labels sit directly above their corresponding tiles.

**Color.** Conditioning region: #F1FFE8 (raster_sampled_composited); Target region: #F8E1DB (raster_sampled_composited); Injected-modality outline: #A62C17 (raster_sampled_composited).

**Typography.** One raster image contains all visible text and geometry. Sans-serif labels and mathematical variables are visible, but no exact font family, point size, or vector stroke width is established.

**Routing.** Vertical transformation arrows live at the left margin. A horizontal injection spine drops into the extra modality slots; it does not cross the example images.

**Transfer.** Keep tensor/sequence positions fixed through transformations. Distinguish the content type from its conditioning/target status. Use real or clearly synthetic exemplars to explain otherwise abstract packed slots.

**Do not copy.** Do not imply photographic images are literally stored in action/value slots; explain the representation. Source artwork is raster; rebuild labels and shapes as vector. State which modalities are predicted jointly and which are supplied.

#### Figure 12 — One latent sequence reused for three training objectives

PDF page 21; crop `[107, 82, 506, 424]`; family: aligned objective comparison with shifting conditioning boundary.

**Layout.** A clean reference sequence spans the top. Three equal-width training rows below retain every slot in the same order while the conditioning/target boundary moves rightward.

**Information layers.** Common sequence schema → Policy objective → World-model objective → Value objective → Batch-mixture proportion → Observed versus noised slots.

**Detail devices.** One canonical reference row; Identical slot widths and ordering; Heavy boundary line at each task split; Grouped state/action/future/value brackets; Explicit mixture percentages; Matching objective formula above each row.

**Density and composition.** Exceptionally useful high-density comparison: most content is held fixed, making the task difference immediately visible. A new version could reduce repeated tiny labels and give the boundary more space. Rows share horizontal landmarks across the full figure. Rose versus pale green gives an immediate split cue while noise texture gives redundancy. The warm red border frames the training condition rather than marking model superiority.

**Color.** Conditioning slots: #F1FFE8 (raster_sampled_composited); Target slots: #F8E1DB (raster_sampled_composited); Objective frame and split: #A62C17 (raster_sampled_composited).

**Typography.** The complete figure is a single raster. Exact typeface and point size are unknown, and no vector-derived stroke width can be reported.

**Routing.** No process arrows are necessary: the shifting split in otherwise identical rows is the comparison. Brackets associate repeated slots with the same variables in every objective.

**Transfer.** For objective comparisons, hold the sequence schema fixed and vary only the scientific difference. Place a clean reference row above transformed or masked variants. Show training mixture proportions near the objective they weight.

**Do not copy.** Do not change slot width or ordering between rows for visual convenience. Source labels are raster and tiny; use shared column headers or an enlarged vector version. Keep the conditioning split semantically exact when adapting the pattern.

## Measurement and provenance cautions

- Visual conclusions are from the rendered selected crop, not from abstract text or a whole-page font list.
- Raw PDF RGB and opacity describe source objects before compositing. Raster samples describe rendered pixels and do not establish the original alpha.
- Nominally visible text can still be clipped or occluded; final roles were checked against the rendered crop. Hidden text and zero-opacity paths are not accepted as visible typography or palette evidence.
- Opaque font aliases, Type 3 glyphs, raster lettering, and outlined text do not establish a named font family.
- Stroke metadata may be transformed incorrectly. Implausible widths are excluded; widths surviving an automatic range check still require visual plausibility.
- Source-paper sizes are observed measurements, not minimum acceptable production typography. Path counts do not measure occupied visual area or aesthetic importance.

Source PDFs and figure crops are retained as inspection intermediates. They should not be included as copied artwork in the installable skill. The JSON stores portable evidence basenames, exact versioned URLs, hashes, pages, and crop coordinates.
