# OpenAI, Anthropic, and Microsoft figure-design expansion

Inspected 11 new papers/reports and 22 figure anchors on 2026-10-21. Nine sources are from 2025; two are from 2026.

Exact source color values are observations, not prescribed house styles. Raster samples are approximate rendered appearances. PDF point sizes and SVG user-unit sizes must not be confused. Native SVG previews used a fallback font; only declared families are reported.

## Contents

- [gpt-oss-120b & gpt-oss-20b Model Card](#gpt-oss)
- [Monitoring Monitorability](#monitorability)
- [GPT-6 Astra System Card](#astra)
- [HealthBench: Evaluating Large Language Models Towards Improved Human Health](#healthbench)
- [Magma: A Foundation Model for Multimodal AI Agents](#magma)
- [Agent Lightning: Train ANY AI Agents with Reinforcement Learning](#agent-lightning)
- [Phi-4-Mini Technical Report: Compact yet Powerful Multimodal Language Models via Mixture-of-LoRAs](#phi-mini)
- [Phi-4-reasoning-vision-15B Technical Report](#phi-vision)
- [Reasoning Models Don't Always Say What They Think](#reasoning-faithfulness)
- [Circuit Tracing: Revealing Computational Graphs in Language Models](#anthropic-circuit-tracing)
- [On the Biology of a Large Language Model](#anthropic-biology)

## Source studies

<a id="gpt-oss"></a>
### gpt-oss-120b & gpt-oss-20b Model Card
OpenAI · 2025 · v1
Source: https://arxiv.org/abs/2508.10925v1
Affiliation check: PDF title page names the company.

#### Figure 1 — Capability benchmark small multiples
Anchor: PDF page 6
- **Color:** 120b highlight #FFA726 (vector_measured); 20b highlight #FFE066 (vector_measured); o3 baseline #EDF8FE (vector_measured); o3-mini baseline #CEE0C8 (vector_measured); o4-mini baseline #B5C5AD (vector_measured)
- **Typography:** Glyphs are outlined: the PDF yields no visible font trace despite vector charts. Exact family/size are unverified.
- **Layout:** Three aligned panels above two centered panels. Model order and color roles repeat; larger HLE grouping occupies extra horizontal space.
- **Geometry/style:** Zero-based bars, black hairline outlines, labels directly above marks, multi-line panel titles, and no surrounding panel cards. The lower row avoids a meaningless empty third cell.
- **Routing:** No connectors; vertical mark alignment and repeated category order carry the comparison.
- **Transfer:** Use a persistent family palette across benchmarks, with warm highlights and subdued comparators. Choose panel widths from category count; a strict equal-cell grid is not always appropriate. Place values at the mark and reserve two-line labels below the axis.
- **Caution:** Do not infer uncertainty from bars without intervals. The 3+2 arrangement and crowded rotated labels can become too small at single-column width.

#### Figure 3 — Reasoning effort versus output length
Anchor: PDF page 8
- **Color:** 120b curve #FFA726 (vector_measured); 20b curve #FFD033 (vector_measured); 120b annotation #B2751B (vector_measured); 20b annotation #B29224 (vector_measured)
- **Typography:** exact family unverified
- **Layout:** Two side-by-side panels with one shared legend above. The same color identifies each model and circle versus square supplies redundant identity.
- **Geometry/style:** Logarithmic token axis; direct low/medium/high annotations are offset above or below the marks. Light dashed grid is source gray #B0B0B0 at approximately 0.18 opacity.
- **Routing:** Straight segments connect successive reasoning settings of the same model; these are trajectories, not a general fitted frontier.
- **Transfer:** Pair color with marker shape when two pale warm curves are close. Use darker related ink for annotations than for the marks themselves. Encode compute settings at the points to reduce legend indirection.
- **Caution:** Do not silently call connected operating points a Pareto frontier. The two panels use different y-ranges; retain explicit scales.

<a id="monitorability"></a>
### Monitoring Monitorability
OpenAI · 2025 · v1
Source: https://arxiv.org/abs/2512.18311v1
Affiliation check: PDF title page names the company.

#### Figure 2 — Monitorable and unmonitorable trace examples
Anchor: PDF page 4
- **Color:** unmonitorable trace fill #FFA0A4 (raster_sampled); monitorable trace fill #B8E9C4 (raster_sampled)
- **Typography:** The figure is one embedded raster; monospace/sans/serif classes are visible, exact families and point sizes are unavailable.
- **Layout:** Three equal columns represent evaluation archetypes. Within each column, a neutral problem precedes a red trace, a narrow audit strip, a green trace, and a second audit strip.
- **Geometry/style:** Rounded transcript cards use compact monospace text; external vertical row labels explain the red/green distinction. White audit strips keep truth and monitor outcome outside the conversational text.
- **Routing:** Alignment replaces arrows. A thin internal rule separates reasoning from answer within each trace.
- **Transfer:** Represent comparable failure and success cases in fixed row roles. Keep the evaluator result in a separate strip so it cannot be mistaken for generated content. Shorten excerpts while preserving the scientific distinction.
- **Caution:** Red and green alone are insufficient; keep explicit row labels and symbols. The source transcript text is very small. Use shorter excerpts or a zoom panel for print.

#### Figure 8 — Monitorability across token budgets and monitor scopes
Anchor: PDF page 17
- **Color:** orange model curve #F46920 (raster_sampled); blue model curve #7292F7 (raster_sampled); green model curve #01C159 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Three same-height panels correspond to CoT-only, action-only, and all-message observation. A single centered legend spans the trio.
- **Geometry/style:** Log x-axes, light vertical/horizontal guides, many short error bars, and compact axis headings keep conditions comparable.
- **Routing:** Within-model segments join measured budget settings; error-bar caps stay perpendicular and compact.
- **Transfer:** Use scope as a panel variable and model as color, keeping that assignment stable. Use identical y-ranges when the comparison is the point. Move the shared legend outside axes to preserve data area.
- **Caution:** Source text and legend are too small for comfortable print reuse at this physical size. Overlapping intervals require fewer curves per panel or a second figure, not thinner unreadable strokes.

<a id="astra"></a>
### GPT-6 Astra System Card
OpenAI · 2026 · Official PDF retrieved 2026-10-21
Source: https://deploymentsafety.openai.com/gpt-6-astra/gpt-6-astra.pdf
Affiliation check: PDF title page names OpenAI and dates the card 2026-09-03; the live official PDF was retrieved on 2026-10-21.

#### Figure 5 — Attack success after increasing attempt budgets
Anchor: PDF page 20
- **Color:** neutral budget shade dark #8C8A87 (raster_sampled); neutral budget shade medium #BAB8B7 (raster_sampled); neutral budget shade light #E3E3E2 (raster_sampled); blue family light #C7D8FC (raster_sampled); Astra family accent #C43C9A (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** A single wide chart compares many models. Within each model, success after k attempts is shown with nested lightness levels; most comparators are gray, while recent OpenAI families get blue and magenta.
- **Geometry/style:** Horizontal grid only, a bold chart title, a compact top-left attempt legend, and tiny numeric values at each level. The categorical baseline is flat with stacked multi-line names.
- **Routing:** No connectors; repeated ordering and cumulative bar heights reveal budget sensitivity.
- **Transfer:** Separate a categorical family color from an ordered lightness encoding. Use a highlighted subset only when the subset has a stated scientific role. Label nested cumulative quantities clearly to distinguish them from additive components.
- **Caution:** Do not imitate these bars as a conventional stacked composition: the quantities are cumulative at k attempts. Dense model labels need wider output or a horizontal redesign.

#### Figure 22 — Aggregate monitorability under three observation scopes
Anchor: PDF page 52
- **Color:** earlier model #405F9C (raster_sampled); Astra model #C43C9A (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Three aligned panels share a top-centered two-model legend, monitor description, and y-scale. Each panel isolates an observation scope.
- **Geometry/style:** Blue squares versus magenta circles provide redundant coding. Both curves carry narrow error bars, with very pale grids and restrained spines.
- **Routing:** Segments express successive token budgets, not causal influence between points.
- **Transfer:** Use a two-color pair plus two marker shapes for high-clarity conditional comparisons. Keep the monitor identity above the entire figure as a controlled-condition label. Align x-axis title baselines across panels.
- **Caution:** The source uses very small labels; enlarge type and shorten panel headings for a manuscript. A raster system-card figure does not reveal an exact font family.

<a id="healthbench"></a>
### HealthBench: Evaluating Large Language Models Towards Improved Human Health
OpenAI · 2025 · v1
Source: https://arxiv.org/abs/2505.08775v1
Affiliation check: PDF title page names the company.

#### Figure 1 — Conversation, candidate answer, and rubric alignment
Anchor: PDF page 2
- **Color:** candidate answer approximate fill #D0E3B6 (raster_sampled); user bubble approximate fill #ECF6DE (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Three columns have distinct roles: conversation, candidate answer, and rubric table. The response and rubric occupy matched vertical spans.
- **Geometry/style:** Light green conversation/answer surfaces sit on white. The rubric has ruled columns and boxed selected criteria. A score ruler sits beneath the rubric.
- **Routing:** Dotted correspondence lines connect exact answer passages to relevant rubric rows, while a small solid right arrow conveys the overall evaluation sequence.
- **Transfer:** Separate process flow from evidence correspondence using different line styles. Align explanatory table rows with their source passages where possible. Put the scoring summary next to the rubric rather than in a remote legend.
- **Caution:** Long medical text is an example artifact, not reusable scientific content. The source has gradients and tiny passage text; simplify fills and excerpt lengths for print.

#### Figure 2 — Performance versus inference cost
Anchor: PDF page 2
- **Color:** plot wash #EAEAF1 (raster_sampled); purple family approximate ink #9779B6 (raster_sampled); brown family approximate ink #8F7053 (raster_sampled); blue family approximate ink #708ED1 (raster_sampled); green family approximate ink #95D088 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** A compact square-ish plot labels model families directly beside isolated marks or short within-family trajectories; model release dates form a smaller second line.
- **Geometry/style:** Log cost axis and a pale lavender-gray plot wash. Several marker shapes separate operating settings; leader segments connect labels to points.
- **Routing:** Only selected within-family operating settings are connected. Labels are positioned around the marks rather than in a separate legend.
- **Transfer:** Direct labels work when each family has enough whitespace. Place historical/date context in a subordinate text line. Reserve one coherent plot wash; avoid combining it with tinted outer cards.
- **Caution:** Many pastel label colors have weak contrast; use darker related text colors in new figures. A headline containing frontier does not justify interpolating unmeasured performance. Keep monetary units and evaluation conditions explicit.

<a id="magma"></a>
### Magma: A Foundation Model for Multimodal AI Agents
Microsoft Research · 2025 · v1
Source: https://arxiv.org/abs/2502.13130v1
Affiliation check: PDF p1 names Microsoft Research, University of Maryland, University of Wisconsin-Madison, KAIST, and University of Washington.

#### Figure 1 — Capability overview with real examples
Anchor: PDF page 1
- **Color:** user prompt card source color #F7ECBF (vector_measured); model answer card source color #E2F0D9 (vector_measured, alpha 0.502); light-blue UI motif #DCEAF7 (vector_measured); card border #BFBFBF (vector_measured)
- **Typography:** Aptos 4.14 pt; Aptos,Bold 4.14 pt; Aptos,Bold 8.24 pt; Source Sans Pro 4.14 pt; Aptos,Bold 5.09 pt
- **Layout:** Three example columns progress from understanding to grounding to full agentic tasks; a narrow right rail shows physical and digital environments.
- **Geometry/style:** Real image/video thumbnails and short conversation snippets are nested inside rounded white cards. Pale neutral sweeps group columns; bold headings sit on the shared lower baseline.
- **Routing:** Dashed curved arrows in the right rail connect the agent to the two environment types. Example panels themselves rely on position and labels, not dense arrows.
- **Transfer:** Use real input/output miniatures when they explain a task more clearly than a generic box. Order panels by capability composition rather than by arbitrary modality. Give qualitative media a stable crop and repeated caption position.
- **Caution:** Source body labels around 4.14 pt and some around 3.54 pt are not a readable print target. Half-opacity source fills must be composited against white; do not copy raw hex as opaque. Company mascot/logo is not a transferable scientific element.

#### Figure 7 — Pretraining input and output lanes
Anchor: PDF page 8
- **Color:** input cards approximate cream #FCF7E4 (raster_sampled); output cards pale green #E2F0D9 (raster_sampled); token tint #F7ECBF (raster_sampled); model border #BDD7EE (raster_sampled); encoder gray #D9D9D9 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Input examples form a left column; encoders and token strips feed a tall central model card; output examples form a right column split into verbal, spatial-temporal, and action roles.
- **Geometry/style:** Vertical encoder labels conserve width. The center card is dominant but not oversized; short token strips make the encoding step visible. Braces label output families.
- **Routing:** Thin orthogonal routes move left to right through explicit encoder/token/model stages. The output branches are separated into lanes.
- **Transfer:** Use a token strip as a semantic transition between a media example and a model. Reserve model-area width according to its explanatory content. Use braces for family grouping and arrows for data flow.
- **Caution:** Do not copy unreadably small input questions; show representative fragments. Rasterized lettering prevents reliable font-family extraction.

<a id="agent-lightning"></a>
### Agent Lightning: Train ANY AI Agents with Reinforcement Learning
Microsoft Research · 2025 · v1
Source: https://arxiv.org/abs/2508.03680v1
Affiliation check: PDF title page names the company.

#### Figure 1 — Agent execution and RL training overview
Anchor: PDF page 2
- **Color:** paired loop arrows #DAB06C (raster_sampled); logo background cream #F8F0E3 (raster_sampled); small tool accent #0288D1 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Agent execution sits left and the RL engine right. Two broad exterior arcs enclose a central wordmark, with the top and bottom labeled as different transferred objects.
- **Geometry/style:** The overall composition is horizontally balanced and uses only a few main elements. Small agent/tool/database symbols explain heterogeneous execution.
- **Routing:** Top arc carries trajectories to the trainer; bottom arc returns updated models. Curves stay outside the content area.
- **Transfer:** Label each direction with the object being transferred. Reserve separate upper and lower corridors for feedback. Use a compact system overview before a more detailed architecture.
- **Caution:** Remove the logo from new scientific figures unless it is the subject. The same arrow color does not mean the two transferred objects are interchangeable.

#### Figure 4 — Training-agent disaggregation architecture
Anchor: PDF page 9
- **Color:** LLM engine blue fill #96DCF8 (raster_sampled); trainer peach fill #FBE3D6 (raster_sampled); framework group green #5FB042 (raster_sampled); server boundary strip #A02B93 (raster_sampled); client boundary strip #E97132 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Two rounded blue-boundary containers flank a dashed central coordination region. The left contains engine/trainer; the right is a vertical stack of agent frameworks.
- **Geometry/style:** Two opposing horizontal green arrows are aligned to their destination modules. Narrow colored bars mark server/client interfaces, and slanted labels attach to those interfaces.
- **Routing:** The top route sends the updated-model API rightward; the lower route returns rewarded traces leftward; a short local vertical arrow links trainer and engine.
- **Transfer:** Draw interfaces as boundary objects rather than floating nouns. Keep training and execution containers at the same visual level. Maintain separate transfer corridors with labels in the white gap above each line.
- **Caution:** Cross-container arrows still require explicit ports and boundary clearance. Green shades across framework examples need not become a new semantic taxonomy.

<a id="phi-mini"></a>
### Phi-4-Mini Technical Report: Compact yet Powerful Multimodal Language Models via Mixture-of-LoRAs
Microsoft Research · 2025 · v1
Source: https://arxiv.org/abs/2503.01743v1
Affiliation check: PDF p1 lists Microsoft as author; the title covers both Phi-4-Mini and multimodal models.

#### Figure 1 — Multimodal architecture and modality adapters
Anchor: PDF page 4
- **Color:** vision fill #A0D1C2 (vector_measured); vision outline #00B294 (vector_measured); audio fill #A0D7F7 (vector_measured); audio outline #00BCF2 (vector_measured); language fill #FFD199 (vector_measured); language outline #BF6900 (vector_measured); ink #404040 (vector_measured)
- **Typography:** Visible source text is Segoe UI about 8.218 pt for modules, 9.885 pt for a model label, and Segoe UI Bold about 4.407 pt for token labels.
- **Layout:** Three input lanes occupy the left two-thirds and a tall language-model stack the right third. Vision/audio lanes expose encoder, merging/projection, and token examples.
- **Geometry/style:** Large black modality icons head each lane. Color is repeated in modules, token tiles, and per-layer adapter rows. Token labels use a much smaller bold size than module labels.
- **Routing:** Downward modality paths merge into one interleaved strip. A long bottom route then enters the base of the model stack, which progresses upward to chat output.
- **Transfer:** Reuse one role color across the entire data-to-adapter path. Show interleaving with a short token example instead of an abstract merge box. Use shape and position to distinguish full modules, token tiles, and repeated layers.
- **Caution:** The bottom route changes reading direction; make the turn explicit and avoid border riding. Source token labels at 4.407 pt should be enlarged or simplified.

#### Figure 3 — Multimodal conversational example
Anchor: PDF page 17
- **Color:** subtle conversation border #EAEAEC (raster_sampled); body text approximate gray #6E6F71 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** A vertically stacked conversation aligns user requests on the right and assistant responses on the left. A waveform introduces the audio artifact before multiple transformations of the same input.
- **Geometry/style:** Near-white role cards, a pale warm user outline, tiny repeated role icons, and ample outer whitespace keep the sequence coherent.
- **Routing:** No arrows; turn order and alternating alignment encode conversation.
- **Transfer:** Keep one shared input visible while showing multiple derived outputs. Use explicit role labels in addition to alignment when removing product UI logos. Crop repeated content to meaningful excerpts.
- **Caution:** This screenshot is a readability counterexample at manuscript scale. Do not substitute brand logos for clear participant labels. Multilingual glyph support must be checked in the exported font.

<a id="phi-vision"></a>
### Phi-4-reasoning-vision-15B Technical Report
Microsoft Research · 2026 · Official PDF retrieved 2026-10-21
Source: https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/Phi-4-reasoning-vision-15B-Tech-Report.pdf
Affiliation check: PDF p1 states Microsoft Research / AI Frontiers and 2026-03-04.

#### Figure 2 — Accuracy versus time and token costs
Anchor: PDF page 3
- **Color:** Phi highlight #4C72B0 (raster_sampled); Kimi family #DD8452 (raster_sampled); Gemma family #55A868 (raster_sampled); Qwen family red #C44E52 (raster_sampled); Qwen family purple #8172B3 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Two aligned scatter panels reuse y-range and model encodings, switching the x-variable from average compute time to average completion tokens.
- **Geometry/style:** Marker shapes distinguish related settings, while a bold white callout names the target model. A large legend sits in the lower-right quadrant of each panel.
- **Routing:** No trajectories connect unrelated models. The callout uses a short leader rather than a heavy arrow.
- **Transfer:** Compare two distinct cost notions with matched panels. Use an explicitly named target callout rather than oversized target markers. Use color for family and shape for configuration only if both mappings are stated.
- **Caution:** The long repeated legends consume substantial data area; a shared legend is a better starting point for a new figure. Do not infer Pareto optimality from sparse observed points.

#### Figure 3 — Mid-fusion architecture
Anchor: PDF page 4
- **Color:** language/encoder outline #0F9ED5 (raster_sampled); blue gradient sample #9BCEF4 (raster_sampled); vision gradient sample #F4A186 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Image and text inputs form two lanes above a full-width aligned-token strip and shared language-model bar. Vision gets two stacked preprocessing modules, text one.
- **Geometry/style:** Rounded modules have stronger colored outlines and soft fills. The token strip supplies a third purple role. The shared bottom module is wider than individual branches.
- **Routing:** Short vertical arrows lead into the modules and out of the final language-model bar; branch alignment explains fusion without excessive crossing connectors.
- **Transfer:** Let width express shared scope after fusion. Use the token representation as the bridge between modality-specific and shared computation. Align input labels, modules, token row, and output on a small number of axes.
- **Caution:** Gradient samples are rendered appearances, not single source fill tokens. Check scientific topology when adapting: token alignment alone must not invent a missing operation.

<a id="reasoning-faithfulness"></a>
### Reasoning Models Don't Always Say What They Think
Anthropic · 2025 · v1
Source: https://arxiv.org/abs/2505.05410v1
Affiliation check: PDF p1 states Alignment Science Team, Anthropic.

#### Figure 1 — Faithfulness by hint type and model
Anchor: PDF page 2
- **Color:** Claude family #E59E66 (raster_sampled); DeepSeek family #66ABD0 (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Seven category groups compare two model families and reasoning/non-reasoning conditions. A compact 2x2 legend sits in the otherwise sparse upper-right region.
- **Geometry/style:** Hue identifies family; diagonal hatching identifies reasoning versions. Values sit above thin capped error bars; the y-axis spans 0–100%.
- **Routing:** No connectors. Equal within-group spacing and fixed legend order encode the factors.
- **Transfer:** Map orthogonal experimental factors to hue and texture rather than four unrelated colors. Use hatching sparingly and keep visible outlines/error bars. Retain direct values for near-zero cases that are otherwise hard to see.
- **Caution:** Hatch density must survive grayscale and final-size export. Near-zero value labels collide easily; use offsets or a small-value inset.

#### Figure 2 — Matched question with and without an injected hint
Anchor: PDF page 3
- **Color:** panel background #EFEDE6 (raster_sampled); assistant response #C9C9D9 (raster_sampled); comparison callout #E2CDCD (raster_sampled)
- **Typography:** exact family unverified
- **Layout:** Two matched columns share a vertical separator. White user cards appear above lavender assistant cards, while the hint is a small magenta text highlight within the right prompt.
- **Geometry/style:** The source case uses a warm off-white canvas and two pale neutral grouping panels. A muted rose callout sits below the left response and explains the behavioral difference.
- **Routing:** Two curved callout connectors point to the relevant response areas; these are explanatory leaders, not system data flow.
- **Transfer:** Hold prompt/response positions constant in counterfactual examples. Highlight only the changed input span. Use a bottom callout to state what changed and whether reasoning reveals the cause.
- **Caution:** Do not use this annotated example as evidence of frequency without accompanying measurements. Route leader endpoints to exact relevant spans rather than into arbitrary card interiors.

<a id="anthropic-circuit-tracing"></a>
### Circuit Tracing: Revealing Computational Graphs in Language Models
Anthropic · 2025 · Official web paper published 2025-03-27; retrieved 2026-10-21
Source: https://transformer-circuits.pub/2025/attribution-graphs/methods.html
Affiliation check: Official web paper author block names Anthropic and publication date March 27, 2025.

#### Opening diagram: methods-diagram-svg — Replacement model aligned to attribution graph
Anchor: https://transformer-circuits.pub/2025/attribution-graphs/figma/methods-diagram-svg.svg
- **Color:** context line #B8B6AD (vector_measured); context module #E6E3D6 (vector_measured); replacement path #CC6500 (vector_measured); replacement module #FFE6CC (vector_measured); selected graph circuit #633636 (vector_measured); inactive node #F6F6F3 (vector_measured)
- **Typography:** Roboto
- **Layout:** Two large regions share horizontal layer registration lines: a replacement-model schematic left and a token-by-layer attribution graph right.
- **Geometry/style:** The left uses rounded rectangular modules and circular addition junctions. The right uses circular features on four token columns. Sparse highlighted paths are thick brown; the large background graph is thin gray.
- **Routing:** Forward residual flow rises vertically; cross-layer additions curve right then re-enter explicit nodes. Graph paths preserve clear directional progression and a muted surrounding network.
- **Transfer:** Align a mechanism view and an abstract graph with shared layer guides. Mute structural context instead of deleting it when context explains the selected path. Use stroke thickness and saturation together for focus.
- **Caution:** Do not interpret opacity/width as numerical attribution without a declared mapping. A dense graph needs pruning plus a companion detailed view; color alone cannot rescue arbitrary hairballs.

#### Multiplicative patching: crosscoder-patching-tutorial-svg — Baseline and intervention passes
Anchor: https://transformer-circuits.pub/2025/attribution-graphs/figma/crosscoder-patching-tutorial-svg.svg
- **Color:** base computation #B8B6AD (vector_measured); module fill #E6E3D6 (vector_measured); recorded activation/copy #788C5D (vector_measured); intervention flow #CC6500 (vector_measured); intervention region #F6F6F3 (vector_measured)
- **Typography:** Roboto
- **Layout:** Baseline and intervention are parallel vertical columns with matched layers. A pale lower-right scope marks only the layers affected by the intervention.
- **Geometry/style:** Small disk/save symbols mark recorded values; modules are subdued, operation junctions are circular, and long dotted horizontal links represent copying stored activations.
- **Routing:** Green dotted routes copy baseline values; orange dotted routes copy intervention parameters; solid orange computation enters addition junctions. After the target layer, a discarded branch is explicitly marked.
- **Transfer:** Use spatial registration for before/after or control/intervention diagrams. Give stored values a compact artifact symbol and copying a separate edge style. Shade exactly the affected scope rather than the whole changed column.
- **Caution:** A web diagram of this height needs shortening for a paper. Do not preserve interactive-only labels or Figure 00 placeholders in a static export.

<a id="anthropic-biology"></a>
### On the Biology of a Large Language Model
Anthropic · 2025 · Official web paper published 2025-03-27; retrieved 2026-10-21
Source: https://transformer-circuits.pub/2025/attribution-graphs/biology.html
Affiliation check: Official web paper author block names Anthropic and publication date March 27, 2025.

#### Multi-step reasoning: dallas-capitial-big-svg — Token-to-supernode explanation
Anchor: https://transformer-circuits.pub/2025/attribution-graphs/figma/dallas-capitial-big-svg.svg
- **Color:** token and supernode fill #E6E3D6 (vector_measured); node outline #706D5C (vector_measured); graph edges #633636 (vector_measured); interaction annotation #CC6500 (vector_measured); neutral token strip #F6F6F3 (vector_measured)
- **Typography:** Roboto Mono; Roboto
- **Layout:** Input token strip anchors the bottom; output strip anchors the top. Supernodes occupy successive intermediate rows, with their vertical positions registered to contributing token locations.
- **Geometry/style:** Stacked-card outlines denote grouped features. A narrow orange right rail explains interactivity and a detailed-graph link sits beneath the main graphic.
- **Routing:** Brown orthogonal paths with rounded bends connect token contributions through concept nodes to output. The main story follows a three-step factual chain while supporting contributions remain present.
- **Transfer:** Ground abstract internal nodes in visible input/output tokens. Use stacked cards only when a node aggregates several features. Keep graph hierarchy legible before adding a full network.
- **Caution:** Interactive hover hints and detailed-graph buttons need replacement in a print adaptation. The simplified graph is an interpretation, not the full computational model.

#### Planning in poems: poems-hero-svg — Candidate planning paths tied to a text span
Anchor: https://transformer-circuits.pub/2025/attribution-graphs/figma/poems-hero-svg.svg
- **Color:** candidate/selected token fill #E6E3D6 (vector_measured); context background #F6F6F3 (vector_measured); node outline #706D5C (vector_measured); influence arrows #633636 (vector_measured); secondary prose #4D4D4D (vector_measured)
- **Typography:** Roboto Mono; Roboto
- **Layout:** A lower prompt strip opens into a rounded scope containing two candidate concepts; two upward arrows lead to alternative continuation strips near the top.
- **Geometry/style:** The shared scope is connected to an exact text span using a broad tapered bridge. A short explanatory paragraph sits in unused space to the left, with emphasis confined to key interpretation terms.
- **Routing:** Thin dark influence arrows are separate from the broad grouping bridge. The bridge expresses scope/association, not a quantitative flow.
- **Transfer:** Tie a conceptual inset to the relevant token span. Use the vacant side of an asymmetric diagram for one concise explanation. Distinguish grouping shapes from directional influence edges.
- **Caution:** Do not treat the broad bridge as a Sankey width. Remove web hover prompts in a static paper adaptation and preserve uncertainty in interpretive claims.

## Design recipes

### Registered control/intervention diagrams
Keep the same entities, layer heights, and role positions in both conditions; highlight the changed operation or prompt span and reserve explanatory callouts outside the primary flow.
Sources: anthropic-circuit-tracing: Multiplicative patching, reasoning-faithfulness: Figure 2
{"canvas": "178 mm, two aligned columns with 10–14 mm gap", "palette": {"context_fill": "#F1F0EA", "context_ink": "#6D726F", "intervention": "#C66516", "copied_state": "#718A58"}, "typography": "8–9 pt sans body, 9.5–10 pt bold panel titles; 7.5 pt minimum detail", "routing": "normal data solid, copied state dotted, annotation leaders thin; do not overload one edge with two meanings"}
Source-derived structural principle; recipe numbers are recommendations, not measurements.

### Token-grounded multimodal architecture
Repeat one modality color in the input, encoder/projector, token strip, and adapter; represent the actual merge or interleaving step with a small concrete token example.
Sources: phi-mini: Figure 1, magma: Figure 7, phi-vision: Figure 3
{"palette": {"vision_fill": "#DDEFE8", "vision_ink": "#257D69", "audio_fill": "#DBEEF9", "audio_ink": "#247CA7", "language_fill": "#FCE5C9", "language_ink": "#9A5B1B"}, "grid": "align lanes to common module heights; keep token labels outside tiles if text will fall below 7 pt", "routing": "reserve bottom or side corridors for any change of reading direction"}
Source-derived semantic color propagation; recommended accessible palette and sizes.

### Matched conditional small multiples
Assign one variable to panels and one to color/marker identity; keep scales, ordering, legends, and controlled-condition labels consistent. Separate operating trajectories from cross-model frontiers.
Sources: gpt-oss: Figure 3, monitorability: Figure 8, astra: Figure 22, phi-vision: Figure 2
{"typography": "8 pt axes, 9 pt panel titles, 7.5–8 pt shared legend", "marks": "1.1–1.4 pt main curves with 3–4 pt markers; lighter grid; error bars unobstructed", "palette": {"family_A": "#405F9C", "family_B": "#B4378D", "baseline": "#899095"}, "layout": "shared legend above the panel set; show per-panel scales when they differ"}
Source-derived layout; production values are recommendations.

### Evidence and rubric correspondence
Keep source text, generated response, and evaluator judgment visually distinct. Use dotted correspondence leaders for evidence mapping and solid arrows only for actual process order.
Sources: healthbench: Figure 1, reasoning-faithfulness: Figure 2
{"layout": "three role columns with aligned evidence passages and rubric rows", "content_budget": "short excerpts with explicit omissions; one score summary next to the rubric", "palette": "neutral evidence surface, one pale answer tint, one dark annotation accent"}
Source-derived structural principle; no clinical content or results are reused.

### Visibility and font provenance gate
Do not infer an exact font from a raster or outlined glyphs. SVG font-family declarations are not proof of the rendered browser font. Measure final physical size independently of source size; source examples with 3–4 pt detail are cautionary.
Sources: gpt-oss: Figures 1 and 3, magma: Figure 1, phi-mini: Figure 1, anthropic-circuit-tracing: native SVG assets
{"required_records": ["source medium", "font evidence class", "visible vs invisible traces", "declared vs rendered family", "source font size or unknown", "chosen final production size", "fallback used in preview"]}
Direct extraction/renderer limitation observed in this study.

## Counting exclusions

The two inaccessible 2026 Anthropic system cards and one incompletely rendered tutorial asset are not included in the counts. The two circuit papers are distinct primary publications; their web announcement is not counted separately.
