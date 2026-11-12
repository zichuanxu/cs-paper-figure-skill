# Visual craft: the rulebook

Read this before drawing. It is organised by design dimension: message, register, colour, typography,
layout, white space, shapes, icons, arrows, text, charts, captions. Numbers are at printed size.

The rules come from three rounds of measured study: AI-lab method figures
([craft-study-2026-10.md](craft-study-2026-10.md), [architecture-study-2026-11.md](architecture-study-2026-11.md)),
benchmark and showcase figures ([arebench-study-2026-11.md](arebench-study-2026-11.md),
[toolspace-study-2026-11.md](toolspace-study-2026-11.md)), and 29 award papers from NeurIPS, ICLR, ICML,
CVPR, ICCV, SIGGRAPH, ACL, EMNLP, NAACL, CHI, UIST, CSCW, SOSP, OSDI, NSDI, PLDI and VLDB
([venue-study-2026-11.md](venue-study-2026-11.md)). Ranges are what those studies measured; a budget or a
starting value is this skill's choice inside the range.

Implementation: [`scripts/paperkit.py`](../scripts/paperkit.py) provides the primitives named here, in
millimetres. Rules that apply to one kind of figure only are in [registers.md](registers.md).

## 1. The message and the hero

State the one thing a reader should get in five seconds before choosing anything else. Then decide which
single element delivers it. That element is the hero.

**Make the hero by difference, not by weight.** In the award figures the hero is the only coloured object
among black ones, the only solid line among dashed ones, the only unhatched bar, the block given most of
the area (55–80 %), or the last panel of a storyboard. None of them thickens the hero's stroke or adds a
shadow. If the hero needs a heavier outline to be found, something else in the figure is too loud.

Three ways to hold a message, in the order they should be tried:

1. **Repeat one drawing and change one thing.** The same tree, chain, page table, network or camera view,
   two to six times, with only the state that the claim is about changed. What is not taken, not live or not
   ours is the same shape at about 20 % strength (`#D9D9D9` or a 20 % tint), never a different shape.
2. **Run one concrete example through every stage.** One question, one program, one prompt, one scene. A
   grid of example × stage needs no arrows; reading order carries the flow.
3. **Put the picture of the idea beside its measurement**, on one grid and in the same colours: schematic
   row over data row, or schematic panel beside the chart it predicts.

In a comparison grid ours gets the same size and treatment as the baselines, on purpose. It is marked by
position (first after the input, or last) and a bold header.

If nothing is visibly the hero, the figure is not done.

## 2. Choose the register

A register is a coherent set of choices for ground, fills, strokes and type. Award figures do not share
one look; they share discipline inside a look. Pick the register before any style value, and never mix two
in one figure.

| Register | Where it belongs | Ground and fills | Strokes | White share |
| --- | --- | --- | --- | --- |
| **Line art** | Systems, PL, databases, theory, data structures; any 84 mm column | White; shapes white or unfilled; at most a few flat state fills | One black weight, 0.4–1.0 pt | 55–96 %, usually above 75 % |
| **Idea schematic** | ML theory and intuition figures; Figure 1 of an analysis paper | White; a few large flat shapes, borderless or black-bordered | One weight, 0.7–1.4 pt | 85–90 % |
| **Example-led** | NLP task and method figures; HCI interface and study figures | White; pale tints behind spans and cards | Thin or none | 50–80 % |
| **Image-led** | Vision, graphics, robotics: teasers, pipelines over pixels, comparison grids | The images; neutral greys for the vector layer | Module outlines 0.7–0.95 pt | 22–72 % by family |
| **Plate** | Full-width method and architecture figures of model papers; agent and benchmark overviews | White page; a pale tint only where scope needs one | Same-hue outlines 0.6–0.8 pt | 40–75 % |
| **Showcase** | Teasers of system and benchmark papers; illustrated survey figures | Pastel fields, plates, logos, illustration | Varied | 30–55 % |

How to choose:

