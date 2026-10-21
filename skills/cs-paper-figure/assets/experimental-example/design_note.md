# Design and scientific note

**Evidence status: SYNTHETIC DATA.** This is an original scientific-figure demonstration generated from an explicit online-memory simulator. The data, intervals and resource costs do not describe real agents. The synthetic disclosure is prominent inside the figure, repeated in its footer, and included in the caption and alt text.

## Argument and panel contract

The reader should be able to distinguish a primary paired effect, its heterogeneity, its resource cost, and a mechanism diagnostic that does not by itself establish a net benefit. The final composition has four panels because these are four different questions.

| Panel | Reader’s question | Inputs and transformation | Connection to the rest |
|---|---|---|---|
| a. Paired success changes | How large is the main policy contrast, and how variable is it across independent replications? | All 24 seed-specific macro differences, plus their mean and paired seed-bootstrap interval. Families and budgets receive equal weight within each seed. | Its highlighted verified-minus-unfiltered contrast is decomposed in b. Its near-zero full-versus-no-history contrast motivates d. |
| b. Where the effect varies | Which task/budget conditions drive the primary average? | The same paired success difference separately in each of 16 fixed conditions, with one common signed scale and directly labeled values. | This is a conditional decomposition of a, not a different performance metric. Open circles identify pointwise intervals spanning zero. |
| c. Quality has a resource cost | What simulated model-token cost accompanies each policy/budget configuration? | Per-seed family averages of success and total tokens, with pointwise intervals on both axes. | All four policy identities match the common legend. The full/no-history crossover shows why the aggregate ablation effect in a can be near zero. |
| d. Rejection-history diagnostic | What error events does history suppress, and what does the ablation actually change? | Corrupted reads and repeated invalid writes per 100 episodes, macro-averaged over the same fixed family/budget suite. | The memory-capacity reservation is stated beside the diagnostic; reduced error events are not presented as sufficient evidence of a success improvement. |

Two materially different compositions were considered: a full-width primary forest above three narrow support panels, and an asymmetric two-by-two arrangement. The first crowded the matrix’s row labels and the two diagnostic axes at a 7.2 pt minimum. The chosen arrangement gives the main contrast a wider column, keeps the 4 × 4 matrix readable, and retains enough width for the resource trajectory and its budget annotations. The final height, 181 mm, follows these content needs rather than a fixed aesthetic aspect ratio.

## Source-specific design evidence

The supplied skill’s scientific contract, dense-composition pattern D, visual-design guidance and production-review workflow were applied. Three actual source figure images were inspected. None of their artwork, data or scientific findings is copied into the delivered figure.

