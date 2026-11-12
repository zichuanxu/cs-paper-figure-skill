# Venue study, 2026-11: 29 award papers across four venue families

The earlier studies in this skill read technical reports from AI labs. This one reads award and oral papers
from peer-reviewed venues, including three families the skill had never looked at (systems, graphics, HCI).
About 90 figures were opened as crops from the PDFs and measured: fonts and sizes from live vector text,
strokes and fills from the drawing commands, white/tint/ink shares from renders. The rules that came out
of it are in [visual-craft.md](visual-craft.md) and [registers.md](registers.md); this file is the evidence.

Read it when a rule in those files looks wrong for the figure in hand and you need to know where the rule
came from, or when you want a model figure for a family.

## Papers

Status was confirmed on the venue's own page unless marked †, where only an author-institution page was
reachable.

| Lane | Paper | Venue, status | Figures read |
| --- | --- | --- | --- |
| ML | 1000 Layer Networks for Self-Supervised RL (arXiv 2503.14858) | NeurIPS 2025 Best Paper | 1, 2, 5–6 |
| ML | Why Diffusion Models Don't Memorize (2505.17638) | NeurIPS 2025 Best Paper | 1, 3 |
| ML | Superposition Yields Robust Neural Scaling (2505.10465) | NeurIPS 2025 Runner-up | 1, 2, 5 |
| ML | Does RL Really Incentivize Reasoning Capacity… (2504.13837) | NeurIPS 2025 Runner-up | 1, 2 |
| ML | LLMs Get Lost In Multi-Turn Conversation (2505.06120) | ICLR 2026 Outstanding Paper | 1, 3 |
| ML | The Polar Express (2505.16932) | ICLR 2026 Honorable Mention | 2, 3 |
| ML | The Flexibility Trap (2601.15165) | ICML 2026 Outstanding Paper | 1, 2, 4, 5 |
| Vision | D4RT (2512.08924) | CVPR 2026 Best Paper | 1–4, 6 |
| Vision | TRELLIS.2 (2512.14692) | CVPR 2026 Best Student Paper | 1–3, 6 |
| Vision | VGGT (2503.11651) | CVPR 2025 Best Paper | 1–3 |
| Vision | BrickGPT (2505.05469) | ICCV 2025 Best Paper | 1, 3–5 |
| Vision | FlowEdit (2412.08629) | ICCV 2025 Best Student Paper | 1, 2, 6, 7 |
| Graphics | Shape Space Spectra (2408.10099) | SIGGRAPH 2025 Best Paper | 1, 7, 8, 13 |
| Graphics | Implicit Minimal Surfaces for Bijective Correspondences (2605.02770) | SIGGRAPH 2026 Honorable Mention | 1–3, 6, 8, 27, 28 |
| NLP | HALoGEN (2501.08292) | ACL 2025 Outstanding Paper | 1, 2 |
| NLP | Measuring CoT Faithfulness by Unlearning Reasoning Steps (2502.14829) | EMNLP 2025 Outstanding Paper | 1, 3, 4 |
| NLP | The BiGGen Bench (2406.05761) | NAACL 2025 Best Paper | 1–3 |
| NLP | REL-A.I. (2407.07950) | NAACL 2025 Best Paper Runner-up | 1–3 |
| HCI | Cocoa (2412.10999) | CHI 2026 Best Paper † | 1–3, 8, 9 |
| HCI | Fostering Appropriate Reliance on LLMs (2502.08554) | CHI 2025 Honorable Mention † | 1, 4, 5 |
| HCI | DocWrangler (2504.14764) | UIST 2025 Honorable Mention | 1, 2, 5, 7 |
| HCI | WeAudit (2501.01397) | CSCW 2025 Best Paper † | 7 |
| Systems | CortenMM | SOSP 2025 Best Paper | 3, 6, 7, 14, 19 |
| Systems | Attack of the Bubbles (PipeMorph) | NSDI '26 Outstanding Paper | 1, 5, 13, 16 |
| Systems | NDD: A Decision Diagram for Network Verification | NSDI '25 Outstanding Paper | 2, 4, 9–11 |
| Systems | OSCAR | NSDI '26 Outstanding Paper | 3–5, 10 |
| PL | Tree Borrows | PLDI 2025 Distinguished Paper | 1, examples |
| DB | AnyBlox | VLDB 2025 Best Research Paper † | 2, 4, 6 |
| Systems | Semisolates and Try | OSDI '26 Best Paper | 1–3 |

Not covered: SIGCOMM, ASPLOS, EuroSys, SIGMOD, POPL, USENIX Security, IEEE S&P, ECCV 2026, SIGGRAPH Asia.
An award does not make every figure good: each paper's weak figures are listed at the end and were used as
counter-examples.

