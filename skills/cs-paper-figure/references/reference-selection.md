# Select and translate figure references

## Contents

1. Find a reference for the reader's task
2. Translate evidence into an original visual system
3. Choose visual density deliberately
4. Record what was actually inspected
5. Extend the corpus without inflating it

## 1. Find a reference for the reader's task

Start with the scientific relation and final physical size. A company name, publication date, or attractive palette alone does not identify an appropriate composition. Use the [current dense atlas](dense-paper-atlas.md) for newer source families and the catalog for a narrow lookup:

```bash
python <skill-root>/scripts/reference_catalog.py search --query "feedback loop" --since 2025 --limit 6
python <skill-root>/scripts/reference_catalog.py search --query "matched comparison" --since 2025
python <skill-root>/scripts/reference_catalog.py search --company NVIDIA --since 2025
python <skill-root>/scripts/reference_catalog.py show qwen38-next --figure "Figure 1"
python <skill-root>/scripts/reference_catalog.py stats
```

The catalog preserves source evidence; its lexical score is not a quality score. The `--family` filter searches explicitly recorded family fields. Earlier records may lack that field; use `--query` to search their observations. Read the complete selected figure record after locating an anchor.

Select two or three references with complementary jobs:

| Reference job | Question to answer | Transferable evidence |
| --- | --- | --- |
| Composition | Where does the reader begin, and where is the scientific change? | Panel ratio, aligned axes, overview/detail relation, spatial scope |
| Visual encoding | Which roles need to remain distinguishable? | Semantic color bindings, node/mark shapes, stroke hierarchy, direct labels |
| Evidence display | How can the reader check the argument? | Concrete records, examples, controlled axes, uncertainty, qualitative registration |

One source can serve all three jobs. Do not combine three incompatible styles merely to cite more papers. If a source has a useful layout but poor small text, preserve its layout principle and correct the typography. Treat excessive radar overlap, overloaded legends, tiny source labels, and ambiguous return paths as cautionary evidence.

## 2. Translate evidence into an original visual system

Use a short translation table before rendering. It prevents an extracted number from silently becoming a universal rule.

| Field | Example of the required distinction |
| --- | --- |
| Exact source anchor | Paper/version plus figure/page; HTML section/asset for native web figures |
| Observed property | A measured color with opacity, a declared SVG family, or a visibly estimated ratio |
| Evidence strength | Vector measurement, raster sample, visual estimate, declared style, or unknown |
| Scientific role in the new figure | Existing component, new operation, persistent state, baseline, or outcome |
| Authored choice | Actual production hex, font, point size, dimensions, stroke, and route |
| Reason for adaptation | Final-size readability, accessible labels, different topology, or manuscript width |

Build a coherent system instead of copying isolated constants:

- **Color:** distinguish role, novelty, and magnitude. If color already means modality, use a border/badge for new versus inherited components. Preserve the same role color in diagram labels, code identifiers, legend entries, and related plots only when the semantic identity is the same.
- **Typography:** distinguish observed family from available family. Use real weights. Source SVG CSS is a declaration; a substitute font used by a local renderer is not proof of the author's appearance. For outlined or raster lettering, leave family unknown unless there is independent evidence.
- **Layout:** preserve matched operation geometry across alternatives; allocate extra panel width for additional operations. Equal comparison conditions do not require equal whitespace. Separate causal time, system scope, and detail magnification.
- **Shapes:** use data examples, token arrays, state stacks, encoders, operators, or code only when they represent actual objects. Keep computation and persistent state distinguishable beyond color.
- **Strokes:** separate data routes, correspondence/zoom guides, scope borders, and statistical intervals. Arrow direction and attachment must remain explicit. A source's decorative shadow is not a data-flow cue.
- **Evidence:** use shared registration lines, fixed image crops, row reference levels, or stable record keys when comparisons depend on alignment. Never transform real heatmap colors or image masks merely to harmonize the palette.

Use the source-specific [recipe cards](style-recipes.md) for worked translations. Recommended values there are authored production choices, not claims of a universal company style.

## 3. Choose visual density deliberately

Richness should make an otherwise hidden relation inspectable. Add a mechanism close-up, a small real data record, or a matched output example when it reduces explanatory burden. Add a dedicated return corridor when it makes control flow clear. These details have scientific jobs.

Use this decision order:

1. Make the main relation visible at the final manuscript width.
2. Give the new operation or primary comparison a clear focal region.
3. Add only the local detail needed to understand or verify it.
4. Move secondary evidence into aligned supporting panels or a separate figure.
5. Resolve crowding by reflowing, shortening labels without changing meaning, or enlarging the figure before shrinking type.

A compact interval plot can be the correct figure. A four-stage method diagram needs more than four generic equal boxes when the mechanism depends on different object types or state changes. Judge specificity by whether the reader can identify the described method, not by the number of decorative elements.

Before approval, inspect the main relation with secondary labels temporarily ignored, then inspect the detailed relation at normal reading size. Both views should work. This is an editorial heuristic, not a quantitative aesthetic score.

## 4. Record what was actually inspected

Use `inspect_pdf_style.py` on a chosen figure crop and inspect the rendered crop. Keep the measurement file outside the packaged skill unless it is needed for an essential reproducible example. In source records, retain the PDF hash, version, page, crop and measurement caveats.

Watch for four concrete failure modes found in this corpus:

1. **Invisible searchable text:** a PDF can expose a familiar font while the visible figure is rasterized. Do not identify visible typography from that overlay.
2. **Outlined glyphs:** text can be vector paths. Its typeface cannot be recovered reliably from a list of path colors or stroke widths.
3. **Transparency:** raw red with 0.2 opacity on white appears pale pink. Preserve raw RGB, opacity and background, or report a sample from the rendered fill. Overlapping fills and non-white backgrounds require actual compositing inspection.
4. **Unreconciled transforms:** a PDF parser can return a stroke width much larger than the page. The inspector flags these raw values, excludes them from point-width summaries and crop padding, and leaves the rendered thickness unmeasured. Never silently divide by a guessed scale factor.

Also distinguish source-placement point sizes from new production sizes. A measured 5 pt label remains a 5 pt label in that source; an 8 pt replacement is a recommendation. A font file being available does not prove it was embedded in the final export.

## 5. Extend the corpus without inflating it

Count a canonical paper once across versions and indexes. Count a numbered or descriptive figure once, not once per panel. Assign one primary corporate group for exclusive totals and retain all affiliations separately. A paper and a blog summarizing it are one research source for coverage counts.

Require primary source identity, title/date/affiliation verification, an exact visual anchor, actual image inspection, and a useful transferable observation before adding a source. Keep inaccessible or text-only candidates outside the inspected corpus. A source may be an official HTML research article with native SVG figures; use its real anchors instead of inventing PDF pages.

The corpus includes peer-reviewed papers, preprints and technical reports. The count establishes neither top-conference acceptance nor scientific correctness. Prefer relevant recent sources, while retaining older examples when they teach a distinct and useful figure pattern.