| Source anchor | Assigned job | Observed feature used | Adaptation and limit |
|---|---|---|---|
| [Monitoring Monitorability, v1, Figure 8, PDF p. 17](https://arxiv.org/pdf/2512.18311v1#page=17) | Controlled evidence presentation | A common legend and repeated axes keep method identities stable across budget conditions; short uncertainty bars accompany observations. | A shared policy key spans the entire new figure, and both quality/cost axes carry seed-block intervals. A same-width inspection at 178 mm showed the source’s dense legend and axes to be harder to read than the new 7.25 pt minimum; the source’s typography was not copied. |
| [Perception Encoder, v1, Figure 8, PDF p. 11](https://arxiv.org/pdf/2504.13181v1#page=11) | Condition matrix and label rail | A stable task-name rail and aligned condition columns make a dense diagnostic structure navigable. | Panel b keeps a stable four-task rail and four budget columns, with a single quantitative scale. It uses 16 labeled cells rather than 21 miniature curves. Task families remain neutral because categorical color already denotes policies. |
| [IdeaScientist, v1, Figure 2, PDF p. 8](https://arxiv.org/pdf/2610.04074v1#page=8) | Primary paired comparison | A dot-and-interval comparison presents a paired outcome directly and gives numerical estimates close to the marks. | Panel a adds the actual independent-unit effects behind the mean interval, prioritizes one contrast, and uses a dedicated numerical rail. It does not borrow the source’s radar chart or win-rate values. |

Source-derived observations are separated from original recommendations: the exact palette, dimensions, point sizes and panel proportions below are choices for this demonstration, not measurements of a corporate or conference style.

## Visual system

- **Physical geometry:** 178 × 181 mm, with 4 mm outer anchors, a wider left analysis column and a narrower right diagnostic column. The header identifies the design and shared policy key. A light horizontal rule separates the main effect/decomposition row from the resource/diagnostic row. The canvas is exported exactly, without a tight crop that changes print size.
- **Typography:** genuine DejaVu Sans TrueType regular and bold programs. The main heading is 10.6 pt, panel letters/headings 9.5 pt, major labels 7.7–8.3 pt, and the smallest supporting labels 7.25 pt. All PDF text is extractable and embedded; the SVG retains editable text. No font-size reduction is used to conceal an overcrowded region.
- **Policy semantics:** gray square = no memory; amber triangle/dashed line = unfiltered updates; teal circle/solid line = verified updates; purple diamond/short-dashed line = verified without history. Shape and line style retain identity in grayscale. The unfiltered small-text ink is darker than its data marks.
- **Quantitative semantics:** panel b’s rose–white–teal scale encodes signed percentage-point change around zero. It is a local quantitative key, not a fifth policy identity. Every cell has an explicit signed number, so sign and magnitude remain available in grayscale. Text switches to white only for the darkest cell; actual rendered fill/text contrast was checked.
- **Emphasis:** a pale continuous row band highlights the primary contrast, with a stronger mean label. Raw seed marks are hollow and lighter; the mean and interval sit above them. Baselines remain legible rather than fading into the background.
- **Lines and uncertainty:** light grid lines support reading values; stronger neutral zero lines define the null contrast. The resource plot joins only observed budget configurations. It does not draw a fitted curve, an attainable frontier or an extrapolated optimum.
- **Annotation routing:** short leaders identify the four verified budget points. The first label was moved off the unfiltered trajectory after inspecting the actual PDF. There are no unexplained system arrows or causal connectors.

## Data and estimand

The preserved inputs contain 24 independent matched seed blocks, four named task families, four configured memory budgets (256, 512, 1,024 and 2,048 tokens), four policies, and 96 sequential episodes per seed/family stream. This produces 9,216 shared exogenous scenario rows and 147,456 condition-specific outcome rows. Data generation, analysis and rendering are separate source files.

Every policy/budget combination receives the same task keys, proposals, baseline difficulty, success uniforms, checker uniforms and base task-token costs within a seed/family. This is actual common-random-number pairing, not a claim of pairing based only on matching seed labels. An update occurs only after the current episode is scored. All streams start with empty memory and all episodes are retained.

The primary estimand is the mean across seed blocks of the within-seed equal-weight average over the 16 fixed family/budget cells of verified success minus unfiltered success. Differences are formed before aggregation and are reported in percentage points. The fixed suite is the target; task-family or budget generalization is not claimed. The no-memory policy ignores budget, so its identical budget rows do not increase the independent sample size.

The 95% intervals are pointwise percentile intervals from 20,000 resamples of the 24 intact seed blocks. A sampled block brings every family, budget, policy and sequential episode with it. No within-stream episode bootstrap is used. The same bootstrap index draws are used across the entire figure. These are approximate finite-sample intervals, not simultaneous intervals, and no multiple-comparison correction is applied.

The history ablation is controlled for **total memory capacity**. Full verification allocates 25% of capacity to rejection hashes and 75% to records; the no-history policy allocates all of it to records. Both use the same checker. This deliberately changes both the presence of history and the available record slots, so the result is a capacity-allocation tradeoff, not an isolated zero-cost history effect. Checker false rejections are remembered too; the policy does not access invalidity ground truth.

The main synthetic effect is +6.57 pp [6.05, 7.13]. Full versus no-history is +0.02 pp [−0.41, 0.46]. The mechanism diagnostics improve under history, but the aggregate success effect does not. That behavior is stipulated by a simulator with helpful valid records, harmful invalid records, a fallible checker and finite memory; it is not a discovered law of memory systems.

## Review and fixes

1. The raw design, denominators, invariants and paired aggregation were verified from the preserved CSV inputs. Every raw outcome was joined back to its shared scenario; all success outcomes, probabilities and model-token totals were independently recomputed. Memory capacity is respected, every condition has 96 episodes, and no duplicate or missing outcome keys were found.
2. Actual final PDF renders were opened in color and grayscale. The first budget label was moved off a data trajectory, the full-versus-ablation wording was clarified, the primary row was made continuous through the plot, and several heatmap labels and amber text were darkened for contrast.
3. The final PDF was inspected at 180 dpi and as a 96 dpi full-width reference. The primary contrast, matrix values, policy shapes, axis units and diagnostic row labels remain readable at the intended 178 mm placement. The small seed dots are deliberately secondary, and the underlying values remain available in `analysis.json`.
4. A grayscale render was inspected after the final changes. Policy marker/line identities and numeric heatmap values remain interpretable. A formal color-vision-deficiency simulation was not performed.
5. Automated checks report exact 178 × 181 mm PDF dimensions, 100 extractable PDF text spans, 7.25 pt minimum exported text, two embedded compatible TrueType font programs, no out-of-page text, 101 editable SVG text nodes, zero raster images in the vector PDF, and zero overlapping measured text rectangles above a 0.5 pt tolerance.

The automatic checks do not certify statistical validity beyond the explicit simulator and estimator, nor do they replace human inspection of print output. The 96 dpi scale reference does not calibrate the user’s monitor. The intended use is a full-width 178 mm figure; reducing this export to 85 mm makes the smallest labels roughly 3.46 pt and requires recomposition.

## Manuscript caption fit

The main `caption.md` is 141 words; the complete 550-word explanation remains in `extended_caption.md`. A word-wrap estimate uses the actual DejaVu Sans advance widths, a 178 mm caption column, 1.2× line spacing, and a 3 mm artwork-to-caption gap. The calculation is preserved in `qa/caption_fit.json`.

| Caption type | Wrapped lines | Caption height | Artwork + 3 mm gap + caption |
|---|---:|---:|---:|
| 8 pt with 9.6 pt leading | 9 | 30.48 mm | 214.48 mm |
| 9 pt with 10.8 pt leading | 10 | 38.10 mm | 222.10 mm |

These totals are placement estimates, not guarantees for a manuscript template. The actual caption face and width, caption-prefix style, leading, paragraph spacing, float rules and available page height can change fit. Verify in the target LaTeX/Word template before placement; use the extended caption in supporting material when the manuscript caption must remain compact.

## Remaining limitations

This synthetic demonstration offers no evidence for real agent or task performance. Token-cost constants are illustrative and are not hardware, latency or monetary measurements. The named task families are parameterized scenarios, not external benchmarks. Only 24 independent seed blocks exist regardless of the number of episodes or bootstrap draws. Intervals are conditional on the fixed suite and simulator, pointwise and unadjusted. The diagnostic rates describe the construction; they do not identify a causal mediation effect. Small interval bars in panel d are partly covered by their mean markers because the simulated rates are precise at the block level; the full numerical intervals are preserved in `analysis.json`.
