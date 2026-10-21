"""Small, auditable Matplotlib helpers for publication figures.

Use dimensions at their final printed size. Export never tight-crops the canvas.
The helper validates geometry and provenance; it cannot validate scientific claims.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
from matplotlib.text import Text

PALETTE = {
    "focus": "#0072B2",
    "reference": "#6B7280",
    "alternative": "#D55E00",
    "teal": "#009E73",
    "purple": "#CC79A7",
    "ink": "#20252B",
    "grid": "#DDE2E7",
}


def style_context(font_size=8.0):
    """Return a scoped rc_context; do not change process-wide plotting defaults."""
    if not np.isfinite(font_size) or font_size <= 0.5:
        raise ValueError("font_size must be finite and greater than 0.5 points")
    return mpl.rc_context({
        "font.family": "DejaVu Sans",
        "font.size": font_size,
        "axes.labelsize": font_size,
        "axes.titlesize": font_size,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.labelcolor": PALETTE["ink"],
        "text.color": PALETTE["ink"],
        "xtick.color": PALETTE["ink"],
        "ytick.color": PALETTE["ink"],
        "axes.edgecolor": PALETTE["reference"],
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.axisbelow": True,
        "axes.grid": False,
        "axes.prop_cycle": cycler(color=[PALETTE[k] for k in
                                          ("focus", "reference", "alternative", "teal", "purple")]),
        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.5,
        "grid.alpha": 0.8,
        "lines.linewidth": 1.25,
        "lines.markersize": 3.5,
        "xtick.labelsize": font_size - 0.5,
        "ytick.labelsize": font_size - 0.5,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "legend.fontsize": font_size - 0.5,
        "legend.frameon": False,
        "legend.handlelength": 1.6,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.transparent": False,
        "savefig.bbox": None,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "cs-paper-figure",
    })


def make_figure(width_mm=85, height_mm=60, nrows=1, ncols=1, **kwargs):
    """Return (figure, axes) from plt.subplots at exact physical dimensions.

    Additional subplots options such as sharex, sharey, squeeze, and gridspec_kw
    are supported. Physical size and constrained layout are intentionally fixed.
    """
    sizes = np.asarray([width_mm, height_mm], dtype=float)
    if not np.all(np.isfinite(sizes)) or np.any(sizes <= 0):
        raise ValueError("width_mm and height_mm must be positive and finite")
    reserved = {"figsize", "layout", "constrained_layout"}.intersection(kwargs)
    if reserved:
        raise ValueError(f"Set physical size using width_mm/height_mm; reserved: {sorted(reserved)}")
    return plt.subplots(nrows=nrows, ncols=ncols, figsize=tuple(sizes / 25.4),
                        layout="constrained", **kwargs)


def validate_intervals(y, lo, hi):
    """Return float arrays after validating finite values and ordered endpoints.

    An estimate need not lie inside an interval. Draw points and endpoints
    separately instead of forcing invalid negative Matplotlib error lengths.
    """
    values = tuple(np.asarray(v, dtype=float) for v in (y, lo, hi))
    if not (values[0].shape == values[1].shape == values[2].shape):
        raise ValueError("estimate, lower, and upper arrays must have identical shapes")
    if not all(np.all(np.isfinite(v)) for v in values):
        raise ValueError("estimate and interval arrays must contain only finite values")
    if np.any(values[1] > values[2]):
        raise ValueError("every interval must satisfy lower <= upper")
    return values


def _text_outside_canvas(fig):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    canvas = fig.bbox
    tolerance = 0.75  # rendering-roundoff tolerance, in display pixels
    # Locators retain extra ticks beyond view limits. Their Text artists can
    # report visible=True although Axis.draw does not paint them. Match the
    # transformed-view selection (including log and inverted axes), without
    # excluding in-range tick labels that really extend outside the canvas.
    undrawn_tick_labels = set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            transform = axis.get_transform()
            bounds = np.sort(np.asarray(transform.transform(axis.get_view_interval()), dtype=float))
            slippage = (bounds[1] - bounds[0]) * 1e-10
            for tick in (*axis.get_major_ticks(), *axis.get_minor_ticks()):
                location = float(np.asarray(transform.transform([tick.get_loc()]))[0])
                if (not ax.get_visible() or not axis.get_visible() or not np.isfinite(location)
                        or not bounds[0] - slippage <= location <= bounds[1] + slippage):
                    undrawn_tick_labels.update((id(tick.label1), id(tick.label2)))
    failures = []
    for item in fig.findobj(match=Text):
        if (id(item) in undrawn_tick_labels or not item.get_visible()
                or not item.get_text().strip() or item.get_alpha() == 0):
            continue
        box = item.get_window_extent(renderer=renderer)
        if not np.all(np.isfinite(box.extents)):
            failures.append({"text": item.get_text()[:100], "reason": "nonfinite bounds"})
        elif (box.x0 < canvas.x0 - tolerance or box.y0 < canvas.y0 - tolerance
              or box.x1 > canvas.x1 + tolerance or box.y1 > canvas.y1 + tolerance):
            failures.append({"text": item.get_text()[:100],
                             "bounds_px": [round(float(v), 2) for v in box.extents]})
    return failures


def export_figure(fig, output_stem, *, source_files=(), metadata=None, dpi=300):
    """Write PDF, editable-text SVG, PNG, and a source-hashed JSON manifest.

    Raise before writing when metadata, sources, or visible text geometry are
    invalid. This check does not detect all overlaps or scientific errors; inspect
    rendered PDF/SVG at final size. Return output paths keyed by format.
    """
    if not np.isfinite(dpi) or dpi <= 0:
        raise ValueError("dpi must be positive and finite")
    metadata = {} if metadata is None else metadata
    json.dumps(metadata, allow_nan=False)  # fail before writing any output
    sources = []
    for source in source_files:
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError(f"Missing figure source file: {path}")
        sources.append({"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "bytes": path.stat().st_size})
    failures = _text_outside_canvas(fig)
    if failures:
        raise ValueError("Visible text extends outside the fixed canvas. Resize/reflow before export: "
                         + json.dumps(failures, ensure_ascii=False))
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    paths = {fmt: str(stem) + "." + fmt for fmt in ("pdf", "svg", "png")}
    paths["manifest"] = str(stem) + ".manifest.json"
    if any(Path(p).resolve() == Path(s["path"]).resolve()
           for p in paths.values() for s in sources):
        raise ValueError("An output would overwrite an input source")
    with mpl.rc_context({"pdf.fonttype": 42, "svg.fonttype": "none",
                         "svg.hashsalt": "cs-paper-figure", "savefig.bbox": None}):
        fig.savefig(paths["pdf"], facecolor="white", transparent=False,
                    metadata={"Creator": "cs-paper-figure", "CreationDate": None,
                              "ModDate": None})
        fig.savefig(paths["svg"], facecolor="white", transparent=False,
                    metadata={"Creator": "cs-paper-figure", "Date": None})
        fig.savefig(paths["png"], dpi=dpi, facecolor="white", transparent=False,
                    metadata={"Software": "cs-paper-figure"})
    width_in, height_in = map(float, fig.get_size_inches())
    manifest = {
        "schema_version": 1,
        "dimensions": {"width_mm": round(width_in * 25.4, 8),
                       "height_mm": round(height_in * 25.4, 8), "png_dpi": float(dpi)},
        "dependencies": {"python": platform.python_version(), "matplotlib": mpl.__version__,
                         "numpy": np.__version__},
        "sources": sources,
        "metadata": metadata,
        "geometry_check": {"out_of_canvas_text": [],
                           "scope": "canvas containment only; manually inspect overlap and scientific fidelity"},
        "outputs": {k: {"path": p, "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
                    for k, p in paths.items() if k != "manifest"},
    }
    Path(paths["manifest"]).write_text(json.dumps(manifest, indent=2, ensure_ascii=False,
                                                 allow_nan=False) + "\n", encoding="utf-8")
    return paths
