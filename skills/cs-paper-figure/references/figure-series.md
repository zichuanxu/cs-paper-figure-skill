# Figure series, survey figures and illustrated scenarios

Surveys, position papers and system reports often carry 10+ figures that explain one framework. They are
read as a set, so the set needs a system. This file records the studies (2026-10) and the devices the
skill now provides for them.

## 1. Studies

**"Proactive AI for Superintelligent Agents"** (Yang et al., UIUC / Google / Stanford / Berkeley / CMU,
203 pp., 15 figures). A six-capacity framework ("6A": Awareness, Anticipation, Agenda, Arbitration,
Action, Adaptation) threads through nine figures.

| Device | Where | Verdict |
|---|---|---|
| **Chapter template**: one large tinted panel per capacity, title in its dark shade, an input tab on the left in the previous capacity's colour and a rotated "To <next>" tab on the right | Figs. 7–12 | strong: consecutive figures read as one chain across 20 pages |
| **Running example** (household agent: "groceries low" → "groceries will run out" → "order groceries" → checks → "prepare dinner now") carried through every capacity | Fig. 6 | strong: the abstract loop becomes concrete nouns |
| **Gate stack**: numbered tests, each with a PASS exit to a licence column and its own FAIL fallback chip | Fig. 10 | strong idea; pass lines cross the fail column |
| **Spectrum**: graded axis (light → dark), three scenes, role chips whose fill darkens along the axis | Fig. 4 | strong: lightness carries "more of the same thing" |
| **Low/High grid**: capability rows × low/high columns, a character pose plus a first-person speech bubble per cell ("Wait – what should I do?" vs "I've got this") | Fig. 3 | memorable; bubbles carry behaviour |
| **Zig-zag timeline**: alternating decade cards on a spine ending in a hero card with the 6A chips | Fig. 5 | clear history at a glance |
| **Annotated scene**: one illustrated scene with three numbered evaluation panels whose tails point at the parts they assess | Fig. 13 | good for "levels of evaluation" |
| Generated illustrations with one recurring robot and human cast | Figs. 1, 3, 4, 13–15 | consistent cast, but see below |

Weaknesses worth beating:
- **The 6A colours change from figure to figure.** Agenda is pink (Fig. 1), purple (Figs. 5, 6) and blue
  (Fig. 9); Arbitration is purple, blue, orange and gold. The reader relearns the legend every time.
- Generated screens and documents contain fake small text ("Task: Fix the printer…"), which reads as
  data and cannot be edited or checked.
- Chapter figures 7–12 are bullet lists in boxes (slideware); the mini-diagrams (counterfactual branches,
  sampled futures in Fig. 8) are the parts that teach.
- Mixed icon registers (line icons, emoji-like glyphs, generated figures) in one panel.

**PlugMem** (arXiv 2603.03296, UIUC / Tsinghua / Microsoft Research). Useful devices: black inverse
label tabs numbered per stage and overlapping the dashed container border; a dashed rounded envelope for
"the system" with out-of-scope components ghosted to grey; stacked offset cards for "many items"; one
colour per memory type carried through Figs. 2–4; node-state rings (new = yellow halo, visited = black
ring, inactive = hatch) with a mini legend; a "↑ higher utility / ← lower cost" direction box inside
scatter axes; hollow markers for ablations, filled for other methods.

