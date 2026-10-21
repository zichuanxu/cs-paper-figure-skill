# Advanced examples: contracts, structure and adaptation

These five original figures apply the corpus-derived workflow to different scientific tasks. They are runnable design examples, not replicas of a source paper or evidence that a proposed research method works. Python 3.10+, Matplotlib, NumPy, Pillow and PyMuPDF are required for the complete export and inspection workflow. Use an output directory outside the installed skill.

## Contents

- [Method and executable transaction](#1-method-overview-with-an-executable-transaction)
- [Representation and exact attention](#2-representation-exact-operator-worked-values-and-availability)
- [Effects and qualified diagnosis](#3-effects-heterogeneity-resource-cost-and-a-qualified-diagnosis)
- [Scene-grounded planning](#4-matched-scenes-candidate-paths-and-a-swept-collision-check)
- [Epoch replay and context change](#5-matched-replay-context-diff-and-the-next-proposal)
- [Delivery and review](#delivery-and-review)

## 1. Method overview with an executable transaction

```bash
python <skill-root>/scripts/render_dense_method.py --out figures/method
```

**Physical specification:** 178 × 200 mm; 7.2 pt minimum text; real regular, bold and monospaced TrueType programs. Runtime uses blue, proposals violet, validation ochre, the slow update teal, acceptance green and rejection rust. Pale scope fills and darker related labels form a consistent hierarchy. Dashed rejection and dash-dot epoch routes have explicit local definitions.

**Information structure:** panel a shows a frozen agent, versioned memory, parallel edit proposals, a budget/conflict merge, validation and atomic commit, rejection feedback, and a separate epoch context update. Panel b instantiates the merge with P1/P2/P3, a 3 × 3 conflict matrix, priority/evidence fields, and before/after records. Panel c replays a distinct case V01 and reports actual assertions, a version/hash receipt and a rejected alternative.

The fixture in `assets/dense-method-fixture.json` supplies the content. T08/T11 are proposal evidence. V01 is a separate deterministic validation case; its value is 7.5 ms with date 2026-10-18. The executor, not a hard-coded label, generates the responses and assertion outcomes. P1 and P2 conflict on one key; the two-edit budget selects P1+P3. The baseline passes 1/3 assertions and the candidate 3/3; P2 alone ties the baseline. An exact rejected proposal ID is excluded from future selection. The figure does not run an entire training process or establish generalization.

The current layout contains 19 semantic nodes, six junctions and 28 declared routes. Those counts help scope the geometry audit; they are not a quality score. The helper checks actual rendered text rectangles and declared ports/paths, then the exported PDF must still be inspected. The epoch update in this overview remains conceptual. Example 5 instantiates that operation with a separate replay/context fixture; its local state identifiers do not imply one continuous run with this example.

**Adaptation:** replace the fixture and revise the code's scientific assertions, labels, topology and caption together. The renderer deliberately rejects a changed selection/outcome that its fixed drawing would misrepresent. Its compaction helper moves geometry while preserving point-sized type, and reruns text/route checks; compaction is not a substitute for redesign if those checks fail.

**Design evidence:** IdeaScientist Figure 1 supplies the principle of a system overview tied to roles and an instance; SkillOpt Figure 2 supplies parallel edits, validation, rejection and distinct update timescales. The example improves explicit state-writer/validation boundaries and minimum type size, but does not claim to explain an equally broad real system.

## 2. Representation, exact operator, worked values and availability

```bash
python <skill-root>/scripts/examples/causal_attention/render_figure.py --out figures/attention
```

**Physical specification:** 178 × 210 mm; 7.2 pt minimum text. Prefix slots are blue squares, completed summaries violet triangles and local keys teal circles in the value view. The same color/identifier mapping appears in the bank, matrix and ledger. Hatching explicitly denotes unavailable entries; scientific meaning does not depend on hue alone.

**Information structure:** a canonical key/value bank and read operator; an indexed 4 × 8 additive mask; a six-row logit/weight/value/contribution ledger with a two-dimensional value view; and a timeline showing when S3 can enter the bank. The matrix replaces a web of repetitive query-to-key arrows. Identical identifiers and column order register all four views.

The preserved input JSON supplies two prefix slots, summaries for completed t1–t4/t5–t8 chunks, and local t9–t12 slots. Each query can read the prefix, both completed summaries and local tokens no later than itself. Permitted-key counts are 5, 6, 7 and 8. S3 is absent for all four queries and can become eligible only after the chunk is sealed and finalized. Canonical future slots in the overview do not imply that their contents are already populated.

For q10, supplied scaled logits `[1.2, 0.6, 0.4, 0.8, 1.1, 0.9]` normalize over six permitted keys. The weighted two-dimensional result is approximately `(0.6000496006970207, 0.7301836296320875)`. The script preserves 60-digit decimal approximations, checks a stable float64 calculation, and derives all displayed numbers from the same inputs. This is a numerical illustration, not a learned model or empirical attention benchmark. The summarizer and later eviction policy are unspecified.

**Adaptation:** the fixed diagram assumes eight columns, four queries and six permitted keys in the worked case. Change the layout and dimension/availability assertions when adapting those counts. Keep the exact computation separate from rounded display values. Do not invent Q/K matrices merely to decorate the figure when only scaled logits are supplied.

**Design evidence:** Fast Byte Latent Transformer Figure 5 and Wan-Animate-2 Figure 1 connect an architecture to explicit representations and indexed operators. Here that principle is extended with a computed instance and a precise streaming boundary. Readable typography consumes more vertical space than the source's compact microtype; check caption fit in the actual template or split the figure.

## 3. Effects, heterogeneity, resource cost and a qualified diagnosis

```bash
python <skill-root>/scripts/render_dense_experiment.py --out figures/study
```

The wrapper writes preserved configuration and portable source into the requested output directory, generates observations, analyzes them and renders the figure. Mutable data and exports stay outside the skill. Source snapshots live in `assets/experimental-example/`.

**Physical specification:** 178 × 181 mm; 7.25 pt minimum text. A shared policy key combines gray/amber/teal/violet with squares/triangles/circles/diamonds and line patterns. A separate zero-centered signed color scale is reserved for the quantitative matrix; numeric cell labels preserve sign and magnitude in grayscale. A light row band and stronger numerical label emphasize the primary contrast.

**Information structure:** a paired contrast plot showing all independent seed effects and mean intervals; a task × memory-budget effect matrix; observed quality/cost configurations with intervals on both axes; and two rejection-history diagnostics accompanied by the capacity tradeoff. Every panel answers a different question about the same constructed study.

The figure says **SYNTHETIC DATA** inside the artwork. A transparent simulator creates four policies × four task families × four budgets × 24 independent matched seed blocks × 96 sequential episodes. Its 147,456 outcome rows do not represent that many independent replications. The 9,216 shared scenario rows preserve actual pairing across conditions. The estimand is the mean seed-specific success difference, equally weighted over the fixed task/budget suite. Pointwise 95% percentile intervals resample all matched conditions within each of 24 intact seed blocks; sequential episodes are never bootstrapped as independent observations.

The example deliberately includes a nontrivial qualification. Verification versus unfiltered updates yields a synthetic +6.57 pp contrast, while full verification versus verification without history is near zero (+0.02 pp, interval spanning zero). History reduces constructed corrupted reads and repeated invalid writes but consumes 25% of total memory capacity. It is a capacity-allocation comparison, not an isolated, cost-free history intervention or a causal mediation result. The resource axis uses simulated total model tokens, not money or measured latency.

**Adaptation:** replace the simulator with real raw observations for a research result. Revisit pairing, sampling units, denominators, task weighting, interval scope and cost accounting; keeping these fixture choices mechanically can produce an invalid analysis. Generate all annotations and labels from the analysis result. Do not retune synthetic parameters merely to manufacture a desirable story and then describe it as a finding.

**Design evidence:** Monitoring Monitorability Figure 8 supports stable identities across budget conditions; Perception Encoder Figure 8 supports an aligned condition structure; IdeaScientist Figure 2 supports paired estimates near their marks. The original design combines them into one four-question evidence figure without copying their data or artwork.

## 4. Matched scenes, candidate paths and a swept collision check

```bash
python <skill-root>/scripts/render_worked_example.py scene-planning --out figures/scene
```

**Physical specification:** 178 × 203 mm; 7.2 pt minimum text. Warm neutral scene fields and gray obstacles remain visually subordinate to three candidate identities: rust D, violet U and teal L. The IDs repeat in trajectory headings, action tables and costs. A starred goal, numbered states, hatched barrier and explicit collision mark support interpretation without hue. Dashed paths are simulated candidates; the solid arrow is the executed first transition. Candidate viewports and physical scales match, and the overview/executed view retain the same coordinate domain and aspect ratio at their own sizes.

**Information structure:** panel a pairs a rendered scene with its exact state and task; panel b compares three complete action sequences, resulting paths and computed scores; panel c magnifies a collision between free sampled endpoints and states the objective; panel d shows the selected first action and the resulting observation. The actual geometric objects do explanatory work: the collision cannot be understood from a generic planner box alone.

The preserved fixture defines a dimensionless point agent, a rectangular barrier, a circular pier, a four-action horizon and additive dynamics. Each action norm is at most 3.5. A slab test for the rectangle and a closest-point test for the circle check the entire closed segment, including tangent contact. The direct candidate's segment `(3, 3) → (5, 3)` intersects the barrier for segment parameter `[0.20, 0.80]`, although both endpoints are free. Nominal trajectories continue beyond a collision for scoring; they are not displayed as executed motion.

The cost is terminal squared distance plus `0.1 × quadratic control effort + 100 × collision indicator`. All three terminal distances are zero. The computed D/U/L costs are 101.600, 2.636 and 2.142. The finite penalized minimum selects L in this fixture; its first action is `(1.5, −1.8)` and its next position is `(2.5, 1.2)`. The execution code also checks that first swept segment. A finite penalty is not a general feasibility guarantee; only one action is executed, and the next observation is available for replanning rather than evidence of a simulated second planning cycle.

**Adaptation:** revise obstacle/footprint geometry, candidate generation, dynamics, objective and selection together. A finite-radius robot needs a corresponding collision model; changing a point glyph into a robot icon does not supply that model. State whether controls measure velocity, displacement or a dimensionless increment. Do not call a sum of squared controls physical energy without a justified model. The supplied observations are deterministic scene drawings from exact state; the planner does not infer state from images or use learned perception. Keep scientific intersections, such as the failing trajectory through an obstacle, separate from connector-layout errors.

**Design evidence:** Cosmos Policy Figure 2 motivates stable representation slots; WorldPlay Figure 2 motivates matched scene views; GR00T N1 Figure 2 connects concrete modalities with downstream representations. This example transfers the correspondence principle to an original exact spatial fixture, without presenting its simple dynamics as a learned world model.

## 5. Matched replay, context diff and the next proposal

```bash
python <skill-root>/scripts/render_worked_example.py epoch-context --out figures/epoch
```

**Physical specification:** 178 × 158 mm; 7.2 pt minimum text. Green identifies improvement and retained gains, rust identifies a regression and its protective constraint, slate identifies unchanged cases, and teal outlines updated context/proposal documents. PASS/FAIL labels, case IDs, field names and before/after positions preserve meaning in grayscale. DejaVu Sans regular/bold provides hierarchy; DejaVu Sans Mono regular/bold distinguishes exact emitted strings and context fields. Pale row bands align comparable artifacts rather than enclosing every item in a process box.

**Information structure:** a dominant replay table shows the same four constructed training cases under two formatter policies, their actual outputs and derived outcome groups. A larger lower-left document shows the fields changed by fixed reflection rules, with source case IDs. A smaller lower-right pair shows the same next request under old and new context. The mechanism and its consequence occupy the figure; the general system overview is omitted because it would not explain the highlighted context update.

The scalar unit/date case improves; appending a unit to a numeric CSV cell causes a regression; a unitless score remains correct; a modeled range-endpoint failure remains unresolved. Outputs are generated first and checked against explicit task contracts, yielding 1 improved, 1 regressed and 2 unchanged cases. Unchanged includes both pass-to-pass and fail-to-fail. These are deliberately selected branches of a deterministic illustration, not representative evaluation statistics.

The fixed reflection rule removes CSV from `allow_inline`, adds scalar unit/date requirements to `retain`, adds `csv.numeric` to `protect`, and carries `range.end` in `open`. Each field cites its evidence case. Under C0 the next request proposes inline units in scalar and CSV formats; under C1 it proposes scalar scope with the retained requirements, CSV guard and unresolved issue. This is an actual computed proposal artifact. Neither proposal is committed or validated; no held-out or test case enters the update. The fixture is separate from Example 1, even where identifiers have the same spelling.

**Adaptation:** preserve matched input identity and inspect emitted artifacts before classifying outcomes. Supply the real updater if the scientific claim concerns learned reflection. Do not label fixed rules as learned reasoning, treat training replay as validation, or infer causal credit for individual edits from one bundled change. Show what the next decision actually reads from the changed context. The range failure is intentionally stipulated here and must not become an invented model finding in an adapted figure.

**Design evidence:** SkillOpt Figure 2 motivates matched old/new replay and an epoch context update; IdeaScientist Figure 1 motivates structured role artifacts and a connected worked case. The original composition expands the actual replay, context fields and subsequent proposal. It complements the earlier overview without claiming to reproduce either research system.

## Delivery and review

Each example provides vector PDF, editable-text SVG, PNG preview, preserved inputs, source, numerical/geometry/export checks and interpretation. Exact SVG appearance still requires the declared fonts. Short main captions are intended for manuscript placement; longer interpretation belongs in the companion note. Add artwork height, caption gap and actual typeset caption height before calling a placement ready.

The two `render_worked_example.py` modes copy only their preserved source/fixture bundles from `assets/scene-planning-example/` and `assets/epoch-context-example/` to the requested output, then run there. They do not alter installed skill assets. The outputs contain editable source snapshots and can be regenerated without the original skill directory. As with the other fixtures, changing the scientific contract may require changing the fixed layout and its assertions.

Review the actual PDF at its intended physical width, then inspect grayscale and its densest region. The supplied checks have explicit limits: rectangle-based route checks do not model every arrowhead, a PDF can embed a wrong font program, synthetic confidence intervals do not validate a real model, and a valid figure is not automatically aesthetically successful. Compare the candidate and relevant source at equal physical widths, state the tradeoffs, and avoid universal claims of superiority.

## MemT-1.0 redesigns

Reference-quality redesigns of arXiv 2610.26825v2 Figures 3 and 4, built with `paperkit` and the rules in [visual-craft.md](visual-craft.md). Values and equations are copied from the paper; nothing is invented.

| Script | Output | Size | Shows |
| --- | --- | --- | --- |
| `scripts/examples/memt/render_fig4.py` | `memt_fig4_architecture.{pdf,svg,png}` | 170 × 108 mm | (a) locator stack with zoom wedge, (b) block with parallel original/memory attention, memory pillar `M_t ∈ R^{H_kv×d_k×d_v}`, (c) read path every token (amber trapezoids = φ, readout `QM/√d_k`, RMSNorm ⊙ SoftCapSiLU), (d) write path once per turn as a token-level chain with one step drawn on the grid (forget → erase → outer-product write) and the typeset update rule, (e) turn timeline with `θ_t = {θ_b, φ, M_t}` |
| `scripts/examples/memt/render_fig3.py` | `memt_fig3_efficiency.{pdf,svg,png}` | 170 × 66 mm | (a) log-axis slope chart 128K → 256K with direct labels, `4.0×`/`59×` brackets and growth factors; (b) area-true waffle, one cell = 40 MiB, with `130×`/`4.3×` callout; derived ratios asserted in code |

Adaptation notes:
- Copy the *structure*, not the content: card helper with a tinted header band, a pillar for persistent state, one zoom-ray pair, colour-coded equation via `Canvas.rich`, chips naming each local colour.
- Coordinates are hand-placed in mm; after any text change re-render and look for clipped labels and text over wires.
- Matrix shading is an illustrative texture; say so in the caption. Replace it with `values=` when showing real data.
- Captions used for the redesigns: Fig. 4 — "Architecture of MemT-1.0. (a) Selected Transformer blocks gain a native memory block. (b) Memory attention runs in parallel with the unchanged backbone attention and is added to its output. The local memory state M_t (green) is read at every generated token (c) and written once at the end of each turn by a token-level stable GDN-2 scan over S_t = X_t‖Y_t (d). Amber projections and gates form the hyper memory φ, trained offline and fixed online. (e) Across interaction steps only M_t changes; it is reset to 0 for a new trajectory. Matrix shading is illustrative." Fig. 3 — "Inference efficiency and storage of MemT-1.0-Nano. (a) End-to-end latency (history preparation + 128-token response) on a log scale; brackets give speed-ups at 256K. (b) Persistent storage per trajectory, area to scale (one cell = 40 MiB). Full Context at 1M is reported as too large; Temp-LoRA and MemT storage is the same at 256K and 1M."

## Restyled classic examples

The five earlier examples, rebuilt with `paperkit` under the rules in [visual-craft.md](visual-craft.md). Each script reads the original fixture/analysis (bundled in `scripts/examples/restyled/data/`), recomputes or re-reads every value and asserts it, and moves status text (SCHEMATIC, fixture disclaimers, receipts) to the caption.

| Script | Size | Hero and main changes |
| --- | --- | --- |
| `render_method.py` | 178 × 134 mm | Paired-replay gate diamond; versioned memory band with real v12 → v13 records and REP/ADD chips; fan-out → arbiter merge bar → candidate doc; reject loop to a rejected-ID stack; outcome cells instead of a PASS/FAIL table |
| `render_attention.py` | 178 × 138 mm | 4 × 8 additive mask with the j ≤ i staircase; columns aligned across cache bank, mask and worked readout; shape glyphs Q ⊗ Kᵀ → A ⊗ V; weight bars and a value-space plot for o₁₀ |
| `render_experiment.py` | 178 × 124 mm | +6.6 pp paired effect in a hero band with all 24 seed blocks; sequential heatmap; cost curve with a +9.1 pp bracket; 2.2× / 4.2× error-ratio brackets; one SYNTHETIC DATA tag |
| `render_scene_planning.py` | 178 × 98 mm | One camera across five scene tiles; selected lower detour as hero; swept-collision panel on a segment-parameter axis; linear cost bars with an axis break for the 100C penalty |
| `render_epoch_context.py` | 178 × 106 mm | Case cards grouped into improved / regressed / unchanged; rule arrows into the C1 rows they cause; C0/C1 as documents with ADD/DEL chips; the next proposal aligned row by row |
