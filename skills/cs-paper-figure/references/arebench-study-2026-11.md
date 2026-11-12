# ARE-bench Figs. 1–3: contrast, state and construction figures (study, Nov 2026)

Source: *ARE-bench: Benchmarking Agents' Research Ability in Real-World Researcher Sessions and
Workspaces* (arXiv 2611.14364). Fig. 1 is a results chart (bars + radar), Fig. 2 a "them vs us"
contrast figure, Fig. 3 a three-role construction pipeline. Together they show how a benchmark paper
explains *what is different about its tasks* rather than *how a model computes*. Rules distilled
below go into [registers.md §7](registers.md#7-contrast-state-and-construction).

## 1. Fig. 2: the contrast figure (strongest of the three)

- **Two columns × two shared rows.** Left column "Existing Benchmarks", right column "ARE-bench".
  Rows are the two dimensions of the claim (Session Context, Workspace State), named once by a
  rotated label in an I-bar bracket at the far left and separated by a dashed rule that spans both
  columns. Every cell answers "what does each side do on this dimension?", so the reader compares
  across one row at a time. The two contribution words from the intro are the two row names.
- **The narrow side is the baseline.** The existing-benchmark column is about one third of the width;
  ours gets two thirds and the detail. Width is spent where the novelty is.
- **Same vocabulary on both sides.** The seven stage icons appear as a straight left-to-right
  pipeline on the left and as seven boxed stages with return arcs on the right. The reader sees the
  difference (order, loops) because the objects are identical.
- **Non-linear order by arcs, not by reordering.** Stages stay in canonical order; the real session's
  jumps are drawn as arcs above (back-jumps) and below (skips) the row, each carrying a numbered badge
  that keys to a request list underneath (`① T7 Check similar papers`). Arc colour = arc kind.
- **Show the cut.** A strip of 42 turn cells, filled to T30, the cut turn T31 in orange, the rest
  grey, labelled "T1 to T30 become the Background, T31 the task". The task boundary is a picture,
  not a sentence.
- **Highlight the task twice, consistently.** The delegated stages get a dashed orange region with an
  italic orange label ("the delegated step"); the T31 request bar is hatched in the same orange star
  colour and ends with "Analyze → Write". One accent colour = "the task".
- **Literal artifacts in monospace.** Requests, the terminal (`$ pytest`, `5/5 passed`) and the file
  tree are set in a mono face inside window chrome (three dots, title bar). Mono means "real data
  from the workspace"; serif means "our explanation".
- **Status tags on data rows.** Each file carries a coloured tick at its left and a right-aligned
  italic tag in the same colour: superseded (amber), current (green), stale (red, with ⊗), paused
  (purple), duplicate. This is the figure's evidence that the workspace is messy.
- **Verdict pill per column.** Each column ends on a pill: red ✗ "Missing the real handoff" vs green
  ✓ "…the real context". The takeaway is the last thing read in each column.
- **"What the agent receives" card list.** Three role-coloured pills (Background, Requirements,
  Environment) each with a terse right-hand gloss, then a scoring card with a lock for hidden
  material. Visible vs hidden is marked with a lock, not a paragraph.

Flaws to avoid: a typo in the verdict pill ("Perseiving"); hand-drawn double-stroke borders read as
playful and blur at small size; the orange dashed region and orange arcs share a hue with the Design
stage box, so "task" and "Design" collide.

## 2. Fig. 3: three-role construction pipeline

- **One tinted column per role** (Curator green, Builder cream/lilac, Validator lilac), each headed by
  an icon + letter + role name. The roles are the paper's §3.2.1–3.2.3 headings, in order.
- **Numbered step cards with a type tag.** "1 Normalize ··· *Events*", "4 Label ··· *Taxonomy*",
  "5 Select ··· *Policy*": the bold step name left, the kind of output right in italic role ink.
  Steps are joined by short down-arrows, so the column reads as a checklist.
- **Rules printed in the card.** S1–S4 selection rules appear verbatim inside "5 Select", so the text
  can cite them by code.
- **Two sub-pipelines in the middle role.** Builder splits into "1 Task construction" and "2 Rubric
  construction", each Inputs → verb (Compile / Replay to T31 / Extract & verify) → product. Verbs sit
  between the boxes as coloured labels under a round operator glyph, not inside boxes.
- **Visibility split.** "Task · actor-visible" is a framed product; "Hidden evaluation" carries a lock.
  The same visible/hidden distinction as Fig. 2, drawn the same way.
- **Feedback as an outer rail.** "Revise" from Human review back to the Builder runs as one rose line
  around the Validator column, labelled on the line; a dashed "Full interaction" side channel runs
  vertically with rotated text. Loops stay outside the main flow so they never cross it.
- **Running example across figures.** "TIC paper restructuring", "42 turns · cut T31",
  `new_paper_plan_v5.md` are the same instance as Fig. 2. The reader recognises the task.

Flaws: the Curator column is cramped (text at ~5 pt), many arrows are 2–3 mm stubs, and three
column tints plus box strokes plus icon colours make about nine hues.

## 3. Fig. 1: overall bars + per-stage radar

- **One legend spans both panels** above them, in rank order; marker shape + colour per model, so the
  radar is readable in greyscale.
- **Value labels on every bar**, error bars (sample s.d. across rounds) and the ± meaning stated in
  the caption; bars sorted by score.
- **Radial range stated.** The radar's axis runs 35–95 %, and the caption says so: a truncated radial
  axis must be declared.
- **Model identity under the bars** via logos, plus two-line names.

Flaws: the bars use a sequential teal→sand ramp while the radar uses categorical model colours, so
the same model has two colours in one figure; seven overlapping radar polygons are hard to compare
(small multiples or a stage × model dot plot would read better); logos depend on venue rules.

## 4. Transfer rules

1. A contrast figure gets shared rows named after the claim's dimensions, a narrow baseline column,
   the same object vocabulary on both sides, and a verdict pill at the foot of each column.
2. Draw a task boundary or cut point as a picture (`cv.turn_strip`), not as a caption sentence.
3. Real artifacts (files, commands, requests) go in mono inside window chrome (`cv.filetree`);
   their state goes in a coloured tick + right-aligned italic tag.
4. Keep canonical order and draw deviations as numbered arcs above/below, keyed to a list.
5. One accent colour means "the task / ours" everywhere in the figure, and it must not be reused by
   a stage or category.
6. Mark hidden-from-the-agent material with a lock icon, the same way in every figure.
7. Step cards: bold step name left, italic output type right; selection rules printed in the card.
8. Loops and side channels run as outer rails, labelled on the line.
9. One model = one colour across every panel of a results figure; declare truncated radial or value
   axes in the caption; prefer small multiples to a radar with more than four polygons.
10. Reuse one running example (same IDs, file names, turn numbers) across the overview, the
    construction figure and the case study.
