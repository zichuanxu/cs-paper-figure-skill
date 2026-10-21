# Figure patterns for CS research

## Contents

1. Compose a scientific argument
2. Method and architecture diagrams
3. Agent, memory, and harness workflows
4. Curves, scaling, and efficiency
5. Comparisons, ablations, and distributions
6. Diagnostic fields and qualitative evidence
7. Data flows and hardware schedules
8. Select a visual explanation without overclaiming

Use the [modern paper atlas](modern-paper-atlas.md) first for inspected 2025–2026 primary sources, exact versions/pages, measured color/font/geometry evidence and limitations. Keep the [foundational paper atlas](paper-atlas.md) for earlier examples. The patterns below are design recommendations synthesized for this skill, not claims about a universal corporate style. Apply [visual-design.md](visual-design.md) for the full palette, typography and shape system, and [diagram-routing.md](diagram-routing.md) for connector construction.

## 1. Compose a scientific argument

Give each panel a job. A useful three-panel structure is **mechanism → controlled evidence → boundary/failure**, but only include panels that answer different necessary questions. One strong panel can be a complete figure.

For a paper's figure set, distribute roles across figures:

| Role | Reader's question | Common mistake |
| --- | --- | --- |
| Problem illustration | What limitation motivates the work? | Inventing a striking failure without showing its frequency |
| Method | What operation or system changes? | A generic pipeline that hides the actual contribution |
| Main result | What is the observed benefit under stated conditions? | A leaderboard with confounded budgets |
| Mechanistic analysis | Which controlled change explains the effect? | Calling an uncontrolled correlation an ablation |
| Boundary | When does the method fail or stop helping? | Showing only favorable tasks or scales |

Avoid repeating the same ranking as a bar plot, radar chart, and table. Use the space for uncertainty, per-task heterogeneity, or a distinct scientific question.

## 2. Method and architecture diagrams

### Minimal mechanism

Use when the contribution can be expressed as a small transformation or operator. Show inputs, changed operation, outputs, and any bypass or state needed to understand it. Make the key mathematical operator visible. A compact monochrome mechanism can communicate more than a large colored system map.

**Reference route:** ResNet, Fig. 2.

**Guardrail:** verify activation, normalization, addition, and residual ordering against the actual method. Do not substitute a familiar diagram for the implemented topology.

Use minimal treatment when the mechanism is genuinely small. For a system with multiple kinds of state, scope or computation, choose a richer grammar rather than forcing the entire contribution into a few undifferentiated rectangles.

### Overview plus expansion

Show the full computation at low detail; enlarge one novel submodule beside or beneath it. Connect the expansion to the relevant block with an explicit locator whose style differs from computational edges. Reuse the block's name and semantic color at both scales. Give the detailed mechanism more area when it carries more explanation. Compress identical repetition with `×N` and explain any exceptions. A small token sequence, record, tensor stack or operator junction can make the operation concrete when it matches the actual method.

**Modern reference route:** Qwen3.8-Next Fig. 1; DeepSeek-V4 Figs. 2–3; Engram Fig. 1. **Foundational route:** Transformer Figs. 1–2; DeepSeek-V2 Fig. 2.

**Guardrail:** do not mix token-level, layer-level, and system-level detail without framing the scale change. Make trainable/frozen modules explicit only where relevant; color alone is insufficient.

### Aligned alternatives

Compare designs using invariant input/output rows, matched orientation, and repeated glyphs. Emphasize the structural difference with an accent, hatching, or local annotation. Keep shared machinery visually quiet.

**Modern reference route:** Engram Fig. 2; V-JEPA 2 Fig. 2; Qwen3-VL-Embedding/Reranker Fig. 2. **Foundational route:** DeepSeek-V2 Fig. 3; Nemotron-H Fig. 2.

**Guardrail:** state whether the number/size of repeated glyphs is literal or schematic. Preserve tensor dimensions and caching semantics; do not imply an unmeasured memory saving with a smaller decorative box.

