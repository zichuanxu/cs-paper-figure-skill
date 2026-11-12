# cs-paper-figure

An agent skill for designing, drawing and critiquing figures for computer-science papers: architecture and method diagrams, agent pipelines, efficiency and benchmark charts. It is distilled from a close study of figures in leading AI research papers and ships a small drawing library so the agent produces editable, reproducible vector figures instead of generic flowcharts.

![The Transformer (Attention Is All You Need, Figure 1), redesigned with this skill](gallery/transformer/transformer_fig1.png)

<sub>The Transformer (*Attention Is All You Need*, Figure 1), redesigned with this skill.</sub>

## What is inside

| Part | Purpose |
| --- | --- |
| [`SKILL.md`](skills/cs-paper-figure/SKILL.md) | The workflow: brief → references → structure → visual system → reproducible source → review |
| [`visual-craft.md`](skills/cs-paper-figure/references/visual-craft.md) | How it should look: typography, role colours, glyph vocabulary, composition, connectors, density, charts, anti-patterns |
| [`architecture-study-2026-11.md`](skills/cs-paper-figure/references/architecture-study-2026-11.md) | What 23 vision/multimodal method figures (Holmes, ReSet, CoPS, SemDiff, LFBNet, HFF-Net, VideoFusion, …) do well and badly, and the rules taken from them |
| [`arebench-study-2026-11.md`](skills/cs-paper-figure/references/arebench-study-2026-11.md) | What ARE-bench Figs. 1–3 do well and badly: contrast figures, task cut strips, workspace file trees, construction pipelines, results-chart colour identity |
| [`toolspace-study-2026-11.md`](skills/cs-paper-figure/references/toolspace-study-2026-11.md) | What ToolSpace Fig. 1 does well (isometric plates, logos as identity marks, radar envelopes) and how a tidier redesign lost it: the "strengths first" rule for redesigns |
| [`paperkit.py`](skills/cs-paper-figure/scripts/paperkit.py) | Drawing primitives in millimetres at print size (cards, section frames, cuboids and layer slabs, feature maps, numeric matrices, mini plots, graphs, key strips, matrices, trapezoids, ⊕/⊙, tokens, documents, icons, routed arrows, typeset math) plus `density`, `compare`, `parity` and `caption` checks (a redesign must not come out emptier, greyer or less illustrated than its original) |
| [`figure-series.md`](skills/cs-paper-figure/references/figure-series.md) | Figure series for surveys and frameworks: one taxonomy palette, chapter frames, running examples, gate stacks, spectra, illustrated scenes with vector dialogue |
| [`codex_images.py`](skills/cs-paper-figure/scripts/codex_images.py) + [`image-generation.md`](skills/cs-paper-figure/references/image-generation.md) | Optional matched icons, scenes and vignettes generated with Codex CLI, embedded at full resolution |
| `scripts/examples/`, `references/` | The gallery's render scripts; a 120-paper figure corpus, per-lab studies and review checklists |

## Gallery

Each redesign keeps the paper's components, values and notation; only the drawing changes.

### The Transformer, Figure 1 ([arXiv:1706.03762](https://arxiv.org/abs/1706.03762))

| Original | Redesign |
| --- | --- |
| <img src="gallery/transformer/original/transformer_original_fig1.png" width="300"> | <img src="gallery/transformer/transformer_fig1.png" width="520"> |

- The three multi-head attention blocks are the only saturated blocks and carry numbers 1–3. Each has the same K, V, Q ports; only the colour of what enters changes: all blue for encoder self-attention, all coral for masked decoder self-attention, and a blue-to-coral blend fed by the encoder output **z**, "to every decoder layer".
- "Add & Norm" is opened into a residual wire, ⊕ and a LayerNorm bar. The two embeddings and the pre-softmax linear layer are three amber trapezoids (one shared weight matrix). "Shifted right" is the one-column offset between the decoder input row and the predicted row of an English→German example.
- Panel (b) zooms from the stack of h = 8 heads into one head with numbers (scores → mask → softmax → weights whose rows sum to 1). Panel (c) shows the three uses as query-by-key matrices over the example tokens, with hatched −∞ cells for the causal mask.

[PDF](gallery/transformer/transformer_fig1.pdf) · [source](skills/cs-paper-figure/scripts/examples/transformer/render_fig1.py)

### Harness², Figures 2 and 3 ([arXiv:2610.14224](https://arxiv.org/abs/2610.14224))

