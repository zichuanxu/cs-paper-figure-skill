# Recent DeepSeek, Tencent and Alibaba/Qwen figure study

**12 papers/reports; 27 inspected figure anchors; all first submitted in 2025–2026.**

Exact-version PDF pages were rendered and visually inspected. Palette measurements, font visibility, source-scale defects and recommendations are recorded separately. No source artwork should be bundled.

## Contents

- [mHC: Manifold-Constrained Hyper-Connections](#deepseek-mhc)
- [DeepSeek-OCR: Contexts Optical Compression](#deepseek-ocr)
- [DeepSeek-OCR 2: Visual Causal Flow](#deepseek-ocr2)
- [DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression](#deepseek-v41-flash)
- [HunyuanWorld 1.0: Generating Immersive, Explorable, and Interactive 3D Worlds from Words or Pixels](#hunyuanworld1)
- [HY-World 2.0: A Multi-Modal World Model for Reconstructing, Generating, and Simulating 3D Worlds](#hunyuanworld2)
- [Hunyuan3D 2.5: Towards High-Fidelity 3D Assets Generation with Ultimate Details](#hunyuan3d25)
- [WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling](#worldplay)
- [Qwen-Image Technical Report](#qwen-image)
- [Qwen3-VL Technical Report](#qwen3-vl)
- [Qwen3-TTS Technical Report](#qwen3-tts)
- [Qwen3.5-Omni Technical Report](#qwen35-omni)
- [Transferable recipes and rules](#transferable-recipes-and-rules)

## deepseek-mhc

**mHC: Manifold-Constrained Hyper-Connections** — DeepSeek, 2025; arXiv:2512.24880v1.
[Primary PDF](https://arxiv.org/pdf/2512.24880v1) · [Record](https://arxiv.org/abs/2512.24880v1)

PDF title page names DeepSeek-AI.

Counted as 2025 by original submission, 31 December 2025; a January 2026 revision exists but was not the inspected version.

### Figure 1 — Matched residual-connection variants (PDF p1)

**Family:** architecture comparison. **Selected region:** [70, 450, 526, 691] PDF pt, top-left origin.

**Layout and hierarchy.** Three parallel, bottom-to-top architecture panels share operation baselines and unchanged-layer geometry. The simpler residual panel is narrower; the two richer variants receive equal additional width. Gray stacked slabs depict widened states, cyan marks the common computation, and orange/green identify the changed mappings.

**Geometry.** Vector background widths are 116.60, 153.34, 153.34 pt; all heights 219.10 pt. Gutters are about 14.82 pt. Layer F rectangles share width about 58.14 pt and height about 15.87 pt, aligned at y=580.71 pt. Thus comparison alignment is preserved without forcing equal panel widths.

**Colors.**
- panel background: `#F2F2F2` (vector_measured). 
- unchanged compute: `#C1E5F5` (vector_measured). 
- unconstrained mappings: `#FBE3D6` (vector_measured). 
- constrained mappings: `#D9F2D0` (vector_measured). 
- new mapping outline: `#4EA72E` (vector_measured). 

**Typography.**
- ordinary labels: Ubuntu-Regular, 7.20 pt, regular (vector_measured).
- panel labels: Ubuntu-Regular, 8.66 pt, regular (vector_measured).
- math: CambriaMath, 7.20 pt, regular (vector_measured).

**Routes and boundaries.** Large, hollow gray arrows distinguish residual state transport from small operation transitions. The side branch enters an explicit addition junction. Repeated stack offsets are consistent; change locations are positionally matched between HC and mHC.

**Transfer.**
- Give unchanged operations identical size, position and style across variants; use accent changes only where the method changes.
- Allocate panel width to structural complexity while maintaining matched functional baselines.

**Cautions.**
- Do not copy state-stack multiplicity as a literal tensor dimension unless the count is specified.
- Subscripts fall to about 4.28–5.22 pt; simplify notation or enlarge the target figure instead of reproducing that small scale.

### Figure 4 — Three-lane communication/computation schedule (PDF p12)

**Family:** execution schedule. **Selected region:** [74, 87, 519, 144] PDF pt, top-left origin.

**Layout and hierarchy.** Three horizontal streams are aligned on a common reading direction. Long blocks encode major operations, while very narrow upright markers indicate added kernels. The lane labels remain outside the activity region, and arrowheads close every stream.

**Geometry.** Selected figure region is only 57 pt tall across 445 pt width, an unusually shallow strip. The measured main stroke is 0.451 pt; this compactness explains the very small typography.

**Colors.**
- main computation: `#A9D18E` (vector_measured). 
- communication: `#FFD966` (vector_measured). 
- weight computation: `#9DC3E6` (vector_measured). 
- recomputation: `#F4B183` (vector_measured). 

**Typography.**
- operation labels: Ubuntu-Regular, 4.92 pt, regular (vector_measured).
- lane labels: Ubuntu-Regular, 5.42 pt, regular (vector_measured).
- kernel math: CambriaMath, 3.94 pt, regular (vector_measured).

**Routes and boundaries.** Horizontal lane arrows provide the schedule spine. Small kernel blocks sit near the appropriate lane rather than being connected by a separate web of arrows.

**Transfer.**
- Use lane identity, color and alignment together to explain overlap; include a compact operation-key legend.
- Label a schedule SCHEMATIC when block lengths are illustrative: this source explicitly says lengths are not actual durations.

**Cautions.**
- Do not interpret block width as measured runtime.
- Do not scale a dense schedule down until 4–5 pt labels become the default; split overview and critical overlap detail.

## deepseek-ocr

**DeepSeek-OCR: Contexts Optical Compression** — DeepSeek, 2025; arXiv:2510.18234v1.
[Primary PDF](https://arxiv.org/pdf/2510.18234v1) · [Record](https://arxiv.org/abs/2510.18234v1)

PDF title page names DeepSeek-AI.

### Figure 1 — Compression and quality–token-cost comparison (PDF p1)

**Family:** paired quantitative plots. **Selected region:** [85, 493, 518, 687] PDF pt, top-left origin.

**Layout and hierarchy.** Two panels have comparable visual weight: the left combines paired bars and dashed ratio curves; the right compares token cost with error using distinct marker shapes, model labels, a broken horizontal axis, and two pale explanatory regions.

**Geometry.** The 433×194 pt crop includes both panels and panel captions. Most internal text is outlined; 956 invisible text traces are searchable metadata, not visible-font evidence.

**Colors.**
- 64-token series: `#B487D8` (visual_estimate). Approximate visible lavender bars; exact fill should be re-sampled for reuse.
- compression-ratio curve: `#6A4C93` (vector_measured). 
- 100-token ratio curve: `#0066CC` (vector_measured). 

**Typography.**
- panel captions: URWPalladioL-Roma, 8.97 pt, regular (vector_measured).
- plot labels: Exact visible family not established, size unverified, small sans-serif; precise visible font is unverified because the plotted text is outlined (visual_estimate).

**Routes and boundaries.** No conceptual flow arrows are needed. The legend distinguishes series on the left and encoder families on the right; marker shape adds redundancy to hue.

**Transfer.**
- Use a neighboring plot to separate a mechanism diagnostic from an external quality–cost comparison.
- Preserve the definition, direction and scale of both axes and visually mark any axis discontinuity.

**Cautions.**
- The dual y-axis and x-axis break require extra interpretive work; a new figure should use separate aligned panels if that improves comparison.
- Do not adopt the invisible DejaVuSans/LiberationSans overlay as proof of visible typography.

### Figure 3 — Optical compression encoder/decoder architecture (PDF p5)

**Family:** typed multimodal pipeline. **Selected region:** [72, 89, 520, 211] PDF pt, top-left origin.

**Layout and hierarchy.** A horizontal pipeline uses actual document patches, a tall perception block, a narrow compression block, a token column, a wide global encoder and a large decoder. Braces group tokenizer and embedding roles, so the design communicates both hierarchy and sequence.

**Geometry.** The composition is approximately 3.67:1 in its selected region. Different block aspect ratios encode stage roles rather than imposing a row of uniform cards.

**Colors.**
- perception encoder: `#EEEAF2` (vector_measured). 
- compression operation: `#FFF2CC` (vector_measured). 
- global encoder: `#DBEEF3` (vector_measured). 
- language decoder: `#FCEBDD` (vector_measured). 
- prompt: `#EBF1DF` (vector_measured). 
- connectors: `#BFBFBF` (vector_measured). 

**Typography.**
- large module names: ArialMT, 8.40 pt, regular (vector_measured).
- mechanism annotations: ArialMT, 6.30 pt, regular (vector_measured).
- small facts: ArialMT, 5.63 pt, regular (vector_measured).

**Routes and boundaries.** The main path moves left-to-right; prompt conditioning enters the decoder below. A light outer route connects encoder output around a projection junction. Dashed grouping and low-activation annotation have a different role from the solid data path.

**Transfer.**
- Use a real, small input/output specimen to make an abstract compression mechanism concrete.
- Show token-count changes at the operation responsible for them and use braces for role grouping.

**Cautions.**
- Very light gray connectors and labels should be darkened when reusing this grammar at small print size.
- The paper thumbnail is evidence of an input type; do not invent or reuse source content without permission.

### Figure 13 — Aligned memory, vision and text degradation analogy (PDF p19)

**Family:** conceptual spectrum. **Selected region:** [82, 88, 520, 230] PDF pt, top-left origin.

**Layout and hierarchy.** Three horizontal rows align six stages of decreasing clarity. A semantic icon labels each row; a long gray arrow gives the progression direction; dashed separators prevent one row being read as a second quantitative axis.

**Geometry.** Repeated circles are equally spaced for ordinal correspondence. The labels express time, viewing distance and model resolution, which do not share numerical units.

**Colors.**
- memory progression: `#CCC2D9` (vector_measured). 
- vision progression: `#92CDDC` (vector_measured). 
- text progression: `#FFD965` (vector_measured). 
- direction arrows: `#A5A5A5` (vector_measured). 

**Typography.**
- progression labels: ArialMT, 5.57 pt, regular (vector_measured).
- row/axis labels: ArialMT, 6.24 pt, regular (vector_measured).

**Routes and boundaries.** Each row has its own direction label; there are no cross-row causal arrows. Alignment expresses analogy, not an experimentally demonstrated causal relation.

**Transfer.**
- Use shared ordinal columns to compare conceptual progressions with different units.
- State SCHEMATIC or ANALOGY in the caption, and explain the row-specific direction.

**Cautions.**
- Do not turn equal stage spacing into a numerical scale or claim equivalent decay rates across rows.
- The pale 5.57 pt labels need darker ink and greater size in a new export.

## deepseek-ocr2

**DeepSeek-OCR 2: Visual Causal Flow** — DeepSeek, 2026; arXiv:2601.20552v1.
[Primary PDF](https://arxiv.org/pdf/2601.20552v1) · [Record](https://arxiv.org/abs/2601.20552v1)

PDF title page names DeepSeek-AI.

### Figure 3 — Causal visual encoder with token reordering (PDF p5)

**Family:** token architecture. **Selected region:** [72, 89, 520, 232] PDF pt, top-left origin.

**Layout and hierarchy.** The previous optical-compression grammar is retained, but the center expands into a pink encoder with a lower noncausal/causal input ribbon and an upper reordered output ribbon. A dashed red scope boundary marks the new encoder subsystem.

**Geometry.** The new central encoder is substantially wider than the perception/compression pair. Two token ribbons and braces expose sequence semantics instead of hiding them in a generic encoder rectangle.

**Colors.**
- perception stage: `#EEEAF2` (vector_measured). 
- compression: `#FFF2CC` (vector_measured). 
- new language-style vision encoder: `#F2DCDA` (vector_measured). 
- language decoder: `#FCEBDD` (vector_measured). 
- causal path accent: `#F59D56` (vector_measured). 

**Typography.**
- large encoder label: ArialMT, 9.83 pt, regular (vector_measured).
- encoder group label: ArialMT, 8.14 pt, regular (vector_measured).
- supporting facts: ArialMT, 6.57 pt, regular (vector_measured).

**Routes and boundaries.** Black arrows distinguish noncausal and causal token order. A separate orange dashed route labels the cascaded causal relationship. The prompt route remains below the primary path.

**Transfer.**
- Preserve the familiar baseline geometry, then expand only the new operation into a token-level explanation.
- Use boundary style, arrow style and token ordering to distinguish subsystem scope from information flow.

**Cautions.**
- A rainbow token sequence needs an explicit identity/ordering meaning; do not use colors merely as decoration.
- Do not infer the hidden dimension or actual number of example tokens from the drawn count.

### Figure 5 — Bidirectional plus causal attention mask (PDF p7)

**Family:** mechanism matrix. **Selected region:** [112, 86, 478, 238] PDF pt, top-left origin.

**Layout and hierarchy.** Two small 3×3 masks on the left combine into one 6×6 mask on the right. A plus sign and arrow express composition; a legend below the small matrices defines both cell colors and the additional white-circle self-attention symbol.

**Geometry.** Measured colored squares are about 11.22 pt on a roughly 21.33 pt vertical pitch, so whitespace helps readers count and compare cells. The full mask separates vision-token and causal-query columns with braces.

**Colors.**
- allowed attention: `#9DBB61` (vector_measured). 
- blocked attention: `#E5B9B5` (vector_measured). 
- self-attention marker: `#FFFFFF` (vector_measured). 
- cell edge: `#000000` (vector_measured). 

**Typography.**
- matrix labels and legend: ArialMT, 9.50 pt, regular (vector_measured).
- composition plus sign: ArialMT, 22.28 pt, regular (vector_measured).

**Routes and boundaries.** The only flow arrow is the left-to-right composition arrow. The mask itself shows relationships without drawing 36 separate arrows.

**Transfer.**
- For dense relation structure, use a matrix with a typed legend instead of an edge forest.
- Use a shape overlay for self-attention so this third category is readable independently of color.

**Cautions.**
- The source labels are pale gray despite comfortable point size; use stronger foreground contrast.
- Preserve row/column semantics and triangular direction exactly; a flipped mask changes the method.

## deepseek-v41-flash

**DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression** — DeepSeek, 2026; arXiv:2609.19969v1.
[Primary PDF](https://arxiv.org/pdf/2609.19969v1) · [Record](https://arxiv.org/abs/2609.19969v1)

PDF title page names DeepSeek-AI.

### Figure 1 — Benchmark bars plus historical KV-cache reduction (PDF p1)

**Family:** paired performance/resource plots. **Selected region:** [80, 510, 523, 675] PDF pt, top-left origin.

**Layout and hierarchy.** The left panel compares benchmark groups using tightly clustered bars and direct value labels; the right aligns model generations vertically and annotates successive cache-size reductions with curved ratio callouts. A saturated blue-purple focus is shared across both panels.

**Geometry.** Chart interiors are embedded raster graphics, so their visible font families and line widths cannot be established from PDF text objects. Palette samples are rendered RGB values, not native design tokens.

**Colors.**
- focus model: `#546AF5` (raster_sampled). 
- related comparator: `#9BA9FA` (raster_sampled). 
- secondary comparator: `#B8C3FC` (raster_sampled). 
- other comparators: `#C5C5C5` (visual_estimate). 

**Typography.**
- chart text: Exact visible family not established, size unverified, compact sans-serif, with bold focus labels (visual_estimate).
- panel letters: URWPalladioL-Bold, 7.97 pt, bold (vector_measured).

**Routes and boundaries.** Curved arrows on the resource panel connect successive generations and carry explicit reduction ratios. The focus model is named in the same accent as the benchmark bars.

**Transfer.**
- Reuse a single focus color across evidence panels to bind quality and cost claims.
- Directly label exact values when a very small bar would otherwise disappear on a linear resource scale.

**Cautions.**
- Do not use historical reduction arrows without checking the denominators and units.
- The dense five-model legend and many tiny value labels should be simplified for a narrow figure.

### Figure 3 — Causal encoder/decoder with explicit reuse paths (PDF p7)

**Family:** nested architecture. **Selected region:** [70, 84, 526, 319] PDF pt, top-left origin.

**Layout and hierarchy.** Two tall, light-background containers separate causal encoder and decoder. Dotted subgroups show repeated blocks; stack glyphs mark hidden states and embeddings. The different attention modes retain their color roles across the figure.

**Geometry.** The selected 456×235 pt region contains approximately equal encoder/decoder widths plus external input and state regions. Source text is around 6 pt, making it a grammar example rather than a safe minimum-size template.

**Colors.**
- neutral modules: `#FAF9F5` (vector_measured). 
- full computation: `#D9F2D0` (vector_measured). 
- reuse mode: `#FDF6C7` (vector_measured). 
- reindex mode: `#CAEEFB` (vector_measured). 
- sliding attention: `#FDE2D2` (vector_measured). 
- route/ink: `#404040` (vector_measured). 

**Typography.**
- module labels: Ubuntu-Regular, 5.98 pt, regular (vector_measured).
- group headings: Ubuntu-Bold, 5.98 pt, bold (vector_measured).
- operation annotations: Ubuntu-Italic, 5.98 pt, italic (vector_measured).

**Routes and boundaries.** Reuse connections reserve outer corridors around repeated-layer groups. A central cross-container transfer is labeled, and the sparse-index candidate pool is explicitly drawn outside the decoder boundary.

**Transfer.**
- Distinguish repeated scope from forward dataflow with dotted containers and ordinary arrows.
- Place reused state in a named external object and route its incoming/outgoing edges around the main stack.

**Cautions.**
- Do not copy a long route through another group simply because the source does; recheck each crossing in the new topology.
- Use larger text or fewer repeated layer boxes for the same physical width.

### Figure 4 — Full, reindex and reuse operating modes (PDF p10)

**Family:** matched computational modes. **Selected region:** [70, 84, 526, 230] PDF pt, top-left origin.

**Layout and hierarchy.** Three equally sized mode cards repeat the shared attention path in the same positions. Colored input cards indicate what is computed or reused. The mode title sits at the upper right of each panel; recycled inputs remain below the main group.

**Geometry.** Fine measured module outlines are about 0.502 pt. Text is only 4.67 pt within a 456×146 pt source crop, so the useful lesson is positional comparison rather than copying the density.

**Colors.**
- neutral shared computation: `#FAF9F5` (vector_measured). 
- computed in current layer: `#D9F2D0` (vector_measured). 
- reused KV/K: `#FDF6C7` (vector_measured). 
- reused indices: `#FBE3D6` (vector_measured). 
- stroke and ink: `#404040` (vector_measured). 

**Typography.**
- module labels: Ubuntu-Regular, 4.67 pt, regular (vector_measured).
- variables: Ubuntu-Italic, 4.67 pt, italic (vector_measured).
- mode headings: Ubuntu-Bold, 6.06 pt, bold (vector_measured).

**Routes and boundaries.** Vertical local dependencies are kept inside each card; reused inputs enter from below. Identical route geometry makes missing or substituted branches easy to spot.

**Transfer.**
- Keep shared topology fixed across algorithmic modes and encode only state provenance with color.
- Explain color semantics with an explicit computed/reused legend, not merely a model-name legend.

**Cautions.**
- Do not reuse the same green for an unrelated performance-success meaning within the same figure set.
- Increase the readable type scale and reduce labels before placing three dense modes in one column.

## hunyuanworld1

**HunyuanWorld 1.0: Generating Immersive, Explorable, and Interactive 3D Worlds from Words or Pixels** — Tencent, 2025; arXiv:2507.21809v1.
[Primary PDF](https://arxiv.org/pdf/2507.21809v1) · [Record](https://arxiv.org/abs/2507.21809v1)

PDF title page names Tencent Hunyuan.

### Figure 2 — Three-stage world-generation overview (PDF p5)

**Family:** multimodal overview with agent trace. **Selected region:** [108, 72, 505, 391] PDF pt, top-left origin.

**Layout and hierarchy.** Three narrow columns carry world-proxy generation, agentic decomposition and reconstruction. Horizontal rules organize column headings. Real example images make each transformation tangible; the middle column shows a miniature multi-step agent exchange with successive scene layers.

**Geometry.** The source composition is portrait-like for an architecture overview: approximately 397×319 pt. The agent trace contains hundreds of characters at 3.64 pt and is an explicit example of excessive detail at manuscript scale.

**Colors.**
- neutral model scope: `#F1F1F1` (vector_measured). 
- model blocks: `#D9D9D9` (vector_measured). 
- image-text/token accent: `#D7E0F9` (vector_measured). 
- conditioning/data accent: `#FBE3D6` (vector_measured). 
- projection/warping accent: `#D1BFBB` (vector_measured). 

**Typography.**
- stage titles: Candara-Bold, 5.98 pt, bold (vector_measured).
- ordinary labels: Candara, 5.98 pt, regular (vector_measured).
- agent trace: Consolas, 3.64 pt, regular (vector_measured).
- agent prose: BookAntiqua, 3.64 pt, regular (vector_measured).

**Routes and boundaries.** Within-stage flow runs downward. The left column separates image and prompt conditioning before convergence; reconstruction separates patch processing from layer-wise depth and world outputs.

**Transfer.**
- Pair symbolic operations with the same representative example as it changes through the pipeline.
- Keep the stage heading baseline and output baseline aligned even when the middle stage is a trace rather than a model stack.

**Cautions.**
- Replace a tiny full transcript with selected, legible state/action snippets; move complete traces to an inset or appendix.
- Do not copy subtle image shadows or decorative cards unless they help separate actual evidence from operators.

### Figure 3 — Typed data acquisition, filtering and annotation (PDF p6)

**Family:** data curation pipeline. **Selected region:** [108, 72, 505, 246] PDF pt, top-left origin.

**Layout and hierarchy.** Three horizontal bands differentiate acquired datasets, automated filters, and human annotation. The top uses three cylinders, the middle four rounded cards, and the bottom one wide annotation card; narrow left labels identify stage role.

**Geometry.** Dataset glyphs are about 119×22.5 pt; filter cards are about 72–81×44.5 pt; human annotation occupies roughly 354×50.7 pt. Stage boundaries use dark dash-dot lines; body text is larger than the previous overview trace.

**Colors.**
- dataset cylinders: `#C0D6F1` (vector_measured). 
- dataset outlines: `#6C9DD7` (vector_measured). 
- automated filters: `#FDF3CD` (vector_measured). 
- filter outlines: `#82631A` (vector_measured). 
- human annotation: `#FAE5D6` (vector_measured). 
- annotation outline: `#CE7133` (vector_measured). 

**Typography.**
- body bullet labels: ArialMT, 7.41 pt, regular (vector_measured).
- main category headings: Arial-BoldMT, 8.63 pt, bold (vector_measured).
- some labels: DengXian-Regular, 7.41 pt, regular (vector_measured).

**Routes and boundaries.** The figure relies on aligned bands and stage labels, avoiding unnecessary arrows among independent filters. Containers express categorization rather than a fully specified computational dependency graph.

**Transfer.**
- Use shape vocabulary to separate datasets, automatic operations and human review.
- Use a wide card for parallel human criteria instead of repeating identical mini-cards.

**Cautions.**
- Do not invent sequential dependencies from the left-to-right order of filters.
- Avoid vertical stage labels when they become difficult to read; horizontal side labels can preserve the same grouping.

## hunyuanworld2

**HY-World 2.0: A Multi-Modal World Model for Reconstructing, Generating, and Simulating 3D Worlds** — Tencent, 2026; arXiv:2604.14268v1.
[Primary PDF](https://arxiv.org/pdf/2604.14268v1) · [Record](https://arxiv.org/abs/2604.14268v1)

PDF title page names Tencent Hunyuan.

### Figure 2 — Four aligned multimodal world-generation stages (PDF p5)

**Family:** staged architecture storyboard. **Selected region:** [108, 72, 505, 271] PDF pt, top-left origin.

**Layout and hierarchy.** Four tall rounded stage cards carry two meaningful operations and an output specimen each. Colored stage names sit directly below; dark-blue model-name strips form a second aligned baseline. Raster scene images, simple semantic icons and trajectory sketches provide different kinds of evidence within the same grid.

**Geometry.** Measured stage cards are 86.67×163.76 pt with 15.68 pt gaps. The gap is about 18% of card width, enough to reserve the inter-stage route. Corners, padding and nested operation shapes are visually consistent. Main nested outlines are about 0.944 pt and thinner lines about 0.630 pt.

**Colors.**
- stage 1 background: `#DDEBF7` (vector_measured). 
- stage 2 background: `#DFEDDA` (vector_measured). 
- stage 3 background: `#FCE6C6` (vector_measured). 
- stage 4 background: `#F6DAF1` (vector_measured). 
- stage 1 outline/route: `#215F9A` (vector_measured). 
- stage 2 outline/route: `#3B7D23` (vector_measured). 
- stage 3 outline/route: `#E97132` (vector_measured). 
- stage 4 outline/route: `#7030A0` (vector_measured). 
- model-name footer: `#002060`, alpha 0.749 (vector_measured). Semi-transparent blue over white; do not use the raw dark blue as its observed opaque appearance.

**Typography.**
- stage titles: AptosDisplay-Bold, 11.33 pt, bold (vector_measured).
- stage names: Aptos-Bold, 8.81 pt, bold (vector_measured).
- model-name footer: Aptos-Bold, 10.07 pt, bold (vector_measured).
- module labels: Aptos, 7.55 pt, regular (vector_measured).

**Routes and boundaries.** Within-stage arrows descend. Thick stage-colored orthogonal routes rise through the open gutters to the next stage input. The route from a stage carries that stage color, so provenance stays visible across transitions.

**Transfer.**
- Reserve connector corridors before placing stage cards.
- Let each stage show the actual operation, a meaningful mini-example and a named output; consistent cards need not have identical internal content.

**Cautions.**
- Use semantic stage labels rather than copying generic stage numbering alone.
- Do not add colorful icons without identifying the corresponding scientific operation.

### Figure 7 — Main diffusion and camera-control branches (PDF p10)

**Family:** parallel branches with memory. **Selected region:** [108, 72, 505, 189] PDF pt, top-left origin.

**Layout and hierarchy.** Two similarly sized branch panels juxtapose the main diffusion route with camera-derived guidance. Real thumbnails occupy the top rows; the model operation and memory bank occupy lower rows. Each branch has a light tint and dashed scope border.

**Geometry.** A wide but very shallow selected region of 397×117 pt makes the thumbnails and 4.4–6.7 pt labels dense. Measured principal outlines are about 0.842 pt. The fills are translucent; their alpha is part of the observation.

**Colors.**
- main branch tint: `#C2F1C8`, alpha 0.502 (vector_measured). 
- camera branch tint: `#FBE3D6`, alpha 0.502 (vector_measured). 
- memory tint: `#C1E5F5`, alpha 0.502 (vector_measured). 
- main branch ink: `#196B24` (vector_measured). 
- camera branch ink: `#C04F15` (vector_measured). 
- memory ink: `#215F9A` (vector_measured). 

**Typography.**
- module headings: TimesNewRomanPS-BoldMT, 6.70 pt, bold (vector_measured).
- small labels: TimesNewRomanPSMT, 5.05 pt, regular (vector_measured).
- smallest ordinary labels: TimesNewRomanPSMT, 4.41 pt, regular (vector_measured).

**Routes and boundaries.** Output views feed back to a named memory bank along a lower route; the camera adapter connects into the diffusion branch at its boundary. These separate corridors help distinguish reuse from conditioning.

**Transfer.**
- Use parallel branches when two evidence sources converge into one computation, with an explicit convergence port.
- Label memory as a persistent state object and distinguish its update route from retrieval.

**Cautions.**
- Do not copy the thumbnail density into a narrow panel.
- Retain fill opacity when borrowing color; raw RGB alone produces an over-saturated result.

## hunyuan3d25

**Hunyuan3D 2.5: Towards High-Fidelity 3D Assets Generation with Ultimate Details** — Tencent, 2025; arXiv:2506.16504v1.
[Primary PDF](https://arxiv.org/pdf/2506.16504v1) · [Record](https://arxiv.org/abs/2506.16504v1)

PDF title page names Tencent Hunyuan.

### Figure 3 — Dark artifact panels with warm processing bars (PDF p3)

**Family:** visual asset pipeline. **Selected region:** [85, 86, 510, 205] PDF pt, top-left origin.

**Layout and hierarchy.** A warm beige strip alternates wide, dark artifact/model panels with narrow golden processing bars. The same object appears as input, shape, texture and final mesh. Stacked input cards imply multiple views; the illustrated object makes the processing sequence understandable without lengthy prose.

**Geometry.** The background strip measures 424.05×105.87 pt. Main generation cards are about 66×80.3 pt; processing bars about 29–30×80.3 pt. Thus width differentiates substantive artifacts from compact transformations.

**Colors.**
- canvas strip: `#F4ECE1` (vector_measured). 
- artifact panels and arrows: `#1E3337` (vector_measured). 
- processing bars / selected labels: `#EACE9E` (vector_measured). 

**Typography.**
- pipeline labels: CenturyGothic-Bold, 9.02 pt, bold (vector_measured).
- pipeline title: CenturyGothic-Bold, 10.02 pt, bold (vector_measured).

**Routes and boundaries.** Short, thick dark arrows connect adjacent stages on a single centerline. The pipeline reads left-to-right without any crossings.

**Transfer.**
- Use dark panels when they improve visibility of rendered assets, while keeping the surrounding document light.
- Alternate evidence-bearing artifact panels and narrow transformation nodes to avoid a uniform box chain.

**Cautions.**
- Vertical processing text is a tradeoff; rotate the whole layout or use short horizontal labels if more text is required.
- Do not reuse the illustrated source asset as decoration or imply it is output from a new method.

### Figure 5 — Pipeline plus expanded multi-task attention block (PDF p4)

**Family:** overview plus mechanism detail. **Selected region:** [88, 86, 509, 314] PDF pt, top-left origin.

**Layout and hierarchy.** The left half shows a two-branch training/inference pipeline with input, material maps and output tiles; the right half expands the central attention operation into generation and reference blocks. Pale backgrounds separate the two scopes without enclosing every small object.

**Geometry.** Nearly equal overview/detail halves occupy 421×228 pt. Major outlines around 0.923 pt are stronger than secondary lines around 0.308–0.462 pt. Token/value miniatures reveal the operation more precisely than a generic attention box.

**Colors.**
- reference branch: `#DCEAF7` (vector_measured). 
- generation branch: `#D9F2D0` (vector_measured). 
- convolution / value blocks: `#F6C6AD` (vector_measured). 
- self-attention: `#D6EAED` (vector_measured). 
- multi-view attention: `#FFE79A` (vector_measured). 
- residual block: `#A99DCB` (vector_measured). 
- routes / body ink: `#747474` (vector_measured). 

**Typography.**
- figure heading: CenturyGothic-Bold, 11.01 pt, bold (vector_measured).
- panel headings: CenturyGothic-Bold, 8.59 pt, bold (vector_measured).
- module labels: CenturyGothic, 6.71 pt, regular (vector_measured).
- small facts: CenturyGothic, 5.50 pt, regular (vector_measured).

**Routes and boundaries.** The left shows vertical conditioning into the generation branch; the right uses explicit Q/K/V connections and addition junctions. Freeze/train icons distinguish parameter status, but need a legend in any new figure.

**Transfer.**
- Give the reader one complete overview and one expanded operation, using different levels of detail intentionally.
- Use source-matched colors to identify the same branch or operator across panels.

**Cautions.**
- Do not let a fire/snowflake symbol be the sole explanation of trainable/frozen status.
- Tiny lower captions and numerous material tiles should be reduced or moved to supplementary detail.

## worldplay

**WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling** — Tencent, 2025; arXiv:2512.14614v1.
[Primary PDF](https://arxiv.org/pdf/2512.14614v1) · [Record](https://arxiv.org/abs/2512.14614v1)

PDF title page explicitly maps affiliation 3 to Tencent Hunyuan and affiliations 1/2 to HKUST/Beihang.

### Figure 2 — Autoregressive world model above a persistent memory timeline (PDF p4)

**Family:** streaming memory architecture. **Selected region:** [58, 70, 554, 268] PDF pt, top-left origin.

**Layout and hierarchy.** A long shared model bar spans two repeated temporal chunks. Each chunk contains an encoder, memory-selected examples, user-action conditioning and a decoder. A memory-cache ribbon anchors the full bottom edge, making persistence explicit across repeated calls.

**Geometry.** The source is an embedded raster in a 496×198 pt crop. Exact native font metrics and stroke widths are unavailable. Color samples describe the rendered image, not a verified source palette file.

**Colors.**
- shared model spine: `#5480AD` (raster_sampled). 
- user-control cards: `#DFE9F5` (raster_sampled). 
- memory and reconstitution: `#C25759` (raster_sampled). Rendered accent sample; JPEG-like edge variation is present.

**Typography.**
- diagram labels: Exact visible family not established, size unverified, sans-serif with bold white model-spine heading (visual_estimate).

**Routes and boundaries.** Blue update routes return decoded chunks to the bottom memory ribbon; red reconstitution routes retrieve selected past views. The two edge roles occupy distinct vertical channels, rather than sharing an ambiguous bidirectional arrow.

**Transfer.**
- Separate the current computation, persistent state and chronological history in space.
- Give read and write paths distinct names and routes, even if they share the same memory object.

**Cautions.**
- Do not use a long model bar to imply a single simultaneous call if the actual method executes sequential chunks.
- Repeated thumbnails are meaningful evidence; limit them to representative, explained samples in a new schematic.

### Figure 4 — Three matched memory-index matrices (PDF p5)

**Family:** aligned relation matrices. **Selected region:** [58, 70, 294, 171] PDF pt, top-left origin.

**Layout and hierarchy.** Three identically sized lower-triangular matrices compare full context, absolute indexing and relative indexing. Blue diagonal cells mark the current chunk; red historical cells carry explicit temporal indices. White unused cells expose sparsity.

**Geometry.** Each matrix is a separate raster, while the panel captions are visible PDF text. The shared 9×9 example geometry supports direct cell-by-cell comparison.

**Colors.**
- memory chunks: `#DB8D8C` (raster_sampled). 
- current chunk: `#88A5C6` (raster_sampled). 

**Typography.**
- matrix indices: Exact visible family not established, size unverified, small white sans-serif numerals (visual_estimate).
- panel captions: NimbusRomNo9L-Regu, 7.97 pt, regular (vector_measured).

**Routes and boundaries.** Matrix adjacency replaces many temporal arrows. Differences are concentrated in selected cells and their numeric indices, not in a rearranged layout.

**Transfer.**
- Keep matrix shape, row ordering and indexing conventions identical across ablations.
- Use an explicit current-state marker plus text indices so meaning survives color loss.

**Cautions.**
- Do not confuse blank cells with zero values: define unavailable/not-attended states.
- For smaller print size, use a smaller representative matrix with larger labels rather than retaining all cells.

### Figure 5 — Memory-aware student, teacher and score branches (PDF p5)

**Family:** training/distillation diagram. **Selected region:** [317, 70, 554, 167] PDF pt, top-left origin.

**Layout and hierarchy.** The memory cache sits on the left, the student in the center, and two vertically aligned scoring branches on the right. Token stacks between modules expose the data handoff; trainable/frozen icons sit near their corresponding branches.

**Geometry.** The source is one raster occupying a narrow 237×97 pt crop, so precise type and stroke measurements are unavailable. The mechanism is clear when enlarged but dense at paper size.

**Colors.**
- student autoregressive model: `#5380AC` (raster_sampled). 
- teacher model: `#80A0C2` (raster_sampled). 
- trainable score branch: `#D18283` (raster_sampled). 

**Typography.**
- module and loss labels: Exact visible family not established, size unverified, sans-serif with white centered model labels (visual_estimate).

**Routes and boundaries.** The cache has separately labeled retrieve/update directions. The student sends a shared condition to both score branches; a subtraction node combines their outputs before the loss label.

**Transfer.**
- Use a shared alignment axis for teacher and comparator branches and explicitly draw the merge operator.
- Keep data retrieval, parameter-update status and objective computation as separate visual roles.

**Cautions.**
- Do not infer that a frozen icon means a module is absent at inference; phase membership needs its own statement.
- Avoid sending the training-loss edge back through the same corridor as a memory read path.

## qwen-image

**Qwen-Image Technical Report** — Alibaba / Qwen, 2025; arXiv:2508.02324v1.
[Primary PDF](https://arxiv.org/pdf/2508.02324v1) · [Record](https://arxiv.org/abs/2508.02324v1)

PDF title page names Qwen Team and links the Qwen repositories; official Qwen3-VL repository About text identifies Qwen team, Alibaba Cloud (https://github.com/QwenLM/Qwen3-VL).

### Figure 6 — Double-stream diffusion overview and expanded block (PDF p7)

**Family:** overview plus mechanism detail. **Selected region:** [70, 70, 526, 333] PDF pt, top-left origin.

**Layout and hierarchy.** The left half provides a full text/image/noise overview; dashed zoom boundaries expand one repeated MMDiT block into the right half. The expanded block keeps text and image streams in parallel blue/purple lanes and shows the exact attention/normalization/gating sequence.

**Geometry.** Selected crop [70,70,526,333] on PDF p7. Vector text and colors are extractable, but eight raw drawing widths of 15875/22225/25400 are implausible transform metadata and MUST NOT be published as point thickness. Rendered line thickness requires a separate trusted measurement.

**Colors.**
- trainable blocks as rendered: `#FFCCCC` (raster_sampled). Native red fill #FF0000 at alpha≈0.196–0.2; the visible result is pale pink.
- frozen encoders as rendered: `#CDEFFC` (raster_sampled). Native cyan #00B0F0 at alpha≈0.196–0.2.
- text-stream routes: `#4472C4` (vector_measured). 
- image-stream routes: `#7131A1` (vector_measured). 
- text example card: `#FAECDC` (vector_measured). 

**Typography.**
- large module headings: TimesNewRomanPS-BoldMT, 12.22 pt, bold (vector_measured).
- detail labels: TimesNewRomanPSMT, 6.72 pt, regular (vector_measured).
- math: CambriaMath, 7.32 pt, regular (vector_measured).

**Routes and boundaries.** Colored residual routes stay on the outer edges of their lanes. Thin gray modulation routes connect to both streams; dashed black expansion boundaries have no arrowheads and must not be mistaken for dataflow.

**Transfer.**
- Use explicit overview-to-detail expansion and keep corresponding stream colors unchanged in both levels.
- Keep dataflow, residual connections, conditioning and visual zoom boundaries distinguishable by role.

**Cautions.**
- Never use raw saturated red/cyan as the observed pastel fill without retaining opacity or sampling the composite.
- Reject physically implausible extracted line widths; do not let malformed widths contaminate crop selection.

### Figure 10 — Seven-stage curation with split and rejected flows (PDF p11)

**Family:** data curation flow / Sankey. **Selected region:** [70, 70, 526, 322] PDF pt, top-left origin.

**Layout and hierarchy.** Seven colored vertical stages progress across the page while gray reject streams peel downward. Central branching and recombination expose data categories, caption paths and later specialization. Color follows stage position rather than a single persistent dataset identity.

**Geometry.** The entire figure is rasterized. Ribbon width is a quantitative-looking encoding, but this design study has not verified the flow quantities underlying the widths. The graphic should not be treated as a source of dataset counts.

**Colors.**
- stage 1 flow: `#F7AFAF` (raster_sampled). 
- stage 2 flow: `#F6CC9D` (raster_sampled). 
- stage 3 flow: `#FCF6B4` (raster_sampled). 
- stage 4 flow: `#9AFB86` (raster_sampled). 
- stage 5 flow: `#8CEEF2` (raster_sampled). 
- stage 6 flow: `#A0C1F9` (raster_sampled). 
- stage 7 flow: `#BD9DF8` (raster_sampled). 

**Typography.**
- flow labels: Exact visible family not established, size unverified, very small sans-serif; precise family is unverified (visual_estimate).

**Routes and boundaries.** Thick curved ribbons carry retained flows; thinner gray ribbons carry filtering outcomes. Crossings in the middle are readable only when enlarged; tiny endpoint labels are a weak point.

**Transfer.**
- Show data lost to each filter instead of depicting curation as cost-free serial boxes.
- Use Sankey widths only when verified quantities and conservation rules exist; otherwise choose explicit stage/branch cards.

**Cautions.**
- Do not infer numeric retention rates from pixel widths.
- Avoid a rainbow palette with dozens of unreadable labels when a smaller stage graph communicates the same causal story.

## qwen3-vl

**Qwen3-VL Technical Report** — Alibaba / Qwen, 2025; arXiv:2511.21631v1.
[Primary PDF](https://arxiv.org/pdf/2511.21631v1) · [Record](https://arxiv.org/abs/2511.21631v1)

PDF title page names Qwen Team and links the Qwen repositories; official Qwen3-VL repository About text identifies Qwen team, Alibaba Cloud (https://github.com/QwenLM/Qwen3-VL).

### Figure 1 — Variable-resolution examples and multimodal token sequence (PDF p3)

**Family:** tokenization architecture. **Selected region:** [70, 70, 526, 335] PDF pt, top-left origin.

**Layout and hierarchy.** Different-sized picture examples and a stacked video clip occupy the lower half. Their dimensions and token counts are shown explicitly before all inputs converge into a long color-coded token ribbon. A small side inset exposes multi-layer feature injection.

**Geometry.** The architecture is embedded as one raster, so exact visible font family, point size and native strokes are not recoverable from PDF text. The chosen examples deliberately differ in shape and scale to illustrate variable resolution.

**Colors.**
- large model/encoder fill: `#F4DDBE` (raster_sampled). 
- text tokens: `#C6C7F5` (raster_sampled). 
- picture tokens: `#F5BCB5` (raster_sampled). 
- video tokens: `#A1DEDF` (raster_sampled). 
- main lettering: `#5851D5` (raster_sampled). 

**Typography.**
- architecture labels: Exact visible family not established, size unverified, mostly italic sans-serif large module labels; small serif-like dimensional annotations (visual_estimate).

**Routes and boundaries.** Vertical arrows carry examples into the vision encoder. Brackets partition the token ribbon by input item, and a dashed side scope separates the DeepStack detail from the main decoder.

**Transfer.**
- Use input examples with different aspect ratios when variable-resolution processing is the claim.
- Show a token ribbon with explicit group boundaries and a small inset for cross-layer integration.

**Cautions.**
- Do not use a logo as the focal point of a scientific mechanism.
- Replace tiny token-count and dimensional annotations with fewer readable representative examples when downsizing.

### Figure 3 — Shared-scale within-range and extrapolation heatmap (PDF p25)

**Family:** faceted heatmap. **Selected region:** [70, 70, 526, 231] PDF pt, top-left origin.

**Layout and hierarchy.** Two contiguous heatmap panels separate within-training context from extrapolated context. They share the depth rows and one color scale; a small white gutter and separate headings communicate the experimental boundary.

**Geometry.** Colored cells and borders are vector objects (white strokes about 0.448 pt), but the plot lettering is outlined with 258 invisible text traces. Search-overlay DejaVuSans names are not proof of visible fonts.

**Colors.**
- near-perfect score cells: `#9AD5B3` (vector_measured). 
- slightly lower score cells: `#A2D2A8` (vector_measured). 
- cell boundaries: `#FFFFFF` (vector_measured). 

**Typography.**
- heatmap labels: Exact visible family not established, size unverified, bold sans-serif headings and smaller sans-serif tick labels; exact visible family unverified (visual_estimate).

**Routes and boundaries.** No arrows are required. Column ordering expresses increasing context duration; row ordering expresses needle depth. Panel boundaries encode a change in test regime rather than a change in color scale.

**Transfer.**
- Use a common scale when comparing in-distribution and extrapolation performance.
- Make regime boundaries explicit with a gutter and headings instead of changing palettes.

**Cautions.**
- Near-saturated cells can conceal small errors; add a labeled error inset or exact cell values when those differences matter.
- Do not label a dimension as percent in prose while showing an unqualified 0–1 colorbar; declare units consistently in the new figure.

## qwen3-tts

**Qwen3-TTS Technical Report** — Alibaba / Qwen, 2026; arXiv:2601.15621v1.
[Primary PDF](https://arxiv.org/pdf/2601.15621v1) · [Record](https://arxiv.org/abs/2601.15621v1)

PDF title page names Qwen Team and links the Qwen repositories; official Qwen3-VL repository About text identifies Qwen team, Alibaba Cloud (https://github.com/QwenLM/Qwen3-VL).

### Figure 2 — Parallel speech-tokenizer designs with phase-specific edges (PDF p3)

**Family:** matched encoder/decoder pipelines. **Selected region:** [70, 70, 526, 304] PDF pt, top-left origin.

**Layout and hierarchy.** Two vertical codec diagrams stand on either side of a dashed divider. Both begin with waveform input and expose intermediate code tokens; the left includes a semantic auxiliary branch while the right displays quantizers and a reconstructed waveform.

**Geometry.** One embedded raster covers both diagrams. Equal visual widths and aligned waveform baselines help compare their different internal structures; exact native type and stroke widths are unavailable.

**Colors.**
- audio encoder: `#F3DCD0` (raster_sampled). 
- vector quantizer: `#B4C7E7` (raster_sampled). 
- code tokens: `#FFC000` (raster_sampled). 
- ordinary outlines: `#172C51` (raster_sampled). 
- headings: `#5A44CA` (raster_sampled). 

**Typography.**
- module labels: Exact visible family not established, size unverified, italic purple sans-serif labels, darker bold panel captions (visual_estimate).

**Routes and boundaries.** A local legend defines dotted paths as training-only and solid paths as training-plus-inference. Auxiliary objectives route around the outer margins, away from the central encoder/decoder spine.

**Transfer.**
- Define training-only edge style locally and use it consistently for auxiliary objectives.
- Keep input/output baselines aligned when comparing different codec designs.

**Cautions.**
- Do not use dashed lines for both optionality and training-only status without distinguishing or explaining those meanings.
- A purple italic label is an observed choice, not a mandatory Qwen font rule.

### Figure 3 — Dual-track token input and multi-token speech generation (PDF p4)

**Family:** streaming token architecture. **Selected region:** [70, 164, 526, 415] PDF pt, top-left origin.

**Layout and hierarchy.** A long neutral language-model bar sits above two aligned input token tracks. The upper-right generation block expands zero-th and residual codebooks into vertical token stacks before waveform decoding. A left legend explains six distinct token/embedding categories.

**Geometry.** The overview is raster. The example uses many small repeated tokens, plus a large central logo that consumes space without explaining mechanism. A new layout can reallocate that area to larger semantic labels.

**Colors.**
- text tokens: `#C5C8F2` (raster_sampled). 
- text padding: `#FDFEC1` (raster_sampled). 
- think tokens: `#A8E8E2` (raster_sampled). 
- code tokens: `#D3E590` (raster_sampled). 
- code embeddings: `#E9B089` (raster_sampled). 
- heading accent: `#5A44CA` (raster_sampled). 

**Typography.**
- module labels and token legend: Exact visible family not established, size unverified, large italic purple labels; compact dark legend text (visual_estimate).

**Routes and boundaries.** Solid upward paths show generated codes entering the streaming decoder. Dashed outlines indicate optional elements, a different semantic use from the training-only dashed routes in Figure 2.

**Transfer.**
- Give each token type a stable fill and an explicit legend, and show alignment across parallel tracks.
- Expand codebook generation only where the mechanism requires it; abbreviate long sequences with an ellipsis and a stated example count.

**Cautions.**
- Do not reuse Figure 2 dashed-line semantics automatically: in Figure 3 the caption defines dashed elements as optional.
- Do not preserve the logo/empty center at the expense of legible code labels.

## qwen35-omni

**Qwen3.5-Omni Technical Report** — Alibaba / Qwen, 2026; arXiv:2604.15804v1.
[Primary PDF](https://arxiv.org/pdf/2604.15804v1) · [Record](https://arxiv.org/abs/2604.15804v1)

PDF title page names Qwen Team and links the Qwen repositories; official Qwen3-VL repository About text identifies Qwen team, Alibaba Cloud (https://github.com/QwenLM/Qwen3-VL).

### Figure 2 — Thinker/Talker with interleaved multimodal context (PDF p3)

**Family:** stacked multimodal token architecture. **Selected region:** [70, 70, 526, 374] PDF pt, top-left origin.

**Layout and hierarchy.** A time-aligned video/waveform specimen at the bottom feeds two modality encoders. An interleaved token ribbon enters the Thinker, whose hidden states and generated text form a second ribbon for the Talker. A compact upper-right inset expands code generation.

**Geometry.** A single raster embeds the diagram. Long horizontal model bars provide hierarchy; color-coded token rows connect scales from input frames through hidden representations to speech codes.

**Colors.**
- text tokens: `#C6C8F1` (raster_sampled). 
- vision hidden states: `#FEFFBF` (raster_sampled). 
- audio hidden states: `#FCE5D7` (raster_sampled). 
- text hidden states: `#A7E8E4` (raster_sampled). 
- code embeddings: `#E9AF87` (raster_sampled). 

**Typography.**
- model labels: Exact visible family not established, size unverified, large purple italic sans-serif, much smaller token annotations (visual_estimate).

**Routes and boundaries.** Short vertical arrows map aligned hidden-state positions between Thinker and Talker. The speech output stays in a separate upper-right region, preventing it from obscuring the input chronology.

**Transfer.**
- Use spatial alignment to show correspondence between token sequences at different architectural levels.
- Keep multimodal input time, model scope and generation order as distinct visual axes or regions.

**Cautions.**
- Do not reproduce every tiny token when a grouped sample and count can communicate the same correspondence.
- Use labels, not hue alone, to distinguish pale yellow, peach and lavender states in grayscale reproduction.

### Figure 3 — Compact audio encoder/decoder with external text-conditioning route (PDF p4)

**Family:** vertical encoder–decoder. **Selected region:** [162, 76, 427, 310] PDF pt, top-left origin.

**Layout and hierarchy.** Two large neutral rounded groups divide encoder and decoder. White inner operation bars show repeated layers, with counts placed outside a brace. Waveform and token strips sit between stages rather than inside overloaded model labels.

**Geometry.** The portrait-like crop is 265×234 pt. Module groups have generous width compared with inner bars; the input waveform and token rows make the rate transition concrete. The native graphic is raster, so precise font and stroke metrics remain unknown.

**Colors.**
- acoustic feature tokens: `#F8DA79` (raster_sampled). 
- audio hidden tokens: `#F0DFD6` (raster_sampled). 
- outline: `#1F2D50` (raster_sampled). 
- heading accent: `#5846C3` (raster_sampled). 

**Typography.**
- module headings: Exact visible family not established, size unverified, italic purple sans-serif headings and dark repetition counts (visual_estimate).

**Routes and boundaries.** The main audio path runs bottom-to-top. A right-side conditioning route travels around both groups and enters decoder cross-attention directly, preserving a clean central spine.

**Transfer.**
- Reserve an outside corridor for conditioning that bypasses earlier stages.
- Use repetition brackets and counts to compress regular stacks while keeping their order explicit.

**Cautions.**
- Do not infer timing or token count solely from the waveform or drawn token strip.
- Add an explicit edge label if the bypass route could be mistaken for feedback.

## Transferable recipes and rules

### Matched change localization

Sources: deepseek-mhc Figure 1, deepseek-v41-flash Figure 4.

**Use:** Architectural variants or compute/reuse modes whose shared structure matters.

**Observed basis:** Matched operator positions; complexity-proportional panel widths; unchanged compute retains cyan/neutral; changed mappings use paired warm/green accents.

**Composition:** Start with a 0.76:1:1 panel-width ratio only when the first variant is simpler. Keep the same operation centerlines and box dimensions; write a short legend for change and state provenance.

**Caution:** These sizes and weights are production recommendations, not measurements of the source. Do not add green success semantics that conflict with computed/reused state.

Recommended production tokens (not source measurements):

```json
{
  "canvas_mm": [
    178,
    92
  ],
  "font": "installed readable sans-serif; math companion only for notation",
  "body_pt": 8.5,
  "heading_pt": 10.5,
  "small_pt": 7.5,
  "module_outline_pt": 0.8,
  "route_pt": 1.0,
  "background": "#F2F2F2",
  "shared_compute_fill": "#C1E5F5",
  "baseline_change_fill": "#FBE3D6",
  "proposed_change_fill": "#D9F2D0",
  "baseline_change_outline": "#C04F15",
  "proposed_change_outline": "#4EA72E"
}
```

### Four-stage mechanism storyboard

Sources: hunyuanworld2 Figure 2, hunyuanworld1 Figure 3.

**Use:** A real multi-stage pipeline with different operations, intermediate data and meaningful outputs.

**Observed basis:** Four equal tall stage cards, generous route gutters, aligned stage/model labels, semantic icons and real miniature outputs.

**Composition:** Give each stage one or two named operations and one meaningful example/output, with forward routes in the 6 mm gutters. Use glyphs for data, computation and state only where those roles differ.

**Caution:** Do not force four stages onto a method with another causal structure. The recommended opaque footer is a practical color token, not a raw source fill measurement.

Recommended production tokens (not source measurements):

```json
{
  "canvas_width_mm": 178,
  "outer_margin_mm": 6,
  "card_width_mm": 37,
  "gutter_mm": 6,
  "body_pt": 8.5,
  "heading_pt": 10.5,
  "small_pt": 7.5,
  "card_outline_pt": 0.75,
  "main_route_pt": 1.2,
  "stage_fills": [
    "#DDEBF7",
    "#DFEDDA",
    "#FCE6C6",
    "#F6DAF1"
  ],
  "stage_inks": [
    "#215F9A",
    "#3B7D23",
    "#E97132",
    "#7030A0"
  ],
  "footer_opaque_recommendation": "#405888"
}
```

### Multimodal overview with one expanded operation

Sources: qwen-image Figure 6, qwen3-tts Figure 3, qwen35-omni Figure 2.

**Use:** Models with multiple token/hidden-state types and one important fusion/generation mechanism.

**Observed basis:** Overview/detail split; stable stream colors; short token ribbons; semantically separate residual/conditioning routes; expanded attention or codebook generation.

**Composition:** Use a compact input example and grouped token ribbon in the overview; reserve almost half the width for the new mechanism. Use dashed, arrowless expansion boundaries and named colored data routes.

**Caution:** The source red/cyan fills are translucent. Use the rendered pastel or retain alpha. Do not import raster-only font identities or copy source logos.

Recommended production tokens (not source measurements):

```json
{
  "overview_to_detail_ratio": [
    0.52,
    0.48
  ],
  "body_pt": 8.5,
  "heading_pt": 10.5,
  "small_pt": 7.5,
  "token_width_mm": 2.8,
  "token_height_mm": 3.0,
  "token_gap_mm": 0.8,
  "trainable_fill": "#FFCCCC",
  "frozen_fill": "#CDEFFC",
  "text_route": "#4472C4",
  "image_route": "#7131A1",
  "dark_ink": "#263238"
}
```

### Persistent memory beneath a streaming computation

Sources: worldplay Figure 2, worldplay Figure 4, worldplay Figure 5.

**Use:** Streaming agents, chunked generation, retrieval/replay, or memory-augmented distillation.

**Observed basis:** A persistent lower memory ribbon, repeated current-step groups, separate retrieval and update corridors, and matched memory-index matrices.

**Composition:** Give memory a continuous physical region and each time step a bounded current computation. Label read, write and loss paths separately. Use a matrix inset only when index selection itself is the contribution.

**Caution:** The source artwork is rasterized; the sampled colors are approximate rendered tokens, and proposed dimensions/fonts are new design recommendations.

Recommended production tokens (not source measurements):

```json
{
  "current_compute": "#5480AD",
  "memory_accent": "#C25759",
  "current_fill": "#DFE9F5",
  "body_pt": 8.5,
  "heading_pt": 10,
  "route_pt": 1.0,
  "feedback_corridor_mm": 5
}
```

### Data-flow quantity contract

Sources: qwen-image Figure 10, hunyuanworld1 Figure 3.

**Rule:** A Sankey-like ribbon invites a quantitative reading. Use widths only for known flows with units and conservation checks; otherwise use an explicitly schematic branch graph. Show reject paths without implying measured fractions. Stage-specific color is acceptable when named as stage role, but it does not track persistent cohort identity.

### Phase-aware dash vocabulary

Sources: qwen3-tts Figure 2, qwen3-tts Figure 3.

**Rule:** Even within one report, a dashed line can mean training-only in one figure and optional in another. Derive line-style semantics from each caption; define a local legend and keep that meaning consistent inside the delivered figure set.

### Physical plausibility before trusting extraction

Sources: qwen-image Figure 6, deepseek-ocr Figure 1, qwen3-vl Figure 3.

**Rule:** Validate extracted geometry against rendered appearance and region scale. Treat enormous raw drawing widths as untrusted metadata, invisible text as search/OCR metadata, and transparency as part of a color. Record a visible font as unknown when only outlines or raster lettering exist.

### Do not inherit poor source legibility

Sources: hunyuanworld1 Figure 2, deepseek-v41-flash Figure 4, deepseek-mhc Figure 4.

**Rule:** Prestigious reports still contain 3.6–5 pt diagram labels. Use their grouping and comparison grammar while enlarging text, removing a full transcript, replacing repeated operations with counts, or adding a detail panel.

