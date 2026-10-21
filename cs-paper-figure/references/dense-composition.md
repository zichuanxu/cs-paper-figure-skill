# Dense figures that explain a mechanism

A sophisticated scientific figure carries several **connected levels of explanation**. Extra boxes, pastel cards, icons, or panels alone do not supply those levels. Start with the reader's questions and the actual content; density follows from the answers.

Read this reference when the user asks for a rich method figure, a full-page overview, complex architecture, a mechanism inset, or a figure comparable to the supplied IdeaScientist / SkillOpt examples. For a substantial scientific overview, the small demonstrations in `render_examples.py` and `render_reference_recipe.py` are component examples, not the finished complexity target.

## Contents

- [Information hierarchy](#1-build-an-information-hierarchy-before-a-layout)
- [Connected compositions](#2-choose-a-connected-composition)
- [Concrete detail](#3-make-detail-concrete)
- [Typography and color](#4-typography-and-color-at-physical-size)
- [Routing](#5-route-the-full-explanation)
- [Complexity and scientific review](#6-complexity-and-scientific-review)
- [Handoff](#7-what-a-strong-handoff-contains)

## 1. Build an information hierarchy before a layout

Specify the following levels where the scientific material supports them:

| Level | Reader's question | Concrete content |
| --- | --- | --- |
| System | What enters, what happens, and what leaves? | Named artifacts, operations, persistent state, scope, time, dependencies |
| Mechanism | What operation is actually new? | Attention mask, address/key mapping, patch conflict, tensor transformation, objective, scheduler, or protocol |
| Instance | What does the operation do to one real object? | Before/after record, token sequence, source-grounded trace, selected frame, executed edit, or proof step |
| Evidence | Why believe the claim, and where does it fail? | Controlled results, paired effects, uncertainty, ablations, boundary conditions, or a deterministic correctness fixture |

An overview needs enough of these levels to explain its contribution. It need not include all four in one image. Place a longer evidence analysis in a companion figure when integrating it would make either argument illegible. Do not invent results to fill an evidence panel. A deterministic fixture is not an empirical benchmark.

Write a **panel contract**: one question, one conclusion, required inputs, and the link to adjacent panels. If a panel can be removed without changing what the reader learns, remove it or replace it with missing mechanism detail. A detail inset must share identifiers with its parent; a worked case must instantiate the displayed algorithm.

Identify the **operation carrying the claim**. Record its input artifact, governing rule, changed output and observable consequence. A worked example of a convenient neighboring stage does not explain a highlighted novelty that remains a named box. For example, a concrete fast memory edit does not instantiate an epoch context update; that requires matched replay outcomes, a changed context field and a subsequent proposal that uses it. Narrow the title or explicitly mark a conceptual boundary if the actual transformation is unavailable.

## 2. Choose a connected composition

### A. System → transaction → replay

Use for agents, memories, skill evolution, verification, or compiler transformations. Allocate area according to the unresolved reader question. A wide overview can occupy half the height when the interaction topology is the contribution; when the contribution is a local update, make the overview a narrow locator and give the transaction/replay most of the area. Do not retain a large general pipeline merely because a template already has one. Put the expanded operation near its matching identifier. Align before/after objects by field, not by decorative card height.

Useful source anchors: IdeaScientist Figure 1, SkillOpt Figure 2, UFO2 validated-execution figures, R&D-Agent / R&D-Agent-Quant research and development interiors. The example `render_dense_method.py` uses a new illustrative memory-update fixture; it does not reproduce those systems.

### B. Stable tensor slots → changing mask → observed behavior

Use for attention, patching, multimodal tokenization, memory addressing, or conditional world models. Keep token/latent positions registered across conditions. Show the exact mask or index relation; color alone is insufficient. Repeat a small source sequence beside the matrix and decoded result. Distinguish masked, permitted, selected, and cached cells with shapes or marks in addition to color. Use a shared scale if numeric values are compared.

Useful anchors: Fast BLT, Native Sparse Attention, Cosmos Policy, Qwen3-ASR, MIRAS. A matrix is meaningful only if rows, columns, units, and the selection rule are explicit.

### C. Stage overview → local architecture → matched outputs

Use for multimodal generation, robotics, and video. Reserve the largest area for the novel local operation. A thin overview establishes stage order; filmstrips or aligned output rows show actual consequences. Preserve scene identity, camera/view, timestep, crop, and prompt across compared methods. Real outputs must come from supplied or authorized evidence, not generated look-alikes.

Useful anchors: DreamDojo, Cosmos-Transfer1, HunyuanCustom, HunyuanVideo-Avatar, Wan-Animate. A repeated image is an actual datum or a clearly labeled illustrative object, never filler.

### D. Primary effect → heterogeneity → resource cost → failure mode

Use for a substantial experimental figure. Give the main estimand the strongest position and most area. Show independent-unit observations or paired differences when they explain variance. Use a heatmap for condition-specific effects, a resource plot for the cost of obtaining them, and a compact diagnostic for the mechanism. Keep method identity stable across panels, distinguish ablations from separate methods, and name every aggregation. Do not assume a multi-panel figure becomes strong by adding more chart types.

Useful anchors: IdeaScientist Figure 2, SkillOpt Figure 3, PaperBench evaluation decompositions, reward-seeking interventions, and the prior corpus's controlled efficiency plots.

### E. Matched replay → changed context → next decision

Use when adaptation, reflection or an outer loop is the contribution. Make the paired artifact table the dominant region: identical case IDs, old/new outputs, exact changed tokens, and derived improved/regressed/unchanged groups. Beside it, show a readable context diff with evidence IDs next to each changed field. Then show the same next request under the two context states, so the effect on a proposal is inspectable.

Distinguish a proposed change from a validated or committed change. An updater that is a deterministic rule or template must be named as such. Keep training replay separate from validation and test claims. A provenance hash or a PASS badge can support verification, but it cannot substitute for the changed artifact or explain why a competing response fails.

Useful anchors: SkillOpt Figure 2's old/new replay and outcome grouping, and IdeaScientist Figure 1's structured role artifacts and worked case. A compact companion often explains this operation better than squeezing it into a thin footer band under a large fast-loop overview.

## 3. Make detail concrete

Replace a generic noun with a small structured object when its contents matter:

- `Memory` → version, key, value, source, and update scope.
- `Optimizer` → proposed operation, target field, precondition, budget, and rejection outcome.
- `Multimodal input` → actual interleaved modality tokens with segment boundaries.
- `Retrieval` → query-to-key correspondence, selected records, and provenance path.
- `Evaluation` → scoring unit, matched conditions, decision rule, and sealed test boundary.
- `Feedback` → a named artifact whose destination is a real mutable state or operation.
- `Parallel processing` → two or three representative lanes plus an explicit repetition count when relevant; do not draw every worker.

Concrete contents are abbreviated for legibility, not replaced by meaningless gray lines. Use ellipses only when the omitted content is genuinely repetitive and the truncation is stated. If a table matters scientifically, include actual column labels and a representative row. If an icon helps recognition, pair it with a readable label and keep the icon simpler than the mechanism it introduces.

## 4. Typography and color at physical size

For a dense full-width manuscript figure, start at **178 mm** width with a content-driven height. Use 7.2–8 pt details, 8–9 pt module labels, 9–10 pt panel titles, and 10–11 pt section emphasis. These are production recommendations, not measurements of the papers. Keep the minimum size fixed while composing; increase height, tighten wording, group repetitions, or move material to a companion figure before shrinking.

Budget the caption before finalizing height. The artwork, caption, and gap must fit the actual text block together. A 228 mm figure plus a 200-word caption can exceed a full manuscript page even though the figure alone opens correctly. Prefer a roughly 180–210 mm plate where the venue permits, shorten the caption while preserving scientific essentials, or split the figure. Recompose geometry while retaining type sizes; do not fix page fit by scaling the entire export until labels become microtype.

Use one family with verified regular/bold font programs and a compatible monospace companion for actual code or identifiers. Serif body typography can work well when coordinated with the manuscript; do not imitate a source's font without inspecting its embedding or declaration. Avoid mixing serif microtext, large sans titles, and a third display face without a role for each.

Assign color to **one principal scientific dimension**. For an update protocol, blue may mean runtime/state, violet proposals, amber validation, teal consolidation, and red rejection. Keep fields and object IDs consistent across overview, detail, and replay. Use a pale background for scope, a stronger border or small tab for object identity, and dark ink for text. The strongest fill should identify the key operation or decision, not every module. Avoid large dark filled cards that force all details into tiny white text.

Quantitative scale colors have a different role from categorical method colors. Never reuse the same legend item to mean both an actor and a magnitude. Use a shared semantic key and local keys for mask states or edge types.

## 5. Route the full explanation

Declare operations and state separately. A feedback arrow must end at what it updates; an arrow near a module is not sufficient. Draw training, validation, and final test access as distinct operations or boundaries. State that is read is not automatically updated.

Reserve corridors before placing child cards: a forward lane, a return lane, and any slower update lane. Use explicit junction dots for fan-in/fan-out. A shared bus is a set of declared junction segments, not several overlapping independent arrows. Place edge labels in reserved gaps, not on top of arrowheads.

Use a cross-panel reference instead of an unreadable long connector when the panels are different explanatory views. Give the same artifact a stable identifier and explicitly label the reference, for example `T: trace ledger from panel a`. Record that correspondence in the scene specification. Do not disguise a missing data dependency with a decorative dashed line.

Distinguish edge types locally: solid execution, dashed rejection, dash-dot epoch update, dotted correspondence, for example. Scope boundaries are not execution edges. Mark intentional crossings with a bridge/gap and a documented non-junction; prefer a layout that avoids them.

## 6. Complexity and scientific review

Record the number of panels, semantic objects, routes, concrete instances, and information levels as descriptive statistics only. They are not a quality score. Thirty meaningless nodes are worse than six sufficient ones.

Review in this order:

1. **Scientific trace:** follow one item from input to output. Replay one accepted and one rejected/alternative path when those paths exist. Check the detail panel and worked instance against the same specification.
2. **State trace:** name every mutable object, its writer, its readers, and the time at which it changes. Frozen model weights and final held-out tests must remain consistent with the contract.
3. **Visual trace:** inspect actual PDF routes, attached arrowheads, branch dots, labels, and edge meanings. Automated centerline checks do not certify painted arrowhead clearances.
4. **Reading order:** at a glance, find the system, the new mechanism, and the concrete case. At close inspection, recover the identifiers, values, and conditions.
5. **Final-size comparison:** render candidate and reference at the same physical width. Compare information levels, readable type, local contrast, ambiguous routes, and mechanism specificity. Do not judge by zoomed screenshots alone.
6. **Export:** inspect PDF and SVG, verify real font embedding and editable text, run containment/overlap checks, and inspect grayscale. Keep source, fixture/data, caption, alt text, and provenance.

Use source weaknesses as evidence for improvement. The inspected IdeaScientist overview contains much body text around 5.6 pt at its source placement; SkillOpt's pipeline contains labels from roughly 2.5 to 7.4 pt. Their structural richness is valuable, but those sizes are not a production target. Palette counts and raw path counts also do not measure occupied area or semantic complexity.

## 7. What a strong handoff contains

Deliver the full argument, not just a preview. Include the final PDF/SVG/PNG, runnable source, actual inputs, a caption that states evidence status and qualifications, and a brief design note linking reference observations to original decisions. Explain what is more sophisticated than the prior version: the additional mechanism, concrete instance, preserved dependencies, or experimental analysis. Do not claim to outperform an entire corpus based on an aesthetic preference or an automated checklist.
