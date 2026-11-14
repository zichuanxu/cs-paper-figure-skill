---
name: cs-paper-figure
description: Design, implement, critique and redesign figures for computer science research papers, with deliberate control of colour, layout, typography, white space, shapes, icons and arrows. Use for method and architecture diagrams, idea schematics, system and protocol figures, annotated examples, interface and study figures, teasers, qualitative grids, evaluation charts and multi-figure sets, at single-column or full width. Use when asked to draw or improve a paper figure, make a NeurIPS/ICML/ICLR/CVPR/ACL/CHI/SOSP/OSDI/SIGGRAPH-quality figure, redesign Figure N of a paper, or extract a figure's visual style. Rules are measured from award papers at those venues and from 2025–2026 AI-lab reports. Produces scientifically faithful, editable, reproducible vector figures.
---

# CS Paper Figure

Make the scientific argument visible and give it a deliberate visual form. A figure succeeds when a reader
gets its one message in five seconds, can trace the mechanism or comparison behind it, and can read every
label at printed size. Scientific fidelity comes first: no invented data, edges or modules.

Ten principles held in every strong figure studied, across systems, ML, vision, graphics, NLP and HCI
venues. They are the core of this skill; [visual-craft.md](references/visual-craft.md) turns each into
rules with measured values.

1. **One message, one hero, and the hero is the thing that differs**: the only coloured object, the only
   solid line, the largest block. Never the thickest outline.
2. **Choose a register first** (line art, idea schematic, example-led, image-led, plate, showcase) from the
   venue, the column width and the claim, and stay inside it.
3. **Count everything**: at most four hues, two stroke weights, three text sizes, three arrow styles, one
   icon family, one panel treatment.
4. **Repeat one drawing and change one thing**; ghost what was not taken.
5. **Run one concrete example through every stage.**
6. **Colour is a name**: one meaning per hue, kept through every form the thing takes and every figure of
   the paper. Colour only what is new, wrong or being followed.
7. **The page is the ground and white space is grouped**: gutters, bands and label rows, never scattered
   holes, never a frame and a tint on everything.
8. **Draw the noun** and put labels on the thing; say shared things once.
9. **Define every encoding** beside a sample of itself, in a key or the caption.
10. **Type matches the page**, at sizes that fit the placement: labels at 5.8 pt or above, nothing below
    5 pt.

**The failure to expect.** A figure can obey every budget above and still look unfinished: a motivating
example set as a table of sentences with score bars, or a method overview cut into lettered panels that
share nothing. Both come from choosing style values before deciding what the picture is, and from never
looking at a finished figure of the same kind. So the workflow below has three steps that are not optional:
write the picture in one sentence (step 2), open a model figure before drawing (step 2), and revise at
least once after a cold read of the render beside that model (step 6).

## What to read

**Always, before drawing:** [model-figures.md](references/model-figures.md): the seven things every strong
figure has, the two ways a compliant figure fails, and one rendered model per figure family in
`assets/models/`. Open the model's PNG, not only its description. Then
[visual-craft.md](references/visual-craft.md), the rulebook by design
dimension. Read §1–§2 (message, register) first and pick the register; then read the one section of
[registers.md](references/registers.md) for that register and family; then the rest of visual-craft
(colour, typography, layout, white space, shapes, icons, arrows, text, charts, captions, redesign
protocol, checklist).

Paths in this file are relative to the skill directory; run the commands from there.

**When the task calls for it:**

| Need | Resource |
| --- | --- |
| What may and may not be claimed: data, units, uncertainty, transformations | [scientific-contract.md](references/scientific-contract.md) |
| Several figures for one paper, survey or framework: shared palette, chapter frames, running example | [figure-series.md](references/figure-series.md) |
| Generated icon sets, scenes and vignettes with Codex CLI (showcase register only) | [image-generation.md](references/image-generation.md), [scripts/codex_images.py](scripts/codex_images.py) |
| Rich multi-level plates (system, mechanism, instance, evidence) | [dense-composition.md](references/dense-composition.md) |
| Scenes, frame sequences, trajectories, visual memory | [visual-objects.md](references/visual-objects.md) |
| Explicit ports, return loops, collision review | [diagram-routing.md](references/diagram-routing.md) |
| Extracting a source figure's colours, fonts and geometry | [design-extraction.md](references/design-extraction.md), `scripts/inspect_pdf_style.py` |
| Export, fonts in the PDF, final checks | [production-review.md](references/production-review.md) |
| Strict chart specification for supplied values | [spec-format.md](references/spec-format.md), `scripts/plot_from_spec.py` |