- **Venue and width decide first.** A two-column systems, NLP or vision venue means most figures are one
  column (76–85 mm). Design for that width from the start (§5).
- **Look at the paper's other figures and the venue's recent papers.** A figure should look like it belongs.
- **In a redesign, stay in the source's register** unless the brief says otherwise, and beat it there
  (§13). Turning an illustrated showcase figure into line art loses; so does turning line art into a plate.
- **The claim decides the rest.** An idea → schematic. A mechanism with tensors and modules → plate. A
  protocol, layout or data structure → line art. Behaviour on text → example-led. Behaviour on pixels →
  image-led.

Each register's specific devices and families are in [registers.md](registers.md).

## 3. Colour

**Count the hues. The budget is four, each with one meaning.** Strong figures measured zero to five; zero
or one is common: a black figure with one red object, a one-hue ramp, a greyscale diagram with one accent.
Figures with seven or more hues were the weakest in every paper that had one. The one exception is series
identity in a field chart (§11): one hue per system, up to seven, each with a second channel.

- **Colour what is new, wrong or being followed.** Everything inherited, standard or contextual is black,
  grey or white. In a plate, inherited modules are neutral and the contribution takes the hue.
- **A hue is a name; keep it for the whole paper.** The same thing has the same hue in the overview, the
  detail, the chart and the caption. Carry it through every form the thing takes: its chip, its wire, its
  token, its curve, the word that names it (`cv.rich`). Define the paper's palette once
  (`paperkit.series`) and import it in every figure script. A colour pair that changes meaning between
  adjacent figures is a recurring defect even in award papers.
- **An ordered variable is one hue on a lightness ramp** (depth, steps, checkpoints, coarse → specific).
  Unrelated hues for ordered levels hide the order. Model identity is categorical; settings of one model are
  a ramp.
- **Use fill versus outline before spending a hue.** A tinted borderless bubble against a white bordered
  one, a filled disc against an outlined one: a binary carried without a second colour.
- **Text is black or near-black** (`#000000`–`#262B33`). Colour a word only when it names a coloured thing
  or sits on a saturated fill (then white). Grey (`#6B7480`) is for secondary text.
- **Scaffolding is grey.** Arrows, frames and trays that are not the subject take two or three greys
  (`#7F7F7F`, `#BFBFBF`, `#EFEFEF`).
- **Tints mean scope.** A pale field says "these things belong together" or "this condition holds here".
  Tint a region only when the tint explains something; the page is the default ground. Tints sit at
  L\* 88–97; accents are saturated.
- **In image-led figures the content owns the colour.** Keep the vector layer neutral and spend saturated
  hues only on marks that must be found on the pixels, in colours the images lack.