| Original | Redesign |
| --- | --- |
| <img src="gallery/harness2/original/harness2_original_fig2.png" width="420"> | <img src="gallery/harness2/harness2_fig2_components.png" width="420"> |
| <img src="gallery/harness2/original/harness2_original_fig3.png" width="420"> | <img src="gallery/harness2/harness2_fig3_pipeline.png" width="420"> |

- Fig. 2 follows one model call from left to right: files, context, frozen model, plugin hook, tools. Each of the eight components is a file card with its activation as a tag on the border (solid = every call, dashed = on demand), and the context is a stack whose bands take the colour of the group that owns them.
- Fig. 3 nests the task-level frame inside the harnessing-level frame. Every harness is a rack of C1–C8 in which grey cells are inherited, teal cells were edited by the invariant candidate and coral cells by the domain candidate, so the composed successor shows the merge on the object. Both probes are contrasted with the same reference record e₀.
- The two figures share one visual system (the rack, the execution-record page, one robot and file-icon family, no hue with two meanings). The icons come from the skill's Codex helper; `--vector-icons` renders without them.

[Fig. 2 PDF](gallery/harness2/harness2_fig2_components.pdf) · [Fig. 3 PDF](gallery/harness2/harness2_fig3_pipeline.pdf) · [source](skills/cs-paper-figure/scripts/examples/harness2/)

### A figure series: *Proactive AI for Superintelligent Agents*

Six figures of a 15-figure survey ([PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/1048480.pdf)) rebuilt as one series; Fig. 1 is shown here, the other five are in the PDFs and source linked below. The originals are illustrated figures, and their pictures, solid headers and large type are what make them work, so the redesigns keep all of that and fix the faults: each capacity's colour now stays the same in every figure (the paper paints Agenda pink, purple and blue), text baked into the illustrations becomes editable vector text, and overlapping eras, crossings and uneven type are cleaned up. The 41 illustrations come from the skill's Codex helper as one cast; every redesign passes `paperkit.py parity` (not emptier, greyer or less illustrated than its original).

| | Original | Redesign |
| --- | --- | --- |
| **Fig. 1**, proactive vs. reactive | <img src="gallery/proactive/original/proactive_original_fig1.png" width="400"> | <img src="gallery/proactive/proactive_overview.png" width="400"> |

- Two rows over three shared columns (identify the work and initiate action, act, outcome). In the reactive row the first columns are the user's turn; in the proactive row the same columns hold Awareness, Anticipation, Agenda and Arbitration, and "Act when asked" sits directly above "Action: before being asked".
- Each stage card ends in an object made from its own definition: a progress bar with the gap left open, the candidate goals as a checklist, three ticked tests (worthwhile, timely, safe), and suggest / assist / execute on a lightness ramp.
- Adaptation is a rail under the stages: outcomes and feedback enter it, dashed arrows return to every capacity, and no feedback line crosses a card.

[PDFs](gallery/proactive/) · [source](skills/cs-paper-figure/scripts/examples/proactive/) · [what the studies found](skills/cs-paper-figure/references/figure-series.md)

### ReHarness, Figure 1 ([arXiv:2610.12668](https://arxiv.org/abs/2610.12668))

| Original | Redesign |
| --- | --- |
| <img src="gallery/reharness/original/reharness_original_fig1.png" width="420"> | <img src="gallery/reharness/reharness_fig1.png" width="420"> |

- One instance stream, two harnesses: the three trajectories are drawn once in the middle, with the stateful harness above and ReHarness below on the same column grid. The τ<sub>t+1</sub> card carries both answers, {7,4,3} wrong for (a) and {3,4,7} correct for (b).
- Backward revision is its own orange row under the unchanged blue forward row. The h′<sub>t</sub> card shows the edit itself: "Put larger numbers first" struck out, "Larger first only if descending" with the new condition highlighted.
- Every numbered edge carries its label on the wire ("write R<sub>t</sub>", "read R′<sub>t−1</sub>", "revise R<sub>t−1</sub>"), coloured by type; numbers are tokens shaded by magnitude, and each panel ends on a verdict pill.

[PDF](gallery/reharness/reharness_fig1.pdf) · [source](skills/cs-paper-figure/scripts/examples/reharness/render_fig1.py)

### ToolSpace, Figure 1 ([arXiv:2611.05036](https://arxiv.org/abs/2611.05036))

| Original | Redesign |
| --- | --- |
| <img src="gallery/toolspace/original/toolspace_original_fig1.png" width="420"> | <img src="gallery/toolspace/toolspace_fig1_overview.png" width="420"> |