**Evidence, for lookup only.** Read a study when a rule looks wrong for the figure in hand or you need a
model figure; do not load them for every task.

| Study | Covers |
| --- | --- |
| [venue-study-2026-11.md](references/venue-study-2026-11.md) | 29 award papers (NeurIPS, ICLR, ICML, CVPR, ICCV, SIGGRAPH, ACL, EMNLP, NAACL, CHI, UIST, CSCW, SOSP, OSDI, NSDI, PLDI, VLDB): measurements, what held everywhere, model figures per family |
| [craft-study-2026-10.md](references/craft-study-2026-10.md), [architecture-study-2026-11.md](references/architecture-study-2026-11.md) | AI-lab method figures; 23 vision and multimodal architecture figures |
| [arebench-study-2026-11.md](references/arebench-study-2026-11.md), [toolspace-study-2026-11.md](references/toolspace-study-2026-11.md) | Benchmark contrast and construction figures; showcase teasers and a failed redesign |
| Lab corpus: 120 papers, 261 figure anchors | `python scripts/reference_catalog.py search --query "attention mask streaming" --since 2025 --limit 6`, then `show <paper-id> --figure "Figure 2"`; atlases and per-lab studies under `references/` ([dense-paper-atlas.md](references/dense-paper-atlas.md) is the index) |

Older references ([visual-design.md](references/visual-design.md), [style-recipes.md](references/style-recipes.md),
[figure-patterns.md](references/figure-patterns.md), [reference-selection.md](references/reference-selection.md),
[advanced-examples.md](references/advanced-examples.md)) remain for their composition recipes and
contracts. Where they give a size, stroke or font that differs from visual-craft, visual-craft governs.

## Modes

- **Create:** turn claims, methods or data into figures and reproducible source.
- **Redesign:** keep the scientific meaning, values, topology and conditions; stay in the source's register
  and beat it there. First list what the original does well and keep or beat each strength
  (visual-craft §13). A more correct but plainer figure has failed; so has a more decorated, harder one.
- **Critique:** open the actual figure and caption, count hues, stroke weights, sizes and arrow styles,
  walk the checklist (visual-craft §14), and give specific fixes by region. If the image cannot be opened,
  say so; do not invent its defects.
- **Figure set:** give each figure an evidential role; one palette, one shape grammar and one type scale
  for the paper.
- **Narrow edit:** reuse the source and check the changed region and the export. Do not rebuild.

Use available sources, code and templates before asking questions. Decide routine style choices yourself.
Ask only when an unresolved scientific fact changes correctness.

## Workflow

### 1. Brief the content

Capture, compactly or in [figure-brief.yaml](assets/figure-brief.yaml):

- The one claim or mechanism, and the operation that carries it: input, rule, changed output, consequence.
- Evidence status of everything shown: measured, reported, derived, illustrative or schematic.
- For data: comparison, units, sampling unit, aggregation, what intervals mean.
- For diagrams: verified entities, operations, state, boundaries and directed edges.
- **Venue, template and placement: one column (76–85 mm) or full width (140–178 mm), and the body face.**
  "Single-column template" and "one-column figure" are different things. A single-column template (NeurIPS,
  ICLR: text 140 mm wide) has only full-width figures, and a small one is centred at 76–100 mm. A
  two-column template (ICML 2 × 83 mm in 171; CVPR 2 × 83 in 175; ACL 2 × 77 in 160; ACM 2 × 85 in 178) has
  column figures and full-width ones.
- Unknown facts and necessary qualifications.

Do not add a module, edge, update or memory write the system does not have. Do not invent data or
uncertainty to complete a layout; show a pending state instead. Label invented measurements
**SYNTHETIC DATA** or **ILLUSTRATIVE DATA** inside the export and in the caption. A method diagram is
schematic by nature: say so in the caption, not as a watermark in the art. When the paper supplies no
running example, write a small plausible one (a turn, a query, an answer) and carry it through every stage:
sample text in a schematic is plainly an example and needs no disclaimer. It must not look like a result.

### 2. Decide the message, the picture, the hero and the register

Write the five-second message. Then write **the picture** in one sentence, before any style value: which
objects are drawn, what joins them, and what visibly differs. For example: "the task stream once in the
middle, the baseline above and ours below on the same columns, the revised rule struck out and rewritten on
its card, a cross and a tick at the two ends." Check the sentence against two tests and rewrite it until it
passes both ([model-figures.md](references/model-figures.md)):

- **Not a table.** If LaTeX could set the figure as a `tabular` without losing anything, the claim is
  written, not drawn. Draw the objects and the relation the claim is about.
