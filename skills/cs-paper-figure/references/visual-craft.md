# Visual craft: drawing figures that look like top-lab figures

Read this before drawing anything. It is the rulebook distilled from a 2026-10 close study (see
[craft-study-2026-10.md](craft-study-2026-10.md)) of IdeaScientist Fig. 1 (Meta), SkillOpt Figs. 1–2
(Microsoft), Gated DeltaNet (NVIDIA), Kimi Linear and MoBA (Moonshot), Titans (Google), NSA and
DeepSeek-V3 (DeepSeek), Qwen Gated Attention, Nemotron-H and Hymba (NVIDIA), BLT and Memory Layers
(Meta), plus the MemT-1.0 figures that were redesigned as worked examples. Numbers are at printed size.
General colour/typography background remains in [visual-design.md](visual-design.md).

Implementation: [`scripts/paperkit.py`](../scripts/paperkit.py) provides every primitive named below in
millimetre units. Worked example: [`scripts/examples/memt/`](../scripts/examples/memt/).

## 0. Why earlier outputs looked plain

The previous examples were scientifically careful but read as flowcharts or compliance reports:

| Symptom | Fix |
| --- | --- |
| White boxes with thin coloured outlines, every box the same weight | Role colour *families*: pale fill + same-hue stroke + dark same-hue text; one hero element with heavier stroke/shadow |
| DejaVu Sans, bold everywhere | Times/STIX serif with STIX math to match the paper body (or Helvetica/Arial); bold only for titles and the hero |
| Sentences as panel titles ("Replay a separate case, then commit or retain the baseline") | Noun-phrase titles ≤ 6 words in a header band; narrative goes in the caption |
| Words where an object belongs ("Memory M_t current snapshot") | Draw the noun: a matrix glyph, token strip, document, trapezoid, gate circle (§4) |
| Watermarks and receipts inside the art ("SCHEMATIC", "AUDIT RECEIPT", "Fixture, not benchmark data") | Status labels belong in the caption; keep an in-art label only for invented data that could be mistaken for results |
| Mono-spaced tables and pass/fail grids as the main visual | Tables only when lookup is the task; otherwise show the change on the object itself |
| Default-looking charts with legends | Hero/muted colouring, direct labels, ratio callouts, area-true encodings (§9) |

## 1. The five-second test

Before polishing, state the one thing a reader should get in five seconds and make it the largest,
most saturated, highest-contrast element. MemT Fig. 4 → "memory is read every token and written once
per turn"; the redesign gives the state matrix its own column, colours the read path blue, the write
path violet, the state teal, and adds a turn timeline. MemT Fig. 3 → "4× faster, 130× smaller"; the redesign prints
those ratios in bold hero blue next to brackets. If nothing is visibly the hero, the figure is not done.

## 2. Typography

- **Family.** Match the manuscript. For LaTeX/Times papers use Times New Roman or STIXGeneral (bundled
  with matplotlib, so no fallback) with `mathtext.fontset = "stix"`; never DejaVu Sans. For sans papers
  use Helvetica/Arial with `stixsans`. `paperkit.use_fonts()` does this and embeds TrueType (Type 42).
- **Sizes (pt at print).** Panel titles 7.5–8.5 bold; node titles 6.8–7.5 bold; body/math 6.5–7.2;
  annotations 5.8–6.3 italic, muted. At most 3 sizes plus the annotation size. Math subscripts must
  stay ≥ 4.5 pt → math base ≥ 6.4 pt. (Measured: Gated DeltaNet 6.2 pt everywhere; Kimi Linear 7.9/7.1;
  DeepSeek-V3 8.9 titles / 6.5–8.9 math; MemT original 3–3.5 pt subscripts — avoid.)
- **Weight hierarchy.** Bold = title, hero number, hero method name. Regular = everything else.
  Italic = connector annotations and caveats. All-bold text (Hymba, Memory Layers) flattens hierarchy.
