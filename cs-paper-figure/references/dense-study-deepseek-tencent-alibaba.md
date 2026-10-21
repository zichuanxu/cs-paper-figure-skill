# Dense-figure study: DeepSeek, Tencent and Alibaba/Qwen

Inspected 2026-10-21. **14 distinct new primary papers; 30 numbered figure anchors.** Original years: 2024 = 1, 2025 = 11, 2026 = 2. Company coverage: DeepSeek = 4, Tencent = 5, Alibaba/Qwen = 5.

A distinct primary paper/report counts once; revisions and multiple crops do not increase paper count. A numbered figure counts once even when it contains many panels. Only visually inspected figures are counted. Selection targets technical and visual usefulness, not a claim of an objective top-paper ranking.

Observed PDF object measurements, observed rendered pixels, visual interpretations and new design recommendations are separated. Exact source version, first-submission date, 1-based PDF page, crop and SHA-256 are recorded. Descriptive figure analysis is original; source artwork is not part of the reusable skill deliverable.

## What this study adds

The most reusable finding is an explanatory hierarchy: system overview, representation-level example, and operator or diagnostic detail. Information density is useful when the added detail resolves a scientific ambiguity. More boxes, decorative icons and tiny labels are not a substitute. Several visually rich source figures contain 1.8–6 pt microtype; the skill should improve on that limitation rather than imitate it.

## Source inventory

