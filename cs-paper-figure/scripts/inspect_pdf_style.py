#!/usr/bin/env python3
"""Measure PDF objects in a user-selected figure region; do not infer a design recipe.

Example:
  python inspect_pdf_style.py paper.pdf --page 3 --clip 66 85 530 251 \
      --out figure-style.json --preview figure-crop.png

Requires PyMuPDF. Coordinates are unrotated page points, origin at the top left,
x rightward and y downward; 1 point = 1/72 inch. A page is 1-based. The PDF is
never rewritten. This tool does not identify a figure boundary automatically.

API references (checked 2026-10-21):
https://pymupdf.readthedocs.io/en/latest/functions.html#Page.get_texttrace
https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_drawings
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None


def rounded(values):
    return [round(float(v), 6) for v in values]


def pdf_color(value):
    """Retain raw PDF-extracted values; report a quantized RGB convenience value."""
    if value is None:
        return None
    values = tuple(float(v) for v in value)
    rgb = values * 3 if len(values) == 1 else values if len(values) == 3 else None
    return {
        'components': list(values),
        'hex_rgb_8bit': ('#' + ''.join(f'{max(0, min(255, round(v * 255))):02X}' for v in rgb)) if rgb else None,
        'interpretation': 'GRAY expanded to RGB' if len(values) == 1 else 'PyMuPDF RGB' if len(values) == 3 else 'unsupported component count; no RGB guess',
    }


def overlaps(a, b, padding=0.0):
    """Include zero-height horizontal and zero-width vertical path bounds."""
    return (a[2] + padding >= b[0] and a[0] - padding <= b[2]
            and a[3] + padding >= b[1] and a[1] - padding <= b[3])


def inside_center(bbox, clip):
    x, y = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
    return clip.x0 <= x <= clip.x1 and clip.y0 <= y <= clip.y1


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def text_measurements(page, clip):
    groups = {'visible': [], 'invisible': [], 'other': []}
    for trace in page.get_texttrace():
        selected = [c for c in trace['chars'] if inside_center(c[3], clip)]
        if not selected:
            continue
        mode, opacity = trace.get('type'), float(trace.get('opacity', 1.0))
        category = 'invisible' if mode == 3 or opacity == 0 else 'visible' if mode in (0, 1) else 'other'
        bounds = fitz.Rect(selected[0][3])
        for c in selected[1:]:
            bounds |= fitz.Rect(c[3])
        # A PDF CMap may yield isolated UTF-16 surrogates or invalid code points.
        # They are glyph-extraction failures, not valid Unicode text. Preserve
        # their raw values for audit and never let them break the UTF-8 report.
        invalid = [{'selected_index': i, 'raw_codepoint': c[0]}
                   for i, c in enumerate(selected)
                   if not (0 <= c[0] <= 0x10FFFF and not 0xD800 <= c[0] <= 0xDFFF)]
        text = ''.join(chr(c[0]) if 0 <= c[0] <= 0x10FFFF and not 0xD800 <= c[0] <= 0xDFFF
                       else '\uFFFD' for c in selected)
        groups[category].append({
            'text_in_pdf_order': text,
            'font': trace.get('font'),
            'size_pt': round(float(trace['size']), 6),
            'color': pdf_color(trace.get('color')),
            'type': mode,
            'type_label': {0: 'fill', 1: 'stroke', 3: 'ignored/hidden'}.get(mode, 'unknown'),
            'opacity': opacity,
            'bbox_pt': rounded(bounds),
            'selected_characters': len(selected),
            'invalid_unicode_glyphs': invalid,
            'partial_trace_at_crop_boundary': len(selected) != len(trace['chars']),
            'writing_direction': rounded(trace.get('dir', (1, 0))),
            'layer': trace.get('layer'),
            'paint_sequence': trace.get('seqno'),
        })
    summary = []
    for category, spans in groups.items():
        counts = Counter((s['font'], s['size_pt'], s['type']) for s in spans)
        characters = Counter()
        for s in spans:
            characters[(s['font'], s['size_pt'], s['type'])] += s['selected_characters']
        for (font, size, mode), count in counts.most_common():
            summary.append({'visibility_class': category, 'font': font, 'size_pt': size,
                            'type': mode, 'trace_count': count,
                            'character_count': characters[font, size, mode]})
    return {'classification': 'Nominal PDF text rendering mode and opacity only; occlusion/clipping is not resolved.',
            'unicode_caveat': 'Invalid scalar values, including isolated UTF-16 surrogates, are shown as U+FFFD. Raw values are retained per span; inspect the rendered glyph instead of inferring its text.',
            'counts': {k: len(v) for k, v in groups.items()},
            'region_font_summary': summary, 'spans': groups}


def vector_measurements(page, clip):
    try:
        drawings = page.get_drawings(extended=True)
        extended = True
    except TypeError:
        drawings = page.get_drawings()
        extended = False
    paths, context = [], []
    color_counts, width_counts = Counter(), Counter()
    untrusted_width_count = 0
    page_span = max(float(page.rect.width), float(page.rect.height))
    for d in drawings:
        rect = d.get('rect')
        if rect is None:
            continue
        raw_width = d.get('width')
        width = float(raw_width) if raw_width is not None else None
        width_note = None
        if width is not None and (not math.isfinite(width) or width < 0 or width > page_span):
            # Some transformed PDF paths expose a width in an unreconciled
            # coordinate scale. Never use that number as points, or as crop
            # padding: it would pull unrelated page objects into a figure.
            width_note = 'Untrusted raw width: nonfinite, negative, or larger than the page span. Inspect the rendered stroke; do not infer point units or silently rescale.'
            width = None
        if not overlaps(rect, clip, (width or 0) / 2):
            continue
        if d.get('type') in ('clip', 'group'):
            context.append({'type': d['type'], 'bbox_pt': rounded(rect), 'level': d.get('level'),
                            'scissor_pt': rounded(d['scissor']) if d.get('scissor') else None,
                            'opacity': d.get('opacity'), 'blendmode': d.get('blendmode'),
                            'isolated': d.get('isolated'), 'knockout': d.get('knockout')})
            continue
        fill, stroke = pdf_color(d.get('fill')), pdf_color(d.get('color'))
        if width_note and stroke:
            untrusted_width_count += 1
        for role, color in [('fill', fill), ('stroke', stroke)]:
            if color and color['hex_rgb_8bit']:
                alpha = d.get('fill_opacity' if role == 'fill' else 'stroke_opacity')
                color_counts[(role, color['hex_rgb_8bit'], alpha)] += 1
        if width is not None and stroke:
            width_counts[round(float(width), 6)] += 1
        paths.append({'type': d.get('type'), 'bbox_pt': rounded(rect),
                      'crosses_selected_region_boundary': not clip.contains(rect),
                      'fill': fill, 'stroke': stroke,
                      'stroke_width_pt': round(float(width), 6) if width is not None else None,
                      'raw_stroke_width': float(raw_width) if raw_width is not None and math.isfinite(float(raw_width)) else None,
                      'stroke_width_note': width_note,
                      'fill_opacity': d.get('fill_opacity'), 'stroke_opacity': d.get('stroke_opacity'),
                      'dash_pattern': d.get('dashes'), 'line_cap': d.get('lineCap'),
                      'line_join': d.get('lineJoin'), 'path_item_count': len(d.get('items', [])),
                      'path_item_types': dict(Counter(item[0] for item in d.get('items', []))),
                      'level': d.get('level'), 'layer': d.get('layer'), 'paint_sequence': d.get('seqno')})
    return {'path_count': len(paths), 'extended_context_available': extended,
            'untrusted_stroke_width_path_count': untrusted_width_count,
            'stroke_width_sanity_rule': 'Widths exceeding the longest page dimension, negative widths, and nonfinite widths are retained as untrusted raw metadata but excluded from point-width summaries and crop padding. This conservative check cannot detect every transform error.',
            'color_counts': [{'role': r, 'hex_rgb_8bit': c, 'opacity': a, 'path_count': n}
                             for (r, c, a), n in color_counts.most_common()],
            'stroke_width_counts': [{'width_pt': w, 'path_count': n} for w, n in width_counts.most_common()],
            'paths': paths, 'clip_and_group_context': context,
            'count_interpretation': 'Object counts, not occupied image area. Outlined glyphs may dominate counts.'}


def inspect_pdf(pdf, page_number, crop, out, preview=None, dpi=216):
    if fitz is None:
        raise RuntimeError('PyMuPDF is required: install pymupdf in the active Python environment.')
    if not pdf.is_file():
        raise ValueError(f'PDF not found: {pdf}')
    if not all(math.isfinite(v) for v in crop) or crop[0] >= crop[2] or crop[1] >= crop[3]:
        raise ValueError('--clip must contain finite ordered coordinates x0 < x1 and y0 < y1.')
    if not math.isfinite(dpi) or not 36 <= dpi <= 600:
        raise ValueError('--dpi must be between 36 and 600.')
    targets = [out.resolve()] + ([preview.resolve()] if preview else [])
    if pdf.resolve() in targets or len(set(targets)) != len(targets):
        raise ValueError('Output paths must be distinct and must not overwrite the input PDF.')
    if preview and preview.suffix.lower() != '.png':
        raise ValueError('--preview must have a .png filename.')
    with fitz.open(pdf) as doc:
        if not doc.is_pdf:
            raise ValueError('Input must be a PDF.')
        if doc.needs_pass:
            raise ValueError('Encrypted PDF requires decryption before style inspection.')
        if not 1 <= page_number <= len(doc):
            raise ValueError(f'--page must be from 1 to {len(doc)}.')
        page = doc[page_number - 1]
        original_rotation = page.rotation
        original_page_size = [page.rect.width, page.rect.height]
        # Normalize only the in-memory page so crop coordinates and preview agree.
        page.set_rotation(0)
        bounds = page.rect
        clip = fitz.Rect(crop)
        if not bounds.contains(clip):
            raise ValueError(f'--clip must lie inside unrotated page bounds {tuple(bounds)}.')
        rasters = []
        for im in page.get_image_info():
            if overlaps(im['bbox'], clip):
                rasters.append({'bbox_pt': rounded(im['bbox']), 'pixel_width': im['width'],
                                'pixel_height': im['height'], 'colorspace': im.get('cs-name'),
                                'has_mask': im.get('has-mask'),
                                'crosses_selected_region_boundary': not clip.contains(fitz.Rect(im['bbox']))})
        report = {
            'schema_version': '1.1', 'measurement_kind': 'observed PDF object properties; no design recommendations',
            'input': {'path': str(pdf.resolve()), 'sha256': digest(pdf), 'page_1_based': page_number,
                      'pymupdf_version': fitz.VersionBind},
            'coordinate_system': {'units': 'PDF points; 1 pt = 1/72 inch',
                                  'origin': 'top left of unrotated page', 'x': 'rightward', 'y': 'downward',
                                  'region_selection': 'required user-selected rectangle; no automatic figure identification'},
            'page': {'original_rotation_degrees': original_rotation,
                     'original_display_size_mm': rounded(v * 25.4 / 72 for v in original_page_size),
                     'unrotated_size_pt': rounded([bounds.width, bounds.height]),
                     'unrotated_size_mm': rounded([bounds.width * 25.4 / 72, bounds.height * 25.4 / 72])},
            'selected_region': {'bbox_pt': rounded(clip), 'size_mm': rounded([clip.width * 25.4 / 72, clip.height * 25.4 / 72]),
                                'aspect_ratio': clip.width / clip.height,
                                'width_fraction_of_page': clip.width / bounds.width,
                                'height_fraction_of_page': clip.height / bounds.height},
            'text': text_measurements(page, clip), 'vector': vector_measurements(page, clip),
            'raster': {'occurrence_count': len(rasters), 'occurrences': rasters,
                       'note': 'Occurrences, not unique images. Raster font/color measurements are not inferred.'},
            'caveats': [
                'Only objects selected by the crop are reported. Do not call whole-page fonts figure fonts; choose the actual figure bounds.',
                'Visible means nominal text mode 0/1 with positive opacity. Later objects, clipping, optional content or masks can still hide it; visually inspect the preview.',
                'Invisible text mode 3 and zero-opacity text may be OCR/search overlays. Their fonts, sizes and colors are metadata, not proof of visible editable typography.',
                'Text outlines appear as vector paths; raster lettering appears in images. These cannot be identified as a font solely by this report.',
                'Hex values quantize PDF-extracted RGB to 8-bit. Transparency, blending, color profiles and backgrounds can change the rendered appearance.',
                'A raw fill color with opacity below 1 is not an observed opaque swatch. Retain opacity and background, or sample the actual rendered region. Overlapping/translucent objects cannot be reduced to one reliable color by a general white-background formula.',
                'Implausible raw stroke widths can result from unreconciled PDF transforms. Flagged widths are not measurements in points and are excluded from stroke summaries; they never expand the crop-selection bounds.',
                'Vector selection uses intersecting path bounds (expanded by half stroke width), not full clipping/occlusion evaluation. Paths crossing the crop retain full-object bounds.',
                'Clip/group metadata is recorded when supported, but composite visibility is not reconstructed. Counts can include clipped or obscured paths.',
                'Path counts include outlined glyphs and are not palette area or importance. Character counts may double-count fill-plus-stroke rendering.',
                'Text is in PDF paint order; inferred spaces and reading order are not added. A trace may contain only one character.',
                'Measured point sizes describe source-paper placement, not a recommended production size or a corporate house style.',
                'Source objects and figures must be visually inspected before drawing aesthetic conclusions. No quality score is inferred.',
            ],
        }
        if preview:
            preview.parent.mkdir(parents=True, exist_ok=True)
            page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), clip=clip,
                            colorspace=fitz.csRGB, alpha=False, annots=False).save(preview)
            report['preview'] = {'path': str(preview.resolve()), 'dpi': dpi, 'orientation': 'unrotated',
                                 'sha256': digest(preview)}
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--page', type=int, required=True, help='1-based PDF page')
    parser.add_argument('--clip', type=float, nargs=4, required=True, metavar=('X0', 'Y0', 'X1', 'Y1'),
                        help='Figure-region bounds in unrotated page points, top-left origin')
    parser.add_argument('--out', type=Path, required=True, help='JSON measurement report')
    parser.add_argument('--preview', type=Path, help='Optional PNG of exactly the selected region')
    parser.add_argument('--dpi', type=float, default=216, help='Preview resolution, default 216')
    args = parser.parse_args()
    try:
        r = inspect_pdf(args.pdf, args.page, args.clip, args.out, args.preview, args.dpi)
    except Exception as error:
        print(f'Style inspection failed: {error}', file=sys.stderr)
        return 2
    print(json.dumps({'output': str(args.out), 'text_trace_counts': r['text']['counts'],
                      'vector_paths': r['vector']['path_count'], 'raster_occurrences': r['raster']['occurrence_count'],
                      'status': 'Measured; visual review and interpretation still required.'}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
