# Scientific contract

## Contents

1. Establish what is being claimed
2. Identify the data-generating unit
3. Represent uncertainty honestly
4. Preserve comparison validity
5. Audit transformations and axes
6. Handle missing inputs and schematics
7. Write the caption and provenance

## 1. Establish what is being claimed

State the estimand or mechanism before drawing. Replace an unrestricted claim such as "memory improves agents" with a testable description such as "under the supplied task set and token budget, the measured success rate differs between these memory policies." Let the scope follow the study design.

Classify every visual element:

| Status | Meaning | Required treatment |
| --- | --- | --- |
| Measured | Produced by the current experiments | Retain raw observations, processing code, and conditions |
| Reported | Transcribed or extracted from a cited source | Record exact table/figure/version and transformations |
| Illustrative | Constructed to explain a layout or concept | Mark inside figure and caption; avoid empirical claims |
| Schematic | Represents topology, operations, or conceptual relations | Define edges; mark quantities as not to scale where relevant |
| Fitted/derived | Computed from observations under a model or formula | Show assumptions and distinguish from direct observations |

A single figure can contain several statuses if the distinction is visible. A conceptual arrow is not evidence of causal identification. An attention map is not automatically a causal explanation. A diagram of a future system must not be presented as the implemented system.

## 2. Identify the data-generating unit

Determine what could have been independently sampled or repeated: training run, task, user, document, query, environment, or device trial. The number of tokens, checkpoints, retrieved chunks, or repeated judgments is not automatically the independent sample size.

- Keep runs/checkpoints/items as separate columns until the aggregation is specified.
- Preserve genuine pairing when the same items are evaluated under both methods.
- Do not infer pairing solely from equal row counts or matching arbitrary seed numbers.
- Preserve nesting or clustering, such as responses within a user or episodes within a trained policy.
- Decide whether the task suite is a fixed target or a sample from a task population before deciding which levels to resample.
- Preserve actual timestamps or compute coordinates. Connecting equally spaced marks must not imply equally spaced observations.

For a benchmark table, specify macro versus micro averaging, task weights, score directions, and missing task handling. Do not average unrelated metrics merely because they are all expressed as percentages. Record the denominator for pass@k, win rate, success rate, and failure proportions.

## 3. Represent uncertainty honestly

Distinguish:

| Quantity | Describes | Label example |
| --- | --- | --- |
| Standard deviation | Spread of observations at the stated unit | Mean ± SD across five independent runs |
| Standard error | Estimated precision of an estimator under assumptions | Mean ± SE; state independent unit |
| Confidence interval | A procedure's coverage for an estimand | 95% paired bootstrap CI over queries |
| Quantile range | Distributional spread | Median and 10th–90th percentiles across tasks |
| Prediction interval | Uncertainty for a future observation | 90% predictive interval |
| Min–max | Extremes of observed samples | Range across four runs |

Do not relabel one as another. A pale band in a source figure does not establish what it represents. No interval can be reconstructed from a mean alone. With very few independent samples, expose the individual observations and qualify the estimate; a large number of bootstrap draws does not create new experimental information.

For a paired contrast, compute the contrast at the paired unit before summarizing. If item `i` has outcomes `a_i` and `b_i`, estimate the desired statistic from `d_i = a_i - b_i`. Resample paired units together when the design supports it. For nested data, use a design-appropriate hierarchical or cluster procedure rather than pretending all rows are independent.

Show observed point estimates together with intervals. Some valid interval constructions need not contain the displayed estimate; draw endpoints independently and check the analysis rather than silently forcing containment. Never clip an invalid interval to a metric's legal range to make it appear plausible; use an appropriate analysis or disclose the limitation.

For trajectories, distinguish pointwise bands from simultaneous bands. Overlap or non-overlap of separate 95% CIs is not a general significance test for a contrast. Avoid stars unless the actual test, comparison family, and correction are known. Report practical effect sizes alongside uncertainty.

