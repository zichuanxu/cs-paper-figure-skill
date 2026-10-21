# Color, typography, composition, and figure style

## Contents

1. [Choose a modern figure grammar](#1-start-from-a-specific-modern-figure-grammar)
2. [Build a complete color system](#2-use-a-complete-color-system)
3. [Define typography hierarchy](#3-treat-typography-as-hierarchy-not-a-font-name)
4. [Compose with a grid and proportions](#4-compose-with-a-visible-grid-and-intentional-proportions)
5. [Define shapes and line styles](#5-define-a-shape-and-line-grammar)
6. [Design arrow routing](#6-design-arrows-as-part-of-the-layout)
7. [Author charts deliberately](#7-make-charts-look-authored)
8. [Review against a visual target](#8-review-against-a-concrete-visual-target)

## 1. Start from a specific modern figure grammar

Prioritize the 2025–2026 studies across [recent-paper-atlas.md](recent-paper-atlas.md) and [modern-paper-atlas.md](modern-paper-atlas.md). Keep [paper-atlas.md](paper-atlas.md) as the foundational collection. Select complementary examples by reader task using [reference-selection.md](reference-selection.md), inspect their actual figure regions, and adapt a relevant [style recipe](style-recipes.md). A lab name is not a style specification.

A strong figure can be visually rich. Achieve that richness through typed objects, intentional contrast, meaningful grouping, data/token miniatures, spatial rhythm, and a clear reading order. Give the novel operation enough space and visual specificity that the diagram could not be mistaken for an arbitrary pipeline.

Use the following figure grammars as candidates, then choose the one matching the content:

| Grammar | Good source anchors | Composition and visual vocabulary |
| --- | --- | --- |
| Overview plus mechanism expansion | Qwen3.8-Next Fig. 1; Engram Fig. 1; DeepSeek-V4 Figs. 2–3 | Narrow backbone, larger detail region, shared module colors, repeated token/weight tiles, explicit operators, a quiet link between overview and detail |
| Nested agent system | Harness² Fig. 2 | Semantic outer containers, white component cards, stronger category headings, mono file/schema labels, typed ports, frequency pills only when the frequency is known |
| Two-level recursion storyboard | Harness² Fig. 3 | Task-level lane, within-task substeps, a separate outer loop, consistent agent/artifact symbols, temporal numbering or scope labels |
| Parallel multimodal lanes | Cosmos 3 Fig. 5; HunyuanVideo 1.5 Fig. 2 | Aligned modality paths, consistent token strips, a shared operation spanning lanes, separate output heads, mask/conditioning inset when scientifically useful |
| Analytical small multiples | Qwen3.8-Next Figs. 5–6; Gemini 2.5 Fig. 4 | Aligned axes, one shared encoding key, controlled color/marker pairs, local numeric annotations, consistent plotting area proportions |
| Evidence storyboard or matched grid | OpenAI Monitoring Fig. 1; CoT-Control Fig. 2; V-JEPA 2.1 Fig. 1 | Fixed reading schema, aligned comparable examples, local emphasis, concrete data, short excerpts or matched crops with selection rules |
| Algorithm linked to code | AlphaEvolve Fig. 2 | Semantic colors repeated in modules and code identifiers, human setup separated from the automatic loop, bounded system group |
| Registered architecture comparison | mHC Fig. 1; Circuit Tracing methods diagram | Fixed unchanged landmarks, complexity-proportional panels, local emphasis on actual changes |
| Mechanism storyboard | HY-World 2.0 Fig. 2 | Equal tall stage cards containing different meaningful artifacts, aligned model footers, open route gutters |
| Task-by-model analytical matrix | Perception Encoder Fig. 8 | Repeated axes and reference lines, task-group labels, direct best-layer annotations instead of overlapping multi-model radar polygons |

Do not apply every visual device at once. Make at least three decisions explicit: the dominant reading direction, the main emphasis, and which shapes mean computation versus data or state.

## 2. Use a complete color system

Assign color to scientific roles before selecting individual hex values. For each role choose a **dark ink/outline**, a **pale fill**, and, if needed, a **mark color**. A single hue pasted onto every rectangle is not a color system.

A useful adapted system, with measured source pairs and clearly marked adaptations, is stored in [design-tokens.json](../assets/design-tokens.json):

| Role | Ink / outline | Fill | Evidence |
| --- | --- | --- | --- |
| Context | `#2F5597` | `#E3EBF6` | Harness² Fig. 2, vector measured |
| Compute / middleware | `#7B5FB5` | `#F1ECF8` | Harness² Fig. 2, vector measured; assign to the matching role in a new system |
| Memory / tools | `#4F7D58` | `#E9F0E7` | Harness² Fig. 2 measured tool pair; memory mapping is an adaptation |
| Orchestration | `#A5637E` | `#F6EDF1` | Harness² Fig. 2, vector measured |
| Update | `#AD6A30` | `#FFF0DE` | Original adapted amber recommendation |

For token-based architectures, source palettes include Qwen3-VL-Embedding's lavender text (`#C8C7F5`), teal vision (`#A2DCDE`), peach weights (`#F5DDBF`), and gray hidden states (`#9A9A9A`). DeepSeek-V4 Fig. 3 distinguishes green queries from yellow key/value tokens. Select the subset that actually exists in the method. Do not use a token color merely because it is attractive.

For empirical plots, Qwen3.8-Next Fig. 6 provides a measured four-series palette: blue `#2563A6`, amber `#D97706`, purple `#7A5195`, green `#4C8C5A`. Pair colors with `o`, `^`, `s`, `D` markers and, where useful, line patterns. Keep one method's identity stable across the entire paper.

Practical recommendations:

- Begin with two to four semantic color families plus neutral text/structure. Add another only when the figure's content requires it.
- Let pale fields define groups; keep nested cards white or a distinct lower-intensity tone. Use dark labels on pale fills.
- Use a stronger accent on the novel mechanism or focal contrast. Keep baselines sufficiently visible to support fair comparison.
- Bind repeated scientific roles across representations: an algorithm component and its code identifier, or a modality and its tokens/encoder/output, should retain identity. Define whether color means modality, novelty, method, or state; do not silently switch its meaning between panels.
- Use a sequential map for ordered magnitude, a diverging map for a meaningful midpoint, and a categorical map for unordered classes. Missing values need their own explicit state.
- Keep quantitative colors and image transforms faithful to the data. V-JEPA's PCA-to-RGB maps are an encoding, not a palette to restyle.
- Use gradients only when they express a defined quantity, continuity, depth, or another necessary distinction. Use translucency when it communicates stacking or scope; do not confuse overlapping transparent fills with measured new categories.
- Check grayscale and available color-vision simulations. Palette selection alone cannot certify accessibility. Dark outlined marks, direct labels, and shape distinctions are useful safeguards.
- Default to a white paper background. A dark treatment, as in Gemini 2.5 Fig. 1, requires deliberate print and contrast checks; derive a light version when the final use demands one.

## 3. Treat typography as hierarchy, not a font name

Choose the font system after the physical dimensions. Source figures use a wide range of families: visible Calibri in DeepSeek-V4 architecture figures; Helvetica and LiberationSans in Qwen3.8-Next; XCharter with Computer Modern math in Cosmos 3; Latin Modern Sans in V-JEPA 2; Futura and Aptos in other modern sources. Harness² Fig. 3 even uses Comic Sans MS internally. These are source observations, not a universal prescription.

The shape, weight, size, line spacing, and placement of each text role matter together:

| Role | Recommended starting size at final output | Treatment |
| --- | --- | --- |
| Panel letter + short heading | 9–10 pt | Real bold or semibold, aligned to the panel grid |
| Group/module heading | 8.3–9 pt | Weight contrast; dark role ink where useful |
| Main labels and axis titles | 7.5–8.3 pt | Regular, short, stable terminology |
| Tick/edge/secondary labels | 7–7.5 pt | Regular, sufficiently dark; no cosmetic low contrast |
| File names, literal schema/code | 7–8 pt | Compatible monospace, only where literal identity matters |
| Equations and symbols | Optically matched | Compatible math face; do not make symbols conspicuously smaller |

These are skill recommendations, not source measurements or venue rules. The actual manuscript template overrides them. Some inspected source figures have 3–6 pt labels; preserve their hierarchy while enlarging or simplifying the content.

Use one main family and at most one functional companion (math or monospace). Portable starting choices are Nimbus Sans/Liberation Sans/DejaVu Sans for a technical diagram, or STIXGeneral/Nimbus Roman/Latin Modern Roman for a serif mathematical figure. State any font substitution. Do not claim a proprietary face is embedded when it is unavailable.

- Use real bold/italic weights. Define exactly which roles receive each weight.
- Use sentence case for descriptive text; preserve actual acronyms, symbols and filenames.
- Prefer two short lines over a long compressed line. Reserve enough line height and vertical padding for ascenders/descenders.
- Align text baselines in repeated modules and control label wrapping consistently.
- Derive final size from placement: `final_pt = source_pt × final_width / source_width`. An 8 pt label at 178 mm becomes 3.8 pt at 85 mm. Recompose before accepting such shrinkage.
- Record font evidence correctly. Visible text spans can support a measured family/size; an invisible searchable overlay is weaker evidence; raster appearances do not identify fonts. See [design-extraction.md](design-extraction.md).
- Check font-program compatibility with the exporter. For Matplotlib Type 42 PDF output, use compatible TrueType programs and inspect the actual PDF; a font being embedded does not guarantee its file format was declared correctly. A native SVG's declared family may differ from the local preview's fallback.

## 4. Compose with a visible grid and intentional proportions

Set the final width from the manuscript. When unavailable, 85 mm and 178 mm are adjustable defaults. Choose height from the content rather than forcing a fixed aspect ratio.

Start with a 2 mm spacing unit. At 178 mm, an outer margin of 2.5–4 mm, panel gutters of 3.5–6 mm, group padding of 2–3 mm, and child-card gaps of 1.5–2.5 mm are practical recommendations. Check the actual labels and edge routes before accepting any default.

Use a small number of aligned axes: shared left edges, repeated module centers, aligned row baselines, and consistent input/output ports. Give additional width to information-rich blocks. Equal rectangles are appropriate only when the scientific objects are genuinely parallel.

| Layout | Adaptable starting ratio | Use |
| --- | --- | --- |
| Backbone + mechanism | 30:70 to 40:60 | A narrow system context plus expanded new operation |
| Overview + detail | 55:45 or 60:40 | Similar importance, different information density |
| Matched alternatives | 50:50 | Controlled comparison of architecture or stage |
| Main finding + support | Full-width top + 2–3 lower panels | One central result with separate explanatory views |
| Runtime + persistent state | Upper runtime lane + lower state/update lane | Different lifetimes or control scopes |

Ratios are design starting points, not measurements of all cited papers. The atlas separately records exact source geometry where measured.

Avoid dead space created by placing tiny boxes far apart. Use the space for a relevant mechanism expansion, concrete record/token example, or wider readable labels. Conversely, do not fill every gap with a border, icon, or explanatory sentence. Keep space for decoding and routing.

## 5. Define a shape and line grammar

Use shape differences to distinguish kinds of objects. Keep repeated objects identical unless a difference carries information.

| Meaning | Suitable form | Detail that makes it specific |
| --- | --- | --- |
| Computation | Rectangle or softly rounded module | Operator name, I/O role, repetition count when known |
| Literal artifact/data | Folded-corner document or token strip | Actual field/token label, a small valid example |
| Persistent state | Record stack/store container | Schema, read/write ports, provenance or version field |
| Group/scope | Pale enclosing region | Scope title, shared semantic role, real boundary |
| Selection/addition/concatenation | Explicit junction/operator | Typed inputs and output, symbol explained |
| Repetition | Stack or bracket | Known multiplicity or clearly schematic repetition |

Semantic icons, colored containers, nested cards, small badges, and local insets are permitted when they explain a role, scope, status, frequency, or mechanism. The first version's blanket aversion to these devices was too restrictive. Use vector icons with consistent stroke and size; keep text labels so icons are not the sole decoding path. Avoid company logos as a substitute for labels.

Use an observable stroke hierarchy. Adaptable final-size recommendations: group borders 0.65–0.8 pt; module outlines 0.8–1.0 pt; focus outlines 1.1–1.35 pt; data connectors 0.95–1.2 pt; guides 0.4–0.55 pt. Source Harness² Fig. 2 uses outer 0.764 pt, inner 0.573 pt, hub 1.147 pt—an example of hierarchy, not compulsory constants.

Corner radii should be coherent: roughly 0.8–1.3 mm for modules and 1.5–2 mm for groups at 178 mm width. Do not use a rounded-card treatment for every mathematical operator or data mark.

## 6. Design arrows as part of the layout

Allocate routing corridors before placing nodes. Use explicit source/target ports; leave each source outward and enter each target normally. Give a return path enough space to be visibly separate from the forward path. Never let a path ride along a node border.

Start with 4–7 mm for an outside feedback corridor, 2.5–4 mm between parallel routes, and 1.2–2 mm between a label and the connector it describes. These are recommendations in final-size units; fit the actual text. An arrow label should be adjacent to its route without obscuring it.

Use different line styles or colors only for defined edge semantics. Add direction with an arrowhead. Mark an actual junction explicitly; an unmarked crossing must not look like a connection. The full routing contract and checker are in [diagram-routing.md](diagram-routing.md).

## 7. Make charts look authored

- Decide which comparison is primary; select direct labels, a shared key, or aligned legends deliberately.
- Match plotting areas across small multiples. Choose aspect ratios for the expected slopes and label density.
- Set axis/guide/text/data stroke levels separately. Use enough grid to support lookup without making a gray mesh.
- Show key observations with markers and uncertainty with a subordinate but visible band or interval. Define the interval.
- Use derived endpoint labels, a measured difference, a known threshold, or an intervention annotation when it explains the result. Keep labels off data and outside shaded uncertainty where possible.
- Keep reference methods legible. Emphasis must not hide unfavorable comparisons.
- Avoid manually typed numeric callouts that can diverge from the data. Generate them from source values.
- Do not make every benchmark a different color if the same conditions are being compared. Faceting and consistent roles often work better.

## 8. Review against a concrete visual target

Before approving a substantial figure, compare the actual output with the selected references at similar physical width. Ask:

1. Is the new operation recognizable within a few seconds?
2. Are computation, state, inputs, and outputs distinguishable by more than color?
3. Is there a clear hierarchy among panel headings, modules, labels, and annotations?
4. Is the whitespace intentional, with enough room for edges and labels?
5. Does a representative mechanism/data detail replace a generic empty box?
6. Does every connector have an unambiguous origin, destination, direction, and meaning?
7. Does the composition survive final-size and grayscale inspection?

A passed font/dimension check is not an aesthetic review. If the result remains a generic set of equal rectangles, revisit grouping and mechanism specificity before adding more colors. If it becomes cluttered, simplify or split the composition while preserving the important structure.