- What the original does well is kept: the tool space is a plate floating between the agent and a plate of MCP servers, with tools standing on it as tiles and the ten servers shown by their own logos; the two radar charts stay radars, because the claim is that one polygon encloses the others.
- What it does badly is repaired. ToolSpace is blue in every panel. Each radar prints the ToolSpace value at every vertex and, on the one axis it loses (τ³-Bench Banking, 43.3 against 46.9), the winner's value beside it; the card states that each axis runs from 0 to its best score. All baseline values are from the paper's Table 1.
- The upper plate opens by zoom rays into the largest panel, where one hue per environment is shared by a walk node, its cluster and its row in the tool chain: "8 calls across 4 environments". Panel (d) shows the drop the text claims, a pale bar to the Standard score and a blue bar to the Pro score for all seven models of Table 2, each row led by the model's mark; the original draws six models and no Standard scores.
- A first redesign of this figure replaced the plates, logos and radars with a flat box, text labels and dot rows, and came out tidier and plainer. The lessons are in [`toolspace-study-2026-11.md`](skills/cs-paper-figure/references/toolspace-study-2026-11.md), and `paperkit` gained `plate`, `tile` and `radar`.

[PDF](gallery/toolspace/toolspace_fig1_overview.pdf) · [source](skills/cs-paper-figure/scripts/examples/toolspace/render_fig1.py)

### GroupAssistBench, Figures 1 and 2 ([arXiv:2611.04867](https://arxiv.org/abs/2611.04867))

| Original | Redesign |
| --- | --- |
| <img src="gallery/groupassist/original/groupassist_original_fig1.png" width="420"> | <img src="gallery/groupassist/groupassist_fig1_overview.png" width="420"> |
| <img src="gallery/groupassist/original/groupassist_original_fig2.png" width="420"> | <img src="gallery/groupassist/groupassist_fig2_pipeline.png" width="420"> |