## What was measured

Sizes are at print. "White" is the share of pixels with grey ≥ 250; "ink" is grey < 120.

| Quantity | Systems / PL / DB | Core ML | NLP / HCI | Vision / graphics |
| --- | --- | --- | --- | --- |
| Typical width | 84.7 mm column, 177.8 full | 140–174 mm, some 68–93 | 76 mm column, 155–178 full | 84 column, 176 full |
| White share | diagrams 53–96 %, charts 62–87 % | 41–89 %, median 71 % | 49–81 %, median 69 % | diagrams 54–70 %, pipelines 49–72 %, image grids 22–62 %, charts 85–92 % |
| Ink share | 2–8 % | 1.6–7.9 %, median 3.4 % | 1.2–3.2 % for screenshots | 2–7 % diagrams |
| Heads and titles | 5.6–8 pt, regular | 9.8–11.9 pt, regular in 6 of 7 papers | 8.3–9.3 pt | grid headers 8–9.5 pt regular |
| Labels | 5.0–7 pt | axis titles ≈ 10 pt, ticks 7.5–8.6 pt | example text 6.7–7.5, labels 6.1–7.1 | diagram text 4.9–5.8 (their weakest part) |
| Text that fails at print | 3.2–4.9 pt | 3.7–4.8 pt | 3.3–5.0 pt | 3.2 pt |
| Text colour | `#000000` in every figure | black unless naming a coloured thing | black in 5 of 8, dark grey in 2 | black in 6 of 7 |
| Diagram stroke | one weight per figure, 0.40–1.14 pt | 0.72–1.4 pt | 0.5–1.0 pt outlines | modules 0.7–0.95 pt |
| Chart line weight | 0.8–0.9 pt, equal for all series | 1.0–1.2 pt, equal for all series | — | — |
| Arrowhead length | 2.3–7 × stroke | 2.8–9 ×, typically 3–4.5 × | 4.5–5.7 × | 3.7–6 ×, median 4.5 × |
| Arrow styles per figure | 2–4, all defined | 1–2 (one figure has 4) | 1–3 | 1–3 (one has 5) |
| Meaningful hues | 1–4 | 1–4, typically 2 | 0–5 in the strong figures, 7–9 in the weak | 0–4 in the vector layer |
| Gutters | 3.0–4.7 mm shared-axis subplots, 8–9 mm otherwise, 2.5 mm between lanes | 6–10 mm between framed axes, 0.7–0.9 mm tick-free | 3.3–4.8 mm grid columns, 8–10 mm unframed panels | 0–1 mm within an image group, 1–3.6 mm between groups |
| Container padding | 0.4–1.5 mm | 1.4–3.5 mm | 1.5–2 mm | 1.5–2 mm |
| Outer margin | none: content spans 76–85 of 84.7 mm | 1.0–4.7 mm, never a frame | 0–2.6 mm | 1–2 mm |
| Corner radius | 0.4–1.2 mm | 0.4–0.6 labels, 1.4–1.5 nodes, 2.3–2.8 containers | 0.85–2.0 cards, 2.7 window | 0.55–1.2 chips, 1.4–1.8 boxes, 2.3–2.5 panels |
| Figures with any icon | 4 of 22 | 3 of 19 | 6 of 8 papers | 5 of 7 papers, sparse |
| Header bands, chart cards | 0 of 22 | 0 of 19 | 0 of 19 | 0 of 31 |
| Vector drop shadows | 0 | 1 (faint, on verdict discs) | only on floating windows and callouts | 0 |

Further measurements the rulebook cites:

- One stroke weight per diagram: 64 of 64 strokes at 0.50 pt (CortenMM 3), 265 of 266 at 0.61 pt (NDD 4),
  77 of 79 at 0.88 pt (AnyBlox 4), 28 of 30 at 0.98 pt (PipeMorph 13).
- Single-column Figure 1: CoT 1 is 76.2 × 72 mm with 9 boxes at 6.7–7.4 pt; REL-A.I. 1 is 75.3 × 41.8 mm
  at 6.5–8.1 pt. Systems column figures are 18–57 mm tall.
- Hero share: 80 % of the area (VGGT 1: 149 × 63 mm of 176 × 67), 75 % of the width (TRELLIS.2 1),
  55 % of the height (BiGGen 1).
- Economy: 2503.14858 Fig. 2 has seven bars, three distinct words and two multipliers.
- Arrows in few-arrow figures are heavier than the outlines: 1.0–2.5 pt in the NLP and HCI set, 1.5–2.0 pt
  for hero arrows in vision.