- **Math.** Typeset, never hand-assemble: bold upright matrices (`\mathbf{M}`), bold-italic vectors
  (`\boldsymbol{\beta}`), italic scalars. Drop a constant index into the panel title ("Transformer
  block l") instead of repeating `(l)` on every symbol. One governing equation per mechanism, under its
  glyph; colour-code its terms by role with `Canvas.rich()`.

## 3. Colour = role families

Each role gets five tokens (`paperkit.ROLE`): `fill` (L\* 95–97, node/card body), `soft` (L\* 88–90,
header bands, chips, highlighted node), `stroke` (L\* 55–65, outlines), `ink` (L\* 25–35, text on that
role), `mark` (saturated, data marks and the hero). Text on a role is always that role's `ink`, never
pure black and never the stroke colour.

- 3–5 hues, each with exactly one meaning, stated somewhere (legend row, caption, or panel title).
  MemT redesign: grey = frozen backbone (recedes), teal = the memory state M only, blue = read path,
  violet = write path, amber = parameters trained offline (φ), coral/grey = locally scoped gate terms.
  Each panel's header band takes the colour of the path it explains, so the reader can match panels
  to wires without a legend. A first draft used green for both the state and the read path; an
  independent review flagged it, and splitting state from read was the single biggest clarity gain.
- **Novel vs inherited.** Inherited parts neutral/slate; the paper's contribution gets the saturated
  hue, a 0.8–1.0 pt stroke, and optionally a soft shadow (`shadow=True`). Do not paint inherited
  and new parts with one hue (MemT original used "inherited" blue for its new K/V/Q projections).
- **Ownership in place.** Instead of a separate inventory box ("Hyper Memory Block: W_Q, W_K …"),
  colour every component that owns those parameters (amber trapezoids). This deletes boxes and long wires.
- **Local colour scope.** A colour may carry a second meaning inside one dashed callout if it is
  labelled there (erase = coral, forget = teal chips in panel d).
- Panel bodies white or near-white with a tinted header band; tint the panel body only when the panel
  *is* the role (the memory pillar). Measured tint share in crafted figures: 10–65 %; white 25–80 %.
- Charts: one hero colour (method) + two greys for baselines (`#5E6875`, `#8E99A8`); the hero line is
  1.6–2.0 pt, baselines 0.9–1.1 pt.

## 4. Draw the noun: object vocabulary

| Concept | Glyph (`paperkit`) | Notes |
| --- | --- | --- |
| Matrix / state / memory | `matrix(depth=3)` grid slabs, 4–6 cells/side, 3-stop ramp of the role hue | Offset slabs = heads/channels; `fade=` for decay, `band=` dashed row/col for erase/write target |
| Vector (q, k, v, gate values) | `vec()` strip of 3–6 shaded cells | Outer product = column strip × row strip |
| Linear projection | `trap()` trapezoid, narrow side = output dim | Pair narrow-right + narrow-left = low-rank down/up projection |
| Elementwise op | `op()` circle 2.4–3.2 mm: `+` ⊕, `.` ⊙, `x` ⊗ | Never a rectangle for an elementwise op |
| Gate / nonlinearity | small chip on the wire or σ circle | Gates are not layers; do not give them layer-sized boxes |
| Tokens / sequence | `tokens()` rounded squares, fill by token type | Inputs vs generated in two tones of one neutral |
| Multiplicity (heads, experts, batches) | `stack(n=3)` offset cards, or 3 copies + `⋯` | SkillOpt: K minibatch lanes with vertical ellipsis |
| Document / artifact / skill file | `doc()` folded corner + faux text lines | Paperclip/tape title for a corpus (IdeaScientist) |
| Store / database | `cylinder()` | |
| Decision / validation gate | `diamond()` with accept/reject coloured exits | SkillOpt: mustard gate, green accept, red dashed reject |
| Frozen / trainable / fixed / evolving | `icon_snow`, `icon_flame`, `icon_lock`, `icon_cycle` | One icon per role, top-right of the node, 2.4 mm |
| Agent / model | `icon_robot`, distinct colour per role | IdeaScientist: one coloured robot head per agent + a role glyph |
| Edits / operations on text | `chip()` pills: ADD / DEL / REP | |
| Scores, traces, curves | mini plot inside the card | SkillOpt trace cards carry a tiny line plot and a score |
| Time / turns / epochs | columns t−1 · t · t+1, or a strip with write arrows between | Promote time to a panel when evolution is the claim |

## 5. Composition patterns

1. **Overview → zoom → mechanism** (MemT redesign, DeepSeek-V3, Kimi Linear). Narrow locator stack
   (≈20 % width), zoom rays (`zoom()` with a faint wedge fill) into the block, then the mechanism.
   Max 2 zoom levels per canvas; deeper detail becomes another panel reached by an elbow arrow.
2. **State pillar between reader and writer.** Give persistent state its own column; the read path
   leaves it at the top, the write path returns to it at the bottom. Replaces long looping wires.
3. **Mechanism storyboard on the object.** Show one step on the actual glyph:
   `M_{i-1} →(forget) faded M →(erase) M with dashed row ⊕ (v × k outer product) → M_i`, then the
   typeset equation underneath, colour-coded by the same chips.
4. **Infographic quadrants** (IdeaScientist): system overview + performance + a concrete case in one
   plate, each section in a dashed rounded region with a large title tab breaking the border, a
   repeated micro-template per agent (Input / Action / Output), and a bold takeaway banner.
5. **Fan-out / merge pipeline** (SkillOpt): data splits as coloured cards → stacked rollout cards with
   mini plots → K parallel lanes → one tall merge bar → gate diamond → accepted artifact; feedback
   loops dashed and colour-coded by meaning (red reject, teal slow update), in a reserved corridor.
6. **Timeline strip** under a mechanism figure when the claim involves evolution across steps.

Grid: 2 mm unit; card gutter 2.5–3.5 mm; card radius 2.0 mm; node radius = min(1.6 mm, 0.16·h);
header band height ≈ 0.62 × title pt in mm. Align corresponding stages on shared baselines.

## 6. Connectors

- Default wire: `#4A4F57`, 0.6–0.75 pt, orthogonal, 1.0–1.2 mm rounded elbows, filled head ≈ 1.2–1.5 mm.
- Hero path: role `mark` colour, 0.9–1.0 pt, head 1.4–1.5 mm. Coloured wires only when colour encodes
  the path type (read / write / reject / feedback). Residual/skip paths lighter grey, 0.55 pt.
- Dashed only for control, feedback, zoom rays and "conceptual" links; define each dash meaning locally.
- Junction dots (0.8–0.9 mm) where a wire splits. Arrowheads touch borders exactly.
- Fat neutral block arrows (`block_arrow`, `#D5D9DF`) for stage-to-stage flow between big sections.
- Longest wire ≲ 45 mm; if longer, move the endpoints (state pillar) instead of routing around.
- Zero unexplained crossings; one zoom-ray pair per figure.

## 7. Density and contrast targets

Measure with `python scripts/paperkit.py density fig.png` (fractions of white ≥ 250, tint 200–249,
ink < 120 in greyscale):

| Figure | white % | tint % | ink % |
| --- | --- | --- | --- |
| Gated DeltaNet / Kimi Linear | 39–43 | 50–53 | 6.0–6.4 |
| DeepSeek-V3 / NSA | 67–82 | 11–14 | 5.2–8.4 |
| MemT-1.0 Fig. 4 (original) | 43 | 50 | 2.5–2.8 (pale, generic) |
| MemT Fig. 4 redesign | 62 | 29 | 2.9 (+ saturated glyphs) |

Targets: no empty region > 15 % of a panel; ink ≥ 2.5 % with dark text, or ≥ 5 % when the figure is
mostly line art. Low ink with hairline coloured strokes is the "pale/generic" failure mode.

## 8. Text inside figures

Labels 1–4 words. No slogans ("Memory becomes part of the model's forward pass") — that is caption
text. Units and conditions go in a one-line italic subtitle under the panel title. Every number shown
must come from the inputs; derived ratios are computed in code and asserted.

## 9. Charts

- **Encode what the claim is about.** Speed-up claims need the ratio visible: bracket between hero and
  baseline with a bold `4.0×` label. Bars on a log axis that start at an arbitrary floor (MemT Fig. 3)
  make length meaningless — use dots/slope lines on log axes, bars only on linear axes from zero.
- **Area-true comparisons** for "N× smaller": a waffle where one cell = the hero's footprint
  (130 cells vs 1 cell) is honest and visceral; partial cells for fractions.
- **Slope chart** for two conditions (128K → 256K): shows both the level and the scaling; print growth
  factors (×1.46 vs ×3.14).
- **Direct labels** at line ends/segments in the series colour; no legend when ≤ 4 series.
- Axes: no top/right spines, light value-axis grid `#E6E9ED` 0.5 pt, tick labels `#5A626D` 6.2 pt,
  label only major decades on log axes; values formatted `1,401` / `23.7` (≤ 3 significant digits).
- Hero method: saturated `mark`, bold value labels, larger marker (2.1 mm vs 1.6 mm) with white edge.
- Model icons (logos) only when the venue allows; otherwise text labels.
- Cards: each chart in a rounded white card with a tinted header band, matching method figures.

## 10. Beat-the-original protocol (redesign tasks)

1. Render the original figure region at print width; list concrete defects (zoom levels, crossings,
   min text size, colour meaning conflicts, hidden key idea, slogans, dead space, ink %).
2. Re-read the method text and extract the governing equations and timing; the redesign must be at
   least as faithful (MemT: read every token, write once per turn, M = 0 at a new trajectory).
3. Decide the five-second message and the hero; choose a composition from §5.
4. Build with `paperkit`, export PDF/SVG/PNG, then compare side by side at the same width
   (`python scripts/paperkit.py compare original.png new.png out.png`) and with `density`.
5. Fix overlaps and clipped labels found in the PNG; iterate until the side-by-side shows a clear win
   on message, hierarchy, faithfulness and legibility, not only on decoration.

## 11. Anti-patterns checklist

- [ ] Equal-weight boxes, no hero
- [ ] Box containing a sentence or an inventory of parameter names
- [ ] Gate / elementwise op drawn as a layer-sized rectangle
- [ ] State or memory drawn as a text box
- [ ] Colour with two meanings without a local label
- [ ] Wire > 45 mm or crossing another wire
- [ ] Text < 5.8 pt, subscripts < 4.5 pt, or DejaVu Sans in a Times paper
- [ ] Watermarks / audit receipts / slogans inside the art
- [ ] Legend where direct labels fit; ratio claims without a visible ratio
- [ ] Log-axis bars, unexplained hatching, or decorative 3-D
