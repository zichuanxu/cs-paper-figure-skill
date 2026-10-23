# Production and review

## Contents

1. Choose the implementation
2. Establish the visual specification and build editable source
3. Export without changing the intended size
4. Inspect the actual artifact
5. Apply completion gates
6. Hand off caption, alt text, and provenance

## 1. Choose the implementation

| Content | Preferred starting tools | Notes |
| --- | --- | --- |
| Quantitative plots | Matplotlib; existing scientific plotting stack | Preserve data and statistical processing separately |
| Exact architecture diagrams | SVG, TikZ, Graphviz, or programmatic vector shapes | Preserve topology, editable text, and layout source |
| Timelines | Vector rectangles/paths on a true time axis | State measured or schematic timing |
| Dense images/spatial arrays | Raster data inside vector labels/axes | Preserve original image and display transform |
| Qualitative grids | Real experimental image assets in an aligned layout | Preserve sample IDs and selection policy |
| Interactive explanatory companion | Appropriate interactive plotting framework | Still export a standalone paper figure if requested |

Do not use a raster image generator for exact data charts, equations, labels, or computational topology. Do not use a web screenshot as the editable master. Preserve an established project toolchain unless it blocks a necessary output.

## 2. Establish the visual specification and build editable source

Choose complementary 2025–2026 figures from [recent-paper-atlas.md](recent-paper-atlas.md) or the earlier [modern-paper-atlas.md](modern-paper-atlas.md), using the catalog to retrieve exact records. Give each source a job such as composition, semantic encoding or evidence presentation. Inspect its actual figure region, then record the chosen palette roles, typography hierarchy, layout proportions, shape vocabulary and route channels in the figure brief. Keep measured source properties separate from recommendations for the new figure. Follow [design-extraction.md](design-extraction.md) when adding a source study, and [style-recipes.md](style-recipes.md) when translating evidence into an original composition.

Keep the figure brief, data, processing code, and rendering source accessible. Use the strict JSON renderer only for its supported cases; use custom code for other layouts. Read [spec-format.md](spec-format.md) for the actual accepted fields and examples. A shared style helper supplies consistent defaults; it does not replace choosing a figure-specific composition.

The style helper provides:

```python
from figure_style import style_context, make_figure, export_figure

with style_context(font_size=8):
    fig, ax = make_figure(width_mm=85, height_mm=60)
    # Draw verified data here; set metric labels, units, and scope.
    files = export_figure(
        fig, "figures/result",
        source_files=["data/result.csv", "figures/result.py"],
        metadata={"data_status": "measured", "claim": "Scoped finding"},
    )
```

Place the helper on the Python import path or copy it with the figure source when a self-contained handoff is needed. The helper uses NumPy and Matplotlib. The PDF checker additionally uses PyMuPDF; install/use an available equivalent if it is missing, or explicitly report the unavailable automated check. Do not alter the scientific analysis merely to fit a bundled renderer.

Keep final-size typography in the source. Derive labels, deltas, and ratios from the same data used to draw the marks. If a renderer sorts a coordinate for a curve, preserve the series identity and all values. Do not silently sort categorical conditions to make a narrative look stronger.

Use the modern examples for a routed architecture and quantitative panels:

```bash
python <skill-root>/scripts/render_modern_examples.py --out /tmp/cs-modern-figure-examples
```

They produce a schematic memory architecture with semantic tinted groups, nested cards, record miniatures and explicitly routed feedback, plus two empirical-style panels using synthetic observations, consistent marker/color roles, defined uncertainty and data-derived annotations. The diagram validates its declared geometry before export. Each package preserves the inputs, caption, alt text and provenance. Adapt the visual grammar to the actual system; do not copy the example's modules or edges into a different method.

Use the reference-driven recipe for matched state cards, evidence correspondence, and diagram-to-code color binding:

```bash
python <skill-root>/scripts/render_reference_recipe.py --out /tmp/cs-reference-recipe
```

This original schematic combines transferable principles from AlphaEvolve, SAM 3 and Circuit Tracing. It declares six directed routes, validates them against rendered text bounds, and separates edited state from an audit receipt. Its hypothetical record and verified-write topology are demonstration assumptions, not claims about any source paper. The renderer's font helper chooses real regular/bold TrueType font programs for its Matplotlib Type 42 exports and records the selected files.

