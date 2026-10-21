# Craft study, 2026-10: what makes top-lab figures look good

Evidence behind [visual-craft.md](visual-craft.md). Sections 1–3 are visual readings of the
user-supplied anchors and the MemT redesign; section 4 is the measured architecture-figure study
(PyMuPDF vector measurement, colour quantisation, ink density). "Measured" values come from vector
data or pixel sampling; others are estimates from renders at print width.

## 1. User anchors

### IdeaScientist Fig. 1 (Meta, arXiv 2610.04074) — infographic plate
- **Composition.** One full-page plate split into three dashed rounded regions: method (top, ~60 %),
  performance (bottom-left, ~30 % width) and "in action" worked case (bottom-right). Each region title
  sits in a large rounded tab that *breaks* the dashed border (slate-blue serif, ~16 pt at print).
- **Typography.** Times-like serif throughout, three clear sizes; section labels Input / Action /
  Output in bold slate blue, content in regular dark grey. Concrete strings, not placeholders.
- **Repeated micro-template.** Every agent (orchestrator, gap finder, innovator, report writer) uses the
  same Input / Action / Output ruled card under a coloured robot head + a role glyph (gear, magnifier,
  bulb, pen). Repetition makes a dense plate scannable.
- **Objects.** A stacked document vault with a taped label; a handwritten "research task" note with a
  paperclip; a database glyph for memory; pie chart of domains; hatched horizontal bars with direct
  numeric labels; mini bar charts inside the causal-inference steps; coloured inline tags
  (relaxed / deadline) in a conversation transcript.
- **Palette (estimated).** Muted earth tones on white: salmon `#D9937A`, sage `#6E9C86`, mustard
  `#C9B458`, slate blue `#4E6FA3`, lavender `#9C86B8`, warm cream panel `#FBF4E2`; light grey fat
  block arrows `#CFCFCF`; one takeaway banner on pale yellow with bold black text.
- **Why it reads premium.** Every region contains a real artifact (documents, transcript, numbers);
  icons give each actor identity; one consistent serif; colour per agent repeated in its icon.
- **Weaknesses.** Very dense for a column-width read; hatched bars add texture without meaning.

### SkillOpt Fig. 2 (Microsoft, arXiv 2605.23904) — fan-out pipeline
- **Composition.** Left data column (three coloured split cards: green train, mustard validation, grey
  locked test) → stacked rollout trace cards with mini line plots and a score → K parallel lanes
  (mini-batch doc → purple optimizer box → atomic-edit card with ADD/DEL/REP chips) with vertical
  ellipses → one tall purple merge bar → stacked rank/clip cards → candidate doc → mustard diamond
  validation gate → blue skill doc → `best_skill.md`. Bottom: a dashed teal region for the epoch-wise
  slow update with improvements / regressions / persistent failures / stable successes pills.
- **Typography.** Serif bold for node titles, smaller serif for sub-lines; caption in a bold sans label
  + serif body.
- **Objects.** Folded-corner documents (blue = skill), stacked cards for multiplicity, robot with a
  lock (frozen agent), flame on the trainable skill doc, chips for edit types, a calendar glyph for the
  LR schedule, mini plots in traces.
- **Connectors.** Dark grey `#4A4A4A` ~1.5 pt arrows with large filled heads for the main flow;
  feedback loops dashed and colour-coded (red reject → buffer → merge, teal slow update) running in
  reserved corridors below the main row.
- **Palette (estimated).** Pastel fills with darker same-hue strokes: green `#A9D18E`/`#6A9A4A`,
  mustard `#F3D27A`/`#C9A227`, purple `#D6B8E2`/`#7A4F94`, teal `#9ED3CF`/`#2E8C88`, salmon
  `#F19A7A`, blue docs `#A9C8EE`/`#3E6FB0`.
- **Weaknesses.** Small text inside chips; the merge bar's sub-text is tiny.

## 2. MemT-1.0 originals (arXiv 2610.26825v2) and the redesigns

