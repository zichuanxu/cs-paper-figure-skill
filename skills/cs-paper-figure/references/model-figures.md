# Model figures: look before you draw

Rules describe a good figure; they do not show one. Before drawing, open the model for your figure's family
with your image reader (the PNG, not this text), and open it again beside your own render in review. The
previews are in [`assets/models/`](../assets/models/); each is the output of the script named beside it.

A model is a standard to reach, not a layout to copy. Take its level of finish and the devices listed; the
content, the skeleton and the palette come from your paper.

## What every model has that a compliant-but-plain figure lacks

Each of these is a floor. A figure can pass every budget in the rulebook and still miss all seven.

1. **One composition.** There is a frame, a spine or a grid that carries the eye from the input to the
   outcome. Panels are zooms of a point on that spine, tied to it by rays, a rail, a shared hue or position.
   No panel could be cut out and published alone without losing its meaning.
2. **Every concept in the message is a drawn object** (a rack of components, an execution record, a chat
   thread, a matrix, a memory card), drawn the same way each time it appears. Words label objects; they do
   not replace them.
3. **One concrete instance runs through it**: real tokens, a real request, a real file name, real values.
4. **The claim is drawn as a relation**, not written in a cell: a rail joining the two facts that conflict,
   an edit shown on the object it changed, the merged state striped in the second hue, two final answers on
   one line with their verdicts.
5. **The placement is used.** Full-width models are 14–44 % blank; column schematics 38–69 %
   (`paperkit.py fill`). Objects are large enough that the figure reads at arm's length.
6. **Colour and fill are present and mean something**: two to four hues, pale fields for scope, one or two
   saturated objects for the hero. Not black hairlines on white with one accent, unless the register is line
   art.
7. **Every encoding is defined**: in one key strip beside samples of the real marks, or by labels on the
   marks themselves when there are few (a relation named on its thread, a name tab on a card). Not both.

## Two ways a figure passes the checks and still fails

**The typeset table.** A motivating or qualitative example drawn as rows of sentences with a status column
and score bars. Everything is aligned and legible, and nothing is drawn: no speaker, no store, no link
between the message and the memory it affects. Test: *could LaTeX set this as a `tabular` without losing
anything?* If yes, either typeset the table, or draw what a table cannot: the objects (message bubble,
memory cards, each system's pick) and the relation the claim is about (the surface match that misleads one
system, the implication the other one follows), with the verdict on the object. The numbers in such a
figure could always go in a table; the test is passed when the links and positions carry the reason for
them, which a table would lose.

**The islands.** A method overview drawn as lettered panels (a) (b) (c), each a small self-contained
diagram with its own subtitle, sharing no object and joined by no line. Each panel is fine; together they
are three thumbnails on a wide page. Test: *cover the panel letters; does the eye know where to start and
where it ends?* If not, find the spine (the path of one item through the system), lay the whole figure on
it, and turn the side topics into zooms of the object they describe: the decision rule opens from the
object that makes the decision, the baseline is a ghosted lane beside ours, the chart sits where its
quantity lives.

Both come from the same habit: following the budgets (few hues, few sizes, white ground, no icons) without
first deciding what the picture is.

## The models