- **Gradients draw continuous quantities** (a density, a ramp, a blend of two sources). The showcase
  register also uses them as surface on plates and bars ([registers.md §8](registers.md#8-showcase));
  nowhere else.
- **Check greyscale** when the venue prints or the series count exceeds three:
  `python scripts/paperkit.py grey fig.png grey.png`. Series must still be told apart (§11).

Role families for the plate register: `paperkit.ROLE` gives each hue five tokens, `fill` (L\* 95–97),
`soft` (88–90), `stroke` (55–65), `ink` (25–35), `mark` (saturated). `ROLE["line"]` is white fill with
black stroke and text, for line art.

## 4. Typography

**One scale per placement.** Sizes are points at print.

| Role | 84 mm column, any register | Full-width plate (dense) | Full-width schematic, chart, image grid |
| --- | --- | --- | --- |
| Panel head, column header | 6.5–8 | 7.5–8.5 | 8–11 |
| Labels, legends, axis titles, example text | 5.8–7.5 | 6.5–7.2 | 7–10 |
| Tick labels, fine annotations | 5.2–6 | 5.8–6.3 | 6–8.5 |

- **Floor.** Nothing below 5.0 pt. Only tick labels and fine annotations go below 5.8 pt; labels, legends
  and anything else a reader must read stay at 5.8 pt or above. Math subscripts ≥ 4.5 pt. Award figures
  with text at 3.2–4.9 pt fail at print in exactly those places; do not copy them. If content does not fit,
  cut content or add height.
- **Size down for density, up for emptiness.** A sparse schematic with 6.5 pt labels looks timid; a dense
  plate with 10 pt labels does not fit. Fill the placement.
- **Two or three sizes per figure.** Build hierarchy with size and position first. Bold is for panel
  letters, ours in a header or legend, a number that is the claim, the changed word in a sentence, and the
  column or stage headers of a grid when they are its only heads. Other panel heads are regular weight.
  All-bold flattens the hierarchy.
- **Face.** Page-level text (panel heads, column headers, axis labels, chart text) takes the manuscript's
  body face: Times/STIX with STIX math for LaTeX papers (`paperkit.use_fonts("serif")`). Text inside a
  drawn diagram may instead be one sans family, used for every diagram in the paper
  (`use_fonts("sans")`). Never two sans families, and never a default face in the charts beside designed
  diagrams: DejaVu Sans in a Times paper is what makes a chart read as unedited matplotlib output.
- **A second voice for text from the world.** Machine-written text, code, file names and template slots
  are monospace. Human prompts and quotes are quoted or set in a distinct face. The figure's own labels stay
  in the main face. A condensed cut can fit a sentence in a narrow tile.
- **Math is typeset**, bold upright matrices, bold-italic vectors, italic scalars, with a constant index
  moved into the panel title. Set an equation on the object it describes, rotated along a curve when it
  labels one (`paperkit.curve_label`).

## 5. Layout

- **Design for the column.** In a two-column venue the figure is 76–85 mm wide unless it earns the full
  width. A column figure is its own design, not a shrunk plate: one example, one vertical axis of reading,
  two or three tiers, about 9–15 objects. Full-width figures are 140–178 mm wide and usually 30–70 mm tall.
- **Fill the width.** Content runs to within 1–2 mm of the column edge. The page supplies the margin;
  never draw an outer frame.
- **Pick a skeleton with named axes**, then place things on it:

  | Skeleton | Use |
  | --- | --- |
  | Grid: example × stage, construct × study, condition × metric, method × scene | Comparison and correspondence; headers carry the meaning, arrows are optional |
  | Hero plus satellites: one object at 60–80 % of the area, inputs in a strip on one side, outputs small on the other | Teasers |
  | Storyboard: 3–6 equal panels, one drawing, one change per panel | Protocols, algorithms, interactions |
  | Overview → zoom → mechanism: narrow locator (≈ 20 %), zoom rays, large detail | Architectures with one new block |
  | Horizontal bands named at the edge, interfaces drawn on the boundaries | Layered systems, planes, address spaces |
  | Schematic row over data row, columns = regimes | Theory with evidence |
  | State pillar between reader and writer | Persistent memory or state |
  | Fan-out, parallel lanes, merge bar, gate | Pipelines with parallel work |
  | Timeline: time on x, rows = actors or stages | Schedules, sessions, procedures |

- **The largest block is the contribution.** Give the operation that carries the claim the most area and
  shrink context to a locator.
- **Use a module.** Choose a unit (2 mm, or the height of one text box) and make every box a multiple of
  it; make parallel things identical in size. Three stage cards of 18.8 × 13.3 mm read as a set; three
  cards of slightly different sizes read as an accident.
- **Align across panels.** Shared left edges, shared baselines for corresponding stages, callouts on one
  vertical line. Symmetry carries a comparison.
- **Say shared things once.** One legend, one y label, x labels on the bottom row, column heads on the
  top row, row conditions as rotated labels at the left (`cv.axes_grid`).
- **Separate zones with space, a hairline or a dashed rule.** Not with a box around each one.

## 6. White space

White space is the cheapest and most neglected tool. Award figures are mostly white (median about 70 %);
what they have in common is where the white is.

- **The page is the ground.** Start with a white canvas and add fills only where a fill explains something.
  A figure whose every panel has a tinted body and a frame has no ground left and reads as heavy.
- **Group the emptiness.** White belongs in gutters, in bands between layers, in a label row, in the strip
  between a legend and its axes, and around the hero. A scattered hole inside a panel is a defect: shrink
  the canvas or move the neighbours, never fill it with decoration.
- **Emptiness can be the finding**: the flat window between two regimes, the gap between two schedule
  rows. Mark it with a double-headed arrow and leave it empty.
- **Proximity is the grouping rule.** A label sits closer to its object than to anything else. Things in a
  group are closer to each other than to the next group. Use two gutter widths, not one.

| Distance | Measured range | Starting value |
| --- | --- | --- |
| Label to its object | 0.3–1.5 mm | 1 mm |
| Padding inside a container | 0.4–1.5 mm (column line art), 1.5–3.5 mm (elsewhere) | 1.5–2 mm |
| Gutter inside a group (images, cards) | 0–1 mm images, 2.5–3.5 mm cards | 1 mm / 3 mm |
| Gutter between groups or panels (image grids: [registers.md §5](registers.md#5-image-led)) | 3–5 mm framed, 8–10 mm unframed | 4 mm / 8 mm |
| Subplots sharing an axis | 3.0–4.7 mm | 4 mm |
| Subplots with their own tick labels | 6–10 mm | 7–8 mm |
| Between lanes or layer bands | 2.5 mm | 2.5 mm |
| Outer margin | 0–4.7 mm, usually under 2 | 1 mm |
| Figure to caption | 3.7–6.3 mm | 4 mm |

White share by register is in §2. Measure with `python scripts/paperkit.py density fig.png` (white ≥ 250,
tint 200–249, ink < 120 in greyscale). It warns below 40 % white, the bottom of the measured range outside
image grids. Ink is typically 2–8 % in diagrams and higher in charts with filled bars; below 2 % with
hairline coloured strokes is the pale failure, fixed by black text and a darker stroke, not by more fill.

## 7. Shapes and objects

**Shape means kind.** Decide the mapping once per paper and keep it.

| Shape | Kind |
| --- | --- |
| Square-cornered rectangle | Memory, data, a buffer, a table cell |
| Rounded rectangle | A component, module, process or graph node |
| Tall rounded bar or slab | A layer |
| Trapezoid | A projection or encoder (narrow side = output) |
| Circle 2.4–3.2 mm | An elementwise operator, a decision node, a numbered callout |
| Disc | A discrete unit: token, feature, point |
| Hexagon (`cv.hexagon`) | An interface, drawn on the boundary it crosses |
| Diamond | A gate or validation test |
| Cylinder | A store or a whole external system |
| Folded-corner sheet | A document or artifact |
| Speech bubble with tail | A human utterance (square box = model output) |
| Pill | A chip, tag, button or slot |
| Stack of three offset cards (≈ 1 mm) | Many of these |
| Dashed frame | A plane, sandbox or scope; anything that is not a concrete object |
| Flat filled region | A regime or condition |

- **Borders: one weight per diagram.** Line art has every stroke at one weight (64 of 64 strokes at
  0.50 pt in CortenMM Fig. 3). Use a second weight for one thing only, and know what it means.
- **Borders or fills, not both by habit.** In line art the border separates objects and fills are for
  state. In fill-on-fill figures (white tile on a grey tray, pill on a card) borders are dropped and
  reserved for modules, ours and zoom boxes. A pale fill with a same-hue outline on every object is the
  plate register's device; elsewhere it is noise.
- **State goes in the border style as well as the fill** (solid / hatched / dashed / dotted) so it
  survives greyscale.
- **Radii scale with size:** chips and labels 0.5–1.2 mm, nodes 1.4–2.0 mm, containers 2.3–2.8 mm, plates
  3.5–4 mm. One radius per size class.
- **Title a container with a tab on its border or a plain head above it.** Header bands were found in
  none of about 90 award figures. `cv.section` and `cv.tab` draw the tab; `cv.group(band=True)` is kept for
  compatibility and should not be the default. The exception is the showcase register, whose illustrated
  stage cards carry solid colour headers ([registers.md §8](registers.md#8-showcase)).
- **No shadows**, except under something that floats above the content: a window, a callout disc.
- **Flat by default.** Depth is for feature tensors and layer runs in vision architectures (`cv.cuboid`)
  and for a layering relation in a showcase figure (`cv.plate`). Systems, ML theory and NLP figures are flat.

**Draw the noun.** A thing the method reads, writes or transforms is drawn as an object, not named in a
box. In example-led figures the sentence is the noun: set it in type and mark it (§10).

| Concept | Glyph (`paperkit`) |
| --- | --- |
| Matrix, state, memory | `matrix(depth=3)`; `fade=` for decay, `band=` for the written row |
| Vector | `vec()` strip of 3–6 cells; grey bar in drawn brackets for a column vector |
| Feature tensor, layer run | `cuboid`, `cuboid(rotate=True)` |
| Feature or attention map | `fmap(n=)` |
| Scored matrix, values in cells | `num_matrix(hi=)` |
| Tokens, sequence | `tokens()`; discs on a chain for an order |
| Multiplicity | `stack(n=3)` |
| Document, store, gate | `doc()`, `cylinder()`, `diamond()` |
| Graph, tree | `graph()`; hand-placed discs and straight edges for a search tree |
| Distribution, score, trace | `mini_plot()` inside the card |
| Real files and commands | `filetree()`, `listing()` in monospace |
| Example text with marked spans | `rich(..., family="monospace")` with a mark per segment |
| Turn or step sequence with a cut | `turn_strip()` |
| Layering with depth | `plate()` + `tile()` |
| Verdict | `icon_check()` / `icon_cross()` on the corner of the judged thing |
| Elided items | An ellipsis or a ghosted frame |

## 8. Icons

Start from no icons (16 of 19 ML figures and 18 of 22 systems figures have none). Add one only when it
passes this test: **it replaces a word that would otherwise repeat, and the reader already knows what it
means.**

- **What earns an icon:** an actor (person, agent), a source or product (its real mark), a verdict (tick,
  cross), a state that repeats on many objects (frozen, trainable, locked), the place an action happened (a
  cursor). Operations, stages and abstract concepts get a word.
- **One family per figure**, line or filled, not both. Line icons take the figure's stroke weight
  (0.5–1.2 pt). The exception is one motif used throughout the paper.
- **Size 1.7–3 × the cap height of the adjacent text** (about 2.5–4 mm beside 6–7 pt text). Above 3 × an
  icon reads as clip art.
- **Every icon has a word beside it** at first use, or is defined in the key or caption.
- **Verdicts sit on the judged thing**: on its corner or the right end of the span, 1.6–3 × cap height.
- **Filled versus outlined is a free binary** (user versus agent).
- **Logos are identity marks**: official, unmodified, in a white tile beside the name
  (`cv.tile(image=...)`), one size per row, never larger than a technical object. Keep a text fallback.
- **Emoji** render from a bitmap font and differ between machines; use `icon_*` vectors.
- **Illustrated icon sets** (generated or drawn) belong to the showcase register only, 3–7 matched icons
  with a label beside each ([image-generation.md](image-generation.md)).

`paperkit`: `icon_snow`, `icon_flame`, `icon_lock`, `icon_cycle`, `icon_robot`, `icon_clock`, `icon_doc`,
`icon_check`, `icon_cross`; `badge` for numbered discs; `callout` for lettered discs with a leader.

## 9. Arrows and connectors

**First ask whether the figure needs arrows.** A grid with headers, a storyboard read left to right and a
stack read bottom to top need none. Counts in strong example-led figures are 0–3.

- **Weight.** In line art, and in any diagram with many arrows, arrows take the box stroke (0.4–1.1 pt).
  In a schematic or example-led figure with fewer than ten arrows, make them heavier than the outlines
  (1.0–2.5 pt) so the flow is the first thing read. One weight per arrow style.
- **Head.** Filled triangle, length 3–6 × the stroke (median 4.5 ×); up to 7 × on strokes under 0.6 pt;
  below 2.5 × the head disappears. One head shape per figure. `cv.arrow` defaults (0.7 pt, 1.4 mm) are
  5.7 ×.
- **Geometry follows the structure.**
  - Orthogonal, square or 1 mm rounded elbows: layered systems, pipelines, memory maps.
  - Straight diagonals: graphs and trees.
  - Arcs: time, self-loops, jumps, a bypass. A curve should mean something; one curved arrow among
    straight ones says "this one is different".
  - Free curves: anything drawn over an image, so it is not read as part of the scene.
- **At most three arrow styles, each defined** beside a sample of the real arrow in a key row or the
  caption. Typical pairs: solid = data, dotted = control; solid = taken, grey dashed = not taken; colour =
  phase. Number arrows with small discs in the arrow's colour when order matters.
- **Dashed means "not a concrete flow"**: control, optional, train-only, not taken, a construction line.
- **Leaders are not arrows.** A callout leader is a 0.6–1.0 pt line ending in a dot. A relation between
  two regions is a line with a dot at each end. A region gets a bracket.
- **Wedges and zoom rays tie a word or a block to its detail**: a translucent wedge from a highlighted
  word to the thing it names, a ray pair from a block to its expansion (`cv.zoom`). One per target.
- **Double-headed arrows measure** an interval or a dimension.
- **Block arrows** (`cv.block_arrow`, grey) mark a stage change or a row's reading direction, nothing else.
- **Rails.** Feedback and retry paths run around the outside of a column, labelled on the line. Outcome
  types can ride as pale bands under one wire style, like metro lines.
- **Reverse or bend an arrow to say something went wrong**: a cost arrow pointing right to left, the only
  curved line as the bypass.
- **Over images:** ghost the image under the arrow, use a hue the image lacks, or switch the stroke from
  black to white where it crosses the dark part. Check contrast on the lightest and darkest pixels it
  crosses.
- **No wire through a label or behind a box**; no unexplained crossing (`cv.wire_crossings()`,
  `arrow(..., halo=True)` for a bridge). If a wire is longer than about 45 mm, move its endpoints together.

## 10. Text inside figures

Two kinds of text, with different rules.

**The figure's own voice** (labels, heads, annotations): one to four words, regular weight, sentence case.
Narrative belongs in the caption. Two exceptions earn their place: a storyboard step title may be a short
sentence ("③ T1 unmaps z, marking it stale"), and a consequence label on a transition arrow may state the
claim ("more efficient sampling"). Units and conditions go in an italic line under the head or in the
caption. Status words ("schematic", "illustrative") go in the caption, except a label on invented data
that could be mistaken for results.

**Text from the world** (examples, prompts, model output, quotes, code, interface text): this is an
object, and it can be long. Set it in the second voice (§4) at 6.7–7.5 pt so it can be read.

- **Mark spans with borderless bands at full line height** (1.2 × the font size) in a pale tint, three
  tints at most, each with one meaning (`cv.rich` with a mark per segment). A verdict glyph goes at the
  span's right end.
- **Or mark by type**: bold for the step in question, an accent colour for changed or erased words, grey
  italic for elided text.
- **Grey out what the reader does not need** (`cv.greek`): bars in place of irrelevant paragraphs make the
  eye go to the lines set in real type.
- **Code:** monospace 7–9 pt in a full-width figure, 6–7 pt in a column, at most three syntax colours, no
  background box, line numbers when the text cites lines (`cv.listing`), and one device that shows the
  claim: a highlight band, a before/after pair, or the data structure drawn beside the code with
  identifiers in matching colours.
- **Every number shown comes from the inputs.** Derived ratios are computed in the script and asserted.

Proof-read every word, stage titles and verdict pills first.

## 11. Charts

**A chart sits bare on the page**: no card, no header band, no frame beyond its own axes. Inside a
composite plate it takes the plate's panel treatment and nothing more.

**Two idioms. Choose by the number of series and the kind of claim.**

| | Claim chart | Field chart |
| --- | --- | --- |
| Use when | One comparison is the message: 2–4 series, one ratio, one crossing | Many systems × many conditions; the reader will look things up |
| Colour | Ours in one accent, the rest in two greys (`#5E6875`, `#8E99A8`) | `paperkit.SERIES_STYLE`: one hue per system, kept across figures |
| Second channel | Not needed | Marker + dash for lines, hatch for bars (`series_kw(k)`) |
| Ours | The accent, the larger marker, bold value | Index 0: the only solid line and the only unhatched bar, first in the legend |
| Line weight | One weight (1.0–1.6 pt); ours differs by colour and marker, not thickness | One weight for all series (0.8–1.2 pt) |
| Labels | Direct labels at line ends; the ratio printed in bold | One frameless legend row above the grid (`cv.chart_legend`) or in the emptiest panel |
| Size | ≈ 85 × 40 mm, or a panel of a plate | Subplots 28–75 mm wide, 9–18 mm tall, 2:1 to 7:1 |

Rules for both:

- **Encode what the claim is about.** A speed-up needs the ratio visible: a bracket or shaded gap with a
  bold `4.0×`. "N× smaller" is area-true as a waffle. Two conditions are a slope chart with growth factors.
  A crossing is the same pair of curves in every panel.
- **Say shared things once** (§5). `cv.axes_grid` builds the grid with one y label, bottom-row x labels,
  column heads and rotated row labels.
- **A legend never sits on data.** Frameless, one row, ours first. Region names, boundaries, reference
  lines and power laws are labelled on the mark itself, rotated to it (`curve_label`); colour an axis title
  to match its curve when two quantities share a panel.
- **Annotate inside the plot.** Totals on stacks, the share inside a bar segment, a shaded regime band, a
  dotted ring with a two-line note on the look-here spot, quantile drop-lines on a CDF, a trend arrow, a
  named tick ("1 (AR)"), an off-scale point as a dotted arrow with its value.
- **Bars start at zero on a linear axis.** For gaps of a few points on a high baseline use a dot plot or
  plot the difference; for values over decades use dots on a log axis. Two ranges are two panels, not a
  broken axis.
- **Spines.** Open (left and bottom) or a full box; use the full box for tight grids
  (`cv.axes_grid(..., box=True)`, or `chart_axes(ax, box=True)` on an axes from `cv.axes`).
  Light grid on the value axis (`#E6E9ED`, 0.5 pt) or none.
- **Two factors take two channels and two small legends**: colour for one, dash for the other, the dash
  legend drawn in black.
- **Uncertainty and statistics are drawn and defined**: band or whiskers named in the caption (95 % CI,
  s.e.m., min–max), significance brackets with stars, the mean printed at the bar.
- **Small n: show every unit.** One strip or stacked bar per participant, same order in every condition;
  desaturate the baseline's version of each hue.
- **Qualitative axes.** A schematic plot drops ticks and numbers, names the axes and the regions, and uses
  symbols as tick labels where a quantity is defined in the text.
- **Rescaling claims** are a raw-axis panel beside a rescaled-axis panel sharing the y axis.
- **Heatmaps**: values in the cells and no colour bar when the grid is small; otherwise a colour bar with
  a scale. Diverging map only around a meaningful zero.
- **Radar** only for an envelope claim on 5–8 axes with at most four polygons: state the axis scaling,
  print the hero's value at each vertex and the rival's where the hero loses (`cv.radar`). Otherwise use
  aligned dot rows.
- **Check greyscale** for a field chart (`paperkit.py grey`).
- Tick labels in the chart's own scale (§4), values with at most three significant digits, `1,401` / `23.7`.

## 12. Captions

The caption is part of the figure's design.

- **Open with the claim**, in bold where the venue's style allows: what the figure shows, as a statement.
- **Then define every encoding the art does not label**: line styles, numerals, colours, bands, error
  bars, direction ("higher is better"), a truncated axis. A caption word may be set in the colour or tint it
  defines, which removes the legend.
- **Length follows the encoding.** Four to eight words for an architecture whose parts are labelled; 25–75
  where styles or reading order need defining; 70–130 for a lettered walkthrough of a system figure
  ("(A) …, (B) …").
- **Say what to look for** in a qualitative figure: the region, the artefact, the row.
- **Leave out** how the figure was made, drawing mechanics, tools, protocol details the methods section
  gives, and disclaimers (`python scripts/paperkit.py caption caption.txt` flags these).

## 13. Redesign protocol

0. **Strengths first.** List three to five things the original does well that a reader would miss: a depth
   metaphor, logos, an illustrated object, a chart whose shape is the claim, calm white space, a clean
   single-column fit. Each is kept or replaced by something visibly stronger. A redesign that is more
   correct but plainer has failed; so has one that is more decorated but harder to read.
1. Render the original region at print width; name its register (§2) and list concrete defects: text
   under 5 pt, hues with two meanings, crossings, scattered holes or crowding, a hidden key idea, slogans.
2. Re-read the method text; the redesign must be at least as faithful to equations, timing and topology.
3. Decide the five-second message and the hero (§1); pick a skeleton (§5).
4. Build with `paperkit`; export PDF, SVG and PNG; compare side by side at one width
   (`paperkit.py compare original.png new.png out.png`) and with `density`.
5. For showcase and illustrated sources run `paperkit.py parity original.png new.png`: it fails a redesign
   that is emptier, greyer or less illustrated. For line-art, schematic and example-led sources, parity's
   "emptier" warning is not a defect; crowding is.
6. Look at both at one width and ask which a reader would choose for a slide. If the original wins the
   first glance, find out why before shipping.

## 14. Checklist

Count first. Each of these has a budget; exceeding one needs a reason.

- [ ] Hues with a meaning: ≤ 4, each defined, each the same in every figure of the paper
- [ ] Stroke weights: 1–2; text sizes: 2–3; arrow styles: ≤ 3, each defined; icon families: ≤ 1
- [ ] Panel treatments: 1 (not a dashed frame here, a banded card there and a bare panel beside them)

Then walk the figure.

- [ ] No visible hero, or a hero made by a thicker stroke or shadow where a difference would do (§1)
- [ ] Two registers mixed, or a register that does not match the venue and the paper's other figures (§2)
- [ ] A full-width plate shrunk into a column; text under 5 pt, or labels and legends under 5.8 pt (§4, §5)
- [ ] A default typeface in a chart beside designed diagrams; two sans families; all-bold labels (§4)
- [ ] Every panel tinted and framed, white below 40 % outside an image grid; a scattered hole; an outer
      frame; a gap filled with decoration (§6)
- [ ] A label nearer to a neighbour than to its own object; one gutter width for everything (§6)
- [ ] A header band on a card outside the showcase register; a chart in a card; a shadow on something
      that does not float (§7, §11)
- [ ] The same kind of thing in two shapes, or two kinds in one shape; a gate or operator drawn as a
      layer-sized box; state or memory written as a word when it could be drawn (§7)
- [ ] An icon that replaces nothing, larger than 3 × cap height, from a second family, or with no word (§8)
- [ ] An undefined arrow style; a wire through a label or behind a box; an unexplained crossing; a low-
      contrast arrow over an image; arrows where reading order would do (§9)
- [ ] A sentence in the figure's own voice; example text too small to read; a typo (§10)
- [ ] A legend on data; shared labels repeated in every panel; a claim about a ratio with no ratio shown;
      a field chart that fails in greyscale; bars on a log axis or from a non-zero floor; an unlabelled
      band or error bar; a radar with more than four polygons or unstated scaling (§11)
- [ ] One model or condition in two colours across panels or figures; an ordered variable in unrelated hues (§3)
- [ ] A caption that narrates production or leaves an encoding undefined (§12)
- [ ] A redesign plainer than its source in the source's own register, or more decorated and harder to
      read (§13)
- [ ] A rule from [registers.md](registers.md) for this figure's family
