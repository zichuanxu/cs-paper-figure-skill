# Strict chart specification

Use `scripts/plot_from_spec.py INPUT.json --out OUTPUT_STEM` for reproducible curves, interval comparisons, trade-offs, and heatmaps. The command exports PDF, SVG, PNG, and a provenance manifest. Use Python with NumPy and Matplotlib; the adjacent `figure_style.py` must be present. Use custom plotting code for figure types this format cannot express honestly.

Contents: [Common fields](#common-fields) · [Curve](#curve) · [Interval comparison](#interval-comparison) · [Trade-off](#trade-off) · [Heatmap](#heatmap) · [PDF checks](#pdf-checks).

## Common fields

| Field | Requirement |
|---|---|
| `kind` | `curve`, `interval`, `tradeoff`, or `heatmap` |
| `title`, `claim` | At least one nonempty string; `title` is displayed when both exist; `claim` remains in the manifest |
| `x`, `y` | Objects with nonempty `label` and `unit`; use `"unitless"` explicitly for dimensionless quantities |
| `x.scale`, `y.scale` | Optional `linear` (default) or `log`; categorical axes must remain linear |
| `data_status` | `measured`, `reported`, or `illustrative`; illustrative outputs visibly say **ILLUSTRATIVE DATA** |
| `provenance` | Nonempty string identifying the data origin, evaluation population, and relevant conditions; never invent provenance |
| `size` | Optional object: positive `width_mm`, `height_mm`, and `font_size` above 0.5 pt; defaults 85 mm, 65 mm, 8 pt; use at least 7 pt for normal print labels |
| `interval_semantics` | Required whenever intervals exist: state interval type/level, sampling or resampling unit, and computation method |

Unknown fields and duplicate JSON keys are rejected. All numeric observations must be finite JSON numbers, not strings or booleans. `NaN` and infinity are rejected. Empty datasets, mismatched lengths, duplicate labels, reversed endpoints, and nonpositive observations **or interval endpoints** on log axes are rejected. Log checks also apply to null-reference lines. No smoothing, fitting, aggregation, interval estimation, or missing-value imputation is performed.

Log axes use compact plain numeric/scientific tick labels and explicitly say `[log scale]` in the axis label. This avoids tiny superscripts and crowded repeated powers of ten at column width.

Intervals need not contain the estimate: the renderer draws the estimate and endpoints independently. This permits legitimate interval constructions without silently changing the estimate. The supplied interval must still be scientifically justified.

`role` is optional for series, interval items, or trade-off points: `focus`, `reference`, `alternative`, `teal`, or `purple`. It chooses a semantic theme color. When absent, roles cycle in that order. Curves also receive distinct line/marker styles. Supply a stable role mapping across figures, rather than relying on ordering. Color alone must not bear a scientific distinction.

The manifest hashes the input spec and rendering code. Its provenance description is user-supplied metadata, not external verification of the dataset. Archive the actual source data and preprocessing separately when they are external to the spec.

## Curve

Provide `series`, a nonempty array of objects with unique `label`, equally sized numeric `x` and `y`, and optional `role`. Each `x` sequence must be strictly increasing; sort deliberately before authoring the spec if appropriate. To show a band, provide both `lower` and `upper`, each matching `y`. Bands show supplied intervals; lines join supplied observations without fitting.

```json
{
  "kind": "curve",
  "title": "Success across interaction budgets",
  "x": {"label": "Interaction budget", "unit": "calls", "scale": "log"},
  "y": {"label": "Task success", "unit": "%"},
  "data_status": "illustrative",
  "provenance": "Synthetic layout example; these are not research results.",
  "interval_semantics": "Illustrative bounds only; not estimated confidence intervals.",
  "series": [{
    "label": "Example system", "role": "focus",
    "x": [1, 2, 4, 8], "y": [35, 46, 57, 63],
    "lower": [30, 41, 52, 58], "upper": [40, 51, 62, 68]
  }]
}
```

## Interval comparison

Provide `items`, preserving the intended row order. Each has `label`, `estimate`, `lower`, `upper`, and optional `role`. Here `x` is the quantitative metric, while `y` names the categorical rows. Optional `reference` is exactly `0` or `1`, denoting a null comparison value; omit it when neither is meaningful. The reference must be positive on a log axis.

```json
{
  "kind": "interval",
  "title": "Effect estimates by system",
  "x": {"label": "Success difference", "unit": "percentage points"},
  "y": {"label": "System", "unit": "unitless"},
  "data_status": "illustrative",
  "provenance": "Synthetic layout example; no empirical inference.",
  "interval_semantics": "Illustrative interval endpoints, not statistical estimates.",
  "reference": 0,
  "items": [
    {"label": "A", "estimate": 4, "lower": 1, "upper": 7, "role": "focus"},
    {"label": "B", "estimate": 1, "lower": -2, "upper": 4, "role": "reference"}
  ]
}
```

## Trade-off

Provide `points` with unique `label`, numeric `x` and `y`, and optional `role`. Both axes must explicitly declare `direction`: `minimize` or `maximize`; arrows beside the labels expose those directions. Optional `frontier: true` outlines the **observed nondominated set among supplied points**. It does not infer a continuous frontier or account for measurement uncertainty. Domination requires no worse performance on both axes and strictly better performance on at least one; exact-coordinate ties all remain nondominated when applicable. Labels for identical coordinates are grouped.

```json
{
  "kind": "tradeoff",
  "title": "Success and latency",
  "x": {"label": "Latency", "unit": "ms", "direction": "minimize"},
  "y": {"label": "Task success", "unit": "%", "direction": "maximize"},
  "data_status": "illustrative",
  "provenance": "Synthetic layout example; hardware and evaluation are unspecified.",
  "frontier": true,
  "points": [
    {"label": "A", "x": 50, "y": 60},
    {"label": "B", "x": 80, "y": 72},
    {"label": "C", "x": 90, "y": 65}
  ]
}
```

Prefer sparse, directly labeled comparisons. Dense point clouds or long model names need a custom labeling/layout solution and visual review.

## Heatmap

Provide unique `rows` and `columns`, a matching rectangular `values` matrix, and `colorbar: {"label": ..., "unit": ...}` for the encoded numeric metric. Only heatmap cells may be `null`; they receive a separate gray/hatch encoding and `NA`, never zero. At least one cell must be observed. `zero_center: true` selects a symmetric diverging scale and requires a nonzero observation. Otherwise the scale is sequential. Optional `annotate: true` prints observed numbers to three significant digits; the manifest/spec retains original precision.

```json
{
  "kind": "heatmap",
  "title": "Success across task conditions",
  "x": {"label": "Budget", "unit": "calls"},
  "y": {"label": "Task family", "unit": "unitless"},
  "colorbar": {"label": "Success", "unit": "%"},
  "data_status": "illustrative",
  "provenance": "Synthetic layout example; NA marks an unobserved combination.",
  "rows": ["Retrieval", "Planning"], "columns": ["2", "4", "8"],
  "values": [[30, 46, 58], [25, null, 49]],
  "annotate": true
}
```

## PDF checks

Run `python scripts/check_figure.py FIGURE.pdf --expected-width-mm 85 --min-font-pt 7 --json QA.json`. PyMuPDF is optional for this check. It reports page dimensions, text spans below the threshold, text outside the page, and extractable font embedding. Exit codes: `0` for no automated findings; `1` for findings; `2` for invalid input or an unavailable dependency. Type3 font embedding is reported as unverified, and pages without extractable text are flagged as inconclusive. The default width tolerance is 0.5 mm and can be set with `--width-tolerance-mm`.

These checks do not certify absence of overlaps, scientific validity, statistical correctness, color accessibility, or legibility of rasterized/outlined text. Inspect every final-size export. Use the full QA workflow in the skill for interpretation, captions, and print-scale review.
