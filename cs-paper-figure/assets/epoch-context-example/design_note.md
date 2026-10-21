# Design and scientific note

## Claim and scope

The figure makes a single state transition inspectable: matched training replay changes the context constraints used by the next proposal. Its claim is bounded to an executed, deterministic fixture. The formatter is fixed, reflection uses disclosed rules, and no learned model, validation set, test set, or real-agent evaluation is involved. The next proposal is an artifact; it is not applied to memory and has no acceptance verdict.

This is a separate fixture from the earlier fast-loop memory figure. The state identifiers M0/M1 and C0/C1 are local to this example. A reader should not interpret the two figures as one continuous experimental run.

## Actual intermediate objects

The inputs contain two memory policies and the same four training cases. M0 attaches units to headers and omits a scalar source date. M1 applies inline units to scalar and CSV outputs and includes the scalar source date. The score and range renderers are held fixed. The artwork labels this exact scalar/CSV scope.

The code first emits actual output strings, then evaluates explicit requirements. It does not assign verdicts from desired group labels. T08's scalar response gains its unit and date. T11's CSV cell changes from the number `12` to the string `12 ms`, which is no longer numeric. T03's unitless score remains correct. T14 remains wrong because the deliberately limited range formatter emits only its lower endpoint. That limitation is a stipulated part of the fixture, not a discovered behavior of a model.

Outcome groups compare the task pass/fail verdict under the two memory states. A task passes only when all of its required checks pass. Improved means fail-to-pass; regressed means pass-to-fail; unchanged includes both pass-to-pass and fail-to-fail. The count labels and row classifications are derived from those verdicts. There are no confidence intervals or population estimates because this is a fixed, selected case illustration.

The reflection code applies four fixed rules. Newly satisfied scalar requirements from an improved case enter `retain`. A numeric CSV regression removes CSV from `allow_inline` and adds `csv.numeric` to `protect`. Requirements that fail under both states enter `open`. A stable pass adds no new rule. Every change carries its source case ID. The context diff in panel b is therefore an actual before/after object with a derivation trace in `analysis.json`.

Finally, one preserved request asks for inline units in scalar and CSV formats. The proposal generator intersects that request with `allow_inline` and attaches retained requirements, protected contracts, and open issues. Under C0 it proposes both formats; under C1 it proposes scalar scope and carries the CSV guard, scalar unit/date requirements, and unresolved range issue. The display aliases `INLINE`, `KEEP`, `GUARD`, and `DEFER` are defined in `figure_brief.json`; the complete structured patch remains in `analysis.json`.

## Composition

The canvas is 178 × 158 mm. The main object is the replay table: matched case IDs, required contracts, concrete output strings, task verdicts, and derived groups are registered in one row. This makes the failure mechanism visible without routing a long sequence of generic processing boxes.

The lower row is asymmetric. The larger left document contains the actual context diff; its source IDs repeat those in the replay rows. The smaller right region compares two proposal documents for the same request. This gives the context change a downstream consequence rather than ending at a box labeled “reflection.” A short rule summary above the diff states the fixed policy: keep gains, guard regressions, carry failures.

Two compositions were considered. A left-to-right replay-to-reflection-to-proposal chain would have forced narrow replay columns and encouraged abstract reflection nodes. The chosen full-width replay table above the diff and decision example keeps all actual artifacts readable. It also avoids using one large overview to dominate the mechanism.

Color follows replay outcome: green for improvement and retained gains, rust for regression and its protective constraint, slate for unchanged verdicts and the unresolved issue. Teal outlines identify updated context/proposal documents. Textual verdicts, source IDs, and pass/fail badges preserve meaning in grayscale. The document folds distinguish persistent artifacts; horizontal rules register comparable fields. There are no process arrows to interpret as execution, validation, or causal identification.

Typography uses actual DejaVu Sans regular/bold and DejaVu Sans Mono regular/bold TrueType programs. Main title text is 10.5 pt, panel titles 8.8–9 pt, and every detail is at least 7.2 pt. Monospaced output and field text distinguish exact artifacts from surrounding explanation. The SVG keeps editable text rather than outlining labels.

## Design evidence

The actual supplied crops of IdeaScientist v1 Figure 1 (PDF page 2) and SkillOpt v2 Figure 2 (PDF page 4) were inspected. IdeaScientist informed the principle of connecting an overview to structured artifacts and a worked case. SkillOpt informed the distinct epoch timescale, replaying the same cases under two states, and grouping changes before updating optimizer context. The new composition is original: it centers an executed replay table, a field-level context diff, and a paired next-proposal example. It does not reproduce their artwork, result values, system implementation, or microscopic labels.

Source versions: [IdeaScientist v1, Figure 1](https://arxiv.org/html/2610.04074v1) and [SkillOpt v2, Figure 2](https://arxiv.org/pdf/2605.23904v2). They supply visual design evidence, not scientific evidence for the constructed fixture. Source artwork is not included in this bundle.

## Verification and limits

The executable fixture checks all outputs against preserved expected strings, derives every verdict from explicit output requirements, verifies the resulting context against a separately preserved expected context, and confirms that the same request produces the displayed two scopes. These checks address the actual transformation, not an empirical learning claim.

The figure's text bounds and pairwise overlaps are measured before export. The final PDF is checked for physical dimensions, minimum text size, visible text staying inside the page, embedded compatible font programs, and raster objects. The editable SVG is inspected for text nodes. Color and grayscale PDF renders are reviewed at enlarged and nominal full-width raster scales. These production checks support faithful delivery; they do not substitute for judging whether the mechanism is useful for a real method.

The examples are deliberately selected to exercise the reflection branches. They are not representative samples, independent experimental replications, or evidence that this context updater works for learned agents. The range bug is explicitly modeled. Retained requirements follow a fixed rule on observed pass/fail changes; this is not causal attribution of the separate contributions of unit and date edits. Actual training would require a specified learned updater, real traces, and an appropriate evaluation design outside this figure.

The compact plate leaves room for its short caption in a full-width manuscript setting, but final placement should use the target manuscript's actual caption face, leading, float rules, and usable text block. A calculated caption budget is preserved in `qa/caption_fit.json`.
