# Extract a verifiable visual specification from a research figure

## Evidence levels

Keep source observation separate from a recommendation for a new drawing.

| Level | What can be stated | Main limits |
| --- | --- | --- |
| `vector_measured` | Actual PDF fill/stroke values, opacity, path widths, visible text family/size, coordinates | PDF compositing, clipping, transforms and glyph paths can complicate interpretation |
| `searchable_overlay` | Font/name/size metadata in an invisible search layer | Does not certify the visible font, color, editability or glyph match |
| `svg_declared` | Family, weight, fill or size declared in the inspected native SVG/CSS | A declaration does not prove a local renderer had that font; user units are not PDF points |
| `raster_sampled` | RGB samples from a specified image or rendered crop | Compression, antialiasing, display transforms and transparency affect values; original font unknown |
| `visually_estimated` | Observed hierarchy, approximate ratios and spacing, topology, style | Label as an estimate; do not fabricate exact pixels/points/hex values |
| `recommendation` | Proposed tokens and geometry for the new task | These are design choices, not facts about the source |

## Procedure

1. Pin the paper version, actual publication/submission date, PDF hash, figure identifier and one-based page. Keep front-page dates separate from arXiv version dates when they differ.
2. Render the page, identify the exact figure boundary, and inspect the image. Text extraction alone does not establish aesthetics.
3. Define a crop in PDF points (top-left coordinates) that excludes page text and captions unless a caption is genuinely part of the figure composition. Save the crop bounds in the record.
4. Run the inspector:

```bash
python <skill-root>/scripts/inspect_pdf_style.py paper.pdf --page 3 \
  --clip 66 85 530 251 --out figure-style.json --preview figure-crop.png
```

5. Assign extracted colors to visible roles by inspecting the crop. The most frequent black paths may be glyphs; frequency is not evidence of semantic importance. Inspect opacity separately from RGB.
6. Check text-rendering modes. Text rendering mode 3 (invisible) and opacity-zero text are not visible typography. This rendering-mode value is unrelated to the PDF Type 3 font format. Whole-page font resources can belong to body prose. An outlined or raster figure may have no verifiable font even when the paper is searchable.
7. Record the hierarchy: panel/group/module/body/edge/mono/math; actual point sizes at PDF placement; weights; alignment; wrapping; repeated labels; font substitutions if known.
8. Record layout: figure aspect, panel ratios, gutter sizes, group padding, card spacing, shared baselines, alignment axes, reading order, overview-to-detail links and insets.
9. Record shapes/edges: computation versus data/state, corner radii if measurable, border hierarchy, arrowhead style, endpoint ports, junctions, curve/orthogonal routes, label offsets, feedback corridors and boundary meaning.
10. Record strengths and weaknesses. A source may have useful grouping but unreadably small labels or misleading scale treatment. Preserve what works and correct what fails.
11. Translate the source into an original design recipe at the new physical size. Keep the scientific system's actual entities and edges. Distinguish measured source constants from readable production recommendations.

## Five extraction failure modes

**Invisible text.** Exclude invisible OCR/search layers from visible-font claims. Preserve their separate evidence category if useful for labels. A searchable page is not necessarily an editable figure.

**Outlined or raster text.** Use an unverified family when the actual glyph program is unavailable. Native SVG declarations can establish the intended family but not the font used by a local fallback rendering. Record preview substitutions, and do not convert SVG user-unit sizes to points without the viewport transform and physical placement.

**Transparency and compositing.** Preserve raw RGB, path alpha, enclosing group opacity and background as a set. A path with alpha 1 can still be inside a group with opacity 0.25, as observed in the new Emergent Misalignment study. For simple foreground-over-background compositing, a raw red at alpha 0.2 over white appears pale pink; do not substitute opaque red in a new design because an extractor returned `#FF0000`. Label rendered samples separately from raw vector values. Clipping, blending modes and overlapping objects can require inspection beyond the simple alpha formula.

**Transform-anomalous stroke widths.** Qwen-Image Figure 6 returned raw widths 15,875–25,400 from the drawing API although the figure visibly has ordinary strokes. The inspector flags non-finite, negative and larger-than-page widths, preserves their raw values, and excludes them from physical-width summaries and crop-overlap padding. This is a sanity filter, not complete transform recovery: inspect plausible-looking widths too when the crop disagrees. Do not infer stroke thickness from an anomalous number or let it expand an object's crop intersection.

**Malformed Unicode glyph mappings.** DeepSeek-Prover-V2 Figure 2 yielded isolated UTF-16 surrogate values in PDF text traces. Those values are not valid Unicode scalar characters. The inspector writes U+FFFD in the extracted string and preserves each original code point and selected index in `invalid_unicode_glyphs`; the UTF-8 JSON report remains writable. Do not guess the missing mathematical symbol from the replacement character. Inspect the rendered crop and retain the extraction caveat.

## Minimum useful study record

Include source/version/page/figure/hash; the inspected crop; evidence level for every numerical claim; semantic palette with fill/outline/text roles; typography hierarchy; layout geometry; shape/arrow grammar; one transferable recipe; one caution; and what remains unknown. Do not claim to have recovered the original authoring program solely from familiar colors or shapes.

The modern and recent atlases follow this procedure. Use [recent-paper-atlas.md](recent-paper-atlas.md) to locate the 35 additional studies and [reference-selection.md](reference-selection.md) to translate observations into task-specific choices. The bundled inspector intentionally does not infer a complete CSS theme or layout from an entire page. A local crop plus human visual interpretation is necessary to connect measurements to scientific meaning.