| Family | Preview | Script (`scripts/examples/`) | What to take from it |
| --- | --- | --- | --- |
| Method overview of an agent or system with nested loops | `plate_agent_system.png` | `harness2/render_fig3.py` | Inner frame inside outer frame, titles on tabs; one object (the rack C1–C8) drawn at every stage so the merge is visible on it; two candidate lanes in two hues that meet at a composer; phase bar under the frame; key strip |
| Method overview following one call through components | `plate_agent_components.png` | `harness2/render_fig2.py` | One left-to-right spine; every component a file card with its state as a tag on the border; the context drawn as a stack whose bands take their owner's hue |
| Ours versus a baseline on one shared stream | `plate_agent_loop.png` | `reharness/render_fig1.py` | The shared instances drawn once in the middle, baseline above and ours below on one column grid; the new operation in its own tinted row and hue; numbered edge labels on the wires; each side ending on a verdict pill; the edit shown as struck text and a highlighted condition |
| Model architecture with mechanism detail | `plate_architecture.png` | `memt/render_fig4.py` | Narrow locator, zoom rays, three detail panels each with a data object (matrices, trapezoids, a curve), section frames in the module's hue, key strip |
| Classic architecture, calm plate | `plate_architecture_classic.png` | `transformer/render_fig1.py` | Three text sizes and two stroke weights for a whole plate; only the contribution saturated; bare panels under plain heads |
| Benchmark or dataset overview | `benchmark_overview.png` | `groupassist/render_fig1.py` | Statistics as three large numbers with icons; the real example as a chat thread with avatars and marked spans; each task level a coloured band that begins as a taxonomy row and continues as a worked instance; a red rail joining the two facts that conflict |
| Construction pipeline | `benchmark_pipeline.png` | `groupassist/render_fig2.py` | Numbered heads on the page over pale trays; one amber object followed through every step; counts and a kept-share bar per step |
| Idea in one column | `idea_schematic_column.png`, `idea_schematic_two_states.png` | `memt/render_idea_column.py`, `lora/render_fig1.py` | One drawing shown in two states; large objects and 7–8 pt type; three arrow hues defined in a key row; the changed state as the only saturated region |
| Motivating example: one input, a few items, what two systems do | `example_led_scene.png` | `scene/render_retrieval_scene.py` | The input said once in a bubble by a user glyph; items as white cards on one tray, drawn once; a thread from the marked span in the input to the span on the card each system ranks first, grey for the baseline and the one hue for ours, the relation named on the thread; the system's name and verdict as a tab on the card it picks; each item's own status as a tag on its bottom border |
| Methods compared on one text example | `example_led_methods.png` | `react/render_fig1.py` | The question once across the top; a column per method with ours widest; three voices (monospace, grey body, gutter labels); rails beside reasoning; verdict glyph after each final answer, answers on one line |
| Protocol in one column | `line_art_sequence.png` | `ray/render_fig7.py` | Lanes with lifelines, one message per row, numerals in one aligned column, state drawn in the row that creates it, one hue for the plane the claim is about |
| Teaser of a system paper | `showcase_teaser.png` | `toolspace/render_fig1.py` | Isometric plates for a layering claim, logo tiles, honest radars, zoom into the largest panel |
| Illustrated survey figure | `showcase_illustrated.png` | `proactive/render_overview.py` | Two rows over shared columns, solid colour headers, a vignette and an object made from each stage's definition, a feedback rail |
| Claim chart | `chart_claim.png` | `memt/render_fig3.py` | Ours in one accent, rivals in two greys, the ratio printed in bold on a bracket |
| Field chart in one column | `chart_field_column.png` | `toolspace/render_table1_column.py` | One hue plus marker per system, one legend row, shared labels said once |
| Four-panel results figure | `chart_four_panel.png` | `restyled/render_experiment.py` | One series palette across panels, direct labels, panel heads in the body face |

The full-width models are 178 mm plates. A 140 mm figure (NeurIPS, ICLR) holds about 60 % of their
objects at the same type size, and `compare` scales both to one pixel width, so judge finish, composition
and use of area, not how many things are drawn.

No model for your family: take the nearest one for finish, and find a published figure of your kind with
`python scripts/reference_catalog.py search --query "..."`.

## How to use a model

- **Before drawing** (workflow step 2): open the preview. Write down three devices you will take and the
  one thing your figure has that the model does not.
- **In review** (workflow step 6): `python scripts/paperkit.py compare assets/models/<model>.png
  figures/yours.png out.png`, open `out.png`, and answer in one line each: which looks more finished, which
  uses its area better, which would an area chair remember. If the model wins all three, the figure is not
  done.