| Paper | Original year | Pinned version | Inspected figures (PDF pages) |
|---|---:|---|---|
| [Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling](https://arxiv.org/abs/2501.17811v1) | 2025 | 2501.17811v1 | Figure 3 (p3), Figure 4 (p8) |
| [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention](https://arxiv.org/abs/2502.11089v1) | 2025 | 2502.11089v1 | Figure 2 (p3), Figure 3 (p9) |
| [DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition](https://arxiv.org/abs/2504.21801v1) | 2025 | 2504.21801v1 | Figure 2 (p3), Figure 3 (p4) |
| [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437v1) | 2024 | 2412.19437v1 | Figure 3 (p10), Figure 4 (p12), Figure 5 (p13) |
| [HunyuanCustom: A Multimodal-Driven Architecture for Customized Video Generation](https://arxiv.org/abs/2505.04512v1) | 2025 | 2505.04512v1 | Figure 2 (p4), Figure 3 (p5) |
| [HunyuanPortrait: Implicit Condition Control for Enhanced Portrait Animation](https://arxiv.org/abs/2503.18860v1) | 2025 | 2503.18860v1 | Figure 2 (p3), Figure 3 (p5) |
| [HunyuanVideo-Avatar: High-Fidelity Audio-Driven Human Animation for Multiple Characters](https://arxiv.org/abs/2505.20156v1) | 2025 | 2505.20156v1 | Figure 2 (p4), Figure 3 (p5) |
| [HunyuanVideo-Foley: Multimodal Diffusion with Representation Alignment for High-Fidelity Foley Audio Generation](https://arxiv.org/abs/2508.16930v1) | 2025 | 2508.16930v1 | Figure 2 (p4), Figure 4 (p12) |
| [WorldMirror: Universal 3D World Reconstruction with Any-Prior Prompting](https://arxiv.org/abs/2510.10726v1) | 2025 | 2510.10726v1 | Figure 2 (p4), Figure 5 (p8) |
| [Wan: Open and Advanced Large-Scale Video Generative Models](https://arxiv.org/abs/2503.20314v1) | 2025 | 2503.20314v1 | Figure 6 (p11), Figure 21 (p31) |
| [Qwen2.5-Omni Technical Report](https://arxiv.org/abs/2503.20215v1) | 2025 | 2503.20215v1 | Figure 2 (p3), Figure 3 (p4), Figure 4 (p5) |
| [Wan-Animate: Unified Character Animation and Replacement with Holistic Replication](https://arxiv.org/abs/2509.14055v1) | 2025 | 2509.14055v1 | Figure 2 (p4), Figure 3 (p6) |
| [Wan-Animate-2: Pushing the Application Boundaries of Character Animation](https://arxiv.org/abs/2608.06009v1) | 2026 | 2608.06009v1 | Figure 1 (p5), Figure 2 (p7) |
| [Qwen3-ASR Technical Report](https://arxiv.org/abs/2601.21337v1) | 2026 | 2601.21337v1 | Figure 2 (p3), Figure 3 (p6) |

## Reusable advanced recipes

### One mechanism at three scales

A sophisticated figure exposes different levels of explanation instead of merely increasing box count. The strongest examples connect the system overview to the representation geometry and to the exact operation.

**Source anchors:** wan-animate2-fig1, native-sparse-attention-fig2, native-sparse-attention-fig3, hunyuan-portrait-fig2, hunyuan-video-foley-fig2

**Construction:**

1. Allocate the largest stable region to an overview with one readable main path. Use the remaining area for one representation panel and one operator panel. These regions need not have equal width or height.
2. Carry a small set of semantic object identities across all panels: e.g. query tokens, reference tokens and retained memory. Make the corresponding labels identical.
3. Let each panel use the right visual form: architecture lanes, token/time strips, tensor cuboids, attention matrices or loss-alignment rows.
4. Attach explicit dimensions, access-mask axes or transformation examples where they settle a technical ambiguity.
5. Use saturated color for the novel selection or changed state; keep containers and established operations quieter.

**Production requirements:**

- Recommended target: 7.5–9 pt ordinary labels at final placement, larger panel headings and a separately readable caption. These are new design recommendations, not claimed source measurements.
- Start at final physical width, then choose the number of panels and examples. If an operator becomes unreadable, split it into a second figure or a larger inset.
- Use editable vector text, paths and matrices; use raster only for meaningful media evidence.

**Review:** Can the reader find the new computation within five seconds? Does every detail panel answer a question not already answered by the overview? Do token identity, axes and endpoints agree across panels?

### Stateful time: static condition, current chunk, retained state and output

Streaming and systems figures become informative when they expose state and timing boundaries. Merely repeating an encoder block hides the dependency that matters.

**Source anchors:** wan-animate2-fig2, wan21-fig6, qwen25-omni-fig3, qwen25-omni-fig4, deepseek-v3-fig4, deepseek-v3-fig5

**Construction:**

1. Use a shared time coordinate. Put static conditions in a small side region; keep current inputs and outputs in separate aligned lanes.
2. Draw the chunk boundary or cache boundary and explicitly name retained, padded, evicted and newly computed objects.
3. Show at least one nontrivial boundary transition. Use indexed tokens or frame groups so the carried state can be traced.
4. Use a matrix for many device/time or query/context relationships; use a few explicit arrows for the specific return dependency.
5. If claiming efficiency, pair a schematic schedule with measured latency or memory data and clearly state units, hardware, batch size and concurrency.

**Production requirements:**

- Do not use schematic cell counts as runtime evidence.
- Encode temporal role redundantly through position, labels and a pattern or border style rather than color alone.
- Keep cache-return arrows outside dense content, ending at a named state object or port.

**Review:** What exactly persists between steps? Where does time advance? Are shared weights and shared state distinguishable? Does the drawing accidentally suggest future access in a causal path?

### Worked structured artifacts with a visible local change

The missing ingredient in many plain AI diagrams is an actual object being transformed: a proof, program, instruction, token sequence, mask or grounded description. A small truthful example explains more than an ornamental icon.

**Source anchors:** deepseek-prover-v2-fig2, deepseek-prover-v2-fig3, qwen3-asr-fig3, hunyuan-custom-fig3, janus-pro-fig4

**Construction:**

1. Choose one short input artifact with enough context to understand the operation. Show it before the transformation and after it.
2. Keep unchanged identifiers, order and phrasing identical so the reader can perform a visual diff.
3. Assign a persistent numbered marker or highlight to the artifact being selected or modified. Use a second explicit state label for accepted, rejected, unresolved or resolved.
4. If training is involved, show the aligned target/output positions and exactly where the objective applies.
5. Place a validator or evidence object beside the changed artifact when success depends on a specific check.

**Production requirements:**

- Use a real or explicitly synthetic worked example; do not fabricate an experiment result.
- Excerpt long code and responses. Preserve the changed span plus only the necessary surrounding context.
- Avoid full paragraphs below 7.5 pt. An attractive high-resolution preview is not a paper-size proof.

**Review:** Can the reader name the input and output artifact types? Is the exact change visible? Does the example demonstrate the claimed operation without suggesting unmeasured generality?

### Controlled comparison: invariants aligned, differences localized

Comparison becomes precise when identical elements look identical and meaningful differences are placed at corresponding coordinates.

**Source anchors:** hunyuan-video-avatar-fig3, worldmirror-fig5, deepseek-v3-fig3, wan21-fig6

**Construction:**

1. Choose the comparison axis: method variant, injected prior, objective depth or boundary condition. Keep all other relevant conditions visible and fixed.
2. Align common module baselines, image viewpoints, token indices and panel scales.
3. Use accent color only around the changed operation or condition. Keep shared stages neutral.
4. Allow unequal panel width when complexity genuinely differs, while preserving invariant baselines.
5. For empirical comparisons, label the intervention and reference target and disclose the example-selection rule.

**Production requirements:**

- Use named mechanisms instead of generic baseline/ours headings when the figure is intended to teach.
- Add redundant labels or patterns for before/after rather than relying on red/green alone.
- Do not imply superiority by giving one method a larger or more decorated area.

**Review:** What changed, and what was held fixed? Can the reader find the difference without comparing unrelated visual styles? Are selected examples being kept distinct from aggregate evidence?

### Mechanism paired with a matching diagnostic

Architecture alone cannot establish that the mechanism has the intended effect. The most informative figure sets connect a named mechanism to a diagnostic that measures or illustrates that effect.

**Source anchors:** hunyuan-video-foley-fig2, hunyuan-video-foley-fig4, worldmirror-fig2, worldmirror-fig5, janus-pro-fig3, janus-pro-fig4

**Construction:**

1. Choose the diagnostic from the claim: temporal alignment uses a time-aligned signal, geometry uses matched viewpoints and local regions, sparse computation uses an access mask, and artifact editing uses a before/after diff.
2. Use the same scenario, object identities or time coordinates between the method explanation and evidence.
3. Make units, scale, normalization, reference targets and uncertainty explicit where applicable.
4. Separate descriptive schematic evidence from measured data; label synthetic examples if used.
5. Include a failure or limiting case when it materially explains the scope.

**Production requirements:**

- Never use a visually appealing heatmap as evidence without defining its scalar mapping.
- For media evidence, preserve crop, viewpoint, frame timing and display settings across methods.
- Keep qualitative example selection transparent.

**Review:** What part of the mechanism does this diagnostic test? Could scale or normalization create the apparent difference? Does the evidence support the stated scope?

## Measurement cautions

PDF RGB values are raw object properties and preserve alpha. The rendered appearance may differ because of blending, masks, clipping or background. Raster palette entries are explicit samples from the inspected 216 dpi crop, and do not recover an authoring palette. Whole-page fonts, invisible text and OCR layers are excluded from visible typography claims. Type3 or outlined glyphs do not identify a typeface. Raster lettering has no recovered point size. Native stroke metadata is retained only where trusted; transformed raw widths are flagged. The Prover-V2 inspection exposed lone-surrogate glyphs; the updated inspector preserves the raw codepoint/index and exports valid Unicode replacement characters.

## Paper-by-paper figure analysis

<a id="janus-pro"></a>
### Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model Scaling

**DeepSeek · original year 2025 · 2501.17811v1 · first submission 2025-01-29**

[Primary PDF](https://arxiv.org/pdf/2501.17811v1) · [Version metadata](https://arxiv.org/abs/2501.17811v1)

PDF title page explicitly credits DeepSeek-AI and links the official deepseek-ai/Janus repository.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `2f5b4b26341f7be4a5c2851718f84af9c41b3084093ad71254e54ad68272a793`

#### Figure 3, PDF p3: Decoupled vision encoding with a shared autoregressive backbone

**Family:** architecture overview. **Crop:** [70, 83, 526, 275] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Two lightly tinted task territories flank a shared full-width backbone. Inputs sit below the common model and outputs above it; each task has a vision branch and a text branch. The common backbone crosses the territorial split, making shared computation physically visible.

**Routing.** All actual computation arrows point upward. The two encoding paths remain separate until the shared transformer. Ellipses bridge the task territories rather than indicating explicit data flow.

**Information layers:** task identity: understanding versus generation; modality-specific input encoder or tokenizer; shared autoregressive model; task-specific output decoder.

**Detail devices:** aligned input and output baselines; subscripts connect image, instruction and response symbols; one spanning backbone instead of duplicated model boxes; distinct pale task territories.

**Density assessment.** Moderate density and unusually readable main labels; the figure explains one architectural distinction well but cannot alone supply the mechanism-level sophistication requested by the user.

**Color evidence:**

- understanding encoder: `#DAE9FD`; vector_measured; alpha 1.0000.
- generation encoder and decoder: `#FFF3CC`; vector_measured; alpha 1.0000.
- common operations: `#F5F5F5`; vector_measured; alpha 1.0000.
- understanding domain tint: `#ECF0F9`; vector_measured; alpha 0.4706.
- generation domain tint: `#FFF4CC`; vector_measured; alpha 0.2980.

**Typography:**

- module labels: Georgia at 7.99 pt (visible_pdf_text_measured).
- shared backbone: Georgia at 11.42 pt (visible_pdf_text_measured).
- mathematical subscripts: CambriaMath at 5.71 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 67.7 mm; aspect 2.38. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The backbone is wider and typographically larger than all adapters, correctly making shared computation the first read.
- Shadows and rounded pills make the schematic friendly, but do not explain any additional mechanism.
- Both pastel territory fills are translucent; raw RGB must not be mistaken for their much lighter rendered appearance.

**Transferable rules:**

- Show a genuinely shared module as a spanning object across aligned task lanes.
- Use this as the overview panel of a richer figure, then add tokenization or attention detail and a worked case.
- Reserve larger type for the architectural claim; keep task labels and object symbols subordinate.

**Do not copy blindly:**

- Do not use this simple overview alone as the target level of sophistication for a complex method.
- Do not reproduce heavy drop shadows or low-contrast gray headings merely because they appeared in the source.

Evidence status: 45 nominally visible text traces; 0 invisible traces; 20 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 4, PDF p8: Capability evidence board with worked multimodal exchanges and prompt–image pairs

**Family:** worked-example evidence board. **Crop:** [70, 82, 526, 739] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A full-width description example sits above a two-column middle: landmark/general-knowledge cases occupy the wider left region and OCR occupies a tall right region. A bottom 4×2 contact sheet pairs generated images with prompts. Black task tabs and thin rectangular borders create local entry points.

**Routing.** There are no causal arrows. Image, prompt and answer proximity defines each exchange. Task tabs define grouping, so this is an evidence board rather than an architecture graph.

**Information layers:** capability category; concrete input image; actual user prompt; model answer with selected phrase emphasis; text-to-image output and conditioning prompt.

**Detail devices:** task-specific tab headers; paired input/prompt cards; selective answer highlighting; 4×2 generated-example grid; mixed Chinese and English examples.

**Density assessment.** High content volume with clear groups, but source paragraphs fall near 5.5 pt. The board requires enlargement and deliberate excerpt selection to remain readable at ordinary paper size.

**Color evidence:**

- task tabs: `#000000`; vector_measured; alpha 1.0000.
- prompt boxes: `#F0F7FF`; vector_measured; alpha 1.0000.
- answer text: `#1F2937`; visible_text_color_measured; alpha 1.0000.
- selected answer phrases: `#00B050`; visible_text_color_measured; alpha 1.0000.

**Typography:**

- dense English responses: Aptos at 5.51 pt (visible_pdf_text_measured).
- larger response and prompt labels: Aptos at 7.34 pt (visible_pdf_text_measured).
- Chinese response: DengXian-Regular at 7.34 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 231.8 mm; aspect 0.69. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 5. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The OCR example gets a taller cell because a large text image needs vertical space.
- The bottom examples use a regular grid while the heterogeneous understanding examples use unequal regions.
- Green phrase emphasis helps locate grounded claims, but the source does not provide bounding-box links that prove which image region supports each phrase.

**Transferable rules:**

- Give heterogeneous evidence examples unequal space according to their actual reading burden.
- Pair every output with its conditioning input and an explicit task label.
- For a new figure, reduce each answer to the relevant excerpt and connect selected phrases to image regions with numbered evidence markers.

**Do not copy blindly:**

- Do not treat a curated gallery as aggregate evidence of model quality.
- Do not preserve every paragraph in a reduced column-width board.
- Do not copy the transformed raw stroke widths: five paths fail the inspector sanity rule.

Evidence status: 276 nominally visible text traces; 0 invisible traces; 16 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="native-sparse-attention"></a>
### Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention

**DeepSeek · original year 2025 · 2502.11089v1 · first submission 2025-02-16**

[Primary PDF](https://arxiv.org/pdf/2502.11089v1) · [Version metadata](https://arxiv.org/abs/2502.11089v1)

PDF title page lists DeepSeek-AI, Peking University / PKU-Anker LLM Lab, and University of Washington; DeepSeek is affiliation 1.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `d96f7b38fa7480cbb8add18fba1307249175865a6674583ccbd5db14b5a13aa2`

#### Figure 2, PDF p3: Three sparse-attention branches linked to their explicit masks

**Family:** architecture plus operator masks. **Crop:** [70, 80, 526, 218] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A wide upper token sequence is partitioned into contiguous blocks, then branches into compression, selection and a sliding window. Three branch outputs align at the bottom and merge into one gated output. A separate right column contains three matching attention masks in the same vertical order.

**Routing.** The query token feeds all three branches along a low horizontal bus. Key/value branches descend from the common sequence. A dashed return from compressed scores to top-n selection exposes selection dependence. Only branch outputs meet at the final gate.

**Information layers:** input sequence and block partition; three distinct sparsification operations; query sharing and score-driven selection; branch output fusion; mask geometry of each operation.

**Detail devices:** token strips with fixed cells; coarse compressed blocks versus fine selected cells; ghosted evicted tokens; three explicit attention matrices; common branch ordering between mechanism and masks; local legend for active, evicted and ignored tokens.

**Density assessment.** Very high and intellectually productive density: every repeated strip or matrix exposes a different transformation. The source is much too small in its original placement, with many labels around 3.6–5.3 pt.

**Color evidence:**

- query token: `#EA9424`; vector_measured; alpha 1.0000.
- input token tint: `#4A90E2`; vector_measured; alpha 0.2000.
- stronger activated tokens: `#4A90E2`; vector_measured; alpha 0.8000.
- computed attention fields: `#27A700`; vector_measured; alpha 0.4000.
- selection or branch accent: `#27A700`; vector_measured; alpha 1.0000.
- eviction ghosting: `#333333`; vector_measured; alpha 0.6000.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Compact bold sans-serif labels, italic branch names and mathematical symbols; the PDF reports Unnamed-T3 glyph fonts, not an identifiable family.
- reported Type3 label size, family unknown: Unnamed-T3 at 3.56 pt (visible_pdf_text_measured).
- reported Type3 major-label size, family unknown: Unnamed-T3 at 5.34 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 48.7 mm; aspect 3.30. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The left diagram teaches the process, while the right column makes the process checkable as patterns of computed cells.
- Input width and branch widths differ by purpose; visual regularity comes from aligned baselines rather than uniform box sizes.
- Green and blue vary through opacity, so they are families of rendered tones rather than single opaque colors.

**Transferable rules:**

- Pair a mechanism overview with the exact binary or weighted operator pattern it induces.
- Keep branch order identical in the pipeline, output row and diagnostic masks.
- Represent removal through ghosting and explicit legend states, not by silently deleting elements.
- Allocate a full-width figure or a dedicated detail panel when token labels would otherwise drop below a readable size.

**Do not copy blindly:**

- Do not report Unnamed-T3 as a named corporate font.
- Do not blindly adopt the tiny label scale or claim block widths encode real token counts without specifying the scale.
- Do not turn schematic masks into empirical attention heatmaps.

Evidence status: 24 nominally visible text traces; 0 invisible traces; 9 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 3, PDF p9: Memory-aware sparse-attention kernel on a Q–K–V tile field

**Family:** hardware kernel dataflow. **Crop:** [175, 235, 430, 436] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A square computation field is framed by K across the top, V down the right, Q as a stacked set of heads on the left, and output along the bottom. A small green tile in each memory bank is carried to a central SRAM computation. The outer margins hold loop directions and tensor dimensions.

**Routing.** Green orthogonal arrows encode loads into the active tile. Gray dashed hooks encode sparse block selection. A black path sends the computed output down to HBM. Outer black arrows distinguish grid-loop motion from inner-loop motion.

**Information layers:** tensor axes and dimensions; GQA query grouping; sparse K/V selection; HBM-to-SRAM transfer; inner and outer loop order; output writeback.

**Detail devices:** matrix backdrop; small dimension brackets; stacked heads; active green tile; different line styles for selection and transfer; named memory locations at the action.

**Density assessment.** High and coherent: the spatial frame is the computation. Labels are near 6.7 pt, larger than the companion overview but still require a paper-size proof.

**Color evidence:**

- HBM tile tint: `#4A90E2`; vector_measured; alpha 0.2000.
- active query stack: `#4A90E2`; vector_measured; alpha 1.0000.
- SRAM tiles and transfers: `#27A700`; vector_measured; alpha 1.0000.
- selected tile field: `#27A700`; vector_measured; alpha 0.1000.
- grid: `#DDDDDD`; vector_measured; alpha 0.8000.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Bold sans-serif loop and operation labels with serif math dimensions; the PDF stores Unnamed-T3 glyphs.
- reported Type3 labels, actual family unknown: Unnamed-T3 at 6.74 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 90.0 × 70.9 mm; aspect 1.27. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- Edges carry stored tensors; the center carries computation, so spatial position has a stable technical meaning.
- The token and memory color identities are inherited from the overview without repeating its full legend.
- The route from three sources to the active tile has genuine convergence; junctions should be made unambiguous in a new implementation.

**Transferable rules:**

- For a tiled kernel, let the matrix axes organize the entire figure rather than placing a disconnected matrix beside generic boxes.
- Write tensor shapes adjacent to the physical strip they describe.
- Use different route styles for selecting a block, loading it and writing a result.

**Do not copy blindly:**

- Do not imply geometric tile area equals bytes or latency unless the scale is explicitly defined.
- Do not infer a named font or reliable stroke width from filled Type3/outline geometry.

Evidence status: 16 nominally visible text traces; 0 invisible traces; 2 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="deepseek-prover-v2"></a>
### DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition

**DeepSeek · original year 2025 · 2504.21801v1 · first submission 2025-04-30**

[Primary PDF](https://arxiv.org/pdf/2504.21801v1) · [Version metadata](https://arxiv.org/abs/2504.21801v1)

PDF title page explicitly states DeepSeek-AI and links the official DeepSeek-Prover-V2 repository.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `2a4cd822a133fcc566b76b6e78adb40ac0a98b2e0d20db432ca50d18a24bc8ae`

#### Figure 2, PDF p3: Worked proof decomposition, recursive subgoal solving and synthesis

**Family:** worked transformation and verification. **Crop:** [70, 80, 526, 313] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Two large equal-height territories carry a single proof case from natural-language interpretation and a proof skeleton on the left to recursive subgoal solving and a completed proof on the right. The top-right subgoal card is smaller; the lower-right proof card is taller to show the inserted solution in context.

**Routing.** Reading order and repeated theorem names express the transformation. An orange clipboard marker and an orange highlight carry the same unresolved induction step between cards; a green checked marker highlights its resolved insertion. No dense arrow network is required.

**Information layers:** input proposition; informal reasoning sketch; formal skeleton with holes; a selected subgoal as a stand-alone lemma; completed proof with the resolved span in place.

**Detail devices:** actual mathematical example; syntax coloring; persistent subgoal identity; orange-to-green state transition; local code excerpt highlights; before/after code context.

**Density assessment.** High semantic density with a precise worked example. It is more informative than a five-box training pipeline, but much text is about 6.1 pt; a new version should shorten the code around the changed span.

**Color evidence:**

- natural-language decomposition territory: `#B6C7EA`; vector_measured; alpha 1.0000.
- formal-solving territory: `#D9D9D9`; vector_measured; alpha 1.0000.
- code cards: `#F0EFEF`; vector_measured; alpha 1.0000.
- unresolved subgoal: `#FCE6D5`; vector_measured; alpha 1.0000.
- resolved replacement span: `#E3F2D9`; vector_measured; alpha 1.0000.
- input theorem card: `#EFF6FF`; vector_measured; alpha 1.0000.

**Typography:**

- code and mathematical content: Calibri at 6.07 pt (visible_pdf_text_measured).
- explanatory prose: TimesNewRomanPSMT at 6.07 pt (visible_pdf_text_measured).
- section labels: TimesNewRomanPS-BoldMT at 6.07 pt (visible_pdf_text_measured).
- mathematical symbols: CambriaMath at 6.07 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 82.2 mm; aspect 1.96. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The same object appears at different levels of abstraction, which lets the reader verify the claimed transformation.
- Color partitions process phases while small highlights indicate state changes; these are separate color roles.
- A major strength is preserving surrounding proof context so the green solved block is seen as an insertion rather than a detached success badge.

**Transferable rules:**

- For reasoning or agent systems, include an actual structured artifact before and after the key operation.
- Assign one persistent marker to the artifact being transformed across panels.
- Highlight the changed span, while leaving unchanged context quiet.
- Use explicit unresolved and resolved labels in addition to color.

**Do not copy blindly:**

- Do not substitute decorative code for an artifact that is actually processed by the method.
- Do not confuse a displayed complete proof with a reproducibly verified claim unless the verifier and result are supplied.
- Do not re-use the raw extracted text blindly: this crop contained 16 lone-surrogate glyph values, retained as raw metadata and rendered as replacement characters in JSON after the inspector fix.

Evidence status: 316 nominally visible text traces; 0 invisible traces; 6 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 3, PDF p4: Exact lemma rewrite with and without preceding subgoals as premises

**Family:** local transformation comparison. **Crop:** [70, 80, 526, 225] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** The left half shows the full decomposed theorem. The right half contains two vertically stacked lemma forms: substituting the selected goal, then incorporating previously proved subgoals as premises. The selected line uses the same orange mark in all three code regions.

**Routing.** A repeated marker and matching text perform the linking. The source deliberately avoids long arrows through code, allowing code alignment and heading order to establish the correspondence.

**Information layers:** original theorem and all decomposed subgoals; selected lower-bound subgoal; stand-alone lemma form; additional premises from earlier subgoals.

**Detail devices:** two alternative transformed code blocks; line-level highlight; stable variable names; syntax color; compact numbered panel headings.

**Density assessment.** Dense but focused: two rewrite rules are grounded in one real example. The 5.9 pt source code is not an acceptable default for a new figure at reduced size.

**Color evidence:**

- decomposition territory: `#B6C7EA`; vector_measured; alpha 1.0000.
- derived lemma territory: `#D9D9D9`; vector_measured; alpha 1.0000.
- code cards: `#F0EFEF`; vector_measured; alpha 1.0000.
- selected goal: `#FCE6D5`; vector_measured; alpha 1.0000.

**Typography:**

- code: Calibri at 5.91 pt (visible_pdf_text_measured).
- panel headings: TimesNewRomanPS-BoldMT at 5.91 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 51.2 mm; aspect 3.14. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The unmodified part of the expression is repeated to make the changed goal and added premises inspectable.
- The right upper card is shallower than the lower card because the second transformation genuinely adds information.
- The colored territory is a context frame; the orange row is the actual point of attention.

**Transferable rules:**

- When presenting a transformation rule, show one shared input and aligned alternative outputs.
- Keep unchanged identifiers identical so the reader can perform a visual diff.
- Use a row highlight for the specific operation and a different color role for the broader process phase.

**Do not copy blindly:**

- Do not replace the transformation with an arrow labeled improve; expose the actual edit.
- Do not preserve full long expressions if the necessary local context can be shown more readably.

Evidence status: 335 nominally visible text traces; 0 invisible traces; 3 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="deepseek-v3"></a>
### DeepSeek-V3 Technical Report

**DeepSeek · original year 2024 · 2412.19437v1 · first submission 2024-12-27**

[Primary PDF](https://arxiv.org/pdf/2412.19437v1) · [Version metadata](https://arxiv.org/abs/2412.19437v1)

PDF title page states DeepSeek-AI and gives research@deepseek.com.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision. The original and inspected version are 2024, even though a later v2 was submitted in 2025; this source is retained for distinct MTP and DualPipe visual mechanisms.

PDF SHA-256: `a67e18a4ca6e2c81abc030239a3ee53705f656b79efab8ce1d6b5ac25630c2a5`

#### Figure 3, PDF p10: Multi-token prediction with shifted targets and explicit parameter sharing

**Family:** parallel objectives and causal dependencies. **Crop:** [70, 80, 526, 289] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Three left-to-right columns show the base model and two prediction depths. Target token strips and cross-entropy losses align across the top; input token strips and embeddings align across the bottom. Middle operations expand in the auxiliary columns to expose normalization, concatenation and projection.

**Routing.** Black arrows carry activation dependencies vertically and between successive depths. Pale green dotted lines mark tied output and embedding parameters, which are explicitly distinct from the black causal routes. Each depth has its own named loss.

**Information layers:** prediction depth; shifted input and target indices; local auxiliary module operations; cross-depth hidden-state dependency; shared versus independent parameters; per-depth objective.

**Detail devices:** aligned shifted token rows; dashed module containers; multiplicity stack for the main transformer; paired normalization nodes; separate line style for parameter sharing; explicit loss symbols.

**Density assessment.** High but controlled, with a common column grammar. The operation labels are about 7.7 pt and more practical than many dense sources; mathematical indices still fall near 5 pt.

**Color evidence:**

- compute and losses: `#FFF2CC`; vector_measured; alpha 1.0000.
- shared embedding and output heads: `#C5E0B4`; vector_measured; alpha 1.0000.
- token strips: `#EDEDED`; vector_measured; alpha 1.0000.
- module boundaries: `#2E75B6`; vector_measured; alpha 1.0000.
- module outlines: `#172C51`; vector_measured; alpha 1.0000.

**Typography:**

- module labels: Calibri at 7.69 pt (visible_pdf_text_measured).
- sharing annotations: Calibri-Italic at 6.12 pt (visible_pdf_text_measured).
- equation symbols: CambriaMath at 6.91 pt (visible_pdf_text_measured).
- small mathematical indices: CambriaMath at 5.07 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 73.7 mm; aspect 2.18. Most frequent trusted native widths: 0.5756, 0.8635 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- Uniform baselines make index shifts immediately visible.
- The large main model is compressed into a stack, while the novel auxiliary module is expanded.
- Parameter sharing is presented orthogonally to computation, preventing a common scientific diagram ambiguity.

**Transferable rules:**

- Use matched input, output and loss baselines for parallel objectives.
- Compress established components and expand the new computation.
- Give weight tying a distinct non-causal line style and an explicit label.
- Show the shifted token indices whenever prediction depth is the main contribution.

**Do not copy blindly:**

- Do not imply that tied parameters create an activation dependency.
- Do not make tiny mathematical subscripts the only evidence of a crucial difference; add depth labels.

Evidence status: 110 nominally visible text traces; 0 invisible traces; 0 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 4, PDF p12: Local computation–communication overlap timeline

**Family:** distributed-systems micro-schedule. **Crop:** [70, 80, 526, 133] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Two tightly coupled lanes share a time axis: computation above communication. Rectangular segments expose operation overlap. Hollow and filled triangle suffixes distinguish the two chunks in addition to the work-type colors.

**Routing.** Time runs left to right; there are no causal inter-operation arrows. Vertical alignment of segment extents, not connector lines, expresses concurrency.

**Information layers:** operation identity; compute versus communication resource; forward versus backward chunk; temporal overlap and boundaries.

**Detail devices:** two aligned resource lanes; triangle identity marks; operation abbreviations with direction suffixes; specific dispatch and combine labels; distinct pipeline communication segment.

**Density assessment.** Compact and meaningful as a local detail accompanying a global schedule. It is too short vertically to carry extensive explanation, and its lane labels are only about 4.8 pt.

**Color evidence:**

- forward work: `#FFC60A`; vector_measured; alpha 1.0000.
- backward-input work: `#B3D600`; vector_measured; alpha 1.0000.
- backward-weight work: `#7EDAFB`; vector_measured; alpha 1.0000.
- pipeline communication: `#AD82F7`; vector_measured; alpha 1.0000.
- communication boundary: `#F76964`; vector_measured; alpha 1.0000.

**Typography:**

- operation labels: Times-Roman at 6.65 pt (visible_pdf_text_measured).
- lane labels: HelveticaNeue-Bold at 4.75 pt (visible_pdf_text_measured).
- chunk legend: HelveticaNeue-Bold at 6.65 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 18.7 mm; aspect 8.60. Most frequent trusted native widths: 0.1663, 0.1188, 0.3564 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The schedule gives two different encodings to chunk direction and work type, avoiding an overloaded palette.
- All-to-all and pipeline communication are shown in the same resource lane, making their timing claim visible.
- Some raw fills have zero opacity; these are not visible palette colors and must be excluded.

**Transferable rules:**

- For overlap claims, align actual resource lanes against one time coordinate.
- Use a second visual channel for task identity when color already encodes operation type.
- Pair the local schedule with a global device schedule rather than attempting one unreadably complete timeline.

**Do not copy blindly:**

- Do not call schematic segment widths measured runtime unless timings are available.
- Do not copy invisible raw colors or extremely thin 0.12–0.17 pt source strokes into a new output.

Evidence status: 29 nominally visible text traces; 0 invisible traces; 0 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 5, PDF p13: DualPipe device-by-time schedule with split-cell overlap states

**Family:** distributed-systems global schedule. **Crop:** [70, 80, 526, 161] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Eight device rows share a fine time grid. A diagonal startup and reverse-direction startup meet in a dense middle region, while split orange/green cells indicate overlapped forward and backward work. The legend sits directly below and includes the compound state.

**Routing.** No explicit connectors are needed: device rows and repeated micro-batch IDs express progression. Direction-specific symmetry is explained in the caption; reverse-direction IDs are omitted in the source.

**Information layers:** device identity; time slot; micro-batch identity; forward/backward work type; overlap within a time cell; startup and drain bubbles.

**Detail devices:** device-by-time matrix; numeric batch IDs; split-color compound state; white idle cells; compound legend entry.

**Density assessment.** Extremely dense and effective for showing a global scheduling pattern, but 4.5 pt labels make individual batch tracing hard at paper size. A new figure should include a highlighted batch route and a readable zoom.

**Color evidence:**

- forward work: `#FEAE00`; vector_measured; alpha 1.0000.
- backward work: `#61D836`; vector_measured; alpha 1.0000.
- backward weight work: `#56C1FF`; vector_measured; alpha 1.0000.
- idle cells: `#FFFFFF`; vector_measured; alpha 1.0000.

**Typography:**

- schedule labels and batch indices: HelveticaNeue at 4.53 pt (visible_pdf_text_measured).
- device and legend labels: HelveticaNeue-Bold at 4.53 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 28.6 mm; aspect 5.63. Most frequent trusted native widths: 0.3233, 0.1131 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The empty cells carry as much meaning as colored cells because they reveal the pipeline bubble.
- The matrix is more economical than hundreds of routed task arrows.
- The source uses the same green for full backward and backward-input work; adjacency and legend context carry part of the distinction.

**Transferable rules:**

- Use a device×time matrix for dense schedules, preserving idle cells as first-class states.
- Explain compound occupancy with a compound legend sample.
- Add one highlighted micro-batch trajectory or a magnified strip when individual causality matters.
- Provide assumptions and time units outside the matrix.

**Do not copy blindly:**

- Do not interpret the count of schematic cells as a measured speedup.
- Do not rely on the 4.5 pt micro-labels or on color alone to distinguish scheduling states.

Evidence status: 197 nominally visible text traces; 0 invisible traces; 0 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="hunyuan-custom"></a>
### HunyuanCustom: A Multimodal-Driven Architecture for Customized Video Generation

**Tencent · original year 2025 · 2505.04512v1 · first submission 2025-05-07**

[Primary PDF](https://arxiv.org/pdf/2505.04512v1) · [Version metadata](https://arxiv.org/abs/2505.04512v1)

PDF title page explicitly states Tencent Hunyuan.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `847debe841a3631a9180548f40022022da23ada597e68555672ab9148317ad09`

#### Figure 2, PDF p4: Multimodal customization with distinct subject, video and audio injection routes

**Family:** multi-input architecture. **Crop:** [108, 69, 504, 307] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A full-width subject-conditioning lane sits above the central video-generation lane. Two lower side-by-side territories explain video and audio control. The model sits near the center and receives each condition at the correct injection point. The top lane expands LLaVA into text/image prompt token strips and their interaction.

**Routing.** Blue subject/image routes enter both identity-enhanced latents and the central model. Green video controls pass through tokenizer and feature alignment to an explicit add junction. Orange audio controls travel from a waveform through an encoder and temporal compression to cross-attention. The lane geometry avoids placing all inputs in one undifferentiated list.

**Information layers:** four input modalities with concrete examples; subject identity enhancement; text/image token fusion; video mask and feature alignment; audio temporal compression and spatial cross-attention; generated video.

**Detail devices:** actual input and output frame stacks; token examples inside the language-model subgraph; mask imagery; noise-versus-identity-enhanced latent comparison; explicit add junction; modality-colored injection routes.

**Density assessment.** High useful density with a clear central action. Source labels near 4.7 pt and numerous miniature token words require enlargement or a two-panel decomposition in new work.

**Color evidence:**

- subject and model territory: `#DAE3F5`; vector_measured; alpha 1.0000.
- base generation territory: `#FFF2CA`; vector_measured; alpha 1.0000.
- video control territory: `#E3F2D9`; vector_measured; alpha 1.0000.
- audio control territory: `#FCE6D5`; vector_measured; alpha 1.0000.
- subject route: `#4874CB`; vector_measured; alpha 1.0000.
- video route: `#75BD42`; vector_measured; alpha 1.0000.
- audio route: `#EE822F`; vector_measured; alpha 1.0000.

**Typography:**

- ordinary labels: Arial-BoldMT at 4.75 pt (visible_pdf_text_measured).
- larger module labels: Arial-BoldMT at 7.12 pt (visible_pdf_text_measured).
- token and math annotations: KingsoftMath at 4.75 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 139.7 × 84.0 mm; aspect 1.66. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The pale regions have distinct process meanings and the small saturated routes repeat those meanings.
- The top lane contains a detailed internal mechanism, while the central lane stays simple enough to orient the reader.
- Images depict the actual controlled identity rather than generic stock icons.

**Transferable rules:**

- Organize multimodal architecture by injection mechanism, not merely by input modality names.
- Pair each condition with the actual data object it carries: masked frames, waveform, token strip or identity reference.
- Use a single central generation lane and named side routes to preserve reading order.
- Put the key fusion operation inside an expanded module.

**Do not copy blindly:**

- Do not let corporate logos occupy more space than a technical operation.
- Do not reproduce the 4.7 pt labels or depend solely on similar pastel territories to define modality.

Evidence status: 44 nominally visible text traces; 0 invisible traces; 20 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 3, PDF p5: Data-construction recipe with filtering, grounding, segmentation and audio alignment examples

**Family:** data pipeline and concrete preprocessing. **Crop:** [108, 69, 504, 260] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A narrow data-source contact strip is followed by a large four-row filtering column, then a second four-row column of task-specific extraction. The right rows have different heights because single-subject detection, multi-subject grounding and audio synchronization require different amounts of evidence.

**Routing.** Numbered filters imply stage order without arrows between every filter. Within extraction rows, arrows expose specific transformations: detection boxes, grounded noun phrases, segmented subjects and audio alignment. The distinction between a checklist-like sequence and an actual dataflow is visible.

**Information layers:** raw data diversity; four filtering operations and criteria; single-subject detection and matching; multi-subject text grounding and segmentation; audio synchronization and quality filtering.

**Detail devices:** numbered stage badges; criteria chips; real image bounding boxes; noun-phrase highlights linked to grounded objects; cut-out subjects; waveform and alignment checkpoint.

**Density assessment.** Very high and semantically rich, but some source labels are only 1.8–4.7 pt. The architecture of this board is useful; the literal density is not a readable production target.

**Color evidence:**

- filtering territory: `#E8F1F9`; vector_measured; alpha 1.0000.
- criteria chips: `#C5E0B4`; vector_measured; alpha 1.0000.
- stage markers: `#4472C4`; vector_measured; alpha 1.0000.
- single-subject territory: `#FFF2CC`; vector_measured; alpha 1.0000.
- operation callout: `#C8621C`; vector_measured; alpha 1.0000.
- detected span highlight: `#00FF00`; vector_measured; alpha 1.0000.

**Typography:**

- stage labels: Calibri-Bold at 4.69 pt (visible_pdf_text_measured).
- small criterion labels: Calibri-Bold at 3.62 pt (visible_pdf_text_measured).
- very small local annotations: Calibri-Bold at 1.81 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 139.7 × 67.4 mm; aspect 2.07. Most frequent trusted native widths: 0.9712, 0.259 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The far-left thumbnails establish input diversity without repeating paragraphs.
- Common filters use a stable card grammar, while specialized extraction uses concrete visual examples.
- Vivid green highlights and red/yellow detection boxes compete for attention; in a new version, reserve saturated color for one evidence-linking purpose.

**Transferable rules:**

- Show what a preprocessing stage does to one example instead of listing only tool names.
- Use repeated cards for repeated screening logic and a different spatial grammar for heterogeneous extraction logic.
- Make acceptance criteria and transformation outputs explicit.
- Split the final board into an overview and two enlarged worked rows when text becomes microscopic.

**Do not copy blindly:**

- Do not reproduce tiny tool logos, 1.8 pt microtext, or many competing saturated annotations.
- Do not imply a numbered checklist alone proves the flow or order of all data processing.

Evidence status: 109 nominally visible text traces; 0 invisible traces; 27 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="hunyuan-portrait"></a>
### HunyuanPortrait: Implicit Condition Control for Enhanced Portrait Animation

**Tencent · original year 2025 · 2503.18860v1 · first submission 2025-03-24**

[Primary PDF](https://arxiv.org/pdf/2503.18860v1) · [Version metadata](https://arxiv.org/abs/2503.18860v1)

PDF title page explicitly lists Hunyuan, Tencent, alongside Tsinghua University, Sun Yat-Sen University and HKUST.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `1f7832a65691d279625705b29d7442c391df24fe30dd76dcf03ef51c40bb3492`

#### Figure 2, PDF p3: Portrait animation overview with two matching extractor expansions

**Family:** architecture plus module detail. **Crop:** [58, 69, 554, 375] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** The upper region shows video diffusion with appearance, pose and motion controls injected at multiple U-Net depths. A horizontal dash-dot divider leads to two lower module expansions: the appearance extractor on the left and the intensity-aware motion extractor on the right. Matching pink and lavender fills maintain identity between overview and detail.

**Routing.** A pink horizontal bus fans into appearance attention blocks; a lavender bus fans into motion blocks. Black routes carry image, pose and face-crop data. Lower module expansions show residual paths, concatenation or addition explicitly, with motion memory entering cross-attention from below.

**Information layers:** reference and driving image roles; denoising U-Net stages; multi-depth appearance and motion injection; fine-grained appearance extractor internals; intensity-controlled motion extractor internals; motion memory bank.

**Detail devices:** colored U-Net operation bars; matched overview/detail color identities; face-crop example reused in modules; residual/add junctions; memory-bank slots; repeated block stacks with consistent offsets.

**Density assessment.** High but well layered. Most labels near 7.3 pt are more readable than many competitors; the figure still needs full-width placement because three pathways and two expansions are involved.

**Color evidence:**

- denoising container: `#FBF5DE`; vector_measured; alpha 1.0000.
- appearance pathway: `#FADBDF`; vector_measured; alpha 1.0000.
- appearance injection routes: `#EF949E`; vector_measured; alpha 1.0000.
- motion pathway: `#DFE3F1`; vector_measured; alpha 1.0000.
- motion injection routes: `#B6C7EA`; vector_measured; alpha 1.0000.
- temporal or cross attention: `#E3F2D9`; vector_measured; alpha 1.0000.
- spatial convolution and adapter accent: `#F5B482`; vector_measured; alpha 1.0000.

**Typography:**

- ordinary labels: ComicSansMS at 7.27 pt (visible_pdf_text_measured).
- larger headings: ComicSansMS at 8.87 pt (visible_pdf_text_measured).
- some operation symbols: HelveticaNeue at 7.27 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 175.0 × 108.0 mm; aspect 1.62. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The overview receives roughly three-fifths of the figure height, while the two novel modules share the remainder.
- A legend explains operation categories near the U-Net rather than forcing the reader to infer colors from prose.
- The informal rounded font is an observed stylistic choice, not evidence that this font improves scientific communication.

**Transferable rules:**

- Build an overview with one or two detail panels whose object identity matches exactly.
- Expose the repeated injection sites with aligned operation bars rather than one vague conditioning arrow.
- Place a module expansion near the input example that helps interpret it.
- Use residual junctions and memory-bank objects only where those operations actually exist.

**Do not copy blindly:**

- Do not adopt Comic Sans by default; choose a legible available family appropriate to the paper.
- Do not let the dash-dot panel divider be mistaken for a computational boundary.
- Do not create crossing buses without differentiating junctions from pass-through crossings.

Evidence status: 47 nominally visible text traces; 0 invisible traces; 44 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 3, PDF p5: ID-aware multi-scale adapter as a focused local computation

**Family:** expanded local operator. **Crop:** [58, 69, 295, 136] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A single horizontal data path goes from downsampling to three stacked convolution branches, an explicit channel concatenation node, cross-attention and upsampling. The ID feature travels above the main path and enters attention at a separate port.

**Routing.** Parallel convolution branches have their own short arrows and meet at C. The ID feature does not join the convolution concatenation; it enters attention through a separate top route. This separation clarifies feature fusion semantics.

**Information layers:** latent resolution change; three spatial receptive-field sizes; channel concatenation; identity conditioning; restored output resolution.

**Detail devices:** three labeled kernel sizes; dedicated identity route; C junction; down/up taper shapes.

**Density assessment.** Moderate focused detail. This small operator is valuable as an inset in the richer preceding overview, rather than as the sole showcase figure.

**Color evidence:**

- identity feature: `#DAE3F5`; vector_measured; alpha 1.0000.
- latent: `#F5B482`; vector_measured; alpha 1.0000.
- multi-scale convolutions: `#FFF2CA`; vector_measured; alpha 1.0000.
- cross-attention: `#DAF4DA`; vector_measured; alpha 1.0000.
- sampling stages: `#F2F2F2`; vector_measured; alpha 1.0000.

**Typography:**

- module labels: ComicSansMS at 6.43 pt (visible_pdf_text_measured).
- operation symbol: HelveticaNeue at 6.43 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 83.6 × 23.6 mm; aspect 3.54. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- Only the multi-scale operation is expanded; a reader can see the actual architectural change.
- The top identity route provides a clean example of routing a condition around a main chain without crossing it.

**Transferable rules:**

- Expand the novel operator at a scale that lets its input roles and merge operation be verified.
- Stack parallel operations vertically when they share an input and output.
- Keep conditioning arrows separate from concatenation unless they really share that operation.

**Do not copy blindly:**

- Do not add extra decorative stages to make a small true computation look complex.
- Do not infer that a tapered shape always means a particular encoder without labeling the operation.

Evidence status: 20 nominally visible text traces; 0 invisible traces; 5 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="hunyuan-video-avatar"></a>
### HunyuanVideo-Avatar: High-Fidelity Audio-Driven Human Animation for Multiple Characters

**Tencent · original year 2025 · 2505.20156v1 · first submission 2025-05-26**

[Primary PDF](https://arxiv.org/pdf/2505.20156v1) · [Version metadata](https://arxiv.org/abs/2505.20156v1)

PDF title page explicitly states Tencent Hunyuan and links the official Tencent-Hunyuan/HunyuanVideo-Avatar repository.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `24ec31785abf37249ef0542866acf670f4892e17ee029e7cad6535de07660dd9`

#### Figure 2, PDF p4: Avatar architecture with training status, emotional control and face-masked audio injection

**Family:** multi-condition training architecture. **Crop:** [108, 69, 504, 248] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** The left side builds tokens from repeated reference frames, video and a text prompt. The top-right center contains the HunyuanVideo backbone. Two expanded conditioning modules occupy the lower center and the far right: a face-aware audio adapter and an emotion module. A compact top-left legend establishes addition, trainable and frozen states.

**Routing.** Colored routes trace the reference-image token path, tokenizer weight copy, audio adapter injection and emotion cross-attention. Q, K and V are explicit at the audio adapter; a face mask multiplies the resulting latent before it is injected into the backbone.

**Information layers:** input repetition and latent encoding; tokenizer relationship and copied weights; frozen versus trainable modules; backbone double/single blocks; Q/K/V audio conditioning; face-mask gating; emotion reference conditioning.

**Detail devices:** snowflake/fire training-status icons; three modality token colors; Q/K/V ports; face-mask stack; addition and multiplication symbols; concrete character/emotion images.

**Density assessment.** Very high technical density but crowded at the source size. Fine labels around 3.9 pt are a strong caution; a new version should dedicate a full panel to the face-aware adapter.

**Color evidence:**

- video tokens: `#6E2D9E`; vector_measured; alpha 1.0000.
- double-block and routing accent: `#237C94`; vector_measured; alpha 1.0000.
- text tokens: `#70AD47`; vector_measured; alpha 1.0000.
- expanded adapter territory: `#DCEEF4`; vector_measured; alpha 1.0000.
- base neutral region: `#F4F2F1`; vector_measured; alpha 1.0000.

**Typography:**

- fine architecture labels: TimesNewRomanPSMT at 3.93 pt (visible_pdf_text_measured).
- major labels: TimesNewRomanPS-BoldMT at 5.26 pt (visible_pdf_text_measured).
- larger labels: TimesNewRomanPSMT at 5.90 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 139.7 × 63.1 mm; aspect 2.21. Most frequent trusted native widths: 0.5736, 0.9834, 0.6146, 1.1473, 0.9424, 1.2292, 0.5327, 0.6966 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- Training status is encoded through small icons while modality identity is encoded by color, allowing two independent readings.
- The audio module is a true expansion with inputs, attention and a mask; it is not merely a colored box labeled adapter.
- Different token and latent stages use different palettes; labels must state those representation changes so color does not falsely imply identity.

**Transferable rules:**

- Separate representation identity from training-state identity by using two visual channels.
- Expose Q/K/V roles and mask gating when they are central to the mechanism.
- Give each novel conditioning path its own local diagram and named endpoint.
- Use a few genuine input examples to make control semantics concrete.

**Do not copy blindly:**

- Do not preserve dense 3.9 pt labels, redundant icons or all inline prose.
- Do not use flames and snowflakes without a legend or as an aesthetic motif unrelated to trainability.
- Do not let a copied-weight route look like a runtime data route.

Evidence status: 76 nominally visible text traces; 0 invisible traces; 38 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 3, PDF p5: Three character-injection variants with invariant attention geometry

**Family:** controlled architecture comparison. **Crop:** [108, 69, 504, 237] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Three side-by-side variants share the same vertical ordering: input token strip, tokenizer or tokenizers, QKV concatenation, attention, projection, output token strip. The first two variants have equal-sized attention boxes; the proposed variant receives extra horizontal room for the actual added projection and add junction.

**Routing.** Black arrows encode computation. A small repeated-image route and an explicit projected addition explain how the proposed variant differs. Common QKV and attention stages retain the same order in all columns.

**Information layers:** modality token identity; tokenizer allocation; token-versus-channel concatenation; projection-based injection; invariant attention and output stages.

**Detail devices:** matched operation baselines; same colored token grammar across variants; explicit repeat count T; localized projected addition; panel labels with method names.

**Density assessment.** High comparison value with moderate visual clutter. Source labels are 5.4–7.3 pt; extra width is warranted because the comparison is about small wiring differences.

**Color evidence:**

- video tokens: `#6E2D9E`; vector_measured; alpha 1.0000.
- text tokens: `#70AD47`; vector_measured; alpha 1.0000.
- image tokens: `#FFD966`; vector_measured; alpha 1.0000.
- attention modules: `#B4C7E7`; vector_measured; alpha 1.0000.
- common projection or tokenizer: `#DDEEF4`; vector_measured; alpha 1.0000.
- attention operation: `#FFE79A`; vector_measured; alpha 1.0000.

**Typography:**

- module labels: TimesNewRomanPSMT at 6.45 pt (visible_pdf_text_measured).
- small token labels: TimesNewRomanPSMT at 5.36 pt (visible_pdf_text_measured).
- variant headings: TimesNewRomanPS-BoldMT at 6.45 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 139.7 × 59.3 mm; aspect 2.36. Most frequent trusted native widths: 0.7723, 0.1343 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The reader can compare the changed input-conditioning region while ignoring the repeated attention body.
- A neutral shared background keeps the comparison from becoming three unrelated cards.
- The proposed variant is larger because it contains more inputs; invariants are aligned rather than forced into identical box widths.

**Transferable rules:**

- Preserve common module order, colors and baselines across architecture variants.
- Spend the extra space only on the changed computation.
- Label the actual concatenation axis or addition semantics.
- Use exact repeated objects rather than drawing each variant in a different visual style.

**Do not copy blindly:**

- Do not equate larger visual area with better method quality.
- Do not label a variant ours without an informative mechanism name in a reusable template.

Evidence status: 46 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="hunyuan-video-foley"></a>
### HunyuanVideo-Foley: Multimodal Diffusion with Representation Alignment for High-Fidelity Foley Audio Generation

**Tencent · original year 2025 · 2508.16930v1 · first submission 2025-08-23**

[Primary PDF](https://arxiv.org/pdf/2508.16930v1) · [Version metadata](https://arxiv.org/abs/2508.16930v1)

PDF title page explicitly lists Tencent Hunyuan, Zhejiang University and Nanjing University of Aeronautics and Astronautics.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `b888e987dd4d839ddea38158867d2896c5c3df59da11b19ae31b59543f74d21f`

#### Figure 2, PDF p4: Audio-generation stack with synchronization, representation loss and an expanded multimodal block

**Family:** architecture plus loss and operator detail. **Crop:** [54, 49, 558, 351] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A tall overview stack runs upward from text, video and audio inputs through multimodal blocks, audio-only blocks and a waveform decoder. The left margin carries synchronization and representation-alignment loss branches. A narrow right column expands one multimodal block into two stream-specific towers and their attention interactions.

**Routing.** Black routes carry data; gray side buses carry modulation; a dashed expansion bracket connects the multimodal stack to the detailed right tower. The audio stream alone continues to the unimodal blocks. A frozen audio feature extractor supplies a separate REPA loss target.

**Information layers:** three modality encoders; synchronization features and time embedding; multimodal-to-unimodal transition; representation alignment supervision; self-attention and cross-attention composition; interleaved positional encoding; residual and gated updates.

**Detail devices:** N1/N2 multiplicities; explicit audio-only transition; loss branch with frozen reference encoder; two-stream operator expansion; Q/K/V role labels; residual and gate junctions; waveform at input and output.

**Density assessment.** Very high mechanism density, with a disciplined large overview and narrow local expansion. The raster artwork is crisp at this inspection size, but exact typography and line widths cannot be measured from native PDF text.

**Color evidence:**

- multimodal blocks: `#FFE6CC`; render_sampled.
- text and frozen audio encoder modules: `#DAE8FC`; render_sampled.
- audio latent and encoder: `#D5E8D4`; render_sampled.
- visual pathway: `#FFF2CC`; render_sampled.
- synchronization pathway: `#C6F7F7`; render_sampled.
- interleaved RoPE: `#E1D5E7`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Handwritten-looking rounded sans-serif labels with heavier stage labels; the entire figure is one raster image, so no exact family or point size is recoverable.

**Geometry and strokes.** Selected region 177.8 × 106.5 mm; aspect 1.67. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The most complex region is isolated to the right, so the main path remains legible.
- Loss and synchronization branches live on the opposite side from the operator expansion, reducing crossovers.
- Pastel module colors encode modality or operation class while the gray bus indicates conditioning.

**Transferable rules:**

- Give side branches stable roles: supervision on one side, module expansion on the other.
- Explicitly label where a multimodal architecture becomes single-modality.
- Expose the internal attention ordering and residual paths when that ordering is part of the contribution.
- Name loss targets and frozen reference models at their actual branch.

**Do not copy blindly:**

- Do not infer a native font or stroke width from this raster source.
- Do not add arrows that cross a stream merely to balance the composition; preserve actual operator semantics.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 4, PDF p12: Video-to-audio temporal evidence board with matched spectrogram rows

**Family:** time-aligned qualitative diagnostics. **Crop:** [90, 49, 535, 332] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Two scenario columns share the same layout. A three-frame video strip sits above six method spectrogram rows. Each method is held at the same row across scenarios, allowing both within-scenario and across-scenario comparison.

**Routing.** Vertical alignment links visible action times to acoustic events; no flow arrows are used. Horizontal position is implicitly temporal, but the source does not display a time axis or frequency units.

**Information layers:** visual event sequence; method identity; acoustic energy over time and frequency; comparison across two motion types.

**Detail devices:** frame-strip context; equal-size spectrogram panels; consistent method ordering; shared column boundaries; concrete rhythmic and start/stop events.

**Density assessment.** High diagnostic density and a useful complement to an architecture figure. Its scientific interpretability is limited by absent visible time/frequency axes and an unspecified color scale in the artwork.

**Color evidence:**

- spectrogram intensity: Dark blue/purple through magenta and orange to light yellow; the figure has no visible numeric colorbar, so its scalar mapping cannot be recovered or assumed. (visual_estimate).
- image examples: Two fixed video scenarios, each shown as a three-frame strip. (raster_observed).

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Bold sans-serif method names rotated along the left edge. All lettering and spectrograms are embedded in a single raster.

**Geometry and strokes.** Selected region 157.0 × 99.8 mm; aspect 1.57. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The video strip is not decoration: it establishes the event whose timing the spectrograms should follow.
- Equal panel dimensions support local timing comparison, but they do not by themselves guarantee shared spectrogram normalization.
- The source makes it easy to scan rows but harder to read the rotated small method labels.

**Transferable rules:**

- Place concrete event evidence immediately above the aligned signal representation.
- Hold scenario columns and method rows fixed across all panels.
- For a new scientific figure, add time/frequency units, a shared or explicitly per-panel intensity scale, and event markers.
- Describe the example-selection rule and provide aggregate results separately.

**Do not copy blindly:**

- Do not claim sound fidelity from a visually attractive spectrogram alone.
- Do not copy the missing axes or assume a shared normalization without verifying it.
- Do not use this intensity palette as a categorical architecture palette.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="worldmirror"></a>
### WorldMirror: Universal 3D World Reconstruction with Any-Prior Prompting

**Tencent · original year 2025 · 2510.10726v1 · first submission 2025-10-12**

[Primary PDF](https://arxiv.org/pdf/2510.10726v1) · [Version metadata](https://arxiv.org/abs/2510.10726v1)

PDF title page explicitly lists Tencent Hunyuan, Zhejiang University and Chinese University of Hong Kong.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `f8b2dfa3e8ff27c457ff994fe35ccc57bd268500c0618d96c1d9625d1afacbc3`

#### Figure 2, PDF p4: Optional geometric priors merged into tokens and decoded into six output representations

**Family:** multi-representation architecture. **Crop:** [108, 79, 504, 211] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A five-stage horizontal architecture pairs three concrete multiview inputs with three optional-prior stacks. A compact token-merging inset explains how priors meet image tokens. Feature aggregation and stacked heads lead to a 2×3 output gallery: point maps, normals, Gaussians, cameras, depths and novel views.

**Routing.** Short gray arrows connect stages. Token merging uses stacked examples and a local thick arrow instead of a fan-out of every individual token. The output gallery is grouped under one heading, while each output remains individually labeled.

**Information layers:** multiview inputs; optional geometric prior types; token-level merge operation; shared feature aggregation; task-specific prediction heads; different output representation forms.

**Detail devices:** actual matched building views; camera/depth/pose thumbnails; hatched token types; local merge inset; typed prediction heads; six concrete output forms.

**Density assessment.** High representation density in a shallow full-width figure. It is especially useful for explaining one representation transformed into several outputs, but the tiny raster token legend needs enlargement in a new design.

**Color evidence:**

- prior-prompt territory: `#F2EFFB`; render_sampled.
- prediction heads: `#DFE9F6`; render_sampled.
- depth token: `#A7DAF5`; render_sampled.
- merged-token tones: `#BFB9DD`; render_sampled.
- image token tone: `#EAF7D5`; render_sampled.
- image token companion tone: `#FCF0DC`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Bold sans-serif region headings, regular sans-serif module labels and mathematical subscripts; the PDF figure is a single raster.

**Geometry and strokes.** Selected region 139.7 × 46.6 mm; aspect 3.00. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- Real outputs prevent abstract head names from becoming the only explanation.
- The central token inset contains the main fusion mechanism; the rest of the architecture stays compressed.
- Hatching adds an identity channel for some geometric tokens that is independent of pastel color.

**Transferable rules:**

- When a model has multiple geometric outputs, show an example of each representation beside its head.
- Use a small token-merging inset to explain how optional priors enter a shared backbone.
- Encode optional conditions explicitly and preserve their labels into the merge.
- Use patterns as well as colors for semantically different token families.

**Do not copy blindly:**

- Do not mistake the raster source for editable vector typography.
- Do not infer that output image area represents task importance, accuracy or compute.
- Do not show all possible priors as mandatory inputs.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 5, PDF p8: Controlled reconstruction comparison isolating the effect of each geometric prior

**Family:** matched intervention evidence. **Crop:** [108, 79, 504, 260] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Three rows use different scenes to demonstrate camera poses, camera intrinsics and depth. Four logical columns show multiview inputs, images-only reconstruction, reconstruction with priors and ground truth. The added prior is labeled between the matched reconstructions.

**Routing.** A gray arrow introduces the baseline reconstruction; a purple arrow labels the added prior. Dashed detail boxes occupy corresponding object regions before and after the intervention. These arrows mean a changed conditioning configuration, not elapsed time.

**Information layers:** input views; baseline reconstruction; single named prior intervention; conditioned reconstruction; ground-truth reference; local geometric detail differences.

**Detail devices:** fixed output viewpoints; four-column matched comparison; row-specific named intervention; corresponding dashed regions; explicit ground-truth column.

**Density assessment.** High evidence content without many words. The matched camera framing and intervention labels do more work than additional decorative callouts would.

**Color evidence:**

- prior-addition arrows: `#A486C3`; render_sampled.
- prior and model label accent: `#67359A`; render_sampled.
- baseline detail boxes: `#E73323`; render_sampled.
- conditioned detail boxes: `#6FC069`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Bold sans-serif column headings, italic purple model name and regular purple intervention labels; the figure is raster embedded.

**Geometry and strokes.** Selected region 139.7 × 63.9 mm; aspect 2.19. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- Each row changes one prior type, allowing the reader to connect a concrete condition with a visible geometric effect.
- The baseline and conditioned outputs have consistent visual scale within a row.
- Red and green boxes communicate before/after but are not independently accessible to every reader; labels or shapes should be added.

**Transferable rules:**

- Use matched views, scale and crops for intervention comparisons.
- Label the exact changed input between baseline and result.
- Retain a reference column when it makes the target geometry inspectable.
- Use identical detail-region coordinates and add explicit before/after labels.

**Do not copy blindly:**

- Do not present selected scene comparisons as an unbiased aggregate result.
- Do not copy red/green-only distinction or treat the arrow as proof of causality without controlled experimental conditions.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="wan21"></a>
### Wan: Open and Advanced Large-Scale Video Generative Models

**Alibaba / Qwen · original year 2025 · 2503.20314v1 · first submission 2025-03-26**

[Primary PDF](https://arxiv.org/pdf/2503.20314v1) · [Version metadata](https://arxiv.org/abs/2503.20314v1)

PDF title page explicitly states Wan Team, Alibaba Group.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `a144f86e8a921aa4d8b9c720d77eff2fef31bc4f1e6d7754a5095e53d99a1989`

#### Figure 6, PDF p11: Chunk-boundary feature caching with explicit padding and temporal downsampling

**Family:** temporal dependency diagram. **Crop:** [108, 79, 504, 190] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Two matched horizontal panels compare the default causal convolution with 2× temporal downsampling. Each has an upper input row split into Chunk 0 and Chunk 1, a lower output row and dependency arrows. Orange zero/cache padding marks sit at the exact chunk boundary where they matter.

**Routing.** Gray dashed arrows map each input window to an output. Black short routes identify which preceding features become cached padding. A large blue curved arrow names the common causal convolution. The two panels use the same grammar but different output spacing/counts.

**Information layers:** chunk boundary; real versus zero-padded versus cached input; causal receptive field; output index; effect of temporal downsampling.

**Detail devices:** indexed circles; hatched cache token; dashed chunk boxes; explicit zero versus cache labels; paired comparison; dependency arrows.

**Density assessment.** Moderate density with strong explanatory specificity and principal source labels around 8.8 pt. This is a good model for a readable detail panel inside a more complex system figure.

**Color evidence:**

- frame or feature position: `#9DCED1`; vector_measured; alpha 1.0000.
- padding outline: `#ED7D31`; vector_measured; alpha 1.0000.
- causal-convolution arrow: `#2F77B2`; vector_measured; alpha 1.0000.
- background chunk territory: `#EFEDE3`; vector_measured; alpha 0.1961.
- ghosted padded feature: `#BFBFBF`; vector_measured; alpha 0.4627.

**Typography:**

- frame indices: Calibri at 8.85 pt (visible_pdf_text_measured).
- operation and padding labels: TimesNewRomanPSMT at 8.85 pt (visible_pdf_text_measured).
- panel descriptions: TimesNewRomanPSMT at 8.85 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 139.7 × 39.2 mm; aspect 3.57. Most frequent trusted native widths: 0.7366, 0.491, 0.0687 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The important boundary case is drawn explicitly instead of hidden in an ellipsis.
- Hatching disambiguates cached padding from ordinary colored inputs.
- The output count and arrow incidence show the effect of downsampling without a paragraph of prose.

**Transferable rules:**

- For streaming systems, draw the chunk boundary and expose retained state.
- Distinguish real, padded and cached elements with shape/pattern as well as color.
- Align two schedules using the same indices and receptive-field grammar.
- Use one nontrivial boundary example rather than many repeated middle-of-sequence steps.

**Do not copy blindly:**

- Do not assume all dashed arrows have the same semantics as elsewhere; label the dependency convention.
- Do not treat translucent raw fills as opaque swatches.

Evidence status: 42 nominally visible text traces; 0 invisible traces; 2 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 21, PDF p31: VACE generation overview with a two-sided context-tokenization mechanism

**Family:** architecture plus structured preprocessing. **Crop:** [108, 79, 504, 365] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** The upper third gives the generation overview: text and time condition a DiT, noise and context enter from below, and a decoder yields video. The lower two-thirds expand context tokenization. Reference frames and masks enter from the left, editing frames and masks from the right, and both are decomposed into reactive/inactive channels that meet in a central context stack.

**Routing.** The mirrored lower flow converges inward and then upward into the shared context. A separate bottom route reshapes masks into the central stack. Dashed context-block routes in the upper panel distinguish adapter-module tuning from direct full-finetuning injection.

**Information layers:** main diffusion generation; two training/injection strategies; reference frame and mask preprocessing; editing frame and mask preprocessing; concept decoupling into reactive/inactive channels; mask reshaping; multiple editing modalities.

**Detail devices:** mirrored preprocessing lanes; actual frame/mask pairs; reactive versus inactive channel stacks; C/P/decoupling symbol legend; concrete canny/depth/pose/scribble inputs; full-finetuning versus adapter routes; upper overview linked to lower expansion.

**Density assessment.** Very high but organized around one central artifact: context tokens. The lower mirrored layout contains substantial detail without making all inputs compete at the main model.

**Color evidence:**

- main DiT backbone: `#E0E1FF`; render_sampled.
- VAE encoder and decoder: `#AADDD9`; render_sampled.
- task-example strip: `#FCE7CB`; render_sampled.
- reactive channels: `#82FF7E`; render_sampled.
- text encoder: `#F7ECC9`; render_sampled.
- time conditioning: `#C5EDFF`; render_sampled.
- neutral context or mask region: `#F2EFE7`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Predominantly serif module labels and italic example captions, with large bold backbone text; the source is a single embedded raster.

**Geometry and strokes.** Selected region 139.7 × 100.9 mm; aspect 1.38. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The overview and detailed preprocessing use different spatial grammars appropriate to their jobs.
- The central context stack is the visual hinge between both lower branches and the upper generator.
- The source uses unusually saturated green for reactive channels; this is semantically useful but can overwhelm the rest of the palette.

**Transferable rules:**

- Make the intermediate representation the center of a rich figure when many tasks share it.
- Use symmetric inward routes for genuinely parallel preprocessing paths.
- Show the actual mask, conditioned data and resulting channel families together.
- Explain alternative training routes with separate line styles and names.

**Do not copy blindly:**

- Do not infer exact native fonts or line widths from the raster.
- Do not use pure vivid green unless it earns its salience through a specific semantic role.
- Do not let a stacked-frame silhouette imply a precise number of frames without a multiplicity label.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="qwen25-omni"></a>
### Qwen2.5-Omni Technical Report

**Alibaba / Qwen · original year 2025 · 2503.20215v1 · first submission 2025-03-26**

[Primary PDF](https://arxiv.org/pdf/2503.20215v1) · [Version metadata](https://arxiv.org/abs/2503.20215v1)

PDF title page credits Qwen Team and links the official repository; the repository description explicitly identifies Qwen team at Alibaba Cloud.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision. arXiv v1 submission is 2025-03-26; the PDF title-page dateline is 2025-03-27.

PDF SHA-256: `95906505512440a3a32c37b10a6aeeef092c44d60fcfaebfb309950685b7cbf1`

[Official affiliation evidence](https://github.com/QwenLM/Qwen2.5-Omni)

#### Figure 2, PDF p3: Thinker–Talker architecture with aligned token/hidden-state tracks and streaming speech

**Family:** multimodal autoregressive architecture. **Crop:** [112, 192, 483, 530] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A bottom audiovisual time strip feeds vision and audio encoders. An interleaved sequence enters a full-width Thinker band. Above it, aligned rows distinguish tokens, hidden states and pads before a full-width Talker band. Codec tokens then feed a streaming waveform decoder. The legend occupies the top-left beside the output.

**Routing.** Curved short routes associate generated text tokens with hidden-state rows; solid and dashed routes distinguish forward and backward propagation. The codec decoder is fed from explicit token cells rather than one opaque speech arrow.

**Information layers:** synchronized audiovisual inputs; input modality encoders; interleaved multimodal sequence; Thinker hidden representations and sampled text; Talker codec generation; padding and propagation states; streaming waveform output.

**Detail devices:** token rows with fixed cells; separate hidden/token vocabularies; actual input/output text snippets; audio/video time axis; propagation-style legend; pads and sampled tokens; streaming codec strip.

**Density assessment.** High representation detail. Its many token colors and propagation routes are meaningful, but the large brand mark consumes space that a new technical figure should spend on readable labels.

**Color evidence:**

- model and label accent: `#5A44CA`; render_sampled.
- text tokens: `#C5C8F2`; render_sampled.
- text hidden state: `#E0EBF6`; render_sampled.
- vision hidden state: `#FEFEC0`; render_sampled.
- audio hidden state: `#FAE4D6`; render_sampled.
- codec output and decoder: `#E8AF88`; render_sampled.
- codec hidden state: `#EADFF3`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Rounded/geometric sans-serif lettering with violet italic model names; the whole figure is raster, so the actual family and point sizes are not recoverable.

**Geometry and strokes.** Selected region 130.9 × 119.2 mm; aspect 1.10. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The figure exposes representation boundaries that a plain Thinker→Talker chain would conceal.
- The two wide model bands establish hierarchy; all smaller objects are arranged relative to them.
- Color is not enough: token and hidden-state roles require the explicit legend and aligned row position.

**Transferable rules:**

- Draw distinct rows for tokens, hidden states and outputs when their interaction is the contribution.
- Provide one concrete short transcript so abstract cell colors have an interpretable example.
- Show padding and streaming state explicitly rather than hiding them in an ellipsis.
- Use the architecture overview together with a separate timing/attention detail.

**Do not copy blindly:**

- Do not reuse the large corporate logo or reproduce the raster as editable figure source.
- Do not make the cell count look proportional to real sequence length unless the scale is stated.
- Do not use unlabeled solid/dashed arrows when they mean different propagation modes.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 3, PDF p4: Time-aligned multimodal position encoding on image patches and audio

**Family:** temporal and spatial indexing. **Crop:** [70, 91, 526, 222] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Three consecutive two-second groups run left to right. Within each group, patch grids for successive video frames sit above a shared waveform. Each patch carries a position tuple, while audio positions and brackets sit below the waveform.

**Routing.** Short down arrows associate frame groups with the audio track. Horizontal arrows connect audio position tuples; braces define equal time chunks. This is a coordinate diagram, not an attention graph.

**Information layers:** time chunk; video frame time; height/width patch coordinates; audio position sequence; synchronized multimodal numbering.

**Detail devices:** overlaid coordinate tuples; paired frame grids; common waveform axis; equal-duration braces; monotonic temporal indices.

**Density assessment.** High conceptual efficiency: a single worked sequence replaces abstract positional-encoding prose. The source uses faded screenshot backgrounds that can still compete with tuple labels.

**Color evidence:**

- position tuples and selected labels: `#5A45D1`; render_sampled.
- backdrop: Lightly faded image patches behind position tuples; black timing arrows and waveform. (visual_estimate).

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Italic violet tuple labels and small bold sans-serif time labels; raster source, exact typeface and size unknown.

**Geometry and strokes.** Selected region 160.9 × 46.2 mm; aspect 3.48. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- Patch grids establish spatial coordinates while the waveform establishes temporal continuity.
- Repeated two-second groups teach a pattern rather than asking the reader to infer it from one isolated tuple.
- The violet tuple text is the actual data; background imagery is subordinate context.

**Transferable rules:**

- For positional encodings, show an explicit small indexed example with real time and spatial coordinates.
- Keep one shared time axis across modalities.
- Fade or simplify the background enough that coordinates remain readable.
- Label what each tuple component means outside the dense grid.

**Do not copy blindly:**

- Do not turn numeric position IDs into elapsed-time claims without the mapping.
- Do not make a faint screenshot carry essential information behind the tuple labels.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 4, PDF p5: Sliding-window block attention with explicit past/current/future states

**Family:** attention-mask detail. **Crop:** [227, 526, 370, 681] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A compact square matrix uses repeated rounded cells. A diagonal band shifts across rows, containing two past blocks, a current block and a future block. Empty white cells remain visible as the uncomputed region.

**Routing.** Matrix position expresses permitted access; there are no arrows. The source does not place row/column axis labels on the artwork, so its orientation must be read from the surrounding explanation.

**Information layers:** query block; key/context block; lookback extent; current computation; lookahead extent; excluded context.

**Detail devices:** fixed-size cell lattice; four shades for temporal role; visible unselected cells; local legend.

**Density assessment.** Low decorative complexity and high operator clarity; it works best as a detail panel linked to a streaming architecture.

**Color evidence:**

- nearer past block: `#F4D3BE`; render_sampled.
- older past block: `#F6EBE4`; render_sampled.
- current block: `#F7B487`; render_sampled.
- future block: `#E6BEA2`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Small bold sans-serif legend text; raster source.

**Geometry and strokes.** Selected region 50.4 × 54.7 mm; aspect 0.92. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The compact band is easier to compare than a fan-out of access arrows.
- Past and future colors are very similar; text labels and explicit axes are needed for reliable decoding.
- The source provides a concrete access pattern but not timing measurements.

**Transferable rules:**

- Represent dense access patterns as a matrix with explicit query and context axes.
- Show unselected cells and label the receptive-field limits.
- Use distinct labels or patterns for past/current/future if a single-hue palette is retained.

**Do not copy blindly:**

- Do not omit matrix axis semantics in the new figure.
- Do not infer runtime, latency or a causal training mask directly from this inference access schematic.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="wan-animate"></a>
### Wan-Animate: Unified Character Animation and Replacement with Holistic Replication

**Alibaba / Qwen · original year 2025 · 2509.14055v1 · first submission 2025-09-17**

[Primary PDF](https://arxiv.org/pdf/2509.14055v1) · [Version metadata](https://arxiv.org/abs/2509.14055v1)

PDF title page explicitly credits HumanAIGC Team, Tongyi Lab, Alibaba.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `2b237bad3f0953f8bdef45ab3d53da1a3a8e7da8745368a428e987d72353d0a5`

#### Figure 2, PDF p4: Unified animation/replacement representation with distinct body, face and relighting controls

**Family:** multi-control latent architecture. **Crop:** [108, 79, 504, 212] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A left visual-input territory shows references, temporal frames and environmental/target regions becoming four latent types. A compact control lane below holds body and face adapters. A central latent column exposes masking, concatenation and addition. A wider transformer region shows repeated DiT blocks, periodic face blocks and an optional relighting tier, followed by output.

**Routing.** Mask, reference, temporal and environment latents concatenate at C; body control enters at an addition node. Face features bypass that junction and route directly into the periodic face blocks. Optional LoRA is a distinct upper subregion. The different endpoints are the main scientific message.

**Information layers:** visual condition types; latent role and mask state; body versus face control; concatenation versus addition; periodic face-block injection; optional relighting adaptation; output video.

**Detail devices:** four color-coded latent families; binary mask strip; C and plus junctions; actual body-pose and face examples; periodic face blocks; optional module tier; frozen VAE symbols.

**Density assessment.** High and purposeful. Many independent controls are readable because the latent column is a central staging area and each condition has an explicit destination.

**Color evidence:**

- reference latent: `#70AD47`; vector_measured; alpha 1.0000.
- temporal latent: `#ED7D31`; vector_measured; alpha 1.0000.
- environment latent: `#FFE699`; vector_measured; alpha 1.0000.
- target latent: `#A5A5A5`; vector_measured; alpha 1.0000.
- VAE and face-control representation: `#8FAADC`; vector_measured; alpha 1.0000.
- face blocks: `#B4C7E7`; vector_measured; alpha 1.0000.
- optional relighting LoRA: `#E2F0D9`; vector_measured; alpha 1.0000.

**Typography:**

- main headings: MicrosoftYaHei-Bold at 6.00 pt (visible_pdf_text_measured).
- labels: MicrosoftYaHei at 6.00 pt (visible_pdf_text_measured).
- module labels: TimesNewRomanPSMT at 6.00 pt (visible_pdf_text_measured).
- smaller labels: MicrosoftYaHei at 5.14 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 139.7 × 46.9 mm; aspect 2.98. Most frequent trusted native widths: 0.8572, 0.6429 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- Color tracks data roles through input and latent regions; operation modules remain mostly neutral.
- Body and face controls are not merged into a generic conditioning arrow, preserving the actual distinction.
- The optional LoRA lane sits above the main stack, giving optionality a spatial and border cue.

**Transferable rules:**

- Let color follow data identity through representation changes, and use labels to announce those changes.
- Draw concatenation, addition and attention as distinct operations with explicit endpoints.
- Show periodic injection using repeated named blocks and a stated interval.
- Treat optional adaptation as an optional subregion, not part of the mandatory main path.

**Do not copy blindly:**

- Do not confuse the blue face feature strip with a generic video latent just because both are blue.
- Do not reproduce the 5.1 pt detail labels or imply a precise layer count from an ellipsis.

Evidence status: 47 nominally visible text traces; 0 invisible traces; 30 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 3, PDF p6: Frame-wise face latent compression and attention tensor expansion

**Family:** temporal adapter and attention geometry. **Crop:** [140, 79, 465, 205] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Three linked territories explain the adapter: face encoding and temporal compression at left, a narrow attention insertion block in the middle, and a tensor-level attention expansion at right. The middle block is deliberately narrow so the two representations receive most of the space.

**Routing.** Compressed face features feed K and V of the middle attention block; Q comes from the main transformer stream. The right callout shows noisy-latent frame tokens meeting face-feature rows in a rectangular attention map.

**Information layers:** per-frame face input; implicit latent sequence; causal temporal alignment; Q/K/V injection roles; frame-wise attention tensor shape.

**Detail devices:** latent strip indexed by position; causal-convolution windows; compressed feature stacks; explicit Q/K/V ports; tensor-shape labels; large attention map callout.

**Density assessment.** High detail in a compact three-part layout. The figure explains how temporal alignment and attention fit together, rather than merely saying face adapter.

**Color evidence:**

- face encoder and region border: `#B4C7E7`; render_sampled.
- frame-wise face latent strip: `#8FAADC`; render_sampled.
- causal temporal compression: `#FFF2CC`; render_sampled.
- face-attention field: `#E2F0D9`; render_sampled.
- compressed frame features: `#9DC3E6`; render_sampled.
- operator expansion boundary: `#F4B183`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Bold sans-serif region headings, serif module labels and mathematical tensor shapes; embedded raster, exact family and point size unknown.

**Geometry and strokes.** Selected region 114.7 × 44.5 mm; aspect 2.58. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The temporal strip and attention matrix expose two different representation geometries.
- The narrow central operator is the link between them; its inputs must remain legible.
- Color is carried from temporal feature stacks into the attention rows, providing continuity.

**Transferable rules:**

- Expand an adapter into both its sequence transformation and its operator-level interaction.
- Preserve feature identity between strip, Q/K/V port and attention axis.
- Write tensor dimensions adjacent to the matrix they describe.

**Do not copy blindly:**

- Do not identify an exact native font from the raster.
- Do not turn a schematic attention map into an empirical weight visualization; state whether cells represent access or values.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="wan-animate2"></a>
### Wan-Animate-2: Pushing the Application Boundaries of Character Animation

**Alibaba / Qwen · original year 2026 · 2608.06009v1 · first submission 2026-08-06**

[Primary PDF](https://arxiv.org/pdf/2608.06009v1) · [Version metadata](https://arxiv.org/abs/2608.06009v1)

PDF title page explicitly lists Tongyi Lab, Alibaba Group.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision.

PDF SHA-256: `595ed69e29bd4a587f445a864e835a0aa74b25a9f62fae0716c08a62d60d586f`

#### Figure 1, PDF p5: Dual-branch video model linked to spatiotemporal token geometry and sparse reference attention

**Family:** overview plus representation plus operator. **Crop:** [70, 59, 543, 372.2] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** The left half is a complete top-to-bottom video architecture with a dual-branch DiT expanded in place. The right half is divided into two stacked explanations: a spatiotemporal token cuboid with T/H/W dimensions, and a sparse-reference Q×K/V access matrix. A strong vertical divider and a horizontal right-panel divider make the three explanatory scales explicit.

**Routing.** Reference and latent branches preserve separate Q/K/V tracks until sparse reference attention. Dashed time-conditioning routes and shared-weight links are labeled. The representation panel shows how denoising and reference tokens are arranged; the matrix then shows the permitted interaction pattern, including dense within-video and sparse matched reference windows.

**Information layers:** target/reference image/reference video roles; dual-branch DiT computation; training-state and shared-weight status; time-aligned spatiotemporal positions; token-family identity; query/key-value window indexing; sparse versus computed attention.

**Detail devices:** actual reference and target frame stacks; expanded Q/K/V tracks; frozen/trainable symbols; T/H/W dimension arrows; colored token cuboids; window identifiers on matrix axes; explicit computed/uncomputed legend; overview/detail matched labels.

**Density assessment.** Very high and strongly layered: the reader can understand the system, then the representation, then the operator. This is one of the strongest sources for the requested level of sophistication, although small operator labels still need a larger or vector redraw in new work.

**Color evidence:**

- DiT container: `#DAE3F3`; render_sampled.
- reference-video tokens and common operations: `#9DC3E6`; render_sampled.
- denoising-video tokens: `#FFE699`; render_sampled.
- reference-image token: `#A9D18E`; render_sampled.
- computed attention cells: `#97D34F`; render_sampled.
- time-alignment label: `#C5E0B4`; render_sampled.
- sparse-attention label: `#FFF2CC`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Mixed serif model/operator labels, italic math and bold sans-serif panel headings; the PDF stores the entire figure as one raster, so exact fonts and sizes cannot be recovered.

**Geometry and strokes.** Selected region 166.9 × 110.5 mm; aspect 1.51. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The three panels answer different questions and do not simply repeat the same block diagram.
- Object labels and panel structure link the representation to the operator, but color semantics are locally scoped: green denotes a reference-image token above and computed attention below, and both ordinary/reference x labels are yellow in the matrix. Use explicit local legends rather than assuming a universal cross-panel color identity.
- The large attention matrix has named axes and explicit white uncomputed cells, making the sparse pattern auditable.
- The left overview occupies a little over half the selected crop width (visual estimate), while the right region splits into two mechanisms. Each view uses a different geometry; this is not evidence for a universal overview/detail width ratio.

**Transferable rules:**

- Build a rich method figure at three scales: system overview, representation layout, and exact operator pattern.
- Carry token identity consistently across every scale.
- Let each panel use the spatial grammar its concept requires rather than forcing equal cards.
- Make matrices explicit about Q versus K/V, window identity and computed versus uncomputed cells.
- Keep the overall hierarchy strong enough that readers can stop after the overview or continue into the detail.

**Do not copy blindly:**

- Do not assume dense visual detail is evidence of superior model quality.
- Do not preserve tiny text or raster typography when an editable vector redraw is possible.
- Do not treat the schematic cuboid counts or matrix cells as measured token quantities without the stated mapping.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 2, PDF p7: Streaming animation with static shared conditions and recycled generated context

**Family:** stateful chunked inference. **Crop:** [70, 59, 543, 247.8] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A single wide Causal DiT band separates an upper output stream from a lower input stream. A narrow green dashed shared-input region on the left holds reference image and noise. Each inference step aligns a driving chunk below with its generated result above, and previous generated results reappear between later input chunks.

**Routing.** Vertical arrows connect each input chunk to the model and each result to the output lane. Dashed diagonal return arrows carry the previous generated result into the next input state; solid diagonal arrows then feed that state to the next model step. Stream arrows establish left-to-right time.

**Information layers:** static shared conditions; driving chunk sequence; generated output sequence; recycled previous-result state; shared causal model; iteration order.

**Detail devices:** distinct input/output lanes; static-condition box; same generated image repeated as later context; dashed feedback route; aligned chunk/result indices; explicit stream direction.

**Density assessment.** High explanatory value with moderate clutter. It captures stateful autoregression in a way a plain repeated-model chain cannot.

**Color evidence:**

- shared causal model: `#DAE3F3`; render_sampled.
- shared-input boundary: `#A9D18E`; render_sampled.
- media: Repeated driving-video and generated-video frame stacks remain visually distinct by their content, not by artificial tinting. (raster_observed).

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Serif stream labels and frame labels, italic shared-input heading; embedded raster, exact typeface/point size unknown.

**Geometry and strokes.** Selected region 166.9 × 66.6 mm; aspect 2.51. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The repeated image is meaningful state, not redundant illustration.
- The single spanning model band emphasizes weight sharing across steps.
- The dashed feedback diagonal is visually distinct from the direct vertical compute route; a new figure should name the carried state and cache horizon explicitly.

**Transferable rules:**

- Separate static conditions, current input, previous state and output in a streaming figure.
- Show the previous result twice when it truly becomes input context, and connect the two appearances.
- Use one shared model band when computation is repeated with the same weights.
- Add chunk duration, cache length and latency axes when those quantities are part of the claim.

**Do not copy blindly:**

- Do not treat schematic frame-stack thickness as a measured chunk length.
- Do not imply that noise is necessarily unchanged at every step solely from its placement in the shared-input region; verify the algorithm.
- Do not route a dashed return into empty space—name the state object and endpoint.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

<a id="qwen3-asr"></a>
### Qwen3-ASR Technical Report

**Alibaba / Qwen · original year 2026 · 2601.21337v1 · first submission 2026-01-29**

[Primary PDF](https://arxiv.org/pdf/2601.21337v1) · [Version metadata](https://arxiv.org/abs/2601.21337v1)

PDF title page credits Qwen Team and links the official repository; the repository description explicitly identifies the Qwen team at Alibaba Cloud.

First-submission year and inspected revision year are separate fields; this study deliberately pins v1 and does not silently substitute a later revision. arXiv v1 submission is 2026-01-29; the PDF title-page dateline is 2026-01-30. The presence of a later v2 does not change the inspected v1 identity.

PDF SHA-256: `757a83e38cbff00acb60667a03b53ae91b1f91f8900f84bf8c12f337be3fedd2`

[Official affiliation evidence](https://github.com/QwenLM/Qwen3-ASR)

#### Figure 2, PDF p3: Audio-encoder internals paired with a contextual ASR model overview

**Family:** component plus system architecture. **Crop:** [70, 69, 526, 241] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** A narrow left panel expands AuT into encoder and decoder stacks with multiplicities and rate labels. A wider right panel shows the ASR system receiving contextual entities, pretrained audio features and text tokens. Output tokens and the transcript align above the Qwen3 LM.

**Routing.** The left decoder cross-attention receives encoded audio while the tokenizer supplies text input. In the system overview, three typed input routes enter the LM separately. Output format examples tie the model to language identification and recognized text.

**Information layers:** audio frontend and hidden-state rates; encoder/decoder layer multiplicity; contextual entity input; pretrained audio encoder reuse; text token input/output; ASR output format.

**Detail devices:** waveform and filterbank token strip; 32×/3×/8× multiplicity labels; 100 Hz versus 12.5 Hz annotations; entity database with examples; actual transcript snippets; matched component identity between panels.

**Density assessment.** Moderately high and coherent. Most model text is legible in a full-width figure, but tiny entity examples around 3.7 pt should be simplified or moved to a caption.

**Color evidence:**

- model blocks: `#D9D9D9`; vector_measured; alpha 1.0000.
- acoustic filterbank tokens: `#FFD966`; vector_measured; alpha 1.0000.
- audio hidden states: `#F5DFD4`; vector_measured; alpha 1.0000.
- text tokens: `#AAE8E3`; vector_measured; alpha 1.0000.
- entity-context tokens: `#DEEBF7`; vector_measured; alpha 1.0000.
- model and text accent: `#5A44CA`; visible_text_color_measured; alpha 1.0000.

**Typography:**

- ordinary labels: Futura-MediumItalic at 5.74 pt (visible_pdf_text_measured).
- major module labels: Futura-MediumItalic at 8.21 pt (visible_pdf_text_measured).
- smaller entity examples: Futura-MediumItalic at 3.72 pt (visible_pdf_text_measured).

**Geometry and strokes.** Selected region 160.9 × 60.7 mm; aspect 2.65. Most frequent trusted native widths: 1.0285, 0.4114, 0.4628, 0.5142, 0.3085, 0.2057 pt. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The component panel is more detailed than the system panel because it teaches the reused encoder.
- Token color and row position distinguish acoustic, context and text objects.
- The source uses italic geometric lettering throughout; this is a local design choice, not a universal Qwen house style.

**Transferable rules:**

- Pair a reusable component expansion with a compressed system view.
- Label sampling or token rates at the exact representation boundary.
- Include short realistic context and transcript examples to clarify model inputs.
- Keep multiplicities explicit instead of drawing dozens of layers.

**Do not copy blindly:**

- Do not reproduce the tiny entity list or use italics for long prose by default.
- Do not silently conflate the audio encoder training configuration with the final ASR inference graph.

Evidence status: 54 nominally visible text traces; 0 invisible traces; 0 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.

#### Figure 3, PDF p6: Forced alignment with dynamic timestamp slots and synchronous supervision

**Family:** token-level training mechanism. **Crop:** [132, 69, 465, 292] PDF pt, top-left origin. **Inspection:** rendered at 216 dpi and visually checked.

**Composition and layout.** Two lower branches encode speech and text. A local two-row slot-insertion example sits above the text tokenizer. The concatenated sequence then passes through the LM and a timestamp-prediction layer. At the top, labels and outputs align cell-for-cell with a synchronous brace and a loss bracket over the supervised subset.

**Routing.** The two modality branches merge only at the LM. The slot-insertion inset demonstrates the actual sequence edit before model input. A straight vertical route connects output slots to the aligned target row; the loss bracket limits where the objective applies.

**Information layers:** speech encoding; text tokenization; dynamic insertion of timestamp slots; masked versus unmasked slots; combined model input; timestamp output head; synchronous targets and selective loss; concrete word/timestamp example.

**Detail devices:** paired label/output rows; dashed masked-slot borders; slot insertion before/after rows; supervision brace; loss bracket over selected positions; literal short sentence and time intervals; full token-type legend.

**Density assessment.** High mechanism density with clear vertical hierarchy. The sequence-level example makes training alignment inspectable; this is much richer than a generic audio→LLM→timestamps pipeline.

**Color evidence:**

- speech tokens: `#F7E6DE`; render_sampled.
- text tokens: `#9084D8`; render_sampled.
- timestamp slots: `#D4C6F8`; render_sampled.
- selected label slots: `#C9B7FA`; render_sampled.
- inactive label slots: `#DEDBF3`; render_sampled.
- timestamp prediction layer: `#FEFED9`; render_sampled.
- model text accent: `#5B45CA`; render_sampled.

**Typography:**

- diagram lettering: Exact visible font family not recoverable from this PDF crop (visual_estimate). Geometric italic sans-serif module labels, bold italic legend and supervision labels; embedded raster, exact visible family and source point sizes unknown.

**Geometry and strokes.** Selected region 117.5 × 78.7 mm; aspect 1.49. No trusted native stroke-width recovery for this crop. Flagged raw-width paths: 0. Region dimensions describe the manually chosen crop, not automatically segmented artwork.

**Composition observations:**

- The slot grid exposes the model objective as well as the architecture.
- Dashed outlines distinguish masking independently of the related purple shades.
- The phrase and its timestamps at the bottom give meaning to every abstract cell above.

**Transferable rules:**

- For token-level objectives, draw aligned inputs, outputs and labels and show exactly which positions receive loss.
- Use an actual short sequence to illustrate masking or slot insertion.
- Encode masked state with a border pattern as well as color.
- Keep the sequence edit separate from the model block so the mechanism is visible.

**Do not copy blindly:**

- Do not assume row alignment implies ordinary next-token prediction; label synchronous or shifted supervision explicitly.
- Do not infer exact font metrics from a raster figure.
- Do not leave nearly identical pastel slot types without a label or pattern.

Evidence status: 0 nominally visible text traces; 0 invisible traces; 1 raster occurrences. Font and stroke measurements describe source placement, never a corporate house style or recommended production minimum.