- **Not islands.** If the panels share no object and no line, there is no figure, only thumbnails. Find the
  spine, the path of one concrete item from input to outcome, and hang everything else on it as a zoom, a
  ghosted lane or an inset attached to the object it describes.

Name the hero and how it will differ from everything else. Pick the register (visual-craft §2) and read its
section in [registers.md](references/registers.md). Open the model figure for the family in
`assets/models/` and note three devices you will take from it. For a redesign, name the source's register
and list its strengths before its defects.

### 3. Choose the structure

| Reader's task | Starting structure |
| --- | --- |
| Grasp an idea or a failure mode | Idea schematic: one object redrawn per condition, alternatives ghosted, the measurement beside it |
| Understand the new operation | Narrow overview, larger mechanism detail, one concrete example on the real object |
| Understand a method that works on text (NLP), in one column | Example-led: one example read top to bottom in three tiers (registers §3) |
| Follow data, state or control | Typed shapes, layer bands or planes, two or three defined arrow styles |
| Follow a protocol or algorithm | Storyboard of equal panels, one change each; or a timeline with time on x |
| See behaviour on text | Example × stage grid with marked spans; no arrows |
| See behaviour on pixels | Hero-plus-satellites teaser; comparison grid with fixed camera; inset zooms |
| Understand an interface | Rebuilt screenshot with lettered callouts; numbered interaction storyboard |
| Compare alternatives | Matched positions and shapes; only the real differences change |
| Compare measured conditions | Claim chart (one comparison) or field chart (many systems × conditions) |
| Inspect scaling or cost | Small-multiples grid with shared labels; quality-cost trade-off with conditions stated |
| Diagnose a component | Paired deltas, ablation panels, distributions, shared-scale heatmaps |

**Earn the width.** A full-width figure (140–178 mm) needs content for it: a spine with five or more drawn
objects on it, a hero that takes 40 % of the area or more, or a long example text. A figure with about a
dozen small objects is a column figure (76–85 mm) even in a single-column template; drawn across the page
it is mostly blank and reads as unfinished. Decide the width from the content, then make the objects fill
it: `paperkit.py fill` fails a full-width diagram that is more than half blank.

For a substantial new figure, sketch two materially different compositions and keep the one with the
clearer reading order and fewer arrows. Give the most area to the operation that carries the claim. Use a
table if exact lookup is the reader's task. If everything will not fit at readable size, split the figure.

### 4. Specify the visual system

Record actual values before rendering, one line each:

1. **Palette:** the hues (0–4), what each names, where each recurs; greys for scaffolding.
2. **Type:** face (body face, or one sans for all diagrams), the two or three sizes from the scale for this
   placement (visual-craft §4), what is bold.
3. **Space:** canvas in mm, the module, the two gutter widths, container padding, where the white goes.
4. **Shapes:** which shape means which kind; the one stroke weight; radii; how containers are titled.
5. **Icons:** none, or the one family and what each replaces.
6. **Arrows:** whether any are needed; the styles (≤ 3) and their meanings; geometry; where the key goes.

### 5. Build reproducible source

Draw with `paperkit.Canvas` (millimetre coordinates = printed size); keep the project's own toolchain
where it has one. Use plotting code for data and vectors for diagrams. Never use image generation for
quantitative marks, exact labels or topology. Keep raw observations separate from summaries; compute
derived numbers in the script and assert them.

```python
import sys; sys.path.insert(0, "scripts")            # or the absolute path of the skill's scripts directory
from paperkit import Canvas, series_kw
cv = Canvas(84, 46, family="serif", size=6.5)        # one column, body face
cv.box(4, 30, 18, 6, "line", "Scheduler", radius=0, lw=0.6, weight="normal")  # line art: white, black stroke
cv.box(30, 30, 18, 6, "line", "Workers", radius=0, lw=0.6, weight="normal")
cv.arrow([(22, 33), (30, 33)], color="black", lw=0.6, head=1.0)               # same weight as the boxes
axs = cv.axes_grid(16, 6, 64, 14, 1, 3, sharey=True, gap=(4, 3), col_titles=["read", "write", "scan"])
for ax in axs[0]:
    ax.plot([1, 2, 4, 8], [1, 1.9, 3.6, 6.5], **series_kw(0))
assert not cv.overlaps() and not cv.text_overlaps() and not cv.wire_crossings()
cv.save("figures/fig2")                              # .pdf (Type 42 fonts) + .svg + .png
```

Primitives by dimension (signatures are in `scripts/paperkit.py`; usage in visual-craft §7–§9):