Keep the earlier statistical recipes as additional examples:

```bash
python <skill-root>/scripts/render_examples.py --out /tmp/cs-figure-examples
```

They cover curves and tradeoffs, paired descriptive intervals, shared-scale heatmaps, and an earlier schematic memory system. Use them for their data/encoding patterns; the modern showcase is the primary reference for current visual design and connector construction. Never reuse any demonstration values as an empirical result.

Use the inspection and checking tools for their distinct purposes:

| Tool | Role | Limits that still require review |
| --- | --- | --- |
| `inspect_pdf_style.py` | Extract source-PDF text-rendering modes, font metadata, vector colors/strokes and coordinates from an explicit figure crop; save an optional preview | Does not identify a whole-page theme, assign scientific roles to colors, recover raster/outlined fonts, or reconstruct complete composited visibility. Invisible search-layer text is not visible-font evidence. Implausible widths are flagged and omitted from summaries; less obvious transform issues still require visual review. |
| `diagram_geometry.py` | Validate declared node rectangles, typed ports, orthogonal polylines and measured label bounds in one coordinate system | Does not solve layout or certify curves, rounded-corner tangencies, painted stroke/arrowhead extents, occlusion or scientific meaning. The renderer must use the same geometry; background group containers are not semantic nodes. |
| `check_figure.py` | Check exported PDF dimensions, text size, out-of-page text, font-embedding evidence and an observed CFF/TrueType program mismatch | Does not certify aesthetic quality, all collisions, all font-format issues, topology or statistical correctness. Raster/outlined text can make a text check inconclusive. |

Read each tool's actual API before using it. Reserve feedback corridors and declare source/target ports before drawing a complex diagram. Use rendered text bounds for label checks, not character-count estimates. See [diagram-routing.md](diagram-routing.md) for the geometry contract and the border-riding failure it prevents.

## 3. Export without changing the intended size

Default to:

- **PDF:** vector marks and text, with embedded fonts where supported; suitable for LaTeX/manuscript placement.
- **SVG:** editable vector source; retain text and document its font dependency.
- **PNG:** quick review preview at a suitable resolution, typically 300 dpi for these examples.
- **Source/spec/data:** sufficient to reproduce the figure, with caption and alt text.

If the venue requires different formats, follow its current template. Prefer vector strokes/text to simply increasing raster DPI. Rasterize only dense artists when necessary for output size and retain vector labels. Check the effective resolution of embedded images at the final physical dimensions.

The helper exports an exact canvas and intentionally avoids `bbox_inches="tight"`, which can change the saved physical size. Its text-boundary check may flag out-of-canvas labels; fix geometry rather than allowing silent cropping. If using another exporter or cropping step, measure the resulting PDF dimensions afterward.

Check actual font programs as well as embedding. A CFF-flavored OTF can be embedded under a TrueType declaration by a mismatched export configuration and still trigger a renderer warning. For Matplotlib Type 42 output, the bundled modern font selector uses true TrueType regular/bold files. Other backends may correctly support CFF; this is an export compatibility rule, not a ban on OTF. Verify the saved PDF in a second renderer when the primary preview and font metadata disagree. Keep the intended family, fallback family, real weights and required SVG fonts in provenance.

The helper records source/output hashes and software versions in a JSON manifest. A manifest supports traceability but does not itself validate the scientific claim. Keep raw private inputs out of public artifacts unless their inclusion is intended.

## 4. Inspect the actual artifact

1. Render the exported PDF, not just the plotting window. Inspect every panel and label.
2. View the figure at intended physical scale and placed in the manuscript page. Do not judge readability solely at a large screen zoom.
3. Compare the output with the selected source figures at similar physical width. Check whether the palette roles, type hierarchy, panel proportions, semantic shapes and mechanism detail satisfy the brief. Fix a generic equal-box layout or unstyled default plot when it fails that target; adding arbitrary color does not resolve a weak composition.
4. Trace every diagram edge against the declared adjacency list. Check visible port attachment, normal entry/exit, arrowheads, nonendpoint intersections, label clearance and separation of return paths. A route must not ride along a node border or use a group boundary as an accidental connection.
5. Check captions, line styles, legends, scales, colors, crop equality, and all glyphs. Ensure that precise labels and derived callouts match their source values.
6. Inspect a grayscale conversion. Run color-vision simulations when available and check redundant encodings.
7. Inspect vector output properties: page size, fonts, raster-only fallbacks, and editability.
8. Reopen/rerender after substantive changes. If tools are unavailable, say which check remains unperformed.