**Fig. 4 original** (measured in section 4): 478 pt wide, outlined Times-like text, titles 6–6.5 pt,
subscripts 3–3.5 pt, strokes 0.45–0.55 pt, ink 2.5–2.8 %. Defects: four zoom levels with crossing
rays; matrix memory and gates as text boxes; green also used for a readout box; "inherited" blue used
for new projections; ~250 pt looping state wires; slogans in the art; the time evolution (the key
idea) as the smallest inset; a separate inventory box of hyper-memory parameters.

**Fig. 4 redesign** (`scripts/examples/memt/render_fig4.py`, 170 × 108 mm): locator stack with zoom
wedge → block with parallel attentions → a memory *pillar* holding `M_t` (3 slabs) → read panel
(amber trapezoids = φ, `QM/√d_k` readout, RMSNorm ⊙ SoftCapSiLU gate) and write panel (token-level
chain of state grids, one step drawn on the grid: forget fade → erase row → ⊕ outer-product write)
→ timeline strip (turn 1 with `M = 0`, read every token, write at turn end). White 62 %, tint 29 %,
ink 2.9 %; min text 5.8 pt; math ≥ 6.2 pt; one zoom-ray pair; no crossing wires.

**Fig. 3 original**: two log-scale horizontal-bar latency panels (128K, 256K) and a storage panel;
bars start at an arbitrary 10 s / 10 MiB floor, so lengths encode nothing; ratios are not shown;
the scaling with context is split across panels; web-style rounded cards + gradient hero bars.

**Fig. 3 redesign** (`render_fig3.py`, 170 × 66 mm): (a) slope chart on a log axis, 128K → 256K,
direct labels, hero blue, brackets with `4.0×` and `59×` at 256K and growth factors ×1.46 / ×3.14 /
×2.00; (b) area-true waffle with one cell = 40 MiB (Full Context 129.6 cells, Temp-LoRA 4.3, MemT 1),
"too large at 1M" stated as reported, and a hero callout `130×` / `4.3×`.

## 3. Chart craft observed across the corpus

- Hero vs muted: the proposed method saturated (blue/orange/purple), baselines in 1–2 greys; hero
  values bold (DeepSeek-V3 Fig. 1, Kimi K2, Qwen3 headline bars).
- Direct value labels above bars or at line ends replace most axes; gridlines faint or absent.
- Speed-up claims carry explicit ratio callouts (NSA Fig. 1; Kimi Linear efficiency vs length).
- Efficiency vs length is a line over context length (MiniMax-01, Kimi Linear, Gemma 3 KV-cache
  memory), not separate bar panels per length.
- Rounded card frames and logo icons are a web/blog aesthetic; acceptable, but they do not substitute
  for encoding the claim.

## 4. Measured study: architecture / mechanism figures

The full measurement report produced for this revision follows.


Method: PDFs from arxiv.org/pdf/<id> -> pdf/. Crops via PyMuPDF 250-500 dpi -> png/. Vector stats (fonts, sizes, fills, strokes, line widths) from get_drawings / text dict (scripts/measure.py). Raster/outlined figures (Titans, MemT, NSA) by colour quantisation + saturated-pixel histograms. Sizes are pt at printed size.

### 0. Density (pixel fraction of figure crop)
| fig | white>=250 | tint 200-249 | ink<120 |
|---|---|---|---|
| MemT Fig4 | 46.2 | 47.3 | **2.8** |
| Gated DeltaNet | 42.5 | 49.5 | 6.4 |
| Kimi Linear | 39.2 | 53.0 | 6.0 |
| Titans MAC | 24.2 | 64.8 | 4.7 |
| NSA | 66.9 | 14.2 | 8.4 |
| DeepSeek-V3 | 82.3 | 10.8 | 5.2 |
| Hymba F1 | 73.0 | 9.3 | 11.6 |
| BLT | 62.7 | 31.0 | 4.9 |
| Memory Layers | 56.7 | 32.7 | 6.7 |
| Nemotron-H | 67.0 | 28.1 | 3.6 |

Headline: crafted figures have 5-9% ink (near-black 0.6-1.0pt strokes, compact boxes, glyphs). MemT has comparable tint but < half the ink: 0.4-0.5pt coloured hairlines + small text = pale/generic.

### 1. Per-figure notes

