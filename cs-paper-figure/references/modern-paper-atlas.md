# Modern paper figure-design atlas: 2025–2026

This atlas studies **18 primary papers and 48 specific figures**: 9 papers from 2025 and 9 from 2026. The first four papers were nominated by the user and receive the most detailed treatment. All listed figure regions were visually inspected; this is a design analysis, not a model-capability survey.

Read the closest figure family and its limitations, then construct an original figure for the current scientific claim. Keep the older [paper atlas](paper-atlas.md) as a historical supplement. The [modern source index](modern-source-index.json) preserves structured measurements and source hashes.

## Contents

- [Evidence legend](#evidence-legend)
- [Coverage and navigation](#coverage-and-navigation)
- [Design conclusions](#design-conclusions-to-carry-into-new-figures)
- [Four detailed 2026 studies](#a-four-user-nominated-2026-papers)
- [Additional 2025–2026 studies](#b-additional-20252026-sources)
- [Adaptation boundaries](#adaptation-boundaries)

## Evidence legend

| Evidence category | What it supports |
| --- | --- |
| `vector_measured` | A property recovered from visible PDF drawing/text objects or their placed bounds. RGB values are rounded to 8-bit. Font identity requires visible text traces with rendering mode 0 or 1. Point sizes describe this PDF placement. |
| `searchable_overlay` | Metadata from text with rendering mode 3 (invisible) placed behind visible glyph outlines. Useful provenance, but it does not establish the visible typeface, editable text, or glyph color. |
| `raster_sampled` | Color sampled from an embedded raster or rendered crop, with compositing where applicable. Compression, antialiasing and color conversion can affect it; not an exact authoring token. |
| `visually_estimated` | An inspected visual relationship, layout proportion, or interpretation without exact authoring-file recovery. Unknown raster/outlined fonts remain unknown. |
| `recommendation` | An original proposed adaptation for a new figure, not a measurement or a claim attributed to source authors. |

All point sizes are at the inspected PDF placement. A source label below 7 pt is a readability compromise, not a recommended target. Manual crop widths/aspects include selected inspection margins; only explicitly measured operator dimensions should be treated as object geometry. A searchable font name cannot establish the visible typeface when the glyphs are outlines. Do not infer an authoring application from a familiar palette.

## Coverage and navigation

| Paper | Organization / collaboration | Year · version | Inspected anchors |
| --- | --- | --- | --- |
| [DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence](https://arxiv.org/pdf/2606.19348v1) | DeepSeek | 2026 · v1 | Figure 2 (p. 6), Figure 3 (p. 9), Figure 5 (p. 15), Figure 9 (p. 40) |
| [On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability](https://arxiv.org/pdf/2608.30320v1) | Alibaba/Qwen | 2026 · v1 | Figure 1 (p. 2), Figure 3 (p. 5), Figure 5 (p. 9), Figure 6 (p. 9) |
| [Cosmos 3: Omnimodal World Models for Physical AI](https://arxiv.org/pdf/2606.02800v4) | NVIDIA | 2026 · v4 | Figure 1 (p. 5), Figure 5 (p. 11), Figure 8 (p. 20), Figure 11 (p. 33) |
| [Harness²: Recursive Agent Harnessing for an Open World](https://arxiv.org/pdf/2610.14224v1) | Google Cloud AI Research; Northwestern University | 2026 · v1 | Figure 1 (p. 1), Figure 2 (p. 3), Figure 3 (p. 5), Figure 9 (p. 12) |
| [DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models](https://arxiv.org/pdf/2512.02556v1) | DeepSeek-AI | 2025 · v1 | Figure 2 (p. 4), Figure 4 (p. 9) |
| [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](https://arxiv.org/pdf/2601.07372v1) | Peking University and DeepSeek-AI | 2026 · v1 | Figure 1 (p. 3), Figure 2 (p. 5), Figure 3 (p. 6) |
| [Qwen3 Technical Report](https://arxiv.org/pdf/2505.09388v1) | Qwen Team (Alibaba) | 2025 · v1 | Figure 1 (p. 9), Figure 2 (p. 20) |
| [Qwen3-Omni Technical Report](https://arxiv.org/pdf/2509.17765v1) | Qwen Team (Alibaba) | 2025 · v1 | Figure 2 (p. 3), Figure 3 (p. 4) |
| [Qwen3-VL-Embedding and Qwen3-VL-Reranker: A Unified Framework for State-of-the-Art Multimodal Retrieval and Ranking](https://arxiv.org/pdf/2601.04720v1) | Qwen Team (Alibaba) | 2026 · v1 | Figure 2 (p. 3), Figure 5 (p. 7) |
| [Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material](https://arxiv.org/pdf/2506.15442v1) | Tencent Hunyuan | 2025 · v1 | Figure 2 (p. 5), Figure 3 (p. 5), Figure 4 (p. 6) |
| [HunyuanVideo 1.5 Technical Report](https://arxiv.org/pdf/2511.18870v1) | Tencent Hunyuan Foundation Model Team | 2025 · v1 | Figure 1 (p. 3), Figure 2 (p. 4), Figure 3 (p. 6) |
| [HunyuanImage 3.0 Technical Report](https://arxiv.org/pdf/2509.23951v1) | Tencent Hunyuan Foundation Model Team | 2025 · v1 | Figure 2 (p. 4), Figure 3 (p. 6), Figure 4 (p. 6) |
| [Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation](https://arxiv.org/pdf/2503.11926v1) | OpenAI | 2025 · v1 | Figure 1 (p. 2), Figure 2 (p. 5) |
| [Reasoning Models Struggle to Control their Chains of Thought](https://arxiv.org/pdf/2603.05706v1) | OpenAI with NYU, UCL, UPenn, and MATS collaborators | 2026 · v1 | Figure 1 (p. 2), Figure 2 (p. 3) |
| [V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/pdf/2506.09985v1) | FAIR at Meta with Mila and Polytechnique Montreal collaborators | 2025 · v1 | Figure 1 (p. 2), Figure 2 (p. 4) |
| [V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning](https://arxiv.org/pdf/2603.14482v3) | FAIR at Meta with Universidad de Zaragoza | 2026 · v3 | Figure 1 (p. 1), Figure 4 (p. 5) |
| [Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities](https://arxiv.org/pdf/2507.06261v6) | Google / Gemini Team | 2025 · v6 | Figure 1 (p. 3), Figure 4 (p. 6) |
| [Automated Researchers Can Reliably Mitigate Alignment Failures](https://www-cdn.anthropic.com/7b1c44894e980876479947dcdd40716278aeeffd/automated-alignment-researchers-august-2026.pdf) | Anthropic / Anthropic Fellows Program with UC Berkeley | 2026 · official-2026-08-28 | Figure 1 (p. 1), Figure 2 (p. 4) |

## Design conclusions to carry into new figures

- Build visual richness from actual structure: nested subsystems, state chips, operators, stage bands, aligned alternatives, local insets, and correctly routed feedback.
- Give a scientific role a small tonal family: dark heading/outline, medium accent, pale fill. The exact role mapping comes from the current method; source palettes are exemplars.
- Use a hierarchy of typography, strokes, and spacing together. A larger heading alone cannot rescue a uniformly laid-out block diagram.
- Reserve connector corridors before filling the page. Opposite directions need distinct ports/tracks; arrow endpoints must meet the intended visible boundary normally.
- Allocate width to information content. Several inspected figures use a narrow overview and a larger mechanism/evidence region; forcing equal cards would weaken them.
- Separate visual texture from meaning: hatching can identify communication; token cells can express sequences; pale cards can identify subsystems. Each must have a specific interpretation.
- Retain contextual diversity: the corpus contains sans, serif, and mixed mathematical/code typography; white, tinted, and dark plots; precise mechanical diagrams and case-study storyboards. Choose a coherent treatment for the current claim.
- Improve the sources where necessary. Very small labels, truncated bar axes, excessive logos, and indistinguishable tints appear in modern papers too. Borrow the effective relationship and repair the weakness.

## A. Four user-nominated 2026 papers

## DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence

**Source:** [v1 PDF](https://arxiv.org/pdf/2606.19348v1) · [arXiv record](https://arxiv.org/abs/2606.19348v1) · DeepSeek.
**Date provenance:** arxiv submission: 2026-04-26; pdf margin date: 2026-04-26; date note: The source reports April 26 despite a June-style identifier. Preserve this discrepancy; do not silently repair it.
**Affiliation evidence:** PDF p1 says DeepSeek-AI.

### Figure 2 · PDF page 6 — Overall architecture

**Color roles.** computational blocks: #FFF2CC [measured in PDF]; mixing operations: #F2F2F2 [measured in PDF]; box stroke: #172C51 [measured in PDF]; repeat boundary: #2E75B6 [measured in PDF]; data flow: #000000 [measured in PDF].

**Typography.** ordinary modules: Calibri 6.31 pt [measured in PDF] repeat boundary heading: Calibri-Bold 6.31 pt [measured in PDF] loss labels: Calibri-Italic 5.67 pt [measured in PDF] math: CambriaMath 6.31 pt [measured in PDF]

Visible text trace (rendering mode 0 or 1) independently checked; declared families/sizes are visible glyph evidence.

**Geometry and spacing.** Stroke widths: 0.472 pt (208 paths), 1.416 pt (18 paths) [measured in PDF].

**Composition, grouping, and routing.**

- A centered vertical architecture occupies only ~97 mm of the A4 page width; a broad caption sits below. [visual observation]
- The recurring block puts the residual stream at left, the main operation at right, and pre/post mixing between them; this layout is repeated vertically. [visual observation]
- Yellow computational blocks are exactly 58.66 × 19.56 pt. Gray mixing cells have the same 58.66 pt width but a 13.36 pt height. [measured in PDF]
- The two repeated attention/MoE stages are displaced vertically by ~88.19 pt. [measured in PDF]
- The input embedding, residual stream, prediction head, and MTP module are aligned on a vertical spine. [visual observation]
- Rounded rectangles encode operators; repeated stacked ribbons/circles encode expanded hidden-state streams. [visual observation]
- Data arrows are orthogonal with solid black triangular arrowheads; auxiliary loss routes use dashed horizontal arrows. [visual observation]
- The repeat boundary is a thin blue dashed rectangle without a background fill. [visual observation]
- Recorded line widths cluster at 0.472 pt for thin outlines and 1.416 pt for stronger paths. [measured in PDF]

**What works.** Multiple geometries distinguish operations from state without relying only on text. Same-width operator boxes and recurring rows give a dense mechanism stable rhythm.

**Adaptation.** Use aligned rows for repeated mechanisms and two distinct box heights for coarse blocks versus local transformations. Represent persistent or expanded state with a compact repeated glyph, while preserving its meaning in the caption. Make boundaries lighter than real data paths; keep dashed losses or auxiliary paths semantically distinct.

**Limitations and changes to make.** At native page placement most module text is only 6.31 pt; scale up or simplify for a new figure. This is a relatively restrained architecture figure despite the paper’s more colorful attention diagrams; it does not justify one universal DeepSeek style.

### Figure 3 · PDF page 9 — Compressed Sparse Attention (CSA)

**Color roles.** KV tokens: #FFE699 [measured in PDF]; compressed indexer keys: #FFF2CC [measured in PDF]; query tokens: #C5E0B4 [measured in PDF]; indexer query tokens: #E2F0D9 [measured in PDF]; operations: #D0CECE [measured in PDF]; index scores: #C4FB3B [measured in PDF]; indexer boundary: #767171 [measured in PDF].

**Typography.** module and data labels: Calibri 6.82 pt, operator labels bold [measured in PDF] group and output heading: Calibri-Bold 8.78 pt [measured in PDF] ellipsis: Calibri 4.39 pt [measured in PDF]

Visible text trace (rendering mode 0 or 1) independently checked; declared families/sizes are visible glyph evidence.

**Geometry and spacing.** Stroke widths: 1.097 pt (38 paths), 1.463 pt (16 paths), 0.671 pt (5 paths), 0.366 pt (5 paths), 0.549 pt (1 paths), 0.244 pt (1 paths) [measured in PDF].

**Composition, grouping, and routing.**

- Wide landscape composition; selected crop 158.04 × 77.61 mm. [visual observation]
- Two input families sit along the bottom, with KV left and query right; information flows upward to one long output-attention bar. [visual observation]
- A dashed middle-right enclosure isolates the Lightning Indexer while keeping its incoming and outgoing paths visible. [visual observation]
- Token glyph width is 7.55 pt. Uncompressed input glyphs are 25.79 pt high; compressed glyphs are 13.23 pt or 7.47 pt high. [measured in PDF]
- Output bar is 394.16 × 13.17 pt; compressor blocks are 58.49 × 19.93 pt. [measured in PDF]
- Trapezoids mark compressors/selectors, rounded bars mark operators, narrow repeated cells mark token sets, and miniature bars mark scores. [visual observation]
- Orthogonal arrows occupy reserved corridors and meet the centers of operator sides. [visual observation]
- Selected token groups are visibly smaller than source groups, while semantic color persists. [visual observation]
- Observed stroke widths include 1.097 pt and 1.463 pt for the dominant outlines/paths. [measured in PDF]

**What works.** Color tracks data identity; shape tracks the kind of transformation. The long output bar visually reunifies the branches without an additional ornamental frame. The indexer is both spatially enclosed and explicitly titled, making a nested mechanism readable.

**Adaptation.** Choose distinct pale fills for data families and neutral operator fills; reserve saturated accent for the selected signal or score. Use token stacks or matrices where they explain data structure, rather than decorating every box. Use a long aggregation/output bar and a nested module boundary to make the reading order visible.

**Limitations and changes to make.** There are many crossing-adjacent paths; preserving corridor spacing is essential when adapting. Do not import the depicted counts or heights as quantitative compression ratios without checking the new method. The 6.82 pt labels are below a comfortable 8 pt starting target; source ellipsis glyphs are particularly small.

### Figure 5 · PDF page 15 — Fine-grained expert-parallel communication and computation

**Color roles.** linear 1: #4D6BFE [measured in PDF]; activation: #66BBEE [measured in PDF]; linear 2: #7AA2FF [measured in PDF]; communication: white with blue diagonal hatch [measured in PDF]; secondary connectors: #888888 [measured in PDF].

**Typography.** phase labels: Searchable overlay metadata: DejaVuSans-Bold 5.06 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only] row labels: Searchable overlay metadata: DejaVuSans 5.06 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only] panel and speedup labels: Searchable overlay metadata: DejaVuSans-Bold 5.78 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only] expert wave labels: Searchable overlay metadata: DejaVuSans-Bold 4.34 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only]

Contains invisible searchable text; family attribution must distinguish visible and overlay.

**Geometry and spacing.** Stroke widths: 0.361 pt (17 paths), 0.868 pt (8 paths), 0.434 pt (8 paths), 0.723 pt (4 paths), 0.578 pt (2 paths) [measured in PDF].

**Composition, grouping, and routing.**

- Three vertically stacked comparisons share a left origin around x = 118.43 pt. [measured in PDF]
- Naive has one timeline; Comet has communication and computation lanes; the proposed version expands to dispatch, computation, and activation/combine lanes. [visual observation]
- The original long L1 block is 116.16 pt wide; the three wave L1 blocks are each 38.72 pt, exactly one third. [measured in PDF]
- Final proposed compute and activation lanes use 10.82 pt block heights. [measured in PDF]
- A compact legend sits at the lower right; theoretical speedup labels occupy open right-side space. [visual observation]
- Solid color separates computation phases, while hatching identifies communication in grayscale. [visual observation]
- Faint diagonals connect scheduling waves without competing with colored duration bars. [visual observation]
- Theoretical, rather than measured, speedup is stated in the figure. [visual observation]
- Thin hatch/border widths include 0.361–0.434 pt; stronger plotted paths include 0.868 pt. [measured in PDF]

**What works.** Semantic texture and consistent phase color make increasing overlap immediately legible. The three-row comparison shows a change in scheduling organization rather than requiring prose to explain it.

**Adaptation.** Use hatching for communication or waiting, solid fills for compute, and light dependency links. Align time origins and retain proportional duration widths when timing is quantitative. Allocate row height according to lane count and keep explanatory labels in unused time-axis space.

**Limitations and changes to make.** All extracted font traces are invisible type-3 searchable overlays. The visible glyphs are vector outlines; do not assert the overlay family as an exact visible font. Searchable-overlay sizes are 4.34–5.78 pt. Visual inspection confirms dense small labels, but the exact visible font and its source size are not recovered; enlarge or simplify the adaptation. The unequal row heights serve different lane counts; arbitrary equal card heights would waste space. A schedule drawn from symbolic times should remain explicitly schematic.

### Figure 9 · PDF page 40 — MRCR 8-needle performance

**Color roles.** primary series: #4D6BFE [measured in PDF]; secondary series: #9DB0FF [measured in PDF]; main text: #262626 [measured in PDF]; secondary values: #666666 [measured in PDF]; grid: #DDDDDD [measured in PDF].

**Typography.** title: Searchable overlay metadata: DejaVuSans-Bold 10.25 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only] axis titles and legend: Searchable overlay metadata: DejaVuSans-Bold 8.86 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only] x ticks: Searchable overlay metadata: DejaVuSans-Bold 6.99 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only] y ticks: Searchable overlay metadata: DejaVuSans 6.99 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only] primary value labels: Searchable overlay metadata: DejaVuSans-Bold 6.06 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only] secondary value labels: Searchable overlay metadata: DejaVuSans 5.59 pt; visible glyphs are outlines, so this does not certify their family or point size. [searchable overlay only]

Contains invisible searchable text; family attribution must distinguish visible and overlay.

**Geometry and spacing.** Stroke widths: 0.746 pt (18 paths), 1.492 pt (2 paths), 0.466 pt (1 paths) [measured in PDF].

**Composition, grouping, and routing.**

- Single wide plot with eight ordered context-length positions. [visual observation]
- Primary values are placed above the primary curve; secondary values are placed below the secondary curve. [visual observation]
- The legend occupies the empty bottom-left area, below all observed trajectories. [visual observation]
- The cropped figure is ~133.35 × 72.32 mm with a broad plotting rectangle. [visual observation]
- Primary series uses star markers; secondary series uses triangles; both have white marker borders. [visual observation]
- Series strokes are 1.492 pt, marker outlines 0.746 pt, and grid stroke 0.466 pt. [measured in PDF]
- Title, axis titles, and the primary value labels are bold, creating a stronger hierarchy than the skill’s old default. [visual observation]

**What works.** Two related blue hues express family identity, while marker shape keeps the series distinct. Direct labels give exact reported values without a table.

**Adaptation.** Use moderate bold hierarchy and direct endpoint or selected-value labels; avoid labeling all points by default. Place secondary annotations on the opposite side of a curve to primary annotations. Reserve an internal legend only when the data leave a stable empty region.

**Limitations and changes to make.** All extracted font traces are invisible type-3 searchable overlays. The visible glyphs are vector outlines; do not assert the overlay family as an exact visible font. Direct labeling every point can become crowded if there are more points or crossing curves. Two light-related colors need redundant shape and contrast checks. No uncertainty band is present; the aesthetic must not be translated into invented error bars.

## On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability

**Source:** [v1 PDF](https://arxiv.org/pdf/2608.30320v1) · [arXiv record](https://arxiv.org/abs/2608.30320v1) · Alibaba/Qwen.
**Date provenance:** arxiv submission: 2026-08-31; pdf cover date: 2026-09-01; date note: PDF cover and arXiv submission dates differ by one day; each retained separately..
**Affiliation evidence:** PDF p1 says Qwen Team; individual institutional affiliations are not printed in the inspected figure pages..

### Figure 1 · PDF page 2 — Qwen3.8-Flash-Next architecture

**Color roles.** GR read: #FFCC99 [measured in PDF]; GR write: #DCE8F4 [measured in PDF]; embeddings: #E1D5E7 [measured in PDF]; MoE: #F2DADB [measured in PDF]; attention group: #E8EEF3 [measured in PDF]; GDN group: #EEF3EA [measured in PDF]; token mixer: #E8EFDF [measured in PDF]; output heads: #F5E8C6 [measured in PDF]; connectors: #2F3742 [measured in PDF].

**Typography.** core labels: Helvetica 5.70–6.22 pt [measured in PDF] large modules and group labels: Helvetica / Helvetica-Bold 6.74 pt [measured in PDF] multiplicity labels: Helvetica 7.77 pt [measured in PDF] small note: Helvetica-Bold 4.66 pt [measured in PDF] branch symbols: Unnamed-T3, mostly 6.22 pt, is invisible searchable-overlay metadata; visible branch circles are not identified as a font. [searchable overlay only]

Contains invisible searchable text; family attribution must distinguish visible and overlay.

**Geometry and spacing.** Stroke widths: 0.518 pt (72 paths), 0.622 pt (29 paths), 0.674 pt (9 paths), 0.777 pt (8 paths), 0.0 pt (1 paths) [measured in PDF].

**Composition, grouping, and routing.**

- A narrow stack overview is on the left; an expanded two-stage mechanism is on the right, linked by dashed expansion guides. [visual observation]
- Right groups are both 227.99 pt wide, heights 120.73 and 124.36 pt, with a 12.43 pt vertical gap. [measured in PDF]
- Read/write boxes are consistently 37.31 × 11.40 pt. [measured in PDF]
- Two major rounded group panels carry blue-gray and pale green backgrounds; bottom vocabulary and n-gram embeddings share purple fill. [visual observation]
- Overview QSA/GDN cells are 46.63 × 11.40 pt and preserve the same semantic group hues. [measured in PDF]
- The n-gram embedding is a long 254.93 × 23.83 pt bar, versus the vocabulary block 85.49 × 20.73 pt. [measured in PDF]
- Connections are thin dark gray orthogonal lines with small filled arrowheads. [visual observation]
- Group corners are larger than module corners, establishing nested spatial hierarchy. [visual observation]
- Dashed blue-gray expansion boundaries are lighter than actual computation paths. [visual observation]
- Measured line widths are predominantly 0.518 pt, 0.622 pt, 0.674 pt, and 0.777 pt. [measured in PDF]

**What works.** This is semantic visual richness: differentiated fills, group backgrounds, repeated modules, state glyphs, and a clear overview/detail relation. Read and write operations are distinguished by color and text across both expanded groups. Repeated group dimensions and aligned ports control a complex diagram.

**Adaptation.** For a complex agent/memory diagram, give the overview roughly one fifth and the expanded mechanism roughly three fifths of the width, adapting remaining space to labels and routing. These fractions are design recommendations, not exact source measurements. Use light group backgrounds, mid-light role fills, and dark gray paths, with explicit operation labels. Align read/write or input/output ports to a small repeated grid and use one expansion relationship rather than several competing zooms.

**Limitations and changes to make.** Most native labels are 5–7 pt, with one 4.66 pt note; improve legibility rather than reproduce the density blindly. The paper uses several similar pastel greens; adjacent roles can merge without their labels and outlines. A hierarchy of enclosures must correspond to real model structure; do not add panels to imply nonexistent components.

### Figure 3 · PDF page 5 — Qwen Sparse Attention

**Color roles.** linear operators: #E2E3F1 [measured in PDF]; normalization: #FEE9C7 [measured in PDF]; RoPE: #FBE5E7 / #FDE6E8 [measured in PDF]; pooling: #CCFFFF [measured in PDF]; selector: #CCE5FF [measured in PDF]; compressed indexer: #D5E8D4 [measured in PDF]; sparse attention: #F6F7DD [measured in PDF]; mask cells: #B9E0A5 [measured in PDF]; group background: #F5F5F5 [measured in PDF].

**Typography.** operator and group labels: LiberationSans 7.27 pt [measured in PDF] minor transform labels: LiberationSans 4.85 pt [measured in PDF] mathematical variables: LiberationSerif-Italic 9.69 pt [measured in PDF] other annotations: LiberationSans 5.45–6.06 pt [measured in PDF]

Visible text trace (rendering mode 0 or 1) independently checked; declared families/sizes are visible glyph evidence.

**Geometry and spacing.** Stroke widths: 0.606 pt (131 paths) [measured in PDF].

**Composition, grouping, and routing.**

- Two equal-height upper enclosures show the indexer on the left and the main attention path on the right. [visual observation]
- Their widths are 181.14 and 260.50 pt, a 41:59 allocation; the gap is 6.66 pt. [measured in PDF]
- A shared lower mask strip spans 448.30 × 57.55 pt and follows after a 10.30 pt gap. [measured in PDF]
- Compressed indexer and sparse attention use matching 24.23 pt heights, but widths 130.25 and 175.68 pt according to their role in the layout. [measured in PDF]
- Repeated normalization and RoPE modules share height12.12 pt; module placement aligns q/k/v streams vertically. [measured in PDF]
- Linear blocks are trapezoids, sparse attention/indexer blocks rounded rectangles, gate/multiply operations circles, and masks actual cell grids. [visual observation]
- Variables are italic serif; descriptive labels are sans serif. This semantic font pairing is deliberate. [visual observation]
- Uniform extracted vector stroke width is 0.606 pt; dashed enclosure strokes are part of the thin hierarchy. [measured in PDF]
- The top-k route exits the left enclosure and enters the right at a reserved horizontal band. [visual observation]

**What works.** The lower mask strip explains an otherwise abstract difference between compressed indexing and sparse selection. Operator shape, fill, label, and mathematical typography jointly provide several levels of structure. The asymmetric width allocation follows complexity rather than forcing two identical cards.

**Adaptation.** Pair a mechanism diagram with a small data-structure view that makes its operation concrete. Use asymmetric panel widths based on information content. Separate math variables from prose typographically, but keep font families limited and ensure consistent rendering.

**Limitations and changes to make.** Tiny 4.85 pt transformation labels are a real readability compromise. Numerous pastel hues need stable semantics; an unrelated new figure should use fewer roles if possible. Small mask cells can become unreadable at one-column reduction.

### Figure 5 · PDF page 9 — QSA architecture ablations

**Color roles.** QSA or stage2: #2563A6 [measured in PDF]; IndexShare or stage1: #D97706 [measured in PDF]; full attention reference: gray dashed line [measured in PDF].

**Typography.** ticks: DejaVuSans 6.97 pt [measured in PDF] data labels and legend: DejaVuSans 6.51 pt [measured in PDF] axis labels: DejaVuSans 7.90 pt [measured in PDF] panel subcaptions: TeXGyrePagella-Regular 8.97 pt [measured in PDF]

Visible text trace (rendering mode 0 or 1) independently checked; declared families/sizes are visible glyph evidence.

**Geometry and spacing.** Stroke widths: 1.023 pt (19 paths), 1.441 pt (4 paths) [measured in PDF].

**Composition, grouping, and routing.**

- Two horizontally aligned panels with common y-axis meaning but different x-axis questions. [visual observation]
- Short subcaptions sit below each panel; the figure caption remains outside the plotting system. [visual observation]
- Point labels are placed near individual configurations in the left panel; the right panel relies on a compact legend. [visual observation]
- Open circles and blue line identify one series; open squares and amber line identify the other. [visual observation]
- A dashed horizontal line marks the full-attention reference. [visual observation]
- Only left and bottom spines are emphasized, and there is no background grid. [visual observation]
- Series line widths are 1.441 pt; marker edge widths are 1.023 pt. [measured in PDF]

**What works.** Color and marker redundancy work without a large legend. Direct configuration labels allow a reader to connect a point with its architectural choice.

**Adaptation.** Use light open markers with readable edge widths and a restrained two-color comparison. Put labels at sparse decision points; use a baseline line only when its interpretation is scientifically valid.

**Limitations and changes to make.** References to a common baseline require the actual baseline value and controlled evaluation conditions. Panel labels and native annotation fonts are small; source fonts should be scaled for the new output width.

### Figure 6 · PDF page 9 — Kernel-level latency, prefill and decode

**Color roles.** QSA: #2563A6 [measured in PDF]; uncompressed indexer: #D97706 [measured in PDF]; dense attention: #7A5195 [measured in PDF]; speedup annotation: #4C8C5A [measured in PDF].

**Typography.** ticks and legend: DejaVuSans 7.01 pt [measured in PDF] axis labels: DejaVuSans 7.95 pt [measured in PDF] panel and workload labels: DejaVuSans 8.42 pt [measured in PDF] speedup: DejaVuSans 7.48 pt [measured in PDF]

Visible text trace (rendering mode 0 or 1) independently checked; declared families/sizes are visible glyph evidence.

**Geometry and spacing.** Stroke widths: 0.842 pt (48 paths), 1.496 pt (8 paths), 1.216 pt (8 paths) [measured in PDF].

**Composition, grouping, and routing.**

- A 2×2 grid separates indexer/attention by rows and prefill/decode by columns. [visual observation]
- Each panel states its exact batch/workload setting in a two-line caption beneath the x-axis. [visual observation]
- The final-context speedup arrow sits just inside the right plot boundary between the two series endpoints. [visual observation]
- Selected viewport is 160.87 × 80.43 mm, close to a 2:1 overall aspect. [visual observation]
- QSA uses solid blue lines and open triangles; comparison indexer uses dashed amber and open squares; dense attention uses purple dash-dot and open diamonds. [visual observation]
- Green double-headed vertical arrows and numeric ratios summarize the comparison at 1M context. [visual observation]
- Measured series strokes are 1.496 pt; marker outlines 0.842 pt; annotation arrows 1.216 pt. [measured in PDF]
- White plotting backgrounds, no grid, restrained left/bottom spines, and small internal legends keep the multi-panel figure light. [visual observation]

**What works.** Color, shape, and dash pattern remain consistent in all four panels. Ratios are tied to a specific context and shown alongside absolute latency curves. The panel taxonomy makes a four-way experiment interpretable without a large title block.

**Adaptation.** Use a two-dimensional panel taxonomy when two experimental factors define the comparison. Reserve a distinct annotation color for one derived contrast, such as endpoint improvement. State absolute units and operating conditions adjacent to each panel; use consistent series tokens across the grid.

**Limitations and changes to make.** Each panel uses a different y-axis range; readers need the axis units and workload text. Annotated speedup ratios must come from the exact displayed endpoint values or documented calculations. The green accent denotes an annotation role, not a fourth experimental method.

## Cosmos 3: Omnimodal World Models for Physical AI

**Source:** [v4 PDF](https://arxiv.org/pdf/2606.02800v4) · [arXiv record](https://arxiv.org/abs/2606.02800v4) · NVIDIA.
**Date provenance:** initial submission: 2026-06-01; version date: 2026-06-23; pdf front date: 2026-06-24.
**Affiliation evidence:** NVIDIA corporate author; explicit PDF affiliation.

### Figure 1 · PDF page 5 — capability atlas

**Color roles.** shared backbone: stroke: #76B900; fill: #FAFCF5 [measured in PDF]; modality icons: language: #000073; image video: #A15912; audio: #4D004D; action: #3D6039 [measured in PDF]; card border: stroke: #B8B8B8; fill: #FFFFFF [measured in PDF].

**Typography.** figure text: visible text fonts: XCharter-Roman, XCharter-Bold; observed size pt: model heading: 11.602; model subtitle: 8.057; modality labels: 5.859; card titles: 4.882; inner model label: 3.867 [measured in PDF]

Visible text traces (type 0) support font family, rendered size and text color extraction.

**Geometry and spacing.** content width pt: 467.3 [measured in PDF]. hero box width height pt: 177.252, 45.924 [measured in PDF]. mini card width height pt: 74.123, 64.455 [measured in PDF]. card gap pt: 4.512 [measured in PDF]. composition: Centered hero occupies ~38% of content width; modality legend forms middle strip; six equal-width cards align on one baseline. [visual observation].

**Composition, grouping, and routing.**

- One common model is introduced above a consistent six-card grid; modality icons explain input-output reconfiguration. [visual observation]
- Outer card stroke 0.451 pt; hero stroke 0.548 pt. [measured in PDF]
- Small modality icons repeat in the same colors in the legend and each card. [visual observation]
- Title/subtitle/legend/card title/model-name create five typography levels. [visual observation]
- Input icons are placed to the left of the model and output icons to the right, preserving a repeated local grammar. [visual observation]

**What works.** One common model is introduced above a consistent six-card grid; modality icons explain input-output reconfiguration.

**Adaptation.** Use a shared model header plus 3-4 matched configuration panels at manuscript scale. Give each modality one persistent color and a simple vector glyph; use the glyph for repeated recognition, with a full text key once. Align identical input/model/output positions across alternatives to make only the configuration differences stand out.

**Limitations and changes to make.** The original six-card density produces 3.867-4.882 pt labels; do not reproduce that scale. A logo is not evidence; use scientific symbols if brand identity is irrelevant. This composition is a functional configuration atlas, not a claim that all tasks share a measured performance level.

### Figure 5 · PDF page 11 — architecture plus attention-mask inset

**Color roles.** AR lane: fill: #F5F5FF; stroke or text: #00008C [measured in PDF]; DM lane: fill: #FFFAF5; stroke or text: #A65300 [measured in PDF]; shared attention: fill: #ECECEC; stroke: #4C4D4C [measured in PDF]; token modalities: vision ar: #D1E7F2; language: #E0E0FF; vision dm: #F9DFC6; audio: #DFBFDF; action: #DDEADC [measured in PDF]; mask: ar causal: #AFAFEC; dm full: #ECCBAB; masked: #F6F6F6 [measured in PDF].

**Typography.** figure text: visible text fonts: XCharter-Roman, XCharter-Bold, Computer Modern math families; observed size pt: tower labels and legend: 7.991; subsequence headers and layer labels: 5.994; encoder and token text: 4.662; some subscripts: 3.33 [measured in PDF]

Visible text traces (type 0) support font family, rendered size and text color extraction.

**Geometry and spacing.** lane width pt: 121.268 [measured in PDF]. lane height pt: 92.088 [measured in PDF]. inter lane gap pt: 3.789 [measured in PDF]. shared bridge width height pt: 227.378, 27.854 [measured in PDF]. matrix size pt: 104.596, 104.596 [measured in PDF]. layout: ~247 pt architecture region + ~41 pt gap + ~136 pt inset including axes; columns share y levels for encoders, token strip, norm, attention, norm, MLP and outputs. [visual observation].

**Composition, grouping, and routing.**

- Two aligned pathways meet once in a shared operator; a linked matrix explains its attention structure. [visual observation]
- AR and DM use cool/warm heading and arrow colors, while modalities retain a second-level token palette. [visual observation]
- Shared attention crosses both lanes and is neutral gray, so common computation is visually explicit. [visual observation]
- Two fine dashed connector rays link operator bounds to the matrix inset. [visual observation]
- Matrix subdivisions reproduce the same AR/DM color identity and show masked zeros distinctly. [visual observation]
- Solid token borders versus dashed noisy-token borders encode an additional state without adding a new hue. [visual observation]
- Encoder borders 0.333 pt, shared operator border 0.666 pt; inset connector 0.533 pt with ~1.998 pt dash/gap. [measured in PDF]
- Full-width token key is placed below the architecture/inset pair. [visual observation]

**What works.** Two aligned pathways meet once in a shared operator; a linked matrix explains its attention structure.

**Adaptation.** Align parallel streams to identical y levels; bridge them only at a verified shared operation. Use subtle lane fills, stronger semantic outlines, and a neutral shared module. Allocate an inset for the local rule (mask, gate, routing matrix) and connect it to its exact source module. Keep mathematical and modality notation stable between overview, inset and legend.

**Limitations and changes to make.** Some source glyphs are 3.33 pt; simplify subscripts and enlarge at final publication size. Do not use an attention-mask matrix as decoration or copy topology to an unrelated mechanism. A six-color modality palette requires labels/shapes; hue alone is insufficient.

### Figure 8 · PDF page 20 — curriculum matrix plus flow

**Color roles.** image mode: fill: #F2DADA; stroke text: #7A2E2E [measured in PDF]; video mode: fill: #F9E3CD; stroke text: #955311 [measured in PDF]; audiovisual mode: fill: #E3C7E3; stroke text: #4D004D [measured in PDF]; action mode: fill: #D9E7D7; stroke text: #3D6039 [measured in PDF]; transfer: fill: #D1E7F2; stroke text: #00476D [measured in PDF]; inactive: fill: #F6F6F6; stroke: #DBDBDB; value: em dash [measured in PDF].

**Typography.** figure text: visible text fonts: XCharter-Roman, XCharter-Bold; observed size pt: column headers: 7.256; mode labels: 6.513; cell values and model labels: 6.449 [measured in PDF]

Visible text traces (type 0) support font family, rendered size and text color extraction.

**Geometry and spacing.** cell width height pt: 41.288, 21.791 [measured in PDF]. vertical cell gap pt: 2.753 [measured in PDF]. pre mid column gap pt: 14.91 [measured in PDF]. composition: Five modality rows; pre/mid columns grouped on left; shared model in a central gap; post-training column and output labels on right. [visual observation].

**Composition, grouping, and routing.**

- A categorical training-stage matrix carries data amounts, then routes the shared model to specialized post-training outcomes. [visual observation]
- Row labels, cell borders and outcome labels share darker versions of row hue. [visual observation]
- Cell fills are light; amounts are black and centered. [visual observation]
- Every cell uses equal area: values are text, so this is not an area encoding of sample count. [visual observation]
- Inactive cells use an em dash and gray rather than a misleading zero. [visual observation]
- Mid-training outputs converge into a shared model; post-training branches then fan out; no model-count proportional line widths. [visual observation]
- Active border 0.524 pt versus inactive 0.403 pt. [measured in PDF]

**What works.** A categorical training-stage matrix carries data amounts, then routes the shared model to specialized post-training outcomes.

**Adaptation.** Use a stage-by-capability matrix when readers must track activation and data amounts together. Preserve dark-label/light-fill pairs and use a neutral unavailable state. Reserve inter-stage whitespace for actual transformations or shared checkpoints instead of squeezing in another box.

**Limitations and changes to make.** Colors identify modes; they do not encode quantity. Distinct amounts must retain their stated units/denominators. Six-ish-point source text requires enlargement or less content in a narrow figure.

### Figure 11 · PDF page 33 — infrastructure flow

**Color roles.** data: fill: #D1E7F2; stroke text: #00476D [measured in PDF]; training: fill: #D9E7D7; stroke text: #3D6039 [measured in PDF]; serving: fill: #E3C7E3; stroke text: #4D004D [measured in PDF]; benchmark: fill: #FFF0E0; stroke text: #C76300 [measured in PDF]; edges: stroke: #4C4D4C [measured in PDF].

**Typography.** figure text: visible text fonts: XCharter-Roman, XCharter-Bold; observed size pt: module titles: 6.029; subtitles: 4.69; edge labels: 5.359 [measured in PDF]

Visible text traces (type 0) support font family, rendered size and text color extraction.

**Geometry and spacing.** module width height pt: 51.467, 43.842 [measured in PDF]. module border pt: 0.469 [measured in PDF]. first three step center distance pt: 91.497 [measured in PDF]. composition: Aligned compact rectangular modules, edge labels above horizontal connectors, dashed separator before the benchmark branch. [visual observation].

**Composition, grouping, and routing.**

- A restrained flat flow uses four coherent color pairs and an explicit separation between serving and benchmarking branches. [visual observation]
- Module title is bold on two lines; descriptive role is smaller below. [visual observation]
- Each module uses its dark outline hue for both title and subtitle. [visual observation]
- Checkpoint is explicitly repeated as an input to the independent benchmark path; a dashed divider separates paths. [visual observation]

**What works.** A restrained flat flow uses four coherent color pairs and an explicit separation between serving and benchmarking branches.

**Adaptation.** A plain rectangular diagram can have visual character through calibrated hue/tint, typography and spacing. Use matching box dimensions for same-level modules and separate branch inputs explicitly.

**Limitations and changes to make.** Do not mistake the benchmark position on the right for a serial dependency after serving; follow its incoming checkpoint/data arrows and caption. Tiny subtitle type is an anti-pattern to fix, not a quality standard.

## Harness²: Recursive Agent Harnessing for an Open World

**Source:** [v1 PDF](https://arxiv.org/pdf/2610.14224v1) · [arXiv record](https://arxiv.org/abs/2610.14224v1) · Google Cloud AI Research; Northwestern University.
**Date provenance:** initial submission: 2026-10-09; version date: 2026-10-09; pdf front date: 2026-10-12.
**Affiliation evidence:** Ruiyao Xu (Northwestern University, work while intern at Google Cloud AI Research); remaining authors Google Cloud AI Research.

### Figure 1 · PDF page 1 — paired result charts

**Color roles.** base: fill: #CFCFCF [measured in PDF]; comparison: fill: #CDBBE0; label: #6D3F7D [measured in PDF]; proposed: fill: #DBE4EF; stroke label: #3F5F92 [measured in PDF]; grid: stroke: #E9ECF0 [measured in PDF]; spines: stroke: #C9CED6 [measured in PDF].

**Typography.** figure text: font metadata: TimesNewRomanPSMT, TimesNewRomanPS-BoldMT, STIXGeneral math; observed overlay size pt: category labels: 9.527; axis labels: 9.112; ticks: 8.284; value labels: 7.87; legend: 8.077 [searchable overlay only]

Text trace type 3 denotes invisible searchable text; visible glyphs are path outlines. Treat font metadata as source overlay metadata; do not use its black color as visible label color.

**Geometry and spacing.** composition: Approx. 1.6:1 plot-width allocation to 9 bars versus 3 trajectories; shared top alignment; direct trajectory labels at the right; horizontal grids only. [visual observation].

**Composition, grouping, and routing.**

- A wider grouped comparison and a compact scaling plot share a muted gray/lavender baseline palette and dark-blue emphasis. [visual observation]
- Proposed trajectory line 2.485 pt; comparison trajectories 1.864 pt (4:3 width ratio). [measured in PDF]
- White-centered circular markers for proposed curve, lavender squares and gray triangles for baselines. [visual observation]
- Baseline traces use distinct dash patterns; proposed curve solid. [visual observation]
- Each bar prints its absolute value; blue gain annotations above proposed bars create a second reading level. [visual observation]
- Three tiny repeated brand/model icons appear inside proposed bars. [visual observation]

**What works.** A wider grouped comparison and a compact scaling plot share a muted gray/lavender baseline palette and dark-blue emphasis.

**Adaptation.** Use a stronger dark contour with pale fill to emphasize one condition without saturating the whole panel. Pair absolute values with explicit deltas where they answer different reader questions. Allocate panel widths according to data density and use direct labels to reduce legend lookup.

**Limitations and changes to make.** The bar axis is truncated around the low 60s, visually amplifying height differences. Prefer dots or a zero bar baseline unless a justified discontinuity is explicit. Small logos inside bars are nonessential and should not obstruct measured marks. Do not infer error bars or significance from these visual comparisons.

### Figure 2 · PDF page 3 — nested harness architecture

**Color roles.** context: stroke heading: #2F5597; fill: #E3EBF6; inner stroke: #B9C9E2 [measured in PDF]; middleware: stroke heading: #7B5FB5; fill: #F1ECF8; inner stroke: #D7CBEA [measured in PDF]; tools: stroke heading: #4F7D58; fill: #E9F0E7; inner stroke: #C6D8C5 [measured in PDF]; orchestration: stroke heading: #A5637E; fill: #F6EDF1; inner stroke: #E5CAD6 [measured in PDF]; neutral: ink: #1F2937; secondary: #6B7280; code: #55637A [measured in PDF].

**Typography.** figure text: font metadata: Charter-Roman, Menlo-Regular; observed overlay size pt: group headers: 8.026; component names: 7.644; filenames and id badges: 5.351; frequency pills: 5.16; model label: 7.453 [searchable overlay only]

Text trace type 3 denotes invisible searchable text; visible glyphs are path outlines. Treat font metadata as source overlay metadata; do not use its black color as visible label color.

**Geometry and spacing.** native canvas pt: 470.56, 168.284 [measured in PDF]. context container pt: 129.546, 156.896 [measured in PDF]. middle model outer diameter pt: 65.493 [measured in PDF]. middleware container pt: 219.51, 113.714 [measured in PDF]. orchestration height pt: 38.864 [measured in PDF]. inner context card pt: 118.032, 28.788 [measured in PDF]. card vertical gap pt: 3.598 [measured in PDF]. context horizontal padding pt: 5.757 [measured in PDF]. outer inner hub stroke pt: 0.764, 0.573, 1.147 [measured in PDF]. composition: Left context ~27.5% width; center hub/output corridor; right middleware with nested tools and a lower orchestration strip. [visual observation].

**Composition, grouping, and routing.**

- Role-colored containers, white component cards, metadata pills, and a central frozen-model hub establish several levels of hierarchy. [visual observation]
- Round-corner category containers carry tint; individual components stay white. [visual observation]
- Component ID badge, human name, monospace path and frequency pill distinguish four text roles. [visual observation]
- Titles sit at a consistent inset, with short gray role descriptions below. [visual observation]
- The central model has a double ring, a white interior and a distinct mathematical M. [visual observation]
- Forward call and return result arrows occupy separate horizontal tracks and carry labels. [visual observation]
- Dashed rose branch to subagents differs from the solid runtime call path. [visual observation]
- A faint raster glow behind the hub exists, but topology is legible without it. [visual observation]

**What works.** Role-colored containers, white component cards, metadata pills, and a central frozen-model hub establish several levels of hierarchy.

**Adaptation.** Use a colored boundary for a genuine subsystem, then white cards for members. Give one hue a dark outline/title, medium badge and pale background variant. Separate technical identifiers in mono from reader-facing labels in the main font. Route opposite directions on separate tracks; keep a clear hub corridor. Use frequency/status pills only when execution timing or state is scientifically relevant.

**Limitations and changes to make.** The 5.16-5.35 pt metadata is very small; retain fewer details or split the figure at manuscript size. A colored box must map to a real system boundary, not arbitrary visual decoration. The original is partly outlined and cannot be called fully editable text merely because text extraction works.

### Figure 3 · PDF page 5 — two-level recursion storyboard

**Color roles.** task lane: fill: #F4F5FC; border: #CCE5FF; heading: #2271AE [measured in PDF]; harnessing lane: fill: #F9F2FF; border text: #9673A6 [measured in PDF]; outer return loop: fill: #C6ABD3 [measured in PDF]; invariant branch: fill: #D5E8D4; stroke: #82B366 [measured in PDF]; domain branch: fill: #FFF2CC; stroke: #D6B656 [measured in PDF]; forward reflection arrow: fill: #A9C4EB [measured in PDF].

**Typography.** figure text: visible text fonts: ComicSansMS, Times-Bold; observed size pt: role labels: 6.103; branch micro labels: 5.548; loop text and store: 7.767; task badge: 8.877; lane titles: 10.542 [measured in PDF]

Visible text traces (type 0) support font family, rendered size and text color extraction.

**Geometry and spacing.** composition: Long landscape figure; task-level lane occupies roughly three quarters of width, reflection/update column the remainder; outer rounded perimeter carries an orthogonal return path along the bottom. [visual observation].

**Composition, grouping, and routing.**

- A task-level sequence is enclosed in a cool lane; a separate reflection/update lane feeds an outer return loop into the next task. [visual observation]
- Repeated robot icons assign executor/editor/composer roles; branch icons and document symbols distinguish working artifacts. [visual observation]
- Small black arrows show local execution; broad pastel arrows show cross-level reflection/update/next-task transitions. [visual observation]
- Invariants and domain-specific edits occupy separate green and warm-yellow sub-rows. [visual observation]
- The final harness uses a green artifact card; improvement harness uses a persistent-store cylinder. [visual observation]
- The return line turns at the outer margin and points upward at the next-task entry. [visual observation]
- Local flow stroke roughly 0.555 pt; broad loop is a filled vector path, not a thick arrow line. [measured in PDF]

**What works.** A task-level sequence is enclosed in a cool lane; a separate reflection/update lane feeds an outer return loop into the next task.

**Adaptation.** Use two arrow scales only when they encode two real abstraction levels. Frame the local workflow and its slower adaptation loop separately. Use a recurring icon system sparingly to make repeated roles/artifacts recognizable. Place feedback along the perimeter, away from labels and local edges.

**Limitations and changes to make.** Mixed Comic Sans/Times and many raster icons are an observed aesthetic, not a mandatory high-quality style. A coherent publication font pair is easier to reproduce. The small role labels demand simplification if the same composition is reduced. Do not add reflection or memory-update edges unless the described method has them.

### Figure 9 · PDF page 12 — case-study evidence storyboard

**Color roles.** context artifacts: accent: #6C8EBF; heading: #2F5F9E; tint: #EEF5FE; border: #AEC1DC [measured in PDF]; tool artifacts: accent: #82B366; heading: #3D7A2E; tint: #ECF5EC; border: #BAD5AB [measured in PDF]; inherited: fill: #F6F6F8; border: #DADADA; text: #B8BAC6 [measured in PDF]; group perimeter: stroke: #C5B2CE [measured in PDF]; outcome perimeter: stroke: #EACFDA [measured in PDF]; ink: fill: #2B2E3B [measured in PDF].

**Typography.** figure text: font metadata: DejaVuSerif, DejaVuSerif-Bold, DejaVuSerif-Italic, DejaVuSansMono, DejaVuSansMono-Bold; observed overlay size pt: outcome value: 13.486; task body: 5.291; main body: 5.083; file names: 4.357; small pills: 3.631 [searchable overlay only]

Text trace type 3 denotes invisible searchable text; visible glyphs are path outlines. Treat font metadata as source overlay metadata; do not use its black color as visible label color.

**Geometry and spacing.** left middle right width pt: 77.797, 261.176, 66.683 [measured in PDF]. inter column gaps pt: 19.449, 19.449 [measured in PDF]. common column height pt: 216.764 [measured in PDF]. inner two card column width pt: 120.864 [measured in PDF]. inner column gap pt: 5.557 [measured in PDF]. composition: Approx. 17.5% task, 58.8% evidence, 15.0% outcome and 8.7% combined gaps; evidence dominates because it explains the mechanism. [visual observation].

**Composition, grouping, and routing.**

- Task/failure, changed artifacts, and outcome form a three-part narrative with explicit provenance of edited versus inherited components. [visual observation]
- A component strip at the top identifies edited versus inherited modules; tint is a provenance channel, not a magnitude scale. [visual observation]
- Artifact cards have a narrow colored left rail, file-type badge, monospace name, source/size metadata and a small invocation pill. [visual observation]
- Code is shown in monospace; explanatory prose in serif, preserving their functional distinction. [visual observation]
- A dashed outer evidence boundary contrasts with solid task/outcome frames. [visual observation]
- Arrow labels bridge columns; outcome value is ~2.6x task body size. [visual observation]
- Subtle depth is produced by three offset shapes at opacity 0.035 each; this is optional and should not compete with data. [visual observation]

**What works.** Task/failure, changed artifacts, and outcome form a three-part narrative with explicit provenance of edited versus inherited components.

**Adaptation.** Allocate most width to causal/mechanistic evidence rather than a giant outcome number. Make changed versus inherited content explicit and carry the same semantic categories into individual artifacts. Use one representative snippet per module in a main-paper figure; put full files in an appendix or linked detail.

**Limitations and changes to make.** Original dense text falls to 3.63-5.29 pt; this is a warning, not a font-size target. File-like cards are useful when the research object is a file-based harness; they are not a universal diagram container. A single case study cannot replace aggregate evidence or establish a general effect.

## B. Additional 2025–2026 sources

## DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models

**Source:** [v1 PDF](https://arxiv.org/pdf/2512.02556v1) · [arXiv record](https://arxiv.org/abs/2512.02556v1) · DeepSeek-AI.
**Date provenance:** initial submission: 2025-12-02.
**Affiliation evidence:** DeepSeek-AI.

### Figure 2 · PDF page 4 — Attention architecture: neutral backbone with a highlighted sparse-selection branch

**Color roles.** core attention: #CFD3D6 [measured in PDF]; new branch fill: #C9EAC4 [measured in PDF]; new branch connectors: #9EDB96 [measured in PDF]; branch math labels: #30711A [measured in PDF]; all other connections: #000000 [measured in PDF].

**Typography.** observed type hierarchy: Measured Calibri 9.557 pt general labels; Calibri 11.134 pt core-attention title; Calibri Bold 11.134 pt indexer/selector; Calibri Italic 7.980 pt transform notes; Cambria Math for variables and smaller subscripts. The 11.134/9.557 ratio is 1.165, and main-label/annotation ratio is 1.198. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.5973 pt (119 paths), 1.1946 pt (11 paths), 1.5928 pt (8 paths), 1.0951 pt (2 paths) [measured in PDF]. geometry notes: Measured base outline 0.5973 pt; stronger outlines 1.1946 pt; green branch strokes 1.5928 pt. The highlighted branch is therefore about 2.67 times the base stroke width. Repeated tensor tiles and orthogonal route elbows create a rhythm without an enclosing presentation card. [measured in PDF].

**Composition, grouping, and routing.**

Bottom-to-top data flow. The large full-width core-attention bar spans both the conventional left branch and the new right branch. Tensor groups are small stacked tiles with circles, not generic labeled boxes. The selection operation is a trapezoid and the indexer is a rounded rectangle, distinguishing the operation types. Labels sit beside tensor tiles instead of competing inside them. Use actual arrowheads at intended ports. Orthogonal routes go through open whitespace and enter a visible edge, while stacked copies indicate multiplicity. The green connector identity persists through the new branch and connects to the shared attention bar.

**What works.** Attention architecture: neutral backbone with a highlighted sparse-selection branch

**Adaptation.** For an added memory or routing mechanism, keep inherited computation neutral and use one saturated connector color plus one pale fill for the new path. Use different primitive shapes for state, projection, selection and combination, rather than coloring identical boxes.

**Limitations and changes to make.** Do not treat the palette as a DeepSeek brand rule. Math subscripts reach 5.83 pt in this PDF; retain the hierarchy but enlarge or simplify for the destination width. Green saturation alone is insufficient to distinguish paths in grayscale: add direct labels and a line-style distinction when appropriate.

### Figure 4 · PDF page 9 — Thinking retention shown as aligned conversation-state columns

**Color roles.** input container: #ECEFF4 [sampled raster]; existing context items: #CFD3D6 [sampled raster]; tool calls outputs: #CDDDFF [sampled raster]; thinking segments: #689EFE [sampled raster].

**Typography.** observed type hierarchy: The entire figure is one JPEG. Font family and original point sizes are not recoverable from PDF text spans; describe the face only as visually sans serif. Any exact font name would be a guess. [visual observation]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** geometry notes: Embedded image is 1280×671 pixels and is placed at 430.861×225.865 PDF points (aspect ratio 1.907). Palette values are dominant raster RGB samples, affected by JPEG compression; they are not exact vector authoring colors. [visual observation].

**Composition, grouping, and routing.**

Four vertically growing columns are aligned to turn headings. Each column contains a pale input group followed by a paler output group. Repeated content stays in the same visual language as the sequence grows. A dotted blue enclosure groups the first three columns and points to the next user turn. Vertical braces explain which output becomes the next input. Use shallow braces for accumulation and a dotted enclosure for a phase. This avoids routing many individual arrows through the boxes. Preserve the distinction between containment, temporal sequence and actual data flow.

**What works.** Thinking retention shown as aligned conversation-state columns

**Adaptation.** For agent context retention or memory evolution, show state snapshots across turns. Make previous state gray, newly generated content tinted, and the active state most saturated; align corresponding content rows so the change can be understood without following long return paths.

**Limitations and changes to make.** The raster export prevents editable text and exact font verification. Adjacent pale blue/gray states need labels. Do not use this layout to imply exact byte/token counts unless row heights encode those quantities intentionally.

## Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models

**Source:** [v1 PDF](https://arxiv.org/pdf/2601.07372v1) · [arXiv record](https://arxiv.org/abs/2601.07372v1) · Peking University and DeepSeek-AI.
**Date provenance:** initial submission: 2026-01-12.
**Affiliation evidence:** Peking University and DeepSeek-AI.

### Figure 1 · PDF page 3 — Backbone plus exploded memory mechanism with token-level evidence

**Color roles.** compute: #FFE6CC [measured in PDF]; memory and token chips: #E1D5E7 [measured in PDF]; retrieval and fusion: #D5E8D4 [measured in PDF]; projection: #DAE8FC [measured in PDF]; vocabulary embedding: #F8CECC [measured in PDF]; module background: #F5F5F5 [measured in PDF]; token outline: #9673A6 [measured in PDF].

**Typography.** observed type hierarchy: ArialMT 7.389 pt labels, with a 6.773 pt convolution label. Black label text is kept neutral even when fills differ. The figure uses a consistent compact sans face while the manuscript caption uses a serif face. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.6157 pt (113 paths), 0.4354 pt (3 paths), 0.5332 pt (2 paths) [measured in PDF]. geometry notes: Measured backbone container 62.496×133.613 pt; expanded mechanism container 207.501×179.793 pt. Its width is 3.32 times the backbone width. Dominant stroke 0.6157 pt. Memory tiles are roughly 66×21.55 pt; token chips are 12.315 pt high with width fitted to the string. Back/front embedding copies have fill opacities 0.5/0.8/1.0, making multiplicity legible. [measured in PDF].

**Composition, grouping, and routing.**

A narrow vertical backbone occupies the left; a much larger rectangular detail view occupies the right. A real token sequence runs along the bottom and selected n-grams are grouped with dashed rectangles. Two parallel n-gram lookup branches converge into fusion. Stacked memory tiles convey multiple heads; small triangles mark linear projections. Dashed diagonal lines are zoom correspondences, not computational edges. Data arrows are thin black with visible arrowheads. Junction circles and multiplicative symbols explicitly mark operations. The two conventions should never share an unlabeled line style.

**What works.** Backbone plus exploded memory mechanism with token-level evidence

**Adaptation.** Expose a new memory mechanism by combining a high-level spine, a magnified module and a concrete miniature example. Scale the expanded view to the reasoning burden rather than giving every box equal size. Repeat the exact token/memory color through both overview and expansion.

**Limitations and changes to make.** Do not copy the literal token example or module topology into an unrelated method. Token chips must correspond to actual items, and layer multiplicity needs a stated interpretation. Low-opacity stacks must remain distinguishable after grayscale export.

### Figure 2 · PDF page 5 — Matched training and inference views with explicit host/device location

**Color roles.** compute: #FFE6CC [measured in PDF]; memory: #E1D5E7 [measured in PDF]; vocabulary embedding: #F8CECC [measured in PDF]; container: #F5F5F5 [measured in PDF].

**Typography.** observed type hierarchy: ArialMT 7.175 pt module labels; Arial Bold 8.371 pt panel headings; Arial Bold 6.577 pt location annotations. The panel-heading/module ratio is 1.167. The smallest memory-hierarchy qualifier is 5.381 pt. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.5979 pt (104 paths) [measured in PDF]. geometry notes: Dominant outline width 0.5979 pt. Storage uses a cylinder, compute uses rectangles and the whole repeated layer uses a rounded enclosure. Similar shapes occupy similar visual sizes in both panels. [visual observation].

**Composition, grouping, and routing.**

Two balanced side-by-side panels share vertical orientation, backbone shapes, component colors and bottom input placement. The left uses two replicated blocks for cross-device training; the right separates device compute from an offloaded cylindrical store on the host. Panel headings sit below the drawings, not inside heavy title boxes. Solid vertical arrows express computation; dotted lateral routes express communication. The all-to-all link crosses only the gap between replicated blocks. Host prefetch links are routed outside the device container with explicit location labels.

**What works.** Matched training and inference views with explicit host/device location

**Adaptation.** For training versus inference or local versus remote memory, make a matched pair with the same semantic palette and stable object vocabulary. Let changed location and connectivity carry the comparison instead of redrawing the entire style.

**Limitations and changes to make.** A cylinder should denote a store, not a learned transform. Qualifier text is undersized at manuscript scale in the source; use a larger canvas or move the qualifier to the caption rather than inheriting 5.38 pt.

### Figure 3 · PDF page 6 — Purple–teal quantitative pair with distinct shapes and light grids

**Color roles.** first series: #3B2C5E [measured in PDF]; second series: #3CAEA3 [measured in PDF]; text: #262626 [measured in PDF]; major grid: #CCCCCC [measured in PDF]; secondary reference: #666666 [measured in PDF].

**Typography.** observed type hierarchy: Measured DejaVu Sans 6.818 pt axis titles, 5.302 pt legend/annotation, 4.666 pt tick text, and 3.266 pt exponent glyphs. STIXGeneral Italic supplies the Greek allocation symbol. These sizes document the source, not recommended minima. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.303 pt (44 paths), 0.4545 pt (33 paths), 0.5681 pt (22 paths), 0.3787 pt (22 paths), 0.7575 pt (8 paths), 0.9469 pt (4 paths) [measured in PDF]. geometry notes: Measured series-line weights include 0.9469 pt, axes about 0.5681 pt and grid/tick strokes about 0.303 pt. The line/grid ratio is roughly 3.1. Neutral spines are lighter than the two series, and point shapes remain visible without color. [measured in PDF].

**Composition, grouping, and routing.**

Two compact landscape plots share a top edge and similar inner plot area. Left uses an allocation axis and two colored y axes; right uses a logarithmic embedding axis. Filled circles versus diamonds distinguish series; dashed trend curves are separated from observed points. A gray reference and small arrow annotation mark the pure-MoE comparison. A short gray leader identifies the reference point. The annotation is anchored to a measured point rather than an arbitrary empty region.

**What works.** Purple–teal quantitative pair with distinct shapes and light grids

**Adaptation.** Use a dark violet plus teal pair with circle/diamond redundancy, light neutral grids, and a compact reference annotation. Keep fits visually distinct from points. Give data marks a substantially heavier stroke than guides.

**Limitations and changes to make.** Do not automatically reproduce the dual-y-axis design: separate panels are safer when axis choices can create an apparent agreement. Avoid the tiny ticks and exponents; preserve the color/stroke hierarchy at a larger final-size typography.

## Qwen3 Technical Report

**Source:** [v1 PDF](https://arxiv.org/pdf/2505.09388v1) · [arXiv record](https://arxiv.org/abs/2505.09388v1) · Qwen Team (Alibaba).
**Date provenance:** initial submission: 2025-05-14.
**Affiliation evidence:** Qwen Team (Alibaba).

### Figure 1 · PDF page 9 — Training roadmap with tinted phase lanes and a serpentine flow

**Color roles.** flagship lane and steps: #FBE5D6 [measured in PDF]; lightweight lane and distillation: #DAE3F3 [measured in PDF]; initial models: #EDEDED [measured in PDF]; final model outline: #FF0000 [measured in PDF].

**Typography.** observed type hierarchy: FandolSong Regular/Bold 7.991 pt stage labels and FandolSong Bold 10.071 pt lane labels. This is an extracted serif choice, not the common assumption that all technical diagrams use Arial. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 1.1288 pt (8 paths), 1.5051 pt (2 paths) [measured in PDF]. geometry notes: Upper lane 452.305×107.822 pt; lower lane 452.305×71.152 pt (height ratio 1.515). Lane fills use 0.4 opacity while step fills use 1.0. Ordinary stage boxes are about 96×33.6 pt; the distillation block is162.116×33.606 pt. Repeated horizontal gaps between major stage columns are about22.2 pt. Main outlines 1.1288 pt; emphasized output outlines 1.5051 pt. [visual observation].

**Composition, grouping, and routing.**

The upper warm lane contains four stages arranged as two rows. The cooler lower lane shows distillation. A shared left edge aligns the two base-model inputs, and output models align on the right. A dashed separator and bold lane labels make the two scales of model construction clear. The elbow from stage 2 to stage 3 follows the inter-row gutter. The output-to-distillation path drops through the lane boundary into the lower block. Arrowheads are kept outside the label area.

**What works.** Training roadmap with tinted phase lanes and a serpentine flow

**Adaptation.** Use pale containers for phases and stronger fills for executable stages. Allow the block representing a broad transformation to be wider than routine stages. Preserve one rhythm of stage heights and gutters, and label phases explicitly.

**Limitations and changes to make.** The bright-red output border is a source-specific emphasis choice, not a universal success color. Serpentine flow must carry visible stage numbers because a naive left-to-right reading would otherwise be wrong.

### Figure 2 · PDF page 20 — Four benchmark curves in a restrained shared grid

**Color roles.** thinking curve: #1F77B4 [measured in PDF]; nonthinking reference: #FF0000 [measured in PDF]; grid: #B0B0B0 [measured in PDF]; legend border: #CCCCCC [measured in PDF].

**Typography.** observed type hierarchy: The lettering is vector outlines, with no extractable text spans in the figure region. It appears serif, but the original font family and point sizes are unverified. Do not infer a font from the manuscript body. [visual observation]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.8 pt (102 paths), 0.6 pt (32 paths), 1.0 pt (32 paths), 1.5 pt (16 paths) [measured in PDF]. geometry notes: Blue data and red reference strokes 1.5 pt, frame/tick/guide strokes0.6–1.0 pt. The panels are nearly equal in width/height. Visible light dashed guides are secondary to the data. [visual observation].

**Composition, grouping, and routing.**

A2×2 plot matrix repeats the same x values and line styles. Serif plot titles identify the tasks. Each panel keeps its own y range but the bottom row shares the same x-axis wording. Red dashed horizontal references are readily separated from blue circle curves. No flow arrows are needed; the repeated x-axis and aligned panel layout encode comparison.

**What works.** Four benchmark curves in a restrained shared grid

**Adaptation.** For budget response, repeat a small number of high-contrast encodings across panels. Use shape plus line-style redundancy. Place a reference line only when its numeric meaning and experimental comparability are documented.

**Limitations and changes to make.** The source repeats identical legends four times; a shared legend can recover plotting area. Different y ranges must remain explicit. Do not use the curve smoothness as evidence of interpolation beyond sampled budgets.

## Qwen3-Omni Technical Report

**Source:** [v1 PDF](https://arxiv.org/pdf/2509.17765v1) · [arXiv record](https://arxiv.org/abs/2509.17765v1) · Qwen Team (Alibaba).
**Date provenance:** initial submission: 2025-09-22.
**Affiliation evidence:** Qwen Team (Alibaba).

### Figure 2 · PDF page 3 — Multimodal token ladder with a seven-role legend

**Color roles.** major modules: #EAEAEA [sampled raster]; outline: #192D54 [sampled raster]; model titles: #5A44CA [sampled raster]; text token: #C5C8F2 [sampled raster]; vision hidden: #FEFEC0 [sampled raster]; audio hidden: #FAE4D6 [sampled raster]; text embedding: #A8E7E2 [sampled raster]; codec hidden: #D3E590 [sampled raster].

**Typography.** observed type hierarchy: The architecture is a single high-resolution raster image:5408×5715 pixels at approximately 362.828×383.425 pt. Font identity and point sizes cannot be verified from PDF text. Visually, module labels are italic sans in purple and small token labels are dark. [visual observation]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** geometry notes: Palette samples are embedded raster RGB values after applying the PDF soft mask and compositing on white. Rounded major containers contrast with square token chips. Some background rows and codec rows have tight spacing, so token-level interpretation needs the large rendering. [visual observation].

**Composition, grouping, and routing.**

A vertical architecture links real image/video frames and a waveform at the bottom to shared thinker/talker bars, then a compact codec-generation column and output waveform above. Token strips repeat across layers so each modality keeps its identity. A small legend occupies the otherwise unused upper-left area. A large logo/wordmark occupies upper-center space. Thin dark arrows enter module boundaries; a hidden-state extraction bridge is named and visually bracketed. Parallel token rows align vertically to imply correspondence, and they should not be mistaken for exact semantic alignment unless the method supplies it.

**What works.** Multimodal token ladder with a seven-role legend

**Adaptation.** When the scientific contribution is cross-modal flow, show a concrete compact representation of each modality:frame, waveform and token chips. Match chip colors to a legend and retain them across layers. Use large neutral module bars so the colored data remains visible.

**Limitations and changes to make.** Seven hues and many tiny labels are expensive. Reduce to the modalities relevant to the current claim. The brand wordmark is decorative and should not consume the explanatory space of an original scientific figure. Do not claim Futura from appearance; it is unverified for this raster.

### Figure 3 · PDF page 4 — Vertical encoder–decoder stack with a bypass route

**Color roles.** module container: #E9E9E9 [sampled raster]; outline: #172C51 [sampled raster]; titles: #5A44CA [sampled raster]; input features: #FFD966 [sampled raster]; hidden state: #F5DFD4 [sampled raster]; feature annotation: #BF9000 [sampled raster].

**Typography.** observed type hierarchy: One4001×3689 raster image, approximately 272.132×250.911 pt in the PDF; no extractable figure fonts or original point sizes. Purple italic module labels visibly form a hierarchy over small neutral annotations. [visual observation]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** geometry notes: The neutral rounded container is the largest shape, internal operations are white outlined strips, and data representations are low-height capsule rows. This produces three distinct visual levels with modest use of color. [visual observation].

**Composition, grouping, and routing.**

Waveform, filter-bank chips, encoder, hidden chips and decoder form a single central vertical spine. Thin internal white boxes expose only the relevant sublayers. Braces label repetition counts. A right-side bypass route carries the text prefix directly to the decoder. The long bypass is routed in the outer right gutter and terminates at the decoder port. It stays separate from the upward central flow, illustrating a good alternative to drawing a return line on top of a box border.

**What works.** Vertical encoder–decoder stack with a bypass route

**Adaptation.** For a narrow mechanism, use a central spine plus one reserved outer route channel. Distinguish group containers, internal functions and flowing data by shape/height as well as fill. Use braces for repetition instead of duplicating every layer.

**Limitations and changes to make.** Source is raster and its exact font is unknown. Do not draw a bypass without an actual corresponding dependency. The bypass should enter a visibly distinct port and avoid touching the container outline anywhere else.

## Qwen3-VL-Embedding and Qwen3-VL-Reranker: A Unified Framework for State-of-the-Art Multimodal Retrieval and Ranking

**Source:** [v1 PDF](https://arxiv.org/pdf/2601.04720v1) · [arXiv record](https://arxiv.org/abs/2601.04720v1) · Qwen Team (Alibaba).
**Date provenance:** initial submission: 2026-01-08.
**Affiliation evidence:** Qwen Team (Alibaba).

### Figure 2 · PDF page 3 — Shared model comparison with a continuous backbone and distinct outputs

**Color roles.** text tokens: #C8C7F5 [measured in PDF]; vision tokens: #A2DCDE [measured in PDF]; model weights: #F5DDBF [measured in PDF]; hidden states: #9A9A9A [measured in PDF]; title text: #5C48D4 [measured in PDF]; decoder outline: #BC6A76 [measured in PDF]; vision outline: #194880 [measured in PDF].

**Typography.** observed type hierarchy: Measured Futura Medium for ordinary labels and Futura MediumItalic for modules/titles. Role hierarchy:legend 6.78 pt; token labels 7.91 pt; result labels10.17 pt; module labels11.188 pt; task headings13.56 pt; shared decoder15.82 pt. Purple#5C48D4 unifies the italic title tier. Decoder/ordinary result ratio1.556; task heading/legend ratio2.0. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 1.2712 pt (26 paths) [measured in PDF]. geometry notes: Shared decoder envelope446.907×89.997 pt; vision-encoder bar289.215×24.594 pt; LM head62.828×18.079 pt; state squares about17.6×18.08 pt. Uniform measured shape outline 1.2712 pt. These are PDF-page measurements, not recommended font/shape sizes for every destination. [visual observation].

**Composition, grouping, and routing.**

Embedding and reranking tasks are placed side by side above one large continuous decoder shape. A short dashed center divider separates task-specific inputs and outputs without slicing the shared module. Token squares sit above the model; hidden-state squares and the reranker head sit below. The legend runs along the bottom. Short horizontal arrows below the backbone explain the result head. Shared model identity is conveyed by the continuous shape rather than extra cross-panel arrows.

**What works.** Shared model comparison with a continuous backbone and distinct outputs

**Adaptation.** To compare two uses of one backbone, draw the shared component once across the task columns and keep inputs/outputs task-specific. Use color and shape for text tokens, visual tokens, model weights and hidden state. Let the genuinely shared mechanism receive the largest type.

**Limitations and changes to make.** A continuous backbone can falsely imply parameter sharing if the methods actually have different checkpoints. Confirm sharing before using this form. Italic geometric type is a style option, not a requirement; if Futura is unavailable use a verified installed face and reflow.

### Figure 5 · PDF page 7 — Three-column training pipeline with typed nodes and edges

**Color roles.** data fill: #A6CAEC [measured in PDF]; data outline text: #163E64 [measured in PDF]; method fill: #F6C6AD [measured in PDF]; method outline text: #80350E [measured in PDF]; model fill: #F5DEBF [measured in PDF]; model outline: #1A4981 [measured in PDF]; model title: #5C48D4 [measured in PDF]; training routes: #747474 [measured in PDF]; mining routes: #8ED973 [measured in PDF].

**Typography.** observed type hierarchy: Futura Medium 8.324 pt data,9.365 pt methods; Futura MediumItalic11.446 pt primary model labels and 9.365 pt the longer stage 2 label; legend 6.243 pt. Text color echoes the relevant border family rather than turning every label black. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 1.1706 pt (17 paths) [measured in PDF]. geometry notes: Stage columns approximately121 pt wide, separated by25.6–26.5 pt gutters. Data heights28.44 pt; method heights33.30 pt; model heights27.3–28.0 pt. Main outlines 1.1706 pt. Final-column short blocks halve the height to accommodate more steps while preserving width. [visual observation].

**Composition, grouping, and routing.**

Three almost equal-width columns form successive model stages. Data nodes have folded corners, methods have square corners and models have rounded corners. A slim vertical source-model bar starts the pipeline. The final column contains more short stages; baseline alignment and repeated widths prevent it from feeling ad hoc. Gray links mean model training; green links mean data mining. Mining routes use the inter-column gap. The legend defines both edge semantics. The gray route from the shared source uses the top corridor and drops into specific operations.

**What works.** Three-column training pipeline with typed nodes and edges

**Adaptation.** Create a node grammar:data=folded corner, operation=rectangle, learned state/model=rounded rectangle. Match fill/border/text families, and reserve a separate connector style for data mining or memory updates. Specify column widths and route gutters before positioning labels.

**Limitations and changes to make.** Two arrow colors alone do not guarantee accessibility; add dash or edge labels when there are only a few paths. The legend is only 6.24 pt in the source and should be enlarged. Variable block height must signify packing, not duration, unless explicitly encoded.

## Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material

**Source:** [v1 PDF](https://arxiv.org/pdf/2506.15442v1) · [arXiv record](https://arxiv.org/abs/2506.15442v1) · Tencent Hunyuan.
**Date provenance:** initial submission: 2025-06-18.
**Affiliation evidence:** Tencent Hunyuan.

### Figure 2 · PDF page 5 — Hybrid pipeline mixing real outputs, latent chips and vector modules

**Color roles.** linear norm: #CBEAFF [measured in PDF]; conditioning attention: #F6C6AD [measured in PDF]; transformer repeats: #A6A6A6 [measured in PDF]; query token examples: #D7E2FA [measured in PDF]; latent secondary: #94C1C9 [measured in PDF].

**Typography.** observed type hierarchy: Extracted Century Gothic Bold mainly4.55–5.42 pt; major group labels 6.838 pt. Aptos Bold supplies ellipses; DengXian Bold appears in a variable label. The label density is high and the source absolute sizes are too small for robust reuse. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.5693 pt (13 paths) [measured in PDF]. geometry notes: Main shape strokes 0.5693 pt. Vertical narrow transform bars alternate two pastel families; groups are enclosed by subtle dotted or dashed rounded borders. The figure uses actual pixel images for object, noise and outputs alongside vector labels/boxes. [visual observation].

**Composition, grouping, and routing.**

A real input thumbnail, latent-noise strip and timestep enter an outlined DiT group. A narrow latent-chip column separates the DiT from a VAE-decoder group. Two rendered output views appear on the right. Different dashed group-outline colors classify the stages without filling every region heavily. The main path is horizontal with a small number of lower conditioning routes. Arrows terminate on group ports and internal bar edges. A multiplication label denotes repeated attention instead of drawing all 16 blocks.

**What works.** Hybrid pipeline mixing real outputs, latent chips and vector modules

**Adaptation.** Use a real input/output miniature when visual data is the subject, while keeping processing stages editable vectors. Use low-saturation contrasting groups and narrow internal operation bars to achieve density without nested heavy boxes.

**Limitations and changes to make.** Never copy the tiny4–5 pt label scale. Avoid rotating text unless a vertical bar materially saves space; otherwise simplify the submodule or show a separate expansion. Image examples must be representative and attributed.

### Figure 3 · PDF page 5 — Compact DiT block with a colored latent ribbon

**Color roles.** token neutral: #D9F2D0 [measured in PDF]; token warm: #F2AA84 [measured in PDF]; attention: #96DCF8 [measured in PDF]; normalization: #F6C6AD [measured in PDF]; linear moe: #A6A6A6 [measured in PDF]; group border: #B4E5A2 [measured in PDF].

**Typography.** observed type hierarchy: Century Gothic4.083–4.089 pt token/skip labels and6.221–6.228 pt operation labels; Century Gothic Bold for the group title and concat symbol. A Calibri label appears for Linear, demonstrating an inconsistent mixed-font detail to avoid. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.5835 pt (24 paths), 0.778 pt (6 paths), 0.389 pt (3 paths), 1.0373 pt (1 paths) [measured in PDF]. geometry notes: Main internal strokes 0.5835 pt; a few stronger 0.778 pt outlines; boundary 1.0373 pt. Internal function bars are tall/narrow and are placed on a common baseline. Modality cells use explicit outlines, not just adjacent color blocks. [visual observation].

**Composition, grouping, and routing.**

A horizontal chain sits inside a lightly tinted dashed green boundary. Input and output latent ribbons use small colored cells. Concatenation is a circular C node. A short skip path joins from above and separate conditioning enters from a top ribbon. Directional arrows remain aligned with the narrow center corridor. Skip and context routes approach from above and join at a visible operation node.

**What works.** Compact DiT block with a colored latent ribbon

**Adaptation.** For a detailed block inset, use a ribbon of data cells and a precise sequence of operations with explicit addition/concat symbols. The inset should preserve the overview palette and its stage identity.

**Limitations and changes to make.** Small text and mixed Calibri/Century Gothic face choice are source shortcomings, not targets. A dashed enclosure should mean a named module; do not use dashed lines indiscriminately for both grouping and data edges.

### Figure 4 · PDF page 6 — Reference/generation branches with frozen and trainable state cues

**Color roles.** residual cross attention: #A99DCB [measured in PDF]; reference attention: #D5EAED [measured in PDF]; self attention: #FFE699 [measured in PDF]; multiview attention: #F8CBAD [measured in PDF]; generation backdrop: #F5EDE1 [measured in PDF].

**Typography.** observed type hierarchy: Extracted Century Gothic and Bold; many labels3.55–5.18 pt. Cambria Math supplies ellipsis; other symbolic spans use DengXian. These tiny source sizes are a significant legibility warning. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.0603 pt (11 paths), 0.6459 pt (8 paths), 0.4306 pt (4 paths) [measured in PDF]. geometry notes: 41 image elements intersect the figure region, including thumbnails and status icons. Fill colors distinguish operations inside a purple dashed expansion boundary. Dominant functional outline about 0.646 pt; some extracted 0.060 pt outlines are extremely thin. A real-data region is visually denser than the expanded block. [visual observation].

**Composition, grouping, and routing.**

Left half shows input geometry and two aligned branches, followed by multi-view output previews. Right half expands a generation block with internal residual, reference, self and multiview attention. Flame and snowflake symbols identify trainable/frozen elements, and a compact symbol legend defines addition/concat. Routes are largely orthogonal; explicit junction circles distinguish additions. Other-view latent input enters a separately outlined RoPE region at the bottom. Frozen reference exchange and learned generation components are separate.

**What works.** Reference/generation branches with frozen and trainable state cues

**Adaptation.** Use a compact status cue such as a small lock/frozen label or trained dot only when this state matters scientifically. Pair the full data path with one detailed module, and show actual before/after or output views when they are part of the evidence.

**Limitations and changes to make.** Do not use flame/snowflake icons as decoration. The source combines many very small labels and thumbnails; a new figure should simplify or enlarge it. Ensure status is understandable without the icon or color alone.

## HunyuanVideo 1.5 Technical Report

**Source:** [v1 PDF](https://arxiv.org/pdf/2511.18870v1) · [arXiv record](https://arxiv.org/abs/2511.18870v1) · Tencent Hunyuan Foundation Model Team.
**Date provenance:** initial submission: 2025-11-24.
**Affiliation evidence:** Tencent Hunyuan Foundation Model Team.

### Figure 1 · PDF page 3 — Unequal-area training stages with concrete artifacts and evaluation outcomes

**Color roles.** SFT group text: #4EA72E [measured in PDF]; ranking group text: #0070C0 [measured in PDF]; preference group text: #80350E [measured in PDF]; accepted: #00B050 [measured in PDF]; rejected: #FF0000 [measured in PDF]; caption cards: #DCEAF7 [measured in PDF].

**Typography.** observed type hierarchy: Microsoft YaHei Bold 8.521 pt stage titles; DengXian Bold 6.74 pt node labels and DengXian 6.749 pt score labels. The title/body ratio is about1.26. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 2.1274 pt (18 paths), 0.7091 pt (12 paths) [measured in PDF]. geometry notes: Panel borders about 0.7091 pt; gray pictogram/line strokes 2.1274 pt. Rounded panels have subtle tinted fills. Check/cross outcome marks are large enough to act as a redundant shape channel. [visual observation].

**Composition, grouping, and routing.**

Two smaller left panels stack SFT and OPA-DPO; a larger right panel contains ranking. Named stage headers, tinted group backgrounds and dashed borders define the phases. Black pictograms identify data, model and human correction; caption miniatures use several horizontal text lines rather than long literal prose. Wide pale inter-panel arrows indicate stage handoff, while fine internal arrows indicate object flow and a dotted feedback path links the critic to candidate scores. A source-inspired reconstruction should label these distinct relations explicitly.

**What works.** Unequal-area training stages with concrete artifacts and evaluation outcomes

**Adaptation.** Allocate more area to the complex phase. Use small document/data miniatures to make intermediate artifacts concrete, and preserve a restrained consistent icon style. Use titled semantic zones and shape-coded outcomes.

**Limitations and changes to make.** Avoid importing saturated red/green without the check/cross or direct words. Decorative 3D-looking gradient transition arrows are not necessary. The source stage order is1→2→3 despite the2 being on the right; include numbers or choose a clearer flow for new work.

### Figure 2 · PDF page 4 — Parallel modality lanes merging into shared neutral computation

**Color roles.** language: #D6B9ED [measured in PDF]; glyph: #CFCBF4 [measured in PDF]; vision: #CADFFC [measured in PDF]; video latent: #FFD4B6 [measured in PDF]; shared attention mlp: #E8E8E8 [measured in PDF]; connectors: #747474 [measured in PDF].

**Typography.** observed type hierarchy: Aptos7.572–7.583 pt module labels,8.539 pt ellipses,5.693 pt prompt example; Cambria Math for multiplication. The main module labels are uniform and compact. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.7116 pt (11 paths), 0.9488 pt (5 paths), 0.4744 pt (1 paths), 0.0664 pt (1 paths) [measured in PDF]. geometry notes: Each modality block is63.20–63.21×17.30 pt. Column gaps are approximately10.17 pt; vertical gap between the two rows11.34 pt. Thus block-width/gutter≈6.21, and two identical-height rows establish a strong rhythm. Connector/shape widths0.4744–0.9488 pt; major tensor-ribbon enclosure is dark dashed. [visual observation].

**Composition, grouping, and routing.**

Four parallel modality columns descend from prompt/image/latent examples through two equally sized transform blocks into a single token ribbon. The ribbon feeds a shared attention bar and a dual-stream residual block. Shared computation is neutral, so modality identity resides in the incoming lanes and chips. Main arrows descend on each lane centerline. A noise input joins at an explicit plus circle. Shared-attention residuals use orthogonal side paths with visible plus nodes. The latent output color is repeated below the shared block.

**What works.** Parallel modality lanes merging into shared neutral computation

**Adaptation.** Build a consistent lane grid first; repeat widths, heights and spacing. Use color to track data through encoders and token strips, then neutralize shared operations. Put merge operations on explicit nodes, and reserve the outer gutter for residual paths.

**Limitations and changes to make.** Very similar purple lanes require labels or token patterns. Prompt miniature text is 5.69 pt in the original and should be shortened or enlarged. A four-lane template should only be used when four meaningful input paths exist.

### Figure 3 · PDF page 6 — Two-stage generative pipeline with conditioning above the main spine

**Color roles.** base model: #F7C9C3 [measured in PDF]; super resolution: #C4E2FC [measured in PDF]; prompt: #E1EAD3 [measured in PDF]; latent cards: #F2F2F2 [measured in PDF].

**Typography.** observed type hierarchy: DengXian Regular 8.021 pt modules,7.055 pt prompt,6.185 pt small data labels; DengXian Bold 8.021 pt prompt heading; Cambria Math variables 8.021 pt with 5.799 pt subscripts. [measured in PDF]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** Stroke widths: 0.2215 pt (16 paths), 0.3322 pt (3 paths), 0.443 pt (2 paths), 0.5537 pt (1 paths) [measured in PDF]. geometry notes: Thin vector strokes0.2215–0.5537 pt; pastel colored model blocks; neutral card stacks. The central upsampler is narrow and vertical, while the two key DiTs have substantial square-like bodies. [visual observation].

**Composition, grouping, and routing.**

A low-height landscape pipeline uses a shared prompt strip above the main flow, base generation at left, a compact latent-resolution transformation in the center, and super-resolution plus image frames at right. Real frames and stacked noise/latent cards add explanatory texture. The prompt fans downward into both learned models. Addition and concatenation are circular labeled nodes. Main flow runs on one horizontal axis, preventing conditioning arrows from being confused with outputs.

**What works.** Two-stage generative pipeline with conditioning above the main spine

**Adaptation.** Place shared conditioning in a separate upper band, use two distinct pastel model roles, and reserve the center for the actual resolution-changing operations. Include a small number of actual input/output frames only when needed to explain the change.

**Limitations and changes to make.** The thinnest source strokes are fragile when printed. Increase them for the actual output size. Model size and card-stack depth should not imply parameter counts or frame counts unless those quantities are intentionally encoded.

## HunyuanImage 3.0 Technical Report

**Source:** [v1 PDF](https://arxiv.org/pdf/2509.23951v1) · [arXiv record](https://arxiv.org/abs/2509.23951v1) · Tencent Hunyuan Foundation Model Team.
**Date provenance:** initial submission: 2025-09-28.
**Affiliation evidence:** Tencent Hunyuan Foundation Model Team.

### Figure 2 · PDF page 4 — Captioning pipeline with a parallel factual-grounding branch

**Color roles.** auxiliary agents: #FBE7CF [sampled raster]; auxiliary information: #FDF3D0 [sampled raster]; image icon: #ACDAB1 [sampled raster]; accepted: #4A7E7C [sampled raster]; rejected: #E54743 [sampled raster]; ink: #2C2C2C [sampled raster].

**Typography.** observed type hierarchy: Single 1918×838 raster; original font family and point size are unknown. Labels are visually simple sans serif. Palette values are sampled raster pixels, not extracted vector authoring values. [visual observation]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** geometry notes: Two gently rounded dotted containers separate agent tools from auxiliary information. The main path has no enclosing card. The narrow final verification node is centered between top and bottom branches. The diagram uses a limited, coherent icon stroke weight. [visual observation].

**Composition, grouping, and routing.**

A main image→captioning→caption row is complemented by a lower agent/information row. Both converge on verification and split into accepted/rejected outputs. Simple dark icons convey object roles; only auxiliary groups have warm tinted enclosures. Short straight or diagonal arrows show the two branches converging. Accepted and rejected marks combine color with a check/cross symbol. Each end arrow has its own terminal, avoiding overlapping routes.

**What works.** Captioning pipeline with a parallel factual-grounding branch

**Adaptation.** Use concrete small pictograms when the figure distinguishes images, text artifacts, tools and decisions. Keep tool subgroups lightly enclosed while the main data path remains open. Use one consistent icon family and label every icon.

**Limitations and changes to make.** The screenshot is raster and would need vector recreation for editable output. Do not invent a verification or rejection path for a method that lacks one. Iconography must encode a known object, not fill blank space.

### Figure 3 · PDF page 6 — Three task lanes unified by one continuous transformer bar

**Color roles.** understanding lane: #FFF0E1 [sampled raster]; generation lane: #E0F2FF [sampled raster]; language lane: #EAEAEA [sampled raster]; shared backbone: #BDE3FF [sampled raster]; generation encoder decoder: #CDF4D3 [sampled raster]; understanding encoder: #FFECBD [sampled raster]; text tokenizer: #D9D9D9 [sampled raster].

**Typography.** observed type hierarchy: One 3548×1220 raster; exact font families and point sizes are unavailable. Main block labels appear bold sans; secondary arrows and operation notes are smaller. Do not infer the face from the serif paper caption. [visual observation]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** geometry notes: Raster is placed at435.588×149.779 pt, giving aspect ratio2.908. The neutral central language lane is narrower than the image lanes. Pastel lane fills have a different role than the stronger shared-backbone fill. Group borders are understated. [visual observation].

**Composition, grouping, and routing.**

Three vertical task lanes have unequal widths based on mechanism complexity. A single blue backbone bar crosses all lanes at the same height, making shared computation immediately visible. Small tabs name the tasks. Rounded encoder/tokenizer capsules sit above/below the bar; image icons and prompt labels anchor the interfaces. Most arrows are vertical, using the common backbone as a shared meeting line. Image-understanding input splits into two encoders through a curved bifurcation. The generation branch includes an explicit noise input instead of burying it in a module label.

**What works.** Three task lanes unified by one continuous transformer bar

**Adaptation.** For a unified system serving several tasks, dedicate lanes to interfaces and draw the common backbone as one uninterrupted bar. Give each lane enough width for its real complexity; use tints for task context and stronger fills for shared computation.

**Limitations and changes to make.** The original pale-gray arrows can lose contrast. Strengthen routes in a new figure. A crossing shared bar must represent genuine shared architecture/parameters, not merely related components.

### Figure 4 · PDF page 6 — Paired attention masks with aligned token-block boundaries

**Color roles.** allowed attention: #FF9E42 [sampled raster]; grid: #CCCCCC [sampled raster]; axis and group brackets: #757575 [sampled raster]; first block outline: #66D575 [sampled raster]; second block outline: #3DADFF [sampled raster].

**Typography.** observed type hierarchy: Raster 5956×2865 pixels; original typeface and point sizes are unknown. The narrow bracket labels are visibly much smaller than the matrix cell geometry. [visual observation]

Text trace rendering modes checked for every studied region.

**Geometry and spacing.** geometry notes: The repeated cell grid and square mask extents make alignment testable. The orange fill is strong while gridlines remain very light. Sparse color outlines mark only the selected block boundaries, avoiding a many-color categorical mask. [visual observation].

**Composition, grouping, and routing.**

Two attention matrices sit side by side at the same visual scale. A single orange marks allowed attention; light-gray grid cells show token structure. Colored outlines isolate modality blocks, and left-side brackets label token intervals. Small(a)/(b) labels identify alternatives. This is a relation matrix, not a flowchart: no causal arrows are required. Bracket endpoints align to exact cell boundaries.

**What works.** Paired attention masks with aligned token-block boundaries

**Adaptation.** Use one strong mask color and a pale grid for binary connectivity, then a small number of colored outlines to locate subblocks. Match row/column order across alternatives and state what filled cells mean.

**Limitations and changes to make.** Do not use arbitrary heatmap smoothing, antialiasing gradients, or inconsistent token ordering. Never infer attention weights from this binary structural mask. Use vector rectangles for a new editable figure.

## Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation

**Source:** [v1 PDF](https://arxiv.org/pdf/2503.11926v1) · [arXiv record](https://arxiv.org/abs/2503.11926) · OpenAI.
**Date provenance:** inspected source version date: 2025-03-14.
**Affiliation evidence:** OpenAI.

### Figure 1 · PDF page 2 — a vertically ordered transcript with a rounded neutral backing; coral summary strips, green reasoning excerpts, and blue code-tool framing

**Color roles.** reasoning excerpt fill: #CEE2B8 [sampled raster]; summary strip: #F7B5A9 [sampled raster]; code/tool frame: #BDE2EE [sampled raster]; local red accent: #EC6959 [sampled raster]; channel blue accent: #00A4E3 [sampled raster]; channel green accent: #81BC47 [sampled raster].

**Typography.** Exact visible font family and authoring point size were not recoverable.

**Composition, grouping, and routing.**

a vertically ordered transcript with a rounded neutral backing; coral summary strips, green reasoning excerpts, and blue code-tool framing. Large section labels, compact body text, and local bold-italic emphasis distinguish three reading levels. Colored circular bullets repeat channel identities. Ellipses disclose omitted spans. This is a semantic transcript layout, not an architecture graph.

**Adaptation.** Use a transcript storyboard when the evidence is a sequence of observed actions or utterances. Give each channel a stable fill, header marker, and typographic role; reserve stronger weight for selected evidence. Keep excerpts short and preserve omission disclosure.

**Limitations and changes to make.** Both inspected figures are raster images in this PDF; the font family and exact authoring point size are unverified. Do not attribute body-page fonts to the image. Colors below are explicitly sampled raster colors.

### Figure 2 · PDF page 5 — a time-series composition combines light reference bars, colored/hatch-filled stacked areas, and two local intervention arrows

**Color roles.** light reference: #D9E3F9 [sampled raster]; dominant area: #6993FF [sampled raster]; second area: #9DCA1C [sampled raster].

**Typography.** Exact visible font family and authoring point size were not recoverable.

**Composition, grouping, and routing.**

a time-series composition combines light reference bars, colored/hatch-filled stacked areas, and two local intervention arrows. The legend sits beside the plot instead of over dense peaks. Gray guides and a light plotting field reduce competition with colored data. Small area classes and a broad legend are weaknesses to simplify in a new drawing.

**Adaptation.** Use a transcript storyboard when the evidence is a sequence of observed actions or utterances. Give each channel a stable fill, header marker, and typographic role; reserve stronger weight for selected evidence. Keep excerpts short and preserve omission disclosure.

**Limitations and changes to make.** Both inspected figures are raster images in this PDF; the font family and exact authoring point size are unverified. Do not attribute body-page fonts to the image. Colors below are explicitly sampled raster colors.

## Reasoning Models Struggle to Control their Chains of Thought

**Source:** [v1 PDF](https://arxiv.org/pdf/2603.05706v1) · [arXiv record](https://arxiv.org/abs/2603.05706) · OpenAI with NYU, UCL, UPenn, and MATS collaborators.
**Date provenance:** inspected source version date: 2026-03-05.
**Affiliation evidence:** OpenAI with NYU, UCL, UPenn, and MATS collaborators.

### Figure 1 · PDF page 2 — a wide paired-bar comparison occupies the top, with three narrow explanatory plots below

**Color roles.** headline condition pink: #CC79A7 [measured in PDF]; headline condition blue: #0072B2 [measured in PDF]; lower-panel amber: #E69F00 [measured in PDF]; lower-panel plum: #882255 [measured in PDF]; other lower-panel accents: #D55E00 / #009E73 [measured in PDF].

**Typography.** visible text metrics: NimbusRomNo9L-Regu 8.81 pt; NimbusRomNo9L-Regu 8.94 pt; NimbusRomNo9L-Regu 8.97 pt; NimbusRomNo9L-Regu 9.15 pt; NimbusRomNo9L-Regu 8.93 pt; NimbusRomNo9L-Regu 8.89 pt [measured in PDF] invisible searchable overlay metrics: TimesNewRomanPSMT 6.85 pt; TimesNewRomanPSMT 7.21 pt; TimesNewRomanPSMT 5.14 pt; TimesNewRomanPSMT 7.22 pt; TimesNewRomanPSMT 6.31 pt; TimesNewRomanPSMT 6.0 pt; TimesNewRomanPSMT 5.41 pt; TimesNewRomanPSMT 5.05 pt [searchable overlay only]

**Geometry and spacing.** Stroke widths: 0.451 pt (36 paths), 0.214 pt (28 paths), 1.127 pt (4 paths), 0.677 pt (1 paths) [measured in PDF].

**Composition, grouping, and routing.**

a wide paired-bar comparison occupies the top, with three narrow explanatory plots below. The main contrast repeats pink versus blue with a centered shared legend; bars carry direct numbers and dark uncertainty whiskers. The lower plots change geometry with the question, including an explicit log scale. Panel narratives sit immediately beneath each plot.

**Adaptation.** Use a dominant overview panel plus a three-part explanation row when one headline comparison requires several mechanisms. For textual evidence use a fixed schema with paired aligned cards and local violation highlights, with monospaced text confined to literal output.

**Limitations and changes to make.** Fig.1 plot labels are glyph outlines plus invisible searchable TimesNewRoman overlays; visible NimbusRoman spans are the panel explanations, not proof of the plotted font. Several searchable-overlay labels are ~5–7 pt. Fig.2 visible text is directly verified.

### Figure 2 · PDF page 3 — two equal-width evidence cards align side by side on #F9F9F9

**Color roles.** evidence-card backing: #F9F9F9 [measured in PDF].

**Typography.** visible text metrics: Inconsolatazi4-Regular 8.97 pt; NimbusRomNo9L-Regu 8.97 pt; NimbusRomNo9L-Regu 9.15 pt; NimbusRomNo9L-Medi 9.15 pt; NimbusRomNo9L-Regu 8.81 pt; NimbusRomNo9L-Regu 9.02 pt; NimbusRomNo9L-Regu 9.1 pt; NimbusRomNo9L-Medi 9.1 pt; NimbusRomNo9L-Medi 8.81 pt; NimbusRomNo9L-Medi 9.02 pt [measured in PDF]

**Composition, grouping, and routing.**

two equal-width evidence cards align side by side on #F9F9F9. Bold serif field names organize question/requirement/reasoning; Inconsolata monospaced excerpts distinguish model text; bright red marks violations at the exact token. Supporting explanations remain adjacent. Visible excerpt text is about 8.97 pt, while stronger field labels are about 9.1 pt.

**Adaptation.** Use a dominant overview panel plus a three-part explanation row when one headline comparison requires several mechanisms. For textual evidence use a fixed schema with paired aligned cards and local violation highlights, with monospaced text confined to literal output.

**Limitations and changes to make.** Fig.1 plot labels are glyph outlines plus invisible searchable TimesNewRoman overlays; visible NimbusRoman spans are the panel explanations, not proof of the plotted font. Several searchable-overlay labels are ~5–7 pt. Fig.2 visible text is directly verified.

## V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

**Source:** [v1 PDF](https://arxiv.org/pdf/2506.09985v1) · [arXiv record](https://arxiv.org/abs/2506.09985) · FAIR at Meta with Mila and Polytechnique Montreal collaborators.
**Date provenance:** inspected source version date: 2025-06-11.
**Affiliation evidence:** FAIR at Meta with Mila and Polytechnique Montreal collaborators.

### Figure 1 · PDF page 2 — an asymmetric overview maps two distinct data sources into a pretrained representation and three vertically aligned downstream branches

**Color roles.** data: #FFEFE1 [measured in PDF]; pretraining: #F0EBF5 [measured in PDF]; adaptation: #E6F5F0 [measured in PDF]; outcomes: #F1F4F7 [measured in PDF]; connectors: #465A69 [measured in PDF].

**Typography.** visible text metrics: LMSans10-Bold 8.01 pt; LMSans10-Regular 8.01 pt; LMSans10-Bold 6.41 pt; LMSans10-Bold 5.61 pt [measured in PDF]

**Geometry and spacing.** Stroke widths: 0.961 pt (11 paths), 0.32 pt (7 paths), 0.641 pt (2 paths) [measured in PDF].

**Composition, grouping, and routing.**

an asymmetric overview maps two distinct data sources into a pretrained representation and three vertically aligned downstream branches. Peach cylinders mark data, lavender marks pretraining, mint marks task-specific adaptation, and cool gray cards name downstream capabilities. Real image stacks give the input types concrete visual form. Slate connectors form one readable shared trunk; output cards use a title/divider/detail hierarchy.

**Adaptation.** Use aligned paired alternatives for training-stage changes. Preserve positions for unchanged parts, color the variable mechanism, and use actual data thumbnails only when available. For overviews, reserve one column for aligned outcomes and make the shared representation trunk explicit.

**Limitations and changes to make.** Source typography in Fig.2 is too small for direct copying. Latin Modern Sans 8.01 pt main labels in Fig.1 are measured; 0.961 pt connector strokes versus 0.320 pt quiet borders give an observable hierarchy.

### Figure 2 · PDF page 4 — paired training diagrams share corresponding positions, block shapes, and thumbnail stacks

**Color roles.** quiet modules: #DEE3E9 [measured in PDF]; loss backing: #FFE5E5 [measured in PDF]; mask/action emphasis: #FF0000 [measured in PDF]; connectors: #465A69 [measured in PDF].

**Typography.** visible text metrics: LMSans8-Regular 6.14 pt; LMSans8-Regular 6.23 pt; LMSans8-Regular 5.37 pt; LMSans10-Bold 5.45 pt; LMSans8-Regular 5.45 pt; LMSans10-Bold 7.67 pt; LMSans8-Regular 3.89 pt; LMSans10-Bold 7.79 pt; LMSans8-Regular 3.84 pt; LMSans10-Regular 7.79 pt [measured in PDF]

**Geometry and spacing.** Stroke widths: 0.934 pt (19 paths), 0.921 pt (11 paths), 0.002 pt (1 paths), 1.246 pt (1 paths), 1.228 pt (1 paths) [measured in PDF].

**Composition, grouping, and routing.**

paired training diagrams share corresponding positions, block shapes, and thumbnail stacks. A thin central separator helps comparison; gray modules are quiet while red masks/actions and loss boxes draw attention to the difference. Dotted EMA and dashed stop-gradient paths differ from solid data routes. Visible Latin Modern Sans is used, but minor labels descend below 4 pt.

**Adaptation.** Use aligned paired alternatives for training-stage changes. Preserve positions for unchanged parts, color the variable mechanism, and use actual data thumbnails only when available. For overviews, reserve one column for aligned outcomes and make the shared representation trunk explicit.

**Limitations and changes to make.** Source typography in Fig.2 is too small for direct copying. Latin Modern Sans 8.01 pt main labels in Fig.1 are measured; 0.961 pt connector strokes versus 0.320 pt quiet borders give an observable hierarchy.

## V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning

**Source:** [v3 PDF](https://arxiv.org/pdf/2603.14482v3) · [arXiv record](https://arxiv.org/abs/2603.14482) · FAIR at Meta with Universidad de Zaragoza.
**Date provenance:** inspected source version date: 2026-06-11.
**Affiliation evidence:** FAIR at Meta with Universidad de Zaragoza.

### Figure 1 · PDF page 1 — a three-row, five-column qualitative comparison keeps each input and its two feature renderings in the same column

**Color roles.** feature colors: PCA-to-RGB data encoding; do not repurpose as an ornamental palette. [visual observation].

**Typography.** visible text metrics: OptimisticDisp-Bd 8.77 pt [measured in PDF]

**Composition, grouping, and routing.**

a three-row, five-column qualitative comparison keeps each input and its two feature renderings in the same column. Gutters are narrow and consistent; shared row labels sit outside the image matrix. The feature colors are PCA-to-RGB encodings, not a cosmetic palette, so recoloring them would change the visualization.

**Adaptation.** For detailed architectures combine repeated token strips with a limited vocabulary of explicit operators. Keep parallel encoders vertically aligned and place supervision/feedback in reserved margins. For qualitative grids use equal crops and a stated selection and color-transformation rule.

**Limitations and changes to make.** The architecture in Fig.4 is rasterized; its internal font cannot be established from PDF font resources. Fig.1 row labels are visibly embedded OptimisticDisp-Bd 8.77 pt, but this is a source observation, not a portable font recommendation.

### Figure 4 · PDF page 5 — two aligned encoder lanes use token chips, feature stacks, layer taps, and a predictor silhouette

**Color roles.** context token channel: #D9E8FB [sampled raster]; prediction channel: #FECCCB [sampled raster].

**Typography.** Exact visible font family and authoring point size were not recoverable.

**Composition, grouping, and routing.**

two aligned encoder lanes use token chips, feature stacks, layer taps, and a predictor silhouette. Neutral model blocks retain visual quietness; blue context and warm red prediction channels remain coherent from tokens to losses. Explicit plus and masking operators establish computational meaning. Dashed loss routes occupy separate bottom/right corridors.

**Adaptation.** For detailed architectures combine repeated token strips with a limited vocabulary of explicit operators. Keep parallel encoders vertically aligned and place supervision/feedback in reserved margins. For qualitative grids use equal crops and a stated selection and color-transformation rule.

**Limitations and changes to make.** The architecture in Fig.4 is rasterized; its internal font cannot be established from PDF font resources. Fig.1 row labels are visibly embedded OptimisticDisp-Bd 8.77 pt, but this is a source observation, not a portable font recommendation.

## Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities

**Source:** [v6 PDF](https://arxiv.org/pdf/2507.06261v6) · [arXiv record](https://arxiv.org/abs/2507.06261) · Google / Gemini Team.
**Date provenance:** inspected source version date: 2025-12-19.
**Affiliation evidence:** Google / Gemini Team.

### Figure 1 · PDF page 3 — a dense cost-performance comparison uses direct labels and a stronger outline around focal models; subdued reference labels, thin guides, and a compact upper-right key establish hierarchy

**Color roles.** sampled dark field shades: #303C4A / #344151 [sampled raster].

**Typography.** Exact visible font family and authoring point size were not recoverable.

**Composition, grouping, and routing.**

a dense cost-performance comparison uses direct labels and a stronger outline around focal models; subdued reference labels, thin guides, and a compact upper-right key establish hierarchy. The horizontal cost axis runs in reverse. The dark backdrop is effective on screen but demands a separate print evaluation; tiny model labels are a weakness. A connected frontier must not be imitated as evidence of feasible unmeasured interpolations.

**Adaptation.** Use equal small multiples for related tasks, with a shared visual grammar and explicit independent scales. Use strong local labels to identify focal points in a dense tradeoff plot, but redesign into a print-safe palette where necessary.

**Limitations and changes to make.** Fig.1 is rasterized, so font family and source point sizes are unknown. Fig.4 visible text is outlined; DejaVuSans4.39–5.36 pt is metadata in an invisible search layer. Directly measured line colors/strokes remain valid subject to compositing caveats.

### Figure 4 · PDF page 6 — three equal-sized small multiples share plot height, grid density, blue #217BFE traces and increasing token budgets

**Color roles.** shared result curve: #217BFE [measured in PDF]; outlined text: #262626 [measured in PDF].

**Typography.** invisible searchable overlay metrics: DejaVuSans 4.39 pt; DejaVuSans 4.87 pt; DejaVuSans 5.36 pt [searchable overlay only]

**Geometry and spacing.** Stroke widths: 0.244 pt (18 paths), 0.609 pt (3 paths) [measured in PDF].

**Composition, grouping, and routing.**

three equal-sized small multiples share plot height, grid density, blue #217BFE traces and increasing token budgets. The y ranges differ across tasks and should remain explicit. Matching geometry makes the rate-of-change patterns easy to scan, while the uniform style avoids assigning arbitrary colors to tasks.

**Adaptation.** Use equal small multiples for related tasks, with a shared visual grammar and explicit independent scales. Use strong local labels to identify focal points in a dense tradeoff plot, but redesign into a print-safe palette where necessary.

**Limitations and changes to make.** Fig.1 is rasterized, so font family and source point sizes are unknown. Fig.4 visible text is outlined; DejaVuSans4.39–5.36 pt is metadata in an invisible search layer. Directly measured line colors/strokes remain valid subject to compositing caveats.

## Automated Researchers Can Reliably Mitigate Alignment Failures

**Source:** [official-2026-08-28 PDF](https://www-cdn.anthropic.com/7b1c44894e980876479947dcdd40716278aeeffd/automated-alignment-researchers-august-2026.pdf) · [primary record](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures) · Anthropic / Anthropic Fellows Program with UC Berkeley.
**Date provenance:** inspected source version date: 2026-08-28.
**Affiliation evidence:** Anthropic / Anthropic Fellows Program with UC Berkeley.

### Figure 1 · PDF page 1 — a compact 2×2 evidence set contrasts warm peach #F8A27E with deep navy #0F3C5F and uses forest #30685C for a separate role

**Color roles.** warm comparison: #F8A27E [measured in PDF]; navy comparison: #0F3C5F [measured in PDF]; selection/proposal role: #30685C [measured in PDF]; neutral candidates: #9A9A9A [measured in PDF].

**Typography.** invisible searchable overlay metrics: TimesNewRomanPS-BoldMT 7.73 pt; TimesNewRomanPSMT 5.67 pt; TimesNewRomanPSMT 6.98 pt; TimesNewRomanPSMT 6.87 pt; TimesNewRomanPSMT 4.81 pt; TimesNewRomanPSMT 4.98 pt; TimesNewRomanPS-ItalicMT 6.87 pt; TimesNewRomanPS-BoldMT 6.44 pt; DejaVuSans 5.67 pt [searchable overlay only]

**Geometry and spacing.** Stroke widths: 0.6 pt (82 paths), 1.0 pt (16 paths), 1.5 pt (2 paths), 1.6 pt (1 paths) [measured in PDF].

**Composition, grouping, and routing.**

a compact 2×2 evidence set contrasts warm peach #F8A27E with deep navy #0F3C5F and uses forest #30685C for a separate role. A neutral cloud of proposals, hollow cross markers for filtered candidates, a best-so-far line and a starred endpoint encode selection transparently. Short italic better/safer cues help with differing metric directions. Typography is serif, demonstrating that scientific style need not always be sans.

**Adaptation.** Use a horizontal operation lane with a separate return corridor for iterative research systems. Express a real isolation boundary with a dashed enclosure; keep inputs above the lane. In empirical panels preserve rejected candidates visibly and distinguish the selected best-so-far path from all proposals.

**Limitations and changes to make.** Fig.1 uses outlined visible text plus an invisible TimesNewRoman searchable layer; those family/size records are provenance clues, not verified editable type. Dense legends are small in the source and should be enlarged in adaptation.

### Figure 2 · PDF page 4 — a compact left-to-right method cycle uses matching stage fills and outlines—blue agent, amber monitor, green train, violet evaluator, gray leaderboard

**Color roles.** agent fill/outline: #F1F4F7 / #35618E [measured in PDF]; monitor fill/outline: #F7EFE6 / #BE7A2E [measured in PDF]; training fill/outline: #EEF5F0 / #3F8E5B [measured in PDF]; evaluator fill/outline: #F3F0F7 / #7C5AA6 [measured in PDF]; leaderboard fill/outline: #F5F5F5 / #6F6F6F [measured in PDF]; isolation boundary: #B7A4CE [measured in PDF].

**Typography.** visible text metrics: NimbusRomNo9L-Regu 6.96 pt; NimbusRomNo9L-Regu 6.83 pt; NimbusRomNo9L-Medi 8.95 pt; CMR7 6.83 pt; CMSY7 6.83 pt [measured in PDF]

**Geometry and spacing.** Stroke widths: 0.975 pt (7 paths), 0.878 pt (5 paths), 0.683 pt (4 paths), 0.39 pt (4 paths), 0.633 pt (1 paths), 0.507 pt (1 paths) [measured in PDF].

**Composition, grouping, and routing.**

a compact left-to-right method cycle uses matching stage fills and outlines—blue agent, amber monitor, green train, violet evaluator, gray leaderboard. Supporting documents sit above the main lane. A dashed violet boundary marks held-out isolation, and a long lower return curve expresses iteration without crossing stage interiors. Bold NimbusRoman headings are 8.95 pt; details6.83–6.96 pt. Main connectors 0.975 pt, quiet borders as low as 0.390 pt.

**Adaptation.** Use a horizontal operation lane with a separate return corridor for iterative research systems. Express a real isolation boundary with a dashed enclosure; keep inputs above the lane. In empirical panels preserve rejected candidates visibly and distinguish the selected best-so-far path from all proposals.

**Limitations and changes to make.** Fig.1 uses outlined visible text plus an invisible TimesNewRoman searchable layer; those family/size records are provenance clues, not verified editable type. Dense legends are small in the source and should be enlarged in adaptation.

## Adaptation boundaries

Preserve the current paper’s data, method topology, experimental conditions, and captions. A warm-colored module is not evidence of a trainable component; a loop is not evidence of online learning; a selected trajectory is not a confidence interval. Use the source study to choose an appropriate visual grammar and to set a concrete style specification. Then measure and inspect the new export at its actual manuscript size.

Source PDFs and figure images are not bundled. Download the pinned primary source when a fresh inspection is needed. Use source artwork only under its actual reuse terms; an original figure should borrow principles rather than reproduce another paper’s artwork.
