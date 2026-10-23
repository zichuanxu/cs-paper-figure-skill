---
name: cs-paper-figure
description: Design, implement, critique, and refine scientific figures for computer science research papers, with detailed control of color, typography, layout, grouping, shapes, arrows, and visual hierarchy. Use for publication figures, method/model architecture diagrams, agent/harness/memory workflows, multimodal and robotics pipelines, scaling plots, benchmarks, ablations, efficiency tradeoffs, uncertainty, heatmaps, qualitative grids, and multi-panel figure sets. Draw on inspected 2025–2026 AI research from OpenAI, Anthropic, Google, Meta, NVIDIA, DeepSeek, Tencent, Alibaba/Qwen, and Microsoft. Use for improve this paper figure, extract this paper's visual style, or make an ICML/NeurIPS/ICLR/ACL/CVPR-quality diagram. Produce visually specific, scientifically faithful, editable, reproducible figures.
---

# CS Paper Figure

Make the scientific argument visible and give it an intentional visual form. Optimize factual fidelity, readable mechanism/comparison, meaningful visual hierarchy, final-size legibility, and coherent polish. Use specific research figures as design evidence; do not invent a corporate house style or assume a prestigious source is flawless.

**Aim for explanatory depth and visual specificity.** A sophisticated figure connects a system view, a precise mechanism, and a concrete instance or evidence view. Use semantic color families, distinct shapes for computation/data/state, nested groups, actual tokens/records/masks, and deliberate panel proportions. A generic set of equal boxes, a large node count, or more colored panels does not establish sophistication.

**Craft first.** Read [visual-craft.md](references/visual-craft.md) before drawing and build with [`scripts/paperkit.py`](scripts/paperkit.py). Earlier outputs of this skill were scientifically careful but looked like flowcharts or audit reports: white boxes with hairline outlines, DejaVu Sans, sentence-long panel titles, words where objects belong, and SCHEMATIC/receipt labels inside the art. Top-lab figures instead use role colour families (pale fill, same-hue stroke, dark same-hue text), a LaTeX-matched serif with typeset math, drawn nouns (state matrices, token strips, trapezoid projections, operator circles, documents, icons), one visible hero, and direct-labelled charts with explicit ratios. The MemT redesigns in [`scripts/examples/memt/`](scripts/examples/memt/) are the reference standard; the older `render_*` demos are component/contract examples only, so do not imitate their look.

## Scope and resource map

- **Create:** turn claims, methods or data into figures and reproducible source.
- **Redesign:** preserve scientific meaning, values, topology and experimental conditions while improving the visual system.
- **Critique:** inspect the actual figure and caption, identify consequential defects, and propose specific fixes.
- **Figure set:** assign each figure an evidential role and preserve consistent colors, symbols, terms and typography.
- For a narrow edit, reuse its source and check the changed region plus final export. Do not rebuild an entire paper unnecessarily.

