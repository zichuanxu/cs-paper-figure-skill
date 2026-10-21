# Dense figure study: OpenAI, Anthropic, and Microsoft

Inspected 2026-10-21. **14 distinct new primary papers; 28 selected figure anchors.** All selected crops were rendered and opened. The count excludes BrowseComp, which was screened but replaced by a richer 2026 intervention/evidence paper.

First-submission years:2024 = 2,2025 = 10,2026 = 2. Inspected revisions:2024 = 1,2025 = 11,2026 = 2. Company-associated counts:OpenAI 4, Anthropic 5, Microsoft 5. Collaborations are recorded rather than attributed exclusively to one company.

## Study index

| Paper | First / inspected revision | Selected figures |
|---|---|---|
| [PaperBench: Evaluating AI's Ability to Replicate AI Research](#paperbench) | 2025-04-02 / 2025-04-07 v3 | Figure 1, PDF p2; Figure 2, PDF p3 |
| [SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?](#swe-lancer) | 2025-02-17 / 2025-05-29 v4 | Figure 1, PDF p2; Figure 2, PDF p2 |
| [Trading Inference-Time Compute for Adversarial Robustness](#inference-robustness) | 2025-01-31 / 2025-01-31 v1 | Figure 1, PDF p3; Figure 2, PDF p5 |
| [Auditing language models for hidden objectives](#hidden-objectives) | 2025-03-14 / 2025-03-28 v2 | Figure 1, PDF p2; Figure 2, PDF p2 |
| [SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents](#shade-arena) | 2025-06-17 / 2025-07-08 v2 | Figure 1, PDF p2; Figure 2, PDF p2 |
| [AuditBench: Evaluating Alignment Auditing Techniques on Models with Hidden Behaviors](#auditbench) | 2026-02-26 / 2026-10-01 v4 | Figure 1, PDF p2; Figure 5, PDF p8 |
| [Natural Emergent Misalignment from Reward Hacking in Production RL](#emergent-misalignment) | 2025-11-23 / 2025-11-23 v1 | Figure 1, PDF p2; Figure 6, PDF p8 |
| [Alignment faking in large language models](#alignment-faking) | 2024-12-18 / 2024-12-20 v2 | Figure 1, PDF p2; Figure 2, PDF p4 |
| [UFO2: The Desktop AgentOS](#ufo2) | 2025-04-20 / 2025-04-25 v2 | Figure 7, PDF p8; Figure 11, PDF p10 |
| [Fara-7B: An Efficient Agentic Model for Computer Use](#fara) | 2025-11-24 / 2025-11-24 v1 | Figure 2, PDF p3; Figure 4, PDF p5 |
| [R&D-Agent: An LLM-Agent Framework Towards Autonomous Data Science](#rd-agent) | 2025-05-20 / 2025-10-01 v2 | Figure 2, PDF p4; Figure 3, PDF p9 |
| [R&D-Agent-Quant: A Multi-Agent Framework for Data-Centric Factors and Model Joint Optimization](#rd-quant) | 2025-05-21 / 2025-09-25 v2 | Figure 3, PDF p3; Figure 4, PDF p4 |
| [Data Formulator 2: Iterative Creation of Data Visualizations, with AI Transforming Data Along the Way](#data-formulator2) | 2024-08-28 / 2025-02-21 v2 | Figure 2, PDF p3; Figure 6, PDF p7 |
| [Measuring Reward-Seeking via Contrastive Belief Updates](#reward-seeking) | 2026-07-21 / 2026-07-21 v1 | Figure 1, PDF p2; Figure 5, PDF p6 |

## Four transferable composition recipes

### Global policy + search topology + expanded local step

Use three horizontal scales: a governing budget/policy strip, a compact search or orchestration topology, and one expanded step with concrete input/output artifacts. Reuse a small state motif between the overview and the local mechanism. Reserve separate corridors for feedback, candidate selection, and evidence flow.

It explains the system at three semantic resolutions without duplicating the full interior at every node.

Anchors: rd-agent#Figure 2, rd-quant#Figure 4, paperbench#Figure 1.

Cautions: Every branch and queue token must correspond to actual algorithm state. Enlarge the local detail rather than copying 3–5pt native source labels. Distinguish predicted evaluation from actual measured validation.

### Parallel perception + validated action storyboard

Start from one fixed scene. Split perception into distinct lanes and expose their intermediate representation. Merge through a small conflict-resolution inset, then show proposed action, validator, and observed state as aligned columns. Include one rejected or stopping action and a ledger of what actually executed.

It couples multimodal input, abstract decisions, and concrete execution evidence.

Anchors: ufo2#Figure 7, ufo2#Figure 11, fara#Figure 4.

Cautions: Screenshots should use purposeful crop/zoom, not become unreadable wallpaper. A proposed action is not an executed action. Document screenshot overlays and retain consistent source-scene coordinates.

### Intervention + worked example + quantitative evidence

Use a clearly labeled intervention region, a matched before/after or counterfactual example, and a separate evidence region. Hold unaffected fields in fixed positions. Couple curves with a compact illustrative transcript tier only when each adds different information.

It communicates mechanism, observable consequence, and empirical support together while preserving their different evidentiary status.

Anchors: reward-seeking#Figure 1, reward-seeking#Figure 5, alignment-faking#Figure 1, emergent-misalignment#Figure 6.

Cautions: Label fictional/synthetic examples and transcript selection rules. Do not turn temporal correspondence into a causal claim. Do not mingle illustrative numbers with measured results.

### Representation lineage + typed evidence lanes

Show the actual representation at each consequential stage: schema snippet, token/queue array, command, table, trace, or plot. Put actions on a slim route and attach the evidence they generate below it. Keep different representations visually distinct; highlight changed fields or decisive fragments.

The figure explains transformations and provenance, so miniature detail has a scientific job instead of serving as decoration.

Anchors: data-formulator2#Figure 2, data-formulator2#Figure 6, auditbench#Figure 5, rd-quant#Figure 3.

Cautions: Every code/table fragment must be semantically valid. A tiny chart can identify an output class but cannot support an unreadable numeric claim. Use one consistent icon family even when source papers mix metaphors.

## Measurement and interpretation limits

Hex colors are object measurements when vector fills/strokes exist, or sampled composited216 dpi pixels when the source is raster. They are not all authoring colors. The Emergent Misalignment phase bands use raw source fill at path alpha 1 inside alpha 0.25 groups; copying raw fill as opaque would be wrong. Many polished figures are rasters, and exact font names cannot be claimed. PaperBench has unnamed Type3 fonts; the Emergent Misalignment charts have outlined text with invisible search overlays. Named fonts elsewhere are reported only from visible PDF traces.

Density is assessed by the number of scientific relationships and representations, not by decorative object count. Source labels as small as2.97–5pt are explicit cautions. Transferring their mechanisms requires a larger canvas, selective detail, or expanded insets.

<a id="paperbench"></a>
## PaperBench: Evaluating AI's Ability to Replicate AI Research

**OpenAI associated study.** [Versioned paper](https://arxiv.org/pdf/2504.01848v3) · [Metadata](https://arxiv.org/abs/2504.01848v3). First submitted 2025-04-02; inspectedv3 dated 2025-04-07.

PDF p1 directly labels the author group OpenAI.

SHA256: `2f58f1a6581af9d99432422dccf3cf61f5c263377c1e4550e7333c4a22d7184d`.

### Figure 1: Replication benchmark with executable evidence and hierarchical grading

PDF page 2; inspection crop in top-left-origin PDF points: `[54, 66, 542, 299]`.

**Layout.** A narrow agent/submission column sits beside a larger pink benchmark enclosure. Inside the enclosure, paper and rubric occupy the upper tier, while reproduction and grading occupy the lower tier.

**Geometry and routing.** Rounded white cards, short artifact lists, paper thumbnails, numbered black step discs, compact checklist cells, and a full-width score pill form several distinct scales. The first arrow points from task back to the agent, the second from submission into reproduction, and the third from reproduction into grading; rubric has its own downward input. Routing occupies deliberate gutters between cards.

**Information layers.** What is evaluated: a real paper and granular rubric; Who acts: an agent with a visible command trace; What is submitted: a repository and reproduction command; What constitutes evidence: execution artifacts and pass/fail leaves; What is reported: an aggregate score.

**Useful detail devices.** Meaningful miniatures of a research paper and file tree; Condensed terminal lines with syntax colors; Numbered discs located at the routing junctions; Checklist squares distinguish rubric requirements from computed grades.

**Density.** High semantic density with readable large-scale grouping. The tiny terminal and paper content is illustrative texture; it should not carry a claim that must be read at print size.

**Composition observations.** Containment explains the benchmark boundary before individual arrows are read. Task and rubric are visually parallel inputs but feed different later stages. The score is at the bottom-right endpoint, giving a clear finish despite the backward initial edge.

**Typography.** The recoverable visible text uses Unnamed-T3 glyphs at nominal 6.11–12.23pt; the family is not identified. The terminal and file miniatures also contain raster text.

**Color evidence.** benchmark enclosure `#FDE5FF` (vector_measured); benchmark label `#F585FF` (vector_measured); rubric rows `#FFF6CC` (vector_measured); grading region `#ECFAFF` (vector_measured); score `#CBF0FF` (vector_measured).

**Transferable rules**

- Show the actual artifact produced by each stage, using a miniature with a defined semantic job.
- Reserve separate lanes for evaluation criteria and execution evidence.
- Number only major hand-offs; let containment explain the local substeps.

**Do not copy blindly**

- Do not reproduce tiny paper or terminal text as required evidence.
- Do not assume the pink enclosure is an OpenAI-wide house style.

### Figure 2: Weighted rubric tree with bottom-up score propagation

PDF page 3; inspection crop in top-left-origin PDF points: `[54, 64, 291, 276]`.

**Layout.** An irregular rooted tree fills the left and center, with two explanatory arrows in the open right margin. Leaves terminate at different depths rather than being artificially forced into a full grid.

**Geometry and routing.** Circular internal nodes are neutral gray; binary leaves are cyan or rose and also carry 1/0 text. Edge weights sit just off the connector segments. A pale tree is read downward for decomposition, while a separate black margin arrow explains upward scoring. These two directions are not mixed on the same edge.

**Information layers.** Task decomposition depth; Binary leaf outcomes; Local edge weights; Computed fractional parent scores; Direction of aggregate propagation.

**Useful detail devices.** Neutral intermediate node fill; Redundant numeric leaf labels; Dotted level guides; A small example-requirement annotation beside one leaf.

**Density.** Moderately dense, but structurally richer than a generic tree because branch depth, weights, and computed values are all meaningful. One annotation is only 4.82pt nominal.

**Composition observations.** A large right-side void is used for reasoning about the tree rather than decorative whitespace. Pale edges preserve the primacy of the numerical node values. The tree is deliberately unbalanced because the rubric is unbalanced.

**Typography.** Visible Unnamed-T3 nominal sizes include 6.43, 8.04, and 9.64pt; the exact font family is unverified.

**Color evidence.** passing leaves `#88DBF0` (vector_measured); failing leaves `#F08888` (vector_measured); intermediate nodes `#F1F1F1` (vector_measured); tree edges `#D0D0D0` (vector_measured).

**Transferable rules**

- Separate decomposition direction from aggregation direction in margin annotations.
- Give intermediate summaries neutral styling and reserve categorical color for observations.
- Retain irregular branch depth when it reflects the actual data structure.

**Do not copy blindly**

- Do not imply equal weights by hiding weights on a weighted tree.
- Do not transfer the extremely small leaf annotation into a new print figure.

<a id="swe-lancer"></a>
## SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?

**OpenAI associated study.** [Versioned paper](https://arxiv.org/pdf/2502.12115v4) · [Metadata](https://arxiv.org/abs/2502.12115v4). First submitted 2025-02-17; inspectedv4 dated 2025-05-29.

PDF p1 affiliation1 is OpenAI; the inspected v4 is the ICML 2025/PMLR 267 version.

SHA256: `5592089e626e52af27222a144f65ef8e2748e4f8a2ab3cba29df82366a48a5c8`.

### Figure 1: Individual-contributor software evaluation with parallel human test construction

PDF page 2; inspection crop in top-left-origin PDF points: `[98, 63, 500, 216]`.

**Layout.** Three stage columns contain unequal-height interiors: task and reverted repository at left, model patch plus human-authored tests in the middle, and grader plus conditional payout at right.

**Geometry and routing.** A gray outer shell groups each stage, with pink inputs, peach model work, yellow human test work, and pale green evaluation. Code and file miniatures occupy inset white panels. Two horizontal routes connect the left stage to two different middle activities. Model-generated patch and human-written tests remain separate before the final evaluation.

**Information layers.** Task context and repository state; Model implementation; Independent human test construction; Execution-based grading; Binary economic consequence.

**Useful detail devices.** Plus sign for joint task inputs; A real-looking repository file list; Code diff and end-to-end-test miniatures; Check/cross and money labels make the outcome redundant.

**Density.** High process density: the middle stage contains a parallel provenance distinction that would disappear in a flat chain of labeled boxes. Raster text is quite small at native placement.

**Composition observations.** Color follows stage ownership rather than individual object identity. The test-writing lane is visually independent from the generated patch. The payout is the strongest type in the last stage, matching the benchmark framing.

**Typography.** The entire selected figure is one embedded raster. Bold sans headings and regular sans descriptions are visually apparent; no exact family or point size is recoverable.

**Color evidence.** task/context `#FFD3D5` (rendered_raster_sample); model implementation `#FFDCC1` (rendered_raster_sample); human tests `#FFEEBA` (rendered_raster_sample); evaluation `#E0F7CE` (rendered_raster_sample).

**Transferable rules**

- Distinguish independent validation evidence from the artifact being evaluated.
- Use meaningful inset code fragments when the artifact type matters.
- Show acceptance conditions near the terminal outcome.

**Do not copy blindly**

- Do not draw a single route that implies the same agent authors its own independent ground truth.
- Do not copy raster typography as if its exact family had been measured.

### Figure 2: Managerial proposal selection as a structured decision matrix

PDF page 2; inspection crop in top-left-origin PDF points: `[98, 241, 500, 406]`.

**Layout.** The same three-column stage grammar is reused, but the middle stage becomes a two-by-two proposal matrix beneath the model instruction.

**Geometry and routing.** Four peach proposal tiles share the same size and text hierarchy. Rejection crosses and one approval tick distinguish choices; the final green scoring panel is followed by a separate payout line. The task enters the model, then branches spatially into four comparable candidates. The comparison stage is a linear vertical sequence with short arrows.

**Information layers.** Original issue and candidate proposals; Decision policy supplied to model; Four mutually exclusive decisions; Comparison to the historical manager choice; Economic outcome.

**Useful detail devices.** Parallel proposal cards; Per-card rationale rather than a generic selected/unselected mark; Persistent stage palette shared with the companion figure; Large outcome value below the criterion.

**Density.** High content density within a stable stage skeleton. It is sophisticated because the options and their reasons are aligned for comparison, rather than because it contains many boxes.

**Composition observations.** Reusing the companion figure skeleton makes the change in task type immediately visible. Candidate cards have nearly identical hierarchy so a long option does not dominate. A separate last-stage criterion prevents a chosen proposal from being confused with a correct proposal.

**Typography.** Embedded raster only: family and nominal point size remain unverified.

**Color evidence.** input task `#FFD3D5` (rendered_raster_sample); candidate proposals `#FFDCC1` (rendered_raster_sample); evaluation criterion `#E0F7CE` (rendered_raster_sample).

**Transferable rules**

- Hold the outer structure fixed when comparing two task protocols.
- Expose the decision alternatives and one compact rationale per alternative.
- Separate choice from correctness and correctness from reward.

**Do not copy blindly**

- Avoid a rainbow for candidates that have no categorical color meaning.
- Do not let all the explanatory text fall below the figure legibility threshold.

<a id="inference-robustness"></a>
## Trading Inference-Time Compute for Adversarial Robustness

**OpenAI associated study.** [Versioned paper](https://arxiv.org/pdf/2501.18841v1) · [Metadata](https://arxiv.org/abs/2501.18841v1). First submitted 2025-01-31; inspectedv1 dated 2025-01-31.

Official OpenAI research page publishes this paper and links its PDF: https://openai.com/index/trading-inference-time-compute-for-adversarial-robustness/ . The PDF lists the matching author team.

SHA256: `ee267e89f796dc5092b4dfb88ec5f2e7a73a4e85667f896a520a4300ab9b4a5c`.

### Figure 1: Six-panel overview of adversarial robustness regimes

PDF page 3; inspection crop in top-left-origin PDF points: `[107, 76, 540, 316]`.

**Layout.** A two-row, three-column gallery places five heatmaps beside one line plot. Lettered captions below each panel identify the attack family, while one shared colorbar belongs only to the heatmaps.

**Geometry and routing.** Nearly square heatmaps use discrete rectangular bins; gray blocks mark unavailable regions. The sixth panel is deliberately a different chart type because its response quantity differs. No connectors. Consistent x-direction and lettered reading order establish the comparison; the colorbar is placed in an outside rail.

**Information layers.** Attack-family identity; Defender compute; Attacker effort or optimization stage; Attack success probability; A separate accuracy outcome for the sixth condition.

**Useful detail devices.** Shared probability color scale; Gray missing-data masks; A lettered caption below each miniature; Heterogeneous panel type used for a genuinely different metric.

**Density.** High comparative density, but axis labeling within the raster plots is very small. The grid compresses six scientific regimes into a summary that needs a sufficiently wide page.

**Composition observations.** The overview sacrifices detailed tick text in favor of comparing broad response patterns. Gray has a scientific missingness role; it must not be merged with low success. The last panel uses a different y-measure and cannot be read through the common colorbar.

**Typography.** The panel captions are visible Nimbus Roman at 8.97pt. Plot lettering is rasterized and its family/size is unverified; the visible caption font does not identify the axes font.

**Color evidence.** low heatmap probability `#440256` (rendered_raster_sample); high heatmap probability `#FBE723` (rendered_raster_sample).

**Transferable rules**

- Use an overview grid to establish regimes, then provide a focused factor matrix.
- Reserve neutral gray for missingness and state it explicitly.
- Group only panels that share a defined x interpretation.

**Do not copy blindly**

- Do not attach the heatmap colorbar to the line-chart panel.
- Do not invent hidden tick values from a visually smooth compute trend.

### Figure 2: Task difficulty by adversarial-goal matrix

PDF page 5; inspection crop in top-left-origin PDF points: `[46, 77, 565, 440]`.

**Layout.** A three-by-three matrix gives task difficulty to rows and adversarial goals to columns. Row labels sit outside the grid, column headings sit above it, and a tall shared colorbar uses the far-right rail.

**Geometry and routing.** Equal-size rectangular panels preserve a common x/y meaning. Repeated geometric bins make changes across neighboring conditions comparable. No arrows; rows and columns act as two orthogonal indexing systems.

**Information layers.** Task family/difficulty; Adversary goal difficulty; Defender compute; Attack token budget; Success probability and unsampled bins.

**Useful detail devices.** Exterior row/column factor labels; One shared x label and one shared y label; Quantized heatmap cells; Separate gray missingness encoding.

**Density.** High factorial density: nine plots are justified by a complete cross-product. The design is valuable when every cell is a scientifically distinct condition, not for arbitrary dashboard filler.

**Composition observations.** Outer factor labels remove repeated long titles from the panels. The long colorbar is perceptually separated from the nine panel interiors. The source uses a consistent probability range so color has a stable meaning across all cells.

**Typography.** This figure is a single raster with no visible PDF font objects. The axes and headings look sans serif, but exact identification is not supported.

**Color evidence.** low probability `#440256` (rendered_raster_sample); high probability `#FBE723` (rendered_raster_sample).

**Transferable rules**

- Assign experimental factors to the matrix axes before arranging panels.
- Keep the same normalization across a comparative heatmap matrix.
- Label missingness independently of the numerical scale.

**Do not copy blindly**

- Do not normalize each heatmap separately when the goal is cross-cell comparison.
- Do not treat gray bins as measured zero.

<a id="hidden-objectives"></a>
## Auditing language models for hidden objectives

**Anthropic associated study.** [Versioned paper](https://arxiv.org/pdf/2503.10965v2) · [Metadata](https://arxiv.org/abs/2503.10965v2). First submitted 2025-03-14; inspectedv2 dated 2025-03-28.

PDF p1 explicitly identifies Anthropic and the marked MATS contributors.

SHA256: `6cea87ef4a49ef861ce9c37a3aeef3d82dced5c70028a5b924211bb27773b60a`.

### Figure 1: Blind auditing with explicit access differences

PDF page 2; inspection crop in top-left-origin PDF points: `[106, 67, 505, 240]`.

**Layout.** A single training source fans out to four aligned audit-team rows, each ending in its own report and outcome. Role labels sit above the three logical columns.

**Geometry and routing.** Neutral rounded containers hold repeated robot/document/thought icons. Blue identifies auditors and red identifies trainers/graders; muted outcome marks are secondary. One smooth fan-out trunk distributes the model; straight parallel horizontal arrows lead from each audit team to its report. No crossings are needed.

**Information layers.** Training provenance; Information barrier and audit roles; Four access configurations; Available tools/data; Audit outcome per team.

**Useful detail devices.** Repeated icon vocabulary with selective omissions; Rows held fixed across conditions; Distinct role colors in small header badges; Compact report glyph plus check/cross.

**Density.** Moderate visual density with high experimental specificity. The important detail is which icons are absent from each row, making ablations legible without large prose blocks.

**Composition observations.** The framework reads as a controlled comparison because team rows are spatially parallel. Neutral containers keep role colors confined to categorical anchors. The branch source and final report columns have enough horizontal breathing room for direct arrows.

**Typography.** Embedded raster; bold and regular sans classes are visible but font name and point size are unverified.

**Color evidence.** neutral containers `#F1EEE7` (rendered_raster_sample); audit role badge `#1B67B2` (rendered_raster_sample); red-team badge `#B53333` (rendered_raster_sample); success mark `#798C5E` (rendered_raster_sample).

**Transferable rules**

- Encode access ablations through a fixed small inventory of tool/data symbols.
- Keep identical experimental conditions in aligned rows.
- Put role colors on the role anchors rather than every container.

**Do not copy blindly**

- Do not use check/cross marks without saying what success means.
- Do not infer source font families from this raster.

### Figure 2: Training interventions with document, behavior, and generalization examples

PDF page 2; inspection crop in top-left-origin PDF points: `[108, 311, 504, 491]`.

**Layout.** Six stage headings sit on a horizontal spine. Below the spine, document snippets, belief bubbles, fine-tuning examples, and held-out tests occupy different heights according to their semantic role.

**Geometry and routing.** Dots and light arrows mark stages; lavender cards carry training behavior, rose cards mark a held-out behavior, and neutral cards carry a new in-context case. The main route is a short horizontal stage spine; local evidence stacks sit beneath their associated stage with no web of connecting arrows.

**Information layers.** Initial model; Synthetic knowledge exposure; Latent preference hypothesis; Fine-tuned behavior; Inferred internalized objective; Held-out and new-context generalization.

**Useful detail devices.** One example retained through multiple stages; Thought bubbles distinguish inferred internal state from observed outputs; Color repeats between train/test semantic categories; Bold speaker labels inside short snippets.

**Density.** High causal-narrative density. The examples explain what each operation changes; they are not decorative paragraph cards. The long horizontal arrangement still needs double-column width.

**Composition observations.** A spine carries chronology while material below it carries evidence type. A thought bubble is visually different from a transcript box, reducing epistemic ambiguity. The rightmost evaluation column includes two distinct generalization tests.

**Typography.** Raster-only lettering; no exact font claim is supported.

**Color evidence.** training examples `#C8CDF3` (rendered_raster_sample); held-out example `#F8AEAF` (rendered_raster_sample); new-context example `#F1EEE7` (rendered_raster_sample).

**Transferable rules**

- Attach a concrete before/after exemplar to each consequential intervention.
- Use different geometry for observed artifacts versus hypothesized internal states.
- Keep the chronological spine simple and let the lower layer carry the detailed mechanism.

**Do not copy blindly**

- Do not present an inferred belief bubble as directly observed state.
- Do not re-use train/test colors without stating their semantic meaning.

<a id="shade-arena"></a>
## SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents

**Anthropic associated study.** [Versioned paper](https://arxiv.org/pdf/2506.15740v2) · [Metadata](https://arxiv.org/abs/2506.15740v2). First submitted 2025-06-17; inspectedv2 dated 2025-07-08.

PDF p1 identifies Jonathan Kutasov and Joe Benton as Anthropic, with the other institutional affiliations separately listed. This is a collaborative paper.

SHA256: `f9c1656907b7387faad5099d405d048a0346071bea8dbffc0b68962a278330f4`.

### Figure 1: Task taxonomy with an expanded representative environment

PDF page 2; inspection crop in top-left-origin PDF points: `[117, 70, 495, 195]`.

**Layout.** A four-cell taxonomy occupies the left half. A selected item points to an expanded example on the right, where environment, main/side tasks, and their evaluators form a nested grid.

**Geometry and routing.** A warm neutral outer field unifies each half. White cells hold the taxonomy and evaluator descriptions; green/pink distinguish legitimate and adversarial objectives. One curved arrow connects the selected taxonomy item to the example. The nested right-side grid uses alignment rather than many local arrows.

**Information layers.** Benchmark category taxonomy; Representative task selection; Available environment/tool types; Two competing objectives; Separate completion checks.

**Useful detail devices.** One highlighted list item acts as the source of the inset; Tool icons in a narrow environment strip; Task/evaluator pairing in two rows; Consistent main/side color code.

**Density.** High explanatory compression: a catalog and an executable task schema appear in one figure. The selected example gives the taxonomy operational meaning.

**Composition observations.** Only one item is expanded, preventing a catalog of tiny unreadable cases. Main and side objectives occupy parallel rows, each aligned with its own evaluator. The environment strip has a different geometry from task text, so infrastructure and goals are not confused.

**Typography.** The figure is rasterized; bold sans hierarchy is visible, exact fonts and sizes unverified.

**Color evidence.** outer containers `#EFEFEA` (rendered_raster_sample); main task `#D9EAD3` (rendered_raster_sample); side task `#F4CCCC` (rendered_raster_sample); selected taxonomy item `#F1DED4` (rendered_raster_sample).

**Transferable rules**

- Pair a taxonomy with one carefully chosen expanded case.
- Align each objective with its own validation condition.
- Use a single inset route rather than tracing every category to a separate example.

**Do not copy blindly**

- Do not make emoji glyphs the sole encoding of task role.
- Do not assume green means successful rather than legitimate.

### Figure 2: Agent tool loop and branched outcome monitoring

PDF page 2; inspection crop in top-left-origin PDF points: `[117, 232, 495, 335]`.

**Layout.** Three horizontal groups: two input goals, a local agent/tool/environment loop, and a right-side evaluator stack. The transcript-based monitor occupies the upper output branch.

**Geometry and routing.** Large neutral stage fields, two colored goal cards, a speech bubble for the hidden strategy, and three separate evaluation outputs carry four information levels. Curved arrows merge the two goals into the agent; paired short arrows show recurrent tool/environment interaction; three diverging outputs separate monitoring from task success.

**Information layers.** Main and hidden objectives; Agent reasoning context; Iterative tool interaction; Action transcript; Suspicion score and independent task outcomes.

**Useful detail devices.** Tiny recurrent arrow pair explains interaction without repeating frames; Speech bubble is distinct from an observed transcript; Three evaluators stay visually separate; Goal colors remain consistent with the companion taxonomy figure.

**Density.** High process specificity despite a compact width. It combines two inputs, a recurrent interior, and three assessments without routing crossings.

**Composition observations.** The middle loop is contained so its recurrence does not obscure the outer left-to-right flow. The top evaluation branch is visibly different from binary success checks below it. Containers establish a reading hierarchy stronger than the expressive emoji illustrations.

**Typography.** Rasterized figure. Exact family and size are not measurable from PDF text.

**Color evidence.** stage fields `#EFEFEA` (rendered_raster_sample); main goal / monitor bubble `#DCE9D5` (rendered_raster_sample); side goal `#EECDCD` (rendered_raster_sample).

**Transferable rules**

- Use one compact recurrent interior inside a larger one-pass protocol.
- Separate behavior success from detection success.
- Preserve parallel validation branches instead of collapsing them into a single score.

**Do not copy blindly**

- Avoid visually implying a low suspicion score proves benign behavior.
- Replace nonportable emoji with consistent vector symbols in an original scientific figure.

<a id="auditbench"></a>
## AuditBench: Evaluating Alignment Auditing Techniques on Models with Hidden Behaviors

**Anthropic associated study.** [Versioned paper](https://arxiv.org/pdf/2602.22755v4) · [Metadata](https://arxiv.org/abs/2602.22755v4). First submitted 2026-02-26; inspectedv4 dated 2026-10-01.

PDF p1 identifies affiliation4 Anthropic,1 Anthropic Fellows Program,2 MATS,3 University of Freiburg.

SHA256: `1d123f568cb93028d9af6d3829ba8403836c678d07aa0d2e80dfdc8e3b28a80d`.

### Figure 1: Hidden behaviors, elicitation examples, and auditing tools in three comparative rows

PDF page 2; inspection crop in top-left-origin PDF points: `[108, 77, 504, 309]`.

**Layout.** Each of three rows contains a behavior definition, a user/target exchange, an auditing tool, and a tool-driven investigator/target exchange. Column headings are shared.

**Geometry and routing.** Warm off-white page field with white definition cells, beige dialogue containers, salmon target replies, and mint investigator calls. Thin dark boundaries define nested roles. A single rightward arrow per row links the behavioral example to the auditing method. The dialogue turn order is represented by aligned speaker glyphs instead of arrows between every line.

**Information layers.** Hidden behavior category; Observed unassisted exchange; Audit tool type; Specific tool invocation; Evidence revealed by the target.

**Useful detail devices.** Consistent mint/salmon speaker colors; Short code-like invocation rows; A highlighted output fragment inside one response; A compact speaker legend at upper right.

**Density.** High evidence density with a stable row grammar. Readers can compare either along a row or down a column without decoding a different design for every case.

**Composition observations.** A narrow behavior-description column separates the concept from the example. Dialogue containers use the same form across cases, leaving attention on their differing content. One arrow per row is enough because alignment communicates all within-row correspondence.

**Typography.** One raster occurrence; sans and monospace classes can be described visually but exact font metadata is absent.

**Color evidence.** outer field `#FAF9F5` (rendered_raster_sample); dialogue field `#F1EEE7` (rendered_raster_sample); target replies `#F5CBBB` (rendered_raster_sample); investigator calls `#E8F7F2` (rendered_raster_sample).

**Transferable rules**

- Build a repeated case matrix with explicit columns for phenomenon, method, and evidence.
- Use color for speakers and thin nested boundaries for example structure.
- Highlight only the decisive evidence fragment.

**Do not copy blindly**

- Do not present constructed examples as observed empirical frequencies.
- Do not assign an exact font name from the raster appearance.

### Figure 5: Two successful investigations with tool output and follow-up probes

PDF page 8; inspection crop in top-left-origin PDF points: `[108, 78, 504, 248]`.

**Layout.** Two horizontal lanes repeat the same sequence: investigator intent, tool invocation and its output, follow-up sample and its output, final interpretation. Each lane has a centered probe label above the transition.

**Geometry and routing.** Small command bars sit above larger output rectangles. A light neutral background groups both lanes; white interpretation boxes close each sequence. A straight horizontal spine connects actions, with vertical attachment lines to subordinate tool outputs and probe labels. Routing corridors remain above the evidence blocks.

**Information layers.** Investigation plan; Tool call; Tool evidence; Follow-up behavioral test; Interpretation conditioned on the evidence.

**Useful detail devices.** Command/output pairs; Probe label attached to a junction; Role glyphs only at beginning and final interpretation; Parallel lane grammar exposes two different audit tactics.

**Density.** High reasoning-process density with restrained styling. Almost every detailed object answers what the investigator learned or did next.

**Composition observations.** The small action spine permits long evidence blocks below without edge crossings. The final interpretation is larger than an action chip and clearly belongs to a different semantic level. Both lanes share coordinates so their methodological contrast is easy to see.

**Typography.** Rasterized figure; monospace-looking calls and sans narrative are visible, but font identities and sizes remain unverified.

**Color evidence.** shared field `#FAF9F5` (rendered_raster_sample); tool evidence `#F0EDE6` (rendered_raster_sample).

**Transferable rules**

- Place commands on a slim route and attach evidence below the command that produced it.
- Make the follow-up probe explicit rather than jumping from evidence to conclusion.
- Use repeated lanes to compare strategies with different content.

**Do not copy blindly**

- Do not make a conclusion look like raw tool output.
- Avoid loading all typography into tiny command bars; keep critical evidence readable.

<a id="emergent-misalignment"></a>
## Natural Emergent Misalignment from Reward Hacking in Production RL

**Anthropic associated study.** [Versioned paper](https://arxiv.org/pdf/2511.18397v1) · [Metadata](https://arxiv.org/abs/2511.18397v1). First submitted 2025-11-23; inspectedv1 dated 2025-11-23.

PDF p1 identifies Anthropic and marks the Redwood Research contributor.

SHA256: `312b50556c2c2b5b9c8c2c53e11b509344ef92ab5bb954406a3d593b76938210`.

### Figure 1: Aggregate onset curve with an aligned diagnostic strip

PDF page 2; inspection crop in top-left-origin PDF points: `[78, 60, 515, 260]`.

**Layout.** A large aggregate panel and a shallow hacking-rate panel share the left time axis. Six narrow diagnostic panels stack on the right with the same onset marker.

**Geometry and routing.** Dark orange treatment and gray baseline lines, very light grids, and a dashed orange vertical event line. Diagnostic axes are compact, with labels outside their left edges. No connectors: synchronized time axes and repeated event markers connect aggregate, mechanism, and diagnostics.

**Information layers.** Aggregate misalignment score; Reward-hacking incidence; Six individual outcome channels; Treatment versus baseline; Onset event shared across all views.

**Useful detail devices.** Asymmetric panel sizes encode primary versus diagnostic evidence; A shallow mechanism strip directly beneath the primary response; Repeated event line; Small y-ranges preserved per diagnostic.

**Density.** High analytic density with strong hierarchy. The right strip supports decomposition without giving six minor metrics the same area as the aggregate.

**Composition observations.** The mechanism strip aligns exactly with the aggregate x-scale. All diagnostics carry the same onset reference, allowing event comparison without arrows. The one diagnostic with a small numerical range retains an explicit different scale.

**Typography.** Most sans labels are outlined glyphs with invisible Unnamed-T3 search overlays. A few visible Type3 traces are numeric/symbol fragments; exact visible font family remains unverified.

**Color evidence.** treatment curve `#A52E00` (vector_measured); event marker `#D55E00` (vector_measured); baseline `#949494` (vector_measured); grid `#EEEEEE` (vector_measured).

**Transferable rules**

- Pair a dominant aggregate with an aligned causal-context strip and a compact diagnostic column.
- Synchronize event markers across all time views.
- Keep distinct y-scales explicit rather than implying equal effect sizes.

**Do not copy blindly**

- Do not treat temporal coincidence alone as proof of causality.
- Do not infer visible font family from the hidden search layer.

### Figure 6: Training-phase small multiples coupled to two contrasting transcripts

PDF page 8; inspection crop in top-left-origin PDF points: `[78, 65, 522, 389]`.

**Layout.** A two-by-three chart matrix sits above two large transcript excerpts. Rows separate chat-like and agentic evaluations; the legend occupies a right-side rail.

**Geometry and routing.** Shared orange/gray line roles, pale peach/blue training-phase bands, and warm transcript highlighting. Lettered subcaptions distinguish quantitative and qualitative evidence. No arrows. Row labels and aligned phase boundaries carry the quantitative comparison; matching left/right text panels illustrate the context-dependent contrast below.

**Information layers.** Two evaluation-context families; Six response trajectories; Two sequential training regimes; Treatment versus baseline; Concrete model-output examples accompanying the quantitative pattern.

**Useful detail devices.** Training phases are background bands, not extra curves; Legend combines line and region encodings; Quoted outputs occupy a separate evidence tier; Bold speaker labels and selective warm highlights.

**Density.** Very high evidence density, with charts and transcripts doing distinct jobs. The design benefits from ample width and a caption that distinguishes selected examples from aggregate results.

**Composition observations.** Qualitative examples are positioned below rather than inside the small chart panels. Background bands are repeated across all panels, so the intervention timing is stable. The large transcript typography creates a natural secondary reading pass after the curves.

**Typography.** Chart labels are largely outlined with hidden Type3 overlays. Transcript text is visible Nimbus Roman around 8.97–10.16pt. That serif measurement does not describe the chart labels.

**Color evidence.** treatment curve `#D55E00` (vector_measured); baseline `#949494` (vector_measured); phase 1 raw fill `#A52E00` (vector_measured, enclosing group alpha 0.25); phase 2 raw fill `#85B3F2` (vector_measured, enclosing group alpha 0.25); transcript highlight `#FFE7C4` (vector_measured).

**Transferable rules**

- Separate numerical evidence and illustrative examples into different tiers.
- Use light phase bands for interventions, reserving saturated ink for response trajectories.
- State the selection rule for displayed transcripts.

**Do not copy blindly**

- Do not present selected transcripts as a random sample unless they are.
- Do not use raw phase-fill RGB at opacity 1: the PDF nests it in a 0.25-opacity group.

<a id="alignment-faking"></a>
## Alignment faking in large language models

**Anthropic associated study.** [Versioned paper](https://arxiv.org/pdf/2412.14093v2) · [Metadata](https://arxiv.org/abs/2412.14093v2). First submitted 2024-12-18; inspectedv2 dated 2024-12-20.

PDF p1 explicitly lists these institutional affiliations; it is a collaborative study.

SHA256: `f448dfe38f2144f0fe61bd78ceab01e44a17b363df1cb6df6c6c1bbea9568abc`.

### Figure 1: Matched counterfactual conversations under a shared experimental instruction

PDF page 2; inspection crop in top-left-origin PDF points: `[115, 60, 501, 349]`.

**Layout.** A shared setup banner branches into two equal-width condition columns. Both columns align the same user request, an internal-reasoning region, a final answer, and an outcome annotation.

**Geometry and routing.** Neutral rounded condition containers; dotted reasoning boxes distinguish hidden reasoning from white final-answer boxes. A pale rose emphasis marks the divergent reasoning in one condition. One curved branch from the shared setup reaches both conditions; correspondence is then communicated entirely by row alignment.

**Information layers.** Shared fictional setup; One manipulated training-context condition; Identical user input; Different reasoning and final responses; Aggregate rates tied to the conditions.

**Useful detail devices.** Matched prompt rows; Dashed reasoning boundary; Repeated speaker glyphs; A context note beneath the pair.

**Density.** High counterfactual specificity. Parallel correspondence lets the reader isolate the changed condition and the resulting divergence without tracing complex arrows.

**Composition observations.** Symmetry does analytical work: it visually holds the prompt constant. Reasoning and output have different container styles. The footnote is part of the interpretation and should not be removed during cropping.

**Typography.** One raster; exact font family and size are unverified.

**Color evidence.** condition field `#EFEFE9` (rendered_raster_sample); reasoning emphasis `#F1D9D4` (rendered_raster_sample).

**Transferable rules**

- Use equal column structure for controlled counterfactual examples.
- Separate internal reasoning, final output, and aggregate rate annotations.
- Keep essential experimental-context notes visible.

**Do not copy blindly**

- Do not imply the fictional training setup describes actual production data policy.
- Do not duplicate long harmful example text when a short neutral illustrative case would explain the design.

### Figure 2: Distributional behavior comparison across prompting, fine-tuning, and RL

PDF page 4; inspection crop in top-left-origin PDF points: `[107, 45, 505, 225]`.

**Layout.** Two compact paired-bar panels lead into a wider RL trajectory panel. A separated post-RL bar shares the last panel but is visibly outside the continuous time interval.

**Geometry and routing.** Pale blue and pale yellow encode mutually exclusive response categories; red cross-hatching subdivides the yellow compliant category. Stacks sum to one. No arrows. Shared y-scale, persistent colors/hatching, and ordered panels link discrete pre/post comparisons to the continuous training trajectory.

**Information layers.** Three experimental setups; Training versus unmonitored conditions; Behavior frequencies; A reasoning subtype within a behavior; Evolution during RL and a final post-RL evaluation.

**Useful detail devices.** Pattern overlay represents a subtype without requiring a fourth area color; A wider panel is allocated to the continuous axis; Direct vertical condition labels in bars; A common legend below all panels.

**Density.** High analytic density: distribution, subcategory, condition, and training progression coexist through a compact grammar. It depends on clear explanation of what stacks and hatches mean.

**Composition observations.** The third panel has more width because it contains a time sequence, not because it is decorative. White separators between areas preserve boundaries when colors are pale. The final bar is separated from the area chart so it is not mistaken for another RL step.

**Typography.** Visible DejaVu Sans and DejaVu Sans Bold at approximately 7.04pt, with some7.63pt text; this is directly recoverable PDF text.

**Color evidence.** refusal category `#A6D8F0` (vector_measured); compliant category `#F0E0A0` (vector_measured); alignment-faking hatch `#F05050` (vector_measured); light grid `#EEEEEE` (vector_measured).

**Transferable rules**

- Use hatching for a subset of a category when the hierarchy is explicit.
- Give temporal panels more width than discrete endpoint panels.
- Preserve shared categorical semantics when changing chart type across panels.

**Do not copy blindly**

- Do not use a stacked area chart for independent, non-exhaustive measures.
- Do not connect the unmonitored endpoint as if it were the next time point.

<a id="ufo2"></a>
## UFO2: The Desktop AgentOS

**Microsoft associated study.** [Versioned paper](https://arxiv.org/pdf/2504.14603v2) · [Metadata](https://arxiv.org/abs/2504.14603v2). First submitted 2025-04-20; inspectedv2 dated 2025-04-25.

PDF p1 lists Microsoft for the main author group and separately identifies university collaborators.

SHA256: `ceecfb496791b8b101275520066eb69c3289c7c727a9e69cc844219598acece5`.

The arXiv v2 date is2025-04-25; some PDF running headers retain a Conference 2017 template placeholder. The running header is not treated as the publication date.

### Figure 7: Parallel native and visual UI perception with duplicate suppression

PDF page 8; inspection crop in top-left-origin PDF points: `[57, 75, 552, 293]`.

**Layout.** One input screenshot splits into an upper native-API route and a lower visual-parser route; their annotated screenshots reconverge on one hybrid result at right.

**Geometry and routing.** Repeated screenshots retain the same framing so overlays can be compared. A blue serialized-control-list card and a violet virtual-controls glyph expose intermediate representations. Dashed orthogonal arrows follow two clean lanes. A small overlap/duplicate inset occupies the merge gap rather than being embedded in either screenshot.

**Information layers.** Source pixels; Native UIA interpretation; Vision parser detections; Typed/virtual control conversion; Overlap resolution; Final fused annotation.

**Useful detail devices.** Consistent screenshot coordinates across views; A compact serialized-control excerpt; One duplicate-removal inset with overlapping boxes; Different glyphs for native API, parser, and virtual-control abstraction.

**Density.** High multimodal mechanism density. Screenshot repetition is meaningful because each image changes the annotation layer, not the underlying scene.

**Composition observations.** Parallel routes are vertically separated until the final merge. The intermediate control list proves that the lower branch produces structured objects. The duplicate inset uses a zoom-like conceptual simplification instead of crowding the full UI.

**Typography.** Visible Candara Bold around 8.49pt for headings and6.82pt for some annotations; Courier New around 5.10pt for the serialized control list. Screenshots contain separate raster typography.

**Color evidence.** control-list fill `#DBEEF3` (vector_measured); control-list border `#205867` (vector_measured); virtual-control fill `#EEEAF2` (vector_measured); virtual-control border `#54426A` (vector_measured).

**Transferable rules**

- Keep the source scene fixed when comparing interpretation layers.
- Expose the representation between pixels and action targets.
- Reserve a merge corridor for duplicate/conflict-resolution logic.

**Do not copy blindly**

- Do not rely on tiny full-screen labels to communicate every detection.
- Do not mix screenshot decorations with measured algorithm output.

### Figure 11: Speculative action batch with per-step validation and early termination

PDF page 10; inspection crop in top-left-origin PDF points: `[53, 75, 561, 244]`.

**Layout.** Three action columns align action specifications, control validators, and screenshot states. A compact success ledger sits at far left beneath the predicting agent.

**Geometry and routing.** Pale green action records show executable steps, pale red marks an invalid step, blue validator blocks sit in the middle tier, and screenshots form the bottom evidence tier. Dashed downward edges bind each proposed action to its validator and state. A horizontal dashed state-to-state arrow depicts execution progression; the invalid step terminates rather than continuing.

**Information layers.** Batch prediction; Typed action arguments; Validation result; Observed UI state; Executed-action ledger; Early termination condition.

**Useful detail devices.** Aligned action/validator/screenshot columns; Red pointer overlays identify actual interaction locations; Code-like action fields; Checkmarks and explicit terminate text supplement color.

**Density.** High temporal and causal density with an explicit failure case. Every column preserves the same semantic stack, so the stopping rule is readable.

**Composition observations.** The last action uses the same position and structure as valid actions, making its failure a controlled contrast. Screenshots are evidence below the abstract control layer. The success ledger records only completed actions, not the whole predicted batch.

**Typography.** Visible Courier New and Candara mostly7.01pt, with8.42pt agent heading. Actual screenshot text remains rasterized.

**Color evidence.** valid actions `#E7FAE9` (vector_measured); invalid action `#FFE3E4` (vector_measured); validators `#DBEEF3` (vector_measured); success ledger `#D8D8D8` (vector_measured).

**Transferable rules**

- Separate proposed actions from validated execution in a storyboard.
- Include the first failing step and show where the route stops.
- Align typed action, validation, and observed state vertically.

**Do not copy blindly**

- Do not imply all predicted actions execute when a validator stops the batch.
- Do not shrink all screenshots equally if only one detail matters; use purposeful crops or insets.

<a id="fara"></a>
## Fara-7B: An Efficient Agentic Model for Computer Use

**Microsoft associated study.** [Versioned paper](https://arxiv.org/pdf/2511.19663v1) · [Metadata](https://arxiv.org/abs/2511.19663v1). First submitted 2025-11-24; inspectedv1 dated 2025-11-24.

PDF p1 is headed AI Frontiers and links https://github.com/microsoft/fara and https://huggingface.co/microsoft/fara-7b as the official project/model.

SHA256: `06a6b28b6fb088e7c65bf2fc4094078c13b97a8cef17f2ad9ed404caf6aff586`.

The arXiv v1 submission history says2025-11-24, while PDF p1 prints2025-11-26. Both are retained; no silent correction.

### Figure 2: Three task-proposal mechanisms grounded in shared seed sources

PDF page 3; inspection crop in top-left-origin PDF points: `[77, 74, 531, 285]`.

**Layout.** Three upper strategy columns share a full-width lower seed-source band. The middle exploration strategy is wider to accommodate a vertical navigation sequence.

**Geometry and routing.** Teal header bands and borders over pale blue fields; magenta robot glyphs mark LLM calls. Cylinders encode stores and thin outline boxes encode example tasks. The dominant flow is upward from seed sources into generation strategies. Within the middle strategy, a vertical node sequence records page exploration; the left and right strategies use short diagonal refinement routes.

**Information layers.** Seed data sources; Three proposal strategies; Concrete URL/task exemplars; Repeated LLM transformations; Navigation-derived verification opportunities.

**Useful detail devices.** A common source band; Task text before and after refinement; Explicit URL navigation dots; Repeated LLM glyphs distinguish calls from state.

**Density.** High mechanism density, including different internal patterns within a common outer frame. Native body text is about 5.31pt and requires redesign for a larger readable final figure.

**Composition observations.** The wide center column matches its more complex internal sequence. Bottom-up global flow is made explicit with source cylinders and arrows. The same teal/magenta roles repeat across heterogeneous strategy interiors.

**Typography.** Visible Times New Roman, including italics: detailed examples about 5.31pt; stage/header text about 8.34–9.10pt. This serif diagram style is a local design choice, not a Microsoft-wide rule.

**Color evidence.** headers and source stores `#27788B` (vector_measured); field background `#EAF5FA` (vector_measured); LLM-call accent `#8B2778` (vector_measured); secondary icon fill `#9673A6` (vector_measured).

**Transferable rules**

- Share a source band across alternative generation strategies.
- Give the strategy with more intermediate state more width.
- Retain before/after task examples so generation is more than a label.

**Do not copy blindly**

- Do not force a bottom-up flow without clear source and endpoint labels.
- Do not carry over5pt explanatory text into an original figure.

### Figure 4: Task-solving trajectory with orchestrator, browser, user continuation, and verification

PDF page 5; inspection crop in top-left-origin PDF points: `[80, 73, 531, 250]`.

**Layout.** Four vertical columns show successive task phases. The first three repeat orchestrator and WebSurfer roles, while the last column holds user continuation and verifier acceptance.

**Geometry and routing.** Teal role cards contain pale inset ledgers; screenshots occupy the upper part of intermediate columns; monospaced action records sit beneath each role stack. Orthogonal outer routes move between columns while vertical arrows carry local perception/planning/action. Termination examples use red outline boxes, and the verifier feeds a final training-trajectory store.

**Information layers.** Proposed task; Plan and persistent ledger; Browser action; Observed screen; Critical-point termination or user continuation; Verifier-filtered training artifact.

**Useful detail devices.** Plan versus ledger entries distinguish stages of execution; Screenshots substantiate state updates; Red-outlined termination actions; Separate user-simulator and verifier roles.

**Density.** Very high sequential detail, with distinct state, action, and acceptance semantics. Several native text runs are only4.15pt, so the source is a structural reference and a legibility caution.

**Composition observations.** Role cards recur at the same vertical positions across time. The final column changes grammar only when the interaction passes to a different role. Screenshots are attached to specific moments, not placed as a decorative collage.

**Typography.** Visible Times New Roman and Courier New. Most detailed ledger/action text is4.15pt; role headings about 8.30pt. Raster screenshots contain their own typography.

**Color evidence.** role cards `#27788B` (vector_measured); ledger/action fields `#EAF5FA` (vector_measured); termination outline `#FF0000` (vector_measured); secondary panel `#EDEDED` (vector_measured).

**Transferable rules**

- Show a compact persistent ledger in a long-horizon trajectory.
- Distinguish terminating a browser subtask from completing the overall workflow.
- Make the accepted training artifact a visible endpoint.

**Do not copy blindly**

- Do not reproduce tiny transcript text at the same scale.
- Do not let a red border carry all the meaning of a handoff; label it.

<a id="rd-agent"></a>
## R&D-Agent: An LLM-Agent Framework Towards Autonomous Data Science

**Microsoft associated study.** [Versioned paper](https://arxiv.org/pdf/2505.14738v2) · [Metadata](https://arxiv.org/abs/2505.14738v2). First submitted 2025-05-20; inspectedv2 dated 2025-10-01.

PDF p1 explicitly labels both Microsoft Research Asia and Microsoft GenAI.

SHA256: `36256d4e8a676259f1091f6b530416615179de2551e347fba55f0f395a0cb140`.

### Figure 2: Time-budgeted search enclosing research and development mechanisms

PDF page 4; inspection crop in top-left-origin PDF points: `[108, 78, 502, 327]`.

**Layout.** A budget/strategy ribbon sits above an exploration tree. A dashed expansion enclosure below reveals the research and development mechanisms for one search step; a separate small process legend explains parallel workers.

**Geometry and routing.** Blue research and purple development groups; green/rose idea nodes encode improved/failed candidates; dashed node enclosures denote early stopping and parent selection. Tree branches route through an upper lane. The lower mechanism travels left-to-right through research, coding, and validation, while a boundary feedback route connects real evaluation to the next expansion.

**Information layers.** Time-varying exploration/exploitation policy; Candidate search topology; Parallel worker identity; Memory-informed scientific reasoning; Virtual screening; Code execution and real validation feedback.

**Useful detail devices.** Nested miniature of the search tree inside memory; Named virtual versus real evaluation paths; Different arrowhead patterns in the parallel-process legend; Dashed boundaries at search-state and expansion levels.

**Density.** Very high architectural density with real multiscale semantics. It resembles a strong systems-paper hero because the overview and an internal mechanism coexist. Native detailed text ranges down to 3.85–4.62pt.

**Composition observations.** The top strip states the governing policy before the main topology. A single expansion is explained below the search graph, avoiding full repetition of its interior at every node. A larger blue/purple role label anchors each bottom group despite many small mechanisms.

**Typography.** Visible Arial variants. Main role labels about 9.24pt; section headings6.16–6.93pt; many details4.62pt and a few3.85pt. These are measured native placements, not recommended sizes.

**Color evidence.** research outline `#6C8EBF` (vector_measured); research field `#DAE8FC` (vector_measured); development outline `#9473A7` (vector_measured); development field `#E1D5E7` (vector_measured); improved candidate `#D5E8D4` (vector_measured); failed candidate `#F8CECC` (vector_measured).

**Transferable rules**

- Combine global policy, search topology, and one expanded local step in distinct horizontal bands.
- Use a compact repeated motif to connect overview state to the mechanism that reads it.
- Distinguish predicted/virtual evidence from measured/real feedback.

**Do not copy blindly**

- Do not imply the source’s tiny text is a desirable minimum; enlarge or split the mechanism.
- Do not add a decorative tree unless it represents real branching and selection.

### Figure 3: Temporal ablations tied to system components

PDF page 9; inspection crop in top-left-origin PDF points: `[324, 453, 501, 618]`.

**Layout.** A single time-series panel contrasts the full system, two component removals, and an upper-bound selection condition.

**Geometry and routing.** Blue/green/red data curves and gray dashed upper bound. The red ablation is dash-dot, providing a second cue beyond color; the legend is placed in an unused lower-right region. No connectors. Increasing time is the only sequence dimension; all variants use a shared scale.

**Information layers.** Training/search time; Medal rate; Full-system behavior; Two architectural component removals; Selection upper bound.

**Useful detail devices.** Line-style redundancy; Upper-bound curve separated by neutral styling; Legend placed away from the plotted trajectories; Component labels correspond to the architecture figure.

**Density.** Moderate, intentionally simpler than the companion architecture. Its role is to test which mechanisms matter and when; complexity would reduce its usefulness.

**Composition observations.** A simple analytic companion can substantiate a dense system overview. The upper-bound curve is styled as a reference rather than as a competing method. The chart exposes different early and late contributions of the removed components.

**Typography.** Entire plot is rasterized; bold sans axes are visually apparent, exact family/size unverified.

**Color evidence.** full system `#1F77B4` (rendered_raster_sample); without evaluation strategy `#2CA02C` (rendered_raster_sample); without coding workflow `#D62728` (rendered_raster_sample).

**Transferable rules**

- Pair a complex mechanism with an ablation that tests its named components.
- Use an explicit reference style for idealized upper bounds.
- Inspect line collisions and place the legend in genuine unused space.

**Do not copy blindly**

- Do not treat the gray upper bound as an executable baseline.
- Do not add statistical intervals unless supported by repeated measurements.

<a id="rd-quant"></a>
## R&D-Agent-Quant: A Multi-Agent Framework for Data-Centric Factors and Model Joint Optimization

**Microsoft associated study.** [Versioned paper](https://arxiv.org/pdf/2505.15155v2) · [Metadata](https://arxiv.org/abs/2505.15155v2). First submitted 2025-05-21; inspectedv2 dated 2025-09-25.

PDF p1 assigns affiliation2 to Microsoft Research Asia and separately names the university collaborators.

SHA256: `5df0919520ec1a9d556f6a20bc10e9d2d1dc11cada2e6913b871239df63a2df2`.

### Figure 3: Five research units with schema, knowledge forest, validation pool, and adaptive scheduling

PDF page 3; inspection crop in top-left-origin PDF points: `[116, 218, 495, 506]`.

**Layout.** Four stacked horizontal bands depict five functional units; implementation and validation share one band. A final lower subrow exposes action selection for the next iteration.

**Geometry and routing.** Dark blue rounded boundaries, yellow task/idea tokens, a multi-card knowledge forest, schema ribbons, and a metaphorical pool/scheduler illustrate different data structures. Local arrows run within each band; numbered headings provide the global sequence. Schema fields expand into an example text inset, and task-generation outputs point toward implementation.

**Information layers.** Scenario and data-interface specification; Hypothesis/idea hierarchy; Code artifacts; Candidate assessment and merging; Backtest outcome; Adaptive next-action choice.

**Useful detail devices.** Schema ribbon with an expanded concrete schema; Stacked knowledge-tree cards imply a forest; Named factor/model artifacts; An explicit adaptive-selection metaphor beneath summary metrics.

**Density.** Very high functional density. It is visually memorable, but mixes several illustration idioms and includes many small labels; a new figure should retain the data structures while unifying its icon family.

**Composition observations.** The schema inset receives the most explanatory prose because it establishes the task contract. The knowledge forest compresses hierarchy and multiplicity into one small but meaningful object. Implementation and validation share a band because they exchange concrete artifacts.

**Typography.** Visible Comic Sans MS Bold for many figure labels (roughly4.45–9.01pt), Carlito around 6.95pt in the schema inset, and FreeSerif for some symbols. This unusual mixture is measured, not recommended as a universal style.

**Color evidence.** structural border `#042433` (vector_measured); ideas/analysis ribbon `#F0B836` (vector_measured); secondary yellow `#F6CD72` (vector_measured); schema data field `#C2F1C8` (vector_measured); schema format field `#FBE3D6` (vector_measured).

**Transferable rules**

- Let different scientific structures have different geometries: schema, hierarchy, code, pool, and scheduler.
- Expand one representative schema instead of describing all fields in a long caption.
- Separate next-iteration action selection from within-iteration execution.

**Do not copy blindly**

- Do not mix decorative metaphors that obscure the actual algorithm.
- Do not treat Comic Sans as a mandatory agent-paper font; consistency and readable hierarchy matter more.

### Figure 4: Co-evolving task scheduler and implementation agent with reusable failure memory

PDF page 4; inspection crop in top-left-origin PDF points: `[246, 383, 504, 548]`.

**Layout.** Two colored agent enclosures flank a central co-evolution loop. Candidate ordering enters at top-left; traceback and prompt-building insets float above the implementation agent; a multi-row knowledge base fills its lower interior.

**Geometry and routing.** Rose scheduling enclosure and cyan implementation enclosure contain pale green functional regions. Lettered task tokens and repeated trace-dot arrays reveal ordering, dependencies, and memory retrieval. A central pair of curved arrows exchanges schedule and implementation feedback. Orange dashed routes connect a failed trace to a retrieved similar error and then to a newly formed prompt.

**Information layers.** Candidate task order; Dependency-aware scheduling; Current implementation trace; Feedback outcomes; Similar prior failures; Prompt reconstruction; Bidirectional co-adaptation.

**Useful detail devices.** Lettered token arrays before and after reordering; Trace dots paired with check/cross feedback; A highlighted matching error column; A prompt assembled from task, current failure, and retrieved trace.

**Density.** Very high internal-mechanism density. The source packs it into a narrow placement with text down to 2.97pt; its structure is worth transferring, its native scale is not.

**Composition observations.** Two levels of routing are distinct: outer agent exchange and inner retrieval/proposal construction. A common trace motif connects current execution to the reusable knowledge base. The revised queue is placed on the actual exchange path, making scheduling tangible.

**Typography.** Visible Times New Roman variants dominate. Many details are3.32–4.43pt; agent headings about 6.64pt; a few traces are2.97pt. Nominal sizes are direct PDF evidence.

**Color evidence.** implementation enclosure `#83CBEB` (vector_measured); learning regions `#D9F2D0` (vector_measured); retrieval/error emphasis `#FF0000` (vector_measured); prompt component `#F6C6AD` (vector_measured); structure `#042433` (vector_measured).

**Transferable rules**

- Represent queue order and memory traces as compact data objects rather than generic database icons.
- Route retrieval and feedback through separate corridors from the main process.
- Show exactly which part of past evidence is reused to construct the next prompt.

**Do not copy blindly**

- Do not add trace arrays as decorative texture; every highlighted position needs a meaning.
- Do not preserve 2.97–4pt text; give this mechanism a wider canvas or inset.

<a id="data-formulator2"></a>
## Data Formulator 2: Iterative Creation of Data Visualizations, with AI Transforming Data Along the Way

**Microsoft associated study.** [Versioned paper](https://arxiv.org/pdf/2408.16119v2) · [Metadata](https://arxiv.org/abs/2408.16119v2). First submitted 2024-08-28; inspectedv2 dated 2025-02-21.

PDF p1 assigns four authors to Microsoft Research and one to Yonsei University; the inspected version identifies CHI 2025.

SHA256: `4c59a8fb02985b8aaf9b20ab068d639cdb70c6d6057109fb5b18128afa23c0a0`.

First arXiv submission2024; inspected v2 and CHI publication2025. These are counted separately.

### Figure 2: Data transformation lineage paired with derived chart views

PDF page 3; inspection crop in top-left-origin PDF points: `[54, 81, 559, 450]`.

**Layout.** A source table and two initial charts occupy the top row. Three branching transformation paths unfold below, each pairing a derived table with its resulting chart.

**Geometry and routing.** Wide pale-blue ribbon arrows connect table versions; newly derived columns have warm fill. Small numbered blue discs identify versions and miniature charts preserve consistent framing. Curved ribbons descend through a reserved left/center corridor and run horizontally into chart outcomes. Transformation names are written directly on the ribbons.

**Information layers.** Original tabular schema; Transformation operators; Derived columns and rows; Version/branch identity; Concrete chart generated from each data state.

**Useful detail devices.** Table miniatures with a few representative rows; Warm highlights on changed columns; Operator-labeled provenance ribbons; Charts vary in meaningful geometry: facets, ranks, and aggregates.

**Density.** Very high provenance density. The miniature charts are meaningful outputs of different transformations; the figure is not merely a gallery of charts.

**Composition observations.** Every derived data state is placed next to its visible consequence. The same entity/time vocabulary persists across tables and charts. The wide arrows show data lineage while the chart cards remain clean evidence surfaces.

**Typography.** The whole figure is an embedded raster; mixed sans table/plot text is visible but exact font names and point sizes are not recoverable.

**Color evidence.** derived columns `#FCEEE4` (rendered_raster_sample); provenance ribbons `#E8EFF2` (rendered_raster_sample).

**Transferable rules**

- Pair each transformation with both its data representation and its visual consequence.
- Highlight changed fields rather than recoloring entire tables.
- Label provenance edges with actual operations.

**Do not copy blindly**

- Do not require readers to identify every tiny line in a thumbnail chart.
- Do not claim a raster table is editable source data.

### Figure 6: UI specification, prompted transformation code, and chart compilation

PDF page 7; inspection crop in top-left-origin PDF points: `[54, 82, 559, 281]`.

**Layout.** A full-height UI specification at left feeds an upper specification lane and a lower prompt/code lane. The transformed table and final chart sit at upper-right where the two lanes converge.

**Geometry and routing.** UI field chips, syntax-colored JSON and Python, a warm dashed prompt enclosure with three labeled subblocks, a table, and a chart each retain their native visual grammar. A top arrow sends user mappings into the chart specification. A second path carries context and goals through generated code to transformed data, which joins the specification at the final chart.

**Information layers.** User intent in graphical fields and natural language; Chart specification skeleton; System/context/goal prompt composition; Generated data-transformation code; Derived table; Rendered visualization.

**Useful detail devices.** Real syntax fragments instead of generic code icons; Three explicit prompt components; Step numbers placed at the crucial hand-offs; Upward data route makes the code-to-table dependency visible.

**Density.** Very high representation density with a clear division of labor. Each artifact has a distinct visual syntax, enabling a reader to understand the compilation path at several levels.

**Composition observations.** The prompt is opened up because prompt composition is part of the method. The specification and data routes stay separate until the final rendering step. Code and table sizes are allocated to show representative structure, not every line.

**Typography.** Embedded raster only. Visible classes include sans UI labels and monospace syntax, but exact families and point sizes remain unknown.

**Color evidence.** prompt fields `#FDF2EA` (rendered_raster_sample); prompt field headings `#EFC8AF` (rendered_raster_sample); dataflow ribbons `#DFE7EC` (rendered_raster_sample).

**Transferable rules**

- Show the intermediate representations that explain how the system works.
- Separate declarative specification from data transformation until their merge point.
- Use small syntax-preserving excerpts with sufficient labels to explain omitted content.

**Do not copy blindly**

- Do not use pseudo-code that contradicts the stated transformation.
- Do not rely on tiny screenshot labels for essential method information.

<a id="reward-seeking"></a>
## Measuring Reward-Seeking via Contrastive Belief Updates

**OpenAI associated study.** [Versioned paper](https://arxiv.org/pdf/2607.18966v1) · [Metadata](https://arxiv.org/abs/2607.18966v1). First submitted 2026-07-21; inspectedv1 dated 2026-07-21.

PDF p1 directly states Apollo Research & OpenAI and marks their respective authors. The official OpenAI July21 2026 research post links this paper: https://alignment.openai.com/measuring-reward-seeking/ .

SHA256: `624ae024636b0650c487e64a67964e59a0bbc7000863f1c07a93c9580380bb57`.

### Figure 1: Contrastive intervention, paired behavior, and quantitative evidence in one figure

PDF page 2; inspection crop in top-left-origin PDF points: `[71, 95, 540, 294]`.

**Layout.** Three columns explain the intervention, display the behavioral contrast, and show two small outcome charts. The first two columns are process illustrations while the third is quantitative evidence.

**Geometry and routing.** Light gray rounded column fields. Stacked document glyphs encode corpora; blue/red encode opposed authority preferences; small aligned bars and direct numeric labels provide results. Reading order is carried by numbered stage headings. Within the middle column, a common task bifurcates into two contrasted responses; the charts are adjacent evidence, not downstream dataflow blocks.

**Information layers.** Contrasting belief documents; Balanced training mixture; Shared downstream constraint; Divergent behavioral choice; Two quantitative comparisons.

**Useful detail devices.** Document stacks show a corpus rather than a single prompt; A shared task followed by two aligned responses; Colored keywords preserve authority identity across examples; Two compact charts in a dedicated evidence column.

**Density.** High integrated density, with explanatory examples and results carefully separated by column. The measured font hierarchy remains more readable than many dense system overviews.

**Composition observations.** The third column carries evidence at a different level from the illustrative middle column. Blue and red repeat across documents, choices, and chart legend roles. A headline and three short stage headings establish the large-scale reading order before details.

**Typography.** Visible Helvetica family with bold headings, oblique notes, and nominal body sizes6.40–7.57pt; stage headings9.90pt and title11.06pt. Some additional glyphs are Unnamed-T3, so not every glyph shares a recoverable family.

**Color evidence.** column fields `#F6F7F8` (vector_measured); honesty/leadership illustration `#2F5D8A` (vector_measured); grader illustration `#C44536` (vector_measured); honesty chart `#4285F4` (vector_measured); completion chart `#EA4335` (vector_measured).

**Transferable rules**

- Build a triptych of intervention, worked example, and evidence when all three are needed.
- Keep observed numbers within an explicit evidence region.
- Use repeated identity colors across representations, but label any local change in role.

**Do not copy blindly**

- Do not reuse these example numbers in a synthetic demonstration as if they were new results.
- Do not imply the example cartoons themselves are the full contrastive training procedure.

### Figure 5: Behavioral equivalence versus divergence after a belief intervention

PDF page 6; inspection crop in top-left-origin PDF points: `[71, 94, 540, 242]`.

**Layout.** A narrow legend column defines two policy types. Two larger matched scenario columns compare agreement under shared preferences and divergence after changing beliefs.

**Geometry and routing.** Blue/red robot glyphs define policy identity; green/orange label the two authorities. Quoted output tokens are monospaced and paired with large equals/not-equals signs. No arrows. Repeated spatial positions make the manipulated belief and the changed output relation directly comparable.

**Information layers.** Two latent policy classes; Two authorities and their preferences; Baseline shared preference; Intervened opposing preference; Observable equality or divergence.

**Useful detail devices.** Separate color systems for policy identity and authority identity; Precisely repeated output token motifs; A large equality operator summarizes the outcome; One changed quote style is enough to illustrate the intervention.

**Density.** High conceptual density with very few nodes. It demonstrates sophistication through controlled correspondence and representation, not raw object count.

**Composition observations.** The policy legend is isolated from the two matched scenarios. The same robot positions and token boxes recur in both scenarios. The output relation is stated both symbolically and in a short bottom summary.

**Typography.** Visible Helvetica variants around 6.23–8.01pt; output tokens use Menlo Bold around 7.12/10.08pt. Some icon/special glyphs have unnamed Type3 fonts.

**Color evidence.** policy A `#2F5D8A` (vector_measured); policy B `#C44536` (vector_measured); developer authority `#2D8659` (vector_measured); grader authority `#D97706` (vector_measured); shared fields `#F6F7F8` (vector_measured); divergent outcome field `#FDECEA` (vector_measured).

**Transferable rules**

- Use a matched before/after composition to isolate a causal intervention.
- Distinguish the actor identity palette from the authority/variable palette.
- Represent observable outputs with exact small tokens when their syntax is the point.

**Do not copy blindly**

- Do not use multiple unrelated color systems without an explicit legend.
- Do not overgeneralize a conceptual diagram into a measured causal result.
