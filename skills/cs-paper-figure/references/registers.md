# Registers and figure families

[visual-craft.md](visual-craft.md) holds the rules every figure follows. This file holds the rules for one
kind of figure at a time. Find the register in visual-craft §2, read its section here, and skip the rest.

Model figures are cited by paper and figure number; the full list with venues is in
[venue-study-2026-11.md](venue-study-2026-11.md).

| Section | Register | Families |
| --- | --- | --- |
| [1](#1-line-art) | Line art | Layer cake, planes, memory map, decision diagram, state machine, schedule timeline, protocol storyboard, sequence chart, code figure |
| [2](#2-idea-schematic) | Idea schematic | Repeated object, ghosted alternatives, phase diagram, geometric intuition, order chain |
| [3](#3-example-led-text) | Example-led: text | Annotated example, example × stage grid, method comparison on one example, single-column Figure 1, taxonomy grid |
| [4](#4-example-led-interfaces-and-studies) | Example-led: interfaces and studies | Rebuilt screenshot, callouts, interaction storyboard, study design, procedure timeline, participant plots |
| [5](#5-image-led) | Image-led | Teaser, comparison grid, inset zoom, labels and arrows on pixels, render storyboard, geometry diagram |
| [6](#6-plate) | Plate | Architecture overview with detail row, section frames, tensors and maps, key strip |
| [7](#7-contrast-state-and-construction) | Plate, for benchmarks | Existing-versus-ours, non-linear process, task cut, workspace state, construction pipeline |
| [8](#8-showcase) | Showcase | Isometric plates, logo tiles, radar envelopes, illustrated stages, what gets a figure chosen |
| [9](#9-evaluation-figures-of-benchmark-and-agent-papers) | Charts of benchmark and agent papers | Leaderboard, row-aligned measures, quality against cost, table-chart, matrix, concept plot, learning curves over a stream |

## 1. Line art

Systems, networking, PL, databases, theory and data-structure figures. White ground, white or unfilled
shapes, one black stroke weight, black text, and colour held back for the one thing that is new or wrong.
Build with `ROLE["line"]` boxes (`cv.box(..., "line", radius=0)`), `cv.line`, `cv.arrow(color="black")`.

- **Width first.** Most are 84 mm wide and 18–57 mm tall. Text 5.8–7 pt; boxes as small as 2.5 mm high
  with 0.4–1.5 mm padding. Use a module: every box a multiple of one unit.
- **One stroke weight** between 0.4 and 1.0 pt for boxes and arrows alike (pass `lw=` to both; the
  defaults differ). Check by counting.
- **Colour only what is new.** One red object in a black figure is enough. If the paper has a palette
  (four hues in PipeMorph), the same hues appear in its charts.
- **State is a border style plus a flat fill**: solid / hatched / dashed / dotted, defined in a small key.
- **No icons, depth, gradients, shadows or cards.** A word, a shape or a numeral does the job.

Families:

- **Layer cake.** Horizontal bands separated by hairlines and named at one edge (User / Kernel / MMU).
  The interface is a shape that straddles the boundary (`cv.hexagon` on the line). Lanes may be pale
  tints 6–11 mm high, 2.5 mm apart (CortenMM 3, AnyBlox 4).
- **Planes.** Control plane and execution plane are two dashed frames titled in bold italic at the top
  left. Solid arrows are control, dotted are data; colour marks the phase; arrows are numbered in their own
  colour and the key shows a sample of each (PipeMorph 13).
- **Memory or address-space map.** One row per level (physical, system, virtual), segments as square
  cells with the name inside, projection lines dropping between rows, a permission key, and circled
  numerals ①–⑥ that reappear under the arguments of the function they explain (AnyBlox 4).
- **Decision diagram, tree, page table.** Black line art with no fills: node shape gives the kind, line
  style gives the edge meaning (solid = true, dotted = false). 91–96 % white (NDD 4, Tree Borrows 1).
- **State machine.** States as bare words or small rounded boxes, transitions labelled on the line.
- **Schedule timeline.** Time on x; rows are stages or actors; cells are operations coloured by type with
  the id inside; idle time is the lane showing through. Stack the baseline run and the perturbed run on one
  axis so the gap is visible (PipeMorph 5). For a protocol, arcs over a time arrow, the failing run ending
  on a red × (OSCAR 5).
- **Protocol storyboard.** Two to six panels of the same drawing with one change each, separated by a
  rule, each titled with a numbered sentence. Grey out what is no longer live (CortenMM 7, Semisolates 2).
  It stops fitting when components × panels outgrow the column: nine boxes in eight phases cannot hold
  5.8 pt labels in 84 mm. Use a sequence chart then.
- **Sequence chart.** For a protocol with many actors and many messages in one column (Ray Fig. 7 has nine
  and seventeen). One lane per component, named at the top and again at the bottom, grouped by node under a
  short rule; grey lifelines; time runs down, one message per row, from a dot at the sender to the
  arrowhead. Step numerals and the paper's verb for each step sit in one aligned column at the left. State
  is drawn in the row that creates it: a table entry, an object in a store. Solid and dotted arrows keep
  the source's planes (`cv.arrow(dotted=True)`), and one hue marks the plane the claim is about. Worked
  example: `scripts/examples/ray/render_fig7.py`.
- **White share with scope tints.** A pale grey column or lane behind a node counts as tint in `density`
  and can take a line-art figure from about 90 % white to about 60 %. That is fine when the tint shows
  what belongs to which node.
- **Code figure.** `cv.listing`: monospace, at most three syntax colours, no background, line numbers the
  text cites. Add one device: highlight bands (red/green for before/after), or the data structure beside the
  code with identifiers in the same colour (CortenMM 6, NDD 2, Tree Borrows).
- **Evaluation charts** in this register are field charts (visual-craft §11): `cv.axes_grid`,
  `series_kw`, one legend row, greyscale-safe.

## 2. Idea schematic

The figure that explains an idea before the paper proves it: Figure 1 of an analysis paper, the intuition
behind a theorem, a failure mode. Very few objects, large type (8–11 pt at full width, 6.2–8 pt in a
column), 85–90 % white. This is a column register: with about ten objects, draw it at 76–85 mm. It earns
the full width only with its measurement beside it or when the drawing is repeated per condition.

- **Seven things, not seventy.** Aim for the economy of 2503.14858 Fig. 2: seven bars, three words, two
  multipliers. Label things in place; a key row of up to three samples is fine, a boxed legend means there
  are too many kinds of thing. (A mechanism drawn on a time axis may need one sample per kind of mark;
  five is the most seen.) When the drawing is repeated, the count is per panel (about ten), and a
  figure of large filled shapes sits nearer 75 % white than 85–90 %.
- **A merged state** of two coloured things is the first thing's fill hatched in the second hue, with a
  clear band for the label (LoRA: `W₀ + BA`). Worked example: `scripts/examples/lora/render_fig1.py`.
- **One object, redrawn.** Draw the tree, chain or interval once per condition and change only the state
  the claim is about. Alternatives not taken are the same shapes at 20 % strength (`#D9D9D9`, a 20 % tint
  of the hue). A red ✗ on the pruned branch (2504.13837 Fig. 1, Flexibility Trap 2).
- **Borderless flat shapes** on white for nodes and containers, or grey shapes with a black border; no
  pale-fill-plus-outline boxes. Drawn nouns (a grid, a token row) keep the lines that make them legible.
- **Transitions carry the claim.** An arrow between two states may hold a short coloured italic phrase
  ("more efficient sampling", "reduced scope"). Reverse the arrow for the cost.
- **Discs for discrete units**, tall rounded bars for layers, a grey bar in drawn brackets for a vector, a
  tinted dashed rectangle for an interval or a product of intervals.
- **Pair it with the measurement.** Put the chart the schematic predicts beside or under it, in the same
  colours (schematic 60–65 % of the width, chart 30–35 %).

Families:

- **Phase diagram.** Filled regions in two or three pale hues with the regime name written inside;
  boundaries as black curves labelled on the curve in a white rounded box (`curve_label`); no ticks in the
  schematic version, measured points added in the data version, same fills in both (2505.17638 Figs. 1, 3).
- **Qualitative curve plot.** No ticks, two named axes whose titles take the colour of their curves, an
  interval marked by a double-headed arrow with drop-lines, regime names in italic at the place they hold.
- **Geometric intuition.** Lollipop vectors from an origin, dashed basis arrows, a slope triangle with
  its value, angles as arcs, math set on the object (2505.10465 Figs. 1, 2; IMS 2, 3, 6).
- **Iteration storyboard on a function plot.** Three panels, a tinted box that shrinks, drop-lines, symbols
  as tick labels, one panel's output marked as the next panel's input (Polar Express 2).
- **Order chain.** Discs on a line with black arrows for the default order, one coloured arc for the
  jump, ghosted branches for the paths not taken.
- **Displacement scatter.** Before-to-after arrows per item, a halo per cluster, a corner summary with the
  delta (2505.06120 Fig. 1).
- **Timing diagram.** For a claim about speed, latency or scheduling. One row per actor (Target, Draft) on
  a shared time axis, drawn twice at one scale: prior above, ours below. Work is a pale filled block with
  its name inside, idle time a hatched grey block, and the claim is a double-headed arrow labelled "saved"
  between two dashed verticals. Two text sizes, three fills, one outline weight; about 4 : 1 (JetSpec++
  Fig. 1: 142.6 × 37 mm, 6.4 and 7.7 pt). This family is full width and made of filled blocks, so the
  register's figures above do not apply to it: expect 65–80 % white and under half the canvas blank.
  Compute every block from the step times and assert the two end times; show a hit and a miss when the
  method can miss (the kept block saturated, the discarded one ghosted and struck out). Hatch with
  `cv.box(..., hatch="/////")`. Model: `idea_timing_diagram.png`
  (`scripts/examples/timing/render_speculation.py`).
- **Landscape trio.** The same pair of axes three times along one long arrow that names the control
  variable; only the curve changes (two wells, one well, a flat basin); the regime's name is a coloured
  headline over each; dotted drop-lines run from the curve's minima to real samples framed in the regime's
  hue, and that frame colour is the legend for every later figure (Diffusion and Associative Memory
  Fig. 1). Redraw its colours: the source uses pure red, green and blue.
- **Search tree with outcomes.** Internal nodes neutral, leaves green or red with ✔ and ✘, forward arrows
  in one hue and the backup arrows beside them in a second, a two-sample key above the tree. The node
  whose value is being computed is ringed, then drawn again, larger, as the input of the next stage. A
  matching loss is a spring between the two distributions (`cv.spring`), each drawn as a three-bar strip
  with its reference line (TreeOPSD Fig. 2).
- **Stories with one geometry.** Two or three small stories drawn with identical layout (inputs on top, a
  pipe, an end node, a "first → later" axis), one thing changed in each, a bold claim over the set and one
  reading line under each story. Where a width is the quantity (a pipe that thickens as a feature
  strengthens), say so in one line: the stroke budget counts structural strokes, not data.
- **Two factors: a 2 × 2 with drawn axes.** Arrowed axes with category ticks; all four cells repeat one
  small drawing and change one thing per axis (Work Agents Fig. 2). Four free scenes do not do this.
- **Concept plot** for a new metric: [§9](#9-evaluation-figures-of-benchmark-and-agent-papers).

## 3. Example-led: text

NLP task, method and benchmark figures. The example text is the object; the figure's job is to typeset it
and mark it. Rules for marking are in visual-craft §10.

- **Single-column Figure 1** (76–85 mm wide, 40–75 mm tall): one example, read top to bottom in three
  tiers (input, what the method does, outcome), about 9–15 boxes, example text 6.7–7.5 pt, content filling
  the column to within 1 mm (CoT 1, REL-A.I. 1).
- **Example × stage grid.** Rows are two examples from different domains, columns are stages, column
  headers are 8–9 pt bold grey, row labels are grey pills at the left, a hairline between rows, and no
  arrows at all (HALoGEN 1). Each cell shows the same text with one more layer of marking.
- **Motivating example: draw the scene, not the table.** A figure that shows one input, a few stored or
  candidate items and what two systems do with them is a scene with actors. Rows of sentences with a status
  column and score bars is a table and should be typeset as one.
  - The input is said by someone: a speech bubble with the speaker's glyph (`cv.bubble`, `cv.icon_user`).
  - Example text at full width is 7–8 pt; in a column, 6.7–7.5 pt.
  - The items are objects in a place: cards in a store, documents in an index, turns in a thread, each a
    white tile on one pale tray, the same size.
  - **The relation the claim is about is a drawn link.** Mark the span in the input and the span in the
    item with the same tint, and join them with a thread (`cv.thread`, ends taken from `cv.spans`), with
    the relation named on it ("shares words", "contradicts", "answers it"). The baseline's thread and
    spans are grey; ours take the figure's one hue, so the eye lands on what ours found. The two threads
    landing on different cards is the figure.
  - **Draw the cards once**, side by side under the input, with both systems' marks on the same set. Two
    copies of the list, one per system, is the table again. A thread arrives vertically, so each card needs
    clear space above it; order the cards by where their spans sit in the input so the threads do not
    cross (reordering unordered items is fine; say so if the paper numbers them), and start each card's
    text with its marked span where the wording allows.
  - **The system's verdict and the item's status are different marks.** The system's choice is a ring in
    its hue and a name tab on the card's top border with the tick or cross inside ("Ours: rank 1"). What is
    true of the item itself ("no longer true", "answers the question") is a tag on its bottom border, the
    one that matters filled dark. Scores are small bars or numbers inside the cards, secondary to the marks.
  - The hero is the item ours finds: the only card with the hue.
  - A control case (a look-alike input that should change nothing) repeats one card beside its own bubble,
    under the main scene, joined by a dashed line where the thread would be.
  - Width: three cards side by side need 140 mm; in a column, two cards, or three stacked with the threads
    run down a side margin. Mark spans only where the paper says why a system ranks an item; a span that is
    your reading of the example is said to be so in the caption.
  - `cv.bubble` takes plain text: for marked text draw it empty (`text=""`, `w=`, `h=`) and lay `rich` or
    `para` over it. Worked example: `scripts/examples/scene/render_retrieval_scene.py`; model
    `assets/models/example_led_scene.png`.
- **Voices.** Prompt in the body face, model output in monospace, what a tool or the environment returned
  in the body face in grey, a human turn in a speech bubble with a tail. Box a model output only when
  several outputs must be told apart inside one cell; otherwise a plain head with a hairline under it
  (`cv.head(..., rule=w)`) and the page as ground.
- **Method comparison on one example** (ReAct 1). Say the question once across the top. Give each method
  a head and its trace: role labels (Thought, Act, Obs) in a gutter, the text wrapped beside them
  (`cv.para`), a rail beside every line of reasoning, the verdict glyph straight after the final answer.
  Give ours the widest column and line up the last lines of the columns, so the final answers sit side by
  side. Transcribe the paper's text exactly; elide only with a visible ellipsis. Worked example:
  `scripts/examples/react/render_fig1.py`.
- **Height.** About 1,700 characters of trace at 6.7 pt monospace need about 88 mm at 140 mm wide. If two
  examples do not both fit at readable size, draw one and say so, or make two figures.
- **Three tints at most**: neutral blue = the unit under study, green = supported, red = error; tick and
  cross glyphs at the right end of the span; the caption repeats the tints on its own words.
- **Largest block = the contribution.** If the paper's point is instance-specific criteria, that card
  takes half the figure (BiGGen 1).
- **Aligned verdicts.** One real example as numbered rows split into two voices (natural language in the
  body face, its formal counterpart in monospace), the failing row tinted; beside it the checker's column
  with ✓ and ✗ at the same heights and the first failure named in words; the output drawn as the same
  ticks and crosses in miniature. One accent, on the judged objects only (LeanPRM Fig. 1; visual-craft §9).
- **Stepwise edit.** The same listing in every step, only the changed block tinted, elisions said, the
  invariant named in an eyebrow (Aligning Autoresearch Fig. 7; visual-craft §10).
- **Token-level run.** One real sentence carried token by token through every column, a fill for tokens
  that differ from the target, a heavier outline for tokens that are fixed, "=" and "≠" between compared
  cells (JetSpec++ Fig. 4). Keep it at 5.8 pt or above by eliding columns, not by shrinking.
- **Behaviour dossier.** The verbatim board, terminal or code with file and line, two or three callouts,
  one typographic role per kind of text, a claim sentence as the title and the entity's colour on its
  sub-head and its left rule (Agent Plasticity Figs. 8, 12–15). Half a page at most in the body.
- **Taxonomy grid.** Equal cards on a grid, chips of one width inside, one hue on a ramp for an ordered
  level. Nine unrelated hues is the failure (BiGGen 2).
- **Results** in this lane are usually default plots; build them as claim or field charts
  (visual-craft §11) in the same face as the diagrams.

`paperkit`: `rich(..., family="monospace")` with marks, `para` for wrapped text, `head`, `rule`, `bubble`, `chip`, `tab`, `icon_check`,
`icon_cross`, `stack` for "many of these". A minimal use of `rich`, `listing`, `callout` and `greek` is the
`tx` block of the smoke test at the end of `scripts/paperkit.py`.

## 4. Example-led: interfaces and studies

HCI system papers and user studies.

- **Rebuild the screenshot; never shrink a window.** Redraw the interface at figure scale so its text
  prints at 6–6.5 pt, keep only the part the paper discusses, and replace everything else with grey bars
  (`cv.greek`). Float the window on a soft shadow instead of a border. A full window scaled into a column
  prints at about 3 pt and carries no information (Cocoa 2 against DocWrangler 2).
- **Callouts** (`cv.callout`): one accent hue the interface does not use; discs of one size (about 5 mm in
  a full-width figure, 3.5 mm in a column) with a white letter; a leader ending in a dot; discs lined up on
  one vertical in white space beside the window. A region takes a bracket; a relation takes a line with a
  dot at each end. The caption is a lettered walkthrough.
- **Interaction storyboard.** Numbered step panels with a tab on the border; a curved arrow in the accent
  hue that starts at a drawn cursor and carries the action as a pill ("click"); the result panel largest
  (Cocoa 3).
- **Teaser.** Abstract the interface to a skeleton: bars for text, colour kept only for the states that
  matter (owner, edit, needs help).
- **Join key.** The same lettered badge on the problem, on the feature that answers it and in the caption.
- **Study design.** Constructs × studies: rows aligned across two frames, the construct names in the
  gutter with an arrow in and out, quotes as stacked cards tagged as examples; no hue needed (Reliance 1).
- **Procedure timeline.** Activities on one row with durations, what each yielded on the row below,
  same-session stages boxed together. Keep icons under 3 × cap height.
- **Participant-level plots.** One strip or stacked bar per participant, same order in both conditions,
  a normalised axis, grey for uncoded time, the legend carrying each category's share (Cocoa 8). Baseline
  categories are desaturated versions of the same hues.
- **Ratings.** Show the response counts (diverging stacked bars centred on neutral), not only a mean bar;
  significance brackets with stars, defined in the caption.

## 5. Image-led

Vision, graphics, robotics and generation papers. The images carry the content and the colour; the vector
layer stays neutral and small. Place every image with `cv.image` (it embeds pixels unchanged).

- **Teaser.** One hero render at 60–80 % of the area; inputs as a thin strip of thumbnails on one side
  (about 19 × 14 mm), outputs as small satellites on the other; leaders or a wedge from input to hero. No
  frames (VGGT 1, TRELLIS.2 1).
- **Comparison grid.**
  - A narrow input column (11–34 mm), then equal method cells (17–68 mm).
  - Column headers once, above the images, in the body face at 8–9.5 pt, regular; only ours bold. Gap to
    the image 0.3–1.4 mm. Row labels rotated at the left.
  - Two gutter widths: 0–1 mm inside a group, 1–3.6 mm between groups. No boxes around images.
  - One camera, pose, crop and backdrop per row, so only the method changes.
  - Ours first after the input or last, the same size as the rest.
  - A missing result stays a cell with a grey note ("N/A"), never a gap.
- **Inset zoom.** Box the source region in a saturated colour the image lacks (1.4 pt), magnify 2–3.5 ×,
  and park the zooms in a corner or a row of their own with the same colour and stroke. One colour per
  method (magenta ours, cyan baseline). No leader lines (IMS 27).
- **Labels on pixels** go on an opaque plate tucked in a corner: a white pill 3.9 mm tall for 8 pt text,
  inset 0.6–0.9 mm. Bare text only on a white image background.
- **Numbers and verdicts on the cell**: runtime in the frame's top-right corner; a full-width red or green
  bar with white text under a render; a small table in the empty corner of the figure.
- **Arrows over pixels** are free curves, 1–2 pt, with filled heads 4–6 × the stroke (the upper half of
  the general 3–6 × range); see visual-craft §9 for keeping them visible.
- **Pipeline over real pixels.** Keep the model as two or three plain boxes and spend the space on the
  real input and output. Give each query or signal one hue and repeat it as chip, wedge, timeline dot and
  mark on the render; ghost the frames that are not being discussed (D4RT 2).
- **Render storyboard.** Equal panels, fixed camera, one arrow style between them, a numbered label per
  step, a verdict glyph under each where steps are checked (IMS 8, BrickGPT 3).
- **Geometry diagram.** No frames; the two shapes in two fixed hues for the whole paper; math set on the
  curve; schematic axes without ticks; tick and cross glyphs on the valid and invalid cases (IMS 2, 3, 6).
- **Chart with image callouts.** Thumbnails hooked to data points by a thin line.
- **A sequence** is a strip of frames with an ellipsis or a ghosted frame for the ones left out.
- **Text from the world** (prompts) in quotes or a distinct face, the changed word in an accent.
- **Charts** are bare, about 85 × 40 mm, direct labels, ours the only accent.

White share depends on the family: framed image grids 22–31 %, silhouette grids on white 43–62 %,
pipelines 49–72 %, geometry diagrams 54–70 %. `density`'s crowding hint does not apply to image grids.

## 6. Plate

Full-width method and architecture figures of model papers, and agent or benchmark overviews. Role colour
families, drawn tensors and maps, section frames. From a study of 23 vision and multimodal method figures
([architecture-study-2026-11.md](architecture-study-2026-11.md)) and the lab figures in
[craft-study-2026-10.md](craft-study-2026-10.md), corrected by the venue study: keep the plate light.

- **Spine first.** Choose one concrete item (a turn, a request, a file, a token) and draw its whole path
  through the system as one connected line of objects from the left or top edge to the outcome. Everything
  else attaches to that line. A write path, a store and a read path are one spine with the store in the
  middle as the hero, not three panels. A decision rule, a cost model or a schedule opens by zoom rays from
  the object that applies it. Prior work is a short ghosted or neutral lane beside the part of the spine it
  replaces, ending on a verdict, never a box in a corner.
- **Floors.** The store, state or model that the paper is about is the largest object (with its zoom, about
  40 % of the area). Stages are cards with a role fill, not bare words with a subtitle. A full-width
  plate has at least five drawn objects on its spine and passes `paperkit.py fill`. Models, in
  `assets/models/`: `plate_agent_system.png`, `plate_agent_loop.png`, `plate_architecture.png`.
- **Layout.** Overview pipeline across the top (45–65 % of the height), a row of two to four equal-height
  detail panels opening the new modules, a glyph key strip along the bottom. Zoom rays or a shared hue link
  each detail panel to its block.
- **The page stays white between modules, and the modules are filled.** Each module's card or tray takes
  its role `fill`; the gutters and the page stay white. Group by white space and fill-on-fill first; frame
  second. Keep white between 40 % and 75 %: below is crowded, above is a line drawing that has not become a
  plate.
- **Heads on the page, trays under them.** For a row of steps or stages: a plain head on the white page
  (number, bold name, the count), then one pale borderless tray per step, with the things the step handles
  as white borderless tiles on the tray. Heads inside the trays push white under 40 %; no trays at all
  reads as a page of text (about 83 % white, outside the plate's range). Worked example:
  `scripts/examples/groupassist/render_fig2.py`.
  The trays may go when every stage is itself a drawn object on one thin through-line with a counts strip
  beneath it: FrontierPhysics Fig. 2 has five numbered heads, five different drawings, no container at
  all, and is 83 % white.
- **Lanes that merge.** Prior work and ours as two stacked lanes, each a pale tray in its own hue with
  the title set in that hue; the stages they share are drawn once, to the right, at the height of both.
  The same glyphs in both lanes, so the eye finds the one that moved (noise added into the weights above,
  into the logits below); the cost of each lane written in it; a rejected candidate ghosted along with
  its arrow (Neural Thickets Fig. 1).
- **Overview strip and braces.** A strip across the top shows the whole method as one row, repeating the
  object of the paper's Figure 1; labelled braces under its parts ("(b)", "(c)") name the lower panels
  that enlarge them; dotted hairlines separate the panels. This is the cure for islands when zoom rays
  would cross (JetSpec++ Fig. 2).
- **Results on the schematic.** When the paper measures something per component, print it in the
  component and colour the boxes by role class; a thick spine arrow carries the stream the components
  read from and write to (Neural Thickets Fig. 3: 7 pt, three hues, strokes 0.47, 1.17 and 1.94 pt). The
  same drawing with new numbers serves the appendix.
- **Define a glyph once, then use it.** An abstract quantity gets a small data glyph (a three-bar
  histogram, a ring of dots with one ringed) defined in a margin figure of its own and then used in the
  architecture and again in the inference figure, where the parts not sampled are ghosted (Parallel
  Language Models Figs. 2, 4, 7).
- **One level of container, and a head with three slots** (visual-craft §7): eyebrow, title, cost.
- **The thing being followed takes the one accent.** In a pipeline that runs one example through every
  step, colour that example's object in each step and leave the structure slate and black. A thing that
  has a hue in a sibling figure may be drawn neutral here when it is not what this figure follows; it may
  not take a different hue.
- **Section frames** (`cv.section`): a dashed border in the module's hue with the title on a tab on the
  border. Name it as the paper does, with the acronym. One panel treatment for the whole figure.
- **Role families.** Inherited parts neutral; the contribution in its hue; parameters coloured in place
  on the components that own them, not listed in an inventory box. Text black, except words naming a hue.
- **Drawn nouns.** Feature tensors as `cuboid` with H×W×C in italic math; layer runs as slabs; encoders as
  `trap`; fused features as a gradient between two source hues.
- **A data object in every detail panel**: a feature or attention map, a numeric matrix with the winner
  bordered, a mini distribution, real tokens, a thumbnail. A panel of only boxes and arrows explains wiring,
  not the operation.
- **Mechanism storyboard on the object**: `M → faded M → M with a dashed row ⊕ (v × k) → M′`, with the
  typeset equation underneath, its terms coloured by role (`cv.rich`).
- **Key strip** (`cv.legend`) defines every circled operator, state icon, dash meaning and abbreviation
  once. **Phase bar** (`cv.phase_bar`) names the stages once.
- **Saturation.** Blocks at `soft`, one or two hero blocks at `mark` with white text.
- **Discipline:** text ≥ 5.8 pt (source figures often fall to 4–5 pt), one meaning per hue, no wire
  through text, one icon family, at most two zoom levels.

## 7. Contrast, state and construction

Benchmark and dataset papers explain what is different about the tasks. From ARE-bench Figs. 1–3
([arebench-study-2026-11.md](arebench-study-2026-11.md)).

- **Contrast figure.** Baseline column narrow (about one third), ours wide. Shared rows named after the
  claim's dimensions, set once as rotated labels in a bracket, separated by a dashed rule spanning both
  columns. Same objects on both sides; the difference is their arrangement. End each column on a verdict
  pill (`icon_cross` red, `icon_check` green).
- **Non-linear process.** Stages in canonical order; jumps as arcs above (back) and below (skip) the row,
  each with a `badge` numeral keyed to a request list under the row.
- **Cut point.** `cv.turn_strip(x, y, w, n, cut)` shows history, the cut turn and the unseen future.
- **Real artifacts.** Files, commands and requests in monospace inside window chrome (`cv.filetree`);
  state per row as a coloured tick and a right-aligned italic tag.
- **One accent for the task or ours**, shared by the highlight region, the task bar and its badge, and
  used by no stage or category.
- **Hidden inputs** carry `icon_lock`, identically in every figure of the paper.
- **Step cards.** Bold numbered step at the left, italic output type at the right; rules printed in the
  card so the text can cite them.
- **Loops as rails** around the outside of a column, labelled on the line.
- **Results.** One model = one colour in every panel.
- **Counts under every stage** (visual-craft §5), and the last stage is the finding: a small chart of
  the failure modes with their shares, so the pipeline ends in what the benchmark found (FrontierPhysics
  Fig. 2).
- **The task as its folder.** Draw the real task directory as nested file chips and let one fill answer
  one question for every file: who can see it. One key line directly beneath; a lock glyph for what is
  withheld; rows aligned so each part of the task sits beside the checks that grade it; the same file
  chips reused as the inputs that drop onto the pipeline's nodes in the next band (FrontierPhysics Fig. 3).
- **A stream of windows.** Environment windows as equal cards, each with a strip of capsule tokens
  (serving in one tint, test in another) and its policy chips; one policy followed across the windows by a
  dotted arrow that says what happened to it ("withdrawn, then returns"; ServeLearnBench Fig. 2).

## 8. Showcase

Teaser and overview figures of system and benchmark papers, and illustrated survey figures, which sell one
idea at a glance. From ToolSpace Fig. 1 ([toolspace-study-2026-11.md](toolspace-study-2026-11.md)) and
*Proactive AI*
([figure-series.md](figure-series.md)).

- **Layering gets depth.** "A layer between X and Y" is stacked isometric plates (`cv.plate`) with objects
  standing on them as tiles (`cv.tile`) and calls and returns in the gap. Everything else stays flat.
- **Real things get their marks**: logo tiles with names (visual-craft §8).
- **Envelope claims keep the radar**, made honest (visual-craft §11).
- **Bars carry identity**: the model's mark above the bar, the value on it, a ghost outline for the
  reference condition when the claim is a drop.
- **Illustrated stages.** Each stage shows the agent doing the thing; solid colour headers with white bold
  text (the one register where a header band belongs); generated or drawn vignettes filling each card edge to edge (`cv.image(..., fit="cover")`); dialogue
  as vector text (`cv.bubble`), never in pixels.
- **Surface.** Gradients on plates and bars only; pastel fields behind clusters; saturated colour for the
  hero and the path being followed.
- **Redesigns stay in this register** and pass `paperkit.py parity`. A showcase figure rebuilt as line art
  is more correct and loses.

**What gets a figure chosen** ([trending-study-2026-11.md](trending-study-2026-11.md)). Two paper-reading
feeds showed one figure for each of 28 papers and reports. What the chosen figures share, and what they do not:

- **Position first.** Nearly every pick is Figure 1 or 2. The figure a reader meets first is the one that
  travels, so the first figure deserves the most work.
- **A result is as good as a schematic.** About a third of the picks are charts with no diagram at all: a
  sorted leaderboard with logos, a staircase frontier, six curves with stars, one green bar among blue. A
  result chart alone on page 1 keeps its type at 8 pt; a chart squeezed beside a schematic does not.
- **Honest attraction** is content that reads at thumbnail size (visual-craft §1): a measured gap, two
  lanes that merge, real proof steps with one failing row, real spectrograms with the masks drawn on
  them, recognised marks beside a shocking scale. **Decoration** is what could be deleted without losing
  a fact: a rendered mascot, a planet per panel, contribution cards with numbered badges, a radar's
  meaningless polygon area. The decorated picks attract and then cannot be read: 81 % of the text in the
  densest one is under 5.8 pt.
- **Three template looks, and what to keep from each.** *Slide kits* (gradient header bands, fat block
  arrows, emoji, a dashed frame per panel, 9–19 text sizes): keep nothing but the real example in the
  middle. *Generated art* (glossy 3-D objects, paintings): keep one recurring noun at most (visual-craft
  §8). *Model-written HTML* (cream ground, small-caps eyebrows, pill badges, cards in cards): keep its
  good habits, which are claim titles, eyebrows that name what is fixed, and labelled reference lines;
  drop the nesting, the word count, the 4–5 pt text and the bitmap export.
- **A title-page illustration is not a figure.** One generated picture under the title with five short
  labels on leader lines may brand a survey; it carries one ordered list and nothing else. Do not number
  it, and do not let its style into the technical figures.
- **A ring of bars** (bars radiating from a circle, grouped by sector) is a showcase device: it earns a
  cover and costs every comparison across sectors, upside-down labels on the lower half and a legend
  lookup per bar. Use it only as a teaser with at most six bars per sector and the top values printed, and
  give the same numbers a row-aligned figure or a table in the body.

## 9. Evaluation figures of benchmark and agent papers

Benchmark and agent papers lead with their numbers: who wins, at what cost, and how behaviour changes over
a run. From the trending study ([trending-study-2026-11.md](trending-study-2026-11.md)); the general chart
rules are in visual-craft §11. Models in `assets/models/`: `chart_measure_rows.png`,
`chart_pareto_column.png`. Charts of this kind are full width at 140–170 mm and only 37–80 mm tall, or
one column. Type follows visual-craft §4: panel heads about 8 pt, labels 7–8 pt, ticks and notes 6–7 pt
(the models use 8.2 / 7.2 / 6.2 and 7 / 6); the same scale in every chart of the paper. A chart is not a
register and has no white-share range; `paperkit.py fill PNG WIDTH chart` is the area check.

**Who wins**

- **Leaderboard.** Sorted by the headline measure, the value printed at the end of each bar, the system's
  identity mark at its name. (Every value is printed when the figure stands in for the table; when the
  same numbers are also in a table of the paper, print only what the claim needs, visual-craft §11.)
  A sorted bar chart claims an order, so say which gaps are established: an
  interval on every bar (FrontierPhysics Fig. 1), or a bracket over the rows the test does not separate,
  in the paper's own words. If the paper reports only a spread over runs, the bracket says that ("within
  run-to-run noise"), not "tied" or "not significant". Colour is one of three things: the systems the
  claim is about in one hue with the field grey; the vendor's identity hue on every bar with the vendor's
  mark as the tick, kept in every figure of the paper and needing no legend (FrontierPhysics Figs. 1, 5,
  7); or, in a benchmark paper with no system of its own and no marks to show, one hue per model family
  with a dot at each name, the same in every figure, so that no hue changes owner when the next figure
  is about a different system. Never a different
  arbitrary hue per bar (Aligning Autoresearch Fig. 5: eight bars, eight hues, no meaning). With more
  than about eight systems, or names longer than a few characters, run the bars horizontally: names
  rotated 45° under vertical bars take a third of the figure's height and are read with a tilted head.
- **Row-aligned measure panels** (`cv.row_panels`). When each system has several measures, name the rows
  once at the left and give each measure its own panel on those rows, with its own x scale and the mark
  that suits it: a bar from zero for a score, a 100 % stack for outcome shares, a dumbbell between two
  thresholds or two phases, a lollipop from a reference value, a point with its interval for a difference.
  Only the bottom spine and a light vertical grid; a head per panel that names the quantity and unit, so
  the x axis needs no title. Order the rows to make the claim, not alphabetically. Past about eight rows
  add pale bands on alternate rows across all panels. Worked example:
  `scripts/examples/accelerate/render_table1_rows.py`.
- **A reference row** (human experts, an oracle, an upper bound) is set apart at the top in dark
  neutral, with a gap under it (give `row_panels` a fractional `n` and place the rows yourself), and its
  value drops through each panel as a dashed line. The other rows' marks may run from that line, so the
  stem is the gap; then one italic phrase over the first stem says which way it runs ("more harmful →",
  "← faster"). The headline gap is a dimension arrow with its number, drawn in one figure of the set and
  not repeated in the next.
- **A dumbbell or ordered-marker row carries its own key**: the labels sit over the marks of the first
  row (open = ≥ 2×, filled = ≥ 1.25×; E, M, L over early, middle, late), in that row's ink. No legend.
- **An ours band.** In a multi-panel leaderboard a pale band in our hue runs across every panel on our
  row; values are printed for ours and the runner-up only (AudioFM Fig. 3).
- **Outcome palette.** A run that failed is grey; runs that succeeded are one hue on a lightness ramp by
  how well (correct but slow → pale, fast → saturated). Keep that triple in every figure of the paper
  (Accelerate Bench Figs. 3–6).

**At what cost**

- **Quality against cost** (`paperkit.pareto_front`). Draw the front as a step line and shade the region
  it dominates; make the points on it full size with a dark edge and name them in place; keep the
  dominated points as the same marks, smaller and at about 45 % strength; put a small "better" arrow in
  the empty corner. Two factors take two channels (hue = method, marker = model) and the shape legend is
  grey. A step, not a diagonal: between two points on the front nothing cheaper reaches the higher value.
  Worked example: `scripts/examples/pareto/render_frontier_column.py`.
  Alternatives seen: a thick pale line under logo markers for the front, and two settings of one system
  joined by a thin line from a ghosted marker to a solid one (FrontierPhysics Fig. 5). Name tags must
  not sit on the front.
- **Draw the claim as a bracket or a band.** A Δ bracket at a fixed x between two curves with the gap on
  it; a shaded band between two x positions at equal score with "≈ 2.0× fewer steps" on a double arrow; an
  arrow from the baseline point to ours with the ratio on it, in our hue for a gain and grey for a
  regression, which is drawn and not hidden (MASS Fig. 2: 1.60×, 1.35×, 0.96×, 0.94×). In a
  quality-per-cost plot add the dashed iso-ratio line through the baseline: above it is better per token.
- **The operating point is a marker form**: the default setting, the chosen configuration or the
  full-scale measurement is one large open marker on its own line, which leaves colour for identity.

**Over a run**

- **A derived metric is marked where it is read.** A star on each learning curve at its saturation point,
  filled when reached and open when not, then the metric as bars in the same colours beside the curves
  (Agent Plasticity Fig. 1).
- **Phases of a stream are bands**, tinted in the colour of the task that is active in that segment, so
  the band and the curve it explains share a hue (Self-Evolving Agents Fig. 1).
- **A shared history is grey and the fork is coloured**: one dark-grey run up to the intervention, a
  dashed vertical naming it, then the two branches in two hues with a star at each branch's best point.
- **Smoothed over raw.** The fitted or smoothed line at full weight over the raw points or trace at about
  a third of it; measured range solid, extrapolation dashed with a pale band.
- **Paired units.** Each unit is a pair of dots joined by a thin line (best and last, before and after),
  the median a short black tick, the group size in the tick label ("New best (26)").
- **A series that occupies a tenth of the axis gets a zoom row**: the same panel underneath with that
  series alone on its own scale.

**Tables and matrices that are figures**

- **A table becomes a figure when its cells are marks.** Row heads carry the legend swatches or short
  codes, each cell holds a bar, a heat cell or a 100 % stack with its number, there are no axes, rows are
  sorted, exceptions sit apart at the bottom, and *n* closes the row (FrontierPhysics Figs. 4, 6, 10). A
  table of numbers in a figure float is still a table, and a chart beside three tabulars under one
  figure number is four things.
- **In a matrix, zero is a ghost tile and the argument is a rectangle.** Cells with nothing to say are
  pale and empty; the cells the text discusses carry a bold value; a dashed neutral outline marks the
  expected block and one solid accent outline the surprising one (Self-Evolving Agents Fig. 4).
- **An inventory is a tile matrix**: category rows with one chip per item, or a count per category with
  three named examples. A sunburst of 110 labels at 1.4 pt is a texture, not an inventory.

**Defining what is measured**

- **A concept plot defines a new quantity** before the data shows it: no tick numbers, the regimes named
  on the curves ("high P", "low P", "P < 0"), the formula on the plot, every annotation in the colour of
  the thing it names, and the same axes as the data panel beside it (Agent Plasticity Fig. 2).

**The paper, not the figure.** The strongest papers of the study are strong as sets: one toolchain, at most
two font families across all figures, one thing → colour table, one width. The weakest have nine font
families in eighteen figures, five visual languages in nine, or two systems that swap colours between
Figures 4 and 11. Audit the set before delivering any one figure ([figure-series.md](figure-series.md)).