| Need | Resource |
| --- | --- |
| **How to make it look good**: diagnosis, typography, role colours, glyph vocabulary, composition patterns, connectors, density targets, chart craft, beat-the-original protocol | [visual-craft.md](references/visual-craft.md) |
| Evidence behind those rules: IdeaScientist/SkillOpt readings, measured architecture figures (Gated DeltaNet, Kimi Linear, Titans, NSA, DeepSeek-V3, Hymba, BLT, …), MemT critique | [craft-study-2026-10.md](references/craft-study-2026-10.md) |
| Drawing primitives in mm: role palette, cards, nodes, matrices, vectors, trapezoids, operators, tokens, docs, icons, zoom rays, routed arrows, rich math, density/compare checks | [scripts/paperkit.py](scripts/paperkit.py) |
| **Figure series** for surveys, frameworks and system reports: one taxonomy palette for every figure, chapter frames with "To next" tabs, running examples, gate stacks, spectra, timelines, illustrated scenes with vector dialogue, diff panels, typed-edge legends, a palette-drift check (studies of *Proactive AI*, PlugMem, StudentSim, PaperBanana, ReHarness) | [figure-series.md](references/figure-series.md), [scripts/examples/proactive/](scripts/examples/proactive/) |
| Optional generated icon sets with Codex CLI: when to use them, rules from 11 top-lab figures, prompt anatomy, helper | [image-generation.md](references/image-generation.md), [scripts/codex_images.py](scripts/codex_images.py) |
| Reference-quality redesigns (architecture + efficiency chart) | [scripts/examples/memt/](scripts/examples/memt/), [advanced-examples.md](references/advanced-examples.md#memt-10-redesigns) |
| Rich multi-level figures; system, mechanism, instance and evidence | [dense-composition.md](references/dense-composition.md) |
| Scenes, frame sequences, trajectories, token structures and visual memory | [visual-objects.md](references/visual-objects.md) |
| Reproducible advanced examples, their contracts and adaptation limits | [advanced-examples.md](references/advanced-examples.md) |
| Current 120-paper coverage, the 44-paper expansion, and task-to-source lookup | [dense-paper-atlas.md](references/dense-paper-atlas.md) |
| Complete paper and inspected-figure inventories | [paper-corpus.csv](references/paper-corpus.csv), [figure-corpus.csv](references/figure-corpus.csv) |
| Select complementary sources and turn observations into design choices | [reference-selection.md](references/reference-selection.md) |
| Eight concrete composition and encoding recipes | [style-recipes.md](references/style-recipes.md) |
| Recent detailed studies: OpenAI, Anthropic, Microsoft | [study-openai-anthropic-microsoft.md](references/study-openai-anthropic-microsoft.md) |
| Recent detailed studies: Google, Meta, NVIDIA | [study-google-meta-nvidia.md](references/study-google-meta-nvidia.md) |
| Recent detailed studies: DeepSeek, Tencent, Alibaba | [study-deepseek-tencent-alibaba.md](references/study-deepseek-tencent-alibaba.md) |
| New dense studies with information layers and detail devices | [OpenAI/Anthropic/Microsoft](references/dense-study-openai-anthropic-microsoft.md), [Google/Meta/NVIDIA](references/dense-study-google-meta-nvidia.md), [DeepSeek/Tencent/Alibaba](references/dense-study-deepseek-tencent-alibaba.md) |
| User-selected IdeaScientist and SkillOpt figure analysis | [dense-user-anchor-study.md](references/dense-user-anchor-study.md) |
| Initial detailed modern studies, including the four user-selected references | [modern-paper-atlas.md](references/modern-paper-atlas.md) |
| Machine-readable modern evidence with confidence levels | [modern-source-index.json](references/modern-source-index.json), [recent-expansion-index.json](references/recent-expansion-index.json), [dense-expansion-index.json](references/dense-expansion-index.json) |
| Color, font hierarchy, composition, shapes, styles and visual critique | [visual-design.md](references/visual-design.md) |
| Adaptable palette/typography/spacing/stroke tokens | [design-tokens.json](assets/design-tokens.json) |
| Extract a source figure's actual visual specification | [design-extraction.md](references/design-extraction.md) |
| Explicit ports, return loops and connector collision review | [diagram-routing.md](references/diagram-routing.md) |
| Scientific meaning, data units, uncertainty and transformations | [scientific-contract.md](references/scientific-contract.md) |
| Select a figure family | [figure-patterns.md](references/figure-patterns.md) |
| Export, caption and review | [production-review.md](references/production-review.md) |
| Strict chart specification | [spec-format.md](references/spec-format.md) |
| Foundational examples and exact source records | [paper-atlas.md](references/paper-atlas.md), [source-index.json](references/source-index.json) |

Read the contract, visual-design guidance and relevant figure family for substantial new figures. Consult only relevant atlas entries, not every paper. Use available source/code/template before asking questions. Infer routine style choices and complete every part that can be done faithfully. Ask only when an unresolved scientific fact changes correctness.

The corpus contains **120 distinct papers/reports and 261 inspected figure anchors** as of 2026-10-21; **96 papers first appeared in 2025–2026** (67 in 2025, 29 in 2026). The 120-paper expansion added 44 papers and 90 anchors, including the user's IdeaScientist and SkillOpt references. Subsequent close readings deepen existing records without counting those papers again. These are curated design references, not a ranking or a count of accepted conference papers. Use `python <skill-root>/scripts/reference_catalog.py search --query "attention mask streaming" --since 2025 --limit 6`, then `show <paper-id> --figure "Figure 2"` for the precise evidence record. Use `stats` for reproducible coverage counts. Read only the relevant study sections. For manual lookup, use `rg -n '^## |^### |Typography|Geometry' references/dense-study-*.md references/dense-user-anchor-study.md`; do not load every atlas or the whole JSON corpus for each task.

## Workflow

### 1. Establish the content and figure brief

Use [figure-brief.yaml](assets/figure-brief.yaml), or capture the same fields compactly:

- One claim or mechanism the reader should understand.
- The operation carrying that claim: its input artifact, governing rule, changed output, and observable consequence. State what the reader can reconstruct beyond the overview's module names.
- Evidence source and status: measured, reported, derived, illustrative or schematic.
- Comparison, units, independent sampling unit, aggregation and interval meaning.
- For diagrams, verified entities, operations, persistent state, boundaries and directed edges.
- Final physical size, manuscript template, panel budget and delivery formats.
- For a rich figure, the information levels and each panel's question, conclusion, inputs, and cross-panel identifiers.
- Any unknown facts and necessary qualifications.

Do not add a model update, memory write, causal edge or module absent from the described system. Do not fabricate data or uncertainty to complete a layout. If an empirical figure is incomplete, show an explicitly pending state, not plausible invented results.

Resolve and open a supplied image or source file before critiquing it. If its path is missing, recover the available attachment or state that the original cannot be inspected; do not invent its defects or claim a faithful redesign. Continue independent work that does not require the missing image.

### 2. Study relevant modern examples at the figure level

Prioritize 2025–2026 entries across the full catalog. Select references by the reader's task, then give each reference a job: **composition**, **semantic encoding**, or **evidence presentation**. Two complementary examples usually suffice; adding unrelated styles creates inconsistency. Use [reference-selection.md](references/reference-selection.md) and adapt a matching [style recipe](references/style-recipes.md).

- Diagram-to-code correspondence: AlphaEvolve Figure 2.
- Matched alternatives and local changes: mHC Figure 1; Anthropic Circuit Tracing.
- Novel versus inherited components, overview plus detail: SAM 3 Figures 4/10; Qwen-Image Figure 6; Qwen3.8-Next and DeepSeek-V4.
- Parallel modality lanes and typed tokens: Phi-4-Mini Figure 1; GR00T N1 Figures 2/3; Qwen3-VL Figure 1; Cosmos 3.
- Multi-stage mechanism storyboards: HY-World 2.0 Figure 2; Hunyuan3D 2.5 Figure 3.
- Evidence and evaluation correspondence: HealthBench Figures 1/2; Monitoring Monitorability Figure 2.
- Condition-controlled plots and task matrices: gpt-oss Figure 3; Monitoring Monitorability Figure 8; Perception Encoder Figure 8.
- Persistent memory, token schedules and return paths: WorldPlay Figures 2/4/5; Nemotron-Labs-Diffusion Figures 3/5; Harness².
- Dense overview coupled to an actual case: IdeaScientist Figure 1; trace the repeated artifact and role identities into the worked example.
- Parallel edits and different update timescales: SkillOpt Figure 2; make state writers and validation access explicit.
- Overview plus representation plus exact operator: Wan-Animate-2 Figure 1; follow shared object labels across architecture, time/space layout and the indexed operator, while explicitly scoping colors whose meanings change between panels.

For new aesthetic observations, inspect the actual image. Use version/page/figure anchors. Extract colors, visible font roles, layout proportions, strokes, node vocabulary and arrow routes; label each as measured, estimated or recommended. Searchable invisible text is not proof of visible typography; declared SVG fonts do not prove a local preview used those fonts. Keep opacity and background with raw colors. Reject physically implausible transformed stroke widths as measurements. Record unknowns honestly.

Borrow a transferable principle and produce an original composition. Keep source dates, affiliations and reuse permissions accurate. Do not reproduce artwork or company logos merely to imply quality.

### 3. Choose the structure and visual grammar

| Reader's task | Starting structure |
| --- | --- |
| Understand the new operation | Narrow overview plus larger mechanism detail; one concrete token/record example |
| Follow data, state or control | Typed nodes, explicit ports, scoped groups and reserved return corridors |
| Compare architectural alternatives | Matched positions and shapes; emphasize actual changes |
| Understand stages or recursion | Aligned lanes or a storyboard; distinguish time from system scope |
| Compare measured conditions | Dot/interval comparison, controlled bars or small multiples |
| Inspect scaling or resource cost | Observations and trajectories; quality-cost tradeoff with explicit conditions |
| Diagnose a component or failure | Paired deltas, ablation panels, distributions or shared-scale heatmaps |
| Inspect outputs | Matched qualitative grid with source and selection rule |

Sketch two materially different compositions internally for substantial new figures. Choose the one with the clearer reading order, stronger mechanism specificity, and fewer unavoidable crossings. Do not ask the user to arbitrate routine layout choices. Use a table if exact lookup is the main task.

For sophisticated figures, read [dense-composition.md](references/dense-composition.md). Build a panel contract and preserve identifiers across overview, mechanism and worked example. Show actual intermediate objects: a mask with labeled dimensions, a scoped record update, an aligned token sequence, a real failure trace, a tensor transformation, or a conditional objective. Reserve a companion figure for empirical analysis if combining everything would force microtype. Do not treat synthetic measurements as scientific evidence.

Allocate the most space to the transformation that carries the claim. An overview can be a narrow locator when the reader needs to inspect a replay table, context diff, attention operator or matched scene. An instance of an easy neighboring step does not explain a highlighted operation that remains a generic box. If that operation is only conceptual, mark its boundary or narrow the title.

For multimodal or spatial figures, read [visual-objects.md](references/visual-objects.md). Link actual scene/frame/state objects to their representation and operator. Preserve object identity, view, scale and time across comparisons; distinguish observations, predictions and executed transitions. Keep the model block compact when its internal architecture is not the claim.

### 4. Specify the visual system before rendering

State the five-second message and the hero element first ([visual-craft.md §1](references/visual-craft.md#1-the-five-second-test)). Then record actual values in the brief:

1. **Palette:** 3–5 roles from `paperkit.ROLE` (fill / soft / stroke / ink / mark), each with one stated meaning; novel parts saturated, inherited parts neutral; parameters owned in place rather than listed in an inventory box. Use a consistent role mapping across panels.
2. **Typography:** match the manuscript (Times/STIX + STIX math for LaTeX papers via `paperkit.use_fonts("serif")`; never DejaVu Sans in a Times paper), real weights, and three readable size levels at final output; noun-phrase panel titles ≤ 6 words.
3. **Geometry:** aspect ratio, panel proportions, grid unit, gutters, container padding, card spacing, corner radii and stroke hierarchy.
4. **Object vocabulary:** computation versus data/state/artifact, repeated modules, operator junctions and any semantic icons or badges.
5. **Routing:** source/target ports, forward lanes, external feedback corridors, label clearances and edge types.

Use the actual manuscript dimensions; otherwise 85 mm or 178 mm are adjustable starting widths. Start near 8 pt main text, 7–7.5 pt small text and 9–10 pt panel headings. Enlarge or simplify dense content before shrinking labels. Source figures with 3–6 pt text are cautionary examples.

Use real font weights and verify the exported font program, not just its family name. With Matplotlib Type 42 PDF output, select a compatible TrueType program; a CFF-flavored OTF mislabeled as TrueType can appear embedded yet produce renderer warnings. Keep the intended family, actual fallback, weight and export format in provenance. Use darker related ink for small labels than for pale data marks or panel fills.

Use white child cards inside tinted groups only when the nesting expresses real scope. Permit icons, token strips, record stacks, insets and light backgrounds when they explain the method. Avoid adding decorative detail that has no scientific role. Use raster images for real image/video/spatial data; use vector objects for exact topology and labels.

**Figure series.** When several figures explain one framework, define its palette once with `paperkit.series(names)` in a module every figure imports, chain stage figures with `cv.chapter(..., prev=, nxt=)`, carry one running example through the stages, and keep dialogue and labels as vector text (`cv.bubble`, `cv.tab`). See [figure-series.md](references/figure-series.md).

**Match the register before "cleaning up".** Method and results figures reward restraint; illustrated survey, position-paper and overview figures do not. There the pictures carry the argument (each stage shows the agent *doing* it), headers are solid colour with white bold text, and titles are large. Redesigning such a figure means keeping all of that and fixing its real faults (colour drift, text inside pixels, crossings, uneven type), never stripping it to outlined boxes: that reads as emptier and loses. Before drawing, list what the original does well and carry each strength over; fill every card edge to edge (`codex_images.py` style `"vignette"`, placed with `cv.image(..., fit="cover", h=, radius=)`); and run `paperkit.py parity original.png new.png`, which fails a redesign that is emptier, greyer or less illustrated at the same width. Lay chips out with `cv.flow_chips` (never hand-picked x positions) and end each script with `assert not cv.overlaps() and not cv.text_overlaps()`.

**Generated images (optional).** When the figure has actors, roles, tools or stages the reader must tell apart, and `scripts/codex_images.py check` succeeds, a matched set of 3–7 illustrated icons may replace the vector glyphs: one style spec, one Codex run, each icon tinted with its role colour, a text label beside every icon, no text inside the pixels, and a vector fallback kept in the render script. Use real photos or screenshots, not generated pictures, for data, inputs or environments. Full-bleed vignettes and scenes for illustrated figures come from the same helper. Place every generated image with `cv.image` and export with `cv.save`: they embed the pixels unchanged at 600 dpi and fail the export if an image would be resampled (matplotlib's own defaults shrink it to 100 dpi in the PDF, which is why generated images looked blurry). Heed `cv.image`'s warning below 300 source px per inch. Follow [image-generation.md](references/image-generation.md); without Codex, use paperkit's vector icons and continue.

### 5. Implement precise, reproducible source

Preserve the project's existing toolchain where appropriate. Use scientific plotting libraries for data, and SVG/TikZ/Graphviz/programmatic vectors for diagrams. Do not use image generation for quantitative marks, exact labels, or computational topology.

Utilities:

```bash
# Reference-quality redesigns built on paperkit (start here and adapt)
python <skill-root>/scripts/examples/memt/render_fig4.py --out figures/memt   # architecture
python <skill-root>/scripts/examples/memt/render_fig3.py --out figures/memt   # efficiency chart
python <skill-root>/scripts/examples/transformer/render_fig1.py --out figures/transformer
python <skill-root>/scripts/examples/harness2/render_fig2.py --out figures/harness2   # [--vector-icons]
python <skill-root>/scripts/examples/harness2/render_fig3.py --out figures/harness2   # [--vector-icons]
python <skill-root>/scripts/examples/proactive/render_arbitration.py --out figures/proactive  # chapter + gate stack
python <skill-root>/scripts/examples/proactive/render_cycle.py --out figures/proactive        # taxonomy loop
python <skill-root>/scripts/examples/proactive/render_spectrum.py --out figures/proactive     # scenes + spectrum
python <skill-root>/scripts/examples/proactive/render_overview.py --out figures/proactive     # Fig. 1 redesign
python <skill-root>/scripts/examples/proactive/render_capabilities.py --out figures/proactive # Fig. 3 redesign
python <skill-root>/scripts/examples/proactive/render_history.py --out figures/proactive      # Fig. 5 timeline
python <skill-root>/scripts/examples/reharness/render_fig1.py --out figures/reharness         # diff panels
python <skill-root>/scripts/examples/paperbanana/render_fig5.py --out figures/paperbanana     # dumbbell chart
python <skill-root>/scripts/paperkit.py swatches fig1.png fig2.png series_check.png          # palette drift

# Optional generated icons, scenes and vignettes via Codex CLI (only if `check` exits 0; see references/image-generation.md)
python <skill-root>/scripts/codex_images.py check
python <skill-root>/scripts/codex_images.py generate icons.json --out figures/icons [--ref existing.png]

# The five classic examples rebuilt in the new style (data bundled under scripts/examples/restyled/data)
python <skill-root>/scripts/examples/restyled/render_method.py --out figures/method
python <skill-root>/scripts/examples/restyled/render_attention.py --out figures/attention
python <skill-root>/scripts/examples/restyled/render_experiment.py --out figures/experiment
python <skill-root>/scripts/examples/restyled/render_scene_planning.py --out figures/scene
python <skill-root>/scripts/examples/restyled/render_epoch_context.py --out figures/epoch

# paperkit: smoke test, density (white/tint/ink %), side-by-side review against an original
python <skill-root>/scripts/paperkit.py
python <skill-root>/scripts/paperkit.py density figures/memt/memt_fig4_architecture.png
python <skill-root>/scripts/paperkit.py compare original.png figures/new.png review.png
python <skill-root>/scripts/paperkit.py parity original.png figures/new.png   # exit 1 if emptier/greyer/less illustrated

# Legacy component/contract demos (plain style; use for contracts and checks, not for looks)
# Original modern demonstrations, including a routed diagram and empirical panels
python <skill-root>/scripts/render_modern_examples.py --out figures/examples

# Evidence-bound original schematic with matched states and diagram-to-code colors
python <skill-root>/scripts/render_reference_recipe.py --out figures/recipe

# Rich overview, parallel proposals, atomic conflict matrix, and replay fixture
python <skill-root>/scripts/render_dense_method.py --out figures/dense

# Exact attention mask, worked softmax/value calculation, and streaming boundary
python <skill-root>/scripts/examples/causal_attention/render_figure.py --out figures/attention

# Four-panel synthetic study: paired effects, heterogeneity, cost, and diagnostics
python <skill-root>/scripts/render_dense_experiment.py --out figures/study

# Matched spatial scenes, candidate paths, swept collision checks and one action
python <skill-root>/scripts/render_worked_example.py scene-planning --out figures/scene

# Matched replay artifacts, context-field changes and the next proposal
python <skill-root>/scripts/render_worked_example.py epoch-context --out figures/epoch

# Validate a supplied chart specification
python <skill-root>/scripts/plot_from_spec.py figure.json --out figures/figure_1

# Inspect an exact source-figure region
python <skill-root>/scripts/inspect_pdf_style.py paper.pdf --page 3 \
  --clip 66 85 530 251 --out style.json --preview crop.png

# Check physical export and text/font handling
python <skill-root>/scripts/check_figure.py figures/figure_1.pdf \
  --expected-width-mm 178 --min-font-pt 7
```

Use `figure_style.py` for export/provenance and `diagram_geometry.py` for declared rectangle/port/polyline validation. Read their APIs before calling. The strict chart renderer draws supplied values; it does not choose an estimator or invent intervals. Use custom source for unsupported layouts.

Use `figure_scene.py` when physical-unit vector composition, typed documents/processes/gates, explicit branch buses, editable text, owner containment, pairwise text-overlap review, and routed-edge audits help. The dense renderer demonstrates the API with a deterministic fixture. Adapt its information hierarchy and components to the actual method; do not reuse its scientific topology for an unrelated task.

The advanced scripts are fixed worked examples, not general scientific models or automatic layout engines. Read [advanced-examples.md](references/advanced-examples.md) before adapting them. Their assertions intentionally bind labels, states, masks and numerical claims to preserved inputs. For real measurements, replace the synthetic generator with actual observations and reconsider the estimand and independent sampling unit.

Store raw observations separately from summaries; preserve transformation code, seeds, software versions and source hashes. Keep labels and numeric callouts derived from the same inputs, and assert derived ratios in the render script (as `render_fig3.py` does). Label invented measurements **SYNTHETIC DATA** or **ILLUSTRATIVE DATA** inside the export and in the caption, because they could be mistaken for results. A method diagram is schematic by nature: say so in the caption (and note illustrative glyph textures such as matrix shading there), not as a watermark, receipt or footnote inside the artwork.

Build diagrams with `paperkit.Canvas` (mm coordinates = printed size). Draw the noun instead of writing it: `matrix` for states, `vec` for vectors, `trap` for projections, `op` for ⊕/⊙, `tokens`, `doc`, `stack`, `diamond`, `chip`, and the frozen/trainable/fixed/evolving icons. Use `group(..., band=True)` cards with white bodies, `zoom` for overview→detail, `rich` for colour-coded equations, and `axes` or hand-placed marks for charts.

### 6. Review the science, appearance and geometry

**Scientific review:** trace values and edges to evidence. Check units, denominators, intervals, aggregation, controlled conditions, omissions and caption scope. Respect pairing/clustering, and distinguish measured nondominated points from unmeasured frontier interpolation.

**Craft review:** open the PNG and walk the [anti-pattern checklist](references/visual-craft.md#11-anti-patterns-checklist); run `paperkit.py density` against the targets in visual-craft §7; for a redesign run `paperkit.py compare` and `paperkit.py parity`, and follow the beat-the-original protocol (§10); a redesign that loses on parity needs a stated reason, not a cleaner-looking excuse. Fix clipped labels, text over wires, and band/label collisions before anything else; they are the most common defects in a first render.

**Design review:** inspect the actual PDF at final physical size and compare it with the selected visual references. Confirm meaningful shape/color hierarchy, specific mechanism detail, coherent typography, balanced information density, deliberate whitespace and readable legends. Check unchanged landmarks align in comparison panels, modality colors persist through transformations, and repeated conditions share scales when their values are being compared. Give dashed lines a local definition. A generic box arrangement or a technically valid default plot still needs redesign if it misses the visual brief.

**Depth review:** for a rich figure, trace one object through all explanatory levels and reconstruct the operation carrying the title's claim. Verify that the detail panel instantiates that operation, that the case follows its displayed rule, and that the changed artifact has an observable consequence. For a loop, show what changes between iterations; for matched scenes, preserve the camera, scale, object identity and time indexing. Compare source and candidate at the same physical width. Record concrete strengths and remaining weaknesses; object counts are descriptive, not a quality score. Preserve readable text rather than copying source microtype.

**Connector review:** trace each declared edge. Check actual painted node bounds, normal port entry/exit, arrowhead attachment, nonendpoint intersections, label collisions, border riding, unintended crossings and feedback separation. Run the geometry helper where supported, then visually inspect the densest region.

**Artifact review:** check dimensions, fonts, editing source, SVG text, PDF rendering, grayscale and rerendering. Budget the artwork, caption gap and caption together against the actual venue text block. Move long interpretation and statistical methods to an accompanying note, or split the figure; do not scale an entire dense plate down until its text becomes unreadable. Inspect color-vision simulations when available. Automated checks cannot certify all overlaps, accessibility, scientific validity or aesthetic quality.

Fix the most consequential issue and inspect again. Stop once the content, visual brief and required checks pass; avoid arbitrary aesthetic churn.

### 7. Deliver and explain the visual decisions

For creation/redesign, deliver requested formats, editable source and inputs, a manuscript-ready caption (each sentence changes how a value is read; no tools, no mark-placement mechanics, no protocol details the methods already give, no disclaimers; `paperkit.py caption` exits 0), concise alt text, and specific design decisions: palette roles, font hierarchy, layout choice, important routing, and any remaining limits. Default to vector PDF, editable SVG and PNG preview when compatible with the task. Follow the host's file-saving rules.

For critique, prioritize concrete defects and fixes. Point to the affected region or connector. Distinguish inspected facts from interpretation. Attribute borrowed design principles and identify copied/adapted artwork accurately.

Verify that every delivered file exists, opens, and uses the final filename. A preview path from a temporary or unavailable workspace is not a completed handoff. Save and link final artifacts using the host's supported workflow.

## Completion gates

- Data, topology and caption agree; illustrative content is unmistakable; the caption says what is shown, not how it was made.
- The figure has a recognizable visual hierarchy and task-specific mechanism detail.
- A visible hero carries the five-second message; key state, projections and operators are drawn as objects, not text boxes; no anti-pattern from visual-craft §11 remains.
- Colors, fonts, shapes, spacing and line styles form a consistent system.
- Labels are legible at final size and routes have unambiguous endpoints.
- The actual export has been inspected; unavailable checks are disclosed.
- The figure can be regenerated from its preserved inputs and editable source.

Do not equate aesthetic polish with a validated scientific result or promise publication outcomes. Scientific integrity and visual craft both need evidence.