**StudentSim** (arXiv 2609.01591, Microsoft Research / UIUC). One role colour per meaning across all
figures (blue `#0B62B3` real loop, purple `#8968C7` simulator, yellow `#F1BC1B` tutor, teal `#40B9C6`
reward); an **identity colour that follows one entity** (student A/B/C) through clothing, data box,
name pill and output badge, so fan-in/fan-out needs no labels; dark `#4D4D4D` title pills with white bold
text; tag pills straddling a box border ("RL Update", "Fixed Parameters"); line style as relation (dotted
= matching, dashed = transition; dashed = prediction, solid = ground truth); verdict badges (dark rounded
square with a ✓/✗ in the actor's colour); a direct-labelled scatter with the winner as a star and a light
italic "(x, y)" line under each name; a mini booktabs table inside a figure with coloured monospace values.
Weak spots: five font families in one figure, generated cartoon characters next to thin line icons, and
pure `#FF0000` next to muted reds.

**PaperBanana** (arXiv 2601.23265, Peking University / Google Cloud AI Research). Almost every figure is a
generated raster. Phase zones (plan `#CCDCEC`, refine `#F8DCC4`) with role props on each agent; a three-class
arrow grammar (solid main flow, dashed auxiliary, an edge-hugging dashed side channel); a bypass elbow over a
node row instead of a crossing; "T = 3 rounds" inside the loop; a reference *line* for the human level
instead of a third bar series; before/after pairs with a numbered change list; error-pairing frames where red
text in the explanation column matches red boxes on the figure. Weak: raster text at mixed sizes, a
truncated bar axis (starts at 30), the round counter colliding with the return arrow.

**ReHarness** (arXiv 2610.12668, MIT / Meta / Yale). A mechanism colour pair (forward blue `#10739E` /
`#B1DDF0`, revision red `#AE4132` / `#FAD9D5`) reused in every diagram; the **same toy example in both
panels**, so only the added layer differs; agent identity as a tab docked on each card; a typed-edge legend
("(3) τ_t → h'_t: **Backward Revision** by π_R …"); primed states aligned directly under the originals; a
reward tab on each trajectory card; a sparkline sharing the x-axis with a heatmap and one dotted event line
through both; a direct label on a reference line. Weak: 5.7–7 pt text in a second font, floating edge
numbers, crossing curves, legends detached from their panels.

## 2. Rules for a figure series

1. **Define the taxonomy palette once** (`paperkit.series(names)`) in a shared module that every figure
   imports; never pick a capacity's colour inside one figure. Check the set side by side before submission.
2. **Chain chapters**: `cv.chapter(..., prev=(name, role), nxt=(name, role))` draws the panel plus the
   input and "To next" tabs in the neighbours' colours.
3. **One running example** through the whole framework figure; draw its items as chips in each stage's
   colour instead of illustrations of the stage.
4. **Decision cascades as gate stacks**: each test owns its failure exit inside its row; pass exits run
   straight to one AND bar, so no line crosses another.
5. **Degrees as lightness** (`cv.spectrum`): one hue ramp for the axis and for every chip that sits on it.
6. **Illustrated scenes** (via `codex_icons.py`, style `"scene"`): one cast described once and passed as a
   reference; no text inside the pixels (blank screens, ticks and bars only); all dialogue as vector
   `cv.bubble()` with the tail on the speaker; scenes framed in light cards of equal size.
7. **Ghost what is out of scope** (grey fill, grey text) rather than inventing another colour.
8. **Diff panels**: when a method adds a layer to a baseline, draw both panels on one column grid with the
   same example; the new layer gets its own row and colour, the outcome that changes gets the border
   (`reharness/render_fig1.py`).
9. **Typed-edge legends**: number badges sit *on* the edges; the legend line names the edge type in its
   colour, then its endpoints, then what it does. Put the legend beside its panel, never in a detached box.
10. **Bridge unavoidable crossings** with `cv.arrow(..., halo=True)` drawn above the other wire.
11. **Charts against a reference**: if the paper compares to a human or oracle level, make that level the
    axis centre and shade the losing side; never truncate a bar axis to exaggerate gaps (dumbbell,
    `paperbanana/render_fig5.py`).
12. **Check the series** with `python scripts/paperkit.py swatches fig*.png out.png`: every figure with its
    dominant saturated colours underneath; a stage whose swatch changes is palette drift.
13. **Stage labels as inverse tabs** (`cv.tab(..., solid=True)`) that overlap the container border, so the
   label belongs to the container.

## 3. Worked examples

`scripts/examples/proactive/`: `sixa.py` (the shared palette), `render_overview.py` (Fig. 1: what the user
experiences beside how the agent works), `render_capabilities.py` (Fig. 3: low/high grid with one generated
robot cast and vector dialogue), `render_history.py` (Fig. 5: proportional timeline, era spans on mirrored
lanes, legacy chips in the capacity colours), `render_arbitration.py`, `render_cycle.py`, `render_spectrum.py`.
`scripts/examples/reharness/render_fig1.py` (diff panels, typed-edge legend, bridged crossing) and
`scripts/examples/paperbanana/render_fig5.py` (dumbbell centred on human parity). The original figures are not redistributed; compare against the
paper's Figs. 4, 6 and 10.
