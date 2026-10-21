# Visual recipes from recent AI research

These eight recipes translate inspected 2025–2026 figures into concrete authoring choices. They are starting compositions, not templates to force onto unrelated science. **Observed** statements describe the exact cited source. **Authoring recipe** values are new recommendations at the final physical size. Do not present the recommended palette, dimensions or fonts as measurements of the source.

## Choose a recipe

| Reader needs to understand | Recipe | Main visual device |
| --- | --- | --- |
| How an algorithm maps to implementation | [1. Components and pseudocode](#1-components-and-pseudocode) | One role color repeated in modules and literal identifiers |
| What an intervention or architectural change changes | [2. Registered alternatives](#2-registered-alternatives) | Fixed landmarks, localized emphasis |
| How modalities become a shared representation | [3. Typed modality lanes](#3-typed-modality-lanes) | Concrete token strips and an explicit merge |
| Which operation is new and how it works | [4. Provenance overview and expansion](#4-provenance-overview-and-expansion) | Provenance key, typed objects, larger mechanism detail |
| What each stage produces | [5. Stage cards with real intermediate objects](#5-stage-cards-with-real-intermediate-objects) | Consistent outer grid, different meaningful interiors |
| Why an evaluator reaches a judgment | [6. Evidence and rubric correspondence](#6-evidence-and-rubric-correspondence) | Exact passages aligned with criterion rows |
| How results vary across tasks or conditions | [7. Conditional diagnostic matrix](#7-conditional-diagnostic-matrix) | Shared comparison structure and explicit scale policy |
| What persists or is reused across steps | [8. State and token schedules](#8-state-and-token-schedules) | Separate temporal/state regions; matched token positions |

## Common production settings

Start from a 178 mm wide figure when the mechanism needs several lanes or panels. Use 4–6 mm outer margins, a 2 mm spacing unit, 2–3 mm inner padding, and 4–6 mm clear routing gutters. At 85 mm, recompose vertically or show fewer panels; halving a 178 mm export also halves every label.

Use a verified installed sans family with actual regular and bold files; add monospace only for literal code, fields or tokens. Starting sizes are **9.5–10 pt headings, 8–8.5 pt main labels, and 7.5–8 pt secondary text**. Use 0.7–0.85 pt group boundaries, 0.85–1 pt module outlines, and 0.95–1.2 pt important routes. These numbers are recommendations, not venue rules. The manuscript template and final-size inspection govern the result.

For the bundled Matplotlib PDF export with `pdf.fonttype=42`, use a genuine TrueType program such as an available DejaVu Sans or Liberation Sans family. A `.ttf` extension alone does not verify the program format; an OpenType CFF program can produce a font-type mismatch in that export path. Other backends may support CFF correctly. Record the chosen font and any substitution, then inspect the rendered PDF. Source font declarations, source visibility, and chosen production fonts are separate facts.

Every color below needs a role, a text/shape redundancy where useful, and final-size contrast checks. See [design-tokens.json](../assets/design-tokens.json) for reusable role pairs and [reference-selection.md](reference-selection.md) for evidence tracking.

## 1. Components and pseudocode

**Use when:** a controller, search loop or agent algorithm becomes clearer when readers can match the conceptual system to a short executable or pseudocode sequence.

**Source:** [AlphaEvolve, v1, Figure 2, PDF p. 4](https://arxiv.org/pdf/2506.13131v1#page=4); [inspection details](study-google-meta-nvidia.md#alphaevolve). Figure 3, p. 6, supplies the complementary idea of unequal code-card heights with explicit reading order.

**Observed:** a human-configuration band sits above four component columns; a controller excerpt spans the lower system area. Blue `#4285F4`, red `#EA4335`, yellow `#FBBC04`, and green `#34A853` recur in the corresponding code identifiers. Visible Google Sans and Google Sans Mono text is about 8.78 pt, group headings about 11.29 pt. Main strokes are about 0.94 pt and secondary dashed boundaries about 0.51 pt. These are source measurements; the proprietary font is not required for a new figure.

**Authoring recipe:** allocate roughly 20:35:45 of the usable height to configuration, modules and code. Use 3–4 module columns only if the method has that many meaningful roles. Align each setup item with its receiving module. Give the code 3–6 relevant lines, real indentation, and 8–8.2 pt monospace. Color an identifier only when it names the same role as its diagram counterpart; ordinary syntax can remain neutral.

Use darker role inks—blue `#2C64B7`, red `#B9453D`, ochre `#8A6500`, green `#287A48`—over white or pale `#EEF3FB`. Keep small text out of the source's bright yellow. Place a final artifact outside the execution scope only if that boundary is true of the system. Give routes separate ports; use bidirectional arrows only for bidirectional interfaces.

**Required check:** trace every colored identifier to a real module and every code dependency to the supplied algorithm. A compact excerpt may omit housekeeping, but cannot silently omit the state or evidence required by an operation. Label omissions and invented examples explicitly.

## 2. Registered alternatives

**Use when:** the contribution changes a connection, operation, prompt span or state while most of the system remains the same.

**Sources:** [mHC, v1, Figure 1, PDF p. 1](https://arxiv.org/pdf/2512.24880v1#page=1), [inspection](study-deepseek-tencent-alibaba.md#deepseek-mhc); [Circuit Tracing, “Multiplicative patching”](https://transformer-circuits.pub/2025/attribution-graphs/methods.html), native `crosscoder-patching-tutorial-svg`, [inspection](study-openai-anthropic-microsoft.md#anthropic-circuit-tracing).

**Observed:** mHC's three panel widths are 116.60:153.34:153.34 pt, approximately **0.76:1:1**. The unchanged Layer F rectangles have matching dimensions and vertical positions. Cyan `#C1E5F5` marks common computation; pale orange and green distinguish changed mappings. Circuit Tracing aligns baseline and intervention layers, gives recorded values a separate symbol, and shades only the affected scope. Its SVG declares Roboto, but the local preview used a fallback; this is not a verified rendered-font measurement.

**Authoring recipe:** use 50:50 panels for equally complex alternatives, or 0.76:1:1 for a genuinely simpler baseline plus two richer variants. First lock common operation centers, dimensions and input/output levels; add changed paths afterward. Allocate 6–10 mm between alternatives when cross-condition copying must be shown. Use the common 10/8.5/7.5 pt hierarchy, with comparable headings in the same position.

Keep unchanged computation pale blue or neutral. Use one dark warm accent for the changed operation and, if needed, a distinct green for copied state. Mark the exact edited field or branch; do not tint the whole proposed system as if every component changed. Separate solid computation, dotted copying and thin annotation leaders with a local key. Addition or selection must have an explicit operator.

**Required check:** differences in position, width, opacity or visual weight must either encode a real difference or be justified by content density. Stack counts do not establish tensor dimensions. A green proposal is not a claim of success. Preserve the factual before/after state, including unchanged fields.

## 3. Typed modality lanes

**Use when:** different input types pass through different encoders, become tokens or embeddings, and join or condition a shared model.

**Sources:** [Phi-4-Mini/Phi-4-Multimodal, v1, Figure 1, PDF p. 4](https://arxiv.org/pdf/2503.01743v1#page=4), [inspection](study-openai-anthropic-microsoft.md#phi-mini); [GR00T N1, v2, Figures 2–3, PDF pp. 3–4](https://arxiv.org/pdf/2503.14734v2#page=3), [inspection](study-google-meta-nvidia.md#gr00t-n1); [Qwen3-TTS, v1, Figures 2–3, PDF pp. 3–4](https://arxiv.org/pdf/2601.15621v1#page=3), [inspection](study-deepseek-tencent-alibaba.md#qwen3-tts).

**Observed:** Phi repeats each modality's hue in inputs, encoders, token tiles and adapter rows. Its visible Segoe UI module text is about 8.22 pt, but token labels are only about 4.41 pt. GR00T distinguishes actual image, instruction, state and action paths; some image/action colors use transparency. Qwen3-TTS's dashed paths mean training-only in Figure 2 but optional elements in Figure 3.

**Authoring recipe:** assign about 60–65% of the width to aligned inputs and transformations and the rest to the shared model or output mechanism. Use one row per actual modality and identical encoder heights where comparable. Show a short real example or an explicitly schematic one. Use 4.5–6 mm token cells for short literal labels, or smaller unlabeled cells with a readable external key. Show 4–8 representative tokens rather than an unreadable full sequence.

Recommended fill/ink pairs are vision `#DDEFE8`/`#257D69`, audio `#DBEEF9`/`#247CA7`, language `#FCE5C9`/`#9A5B1B`. Carry the role through its path, but keep shared computation neutral. Use explicit concatenation, interleaving or cross-attention; these are different operations. If a route reverses reading direction, reserve a 4–6 mm bottom corridor and enter a named port. Distinguish repeated layers from repeated inference iterations.

**Required check:** confirm bypass paths, token order and phase membership. A frozen module, an optional branch and a training-only loss are separate concepts. Define dashed-line semantics locally. Composite source alpha against its actual background or choose a clearly labeled opaque adaptation; never reuse raw saturated RGB as if it were the visible pastel.

## 4. Provenance overview and expansion

**Use when:** readers need enough familiar architecture to locate one new mechanism, and then need to inspect that mechanism in detail.

**Sources:** [SAM 3, v1, Figure 4, PDF p. 4, and Figure 10, p. 19](https://arxiv.org/pdf/2511.16719v1#page=19), [inspection](study-google-meta-nvidia.md#sam3); [Qwen-Image, v1, Figure 6, PDF p. 7](https://arxiv.org/pdf/2508.02324v1#page=7), [inspection](study-deepseek-tencent-alibaba.md#qwen-image).

**Observed:** SAM 3 uses yellow new components, blue inherited SAM 2 components and teal Perception Encoder components. Its encoder trapezoids, memory stack, token rows and circled merge communicate different object types. Figure 10 gives roughly 45:55 of the width to overview and expansion, a visual estimate. Its lettering is outlined, so the exact visible font is unverified. Qwen-Image carries stream colors into the expanded block and distinguishes data routes from arrowless zoom boundaries.

**Authoring recipe:** begin at 40:60 or 45:55, adjusting for the actual novelty. Keep shared names and shapes unchanged between scales; add detail inside the expanded view. Recommended new-component fill/ink is `#FFF2B8`/`#6D5300`; inherited context `#DCEBFA`/`#315F9A`; stored state `#D7ECE8`/`#286E64`. Explain the mapping in a compact provenance key. If color denotes provenance, use labels or shapes for modality rather than reusing the same colors for a second meaning.

Use 8–8.5 pt labels and 9.5–10 pt scope headings. Give state a stack or record card and computation a module; add a plus or merge symbol only for a real combination. Reserve 4–6 mm outside the main flow for feedback. Keep expansion boundaries thin and arrowless; they describe a view, not execution. Match numbered ports across scales when direct correspondence is otherwise unclear.

**Required check:** every expanded edge must remain compatible with the overview. The source Qwen-Image extraction returned implausible raw widths despite ordinary rendered lines; do not inherit unvalidated geometry. Its pale red/cyan fills are alpha composites, not opaque saturated red/cyan. Redraw editable text instead of importing outlined source labels.

## 5. Stage cards with real intermediate objects

**Use when:** a method genuinely has several sequential stages, each with a different operation and meaningful intermediate output.

**Source:** [HY-World 2.0, v1, Figure 2, PDF p. 5](https://arxiv.org/pdf/2604.14268v1#page=5), [inspection](study-deepseek-tencent-alibaba.md#hunyuanworld2).

**Observed:** four cards measure about 86.67 × 163.76 pt with 15.68 pt gaps, about 18% of card width. Fills are blue `#DDEBF7`, green `#DFEDDA`, orange `#FCE6C6` and purple `#F6DAF1`; outlines/routes are `#215F9A`, `#3B7D23`, `#E97132` and `#7030A0`. Visible Aptos body text is about 7.55 pt, bold stage labels 8.81 pt, and Aptos Display Bold headings 11.33 pt. The interiors combine actual scene images, operations and trajectory/state sketches, while footer labels share baselines.

**Authoring recipe:** at 178 mm, **four 37 mm cards + three 6 mm gutters + two 6 mm margins** fit exactly. Choose card height from content, typically 65–85 mm before external headings/footers. Inside each card, budget a short heading, one or two named operations, and one meaningful output specimen. Use 10 pt headings, 8–8.5 pt labels and at least 7.5 pt detail. Do not repeat empty identical boxes when the actual stages produce different objects.

The observed pale fills are usable starting tokens. Darken the orange text to `#9C461D` for the recommended small-label ink; retain the brighter orange only for sufficiently visible marks if desired. Use a common dark footer such as `#405888` only when each footer names the same kind of object. Route forward connections in the gutters and keep within-stage operations vertical. An outgoing route can retain its source-stage color when provenance is the intended reading.

**Required check:** stage count and causal order come from the method. A raster output must be a genuine result with a selection rule, or explicitly marked illustrative. Do not use scene thumbnails as decoration. Stage color does not automatically track a persistent data cohort, and ribbon width must not imply unmeasured quantities.

## 6. Evidence and rubric correspondence

**Use when:** a figure explains evaluation, annotation, grounding or verification by connecting exact evidence to explicit judgments.

**Source:** [HealthBench, v1, Figure 1, PDF p. 2](https://arxiv.org/pdf/2505.08775v1#page=2), [inspection](study-openai-anthropic-microsoft.md#healthbench).

**Observed:** conversation, candidate response and rubric occupy three role columns. Dotted leaders connect exact answer passages to rubric rows; a small solid arrow expresses evaluation order. A score ruler sits beside the rubric. Sampled answer/user fills are approximately `#D0E3B6`/`#ECF6DE`; the selected region does not establish exact visible fonts or native stroke widths.

**Authoring recipe:** allocate about 28:36:36 of the usable width to evidence, candidate output and judgment, with 4–6 mm leader corridors. Excerpt only enough text to support 2–4 criteria. Preserve quotations exactly, label ellipses, and align related evidence spans and rubric rows vertically. Use 8–8.5 pt excerpts, 9.5–10 pt role headings, and 7.5–8 pt criterion/weight labels. If a passage will not fit, enlarge its column or shorten the excerpt with an explicit omission.

Use neutral evidence `#F5F6F7`, pale response `#E8F1DE`, dark ink `#28313D` and one annotation accent such as `#6B743B`. Keep status in text or symbols as well as color. Dotted 0.65–0.8 pt correspondence leaders have no arrowhead; solid 0.95–1.1 pt process arrows do. Put weights and the computed score adjacent to criteria, with a denominator and aggregation rule when quantitative.

**Required check:** selected passages must actually support the mapped criterion. Evidence correspondence is not a causal edge. Do not invent a score, turn an example judgment into a benchmark result, or reuse the source's medical content as generic filler. A compact case must state its selection rule and scope.

## 7. Conditional diagnostic matrix

**Use when:** several tasks, models or observation conditions need fair comparison without many overlapping curves or radar polygons.

**Sources:** [Perception Encoder, v1, Figure 8, PDF p. 11](https://arxiv.org/pdf/2504.13181v1#page=11), [inspection](study-google-meta-nvidia.md#perception-encoder); [Monitoring Monitorability, v1, Figure 8, PDF p. 17](https://arxiv.org/pdf/2512.18311v1#page=17), [inspection](study-openai-anthropic-microsoft.md#monitorability); [AlphaEvolve, v1, Figure 8, PDF p. 18](https://arxiv.org/pdf/2506.13131v1#page=18).

**Observed:** PE crosses three model columns with seven task rows, uses a stable left label rail, groups related tasks by hue, and marks optima/reference lines. Some visible annotations are only about 4.83 pt; the individual curve panels are raster. OpenAI's three scope panels share one legend and comparable axis structure. AlphaEvolve separates two tasks, uses a shared normalized compute axis, and explicitly differs in y range.

**Authoring recipe:** use a 20–25% left rail and the remainder for 2–3 model/condition columns. At 178 mm, begin with 3–4 task rows; split a dense seven-row figure or allocate substantially more height rather than copying microtype. Alternatively use three equal condition panels for one metric. Assign one variable to panels and one to line/marker identity. Use 8 pt axes, 9–9.5 pt headings, 7.5–8 pt ticks/legend, 1.1–1.4 pt curves, 3–4 pt markers and a 0.4 pt grid.

Recommended task-domain accents are teal `#147A82`, blue `#315F9A` and purple `#75469A`, with pale label fields. If color instead identifies methods, keep task groups neutral. Use a shared legend above the set and direct labels only where they remain unobstructed. Share axes within a comparable metric; different units need explicit scales. Within-model budget trajectories may connect observed settings; cross-model frontiers need a separate key and cannot imply unmeasured performance.

**Required check:** define each baseline/reference line, normalization and optimum consistently. Best-layer selection on the displayed evaluation data is not independent validation. Preserve pairing, denominators and interval meaning. Draw uncertainty from supplied observations, with the correct resampling unit. A ribbon alpha of 0.10–0.18 is merely an appearance choice; it does not specify confidence level.

## 8. State and token schedules

**Use when:** a streaming system preserves state across calls, or an inference method drafts, verifies, accepts and reuses specific token positions. Choose the variant that answers the scientific question; do not combine both just to fill space.

**Sources:** [WorldPlay, v1, Figures 2, 4 and 5, PDF pp. 4–5](https://arxiv.org/pdf/2512.14614v1#page=4), [inspection](study-deepseek-tencent-alibaba.md#worldplay); [Nemotron-Diffusion, v1, Figure 5, PDF p. 7](https://arxiv.org/pdf/2607.05722v1#page=7), [inspection](study-google-meta-nvidia.md#nemotron-diffusion).

**Observed:** WorldPlay places repeated current computation above a continuous memory ribbon, with separate retrieval and update routes. Its three indexing comparisons have matched **9 × 9** matrices. The architecture is raster, so fonts are unverified and sampled blue `#5480AD`/red `#C25759` are approximate rendered colors. Nemotron's two equal top panels contrast sequential and parallel generation; a wider lower panel aligns draft and verification and brackets the reusable span. Source token text is about 5.96 pt, which is a caution for reuse.

**Authoring recipe, persistent state:** allocate about 65:35 of the content height to current computation and persistent state, separated by a 5–7 mm route band. Give each chronological step the same internal grid. A memory object has explicit read/write ports and a record/index example. Use separate named retrieval and update routes; do not compress them into an unexplained two-headed arrow. Recommended compute fill/ink is `#DFE9F5`/`#315F8B`, memory fill/ink `#F5E1E1`/`#9D4749`.

**Authoring recipe, draft/verify:** use equal token pitch across all compared rows, with one header defining the time or position axis. At 178 mm, 6–10 representative tokens in 5–7 mm cells are usually more readable than a full sequence. Use neutral context, pale accepted green `#D9F2D0` and rejected red `#FFCECE`, plus explicit labels or symbols. Show shared parameters with one bracket/label when the same model is drawn twice. Bracket only the cacheable span. Use 8 pt token text, 9.5–10 pt panel headings, and distinct draft/verify row labels.

**Required check:** preserve indices, masks, rejected-token handling and read-before-write order. Blank cells need a defined meaning; they are not automatically zeros. Keep a matrix smaller only if it remains a faithful, explicitly schematic example. Schedule block lengths are proportional to time only when backed by timing data. A diagram's token acceptance pattern is an example, not a measured acceptance rate.

## Apply and review

Record the chosen recipe, the exact source anchors, and the role each source plays: composition, encoding, typography or caution. Write down the adaptations before rendering. Then compare the actual PDF to the brief: the intended operation must be visible, common elements must remain aligned, labels must survive final placement, and every connector and numeric mark must trace to the scientific inputs. See [production-review.md](production-review.md) for export and review gates.