- Overview: the two task levels are two bands. Each begins as its row of the 2 × 3 taxonomy, one square per cell with area equal to the number of instances, and continues as the worked instance of that level, so "A is an L1 × M2 instance" is a position. The trip-planning thread is drawn once as a chat window; under it each instance shows the same thread as a strip of ten-message cells with its own cut (#104, #452).
- A red rail joins A's reference fact "7:30 am on May 1" (#34) to B's −2 penalty row: the answer to the recall question is the superseded value in the use request.
- Pipeline: five numbered step columns, each with its output counts from Appendix A under the header, so the row is also the funnel from 13,782 candidates to 2,395 instances. Every sub-step carries one glyph for who does it (rules, language model, humans) and an object from the same thread; feedback is a side rail whose "superseded value −2" chip points into B's penalty row.
- One style module for both figures: amber anchor, red superseded, green current, blue L1, purple L2. Labels that disagreed with the paper's text are corrected (D1–D3 to M1–M3, "serve" to "memory use", "Quires", "two annotators · κ" to the three annotators and raw agreement the text reports).

[PDFs](gallery/groupassist/) · [source](skills/cs-paper-figure/scripts/examples/groupassist/)

### MemT-1.0, Figures 3 and 4 ([arXiv:2610.26825](https://arxiv.org/abs/2610.26825))

| Original | Redesign |
| --- | --- |
| <img src="gallery/memt/original/memt_original_fig4.png" width="420"> | <img src="gallery/memt/memt_fig4_architecture.png" width="420"> |
| <img src="gallery/memt/original/memt_original_fig3.png" width="420"> | <img src="gallery/memt/memt_fig3_efficiency.png" width="420"> |

- Architecture: four panels answer where the memory sits, when it is read and written, how it is read and how it is written. The time panel is a state rail from M₁ = 0 through M<sub>t</sub> to M<sub>t+1</sub>, with a read under every token and one write per turn; the storage panel shows forget, erase and write on the matrix itself. One meaning per colour: grey frozen backbone, green memory state, blue read, purple write, amber hyper-memory parameters.
- Efficiency: the two log-axis bar panels become one slope chart in which the gap between Full Context and MemT-1.0-Nano opens from 1.86× to 3.99×, and storage is drawn to scale in units of Nano's 40 MiB state (a 130-cell block for Full Context, one cell for Nano). Every printed ratio is computed from the data in the script.

[Fig. 4 PDF](gallery/memt/memt_fig4_architecture.pdf) · [Fig. 3 PDF](gallery/memt/memt_fig3_efficiency.pdf) · [source](skills/cs-paper-figure/scripts/examples/memt/)

### Five more examples

Illustrative fixtures or synthetic data, not real benchmark results.

**Method.** A memory-update loop drawn as one clockwise cycle of real artifacts: ledger rows, three edit cards, a conflict matrix, the candidate record, and a paired-replay gate whose "3 > 1" drives the only arrow into memory v13.

<img src="gallery/after/method.png" width="760">

**Attention.** One eight-column grid runs through the cache slots, the 4 × 8 causal mask and the worked read for q10, so a key keeps its position from the slot that stores it to the weight it receives.

<img src="gallery/after/attention.png" width="760">

**Experiment.** One policy keeps one colour and marker in all four panels; the primary contrast (+6.6 pp) sits in a tinted band with its 24 seed-block dots, and the grand mean of the heat table is asserted equal to it.

<img src="gallery/after/experiment.png" width="760">

**Scene planning.** Three candidate rollouts share one scene; the stretch of the direct path inside the barrier is the thick stroke with a cross, and the only solid arrow is the first step that is executed.

<img src="gallery/after/scene-planning.png" width="760">

**Epoch context.** One coloured lane per replayed case crosses the three stages, so a regression can be followed from the check that flipped to the context edit it caused and the clause that cites it.

<img src="gallery/after/epoch-context.png" width="760">

[PDFs](gallery/after/) · [source](skills/cs-paper-figure/scripts/examples/restyled/)

## Installation

```bash
# 1. Skills CLI (Claude Code, Codex and other agents)
npx skills@latest add zichuanxu/cs-paper-figure-skill

# 2. Claude Code plugin
claude plugin marketplace add zichuanxu/cs-paper-figure-skill
claude plugin install cs-paper-figure@cs-paper-figure-skill

# 3. Codex plugin
codex plugin marketplace add zichuanxu/cs-paper-figure-skill
codex plugin add cs-paper-figure@cs-paper-figure-skill
```

Or copy `skills/cs-paper-figure` into `~/.claude/skills/`. The scripts need Python ≥ 3.10 with `matplotlib`, `numpy` and `pillow`.

## Usage

Ask your agent in plain language, for example "Redesign Figure 2 of this paper and beat it", "Draw the architecture figure from Section 3 at 170 mm width" or "Critique this figure and fix the worst problems".

To render the gallery yourself:

```bash
cd skills/cs-paper-figure
python scripts/examples/transformer/render_fig1.py --out out
python scripts/examples/harness2/render_fig2.py --out out
python scripts/paperkit.py compare original.png out/new.png side_by_side.png
```

**Generated images (optional).** With [Codex CLI](https://github.com/openai/codex) installed and logged in, `scripts/codex_images.py` generates a matched set of icons, scenes or vignettes from one JSON spec and records the prompt for disclosure. Without Codex the skill uses its vector icons.

```bash
python scripts/codex_images.py check
python scripts/codex_images.py generate icons.json --out out/icons [--ref existing_icon.png]
```

## Design rules in brief

1. One five-second message, carried by one hero element.
2. The manuscript's font at three sizes, nothing below 6 pt.
3. 3–5 colour roles, one meaning each; new parts saturated, inherited parts neutral.
4. Draw the noun: grids for matrices, trapezoids for projections, strips for tokens.
5. Orthogonal arrows, no crossings; narrative goes in the caption.
6. Charts: direct labels, visible ratios, area-true encodings.
7. Every number comes from the inputs and is asserted in code.
8. Icons, if any: one matched set, labelled, never carrying text or data.
9. Match the register: method figures reward restraint; an illustrated survey figure stays illustrated, with full cards, solid headers and large type.
10. Method figures: one dashed, tinted section per module, pseudo-3D tensors and layer slabs, a data object in every detail panel, and a key strip (learned from 23 CV/multimodal figures; see [`visual-craft.md` §12](skills/cs-paper-figure/references/visual-craft.md#12-the-architecture-register-object-rich-method-figures)).
11. Captions say what is shown and how to read it; how the figure was made or drawn, and protocol the methods already give, stay out (`paperkit.py caption` checks).

## License

[MIT](LICENSE), except the original figure crops in `gallery/*/original/`, each © its authors: MemT-1.0 (CC BY-NC-SA 4.0), Harness² and GroupAssistBench (CC BY 4.0), the Transformer (reproduced under Google's permission for scholarly use with attribution), and *Proactive AI for Superintelligent Agents*, ReHarness and ToolSpace (reproduced for commentary and comparison; removed on request). All redesigns are independent demonstrations, not affiliated with the papers' authors. Product and model logos in the ToolSpace example are the marks embedded in that paper's figure; they are trademarks of their owners and are used only to identify the products.