#### 1.1 Gated DeltaNet Fig 1 (NVIDIA, 2412.06464)
- Composition: H1 stack | H2 stack | Block Design. Zoom = one dashed black elbow arrow (0.75pt), no rays; panel names under panels at 5.6pt.
- Type: NimbusRomNo9L (Times) 6.2pt everywhere; real LaTeX math (CMMIB bold-italic q,k,v; CMMI alpha,beta). 342pt wide of 397pt textwidth. Two sizes total.
- Palette: card #f3f3f4; MLP #ceedf9; SWA #fde6e7; GDN/Mamba2 #f5f6cd; Linear #e3e6f3; Norm/L2 #fde8c9; all strokes #000000; only saturated colour #0000ff inside activation glyphs.
- Line weights: 0.75 boxes/wires, 0.62 glyph circles, 0.5 thin. Card radius ~6pt, box ~2pt.
- Operators: plus/times as 5.0pt circles on wire; SiLU = 5pt circle with blue curve; Linear = trapezoid; multi-head = 2 copies offset ~2pt.
- State: not drawn ("Gated Delta Rule" is a box). No recurrence depiction.
- Weaknesses: alpha/beta triangles overlap and occlude white "Lin." text (bug); state S_t invisible; ~30% empty area under stacks.

#### 1.2 Kimi Linear Fig 3 (Moonshot, 2510.26692)
- 2x2: stacks left, zoom cards right (#f3f3f4, r~8pt), dashed elbow arrows.
- Times 7.9pt labels, 7.1 secondary; CM math.
- Fills: MoE #ceedf9, Norm #f5f5cd, KDA #fef0dd, MLA #e6b3b2, Linear #f9d5d1, shared expert #d5ecd9, routed #e3e5f3; strokes black 0.95 / 0.79 glyph / 0.63 thin.
- Gates: 6.3pt circles with red sigma #b92622 on the wire; plus/times 9.5pt; down/up trapezoid pairs = low-rank gate projection; router logits = orange mini bar chart #f8c898; q/k branch ghosted duplicates.
- Weaknesses: delta-rule state is a text box; zero equations; stack pattern duplicated.

#### 1.3 Titans Figs 2/4/5 (Google, 2501.00663)
- Raster (Keynote). Three rounded swim-lanes r~10pt: Contextual #fcf2de/#fff8e3, Core #e5edf1, Persistent #f8e3e3; right "Test Time" column (Learning / In-context / Fixed + snowflake) repeating lane colours. MAC/MAG/MAL keep identical frame -> variants directly comparable.
- Slab-serif type; lane labels rotated, in saturated lane hue (amber #e0a040, slate #606078); white vertical text in dark op boxes.
- Arrows oxblood #985050 ~1.3pt, big open chevrons; op boxes sage #959a85 / #9393a5; token cubes slate #606078, persistent #9b5353.
- Memory = 4x5x3 isometric cube stack with smooth heat field cream #f8f0e0 -> #e8d0b8 -> oxblood #985050 (reads as "learned weights"). Retrieved tokens = empty cubes with 50%-opacity dashed diagonal rays to source.
- Weaknesses: raster; three arrowhead sizes; bands mostly empty in MAG/MAL.

#### 1.4 NSA Fig 2 (DeepSeek, 2502.11089)
- Token strip -> gradient wedge "split to blocks" -> 3 parallel branch cards (compress/select/slide) -> 3 attention bars -> Gated Output; right mask panel; dashed legend; whole fig in dashed gray frame.
- Open-Sans-like bold sans, outlined; titles ~7pt, labels ~4-5pt; branch titles green #27a700 with icons.
- Importance = blue ramp #dae8f9 -> #4a90e2 (4 levels); attention score green #a8db99/#78c860; query orange #ea9424; evicted = dashed; ignored = white.
- Masks as cell grids (~4.5pt cells, 0.4pt gray lines) with causal staircase; selection = receding 3D stack.
- Weaknesses: ~4pt text; green double-duty; gating formula absent.

#### 1.5 DeepSeek-V3 Fig 2 (2412.19437)
- Zoom: two dashed rays #2e75b6 1.0pt (dash ~4 on/3 off) from source box corners to dashed callout corners; bold callout titles outside frame.
- Calibri 8.9pt (bold titles), Cambria Math 6.5-8.9pt bold vectors; italic 7.1pt wire notes ("concatenate", "apply RoPE").
- Op fill #fff2cc; routed #deebf7; shared #c5e0b4; top-K bars #ffd966; box strokes navy #172c51; wires black 0.67pt.
- Tensors: capsules of 8pt circles with ellipsis; multi-head = 3-4 stacked capsules offset ~1.5pt; hatched circles = cached during inference (legend).
- plus 12.4pt, times 8pt; gate weights on dashed yellow curves.
- Weaknesses: 3 corner radii; cut-off "Transformer Block xL" title; crossing curved spaghetti to experts.

#### 1.6 MoBA Fig 1 (Moonshot, 2502.13189)
- (a) colour-as-identity: blocks #8569cb #5263a5 #509863 #bbbfc4; queries #d25d5a #d4b45b; solid vs dotted line per query. (b) generic Source Sans flowchart, header bars #5178c6.
- Weaknesses: 5pt text; (a)/(b) mismatched visual languages; 82% white.

#### 1.7 Qwen Gated Attention Fig 1 (2505.06708)
- Gate positions G1-G5 as ~12pt coloured disks with italic labels, colours = series colours in adjacent bar chart (#4c72b0/#8da0cb, #55a868, #e78ac3, #cc613d). SDPA #e1d5e7 / stroke #9673a6; W_q/k/v trapezoids with ghosts.
- Weaknesses: default draw.io palette; "g" label collides with G4; informal "Most Effective!".

#### 1.8 Nemotron-H Fig 2 (NVIDIA, 2504.03624)
- Avenir 10.4pt rotated in stroke-less pills: Mamba-2 #d9ead3, Attention #f4cdcc, FFN #c9daf7; "x4" corner tags on rounded cards; arrows #5e5e5e 0.65pt.
- Weaknesses: no mechanism; rows redundant; 67% white.

#### 1.9 Hymba Figs 1, 4 (NVIDIA, 2411.13676)
- Dark heads SSM #004c99 / Attn #990000 with white bold Times + drop shadows; peach trapezoid projections #ffe6cc; meta tokens #006633.
- Fading memory = gradient bar white->#004c99 with curved self-loop (excellent minimal recurrent-state glyph); snapshot memory = discrete red cells.
- Fig 4 zoom: two dotted gray rays #8c8c8c 1.3pt to rounded peach callout; repeat groups dashed #76b900.
- Weaknesses: dated drop shadows; all-bold text (no hierarchy); 4.1-5.6pt text.

#### 1.10 BLT Figs 2, 5 (Meta, 2412.09871)
- Tokens = 5x12pt pills coloured by stage: bytes #f4cccc, encoder #fff2cc, patch #cfe2f3, decoder #d9ead3; patch grouping = rounded outline; entropy plot under encoder; numbered step cards #d9d2e9, text #595959. Arial 9.2pt, strokes 0.58pt.
- Weaknesses: step cards eat 40% width; latent transformer a plain box; mixed 6.2-10.8pt.

#### 1.11 Memory Layers at Scale Fig 3 (Meta, 2412.09764)
- Diff-by-backdrop: added parts on #c9daf8, original memory on #d0e0e3; memory parts #ea9999; gate W1/silu/W2 #b4a7d6. Arial Bold 8.6pt; plus/times 9.6pt circles ~1pt black.
- Weaknesses: long residual loops; product-key memory as text boxes; all-bold text.

### 2. MemT-1.0 Fig 4 critique (2610.26825 p6)
Measured: 478pt wide; text outlined Times-like serif; titles ~6-6.5pt bold, labels 5.5-6.5pt, subscripts ~3-3.5pt (some <3pt); caption 9.86pt. Palette: blue #eaf2fc/#4a7fb5; purple panel #faf7fe, box #eee7fa, stroke/title #9870c6/#6030a0; green #ecf6eb/#579554, arrows #317235; orange #fff8ef/#cf944c; text #18212b; dashed frame #b6bec8. Strokes ~0.45-0.55pt, green wires ~0.9pt. plus ~9pt; odot ~8pt inside a rounded square (inconsistent). Ink 2.8%.

Problems:
1. Four zoom levels (stack -> Transformer Block -> Native Memory Block -> Storage/Utilization); blue and purple dashed rays leave nested boxes at nearly the same spot and cross.
2. Every mechanism is a text box: Erase/Write/Forget are three 55x30pt boxes; "Stable Token-level GDN-2 Update" is text; Matrix Readout is a fraction in a box. The matrix memory appears only as a small grid icon.
3. Gates look like layers (same weight as projections) instead of sigma circles on the wire.
4. Hand-assembled math: floating (l), staggered sub/sup, no space before "=", gap after "(", oversized tilde.
5. Pale/low contrast: hairline coloured strokes, 2.8% ink; labels same weight as titles.
6. Colour scoping broken: green = dynamic state but also Matrix Readout box; purple used for gates, RMSNorm, SoftCapSiLU, Concat and titles; blue = "inherited" yet fills new K/V/Q projections and output gate.
7. Long routed state wires (~250pt green loops, one down the right margin).
8. Slogan sentences inside figure ("Persistent memory brings...", "Memory becomes part of the model's forward pass").
9. Dead space: empty column between H^(l) and Post-Attention; Hyper Memory Block = parameter-name cards (belongs in table/caption).
10. Time evolution (t -> t+1, the key idea) is the smallest inset at bottom-left.
11. Outlined text: not searchable.

### 3. Rules
1. Design at print size: full width 478-500pt, column 234-240pt; never scale >+-10%.
2. Labels 7-8pt, titles 8-9pt bold, sub/superscripts >=5pt; max 3 sizes; one family: STIX Two/Times with real math (mathtext 'stix' or usetex) or a humanist sans (Source Sans 3, Avenir). Never DejaVu Sans.
3. Typeset math: bold upright matrices, bold italic vectors, italic scalars; drop a constant layer index into the panel title.
4. Strokes #1a1a1a 0.75pt (boxes, wires), 0.6pt glyphs, 1.0pt main data path; target 5-8% ink; coloured strokes only for the novel hue.
5. Pastel fills L* 88-95 (#ceedf9 #f5f6cd #fde6e7 #e3e6f3 #fde8c9 #d5ecd9); cards #f3f3f4 r 6-8pt; boxes r 2-3pt.
6. One saturated novel hue (e.g. #985050 or #6a3fa0) for novel outlines (1.0pt), state heat ramp, memory wires, novel panel titles. Inherited = neutral #e3e6f3/#eef1f5; non-novel op boxes colourless; <=4 fill hues, one meaning each.
7. Diff-by-backdrop: tint (novel hue ~12% alpha) behind only the added parts.
8. Operators = circles on the wire: plus/times/odot 6-9pt, white fill, 0.6-0.75pt; gate = 6pt circle with red italic sigma #b92622; activation = 5-6pt circle with function curve. Never a rectangle for an elementwise op.
9. Projections = trapezoids 9-12pt tall; trapezoid pair = low-rank.
10. Multi-head/expert = 2-3 copies offset (+2,+2)pt at 60%/30% opacity.
11. Vectors = 4-6 circles (6-8pt) or cells (5x5pt) with ellipsis; hatch/dashed = cached/evicted; legend chip per encoding.
12. State matrix (the hero): 6x6 grid, 4-5pt cells, 0.4pt white gridlines, filled from a fixed random field on a 3-stop ramp (#f8f0e0 -> #d9a78f -> #985050); multi-head = 3-4 slabs offset 3pt up-right at 100/70/45% brightness, or isometric cubes; 30-45pt overall.
13. Draw the update on the grid: decay = lighter next grid + alpha chip; erase = dashed column highlight; write = outer-product glyph (6x1 strip times 1x6 strip); readout = q strip entering grid + odot.
14. Max 2 zoom levels per canvas; deeper -> sub-figures (a)(b)(c).
15. Zoom connector, one style per figure: (A) two non-crossing dashed rays 0.75pt dash 3-2 from source box's facing corners to callout's near corners; or (B) single dashed elbow arrow. Use B when >=2 zoom sources.
16. Recurrence: t-1 | t | t+1 columns, neighbours at 35-50% opacity; or 6pt-radius self-loop on the state glyph.
17. Parallel branches in equal-width columns merging on one bus or plus; corresponding stages share y.
18. Swim-lanes by update regime (frozen / test-time learned / in-context): full width, r 8-10pt, rotated label in lane hue.
19. <=1 key equation per mechanism, under its glyph, 7pt; <=2 equation lines per panel; projections like K = L2Norm(HW_K) go to text.
20. Density: white <=55%, tint <=50%, ink 5-8%; no empty region >15% of a panel; wires <=120pt where possible.
21. Arrows 0.75pt, one filled head style 3.5-4pt long, orthogonal routing with 2pt corners; dashed only for control/gate signals.
22. No sentences in figure: labels 1-4 words; narrative -> caption or numbered 8pt step chips.
23. Same hue = same entity across all panels and plots.
24. >=3 encodings -> one-row legend, 8pt chips, 7pt text, bottom-right inside frame.
25. Export vector PDF with embedded (not outlined) fonts; never raster.

### 4. Redesign plan: MemT Fig 4 (478 x ~230pt)
Global: STIX Two; labels 7.5pt, titles 8.5pt bold; mathtext; drop "(l)" -> "layer l" in title. Strokes #1a1a1a 0.75pt, data path 1.0pt; ink target ~6%.
Hues: inherited #e3e6f3 (embedding, norm, original attention, LM head); novel memory #6a3fa0 with heat ramp #f3eefa -> #b79ad8 -> #6a3fa0 (M_t grid, memory wires, Memory Attn outline, novel titles); gates = red sigma circles only; offline-trained = #cf944c snowflake chip.

(a) Overview, ~110pt: LM stack on #f3f3f4 card; one block shown as "Attn | Mem" (Mem outlined purple 1.0pt). Below: time strip of three 12pt M grids t-1 | t | t+1 joined by "turn-end write" arrows, neighbours 40% opacity. Replaces theta inset and both slogans.

(b) Native Memory Block zoom, ~120pt, connector A (only ray pair in figure): H~ splits to Original Attn (neutral) and Memory Attn (purple) -> 7pt plus on wire -> Post-Attn. Pre/Post-Attn become 9pt slim bars; empty column removed.

(c) Mechanism, ~240pt, reached by one elbow arrow (connector B). Two lanes: Write (turn end) on top, Read (every token) below; shared M_t glyph between them (3 slabs of 6x6 heat cells, ~40pt).
- Write: h~_i -> trapezoids W_K, W_V -> k, v strips; three sigma circles (beta erase, omega write, lambda forget) replace the three boxes; update glyph M_{i-1} (70%) -> "x lambda" chip -> "-beta k k^T" dashed column -> "+omega v k^T" outer-product glyph -> M_i; one 7pt equation in the paper's exact form; 6pt self-loop "next token" replaces the 250pt green loop.
- Read: h~_t -> W_Q -> q strip into grid -> r = Mq/sqrt(d_k) strip -> RMSNorm slim bar -> odot (7pt circle); gate branch W_{g/d}, W_{g/u} trapezoid pair -> SoftCapSiLU curve circle -> odot; head ghosts -> Concat -> A_mem.
Hyper memory: delete parameter cards; snowflake chip on offline-trained trapezoids; "online" chip on M_t. Legend row: snowflake offline | online | heat grid = M_t | sigma gate.
Pre-export checks: nothing <5pt; <=3 sizes; no connector crossings (1 ray pair + 1 elbow); longest wire <=120pt; ink 5-8%; fonts embedded.

Why it wins: 4 -> 2 zoom levels without crossings; matrix memory and erase/write/forget become pictures; gates read as gates; 6 hand-kerned equation lines -> 1-2 typeset; one meaning per hue; time evolution promoted to the overview; ~2x ink contrast, same visual class as GDN/Kimi/DeepSeek-V3.

Artifacts: png/ (crops), scripts/ (caps.py, fig.py, measure.py), pdf/.