Useful commands when installed:

```bash
python <skill-root>/scripts/check_figure.py figures/result.pdf --expected-width-mm 85 --min-font-pt 7
pdfinfo figures/result.pdf
pdffonts figures/result.pdf
pdftoppm -scale-to 1600 -png -singlefile figures/result.pdf /tmp/result-review
```

The automated checker reports physical dimensions, small text spans, out-of-page text, and available font-embedding evidence. It cannot certify all label overlaps, arrow routing, color distinguishability, statistical validity, or scientific correctness. Read its actual output and inspect the rendered image. Avoid asserting that a figure is "publication ready" solely because a script exits successfully.

## 5. Apply completion gates

| Gate | Pass condition | Common blocking defect |
| --- | --- | --- |
| Evidence | Every value/edge has an identified basis | Invented numbers, unsupported topology, unlabeled synthetic content |
| Comparison | Metrics, budgets, groups, and scope are explicit | Unmatched conditions implied to be controlled |
| Statistics | Aggregation, independent unit, n, and intervals agree | Bootstrap rows that are not independent; guessed CI |
| Visual design | The figure has an intentional hierarchy, task-specific mechanism/data detail, coherent tokens and a defensible comparison with its selected references | Equal-weight generic boxes, decoration without meaning, unplanned spacing, or a default plot that misses the visual brief |
| Connector geometry | Every declared route has visible, unambiguous endpoints and meaning; ports, label clearance, feedback corridors and actual painted boundaries have been checked | Border riding, floating arrowheads, a return path entering the wrong side, accidental intersections or an unmarked junction |
| Readability | Main relation and necessary details are legible at final size | Tiny type, overlapping annotations, undecodable legend |
| Accessibility | Essential categories survive more than hue alone | Color-only condition coding |
| Production | Actual exports render correctly at the intended dimensions | Clipping, font substitution, unexpected page crop |
| Reproducibility | Data/spec/source regenerate the result | Manual edits or annotations disconnected from source |

For critiques, separate **blocking scientific or routing errors**, **material design/readability issues**, and **optional polish**. Correct factual meaning and ambiguous connectivity first, then satisfy the visual brief and final-size legibility. A material design failure is unfinished work even when the export passes technical checks. Do not average a scientific failure away in a composite aesthetic score.

For a simple change, run the checks relevant to the concrete risk. For a new statistical figure or complex diagram, run all applicable gates. Stop optional testing when remaining risk has been resolved.

## 6. Hand off caption, alt text, and provenance

Use meaningful filenames such as `fig3_memory_repair.pdf`, with matching source/spec names. Preserve existing naming conventions. Do not overwrite the raw data or the previous editable source without an intended replacement workflow.

Provide a caption that states the finding, explains panels and encodings, and identifies experimental/uncertainty conditions, and nothing about how the figure was made or drawn (see scientific-contract.md §7, "What stays out"; run `paperkit.py caption`). For invented numerical observations, place an unambiguous label such as **SYNTHETIC DATA** or **ILLUSTRATIVE DATA** inside the figure, and explicitly state in the caption that the values are constructed and are not experimental results. No single exact phrase is required. For a pure conceptual diagram, **SCHEMATIC** is appropriate; do not use that word alone to disguise invented numerical evidence. Label mixed schematic/synthetic panels according to their content.

Write alt text that first identifies the figure's purpose, then the main relationships and any important qualification. Do not rely on color names alone, and do not claim the figure proves more than the analysis supports.

In the delivery note, explain concrete design choices: which role each color represents, the font/size hierarchy, why the layout fits the mechanism or comparison, and how important return paths are routed. State what was checked and any known limit. Link requested artifacts according to the host environment's saving rules. Preserve enough provenance to audit and revise the figure without forcing the user to reconstruct the pipeline.