The primary study [Deep Reinforcement Learning at the Edge of the Statistical Precipice](https://arxiv.org/abs/2108.13264v4) motivates uncertainty-aware benchmark visualization and sensitivity to aggregation. Its particular RL estimands and sampling procedures must be matched to the present design, not applied automatically.

## 4. Preserve comparison validity

For LLM and agent comparisons, preserve model version, prompting, tool access, harness, retrieval corpus, context window, sampling configuration, evaluator, token/call budget, stopping policy, and failure handling when relevant. Mark non-matched conditions instead of implying a controlled ablation.

For systems efficiency, identify hardware, device count, batch/concurrency, precision, context and output lengths, warm-up, caching, latency statistic, software stack, and measurement scope. Distinguish time to first token, inter-token latency, total response latency, and throughput. FLOPs, wall-clock time, tokens, and monetary cost are different resources.

For an observed Pareto set, declare whether each axis is minimized or maximized. Point A dominates B only if A is no worse on every objective and strictly better on at least one. Exact ties do not dominate one another. Retain dominated points for context; a line through efficient observations does not prove that interpolated configurations are attainable. Uncertainty can make apparent dominance inconclusive.

For ablations, preserve equal budgets and the actual intervention. A removal that also changes token use, training compute, or capacity may test multiple factors. Separate the descriptive result from a causal interpretation.

## 5. Audit transformations and axes

- **Bars:** use a zero baseline for ordinary magnitude comparisons. If a close comparison needs an expanded range, prefer dots, intervals, or a clearly labeled delta panel.
- **Line/scatter axes:** a nonzero origin can be appropriate; show honest ticks and keep comparison ranges consistent where needed.
- **Differences:** distinguish percentage points from relative percent change. Name the reference and direction.
- **Ratios:** show the neutral value 1, identify the denominator, and explain a geometric mean when used. A ratio is undefined at a zero denominator.
- **Log axes:** require positive coordinates and positive interval endpoints on the logged axis. Handle zeros and negatives explicitly; do not silently drop them or add an arbitrary epsilon. Label a deliberate symlog transform and threshold.
- **Normalization:** preserve the formula and reference values. Do not hide raw-scale consequences when they matter to the claim.
- **Smoothing:** preserve raw points or a raw trace, state window/kernel and boundary behavior, and do not select smoothing to erase failures.
- **Fits:** distinguish measured points, fitted range, and extrapolation. Report the fit's input range and assumptions. Do not invent an optimum beyond observed support.
- **Heatmaps:** use a shared normalization for panels intended for comparison; display missing or not-applicable cells distinctly from zero. Do not interpolate discrete benchmark cells into a continuous surface without justification.
- **Distributions:** expose sample counts. Use the same meaningful bins or bandwidth choices when comparing groups; do not use a smooth density to imply large-sample certainty.

Preserve failed runs and timeouts according to the declared protocol. If excluded, show their count and rule. A missing result is not a zero score unless the metric explicitly defines that treatment.

## 6. Handle missing inputs and schematics

When data is missing, complete the layout, labels, semantic key, and expected schema. Use pending-data placeholders or explicitly labeled synthetic values only if a demonstration is useful. Never finish an empirical figure by inventing numerical results, confidence intervals, sample sizes, baselines, or references.

For diagrams, verify node types, edge direction, training/inference phases, update scope, and state persistence. Distinguish data flow, control/selection, gradients, and state writes with a small explained vocabulary. Draw a feedback edge only when that operation exists. If arrow width, box size, or glyph count looks quantitative but is schematic, make that status clear.

For qualitative grids, use real supplied/generated experimental samples, shared prompts or inputs, equal crops and display treatment, and an explicit selection policy. Include representative failures when relevant. Disclose compositing, enhancement, best-of-n selection, and different inference budgets. Do not silently regenerate a failed sample for the figure.

For simulated scenes and planning diagrams, preserve one explicit state/geometry fixture. Derive observation depictions, paths, predicted states, constraint flags, costs, selection and the executed transition from it. Use the same viewport, aspect ratio and object identities across compared frames. Label rendered simulator observations, hypothetical rollouts and actually executed steps separately. A predicted path beyond a collision may be a deliberately invalid counterfactual; state that policy and distinguish its continuation from physical execution. Do not imply that a handcrafted scene encoder is a learned perception model, or that an illustrative cost is an empirical reward.

Define the collision geometry, agent footprint, tangent-contact policy and swept segment test. Clear sampled endpoints do not imply a collision-free path between them. A finite collision penalty does not guarantee feasibility under arbitrary inputs; distinguish a penalized minimum, an explicit feasibility filter, and a first-step execution guard. If the fixture executes one action, do not claim that an entire closed-loop rollout was executed. Name a sum of squared controls as quadratic control effort unless its physical energy interpretation has been established.

Separate scientific intersections from layout defects: a candidate trajectory crossing an obstacle can be the displayed failure, while a control-flow connector penetrating an unrelated module is a drawing error. Record the intended data intersection and verify it numerically rather than excluding every intersecting line from review.

## 7. Write the caption and provenance

Use this order, omitting inapplicable parts:

1. The limited scientific takeaway.
2. What each panel shows and how to read the encodings.
3. Dataset, conditions, metric, and sample unit/count.
4. Aggregation and interval method; distinguish pointwise bands.
5. Qualifications, excluded/missing outcomes, and schematic/illustrative status.

For a diagram, explain node/edge semantics and the boundary of the schematic. Use panel letters consistently with the manuscript. A caption should explain enough to interpret the figure without searching the main text for units or uncertainty meaning.

Preserve source paths or stable dataset IDs, hashes where practical, table/row mappings for transcriptions, processing code, and the final plot specification. Keep provenance precise without exposing private paths or sensitive inputs in a public caption.