- Label to object: 0.25–1.5 mm across all four families. Figure to caption: 3.7–6.3 mm (NLP and HCI).
- Radii of isometric plates and large trays: 3.5–4.2 mm (vision).
- Field-chart subplots: 28.3 × 14.7 mm (CortenMM 14), 68.9 × 9.4 mm (CortenMM 19), 75.6 × 10.9 mm
  (PipeMorph 16), 48.3 × 16.1 mm (OSCAR 10), 30.7 × 28.6 mm (2504.13837 Fig. 2).

## What held in all four families

These are the design principles the rulebook now leads with.

1. **The hero is the thing that differs.** One red object among 84 black paths (CortenMM 3); the only solid
   line among five (CortenMM 14); the only unhatched bar (OSCAR 10); the block given 55 % of the height
   (BiGGen 1) or 80 % of the area (VGGT 1). No figure makes the hero by thickening its stroke, and in
   comparison grids ours is deliberately drawn like the baselines and marked by position and a bold header.
2. **Few of everything, and each one counted.** Strong figures hold to one or two stroke weights, two or
   three text sizes, at most four hues, at most three arrow styles, one icon family. The weak figures of the
   same papers are the ones that exceed these (9 hues in BiGGen 2, 7 typefaces in D4RT 2, two badge sizes in
   DocWrangler 5).
3. **One drawing repeated, one thing changed.** The same tree four times with different edges black
   (2504.13837 Fig. 1), the same six-token chain twice (Flexibility Trap 2), the same network before and
   after (CoT 1), the same page table in four steps (CortenMM 7), the same camera for six methods
   (TRELLIS.2 6). What is no longer live or was not taken is the same shape at about 20 % strength.
4. **One concrete example through every stage.** HALoGEN 1 is a 2-example × 4-stage grid with no arrows at
   all; CoT 1 follows one question; Tree Borrows carries one program from listing to tree.
5. **Colour names things, and the name is kept.** D4RT gives its four query fields four hues and repeats
   each as chip, wedge, timeline dot and mark on the render. IMS is purple = A and teal = B in every figure.
   PipeMorph uses the same four hues in its architecture figure and its bar charts. An ordered variable is
   one hue on a lightness ramp (five Blues for depth 4→64 in 2503.14858 Fig. 1).
6. **White space is grouped.** Shares run from 41 to 96 %, but in every strong figure the emptiness sits in
   gutters, bands between layers, a label row or a legend strip. Scattered holes appear only in the weak
   ones (WeAudit 7, Cocoa 9). No figure has an outer frame, and none fills a gap with decoration.
7. **Labels sit on the thing.** Region names inside phase regions and boundary equations in a white box
   rotated to the curve (2505.17638 Figs. 1, 3); runtime in each frame's corner (VGGT 3); totals on bar
   stacks (PipeMorph 1); a verdict bar across the cell (BrickGPT 5).
8. **Everything shared is said once.** One legend strip for 10 or 16 panels, one y label per grid, x labels
   on the bottom row, column heads on the top row, row conditions as rotated labels.
9. **Every encoding is defined next to a sample of itself**, in a key row or the caption: line styles,
   numerals, hatches, bands. Captions open with the claim and then define; their length follows the
   encoding (4–8 words for an architecture, 25–75 where styles need defining, 70–130 for a lettered
   system walkthrough).
10. **Type matches the page or is one sans throughout.** The figures that look most integrated set
    page-level labels in the body face. Diagrams set in one sans family also work (all eight NLP/HCI papers).
    What reads as careless is a default-font chart beside a designed diagram, which happens inside five of
    these award papers.

## What it overturned

