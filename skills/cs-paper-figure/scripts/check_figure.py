#!/usr/bin/env python3
"""Check PDF dimensions, text bounds, font sizes, and font embedding with PyMuPDF."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys


LIMITATIONS = (
    "Automated checks cannot certify absence of overlaps, statistical correctness, scientific validity, "
    "color accessibility, or legibility of rasterized/outlined text. Visually inspect the final-size PDF."
)


def check_pdf(path, expected_width_mm=None, min_font_pt=7, width_tolerance_mm=.5):
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is unavailable; install pymupdf to run these optional PDF checks") from exc
    result = {
        "file": str(path), "min_font_pt": min_font_pt,
        "expected_width_mm": expected_width_mm,
        "width_tolerance_mm": width_tolerance_mm,
        "pages": [], "fonts": [], "limitations": LIMITATIONS,
    }
    seen_fonts, issue_count = {}, 0
    with fitz.open(path) as document:
        if not document.is_pdf:
            raise ValueError("input must be a PDF")
        if document.needs_pass:
            raise ValueError("encrypted PDF requires a decrypted copy for inspection")
        if not len(document):
            raise ValueError("PDF has no pages")
        for i, page in enumerate(document):
            rect = page.rect
            unrotated = rect * page.derotation_matrix
            page_result = {
                "page": i + 1, "width_mm": round(rect.width * 25.4 / 72, 3),
                "height_mm": round(rect.height * 25.4 / 72, 3),
                "rotation": page.rotation, "text_span_count": 0,
                "small_text": [], "out_of_page_text": [],
            }
            width_ok = expected_width_mm is None or abs(rect.width * 25.4 / 72 - expected_width_mm) <= width_tolerance_mm
            page_result["width_within_tolerance"] = width_ok
            issue_count += int(not width_ok)
            # Default extraction clips to the page and can hide the very overflow
            # this check needs to report. Inspect text beyond the crop boundary.
            for block in page.get_text("dict", clip=fitz.INFINITE_RECT())["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if not span.get("text", "").strip():
                            continue
                        page_result["text_span_count"] += 1
                        record = {"text": span["text"], "size_pt": round(span["size"], 3),
                                  "font": span["font"], "bbox_pt": [round(v, 3) for v in span["bbox"]]}
                        if span["size"] < min_font_pt - .001:
                            page_result["small_text"].append(record)
                            issue_count += 1
                        x0, y0, x1, y1 = span["bbox"]
                        if (x0 < unrotated.x0 - .25 or y0 < unrotated.y0 - .25 or
                                x1 > unrotated.x1 + .25 or y1 > unrotated.y1 + .25):
                            page_result["out_of_page_text"].append(record)
                            issue_count += 1
            if page_result["text_span_count"] == 0:
                page_result["text_check_note"] = "No extractable text; font-size and text-bounds checks are inconclusive"
                issue_count += 1
            for font in page.get_fonts(full=True):
                xref, ext, kind, basefont, name = font[:5]
                key = (xref, basefont, kind)
                if key in seen_fonts:
                    seen_fonts[key]["pages"].append(i + 1)
                    continue
                embedded = None
                detail = ""
                program_format_warning = None
                if kind == "Type3":
                    detail = "Type3 glyph streams require separate inspection; extraction cannot verify embedding"
                elif xref == 0:
                    embedded = False
                    detail = "No embedded font resource"
                else:
                    try:
                        extracted = document.extract_font(xref)
                        embedded = bool(extracted[3])
                        detail = "Embedded font program found" if embedded else "No extractable embedded font program"
                        if embedded and extracted[1] == "ttf" and extracted[3][:4] == b"OTTO":
                            program_format_warning = "Font is declared/extracted as TrueType but its program has an OpenType/CFF signature; check backend/font compatibility and external PDF rendering."
                            detail += "; " + program_format_warning
                    except Exception as exc:
                        detail = "Embedding inspection unavailable: " + type(exc).__name__
                font_result = {"xref": xref, "name": basefont, "type": kind,
                               "embedded": embedded, "detail": detail,
                               "program_format_warning": program_format_warning, "pages": [i + 1]}
                seen_fonts[key] = font_result
                if embedded is not True:
                    issue_count += 1
                if program_format_warning:
                    issue_count += 1
            result["pages"].append(page_result)
        result["fonts"] = list(seen_fonts.values())
    result["issue_count"] = issue_count
    result["automated_checks_passed"] = issue_count == 0
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog=LIMITATIONS)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--expected-width-mm", type=float)
    parser.add_argument("--min-font-pt", type=float, default=7)
    parser.add_argument("--width-tolerance-mm", type=float, default=.5)
    parser.add_argument("--json", type=Path, dest="json_path", help="also save the complete report as JSON")
    args = parser.parse_args(argv)
    try:
        for key in ("expected_width_mm", "min_font_pt", "width_tolerance_mm"):
            value = getattr(args, key)
            if value is not None and (not math.isfinite(value) or value <= 0):
                raise ValueError(key.replace("_", "-") + " must be positive and finite")
        report = check_pdf(args.pdf, args.expected_width_mm, args.min_font_pt, args.width_tolerance_mm)
        if args.json_path:
            args.json_path.parent.mkdir(parents=True, exist_ok=True)
            args.json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        for page in report["pages"]:
            print(f"Page {page['page']}: {page['width_mm']:.3f} x {page['height_mm']:.3f} mm; "
                  f"width {'OK' if page['width_within_tolerance'] else 'MISMATCH'}; "
                  f"{len(page['small_text'])} text spans below {args.min_font_pt:g} pt; "
                  f"{len(page['out_of_page_text'])} text spans outside page")
            if "text_check_note" in page:
                print("  " + page["text_check_note"])
        for font in report["fonts"]:
            print(f"Font {font['name']} ({font['type']}): {font['detail']}")
        print(f"Automated findings: {report['issue_count']}. {LIMITATIONS}")
        return 0 if report["automated_checks_passed"] else 1
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
