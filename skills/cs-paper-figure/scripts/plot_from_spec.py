#!/usr/bin/env python3
"""Render four scientific chart families from a validated, explicit JSON spec."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
import textwrap

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import LogFormatter

from figure_style import (
    PALETTE, export_figure, make_figure, style_context, validate_intervals,
)


KINDS = {"curve", "interval", "tradeoff", "heatmap"}
ROLES = ("focus", "reference", "alternative", "teal", "purple")
COMMON = {"kind", "title", "claim", "x", "y", "data_status", "provenance", "size"}
SPECIFIC = {
    "curve": {"series", "interval_semantics"},
    "interval": {"items", "reference", "interval_semantics"},
    "tradeoff": {"points", "frontier"},
    "heatmap": {"rows", "columns", "values", "colorbar", "zero_center", "annotate"},
}


def fail(message):
    raise ValueError(message)


def fields(obj, allowed, required, where):
    if not isinstance(obj, dict):
        fail(f"{where} must be an object")
    missing, extra = set(required) - obj.keys(), obj.keys() - set(allowed)
    if missing:
        fail(f"{where}: missing {', '.join(sorted(missing))}")
    if extra:
        fail(f"{where}: unsupported field(s) {', '.join(sorted(extra))}")


def string(value, where):
    if not isinstance(value, str) or not value.strip():
        fail(f"{where} must be a nonempty string")
    return value.strip()


def number(value, where):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail(f"{where} must be a finite number")
    try:
        result = float(value)
    except (OverflowError, ValueError):
        fail(f"{where} must be a finite number")
    if not math.isfinite(result):
        fail(f"{where} must be a finite number")
    return result


def boolean(value, where):
    if not isinstance(value, bool):
        fail(f"{where} must be true or false")
    return value


def sequence(value, where):
    if not isinstance(value, list) or not value:
        fail(f"{where} must be a nonempty array")
    return value


def unique(labels, where):
    if len(labels) != len(set(labels)):
        fail(f"{where} contains duplicate labels or coordinates")


def numbers(values, where):
    return np.asarray([number(v, f"{where}[{i}]")
                       for i, v in enumerate(sequence(values, where))], dtype=float)


def axis(obj, where, kind):
    fields(obj, {"label", "unit", "scale", "direction"}, {"label", "unit"}, where)
    string(obj["label"], f"{where}.label")
    string(obj["unit"], f"{where}.unit")
    scale = obj.get("scale", "linear")
    if not isinstance(scale, str) or scale not in {"linear", "log"}:
        fail(f"{where}.scale must be linear or log")
    if kind == "tradeoff":
        direction = obj.get("direction")
        if not isinstance(direction, str) or direction not in {"minimize", "maximize"}:
            fail(f"{where}.direction must explicitly be minimize or maximize")
    elif "direction" in obj:
        fail(f"{where}.direction is supported only for tradeoff charts")
    if (kind == "heatmap" or (kind == "interval" and where == "y")) and scale != "linear":
        fail(f"{where}: this categorical axis must use linear scale")


def positive_for_log(values, axis_spec, where):
    if axis_spec.get("scale", "linear") == "log" and np.any(np.asarray(values) <= 0):
        fail(f"{where}: log axes require strictly positive observations and interval endpoints")


def role(obj, i):
    value = obj.get("role", ROLES[i % len(ROLES)])
    if not isinstance(value, str) or value not in ROLES:
        fail(f"role must be one of {', '.join(ROLES)}")
    return value


def intervals(obj, estimates, where):
    lo = numbers(obj["lower"], where + ".lower")
    hi = numbers(obj["upper"], where + ".upper")
    if len(lo) != len(estimates) or len(hi) != len(estimates):
        fail(f"{where}: estimate and interval lengths must match")
    if np.any(lo > hi):
        fail(f"{where}: lower endpoint exceeds upper endpoint")
    validate_intervals(estimates, lo, hi)
    return lo, hi


def validate(spec):
    if not isinstance(spec, dict):
        fail("spec must be an object")
    kind = spec.get("kind")
    if not isinstance(kind, str) or kind not in KINDS:
        fail("kind must be curve, interval, tradeoff, or heatmap")
    fields(spec, COMMON | SPECIFIC[kind],
           {"kind", "x", "y", "data_status", "provenance"}, "spec")
    if not any(k in spec for k in ("title", "claim")):
        fail("provide title or claim")
    for key in ("title", "claim", "provenance"):
        if key in spec:
            string(spec[key], key)
    if not isinstance(spec["data_status"], str) or spec["data_status"] not in {"measured", "reported", "illustrative"}:
        fail("data_status must be measured, reported, or illustrative")
    for key in ("x", "y"):
        axis(spec[key], key, kind)
    if "size" in spec:
        fields(spec["size"], {"width_mm", "height_mm", "font_size"}, set(), "size")
        for key, val in spec["size"].items():
            if number(val, "size." + key) <= 0:
                fail(f"size.{key} must be positive")
            if key == "font_size" and val <= .5:
                fail("size.font_size must exceed 0.5 pt; use at least 7 pt for normal print labels")

    has_intervals = False
    if kind == "curve":
        series = sequence(spec.get("series"), "series")
        labels = []
        for i, item in enumerate(series):
            where = f"series[{i}]"
            fields(item, {"label", "x", "y", "lower", "upper", "role"},
                   {"label", "x", "y"}, where)
            labels.append(string(item["label"], where + ".label"))
            role(item, i)
            x, y = numbers(item["x"], where + ".x"), numbers(item["y"], where + ".y")
            if len(x) != len(y):
                fail(f"{where}: x and y lengths must match")
            if len(x) > 1 and np.any(np.diff(x) <= 0):
                fail(f"{where}.x must be strictly increasing; duplicate x values are not allowed")
            positive_for_log(x, spec["x"], where + ".x")
            positive_for_log(y, spec["y"], where + ".y")
            if ("lower" in item) != ("upper" in item):
                fail(f"{where}: supply both lower and upper")
            if "lower" in item:
                lo, hi = intervals(item, y, where)
                positive_for_log(np.r_[lo, hi], spec["y"], where + ".interval")
                has_intervals = True
        unique(labels, "series")
    elif kind == "interval":
        labels = []
        for i, item in enumerate(sequence(spec.get("items"), "items")):
            where = f"items[{i}]"
            fields(item, {"label", "estimate", "lower", "upper", "role"},
                   {"label", "estimate", "lower", "upper"}, where)
            labels.append(string(item["label"], where + ".label"))
            role(item, i)
            y, lo, hi = (number(item[k], where + "." + k)
                         for k in ("estimate", "lower", "upper"))
            if lo > hi:
                fail(f"{where}: lower endpoint exceeds upper endpoint")
            validate_intervals([y], [lo], [hi])
            positive_for_log([y, lo, hi], spec["x"], where)
        unique(labels, "items")
        if "reference" in spec:
            ref = number(spec["reference"], "reference")
            if ref not in (0, 1):
                fail("reference must be 0 or 1 (a null comparison value)")
            positive_for_log([ref], spec["x"], "reference")
        has_intervals = True
    elif kind == "tradeoff":
        labels = []
        boolean(spec.get("frontier", False), "frontier")
        for i, item in enumerate(sequence(spec.get("points"), "points")):
            where = f"points[{i}]"
            fields(item, {"label", "x", "y", "role"}, {"label", "x", "y"}, where)
            labels.append(string(item["label"], where + ".label"))
            role(item, i)
            for key in ("x", "y"):
                val = number(item[key], where + "." + key)
                positive_for_log([val], spec[key], where + "." + key)
        unique(labels, "points")
    else:
        for key in ("rows", "columns"):
            vals = [string(v, key) for v in sequence(spec.get(key), key)]
            unique(vals, key)
        rows, columns = spec["rows"], spec["columns"]
        matrix = sequence(spec.get("values"), "values")
        if len(matrix) != len(rows):
            fail("values: row count does not match rows")
        observed = []
        for i, row in enumerate(matrix):
            sequence(row, f"values[{i}]")
            if len(row) != len(columns):
                fail(f"values[{i}]: column count does not match columns")
            observed += [number(v, f"values[{i}]") for v in row if v is not None]
        if not observed:
            fail("values must contain at least one observed numeric cell")
        fields(spec.get("colorbar"), {"label", "unit"}, {"label", "unit"}, "colorbar")
        string(spec["colorbar"]["label"], "colorbar.label")
        string(spec["colorbar"]["unit"], "colorbar.unit")
        boolean(spec.get("zero_center", False), "zero_center")
        boolean(spec.get("annotate", False), "annotate")
        if spec.get("zero_center") and max(abs(v) for v in observed) == 0:
            fail("zero_center requires a nonzero observation; omit it for an all-zero matrix")
    if has_intervals:
        string(spec.get("interval_semantics"), "interval_semantics")
    elif "interval_semantics" in spec:
        fail("interval_semantics was supplied without intervals")
    return spec


def observed_nondominated(points, x_direction, y_direction):
    """Return all nondominated indices, preserving every exact-coordinate tie."""
    values = np.asarray([[p["x"], p["y"]] for p in points], dtype=float)
    values *= np.asarray([1 if d == "minimize" else -1
                          for d in (x_direction, y_direction)])
    return [i for i, point in enumerate(values)
            if not np.any(np.all(values <= point, axis=1) & np.any(values < point, axis=1))]


def label(axis_spec, direction=False):
    text = axis_spec["label"].strip()
    if axis_spec["unit"].strip() != "unitless":
        text += " (" + axis_spec["unit"].strip() + ")"
    if axis_spec.get("scale") == "log":
        text += " [log scale]"
    if direction:
        text += " ↓" if axis_spec["direction"] == "minimize" else " ↑"
    return text


def render(spec, input_path, output_stem):
    kind, size = spec["kind"], spec.get("size", {})
    width, height, font = (size.get("width_mm", 85), size.get("height_mm", 65),
                           size.get("font_size", 8))
    meta = {k: spec[k] for k in ("kind", "title", "claim", "data_status", "provenance", "interval_semantics")
            if k in spec}
    meta["transformations"] = {"aggregation": "none", "smoothing": "none", "fitting": "none"}
    with style_context(font_size=font):
        fig, ax = make_figure(width_mm=width, height_mm=height)
        title = spec.get("title", spec.get("claim"))
        fig.suptitle(textwrap.fill(title, max(26, int(width * 0.48))),
                     fontsize=font + 1, fontweight="semibold")
        if spec["data_status"] == "illustrative":
            fig.supxlabel("ILLUSTRATIVE DATA", fontsize=max(7, font - 1), color=PALETTE["ink"])
        ax.set_xlabel(label(spec["x"], kind == "tradeoff"))
        ax.set_ylabel(label(spec["y"], kind == "tradeoff"))
        ax.set_xscale(spec["x"].get("scale", "linear"))
        ax.set_yscale(spec["y"].get("scale", "linear"))
        for key, axis_obj in (("x", ax.xaxis), ("y", ax.yaxis)):
            if spec[key].get("scale") == "log":
                # Compact plain notation avoids overlapping 2 x 10^0 labels
                # and tiny superscripts in a one-column figure.
                axis_obj.set_major_formatter(LogFormatter())
                axis_obj.set_minor_formatter(LogFormatter())
        if kind == "curve":
            for i, item in enumerate(spec["series"]):
                color = PALETTE[role(item, i)]
                if "lower" in item:
                    ax.fill_between(item["x"], item["lower"], item["upper"], color=color, alpha=.16, linewidth=0)
                ax.plot(item["x"], item["y"], color=color,
                        linestyle=("-", "--", ":", "-.")[i % 4],
                        marker=("o", "s", "^", "D", "v", "P", "X")[i % 7],
                        markersize=3.5, linewidth=1.25, label=item["label"])
            ax.legend(loc="best", frameon=False)
            ax.margins(x=.04, y=.12)
        elif kind == "interval":
            for i, item in enumerate(spec["items"]):
                color = PALETTE[role(item, i)]
                ax.hlines(i, item["lower"], item["upper"], color=color, linewidth=1.4)
                ax.vlines([item["lower"], item["upper"]], i - .09, i + .09, color=color, linewidth=1)
                ax.plot(item["estimate"], i, "o", color=color, markersize=4)
            ax.set_yticks(range(len(spec["items"])), [item["label"] for item in spec["items"]])
            ax.set_ylim(len(spec["items"]) - .5, -.5)
            if "reference" in spec:
                ax.axvline(spec["reference"], color=PALETTE["reference"], linestyle="--", linewidth=.8, zorder=0)
            ax.margins(x=.12)
        elif kind == "tradeoff":
            points = spec["points"]
            for i, point in enumerate(points):
                ax.scatter(point["x"], point["y"], color=PALETTE[role(point, i)], s=26, zorder=3)
            groups = {}
            for point in points:
                groups.setdefault((point["x"], point["y"]), []).append(point["label"])
            for (x, y), names in groups.items():
                ax.annotate(" / ".join(names), (x, y), xytext=(5, 5), textcoords="offset points",
                            fontsize=font, color=PALETTE["ink"])
            ax.margins(x=.3, y=.3)
            if spec.get("frontier", False):
                inds = observed_nondominated(points, spec["x"]["direction"], spec["y"]["direction"])
                coords = sorted({(points[i]["x"], points[i]["y"]) for i in inds})
                ax.scatter([p[0] for p in coords], [p[1] for p in coords], s=64,
                           facecolors="none", edgecolors=PALETTE["ink"], linewidths=1,
                           label="Observed nondominated", zorder=4)
                ax.legend(loc="best", frameon=False, fontsize=max(7, font - 1))
                meta["observed_nondominated_labels"] = [points[i]["label"] for i in inds]
                meta["frontier_scope"] = "supplied observations only; no interpolation or uncertainty dominance"
        else:
            data = np.asarray([[np.nan if v is None else v for v in row] for row in spec["values"]], dtype=float)
            missing = ~np.isfinite(data)
            cmap = plt.get_cmap("RdBu_r" if spec.get("zero_center") else "viridis").copy()
            cmap.set_bad("#E8E8E8")
            options = {}
            if spec.get("zero_center"):
                extent = np.nanmax(np.abs(data))
                options = {"vmin": -extent, "vmax": extent}
            image = ax.imshow(np.ma.masked_invalid(data), cmap=cmap, aspect="auto", interpolation="nearest", **options)
            ax.set_xticks(range(len(spec["columns"])), spec["columns"], rotation=35, ha="right")
            ax.set_yticks(range(len(spec["rows"])), spec["rows"])
            for i, j in np.ndindex(data.shape):
                if missing[i, j]:
                    ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, facecolor="none", edgecolor="#999999", hatch="///", linewidth=0))
                    ax.text(j, i, "NA", ha="center", va="center", color=PALETTE["ink"], fontsize=font)
                elif spec.get("annotate", False):
                    rgba = image.cmap(image.norm(data[i, j]))
                    luminance = sum(a * b for a, b in zip(rgba[:3], (.2126, .7152, .0722)))
                    ax.text(j, i, f"{data[i, j]:.3g}", ha="center", va="center",
                            color="white" if luminance < .5 else PALETTE["ink"], fontsize=font)
            colorbar = fig.colorbar(image, ax=ax, fraction=.08, pad=.04)
            colorbar.set_label(label(spec["colorbar"]))
            ax.grid(False)
            meta["missing_cell_count"] = int(missing.sum())
            meta["color_scale"] = "symmetric around zero" if spec.get("zero_center") else "sequential"
        try:
            return export_figure(fig, output_stem,
                                 source_files=(input_path, Path(__file__), Path(__file__).with_name("figure_style.py")),
                                 metadata=meta)
        finally:
            plt.close(fig)


def unique_json_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            fail(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="UTF-8 JSON file; see references/spec-format.md")
    parser.add_argument("--out", type=Path, required=True, help="output filename stem for PDF, SVG, PNG, and manifest")
    args = parser.parse_args(argv)
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"), object_pairs_hook=unique_json_object,
                          parse_constant=lambda value: fail(f"nonfinite JSON value: {value}"))
        files = render(validate(spec), args.spec, args.out)
        print(json.dumps({k: str(v) for k, v in files.items()}, indent=2))
        return 0
    except (ValueError, TypeError, OSError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