| Old rule in this skill | What the award figures do | Rule now |
| --- | --- | --- |
| Charts sit in a rounded white card with a tinted header band | 0 of about 40 charts are in a card; 0 of about 90 figures have a header band | Charts are bare on the page; a container is titled by a tab or a plain head |
| No empty region > 15 % of a panel; crafted figures are 25–43 % white | Median white share is about 70 %; schematics 85–89 %, line art up to 96 % | White space targets by register; the automated check now warns on crowding |
| Legends are an anti-pattern when direct labels fit | 11 of 15 ML chart figures and 6 of 7 systems papers keep a legend, as one frameless row | Direct-label regions, boundaries and reference lines; legend row for many series; never a legend on data |
| Hero line 1.6–2.0 pt, baselines grey and thinner | Every series has one weight; baselines are categorical colours with their own markers | Ours is the only solid line or unhatched bar, first in the legend |
| Hatching is an anti-pattern | Standard second channel in 5 of 7 systems papers | Two channels per series; hatch defined by its legend swatch |
| No top/right spines | Most charts keep the full box | Either; full box for tight grids |
| Text on a role is that role's ink, never black | Black in nearly every figure | Black or near-black; colour a word only when it names a coloured thing |
| Panel titles 7.5–8.5 pt bold everywhere | 5.6–8 pt in an 84 mm column; 9.8–11.9 pt regular on ML charts and schematics | One scale per placement; hierarchy by size before weight |
| Default wire 0.6–0.75 pt, orthogonal, rounded elbows | Geometry follows the structure: orthogonal for layers, diagonals for graphs, arcs for time, curves over images | Arrow geometry by structure; weight equals the box stroke, or heavier when arrows are few |
| White boxes with thin outlines are the "plain" failure | The line-art register of systems and PL papers is exactly that, with one accent | It is a register, chosen on purpose; the failure is using it with no accent and no object |
| 3–5 hues | 0, 1 or 2 hues are common and strong | 0–4 hues |
| Labels 1–4 words, no exceptions | Example text, prompts, quotes and interface text run to hundreds of words | 1–4 words for the figure's own voice; data text is an object and may be long |
| Never DejaVu Sans; match the manuscript | Several award papers ship DejaVu charts, and they look default | Preference with a reason, stated in visual-craft §4 |
| Soft shadow for the hero | No vector shadow outside floating windows | Shadows only for things that float |

## Families with good models

| Family | Model figures |
| --- | --- |
| Scalability grid with shared labels and one legend | CortenMM 14; 2504.13837 Fig. 2; 2503.14858 Fig. 1 |
| Grouped and stacked bars for many systems | CortenMM 19, PipeMorph 1, AnyBlox 6 |
| Layer-cake architecture, control and data planes | CortenMM 3, AnyBlox 4, PipeMorph 13 |
| Schedule timeline, sequence arcs | PipeMorph 5, OSCAR 5 |
| Protocol storyboard | CortenMM 7, Semisolates 2, AnyBlox 2 |
| Decision diagram, tree, page table as line art | NDD 4, Tree Borrows 1 |
| Code figure | CortenMM 6, NDD 2, Tree Borrows |
| Phase diagram with a schematic twin | 2505.17638 Figs. 1, 3 |
| Idea schematic with ghosted alternatives | 2504.13837 Fig. 1, Flexibility Trap 2, Polar Express 2 |
| Geometric intuition | 2505.10465 Figs. 1, 2; IMS 2, 3, 6; FlowEdit 2 |
| Annotated example, example × stage grid | HALoGEN 1, BiGGen 1 |
| Single-column Figure 1 | CoT 1, REL-A.I. 1 |
| Rebuilt screenshot with callouts | Cocoa 2 |
| Interaction storyboard | Cocoa 3 |
| Study design, procedure timeline | Reliance 1, WeAudit 7 |
| Participant-level plot | Cocoa 8, DocWrangler 7 |
| Hero-render teaser | VGGT 1, TRELLIS.2 1, SSS 1 |
| Qualitative comparison grid | D4RT 4, VGGT 3, TRELLIS.2 6, FlowEdit 6, BrickGPT 5 |
| Inset zoom | IMS 27, D4RT 6 |
| Pipeline over real pixels | D4RT 1, 2; VGGT 2 |
| Render storyboard | IMS 8, BrickGPT 3 |

## Flaws in award figures, not to copy

- Text at 3.2–4.9 pt: OSCAR 10, CortenMM 3 cell text, Semisolates 2, 2503.14858 Fig. 1 ticks,
  TRELLIS.2 1 pills, DocWrangler 2 (a whole window shrunk to 3.3 pt).
- Colours that fail in greyscale: PipeMorph 16, Semisolates 3.
- Wires through labels: PipeMorph 13.
- Truncated bar axes (Flexibility Trap 1) and bars on log axes (NDD 11, OSCAR 10).
- Three unrelated hues for three ordered checkpoints (2504.13837 Fig. 1, right).
- A legend sitting on the data (FlowEdit 7); colour bars with no scale (SSS 7, IMS 27).
- A colour pair that changes meaning between adjacent figures (Cocoa 8 vs 9, Reliance 4 vs 5, BiGGen 2 vs 3).
- Low-contrast arrows on a light image (BrickGPT 4: cyan and yellow on white bricks).
- Icons above 3 × cap height reading as clip art (WeAudit 7, HALoGEN logos); seven typefaces in one figure
  (D4RT 2); a spelling error in a stage title (TRELLIS.2 2).
- Default-matplotlib charts beside designed diagrams: REL-A.I. 3, CoT 3–4, Cocoa 9, Reliance 5.