- **Shapes and objects:** `box`, `hexagon`, `section`, `group`, `tab`, `chip`, `matrix`, `vec`, `trap`, `cuboid`,
  `fmap`, `num_matrix`, `tokens`, `stack`, `doc`, `cylinder`, `diamond`, `graph`, `mini_plot`,
  `filetree`, `turn_strip`, `plate`, `tile`, `bubble`.
- **Panels:** `head` (bold letter, regular title, italic note; the default panel treatment), `rule`
  (hairline), `section` and `tab` (titled frames, where a frame is needed).
- **Text from the world:** `rich` (coloured terms, marked spans), `para` (the same, word-wrapped to a
  width), `listing` (code with line numbers and highlight bands), `greek` (grey bars for text the reader
  does not need).
- **Icons and callouts:** `icon_*` (`icon_user` and `icon_robot` for who speaks and who acts), `badge`,
  `callout`, `image` (rasters embedded unchanged at 600 dpi).
- **Arrows:** `arrow` (`dashed=`, `dotted=`, `both=`), `line`, `zoom`, `block_arrow`, `brace`, `op`.
- **Relations:** `thread` (a curve with a dot at each end, for "this matches or implies that"); its ends
  come from `cv.spans`, where `rich` and `para` record every marked span as (text, x0, x1, y).
- **Charts:** `axes`, `axes_grid`, `chart_legend`, `series_kw` / `SERIES_STYLE`, `curve_label`, `radar`,
  `spectrum`.
- **Series and keys:** `series` (one palette for a paper), `legend`, `phase_bar`, `chapter`.
- **Audits:** `overlaps`, `text_overlaps`, `wire_crossings`; command line `fill`, `counts`, `density`, `grey`,
  `compare`, `parity`, `swatches`, `caption`.

End every script with `assert not cv.overlaps() and not cv.text_overlaps() and not cv.wire_crossings()`.
Lay chips out with `cv.flow_chips`, never hand-picked x positions. Put the type scale and the stroke
weights in constants at the top of the script and pass them to every call (`size=`, `lw=`): the defaults
of several primitives differ, and a figure drawn on defaults ends up with eight sizes and eight weights.
Some values have no argument and must be overridden on the returned artists or drawn by hand when they
break a count: `bubble` strokes at 0.55 pt, `zoom` and `rule` at 0.5 pt, `box(sub=)` sets its sub-line at
size − 0.3, `chip` at size − 0.8, and `head(note=)` at size − 1.6 unless `note_size=` is passed.

Worked examples to adapt (each is `python scripts/examples/<dir>/<script>.py --out figures/<dir>`):

| Register | Example |
| --- | --- |
| Line art, one column: sequence chart of a protocol | `ray/render_fig7.py` |
| Idea schematic, one column | `lora/render_fig1.py` (one drawing, two states), `memt/render_idea_column.py` |
| Example-led text: four methods on one example | `react/render_fig1.py` |
| Example-led text: a motivating example as a scene (bubble, cards, threads) | `scene/render_retrieval_scene.py` |
| Field chart, one column | `toolspace/render_table1_column.py` |
| Claim chart; four-panel results figure | `memt/render_fig3.py`; `restyled/render_experiment.py` |
| Other example-led and line-art primitives (`listing`, `callout`, `greek`, `axes_grid`) | the `tx` and `g` blocks of the smoke test at the end of `scripts/paperkit.py` |
| Plate: architecture | `transformer/render_fig1.py` (three sizes, two weights, bare panels), `memt/render_fig4.py`, `restyled/render_attention.py` |
| Plate on an example × stage grid | `restyled/render_epoch_context.py` |
| Plate: agents and harnesses | `harness2/render_fig2.py`, `harness2/render_fig3.py`, `reharness/render_fig1.py` |
| Benchmark overview and pipeline (heads on the page, trays) | `groupassist/render_fig1.py`, `groupassist/render_fig2.py` |
| Showcase and figure series | `toolspace/render_fig1.py`, `proactive/render_*.py` |

The older `scripts/render_*.py` demos and `figure_scene.py` / `diagram_geometry.py` are contract and
geometry examples in a plain style; use them for their checks, not their looks
([advanced-examples.md](references/advanced-examples.md)).

**Generated images** are for the showcase register only: a matched set of 3–7 icons or vignettes from one
style spec, no text in the pixels, a label beside each, a vector fallback in the script, placed with
`cv.image`. Use real photos and screenshots for data, inputs and environments. Run
`python scripts/codex_images.py check` first and follow [image-generation.md](references/image-generation.md).