### Multi-stage training or multimodal flow

Separate phases or modalities into lanes. Carry entity identity through every transformation; name the output artifact passed between stages. Mark training versus inference and supervised versus feedback operations where that distinction explains the method. Align repeated blocks, token strips and lane ports on a deliberate grid. A shared operation can span lanes only when the underlying mechanism is actually shared.

**Modern reference route:** Cosmos 3 Fig. 5; HunyuanVideo 1.5 Fig. 2; Qwen3-VL-Embedding/Reranker Fig. 5; Qwen3 Fig. 1; HunyuanImage 3.0 Fig. 3. **Foundational route:** CLIP Fig. 1; InstructGPT Fig. 2.

**Guardrail:** distinguish a model, a dataset, an objective, and a generated output. An arrow must have one intelligible meaning; label exceptions to the main flow.

### Typed objects and nested scope

Use pale enclosing regions for real phases, ownership or control scope; white child cards can expose components within that scope. Distinguish data/artifacts, persistent state and computation with a small stable shape vocabulary. For example, a folded corner can identify a document, a record stack can show state, and a rounded model block can identify a checkpoint. Pair each family with a coherent fill, border and text treatment.

Use labeled vector icons, status marks or small artifact miniatures when they explain a known role or distinction. Keep their stroke and size consistent, and ensure text remains sufficient to decode them. Do not turn every container into a card or every node into an icon; choose the vocabulary required by the method.

**Modern reference route:** Harness² Fig. 2; Qwen3-VL-Embedding/Reranker Fig. 5; HunyuanImage 3.0 Fig. 2; HunyuanVideo 1.5 Fig. 1.

**Guardrail:** nesting must express actual scope, and an icon or badge must not imply a tool, status, update frequency or evaluation step that the system lacks. Separate group boundaries from computational nodes when validating routes.

## 3. Agent, memory, and harness workflows

Use three conceptual layers when the system warrants them:

| Layer | Typical objects | Questions to make visible |
| --- | --- | --- |
| Task execution | User query, planner/controller, tools, answer | Who chooses an action? What observations return? |
| Persistent state | Episodic memory, knowledge store, skill registry | What survives a task? Which component reads or writes? |
| Adaptation | Evaluator, repair/update policy, parameter training | What evidence triggers a change, and what changes? |

Draw only layers present in the actual system. Show read and write paths separately. A retrieved memory is not an update; a textual reflection is not automatically a parameter change. Distinguish temporary context from persistent storage. For tool calls, separate the outbound action from the returned observation. For multi-agent systems, show message ownership and synchronization only where it explains behavior.

Reserve explicit ports and separate corridors for call, observation, memory read and memory write routes. Give the return path enough space to leave the tool boundary outward and enter its destination normally. Never let a connector coincide with a container border. Keep scope boundaries visually quieter than the actual data/control edges.

When the method operates at two time scales, use a two-level storyboard or aligned scope lanes. Distinguish the within-task loop from between-task adaptation with labels and route grammar. A growing conversation-state strip can explain retained versus discarded context more directly than a dense web of return arrows.

**Modern reference route:** Harness² Figs. 2–3 for nested scope and recursion; DeepSeek-V3.2 Fig. 4 for aligned context snapshots; Anthropic's *Automated Researchers Can Reliably Mitigate Alignment Failures*, Fig. 2, for an automated research workflow. Follow the atlas for exact versions and limitations.

For a memory-repair study, a useful original composition is a system overview plus a small aligned before/change/after state strip, supported by an empirical repair-versus-detection plot. Keep the state strip schematic unless it contains genuine logged examples. This is an application pattern developed for the skill, not a copied lab figure.

For harness bottlenecks, connect each resource constraint to the affected operation and show measured capability/cost separately. Do not use arrow thickness or a "bottleneck" icon as a substitute for measured load or throughput.

## 4. Curves, scaling, and efficiency

### Learning or test-time curves

Use a real ordered coordinate: steps, examples, tokens, calls, wall time, or compute. Show sparse markers on a line when the line connects measured checkpoints. Use intervals whose unit and construction are known. If raw variability and a smoothed trend both matter, show both with clear hierarchy.

Pair an endpoint view with trajectories only when it reveals a distinct result, such as initial improvement followed by relapse. Keep condition colors consistent across both views.

**Modern reference route:** Qwen3 Fig. 2; Qwen3.8-Next Fig. 6; Gemini 2.5 Fig. 4. Use the first for budget response, the second for workload-conditioned latency, and the third for aligned long-context curves. **Additional route:** DeepSeek-R1 Figs. 2–3; Sleeper Agents Fig. 2.

**Guardrail:** distinguish a changing model from a fixed horizontal reference; do not compare nominal steps if per-step compute differs materially. Never infer the meaning of a shaded band from appearance.

### Scaling laws

Use measured points, distinct fit lines, and visibly differentiated extrapolation. Use small multiples to separate compute, parameter count, and dataset size. For iso-budget curves, maintain a stable budget encoding and identify the measured minimum separately from a fitted optimum.

**Modern reference route:** Engram Fig. 3. **Foundational route:** Scaling Laws Fig. 1; Chinchilla Figs. 1 and 3; HunyuanVideo Fig. 10. Translate source typography to readable final-size text; do not inherit tiny ticks or dual axes without checking their interpretation.

**Guardrail:** log scaling requires valid positive values; a straight line does not establish a power law. Disclose fitted ranges, model assumptions, and independently scaled panels.

### Quality versus cost

Plot absolute performance against a defined resource. Directly label a manageable number of models, or use a consistent key for many points. Use shape for a second meaningful grouping. State the preferred direction on both axes. Outline the observed nondominated points if helpful, preserving all observations.

**Modern reference route:** Gemini 2.5 Fig. 1 for direct labels and selective emphasis; Nemotron-H Fig. 1 for resource-conditioned comparisons. **Additional route:** Constitutional AI tradeoff framing; Llama 3 Fig. 27. Preserve workload/hardware conditions when adapting the visual treatment.

**Guardrail:** a tradeoff set is conditional on measured configurations. Do not draw a smooth frontier that suggests attainable unmeasured systems. Put hardware and workload assumptions close to efficiency comparisons.

## 5. Comparisons, ablations, and distributions

### Benchmark comparisons

Use aligned dots and intervals when the important task is judging estimates and precision. Use grouped bars when a small number of magnitudes and a meaningful zero baseline make bars clearer. For many datasets, show per-dataset deltas with a zero reference and a separately defined aggregate.

**Modern reference route:** Harness² Fig. 1; OpenAI's *Reasoning Models Struggle to Control their Chains of Thought*, Fig. 1. Use explicit focal/reference roles, aligned panel geometry and local annotations. **Foundational route:** InstructGPT Fig. 1; Segment Anything Fig. 9; statistical-precipice Fig. 9.

**Guardrail:** retain losses as well as gains, preserve metric direction, distinguish deployable results from oracle/reference results, and avoid ranking by tiny differences unsupported by precision.

### Controlled ablations

Use a dot-and-interval panel of paired differences, a slope graph for a small number of matched units, or small multiples for interacting factors. Put the null at zero for differences and one for ratios. Explain baseline and intervention labels without abbreviations that require rereading the paper.

**Modern reference route:** Qwen3.8-Next Fig. 5. Keep component identity, baseline reference and facet alignment consistent. A source bar chart is an encoding option, not an instruction to invent intervals or convert every ablation into bars.

**Guardrail:** adding/removing components can change budget or capacity. Mark those differences. Do not convert a descriptive quantile range into a confidence interval.

### Distributions and reliability

Use ECDFs or performance profiles when thresholds and tails matter; use individual observations with a box/interval summary for small samples. Keep bins or density choices meaningful and consistent. Show the count per group. An aggregate can sit alongside the distribution, but should not conceal subgroup failures.