### 6. Review and revise

The first render is a draft. No figure is delivered without at least one revision made after looking at the
PNG. Open the exported PNG at full resolution, in crops, not only as a downscaled whole. Judge the PNG or
the PDF; the SVG keeps its text editable, so a viewer without the figure's font sets it differently.

- **Standard.** `python scripts/paperkit.py compare assets/models/<model>.png fig.png side.png`, open
  `side.png`, and say which of the two looks more finished, which uses its area better, and which a reader
  would remember. Where the model wins, name the region of yours that loses and fix it.
- **Fill.** `python scripts/paperkit.py fill fig.png <width in mm>` (add `chart` for a figure of plots). It
  exits 1 when the placement is mostly blank. The fix is larger objects, a spine, or a narrower figure;
  never decoration.
- **Cold read.** Whoever drew a figure cannot see it fresh. If the harness can start a fresh agent or a
  second model, give it only the PNG, the caption and the model's PNG (not the brief, not the script, not
  this conversation) and these questions; otherwise answer them from the PNG at print size before
  rereading the brief. One fresh read is required, on the first complete draft; later rounds may be your
  own look at the regions it named. A 1,600-pixel-wide copy is enough for the reader.
  1. What is the one message? It must match the brief's without help from the caption.
  2. Where does the eye land first? It must be the hero.
  3. What is drawn as an object, and what is only written? Every concept in the message must be drawn.
  4. Could LaTeX set this as a table? Could any part of our method be deleted without the rest noticing?
     (Numbers can always go in a table. The answer is yes only if nothing else would be lost: no link,
     position or drawn object that carries the reason. A prior-work lane is tied in by starting from the
     same input object as ours.)
  5. Which three regions look weakest (empty, cramped, pale, misaligned, wordy), and what fixes each?
  6. Would this figure look at home beside the model figure in a best-paper talk?
  A "no" or a wrong answer on 1–4 or 6 sends the figure back to step 2 or 3, not to a restyle.

- **Science.** Trace every value and edge to evidence. Check units, denominators, intervals, pairing,
  omitted conditions and caption scope.
- **Count.** Hues, stroke weights, text sizes, arrow styles, icon families, panel treatments, against the
  budgets in visual-craft §14. `python scripts/paperkit.py counts fig.pdf` reads the text sizes and stroke
  widths from the export.
- **Craft.** Walk the checklist. Run `python scripts/paperkit.py density fig.png` and compare the white
  share with the register's range; run `grey` for a field chart; for a redesign run `compare`, and `parity`
  when the source is a showcase or illustrated figure.
- **Geometry.** The three `cv` audits pass; then look for what they cannot see: clipped labels, a label
  nearer to a neighbour than to its object, a scattered hole, a wire through text drawn outside paperkit.
- **Depth.** Trace one object through every panel and reconstruct the operation the title claims.
- **Artifact.** `python scripts/check_figure.py fig.pdf --expected-width-mm 84 --min-font-pt 5` for size
  and fonts; SVG text is editable; the figure, its gap and its caption fit the text block together.

Fix the most consequential defect, render and look again. Stop when the cold read finds nothing that
changes what a reader understands or how finished the figure looks, and the checks pass; or after four
renders, and then say what remains.

### 7. Deliver

Vector PDF, editable SVG and PNG preview; the script and its inputs; a caption that opens with the claim
and defines every encoding the art does not label (visual-craft §12; `paperkit.py caption` exits 0); alt
text; and the design decisions in a few lines: message and hero, register, palette roles, type scale,
where the white space goes, arrow styles, the model it was compared with, what the cold read found and what
changed because of it, remaining limits. Confirm every delivered file exists and opens.

For a critique, lead with the defects that change what a reader understands, point to the region, and
separate what was inspected from what is inferred.

## Completion gates

- Data, topology and caption agree; illustrative content is unmistakable.
- The five-second message has a visible hero, made by difference.
- One register, matched to the venue and width; every count within budget or justified.
- Labels are legible at final size (labels and legends ≥ 5.8 pt, nothing under 5 pt); white space is
  grouped; no outer frame.
- Every colour, line style, hatch, icon and numeral is defined in the figure or its caption.
- The picture sentence passes the table test and the islands test; every concept in the message is drawn.
- The render has been revised at least once after a cold read, has been compared with a model figure, and
  passes `paperkit.py fill`.
- The export has been opened and inspected; the audits pass; unavailable checks are disclosed.
- The figure regenerates from preserved inputs and editable source.

Do not present visual polish as a validated result or promise a review outcome.