**Reference route:** statistical-precipice Fig. 7.

**Guardrail:** label whether the curve represents observations, task averages, runs, or a fitted distribution. Dense jitter is not a substitute for disclosing the sampling hierarchy.

## 6. Diagnostic fields and qualitative evidence

### Heatmaps and phase diagrams

Put related conditions in an intelligible order. Label both axes and the colorbar with the actual quantity. Keep normalizations shared across comparisons. Use a meaningful diverging center for signed changes. Render unmeasured cells in a distinct neutral pattern or missing-data mark. Add contours only when they correspond to a defined boundary or interpolated model.

**Modern reference route:** HunyuanImage 3.0 Fig. 4 for aligned structural masks; Cosmos 3 Fig. 5 for an architecture-linked attention-mask inset. **Foundational route:** Toy Models linked matrices/phase diagrams; Qwen2.5 Fig. 2.

**Guardrail:** a uniformly saturated field can hide small differences; use a supplementary delta view or more informative scale without exaggerating noise. If a boundary is fitted or schematic, say so.

For a binary connectivity mask, define what a filled cell means, preserve token ordering and align group brackets to actual cell boundaries. Do not interpret a structural mask as measured attention weights. Keep an inset subordinate to the architecture while making its labels readable.

### Qualitative grids

Choose one stable row meaning and one stable column meaning: examples × methods, or input/masked/output/target. Match crop, camera, lighting, scale, prompt, and budget where appropriate. Use closeups only when the same region is shown for all compared methods. Give failures a recognizable status instead of silently omitting them.

**Modern reference route:** V-JEPA 2.1 Fig. 1; Cosmos 3 Fig. 1. For text/tool evidence storyboards, see Harness² Fig. 9 and OpenAI CoT-Control Fig. 2. **Foundational route:** MAE Figs. 2–3; Hunyuan3D Fig. 7.

**Guardrail:** disclose sample selection, best-of-n, compositing, and any enhanced display. Qualitative examples illustrate behavior; they do not establish prevalence without a sampling design.

## 7. Data flows and hardware schedules

### Data curation and retention

Use a simple staged flow if only the sequence is known. Use a Sankey only when widths encode verified, commensurate counts or proportions. Show discarded branches, stage denominators, and any regrouping that prevents conservation.

**Modern reference route:** Cosmos 3 Fig. 8 for a curriculum matrix plus process flow; Qwen3-VL-Embedding/Reranker Fig. 5 for typed data-to-model stages. **Foundational route:** HunyuanVideo Fig. 4 for retained/discarded counts. Match the chosen form to the evidence actually available.

**Guardrail:** do not make a narrower shape imply measured filtering. Tokens, documents, images, and hours are not interchangeable flow units.

### Resource timelines

Use one row per device, worker, stream, or resource and a shared time axis. Distinguish computation, communication, and idle periods. Align alternatives to the same start and duration scale; preserve identical workload assumptions or state the change. Expand only the interval needed to explain a scheduling improvement.

**Modern reference route:** DeepSeek-V4 Fig. 5 for aligned communication/computation. **Foundational route:** Megatron-LM 2021 Figs. 3–4.

**Guardrail:** label whether times are measured or idealized and disclose overlap assumptions. Keep microbatch numbering readable; unnecessary internal labels can obscure the schedule.

## 8. Select a visual explanation without overclaiming

Sketch two candidates when the encoding is uncertain. Compare them by the reader action they support: locating a mechanism, judging a difference, identifying a tail, or trading quality against cost. Select the composition with clearer hierarchy, stronger task-specific detail and fewer ambiguous routes while preserving all essential distinctions. A richer composition is appropriate when its extra detail explains the research.

Use the strongest visual channel for the main scientific distinction. If every panel needs a paragraph of legend explanation, reduce the number of encodings or split the figure. Preserve honest complexity when the scientific result is conditional, heterogeneous, or uncertain.
