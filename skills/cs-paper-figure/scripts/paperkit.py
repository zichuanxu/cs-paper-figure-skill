"""paperkit: premium vector primitives for CS paper figures (matplotlib, mm units).

The canvas uses millimetres with the origin at the bottom-left, so every size in
code is the printed size. Text sizes are points, stroke widths are points.

    from paperkit import Canvas, ROLE
    cv = Canvas(170, 100)                       # final printed size
    cv.group(2, 40, 60, 58, "memory", "Native Memory Block")
    cv.box(6, 70, 24, 9, "frozen", "Original Attention", icon="snow")
    cv.matrix(40, 60, 14, 12, rows=5, cols=6, depth=3, r="memory")
    cv.arrow([(30, 74.5), (40, 74.5)])
    cv.save("out/figure")                       # .pdf (Type 42) + .svg + .png

Design rules (references/visual-craft.md; per-register rules in references/registers.md):
* the page is the ground: section frames have white fields, tints are opt-in and mean scope;
* role colours come as (fill, soft, stroke, ink, mark) families for the plate register;
  ROLE["line"] is white with a black stroke for line art; SERIES_STYLE gives chart series a hue
  plus a marker, dash and hatch so they survive greyscale;
* corner radius scales with box height; arrows are dark neutral by default, coloured only when
  colour encodes a path type; heads are filled, 3-6 x the stroke;
* glyphs (matrices, token strips, documents, listings, marked spans) carry the content so that
  boxes need fewer words;
* audits: cv.overlaps(), cv.text_overlaps() (canvas and chart text, icons, edge clipping),
  cv.wire_crossings(); command line: density, grey, compare, parity, swatches, caption.
"""
from __future__ import annotations

import math
import os
import re
from pathlib import Path as _P

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import colors as mcolors  # noqa: E402
from matplotlib.patches import (Arc, Circle, Ellipse, FancyArrowPatch,  # noqa: E402
                                FancyBboxPatch, PathPatch, Polygon, Rectangle, Wedge)
from matplotlib.path import Path  # noqa: E402

MM = 1 / 25.4
PT_PER_MM = 72 / 25.4

# ---------------------------------------------------------------- palette ---
# fill (L*~95-97), soft (L*~88-90, header bands / chips), stroke (L*~55-65),
# ink (L*~25-35, text on fill), mark (saturated, for data / hero marks).
ROLE = {
    "neutral": dict(fill="#F4F5F7", soft="#E6E8EC", stroke="#8C95A1", ink="#3A4250", mark="#7D8794"),
    "frozen":  dict(fill="#EEF2F8", soft="#DCE4EF", stroke="#7A8DA8", ink="#34445C", mark="#6F84A3"),
    "blue":    dict(fill="#EAF1FB", soft="#D3E2F6", stroke="#5B8AC9", ink="#1F4E8C", mark="#2F6FC0"),
    "memory":  dict(fill="#E9F4EC", soft="#CFE6D6", stroke="#4E9166", ink="#1E5B36", mark="#2E8B57"),
    "amber":   dict(fill="#FFF4E3", soft="#FCE3BD", stroke="#D49A45", ink="#7A4A0E", mark="#E08A1E"),
    "purple":  dict(fill="#F3EEFA", soft="#E2D8F3", stroke="#9479C4", ink="#4B2F80", mark="#7A54C2"),
    "teal":    dict(fill="#E7F5F5", soft="#C9E8E8", stroke="#4FA3A5", ink="#175E60", mark="#1F8A8C"),
    "coral":   dict(fill="#FDEEEA", soft="#F8D6CC", stroke="#D9826B", ink="#86321F", mark="#D9583B"),
    "rose":    dict(fill="#FBEFF4", soft="#F3D5E2", stroke="#C77D9C", ink="#7A2E50", mark="#C2507F"),
}
# "line": the line-art register of systems, PL and theory figures (references/venue-study-2026-11.md): white
# shapes, one black stroke weight, black text. Colour is then free for the one thing that is new or wrong.
ROLE["line"] = dict(fill="#FFFFFF", soft="#EFEFEF", stroke="#000000", ink="#000000", mark="#000000")
INK = "#262B33"      # body text
MUTED = "#6B7480"    # secondary text
LINE = "#4A4F57"     # default connector ink
HAIR = "#C9CED6"     # hairlines / grid


# Hue order for taxonomy series: maximally distinct neighbours, colour-blind-safe enough with labels.
SERIES_ORDER = ("memory", "blue", "purple", "amber", "coral", "teal", "rose", "frozen")


# Chart series with two channels each (hue + marker + dash + hatch), so a chart with many systems survives
# greyscale printing and colour-vision deficiency. Index 0 is "ours": the only solid line and the only
# unhatched bar, listed first in the legend; every line has the same weight (measured in CortenMM Fig. 14,
# OSCAR Fig. 10; references/venue-study-2026-11.md). Hues are Okabe-Ito.
SERIES_STYLE = [
    dict(color="#D55E00", marker="^", ls="-", hatch=""),
    dict(color="#0072B2", marker="x", ls=(0, (5, 1.6, 1, 1.6)), hatch="////"),
    dict(color="#009E73", marker="d", ls=(0, (4, 2)), hatch="\\\\\\\\"),
    dict(color="#B8860B", marker="v", ls=(0, (1, 1.6)), hatch="...."),
    dict(color="#56B4E9", marker="+", ls=(0, (6, 1.6, 1, 1.6, 1, 1.6)), hatch="xxxx"),
    dict(color="#CC79A7", marker="s", ls=(0, (2, 2)), hatch="----"),
    dict(color="#555555", marker="o", ls=(0, (7, 2)), hatch="++++"),
]


def series_kw(k, kind="line", lw=0.9, ms=3.0):
    """Keyword arguments for series k of a chart: ax.plot(x, y, **series_kw(k)) or
    ax.bar(x, h, **series_kw(k, "bar")). Bars are a pale fill of the hue with a same-hue edge and hatch."""
    st = SERIES_STYLE[k % len(SERIES_STYLE)]
    if kind == "bar":
        return dict(fc=st["color"] if k == 0 else mix(st["color"], "#FFFFFF", 0.62), ec=st["color"], lw=0.6,
                    hatch=st["hatch"])
    return dict(color=st["color"], marker=st["marker"], ls=st["ls"], lw=lw, ms=ms, mew=0.8,
                mfc=st["color"] if k == 0 else "white")


def series(names, roles=None):
    """One colour family per taxonomy item, defined once and imported by every figure of the paper,
    so 'Agenda' is the same hue in the overview, the cycle, its chapter figure and the evaluation figure.
    Surveys that re-pick colours per figure (a common failure) make the reader relearn the legend."""
    roles = roles or SERIES_ORDER
    assert len(names) <= len(roles), "more items than distinct hues; group items or add roles"
    return {n: ROLE[r] for n, r in zip(names, roles)}


def role(r):
    return ROLE[r] if isinstance(r, str) else r


def mix(c1, c2, t):
    """Linear RGB mix, t=0 -> c1, t=1 -> c2."""
    a, b = np.array(mcolors.to_rgb(c1)), np.array(mcolors.to_rgb(c2))
    return mcolors.to_hex(a + (b - a) * t)


# ------------------------------------------------------------------ fonts ---
def use_fonts(family="serif"):
    """serif = Times-like text + STIX math (matches LaTeX/Times papers; STIXGeneral
    ships with matplotlib so this never falls back to DejaVu);
    sans = Helvetica/Arial when present, else DejaVu Sans."""
    from matplotlib import font_manager as fm
    names = {f.name for f in fm.fontManager.ttflist}
    if family == "serif":
        fam = [n for n in ("Times New Roman", "STIXGeneral", "Nimbus Roman") if n in names] or ["serif"]
        matplotlib.rcParams.update({"font.family": "serif", "font.serif": fam,
                                    "mathtext.fontset": "stix"})
    else:
        # only families that ship a real bold weight (macOS Helvetica.ttc is regular-only, so bold silently fails)
        bold = {f.name for f in fm.fontManager.ttflist if f.weight in (600, 700, "bold", "semibold")}
        fam = [n for n in ("Helvetica", "Arial", "Liberation Sans", "DejaVu Sans") if n in names and n in bold]
        matplotlib.rcParams.update({"font.family": "sans-serif", "font.sans-serif": fam,
                                    "mathtext.fontset": "stixsans"})
    matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
                                "axes.unicode_minus": False, "hatch.linewidth": 0.45})
    return fam[0]


# Export resolution for PNG and for images inside PDF/SVG; raster icons are pre-resampled to it so they stay crisp
RASTER_DPI = 600
MIN_SOURCE_DPI = 300  # below this a placed illustration is upsampled and prints soft


def pdf_images(pdf):
    """(width, height) in pixels of every image XObject in a PDF (soft masks included)."""
    import re
    b = _P(pdf).read_bytes()
    return [(int(w), int(h)) for w, h in re.findall(rb"/Subtype /Image[^>]*?/Width (\d+)[^>]*?/Height (\d+)", b)]


def check_embedded(pdf, rasters):
    """Fail the export if a placed raster is missing from the PDF at its full pixel size, i.e. it was
    resampled (to the figure dpi) or merged into a composite on the way out."""
    have = set(pdf_images(pdf))
    bad = [f"{os.path.basename(p)} {w}x{h}" for p, w, h in rasters if (w, h) not in have]
    if bad:
        raise RuntimeError(f"{pdf}: images not embedded at full resolution: {bad}; embedded sizes "
                           f"{sorted(have)[:8]}")


# ----------------------------------------------------------------- canvas ---
class Canvas:
    def __init__(self, width_mm, height_mm, family="serif", size=7.0):
        self.family = use_fonts(family)
        self.w, self.h, self.size = width_mm, height_mm, size
        self.fig = plt.figure(figsize=(width_mm * MM, height_mm * MM))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, width_mm)
        self.ax.set_ylim(0, height_mm)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.nodes = {}
        self.chips = []  # (x, y, w, h, label, region) of every chip, for the overlap audit
        self.rasters = []  # (path, px wide, px high) of every placed image, checked against the PDF on save
        self.solids = []  # (x, y, w, h, kind) of every opaque object, for wire_crossings()
        self.wires = []   # polyline points of every arrow / line, for wire_crossings()
        self.icons = []   # (x0, y0, x1, y1, kind) of every vector icon, for text_overlaps()
        self.spans = []   # (text, x0, x1, y) of every marked span set by rich / para, for thread()
        self._r = None
        self._rm = None  # export-resolution renderer, for text_width
        _add = self.ax.add_patch

        def add_patch(pp):  # bind the first patch drawn after a solid / wire is recorded, so audits follow moves
            for k, e in enumerate(self.solids):
                if e[-1] is None:
                    self.solids[k] = e[:-1] + (pp,)
            if self.wires and self.wires[-1][1] is None:
                self.wires[-1] = (self.wires[-1][0], pp)
            return _add(pp)
        self.ax.add_patch = add_patch

    def _renderer(self):
        if self._r is None:
            self.fig.canvas.draw()
            self._r = self.fig.canvas.get_renderer()
        return self._r

    def axes(self, x, y, w, h, **kw):
        """A data axes placed at (x, y, w, h) mm on the canvas (plot area, excluding tick labels)."""
        return chart_axes(self.fig.add_axes([x / self.w, y / self.h, w / self.w, h / self.h], **kw),
                          size=self.size)

    def axes_grid(self, x, y, w, h, rows, cols, gap=(7.0, 3.5), col_titles=None, row_titles=None,
                  xlabel=None, ylabel=None, sharex=True, sharey=False, box=True, grid="y", size=None):
        """Small multiples in mm: rows x cols plot areas inside (x, y, w, h), `gap` = (horizontal, vertical) mm
        between plot areas (3-4.5 mm with sharey=True, which keeps y tick labels on the first column only and
        gives every panel one y range; 7-9 mm when each panel has its own tick labels).
        Everything shared is said once: column titles on the top row, row titles rotated at the left, one y label
        for the grid, the x label under the bottom row only, inner x tick labels removed when sharex.
        Reserve room left of x for ticks, row titles and the y label (about 5 + 3.5 + 3.5 mm).
        Returns a rows x cols list of axes; add one frameless legend with chart_legend()."""
        size = size or self.size
        pw, ph = (w - (cols - 1) * gap[0]) / cols, (h - (rows - 1) * gap[1]) / rows
        axs = [[chart_axes(self.fig.add_axes([(x + c * (pw + gap[0])) / self.w,
                                              (y + (rows - 1 - r) * (ph + gap[1])) / self.h,
                                              pw / self.w, ph / self.h]), grid=grid, size=size, box=box)
                for c in range(cols)] for r in range(rows)]
        for r in range(rows):
            for c in range(cols):
                ax = axs[r][c]
                if r == 0 and col_titles:
                    ax.set_title(col_titles[c], fontsize=size, pad=2.0)
                if r < rows - 1 and sharex:
                    ax.tick_params(labelbottom=False)
                if sharey:
                    ax.sharey(axs[0][0]) if (r, c) != (0, 0) else None
                    ax.tick_params(labelleft=c == 0)
                if r == rows - 1 and xlabel:
                    ax.set_xlabel(xlabel, fontsize=size - 0.3, labelpad=1.5)
            if row_titles:
                self.text(x - 8.5, y + (rows - 1 - r) * (ph + gap[1]) + ph / 2, row_titles[r], size=size - 0.3,
                          rotation=90)
        if ylabel:
            self.text(max(1.8, x - (12.0 if row_titles else 8.5)), y + h / 2, ylabel, size=size - 0.3, rotation=90)
        return axs

    def chart_legend(self, handles, labels, x, y, ncol=None, size=None, loc="lower center", **kw):
        """One frameless legend row for a whole grid of axes, anchored at (x, y) mm: put it above the grid,
        the paper's own method first. Use ax.legend(frameon=False) instead when one panel has an empty corner."""
        return self.fig.legend(handles, labels, loc=loc, bbox_to_anchor=(x / self.w, y / self.h),
                               ncol=ncol or len(labels), frameon=False, fontsize=size or self.size - 0.3,
                               **{"handlelength": 2.6, "handletextpad": 0.5, "columnspacing": 1.4,
                                  "borderpad": 0, "borderaxespad": 0, **kw})

    # ---- text -------------------------------------------------------------
    def text(self, x, y, s, size=None, color=INK, weight="normal", ha="center", va="center",
             style="normal", z=20, **kw):
        return self.ax.text(x, y, s, fontsize=size or self.size, color=color, weight=weight,
                            ha=ha, va=va, style=style, zorder=z, **kw)

    def text_width(self, s, size, weight="normal", **kw):
        # measured at the export resolution: at the figure's 100 dpi, hinting makes a run about 0.7 % too wide,
        # and in rich() the error adds up to a visible gap before the punctuation that follows a marked span
        t = self.ax.text(0, 0, s, fontsize=size, weight=weight, **kw)
        x0, _, x1, _ = self._text_box(t)
        t.remove()
        return x1 - x0

    def _text_box(self, t):
        """(x0, y0, x1, y1) of a text artist in mm, laid out at the export resolution."""
        if self._rm is None:
            from matplotlib.backends.backend_agg import RendererAgg
            self._rm = RendererAgg(8, 8, RASTER_DPI)
        return tuple(v / RASTER_DPI * 25.4 for v in t.get_window_extent(self._rm, dpi=RASTER_DPI).extents)

    def rich(self, x, y, segments, size=None, ha="left", va="center", z=20, **kw):
        """Inline multi-colour text/math: segments = [(str, color[, weight[, mark]])].
        Use to colour-code terms of one equation by role, or to mark spans of example text: a 4th item (a role
        name or a colour) lays a borderless pale band behind that segment at 1.2 x the font size, the
        annotated-example highlight of HALoGEN Fig. 1. Pass family="monospace" for machine-written text.
        Every marked span is recorded in self.spans as (text, x0, x1, y), so a thread can be drawn from the
        span itself and never from a guessed x. Returns end x."""
        size = size or self.size
        widths = [self.text_width(s[0], size, s[2] if len(s) > 2 else "normal", **kw) for s in segments]
        cx = x - (sum(widths) if ha == "right" else sum(widths) / 2 if ha == "center" else 0)
        bh = 1.2 * size / PT_PER_MM
        for s, w in zip(segments, widths):
            if len(s) > 3 and s[3]:
                self.ax.add_patch(Rectangle((cx - 0.15, y - bh / 2), w + 0.3, bh, ec="none", zorder=z - 1,
                                            fc=ROLE[s[3]]["soft"] if s[3] in ROLE else s[3]))
                self.spans.append((s[0], cx, cx + w, y))
            # SVG viewers drop the leading spaces of a text element ("specialist" + " is" printed as
            # "specialistis"), so each run is drawn from its first glyph and the space becomes an offset
            wt = s[2] if len(s) > 2 else "normal"
            body = s[0].lstrip(" ")
            lead = w - self.text_width(body, size, wt, **kw) if body != s[0] else 0.0
            if body:
                self.text(cx + lead, y, body, size=size, color=s[1], weight=wt, ha="left", va=va, z=z, **kw)
            cx += w
        return cx

    def listing(self, x, y, lines, *, hi=None, start=1, size=None, numbers=True, leading=1.25, z=8):
        """Code, IR or a trace as a figure object: monospace lines from the top-left (x, y), grey right-aligned
        line numbers the text can cite, and hi={line number: role} full-width highlight bands (red/green for
        before/after, one accent for the line the claim is about). No background box and at most three
        colours in the code itself (CortenMM Fig. 6, NDD Fig. 2). Returns the height."""
        size = size or self.size - 0.3
        rh = leading * size / PT_PER_MM
        nx = self.text_width(str(start + len(lines) - 1), size - 0.6, family="monospace") + 1.2 if numbers else 0
        wmax = max(self.text_width(t, size, family="monospace") for t in lines)
        for i, t in enumerate(lines):
            cy = y - (i + 0.5) * rh
            if hi and (start + i) in hi:
                self.ax.add_patch(Rectangle((x + nx - 0.4, cy - rh / 2), wmax + 0.8, rh, ec="none",
                                            fc=role(hi[start + i])["soft"], zorder=z - 1))
            if numbers:
                self.text(x + nx - 1.2, cy, str(start + i), size=size - 0.6, color=MUTED, ha="right",
                          family="monospace", z=z)
            self.text(x + nx, cy, t, size=size, color="black", ha="left", family="monospace", z=z)
        return len(lines) * rh

    def callout(self, x, y, k, to=None, r="rose", d=3.6, lw=0.8, z=14):
        """Lettered callout for a screenshot or a dense object: a solid disc with a white letter in one accent hue
        the content does not use, and a leader to `to` that ends in a dot, not an arrowhead (Cocoa Fig. 2).
        Keep one disc size per figure and line the discs up in the white space beside the content."""
        c = role(r)
        if to:
            self.ax.plot([x, to[0]], [y, to[1]], color=c["mark"], lw=lw, zorder=z - 0.5, solid_capstyle="round")
            self.ax.add_patch(Circle(to, d * 0.2, fc=c["mark"], ec="none", zorder=z))
        self.badge(x, y, k, r, d=d, z=z)

    def greek(self, x, y, w, rows=2, h=1.2, gap=0.9, color="#D9D9D9", z=6):
        """Grey bars standing in for text the reader does not need (a rebuilt screenshot, a document body): the
        eye then goes to the lines that are set in real type. Ragged right edge; (x, y) is the top-left."""
        for i, f in enumerate([1.0, 0.86, 0.94, 0.62, 0.9, 0.74][k % 6] for k in range(rows)):
            self.ax.add_patch(FancyBboxPatch((x, y - (i + 1) * h - i * gap), w * f, h, ec="none", fc=color,
                                             boxstyle=f"round,pad=0,rounding_size={h * 0.3}", zorder=z))
        return rows * (h + gap) - gap

    def para(self, x, y, w, segments, size=None, leading=1.2, z=20, **kw):
        """Example text as a figure object: `segments` (the format of rich: (str, color[, weight[, mark]])) word-
        wrapped to width w from the top-left (x, y), in the fewest lines and with no orphan last word. Marked
        spans keep their bands across line breaks, and at leading=1.2 the bands of consecutive lines touch. Pass
        family="monospace" for what a model wrote. Returns (bottom y, end x of the last line), so a verdict
        glyph can follow the judged span. Worked example: examples/react/render_fig1.py."""
        size = size or self.size
        lh = leading * size / PT_PER_MM
        segs = [(s[0], s[1] if len(s) > 1 else "black", s[2] if len(s) > 2 else "normal", s[3] if len(s) > 3 else None)
                for s in segments]
        # ponytail: widths are measured at regular weight; a long bold run can overshoot w by a few percent
        lines = wrap_marked(segs, lambda t: self.text_width(t, size, **kw), w)
        end = x
        for i, runs in enumerate(lines):
            end = self.rich(x, y - (i + 0.5) * lh, runs, size=size, z=z, **kw)
        return y - len(lines) * lh, end

    def head(self, x, y, letter=None, title="", note=None, size=8.0, rule=None, color="black", note_size=None):
        """Plain panel head, the default panel treatment: bold '(a)', regular-weight title, optional grey italic
        note two sizes down (pass note_size= to keep it on the figure's scale), all on one baseline; (x, y)
        is the top-left. rule=<width in mm> draws a hairline
        under it. No band, no tab, no frame (visual-craft section 7). Returns the y where content can start."""
        base = y - 0.72 * size / PT_PER_MM
        segs = ([(f"({letter}) ", color, "bold")] if letter else []) + [(title, color)]
        end = self.rich(x, base, segs, size=size, va="baseline")
        if note:
            self.text(end + 1.6, base, note, size=note_size or size - 1.6, color=MUTED, style="italic", ha="left",
                      va="baseline")
        bottom = y - 1.05 * size / PT_PER_MM
        if rule:
            self.rule(x, x + rule, bottom - 0.5)
            bottom -= 0.5
        return bottom - 1.2

    def rule(self, x0, x1, y, lw=0.5, color="#B8BEC7", dashed=False, z=4):
        """Horizontal hairline that separates zones or closes a table (booktabs style). It is scaffolding, not
        a wire: wire_crossings() ignores it."""
        self.ax.plot([x0, x1], [y, y], color=color, lw=lw, zorder=z, solid_capstyle="butt",
                     ls=(0, (3.2, 1.8)) if dashed else "-")

    def label(self, x, y, letter, title=None, size=8.0, color=INK):
        """Panel label '(a) Title': bold letter + bold title, top-left anchored. Prefer head(): a regular-weight
        title keeps bold for the letter and for ours."""
        self.text(x, y, f"({letter})", size=size, weight="bold", ha="left", va="top", color=color)
        if title:
            dx = self.text_width(f"({letter})", size, "bold") + 1.0
            self.text(x + dx, y, title, size=size, weight="bold", ha="left", va="top", color=color)

    # ---- containers -------------------------------------------------------
    def box(self, x, y, w, h, r="neutral", title=None, sub=None, *, fill=None, stroke=None,
            lw=0.6, radius=None, dashed=False, shadow=False, size=None, tsize=None, icon=None,
            weight="bold", z=5, title_color=None, align="center", name=None, alpha=1.0, gap=None, container=False):
        """Rounded node. Title bold in role ink, optional sub-line (math welcome). container=True marks a lane or
        background field that wires may cross, so wire_crossings() ignores it."""
        c = role(r)
        rad = radius if radius is not None else min(1.6, 0.16 * h)
        if shadow:
            self.ax.add_patch(FancyBboxPatch((x + 0.35, y - 0.35), w, h,
                              boxstyle=f"round,pad=0,rounding_size={rad}", lw=0,
                              fc="#1A2230", alpha=0.08, zorder=z - 0.2))
        p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rad}",
                           lw=lw, ec=stroke or c["stroke"], fc=fill or c["fill"], zorder=z,
                           ls=(0, (3, 2)) if dashed else "-", alpha=alpha)
        self.ax.add_patch(p)
        if not container:
            self.solids.append((x, y, w, h, f"box '{title or ''}'", p))
        tc = title_color or c["ink"]
        ts = tsize or (size or self.size)
        cx = x + w / 2 if align == "center" else x + 1.6
        ha = "center" if align == "center" else "left"
        if icon:
            getattr(self, f"icon_{icon}")(x + w - 2.3, y + h - 2.3, 2.4, color=c["stroke"])
        if title and sub:
            g = gap if gap is not None else min(h * 0.18, 2.0)
            self.text(cx, y + h / 2 + g, title, size=ts, color=tc, weight=weight, ha=ha, z=z + 1)
            self.text(cx, y + h / 2 - g, sub, size=(size or self.size) - 0.3, color=INK, ha=ha, z=z + 1)
        elif title:
            self.text(cx, y + h / 2, title, size=ts, color=tc, weight=weight, ha=ha, z=z + 1)
        if name:
            self.nodes[name] = (x, y, w, h)
        return p

    def group(self, x, y, w, h, r="neutral", title=None, *, dashed=False, lw=0.7, radius=2.2,
              size=None, fill=None, title_pos="tl", z=1, band=False, color=None, stroke=None):
        """Scope container: pale field + same-hue outline + title in role ink.
        band=True draws a soft header band (card look)."""
        c = role(r)
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                          lw=lw, ec=stroke or c["stroke"], fc=fill or c["fill"], zorder=z,
                          ls=(0, (4, 2.5)) if dashed else "-"))
        if title:
            s = size or self.size + 0.5
            if band:
                bh = s * 0.62
                self.ax.add_patch(PathPatch(_round_top_rect(x, y + h - bh, w, bh, radius),
                                            fc=c["soft"], ec="none", zorder=z + 0.1))
                self.ax.plot([x, x + w], [y + h - bh] * 2, color=c["stroke"], lw=0.4, zorder=z + 0.2)
                self.text(x + 2.0, y + h - bh / 2, title, size=s, weight="bold",
                          color=color or c["ink"], ha="left", z=z + 0.3)
            else:
                tx = x + 2.0 if title_pos == "tl" else x + w / 2
                self.text(tx, y + h - 1.4, title, size=s, weight="bold", color=color or c["ink"],
                          ha="left" if title_pos == "tl" else "center", va="top", z=z + 0.3)

    def chip(self, x, y, s, r="amber", size=None, h=None, pad=0.9, solid=False, z=8, ha="center", region=None,
             lw=0.5):
        """Pill badge; width measured from the rendered text. Returns (x0, w). Every chip is recorded for
        cv.overlaps(); pass region=(x0, y0, x1, y1) when it must stay inside a card, band or cloud. Pass the
        figure's stroke weight as lw; a solid chip's edge takes its fill."""
        c = role(r)
        size = size or self.size - 0.8
        h = h or size * 0.55
        w = self.text_width(s, size) + 2 * pad
        x0 = x - w / 2 if ha == "center" else (x if ha == "left" else x - w)
        self.chips.append((x0, y - h / 2, w, h, s, region))
        self.ax.add_patch(FancyBboxPatch((x0, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h/2}",
                          lw=lw, ec=c["mark"] if solid else c["stroke"], fc=c["mark"] if solid else c["soft"],
                          zorder=z))
        self.text(x0 + w / 2, y, s, size=size, color="white" if solid else c["ink"], z=z + 1)
        return x0, w

    def flow_chips(self, items, x0, x1, ytop, r="amber", size=None, h=None, pad=0.9, gap=1.0, row_gap=0.8,
                   solid=False, z=8, align="center", region=None):
        """Lay chips out like words in a paragraph: measured widths, wrapped into rows that fit [x0, x1],
        rows centred (or left-aligned) and stacked down from ytop. Never place a row of chips at hand-picked
        x positions: widths change with the font and the chips collide or spill out of their container.
        Returns the bottom y of the last row."""
        size = size or self.size - 0.8
        h = h or size * 0.55
        widths = [self.text_width(s, size) + 2 * pad for s in items]
        rows, cur = [], []
        for s, w in zip(items, widths):
            if cur and sum(cw for _, cw in cur) + gap * len(cur) + w > x1 - x0:
                rows.append(cur)
                cur = []
            cur.append((s, w))
        rows.append(cur)
        region = region or (x0, ytop - len(rows) * (h + row_gap) - 0.1, x1, ytop + 0.1)
        y = ytop - h / 2
        for row in rows:
            rw = sum(w for _, w in row) + gap * (len(row) - 1)
            x = x0 + ((x1 - x0 - rw) / 2 if align == "center" else 0.0)
            for s, w in row:
                self.chip(x, y, s, r, size=size, h=h, pad=pad, solid=solid, z=z, ha="left", region=region)
                x += w + gap
            y -= h + row_gap
        return ytop - len(rows) * h - (len(rows) - 1) * row_gap

    def overlaps(self, tol=0.05):
        """Layout audit: chips that overlap each other or leave their declared region. Empty list = clean.
        End every figure script with `assert not cv.overlaps(), cv.overlaps()`."""
        bad = []
        for i, (x, y, w, h, s, reg) in enumerate(self.chips):
            if reg and (x < reg[0] - tol or y < reg[1] - tol or x + w > reg[2] + tol or y + h > reg[3] + tol):
                bad.append(f"'{s}' leaves its region")
            for x2, y2, w2, h2, s2, _ in self.chips[i + 1:]:
                if x < x2 + w2 - tol and x2 < x + w - tol and y < y2 + h2 - tol and y2 < y + h - tol:
                    bad.append(f"'{s}' overlaps '{s2}'")
        return bad

    def text_overlaps(self, tol=0.15):
        """Layout audit for all text: pairs of labels whose rendered boxes overlap, and labels cut by the
        canvas edge. Empty list = clean. Complements overlaps() (chips) for bubbles, cards and captions."""
        r = self._renderer()
        inv = self.ax.transData.inverted()
        boxes = []
        for tx in self.ax.texts:
            if not tx.get_text().strip() or not tx.get_visible():
                continue
            x0, y0, x1, y1 = self._text_box(tx)
            boxes.append((x0, y0, x1, y1, tx.get_text().replace("\n", " ")[:28]))
        tbox = list(boxes)
        kids = self.ax._children  # drawn artists only: get_children() appends spines, axes and titles
        for a, b, c, d, k, n in self.icons:
            art = kids[n] if n < len(kids) else None  # first artist the icon drew; it moves if the script lifts art
            if art is not None:
                tr = art.get_data_transform() if hasattr(art, "get_data_transform") else art.get_transform()
                (a, b), (c, d) = inv.transform(tr.transform([(a, b), (c, d)]))
            boxes.append((a, b, c, d, k))  # an icon on a word is as bad as two words  # an icon on a word is as bad as two words
        from matplotlib.text import Text
        own = set(map(id, self.ax.texts))
        for a in self.fig.axes:  # matplotlib keeps label objects for ticks outside the view; they are not drawn
            for axis in (a.xaxis, a.yaxis):
                lo, hi = sorted(axis.get_view_interval())
                own |= {id(lb) for t in axis.get_major_ticks() + axis.get_minor_ticks()
                        if not lo <= t.get_loc() <= hi for lb in (t.label1, t.label2)}
        for tx in self.fig.findobj(Text):  # chart text (ticks, axis titles, legends) lives in other axes
            if id(tx) in own or not tx.get_text().strip() or not tx.get_visible():
                continue
            # axis labels are placed during a draw, so they are read from the renderer that drew them
            (x0, y0), (x1, y1) = inv.transform(tx.get_window_extent(r).get_points())
            tbox.append((x0, y0, x1, y1, tx.get_text().replace("\n", " ")[:28]))
        bad = [f"'{s}' is cut by the canvas edge" for x0, y0, x1, y1, s in tbox
               if x0 < -tol or y0 < -tol or x1 > self.w + tol or y1 > self.h + tol]
        for i, (a0, b0, a1, b1, s) in enumerate(boxes):
            for c0, d0, c1, d1, s2 in boxes[i + 1:]:
                if s.endswith(" icon") and s2.endswith(" icon"):
                    continue
                if a0 < c1 - tol and c0 < a1 - tol and b0 < d1 - tol and d0 < b1 - tol:
                    bad.append(f"'{s}' overlaps '{s2}'")
        return bad

    def wire_crossings(self, inset=0.35, min_len=0.4):
        """Layout audit: wires (arrow / line) that run THROUGH an opaque object (box, cuboid, slab, doc, cylinder,
        trap, matrix, fmap, token): it enters and leaves, with neither end inside, instead of ending on the border. A wire hidden behind a box reads as a
        wrong edge (MemT Fig. 4: the residual line ran under "Original attention"). Empty list = clean.
        End every figure script with `assert not cv.wire_crossings(), cv.wire_crossings()`."""
        inv = self.ax.transData.inverted()

        def here(pts, art):  # current position: a script may have moved the artist after drawing (lift helpers)
            if art is None:
                return pts
            return [tuple(q) for q in inv.transform(art.get_data_transform().transform(pts))]

        solids = []
        for sx, sy, sw, sh, name, art in self.solids:
            (a0, b0), (a1, b1) = here([(sx, sy), (sx + sw, sy + sh)], art)
            solids.append((a0, b0, a1 - a0, b1 - b0, name))
        bad = []
        for pts, art in self.wires:
            pts = here(pts, art)
            for sx, sy, sw, sh, name in solids:
                a0, b0, a1, b1 = sx + inset, sy + inset, sx + sw - inset, sy + sh - inset
                if any(a0 < px < a1 and b0 < py < b1 for px, py in (pts[0], pts[-1])):
                    continue  # the wire itself starts or ends inside: the object is its container (lane, frame)
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                    L = _clip_len(x0, y0, x1, y1, a0, b0, a1, b1)
                    if L > min_len:
                        bad.append(f"wire ({x0:.1f},{y0:.1f})->({x1:.1f},{y1:.1f}) crosses {name} for {L:.1f} mm")
        return sorted(set(bad))

    # ---- figure-series and narrative devices ----------------------------------
    def badge(self, x, y, k, r="neutral", d=3.0, z=12, size=None, rim=0.5):
        """Numbered disc for steps or sub-mechanisms (solid role mark, white numeral). The white rim (pt)
        separates a disc that sits on a border; rim=0 for a disc on the page."""
        c = role(r)
        self.ax.add_patch(Circle((x, y), d / 2, fc=c["mark"], ec="white" if rim else "none", lw=rim, zorder=z))
        self.text(x, y - 0.05, str(k), size=size or d * 2.0, color="white", weight="bold", z=z + 1)

    def tab(self, x, y, w, h, r="neutral", text="", size=None, rotate=False, solid=False, z=6, radius=None):
        """Rounded tab; rotate=True sets the label vertically (a side tab such as "To Action")."""
        c = role(r)
        rad = radius if radius is not None else min(w, h) * 0.3
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rad}",
                          lw=0.6, ec=c["stroke"], fc=c["mark"] if solid else c["soft"], zorder=z))
        self.text(x + w / 2, y + h / 2, text, size=size or self.size, weight="bold",
                  color="white" if solid else c["ink"], rotation=90 if rotate else 0, z=z + 1, linespacing=1.0)

    def chapter(self, x, y, w, h, r, title, prev=None, nxt=None, tab_w=7.0, size=None):
        """Chapter frame for one item of a taxonomy series: a tinted panel titled in the item's ink,
        an input tab on the left in the previous item's colour and a "To <next>" tab on the right in
        the next item's colour, so consecutive figures read as one chain. prev / nxt are (name, role).
        Returns the inner content rectangle (x, y, w, h)."""
        c = role(r)
        x0, x1 = x, x + w
        if prev:
            self.tab(x, y + h * 0.18, tab_w, h * 0.64, prev[1], prev[0], rotate=True, size=size)
            self.arrow([(x + tab_w + 0.2, y + h / 2), (x + tab_w + 2.6, y + h / 2)], color=role(prev[1])["mark"], head=1.1)
            x0 = x + tab_w + 2.8
        if nxt:
            self.tab(x + w - tab_w, y + h * 0.18, tab_w, h * 0.64, nxt[1], "To " + nxt[0], rotate=True, size=size)
            self.arrow([(x + w - tab_w - 2.6, y + h / 2), (x + w - tab_w - 0.2, y + h / 2)], color=c["mark"], head=1.1)
            x1 = x + w - tab_w - 2.8
        self.ax.add_patch(FancyBboxPatch((x0, y), x1 - x0, h, boxstyle="round,pad=0,rounding_size=2.4",
                          lw=0.8, ec=c["stroke"], fc=c["fill"], zorder=1))
        s = (size or self.size) + 2.4
        self.text((x0 + x1) / 2, y + h - 3.2, title, size=s, weight="bold", color=c["ink"], z=3)
        return x0 + 2.0, y + 2.0, x1 - x0 - 4.0, h - 8.0

    def bubble(self, cx, cy, text, tail=None, r="neutral", size=None, w=None, h=None, fill="white", z=14,
               italic=False, left=None):
        """Speech bubble centred at (cx, cy) (or with its left edge at `left`), sized from its text, with
        vector text (never bake dialogue into a generated image). tail = (tx, ty), the point the tail aims
        at, e.g. the speaker's head; it leaves from the side of the bubble that faces that point."""
        c = role(r)
        size = size or self.size - 0.4
        lines = text.split("\n")
        w = w or max(self.text_width(t, size) for t in lines) + 3.2
        h = h or len(lines) * size * 0.41 + 2.2
        if left is not None:
            cx = left + w / 2
        x, y = cx - w / 2, cy - h / 2
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={min(h, w) * 0.3}",
                          lw=0.55, ec=c["stroke"], fc=fill, zorder=z))
        if tail:
            tx, ty = tail
            if x <= tx <= x + w or y <= ty <= y + h and x <= tx <= x + w:
                side = "bottom" if ty < y else "top"
            else:
                side = "left" if tx < x else "right"
            if side in ("bottom", "top"):
                bx, by = min(max(tx, x + 2.4), x + w - 2.4), (y if side == "bottom" else y + h)
                base = [(bx - 1.1, by), (bx + 1.1, by)]
                inner = (bx, by + (0.6 if side == "bottom" else -0.6))
            else:
                bx, by = (x if side == "left" else x + w), min(max(ty, y + 1.6), y + h - 1.6)
                base = [(bx, by - 0.9), (bx, by + 0.9)]
                inner = (bx + (0.6 if side == "left" else -0.6), by)
            self.ax.add_patch(Polygon([base[0], (tx, ty), base[1]], closed=True, fc=fill, ec=c["stroke"], lw=0.55,
                                      zorder=z - 0.1))
            # hide the bubble outline where the tail joins it
            self.ax.add_patch(Polygon([base[0], base[1], inner], closed=True, fc=fill, ec="none", zorder=z + 0.05))
        self.text(cx, cy, text, size=size, color=c["ink"], z=z + 1, style="italic" if italic else "normal",
                  linespacing=1.15)
        return x, y, w, h

    def spectrum(self, x0, x1, y, c0, c1, labels=(), lw=1.4, head=1.8, size=None, z=6):
        """Graded axis (light -> dark) for a degree, e.g. reactive -> proactive; labels at the ends.
        Sequential lightness, not hue, carries 'more of the same thing'."""
        n = 60
        for k in range(n):
            a, b = x0 + (x1 - head - x0) * k / n, x0 + (x1 - head - x0) * (k + 1) / n
            self.ax.plot([a, b], [y, y], color=mix(c0, c1, k / (n - 1)), lw=lw, zorder=z, solid_capstyle="butt")
        self.ax.add_patch(Polygon([(x1 - head * 1.4, y + head * 0.55), (x1, y), (x1 - head * 1.4, y - head * 0.55)],
                                  closed=True, fc=c1, ec="none", zorder=z))
        if labels:
            self.text(x0, y + 2.4, labels[0], size=size or self.size, color=mix(c0, "#1F2430", 0.4), ha="left", z=z)
            self.text(x1, y + 2.4, labels[-1], size=size or self.size, color=c1, ha="right", z=z)

    # ---- glyphs -----------------------------------------------------------
    def op(self, x, y, sym="+", r="neutral", d=3.0, lw=0.6, z=9, fill="white"):
        """Operator junction drawn as vectors: '+' (⊕), 'x' (⊗), '.' (⊙); other strings as text."""
        c = role(r)
        col = c["ink"] if r != "neutral" else LINE
        self.ax.add_patch(Circle((x, y), d / 2, fc=fill, ec=c["stroke"] if r != "neutral" else LINE,
                                 lw=lw, zorder=z))
        k = d * 0.28
        if sym in ("+", "x"):
            a = 0 if sym == "+" else math.pi / 4
            for t in (a, a + math.pi / 2):
                self.ax.plot([x - k * math.cos(t), x + k * math.cos(t)],
                             [y - k * math.sin(t), y + k * math.sin(t)], color=col, lw=lw, zorder=z + 1,
                             solid_capstyle="round")
        elif sym == ".":
            self.ax.add_patch(Circle((x, y), d * 0.12, fc=col, ec="none", zorder=z + 1))
        else:
            self.text(x, y, sym, size=d * PT_PER_MM * 0.62, color=col, z=z + 1)
        return (x, y)

    def doc(self, x, y, w, h, r="neutral", lines=3, fold=None, title=None, z=6, lw=0.6):
        """Document with folded corner and faux text lines."""
        c = role(r)
        f = fold or min(w, h) * 0.28
        pts = [(x, y), (x + w, y), (x + w, y + h - f), (x + w - f, y + h), (x, y + h)]
        self.solids.append((x, y, w, h, f"doc '{title or ''}'", None))
        self.ax.add_patch(Polygon(pts, closed=True, fc="white", ec=c["stroke"], lw=lw, zorder=z))
        self.ax.add_patch(Polygon([(x + w - f, y + h), (x + w - f, y + h - f), (x + w, y + h - f)],
                                  closed=True, fc=c["soft"], ec=c["stroke"], lw=lw * 0.8, zorder=z + 0.1))
        top = y + h - f - 0.6 if not title else y + h - f - 2.2
        if title:
            self.text(x + 0.9, y + h - 1.2, title, size=self.size - 1.2, color=c["ink"], ha="left",
                      va="top", weight="bold", z=z + 1)
        gap = (top - y - 0.8) / max(lines, 1)
        for i in range(lines):
            ly = top - i * gap
            ln = (w - 1.8) * (0.62 if i == lines - 1 else 1.0)
            self.ax.plot([x + 0.9, x + 0.9 + ln], [ly, ly], color=c["stroke"], lw=0.7, alpha=0.75,
                         zorder=z + 1, solid_capstyle="round")

    def stack(self, x, y, w, h, n=3, r="neutral", dx=0.9, dy=0.9, z=5, **kw):
        """n offset cards (multiplicity: heads, experts, batches). Returns front card rect."""
        for i in range(n - 1, 0, -1):
            self.box(x + i * dx, y + i * dy, w, h, r, z=z - i * 0.01,
                     **{k: v for k, v in kw.items() if k in ("lw", "radius", "fill")})
        self.box(x, y, w, h, r, z=z, **kw)
        return (x, y, w, h)

    def matrix(self, x, y, w, h, rows=5, cols=6, depth=1, r="memory", dx=1.1, dy=1.1, seed=0,
               values=None, lw=0.35, z=6, cmap=None, vmin=0.0, vmax=1.0, empty=False, back_alpha=1.0,
               fade=0.0, band=None, band_color=None):
        """Grid glyph for a matrix / state tensor; depth>1 draws offset slabs behind
        (channels / heads). values: real (rows, cols) data; otherwise a fixed
        illustrative texture (state it in the caption if it could be mistaken for data).
        fade: 0..1 wash toward white (decay); band=('row'|'col', idx): dashed highlight
        of the touched row/column (erase / write target)."""
        c = role(r)
        rng = np.random.default_rng(seed)
        cm = cmap or mcolors.LinearSegmentedColormap.from_list("m", [c["fill"], c["soft"], c["mark"]])
        cw, ch = w / cols, h / rows
        self.solids.append((x, y, w + (depth - 1) * dx, h + (depth - 1) * dy, "matrix", None))
        for k in range(depth - 1, -1, -1):
            ox, oy = x + k * dx, y + k * dy
            vals = values if (values is not None and k == 0) else rng.uniform(0.05, 0.85, (rows, cols))
            for i in range(rows):
                for j in range(cols):
                    if empty:
                        fc = "white"
                    elif k == 0:
                        fc = mix(cm((vals[i, j] - vmin) / (vmax - vmin)), "#FFFFFF", fade)
                    else:
                        fc = c["soft"]
                    self.ax.add_patch(Rectangle((ox + j * cw, oy + h - (i + 1) * ch), cw, ch, fc=fc,
                                                ec=c["stroke"], lw=lw * 0.7, zorder=z - k * 0.01,
                                                alpha=1 if k == 0 else back_alpha))
            self.ax.add_patch(Rectangle((ox, oy), w, h, fc="none", ec=c["ink"], lw=lw * 1.6,
                                        zorder=z - k * 0.01 + 0.005))
        if band:
            kind, idx = band
            bx, by, bw, bh = ((x + idx * cw, y, cw, h) if kind == "col" else (x, y + h - (idx + 1) * ch, w, ch))
            self.ax.add_patch(Rectangle((bx - 0.25, by - 0.25), bw + 0.5, bh + 0.5, fc="none",
                                        ec=band_color or ROLE["coral"]["mark"], lw=0.7, ls=(0, (2, 1.2)),
                                        zorder=z + 0.1))
        return (x, y, w + (depth - 1) * dx, h + (depth - 1) * dy)

    def tokens(self, x, y, n, w=2.2, h=2.2, r="blue", gap=0.35, labels=None, z=7, fills=None,
               size=None, lw=0.45):
        """Token strip of n rounded squares; fills = per-token roles. Returns centres."""
        cs = []
        for i in range(n):
            rr = role(fills[i]) if fills else role(r)
            xx = x + i * (w + gap)
            self.solids.append((xx, y, w, h, f"token {labels[i] if labels else i}", None))
            self.ax.add_patch(FancyBboxPatch((xx, y), w, h, boxstyle=f"round,pad=0,rounding_size={min(w, h) * 0.22}",
                              fc=rr["soft"], ec=rr["stroke"], lw=lw, zorder=z))
            if labels:
                self.text(xx + w / 2, y + h / 2, labels[i], size=size or self.size - 1.5, color=rr["ink"], z=z + 1)
            cs.append((xx + w / 2, y + h / 2))
        return cs

    def trap(self, x, y, w, h, r="amber", narrow="right", ratio=0.58, title=None, size=None, lw=0.6, z=6):
        """Projection / linear layer as a trapezoid. narrow = side that is shorter
        ('right'/'left' for horizontal flow, 'top'/'bottom' for vertical flow).
        A narrow-right + narrow-left pair reads as a low-rank (down/up) projection."""
        c = role(r)
        k = (1 - ratio) / 2
        self.solids.append((x, y, w, h, f"trap '{title or ''}'", None))
        if narrow == "right":
            pts = [(x, y), (x + w, y + h * k), (x + w, y + h * (1 - k)), (x, y + h)]
        elif narrow == "left":
            pts = [(x, y + h * k), (x + w, y), (x + w, y + h), (x, y + h * (1 - k))]
        elif narrow == "bottom":
            pts = [(x + w * k, y), (x + w * (1 - k), y), (x + w, y + h), (x, y + h)]
        else:
            pts = [(x, y), (x + w, y), (x + w * (1 - k), y + h), (x + w * k, y + h)]
        self.ax.add_patch(Polygon(pts, closed=True, fc=c["soft"], ec=c["stroke"], lw=lw, zorder=z,
                                  joinstyle="round"))
        if title:
            self.text(x + w / 2, y + h / 2, title, size=size or self.size - 0.6, color=c["ink"], z=z + 1)

    def vec(self, x, y, n=4, cell=1.4, r="memory", vertical=False, z=7, lw=0.35, seed=0):
        """Vector glyph: a 1×n (or n×1) strip of shaded cells."""
        c = role(r)
        rng = np.random.default_rng(seed)
        cm = mcolors.LinearSegmentedColormap.from_list("v", [c["fill"], c["mark"]])
        for i in range(n):
            xx, yy = (x, y + (n - 1 - i) * cell) if vertical else (x + i * cell, y)
            self.ax.add_patch(Rectangle((xx, yy), cell, cell, fc=cm(rng.uniform(0.15, 0.8)),
                                        ec=c["ink"], lw=lw, zorder=z))

    def cylinder(self, x, y, w, h, r="neutral", z=6, lw=0.6, title=None):
        """Database / store."""
        c = role(r)
        e = min(h * 0.22, w * 0.22)
        self.solids.append((x, y, w, h, f"cylinder '{title or ''}'", None))
        self.ax.add_patch(Ellipse((x + w / 2, y + e / 2), w, e, fc=c["fill"], ec=c["stroke"], lw=lw, zorder=z))
        self.ax.add_patch(Rectangle((x, y + e / 2), w, h - e, fc=c["fill"], ec="none", zorder=z + 0.01))
        for xx in (x, x + w):
            self.ax.plot([xx, xx], [y + e / 2, y + h - e / 2], color=c["stroke"], lw=lw, zorder=z + 0.02)
        self.ax.add_patch(Ellipse((x + w / 2, y + h - e / 2), w, e, fc=c["soft"], ec=c["stroke"], lw=lw, zorder=z + 0.03))
        if title:
            self.text(x + w / 2, y + (h - e) / 2, title, color=c["ink"], weight="bold", z=z + 1)

    def hexagon(self, x, y, w, h, r="line", title=None, z=6, lw=0.6, size=None):
        """Interface: a flat hexagon that sits ON the boundary between two layers (CortenMM Fig. 3)."""
        c = role(r)
        d = min(h / 2, w / 4)
        self.solids.append((x + d / 2, y, w - d, h, f"hexagon '{title or ''}'", None))
        self.ax.add_patch(Polygon([(x, y + h / 2), (x + d, y + h), (x + w - d, y + h), (x + w, y + h / 2),
                                   (x + w - d, y), (x + d, y)], fc=c["fill"], ec=c["stroke"], lw=lw, zorder=z))
        if title:
            self.text(x + w / 2, y + h / 2, title, size=size, color=c["ink"], z=z + 1)

    def diamond(self, x, y, w, h, r="amber", title=None, z=6, lw=0.7):
        """Decision / gate."""
        c = role(r)
        self.solids.append((x + w / 4, y + h / 4, w / 2, h / 2, f"diamond '{title or ''}'", None))  # inscribed box
        self.ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y)],
                                  fc=c["soft"], ec=c["stroke"], lw=lw, zorder=z))
        if title:
            self.text(x + w / 2, y + h / 2, title, color=c["ink"], weight="bold", z=z + 1)

    def gradient_rect(self, x, y, w, h, c0, c1, z=4, radius=0.0, horizontal=True):
        """Gradient-filled rectangle (hero bars, intensity ramps)."""
        grad = np.linspace(0, 1, 256)[None, :] if horizontal else np.linspace(1, 0, 256)[:, None]
        cm = mcolors.LinearSegmentedColormap.from_list("g", [c0, c1])
        im = self.ax.imshow(grad, extent=(x, x + w, y, y + h), cmap=cm, aspect="auto", zorder=z,
                            interpolation="bicubic")
        if radius:
            clip = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                                  transform=self.ax.transData, fc="none", ec="none")
            self.ax.add_patch(clip)
            im.set_clip_path(clip)
        self.ax.set_xlim(0, self.w)
        self.ax.set_ylim(0, self.h)
        return im

    def image(self, path, cx, cy, w, z=12, knockout_white=True, crop=True, fit="width", h=None, radius=0.0,
              focus=(0.5, 0.5), zoom=1.0):
        """Place a raster icon/illustration centred at (cx, cy) with width w mm (height from aspect).
        Use for illustrative content (agent mascots, scene photos) and for product marks inside a tile()
        beside the product's name; never as the only label of a thing, and never for data.
        The icon is resampled exactly once, with Lanczos plus a light unsharp mask, to its printed size
        at RASTER_DPI, and placed on the output pixel grid with nearest-neighbour sampling, so the PNG
        export copies it 1:1 (a second resampling by matplotlib breaks thin outlines into dashes and
        softens edges). knockout_white mattes off only the pure-white background connected to the
        border (cream or pastel fills inside the outline stay opaque), with a 1 px soft rim.
        fit="height" makes w the icon's height instead of its width, so characters of one set with
        different props (a wide laptop, a tall magnifier) come out at the same body size; fit="box"
        makes w the longer side, for object icons of mixed aspect. fit="cover" fills a w x h card edge to
        edge (full-bleed vignettes): the source is cropped to the card's aspect around `focus` (fractions of
        width, height; 0.5, 0.35 keeps faces), never letterboxed, with `radius` mm rounded corners; zoom > 1
        crops tighter around `focus` so a small subject (a robot in a room) fills a thumbnail cell.
        Returns the placed height in mm."""
        from PIL import Image, ImageDraw, ImageFilter
        im = Image.open(path).convert("RGBA")
        im = Image.alpha_composite(Image.new("RGBA", im.size, "white"), im).convert("RGB")
        if fit == "cover":
            assert h, "fit='cover' needs the card height h"
            crop, knockout_white = False, False
            if im.width / im.height > w / h:  # too wide: crop the sides
                cw = round(im.height * w / h)
                x = round(min(max(focus[0] * im.width - cw / 2, 0), im.width - cw))
                im = im.crop((x, 0, x + cw, im.height))
            else:
                ch = round(im.width * h / w)
                y = round(min(max(focus[1] * im.height - ch / 2, 0), im.height - ch))
                im = im.crop((0, y, im.width, y + ch))
            if zoom > 1:
                zw, zh = round(im.width / zoom), round(im.height / zoom)
                x = round(min(max(focus[0] * im.width - zw / 2, 0), im.width - zw))
                y = round(min(max(focus[1] * im.height - zh / 2, 0), im.height - zh))
                im = im.crop((x, y, x + zw, y + zh))
            fit = "width"
        if crop:
            box = im.convert("L").point(lambda v: 255 if v < 245 else 0).getbbox()
            if box:
                pad = 8
                im = im.crop((max(box[0] - pad, 0), max(box[1] - pad, 0),
                              min(box[2] + pad, im.width), min(box[3] + pad, im.height)))
        ppm = RASTER_DPI / 25.4  # output pixels per mm
        if fit == "box":  # w bounds the longer side: mixed wide/tall icons of one set stay in one footprint
            fit = "height" if im.height > im.width else "width"
        tw = max(8, round((w * im.width / im.height if fit == "height" else w) * ppm))
        th = max(8, round(tw * im.height / im.width))
        src_dpi = im.width / (tw / ppm / 25.4)
        if src_dpi < MIN_SOURCE_DPI:  # upsampling invents no detail: the print looks soft whatever the export does
            print(f"[paperkit] warning: {os.path.basename(path)} has {src_dpi:.0f} source px per inch at "
                  f"{tw / ppm:.1f} mm (< {MIN_SOURCE_DPI}); generate it larger or print it smaller")
        im = im.resize((tw, th), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=2))
        a = np.asarray(im).astype(float) / 255.0
        alpha = np.ones(a.shape[:2])
        if knockout_white:
            m = Image.new("L", (tw + 2, th + 2), 255)
            m.paste(Image.fromarray(((a.min(axis=2) > 0.975) * 255).astype(np.uint8)), (1, 1))
            ImageDraw.floodfill(m, (0, 0), 128)
            outside = np.asarray(m)[1:-1, 1:-1] == 128
            rim = np.asarray(Image.fromarray((outside * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
            soft = np.clip((1.0 - a.min(axis=2)) / 0.25, 0.0, 1.0)
            alpha = np.where(outside, 0.0, np.where(rim, soft, 1.0))
            a = np.clip((a - (1.0 - alpha[..., None])) / np.maximum(alpha, 1e-3)[..., None], 0.0, 1.0)
        if radius > 0:  # rounded card corners, antialiased by 4x supersampling
            r4 = round(radius * ppm * 4)
            m = Image.new("L", (tw * 4, th * 4), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, tw * 4 - 1, th * 4 - 1), r4, fill=255)
            alpha = alpha * np.asarray(m.resize((tw, th), Image.LANCZOS), float) / 255.0
        # snap to the output pixel grid so the export is a 1:1 copy of the resampled icon
        x0, y0 = round((cx - tw / ppm / 2) * ppm) / ppm, round((cy - th / ppm / 2) * ppm) / ppm
        w, h = tw / ppm, th / ppm
        # "none" embeds these pixels unchanged in PDF/SVG; any other mode resamples them to the figure dpi (100)
        self.ax.imshow(np.dstack([a, alpha]), extent=(x0, x0 + w, y0, y0 + h), zorder=z, interpolation="none")
        if x0 >= 0 and y0 >= 0 and x0 + w <= self.w and y0 + h <= self.h:
            self.rasters.append((path, tw, th))
        else:
            print(f"paperkit: image {os.path.basename(str(path))} leaves the {self.w:g} x {self.h:g} mm canvas "
                  f"and will be cropped (x {x0:.1f}..{x0 + w:.1f}, y {y0:.1f}..{y0 + h:.1f})")
        self.ax.set_xlim(0, self.w)
        self.ax.set_ylim(0, self.h)
        return h

    # ---- icons (pure vector) -------------------------------------------------
    def icon_snow(self, x, y, s, color=LINE, lw=0.55, z=12):
        """Snowflake = frozen / not trained."""
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "snow icon", len(self.ax._children)])
        for k in range(3):
            a = k * math.pi / 3
            dx, dy = s / 2 * math.cos(a), s / 2 * math.sin(a)
            self.ax.plot([x - dx, x + dx], [y - dy, y + dy], color=color, lw=lw, zorder=z, solid_capstyle="round")
            for sgn in (1, -1):
                bx, by = x + sgn * dx * 0.6, y + sgn * dy * 0.6
                for b in (a + 0.7, a - 0.7):
                    self.ax.plot([bx, bx + sgn * s * 0.17 * math.cos(b)], [by, by + sgn * s * 0.17 * math.sin(b)],
                                 color=color, lw=lw * 0.8, zorder=z, solid_capstyle="round")

    def icon_check(self, x, y, s, color=LINE, lw=0.8, z=12):
        """Tick drawn as vectors (font-independent ✓)."""
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "check icon", len(self.ax._children)])
        self.ax.plot([x - s * 0.45, x - s * 0.1, x + s * 0.5], [y, y - s * 0.38, y + s * 0.42], color=color, lw=lw,
                     zorder=z, solid_capstyle="round", solid_joinstyle="round")

    def icon_cross(self, x, y, s, color=LINE, lw=0.8, z=12):
        """Cross drawn as vectors (font-independent ✗)."""
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "cross icon", len(self.ax._children)])
        for sg in (1, -1):
            self.ax.plot([x - s * 0.4, x + s * 0.4], [y - sg * s * 0.4, y + sg * s * 0.4], color=color, lw=lw,
                         zorder=z, solid_capstyle="round")

    def icon_flame(self, x, y, s, color="#E0702A", z=12):
        """Flame = trainable."""
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "flame icon", len(self.ax._children)])
        h, w = s, s * 0.72
        outer = [(x, y - h / 2), (x + w / 2, y - h * 0.25), (x + w * 0.42, y + h * 0.08), (x + w * 0.08, y + h / 2),
                 (x + w * 0.12, y + h * 0.14), (x - w * 0.08, y + h * 0.1), (x - w * 0.2, y + h * 0.26),
                 (x - w / 2, y + h * 0.0), (x - w / 2, y - h * 0.25)]
        self.ax.add_patch(PathPatch(_smooth(outer), fc=color, ec="none", zorder=z))
        inner = [(x, y - h * 0.42), (x + w * 0.24, y - h * 0.2), (x + w * 0.04, y + h * 0.12),
                 (x - w * 0.24, y - h * 0.2)]
        self.ax.add_patch(PathPatch(_smooth(inner), fc="#FFD27A", ec="none", zorder=z + 0.1))

    def icon_lock(self, x, y, s, color=LINE, z=12, lw=0.55):
        """Lock = fixed after offline training."""
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "lock icon", len(self.ax._children)])
        bw, bh = s * 0.74, s * 0.52
        self.ax.add_patch(Arc((x, y - s / 2 + bh), bw * 0.6, s * 0.7, theta1=0, theta2=180, ec=color,
                              lw=lw * 1.5, zorder=z))
        self.ax.add_patch(FancyBboxPatch((x - bw / 2, y - s / 2), bw, bh,
                          boxstyle=f"round,pad=0,rounding_size={s * 0.08}", fc=color, ec="none", zorder=z + 0.05))
        self.ax.add_patch(Circle((x, y - s / 2 + bh * 0.52), s * 0.075, fc="white", ec="none", zorder=z + 0.1))

    def icon_cycle(self, x, y, s, color=LINE, z=12, lw=0.6):
        """Circular arrows = evolves online / recurrent."""
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "cycle icon", len(self.ax._children)])
        rr = s * 0.4
        for a0 in (30, 210):
            self.ax.add_patch(Arc((x, y), 2 * rr, 2 * rr, theta1=a0, theta2=a0 + 125, ec=color, lw=lw, zorder=z))
            t = math.radians(a0 + 125)
            px, py = x + rr * math.cos(t), y + rr * math.sin(t)
            tx, ty = -math.sin(t), math.cos(t)          # tangent (ccw)
            nx, ny = math.cos(t), math.sin(t)
            k = s * 0.2
            self.ax.add_patch(Polygon([(px + tx * k, py + ty * k), (px + nx * k * 0.55, py + ny * k * 0.55),
                                       (px - nx * k * 0.55, py - ny * k * 0.55)], fc=color, ec="none", zorder=z))

    def icon_robot(self, x, y, s, color=LINE, fill="white", z=12, lw=0.6):
        """Agent / model."""
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "robot icon", len(self.ax._children)])
        hw, hh = s * 0.8, s * 0.62
        self.ax.add_patch(FancyBboxPatch((x - hw / 2, y - hh / 2 - s * 0.08), hw, hh,
                          boxstyle=f"round,pad=0,rounding_size={s * 0.16}", fc=fill, ec=color, lw=lw, zorder=z))
        for sx in (-1, 1):
            self.ax.add_patch(Circle((x + sx * hw * 0.22, y - s * 0.08), s * 0.07, fc=color, ec="none", zorder=z + 0.1))
        self.ax.plot([x, x], [y + hh / 2 - s * 0.08, y + s * 0.42], color=color, lw=lw, zorder=z)
        self.ax.add_patch(Circle((x, y + s * 0.44), s * 0.07, fc=color, ec="none", zorder=z))

    def icon_user(self, x, y, s, color=LINE, fill="white", z=12, lw=0.6):
        """Person: the user or speaker. Same weight and box as icon_robot, so the two read as one family."""
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "user icon", len(self.ax._children)])
        self.ax.add_patch(Wedge((x, y - s * 0.5), s * 0.42, 0, 180, fc=fill, ec=color, lw=lw, zorder=z))
        self.ax.add_patch(Circle((x, y + s * 0.2), s * 0.22, fc=fill, ec=color, lw=lw, zorder=z + 0.1))

    def icon_clock(self, x, y, s, color=LINE, z=12, lw=0.55):
        self.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, "clock icon", len(self.ax._children)])
        self.ax.add_patch(Circle((x, y), s / 2, fc="white", ec=color, lw=lw, zorder=z))
        self.ax.plot([x, x], [y, y + s * 0.32], color=color, lw=lw, zorder=z + 0.1, solid_capstyle="round")
        self.ax.plot([x, x + s * 0.24], [y, y], color=color, lw=lw, zorder=z + 0.1, solid_capstyle="round")

    def icon_doc(self, x, y, s, r="neutral"):
        self.doc(x - s * 0.38, y - s / 2, s * 0.76, s, r, lines=3, fold=s * 0.28, z=12)

    # ---- architecture register (2026-11 study of 23 method figures; references/architecture-study-2026-11.md)
    def section(self, x, y, w, h, r="neutral", title=None, *, tab="top", letter=None, dashed=True, lw=0.75,
                radius=2.4, size=None, fill=None, z=1, italic=False):
        """Module region: a dashed border in one hue around a white field (the page stays the ground; pass
        fill=ROLE[r]["fill"] to tint the field when membership would otherwise be unclear), the title on a pill tab that sits ON
        the top border (tab="top", ReSet/CoPS), a bold strip along the bottom edge (tab="bottom", HFF-Net/STDD),
        a bold-italic title in the top-left corner in the role mark (tab="corner", SemDiff/C2R/CHAL) or the old
        header band (tab="band"). Each module of the method gets its own hue, so panels, wires and the legend
        share one key. letter='a' prefixes '(a) '. Returns the free inner rect (x, y, w, h)."""
        c = role(r)
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}", lw=lw,
                                         ec=c["stroke"], fc=fill or "white", ls=(0, (4, 2.2)) if dashed else "-",
                                         zorder=z))
        s = size or self.size + 0.6
        t = (f"({letter}) " if letter else "") + (title or "")
        if not t.strip():
            return (x, y, w, h)
        st = "italic" if italic else "normal"
        if tab == "top":
            tw, th = self.text_width(t, s, "bold") + 4.0, s * 0.56
            self.ax.add_patch(FancyBboxPatch((x + w / 2 - tw / 2, y + h - th / 2), tw, th,
                                             boxstyle=f"round,pad=0,rounding_size={th / 2}", fc=c["soft"],
                                             ec=c["stroke"], lw=0.6, zorder=z + 0.3))
            self.text(x + w / 2, y + h, t, size=s, weight="bold", color=c["ink"], z=z + 0.4, style=st)
            return (x, y, w, h - th / 2)
        if tab == "bottom":
            bh = s * 0.6
            self.ax.add_patch(FancyBboxPatch((x + 1.0, y + 0.9), w - 2.0, bh, boxstyle=f"round,pad=0,rounding_size={bh / 2}",
                                             fc=c["soft"], ec="none", zorder=z + 0.2))
            self.text(x + w / 2, y + 0.9 + bh / 2, t, size=s, weight="bold", color=c["ink"], z=z + 0.4, style=st)
            return (x, y + bh + 1.4, w, h - bh - 1.4)
        if tab == "corner":
            self.text(x + 2.0, y + h - 1.3, t, size=s, weight="bold", color=c["mark"], ha="left", va="top",
                      z=z + 0.4, style="italic")
            return (x, y, w, h - s * 0.5 - 1.3)
        self.group(x, y, w, h, r, t, band=True, size=s, radius=radius, lw=lw, fill=fill or c["fill"], z=z)
        return (x, y, w, h - s * 0.62)

    def cuboid(self, x, y, w, h, d=None, r="blue", title=None, *, size=None, rotate=False, angle=40.0, fill=None,
               lw=0.5, z=6, grad=None, weight="bold", color=None, sub=None):
        """Pseudo-3D block: front face (x, y, w, h) with top and right faces receding by depth d. Tall thin
        cuboids with rotate=True are layer slabs (Conv, LN, FFN, ResBlock; vertical text); small near-square
        ones are feature tensors with an H×W×C label beside them; grad=(c0, c1) paints the front face as a
        gradient for a fused feature (HFF-Net). Returns the front rect; the top face adds d·sin(angle)."""
        c = role(r)
        d = min(w, h) * 0.35 if d is None else d
        ox, oy = d * math.cos(math.radians(angle)), d * math.sin(math.radians(angle))
        front = fill or c["soft"]
        self.solids.append((x, y, w + ox, h + oy, f"cuboid '{title or ''}'", None))
        self.ax.add_patch(Polygon([(x, y + h), (x + w, y + h), (x + w + ox, y + h + oy), (x + ox, y + h + oy)],
                                  closed=True, fc=mix(front, "#FFFFFF", 0.5), ec=c["stroke"], lw=lw, zorder=z,
                                  joinstyle="round"))
        self.ax.add_patch(Polygon([(x + w, y), (x + w + ox, y + oy), (x + w + ox, y + h + oy), (x + w, y + h)],
                                  closed=True, fc=mix(front, c["stroke"], 0.4), ec=c["stroke"], lw=lw, zorder=z,
                                  joinstyle="round"))
        if grad:
            self.gradient_rect(x, y, w, h, grad[0], grad[1], z=z + 0.01, horizontal=not rotate)
            self.ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=c["stroke"], lw=lw, zorder=z + 0.02))
        else:
            self.ax.add_patch(Rectangle((x, y), w, h, fc=front, ec=c["stroke"], lw=lw, zorder=z + 0.01))
        s = size or self.size
        if title and sub:
            g = (w if rotate else h) * 0.16
            off = (-g, 0) if rotate else (0, g)
            self.text(x + w / 2 + off[0], y + h / 2 + off[1], title, size=s, weight=weight, color=color or c["ink"],
                      rotation=90 if rotate else 0, z=z + 1)
            self.text(x + w / 2 - off[0], y + h / 2 - off[1], sub, size=s - 0.6, color=INK,
                      rotation=90 if rotate else 0, z=z + 1)
        elif title:
            self.text(x + w / 2, y + h / 2, title, size=s, weight=weight, color=color or c["ink"],
                      rotation=90 if rotate else 0, z=z + 1, linespacing=1.0)
        return (x, y, w, h)

    def fmap(self, x, y, w, h, *, n=1, dx=1.0, dy=1.0, cmap="viridis", seed=0, blobs=3, data=None, border=None,
             lw=0.45, z=6, vmin=None, vmax=None):
        """Feature-map / attention-map thumbnail; n offset copies behind = channels, frames or scales.
        data: a real 2-D array (attention weights, a mask, an image channel); otherwise a smooth
        illustrative field. Saying "illustrative maps" once in the caption is enough. Returns the front rect."""
        rng = np.random.default_rng(seed)
        self.solids.append((x, y, w + (n - 1) * dx, h + (n - 1) * dy, "fmap", None))
        for k in range(n - 1, -1, -1):
            ox, oy = x + k * dx, y + k * dy
            a = data if (data is not None and k == 0) else _field(rng, blobs=blobs)
            self.ax.imshow(a, extent=(ox, ox + w, oy, oy + h), cmap=cmap, interpolation="bilinear" if data is None
                           else "nearest", aspect="auto", zorder=z - k * 0.01, vmin=vmin, vmax=vmax)
            self.ax.add_patch(Rectangle((ox, oy), w, h, fc="none", ec=(border or LINE) if k == 0 else "#FFFFFF",
                                        lw=lw, zorder=z - k * 0.01 + 0.005))
        self.ax.set_xlim(0, self.w)
        self.ax.set_ylim(0, self.h)
        return (x, y, w, h)

    def num_matrix(self, x, y, values, cell=3.6, r="blue", fmt="{:.2f}", size=None, hi=(), rows=None, cols=None,
                   lw=0.4, z=6, vmin=None, vmax=None, ch=None):
        """Matrix with its numbers in the cells (ProEmoTrans, Holmes calibration, CoPS weighting): fill on the role
        ramp by value, white numerals on dark cells, bold border on hi=[(i, j)]. rows/cols: header labels.
        Returns (x, y, w, h) of the grid; (x, y) is the bottom-left."""
        c = role(r)
        v = np.asarray(values, float)
        R, C = v.shape
        ch = ch or cell
        self.solids.append((x, y, C * cell, R * ch, "num_matrix", None))
        lo, top = (v.min() if vmin is None else vmin), (v.max() if vmax is None else vmax)
        cm = mcolors.LinearSegmentedColormap.from_list("n", [c["fill"], c["soft"], c["mark"]])
        s = size or self.size - 1.0
        for i in range(R):
            for j in range(C):
                fc = cm((v[i, j] - lo) / max(top - lo, 1e-9))
                cx, cy = x + j * cell, y + (R - 1 - i) * ch
                self.ax.add_patch(Rectangle((cx, cy), cell, ch, fc=fc, ec="white", lw=lw, zorder=z))
                lum = 0.2126 * fc[0] + 0.7152 * fc[1] + 0.0722 * fc[2]
                self.text(cx + cell / 2, cy + ch / 2, fmt.format(v[i, j]).replace("-", "\u2212"), size=s,
                          color="white" if lum < 0.55 else c["ink"], z=z + 1,
                          weight="bold" if (i, j) in hi else "normal")
                if (i, j) in hi:
                    self.ax.add_patch(Rectangle((cx, cy), cell, ch, fc="none", ec=c["ink"], lw=0.9, zorder=z + 0.5))
        self.ax.add_patch(Rectangle((x, y), C * cell, R * ch, fc="none", ec=c["stroke"], lw=0.6, zorder=z + 0.4))
        for j, s_ in enumerate(cols or []):
            self.text(x + (j + 0.5) * cell, y + R * ch + 1.3, s_, size=s, color=MUTED, z=z + 1)
        for i, s_ in enumerate(rows or []):
            self.text(x - 1.0, y + (R - 1 - i + 0.5) * ch, s_, size=s, color=MUTED, ha="right", z=z + 1)
        return (x, y, C * cell, R * ch)

    def graph(self, cx, cy, rad, n=5, r="blue", edges="full", node_d=1.6, colors=None, lw=0.45, z=8, rot=90.0):
        """Small node-link glyph (similarity graph, scene graph, cell graph): n nodes on a circle,
        edges = 'full' | 'ring' | [(i, j), ...]; colors = per-node fill. Returns node centres."""
        c = role(r)
        pts = [(cx + rad * math.cos(math.radians(rot + 360 * k / n)), cy + rad * math.sin(math.radians(rot + 360 * k / n)))
               for k in range(n)]
        es = ([(i, j) for i in range(n) for j in range(i + 1, n)] if edges == "full" else
              [(i, (i + 1) % n) for i in range(n)] if edges == "ring" else edges)
        for i, j in es:
            self.ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], color=c["stroke"], lw=lw, zorder=z)
        for k, p in enumerate(pts):
            self.ax.add_patch(Circle(p, node_d / 2, fc=(colors[k] if colors else c["mark"]), ec="white", lw=0.4,
                                     zorder=z + 0.1))
        return pts

    def mini_plot(self, x, y, w, h, series, roles=None, fill=True, axis=True, lw=0.7, z=8, bars=False):
        """Sparkline inside a card: a distribution, a loss curve, class scores (bars=True). series = list of
        1-D arrays sampled evenly over [x, x + w]; scaled jointly to h. Shape only: no ticks, no numbers."""
        roles = roles or ["blue"] * len(series)
        top = max(float(np.max(s)) for s in series) or 1.0
        if axis:
            self.ax.plot([x, x, x + w], [y + h, y, y], color="#9AA0A8", lw=0.5, zorder=z, solid_joinstyle="miter")
        for s, rr in zip(series, roles):
            c, s = role(rr), np.asarray(s, float)
            if bars:
                bw = w / len(s)
                for k, v in enumerate(s):
                    self.ax.add_patch(Rectangle((x + k * bw + bw * 0.15, y), bw * 0.7, h * v / top, fc=c["soft"],
                                                ec=c["stroke"], lw=0.4, zorder=z + 0.1))
                continue
            xs = np.linspace(x, x + w, len(s))
            ys = y + h * s / top
            if fill:
                self.ax.fill_between(xs, y, ys, color=c["soft"], alpha=0.75, lw=0, zorder=z)
            self.ax.plot(xs, ys, color=c["mark"], lw=lw, zorder=z + 0.1)

    def phase_bar(self, y, segments, h=3.4, size=None, z=2, gap=0.4):
        """Stage strip under the columns of a pipeline (DySeT, MAGRPP): segments = [(x0, x1, role, label)].
        Names the phases once so the panels above need no long titles."""
        for x0, x1, rr, lab in segments:
            c = role(rr)
            self.ax.add_patch(Rectangle((x0 + gap / 2, y), x1 - x0 - gap, h, fc=c["soft"], ec="none", zorder=z))
            self.text((x0 + x1) / 2, y + h / 2, lab, size=size or self.size, color=c["ink"], weight="bold", z=z + 1)

    def turn_strip(self, x, y, w, n, cut, h=2.2, r="amber", past="memory", gap=0.18, z=6):
        """Session progress as n turn cells (ARE-bench Fig. 2): turns before the cut in the `past` soft tint,
        the cut turn solid in `r`, later turns grey. Shows where a task is cut and how much history precedes it."""
        cw = (w - gap * (n - 1)) / n
        for i in range(n):
            t = i + 1
            fc = role(past)["soft"] if t < cut else role(r)["mark"] if t == cut else "#E4E4E4"
            ec = role(past)["stroke"] if t < cut else role(r)["stroke"] if t == cut else "#C8C8C8"
            self.ax.add_patch(Rectangle((x + i * (cw + gap), y), cw, h, fc=fc, ec=ec, lw=0.25, zorder=z))

    def filetree(self, x, y, w, rows, *, title=None, row_h=3.4, size=None, indent=3.0, r="neutral", z=8):
        """Workspace listing as a data object (ARE-bench Fig. 2): a window with three dots and a mono title,
        rows = [(depth, name, status, role)] with status None or a short italic tag ("current", "stale").
        A name ending in "/" is a folder. Each file gets a role-coloured tick so status reads before the tag.
        (x, y) is the top-left; returns the height."""
        size = size or self.size - 0.5
        bar = row_h + 0.8 if title else 0
        H = bar + len(rows) * row_h + 1.6
        c = role(r)
        self.box(x, y - H, w, H, fill="white", stroke=c["stroke"], radius=1.0, z=z, container=True)
        if title:
            self.ax.add_patch(Rectangle((x + 0.3, y - bar), w - 0.6, bar - 0.3, fc=c["soft"], ec="none", zorder=z + 0.5))
            for k, col in enumerate(("#E0645A", "#E8B23A", "#5DB86A")):
                self.ax.add_patch(Circle((x + 2.2 + k * 1.9, y - bar / 2), 0.6, fc=col, ec="none", zorder=z + 1))
            self.text(x + 8.4, y - bar / 2, title, size=size, ha="left", weight="bold", color=c["ink"],
                      family="monospace", z=z + 1)
        for i, (depth, name, status, rr) in enumerate(rows):
            cy = y - bar - 0.8 - (i + 0.5) * row_h
            tx = x + 1.8 + depth * indent
            rc = role(rr)
            folder = name.endswith("/")
            if folder:
                self.ax.add_patch(Rectangle((tx, cy - 0.9), 2.4, 1.7, fc="#F2B33D", ec="none", zorder=z + 1))
            else:
                self.ax.add_patch(Rectangle((tx + 0.7, cy - 1.0), 0.6, 2.0, fc=rc["mark"], ec="none", zorder=z + 1))
            self.text(tx + 3.0, cy, name, size=size, ha="left", family="monospace",
                      weight="bold" if folder or status == "current" else "normal", z=z + 1)
            if status:
                self.text(x + w - 1.5, cy, status, size=size, ha="right", style="italic", weight="bold",
                          color=rc["ink"], z=z + 1)
        return H

    # ---- showcase devices: layered plates, logo tiles, radar (toolspace-study-2026-11.md) ----
    def plate(self, x, y, w, d, *, skew=None, t=2.8, r="blue", label=None, size=None, grad=None, lw=0.5, z=3,
              shadow=True, label_color="white"):
        """Isometric platform: a layer that objects stand on (ToolSpace Fig. 1, a tool layer floating over an
        environment layer). (x, y) is the front-left corner of the top face, w its width and d its depth on the
        page; the back edge is shifted right by skew (default 0.55 d). t is the slab thickness, drawn as a darker
        front face and right face; label is set on the front face. grad=(front, back) overrides the top-face
        gradient. Stand tiles on it with the returned at(u, v): u along the front edge, v from front (0) to back
        (1). A plate is a container: wires may land on it. Returns a namespace with at, top (corners), front."""
        from types import SimpleNamespace
        c = role(r)
        skew = 0.55 * d if skew is None else skew
        A, B, C, D = (x, y), (x + w, y), (x + w + skew, y + d), (x + skew, y + d)
        if shadow:
            self.ax.add_patch(Polygon([(px + 0.5, py - t - 0.8) for px, py in (A, B, C, D)], fc="#1A2230",
                                      ec="none", alpha=0.08, zorder=z - 0.3))
        c0, c1 = grad or (mix(c["fill"], "#FFFFFF", 0.3), mix(c["soft"], c["mark"], 0.14))
        top = Polygon([A, B, C, D], fc="none", ec=c["stroke"], lw=lw, zorder=z + 0.2, joinstyle="round")
        im = self.ax.imshow(np.linspace(1, 0, 256)[:, None], extent=(min(x, x + skew), max(x + w, x + w + skew), y, y + d), aspect="auto",
                            cmap=mcolors.LinearSegmentedColormap.from_list("g", [c0, c1]), zorder=z,
                            interpolation="bicubic")
        self.ax.add_patch(top)
        im.set_clip_path(top)
        side = mix(c["mark"], "#000000", 0.25)
        self.ax.add_patch(Polygon([A, B, (B[0], B[1] - t), (A[0], A[1] - t)], fc=c["mark"], ec=c["mark"], lw=0.3,
                                  zorder=z + 0.1, joinstyle="round"))
        self.ax.add_patch(Polygon([B, C, (C[0], C[1] - t), (B[0], B[1] - t)], fc=side, ec=side, lw=0.3,
                                  zorder=z + 0.1, joinstyle="round"))
        if label:
            self.text(x + w / 2, y - t / 2, label, size=size or self.size, color=label_color, weight="bold", z=z + 1)
        self.ax.set_xlim(0, self.w)
        self.ax.set_ylim(0, self.h)
        return SimpleNamespace(at=lambda u, v: (x + u * w + v * skew, y + v * d), top=(A, B, C, D),
                               front=(x, y - t, w, t))

    def tile(self, cx, cy, s, *, image=None, glyph=None, label=None, inside=False, r="neutral", size=None,
             color=None, radius=None, lw=0.45, z=9, shadow=True, weight="bold", pad=0.17, fill="white"):
        """Upright rounded tile carrying a product mark or a glyph: the unit of a logo row or of the tools standing
        on a plate. image = path of a logo (drawn once, unmodified, in its own colours); glyph = name of an icon_*
        method or a callable(cx, cy, size). label goes under the tile, or inside its lower third with inside=True
        (tool tiles). r colours the border, the glyph and an inside label. Always pair a logo with its name unless
        the mark contains it. Returns the tile patch; the tile is opaque to the wire audit."""
        c = role(r)
        rad = s * 0.2 if radius is None else radius
        size = size or self.size - 1.0
        if shadow:
            self.ax.add_patch(FancyBboxPatch((cx - s / 2 + 0.3, cy - s / 2 - 0.4), s, s, lw=0, fc="#1A2230",
                                             boxstyle=f"round,pad=0,rounding_size={rad}", alpha=0.10, zorder=z - 0.2))
        p = FancyBboxPatch((cx - s / 2, cy - s / 2), s, s, boxstyle=f"round,pad=0,rounding_size={rad}", fc=fill,
                           ec=c["stroke"], lw=lw, zorder=z)
        self.ax.add_patch(p)
        self.solids.append((cx - s / 2, cy - s / 2, s, s, f"tile '{label or ''}'", p))
        iy, isz = cy, s * (1 - 2 * pad)
        if label and inside:
            iy, isz = cy + s * 0.14, s * 0.46
            self.text(cx, cy - s * 0.29, label, size=size, color=color or c["ink"], weight=weight, z=z + 2)
        elif label:
            self.text(cx, cy - s / 2 - 0.45 - size * 0.3528 * 0.55, label, size=size, color=color or INK,
                      weight=weight, z=z + 2)
        if image:
            self.image(image, cx, iy, isz, fit="box", z=z + 1)
        elif callable(glyph):
            glyph(cx, iy, isz)
        elif glyph:
            fn = getattr(self, f"icon_{glyph}")
            fn(cx, iy, isz, **({"color": c["mark"]} if "color" in fn.__code__.co_varnames else {"r": r}))
        return p

    def radar(self, cx, cy, R, axes, series, *, hero=0, scale="axis", vmax=None, rings=4, size=None, fmt="{:.1f}",
              gap=1.3, start=90.0, lead=True, fill=0.13, z=6):
        """Radar (profile) chart for an envelope claim: one model against at most three others on 5 to 8 axes,
        where the reader should see one polygon enclose the rest. axes = names; series = [(name, values, role)];
        series[hero] is drawn last with a heavier line, vertex dots and its value printed at every vertex. With
        lead=True an axis the hero does not win also prints the winning value in that series' ink, so the envelope
        cannot hide a loss. scale="axis" runs every axis from 0 to its own best score (state this in the caption or
        a note: radial lengths are then comparable along an axis, not across axes); scale="shared" runs all axes
        from 0 to vmax (default: the largest value). Use a dot-row chart instead when exact gaps matter more than
        the shape, or with more than four polygons. Returns {series name: [(x, y), ...]} vertex positions."""
        size = size or self.size
        n = len(axes)
        ang = [math.radians(start - 360.0 * i / n) for i in range(n)]
        top = [max(s[1][i] for s in series) for i in range(n)]
        if scale == "shared":
            top = [vmax or max(top)] * n
        assert all(t > 0 for t in top), "radar: an axis with no positive value"

        def ring(f):
            return [(cx + R * f * math.cos(a), cy + R * f * math.sin(a)) for a in ang]

        self.ax.add_patch(Polygon(ring(1.0), fc="#FBFCFD", ec="none", zorder=z - 0.5))
        for k in range(1, rings + 1):
            self.ax.add_patch(Polygon(ring(k / rings), fc="none", ec="#C3C9D2", lw=0.35 if k < rings else 0.5,
                                      ls=(0, (2.2, 1.6)), zorder=z - 0.4))
        for px, py in ring(1.0):
            self.ax.plot([cx, px], [cy, py], color="#C3C9D2", lw=0.35, ls=(0, (2.2, 1.6)), zorder=z - 0.4)
        out = {}
        order = [i for i in range(len(series)) if i != hero] + [hero]
        for i in order:
            name, vals, r = series[i]
            c, h = role(r), i == hero
            pts = [(cx + R * v / t * math.cos(a), cy + R * v / t * math.sin(a)) for v, t, a in zip(vals, top, ang)]
            out[name] = pts
            self.ax.add_patch(Polygon(pts, fc=mcolors.to_rgba(c["mark"], fill if h else fill * 0.6), ec=c["mark"],
                                      lw=1.25 if h else 0.85, zorder=z + (1 if h else 0) + 0.01 * i,
                                      joinstyle="round"))
            if h:
                for px, py in pts:
                    self.ax.add_patch(Circle((px, py), 0.5, fc=c["mark"], ec="white", lw=0.3, zorder=z + 2))
        hv, hink = series[hero][1], role(series[hero][2])["ink"]
        lh = size * 0.3528 * 1.22
        for i, (a, name) in enumerate(zip(ang, axes)):
            ca, sa = math.cos(a), math.sin(a)
            px, py = cx + (R + gap) * ca, cy + (R + gap) * sa
            ha = "left" if ca > 0.25 else "right" if ca < -0.25 else "center"
            seg = [(fmt.format(hv[i]), hink, "bold")]
            best = max(range(len(series)), key=lambda k: series[k][1][i])
            if lead and series[best][1][i] > hv[i]:
                seg.append(("  " + fmt.format(series[best][1][i]), role(series[best][2])["ink"], "normal"))
            # the value sits next to the vertex and the axis name (one or two lines) beyond it
            vy, vva, ny, nva = ((py, "bottom", py + lh, "bottom") if sa > 0.25 else
                                (py, "top", py - lh, "top") if sa < -0.25 else
                                (py + 0.15, "bottom", py - 0.15, "top"))
            self.rich(px, vy, seg, size=size, ha=ha, va=vva, z=z + 3)
            self.text(px, ny, name, size=size, weight="bold", ha=ha, va=nva, z=z + 3, linespacing=1.12)
        return out

    def legend(self, x, y, w, items, *, size=None, frame=True, gap=3.2, glyph=4.2, row_h=None, r="neutral",
               dashed=True, pad=1.6, z=10):
        """Glyph key in a dashed strip, laid out like words: items = [(kind, arg, label)], kind in
        op | snow | flame | lock | cycle | box | cuboid | fmap | line | dash | abbr. Every symbol the reader meets
        unlabelled (⊕ ⓒ ⊗, snowflake, flame, dashed = train only, an abbreviation) gets one entry; this is the
        figure's key, so the panels can stay terse. (x, y) is the bottom-left; returns the strip height."""
        size = size or self.size - 0.4
        row_h = row_h or max(4.2, size * 0.62)

        def gwidth(kind, arg):
            return self.text_width(arg, size, "bold") + 1.8 if kind == "abbr" else glyph

        widths = [gwidth(k, a) + 1.0 + self.text_width(lab, size) for k, a, lab in items]
        rows, cur = [], []
        for it, iw in zip(items, widths):
            if cur and sum(cw for _, cw in cur) + gap * len(cur) + iw > w - 2 * pad:
                rows.append(cur)
                cur = []
            cur.append((it, iw))
        rows.append(cur)
        H = len(rows) * row_h + 2 * pad - 1.0
        if frame:
            self.ax.add_patch(FancyBboxPatch((x, y), w, H, boxstyle="round,pad=0,rounding_size=1.6", fc="white",
                                             ec=role(r)["stroke"], lw=0.6, ls=(0, (3, 2)) if dashed else "-",
                                             zorder=z - 1))
        yy = y + H - pad - row_h / 2 + 0.5
        for row in rows:
            xx = x + pad
            for (kind, arg, lab), iw in row:
                gw = gwidth(kind, arg)
                gx = xx + gw / 2
                if kind == "op":
                    self.op(gx, yy, arg, d=2.8, z=z)
                elif kind in ("snow", "lock", "cycle"):
                    getattr(self, f"icon_{kind}")(gx, yy, 2.7, color=arg or "#4A90C8", z=z)
                elif kind == "flame":
                    self.icon_flame(gx, yy, 2.7, z=z)
                elif kind == "box":
                    self.box(gx - 1.9, yy - 1.2, 3.8, 2.4, arg, radius=0.6, lw=0.5, z=z)
                elif kind == "cuboid":
                    self.cuboid(gx - 1.7, yy - 1.3, 2.6, 2.2, d=1.0, r=arg, z=z)
                elif kind == "fmap":
                    self.fmap(gx - 1.6, yy - 1.3, 3.2, 2.6, cmap=arg, z=z)
                elif kind in ("line", "dash"):
                    self.arrow([(gx - 2.0, yy), (gx + 2.0, yy)], color=arg or LINE, dashed=kind == "dash", head=1.1,
                               z=z)
                elif kind == "abbr":
                    self.box(xx, yy - 1.3, gw, 2.6, "neutral", radius=0.6, lw=0.5, z=z)
                    self.text(gx, yy, arg, size=size, weight="bold", z=z + 1)
                self.text(xx + gw + 1.0, yy, lab, size=size, ha="left", z=z + 1)
                xx += iw + gap
            yy -= row_h
        return H

    # ---- connectors ---------------------------------------------------------
    def arrow(self, pts, color=LINE, lw=0.7, head=1.4, dashed=False, radius=1.2, z=8, both=False,
              start_dot=False, halo=False, dotted=False):
        """Polyline arrow with rounded elbows and a filled head (head in mm).
        Route orthogonally; end exactly on the target border. halo=True lays a white casing under the
        line so an unavoidable crossing reads as a bridge over the other wire (draw it with a higher z).
        dashed / dotted style the shaft only; the head stays solid."""
        pts = _dedupe(pts)
        self.wires.append((pts, None))
        if halo:
            self.ax.add_patch(PathPatch(_rounded_path(pts[:-1] + [pts[-1]], radius), fc="none", ec="white",
                                        lw=lw + 2.6, zorder=z - 0.05, capstyle="butt"))
        style = f"{'<|-|>' if both else '-|>'},head_length={head * 0.95},head_width={head * 0.42}"
        kw = dict(arrowstyle=style, mutation_scale=PT_PER_MM, lw=lw, color=color, zorder=z, shrinkA=0, shrinkB=0,
                  joinstyle="miter", capstyle="butt")
        if (dashed or dotted) and len(pts) >= 2:
            self.ax.add_patch(PathPatch(_rounded_path(pts, radius), fc="none", ec=color, lw=lw, zorder=z,
                                        ls=(0, (1.2, 1.8)) if dotted else (0, (3.2, 1.8)), capstyle="butt"))

            def stub(tip, back):  # a solid piece just long enough to carry the head
                L = math.hypot(tip[0] - back[0], tip[1] - back[1])
                f = min(1.0, head / L) if L else 0.0
                return (tip[0] + (back[0] - tip[0]) * f, tip[1] + (back[1] - tip[1]) * f)

            if both:
                self.ax.add_patch(FancyArrowPatch(posA=stub(pts[0], pts[1]), posB=pts[0],
                                                  **{**kw, "arrowstyle": style.replace("<|-|>", "-|>")}))
            a = FancyArrowPatch(posA=stub(pts[-1], pts[-2]), posB=pts[-1],
                                **{**kw, "arrowstyle": style.replace("<|-|>", "-|>")})
        else:
            a = FancyArrowPatch(path=_rounded_path(pts, radius), **kw)
        self.ax.add_patch(a)
        if start_dot:
            self.ax.add_patch(Circle(pts[0], 0.45, fc=color, ec="none", zorder=z))
        return a

    def line(self, pts, color=LINE, lw=0.6, dashed=False, z=7, radius=1.0, alpha=1):
        pts = _dedupe(pts)
        self.wires.append((pts, None))
        self.ax.add_patch(PathPatch(_rounded_path(pts, radius), fc="none", ec=color,
                                    lw=lw, zorder=z, ls=(0, (3.2, 1.8)) if dashed else "-", alpha=alpha,
                                    capstyle="round", joinstyle="round"))

    def thread(self, p0, p1, color=LINE, lw=0.9, bend=0.5, d=1.1, dashed=False, z=9):
        """A relation between two things, not a flow: a smooth curve with a dot at each end and no head
        (visual-craft section 9). Use it to join a marked span to the object it matches or implies; take the
        ends from self.spans. It leaves and arrives vertically, so stack the two things. bend = how far the
        curve keeps its direction, as a share of the vertical gap."""
        (x0, y0), (x1, y1) = p0, p1
        k = bend * (y1 - y0)
        path = Path([p0, (x0, y0 + k), (x1, y1 - k), p1], [Path.MOVETO] + [Path.CURVE4] * 3)
        self.ax.add_patch(PathPatch(path, fc="none", ec=color, lw=lw, zorder=z, capstyle="round",
                                    ls=(0, (3.2, 1.8)) if dashed else "-"))
        self.dot(x0, y0, color, d, z + 0.1)
        self.dot(x1, y1, color, d, z + 0.1)

    def dot(self, x, y, color=LINE, d=0.9, z=9):
        self.ax.add_patch(Circle((x, y), d / 2, fc=color, ec="none", zorder=z))

    def block_arrow(self, x0, y0, x1, y1, width=3.0, color="#D5D9DF", head=None, z=3):
        """Fat neutral arrow for stage-to-stage flow (IdeaScientist style)."""
        head = head or width * 1.1
        L = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        nx, ny = -uy, ux
        hw, bw = width, width * 0.5
        bx, by = x1 - ux * head, y1 - uy * head
        pts = [(x0 + nx * bw / 2, y0 + ny * bw / 2), (bx + nx * bw / 2, by + ny * bw / 2),
               (bx + nx * hw / 2, by + ny * hw / 2), (x1, y1), (bx - nx * hw / 2, by - ny * hw / 2),
               (bx - nx * bw / 2, by - ny * bw / 2), (x0 - nx * bw / 2, y0 - ny * bw / 2)]
        self.ax.add_patch(Polygon(pts, fc=color, ec="none", zorder=z))

    def zoom(self, src, dst, color="#8C9DB5", lw=0.5, z=2, fill=None, alpha=0.35):
        """Zoom rays from a source rect (x,y,w,h) to a detail rect (to the right or below)."""
        sx, sy, sw, sh = src
        dx, dy, dw, dh = dst
        if dx >= sx + sw:
            a, b, c, d = (sx + sw, sy + sh), (sx + sw, sy), (dx, dy + dh), (dx, dy)
        else:
            a, b, c, d = (sx, sy), (sx + sw, sy), (dx, dy + dh), (dx + dw, dy + dh)
        if fill:
            self.ax.add_patch(Polygon([a, c, d, b], fc=fill, ec="none", alpha=alpha, zorder=z - 0.1))
        for p, q in ((a, c), (b, d)):
            self.ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=(0, (2.5, 1.6)), zorder=z)

    def brace(self, x, y0, y1, side="left", color=LINE, lw=0.6, depth=1.4, z=8):
        """Vertical curly brace spanning y0..y1 at x; returns the tip point."""
        s = -1 if side == "left" else 1
        ym = (y0 + y1) / 2
        q = depth * 0.5
        v = [(x, y0), (x + s * q, y0), (x + s * q, y0 + q), (x + s * q, ym - q), (x + s * q, ym),
             (x + s * depth, ym), (x + s * q, ym), (x + s * q, ym + q), (x + s * q, y1 - q), (x + s * q, y1), (x, y1)]
        c = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3,
             Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3]
        self.ax.add_patch(PathPatch(Path(v, c), fc="none", ec=color, lw=lw, zorder=z))
        return (x + s * depth, ym)

    # ---- export ---------------------------------------------------------------
    def save(self, stem, png_dpi=None, formats=("pdf", "svg", "png")):
        _P(stem).parent.mkdir(parents=True, exist_ok=True)
        out = []
        for f in formats:
            p = f"{stem}.{f}"
            # vector formats rasterise images at the savefig dpi (default: the figure's 100 dpi) and merge
            # neighbouring images into one composite at that dpi; both turn a 600 dpi icon into a few pixels
            kw = {"dpi": (png_dpi or RASTER_DPI) if f == "png" else RASTER_DPI}
            if f == "pdf":
                kw["metadata"] = {"Creator": "paperkit", "CreationDate": None}
            with matplotlib.rc_context({"image.composite_image": False}):
                self.fig.savefig(p, **kw)
            if f == "pdf":
                check_embedded(p, self.rasters)
            out.append(p)
        return out


# ------------------------------------------------------------ path helpers ---
def wrap_marked(segments, measure, maxw):
    """Word wrap for Canvas.para. segments = [(text, color, weight, mark)]; measure(str) -> width in mm.
    Fewest lines; the last line is at least a third of the width when that is possible (no orphan) and the
    lines above it are as full as they can be. A space keeps its mark only inside a span, so a band never
    starts or ends on a space. Returns lines of runs in the same format."""
    chars = [(ch, tuple(s[1:])) for s in segments for ch in s[0]]
    words, cur = [], []
    for k, (ch, a) in enumerate(chars):
        if ch == " ":
            inside = 0 < k < len(chars) - 1 and chars[k - 1][1] == a == chars[k + 1][1]
            words.append((cur, a if inside else a[:-1] + (None,)))
            cur = []
        else:
            cur.append((ch, a))
    words.append((cur, None))
    n = len(words)

    def line(i, j):  # words i..j-1 as characters, no trailing space
        return [c for word, space in words[i:j] for c in word + [(" ", space)]][:-1]

    width = {(i, j): measure("".join(ch for ch, _ in line(i, j))) for i in range(n) for j in range(i + 1, n + 1)}
    best = {(n, 0): (0.0, None)}  # (start word, lines left) -> (cost, next start)
    for left in range(1, n + 1):
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n + 1):
                if (width[i, j] > maxw and j > i + 1) or (j, left - 1) not in best:
                    continue  # a single word wider than the column still gets a line of its own
                slack = max(0.0, maxw - width[i, j])
                cost = (1e6 if slack > 2 * maxw / 3 else 0.0) if j == n else slack ** 2
                cost += best[j, left - 1][0]
                if (i, left) not in best or cost < best[i, left][0]:
                    best[i, left] = (cost, j)
        if (0, left) in best:
            break
    out, i = [], 0
    while i < n:
        j = best[i, left][1]
        runs = []
        for ch, a in line(i, j):
            if runs and runs[-1][1] == a:
                runs[-1][0] += ch
            else:
                runs.append([ch, a])
        out.append([(t,) + a for t, a in runs])
        i, left = j, left - 1
    return out


def _dedupe(pts):
    """Points as tuples with consecutive repeats removed (computed routes often repeat a corner)."""
    pts = [tuple(p) for p in pts]
    return [q for i, q in enumerate(pts) if i == 0 or q != pts[i - 1]]


def _open_rgb(png):
    """Open an image as RGB on white: a transparent background counts as paper, not as black ink."""
    from PIL import Image
    im = Image.open(png).convert("RGBA")
    return Image.alpha_composite(Image.new("RGBA", im.size, "white"), im).convert("RGB")


def _rounded_path(pts, r):
    """Polyline with quadratic-rounded corners (radius r mm)."""
    if len(pts) < 3 or r <= 0:
        return Path(pts)
    verts, codes = [pts[0]], [Path.MOVETO]
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = (np.array(pts[j], float) for j in (i - 1, i, i + 1))
        d0, d1 = p1 - p0, p2 - p1
        l0, l1 = np.linalg.norm(d0), np.linalg.norm(d1)
        rr = min(r, l0 / 2, l1 / 2)
        a, b = p1 - d0 / l0 * rr, p1 + d1 / l1 * rr
        verts += [tuple(a), tuple(p1), tuple(b)]
        codes += [Path.LINETO, Path.CURVE3, Path.CURVE3]
    verts.append(pts[-1])
    codes.append(Path.LINETO)
    return Path(verts, codes)


def _smooth(pts):
    """Closed smooth path through the midpoints of pts (quadratic B-spline)."""
    pts = [np.array(p, float) for p in pts]
    mids = [(pts[i] + pts[(i + 1) % len(pts)]) / 2 for i in range(len(pts))]
    verts, codes = [tuple(mids[-1])], [Path.MOVETO]
    for i in range(len(pts)):
        verts += [tuple(pts[i]), tuple(mids[i])]
        codes += [Path.CURVE3, Path.CURVE3]
    verts.append(verts[0])
    codes.append(Path.CLOSEPOLY)
    return Path(verts, codes)


def _clip_len(x0, y0, x1, y1, a0, b0, a1, b1):
    """Length of segment (x0,y0)-(x1,y1) inside the rectangle [a0,a1] x [b0,b1] (Liang-Barsky)."""
    if a1 <= a0 or b1 <= b0:
        return 0.0
    dx, dy, t0, t1 = x1 - x0, y1 - y0, 0.0, 1.0
    for p, q in ((-dx, x0 - a0), (dx, a1 - x0), (-dy, y0 - b0), (dy, b1 - y0)):
        if p == 0:
            if q < 0:
                return 0.0
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return 0.0
    return (t1 - t0) * math.hypot(dx, dy)


def _field(rng, n=64, blobs=3):
    """Smooth illustrative 2-D field in [0, 1]: a few Gaussian blobs over a low-frequency ripple."""
    yy, xx = np.mgrid[0:1:n * 1j, 0:1:n * 1j]
    f = 0.18 * np.sin(2 * math.pi * (rng.uniform(0.6, 1.6) * xx + rng.uniform(0, 1))) * \
        np.cos(2 * math.pi * (rng.uniform(0.6, 1.6) * yy + rng.uniform(0, 1)))
    for _ in range(blobs):
        cx, cy, s = rng.uniform(0.15, 0.85), rng.uniform(0.15, 0.85), rng.uniform(0.08, 0.22)
        f += rng.uniform(0.5, 1.0) * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * s * s))
    return (f - f.min()) / (f.max() - f.min())


def _round_top_rect(x, y, w, h, r):
    r = min(r, h)
    v = [(x, y), (x + w, y), (x + w, y + h - r), (x + w, y + h), (x + w - r, y + h),
         (x + r, y + h), (x, y + h), (x, y + h - r), (x, y)]
    c = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3,
         Path.CURVE3, Path.CLOSEPOLY]
    return Path(v, c)


# ------------------------------------------------------------- chart style ---
def chart_axes(ax, grid="x", size=7.0, box=False):
    """Chart defaults: light grid on the value axis only, short outward ticks, muted tick labels.
    Open (left + bottom spines) by default; box=True keeps the full frame, which most ML and systems venues
    use for line plots and which separates the panels of a tight small-multiples grid."""
    ax.set_facecolor("none")  # an opaque plot area sits above the canvas and hides labels placed there in mm
    for s in ("top", "right"):
        ax.spines[s].set_visible(box)
    for s in ("left", "bottom") + (("top", "right") if box else ()):
        ax.spines[s].set_color("#9AA0A8")
        ax.spines[s].set_linewidth(0.6)
    ax.tick_params(length=2.2, width=0.6, color="#9AA0A8", labelsize=size - 0.5, labelcolor="#4A5059", pad=1.5)
    if grid:
        ax.grid(axis=grid, color="#E3E6EA", lw=0.5, zorder=0)
        ax.set_axisbelow(True)
    return ax


def curve_label(ax, xs, ys, i, text, size=6.5, color="black", boxed=True, **kw):
    """Label a curve or boundary on the curve itself, rotated to its local slope at index i, in a small white
    rounded box (phase boundaries, reference lines, power laws). Replaces a legend entry for a line that is
    not a data series. Works on log axes: the rotation is taken through the axes transform."""
    j = min(max(i, 1), len(xs) - 1)
    ang = math.degrees(math.atan2(ys[j] - ys[j - 1], xs[j] - xs[j - 1]))
    box = dict(boxstyle="round,pad=0.22,rounding_size=0.5", fc="white", ec=color, lw=0.5) if boxed else None
    return ax.text(xs[i], ys[i], text, fontsize=size, color=color, rotation=ang, rotation_mode="anchor",
                   transform_rotates_text=True, ha="center", va="center", bbox=box, zorder=6, **kw)


def density(png):
    """(white, tint, ink) percentages of a rendered figure: grey >=250, 200-249, <120."""
    a = np.asarray(_open_rgb(png).convert("L"), float)
    return tuple(round(100 * float(v), 1) for v in ((a >= 250).mean(), ((a >= 200) & (a < 250)).mean(), (a < 120).mean()))


def compare(original, new, out, width=1600, labels=("original", "redesign")):
    """Stack two renders at the same pixel width (original on top) for a side-by-side review."""
    from PIL import Image, ImageDraw
    ims = []
    for p in (original, new):
        im = Image.open(p).convert("RGB")
        ims.append(im.resize((width, round(im.height * width / im.width))))
    canvas = Image.new("RGB", (width, sum(i.height for i in ims) + 60), "white")
    y = 0
    for lab, im in zip(labels, ims):
        ImageDraw.Draw(canvas).text((8, y + 4), lab, fill=(200, 40, 40))
        canvas.paste(im, (0, y + 24))
        y += im.height + 30
    canvas.save(out)
    return out


def visual_stats(png, width=1600):
    """At a fixed pixel width: empty % (16 px blocks that are flat white), colour % (saturated pixels),
    picture % (blocks with illustration-like texture: many distinct tones)."""
    im = _open_rgb(png)
    im = im.resize((width, max(1, round(im.height * width / im.width))))
    g = np.asarray(im.convert("L"), float)
    hsv = np.asarray(im.convert("HSV"), float)
    b = min(16, g.shape[0])
    H, W = (g.shape[0] // b) * b, (g.shape[1] // b) * b
    blk = g[:H, :W].reshape(H // b, b, W // b, b).swapaxes(1, 2).reshape(-1, b * b)
    empty = ((blk.min(axis=1) >= 245) & (blk.std(axis=1) < 2)).mean()
    tones = np.array([len(np.unique((r // 12).astype(int))) for r in blk])
    picture = ((tones >= 9) & (blk.std(axis=1) > 14)).mean()
    colour = ((hsv[..., 1] > 60) & (hsv[..., 2] > 60)).mean()
    return {"empty": round(100 * empty, 1), "colour": round(100 * colour, 1), "picture": round(100 * picture, 1)}


def parity(original, new):
    """Redesign parity check: a redesign must not be emptier, greyer or less illustrated than the original
    it claims to beat unless the brief says so. 'Cleaner' that is really 'emptier' is the most common way a
    redesign of an illustrated survey figure loses (Proactive AI, first attempt). Returns (stats, warnings)."""
    o, n = visual_stats(original), visual_stats(new)
    warn = []
    if n["empty"] > o["empty"] + 8:
        warn.append(f"emptier: {n['empty']}% empty blocks vs {o['empty']}% (fill cards, enlarge content, cut canvas)")
    if n["colour"] < 0.6 * o["colour"]:
        warn.append(f"greyer: {n['colour']}% saturated vs {o['colour']}% (solid headers, filled chips, vignettes)")
    if n["picture"] < 0.6 * o["picture"]:
        warn.append(f"less illustrated: {n['picture']}% picture vs {o['picture']}% (keep what the pictures taught)")
    return {"original": o, "redesign": n}, warn


def fill(png, width_mm, chart=False):
    """Does the figure use its placement? Returns (empty %, limit %, advice or None). `empty` is the share of
    flat white blocks (visual_stats). Limits come from this skill's gallery: full-width diagrams sit at 14-44 %
    empty, column schematics at 38-69 %, chart figures at 55-56 %. A full-width diagram above 50 % is a column
    figure drawn too wide, or a set of small islands on a big page; both read as unfinished."""
    empty = visual_stats(png)["empty"]
    limit = (72 if width_mm < 120 else 50) + (12 if chart else 0)
    if empty <= limit:
        return empty, limit, None
    if width_mm >= 120:
        how = ("redraw it at column width (76-85 mm), or keep the width and make the objects earn it: larger "
               "drawn objects and type (8-10 pt), one spine joining the panels, the hero at 40 % or more of the "
               "area. Do not add decoration and do not shrink the canvas to the same sparse drawing")
    else:
        how = "cut the canvas height to the content, or enlarge the objects until they fill the column"
    return empty, limit, f"{empty}% of the canvas is blank (limit {limit}% at {width_mm:g} mm): {how}"


def swatches(pngs, out, k=8, height=260):
    """Series check: the figures side by side, each with its k most-used saturated colours underneath.
    A taxonomy item whose swatch changes between figures is a palette drift to fix (Proactive AI's 6A)."""
    from PIL import Image, ImageDraw
    tiles, palettes = [], []
    for p in pngs:
        im = Image.open(p).convert("RGB")
        im.thumbnail((10_000, height))
        tiles.append(im)
        # sample only saturated pixels: pale fills and thin coloured strokes would otherwise lose to white
        a = np.asarray(im.convert("HSV")).reshape(-1, 3)
        sat = a[(a[:, 1] > 70) & (a[:, 2] > 60)]
        rgb = np.asarray(im).reshape(-1, 3)[(a[:, 1] > 70) & (a[:, 2] > 60)]
        cols = []
        if len(rgb):
            strip = Image.fromarray(rgb[None, :, :].astype("uint8"))
            q = strip.quantize(colors=24, method=Image.Quantize.MEDIANCUT)
            pal = q.getpalette()
            for n, i in sorted(q.getcolors(), reverse=True):
                hexc = "#%02X%02X%02X" % tuple(pal[3 * i:3 * i + 3])
                if all(sum(abs(int(hexc[j:j + 2], 16) - int(c[j:j + 2], 16)) for j in (1, 3, 5)) > 60 for c in cols):
                    cols.append(hexc)
                if len(cols) == k:
                    break
        palettes.append(cols)
    W = sum(t.width for t in tiles) + 20 * (len(tiles) + 1)
    sheet = Image.new("RGB", (W, height + 110), "white")
    d = ImageDraw.Draw(sheet)
    x = 20
    for t, cols, p in zip(tiles, palettes, pngs):
        sheet.paste(t, (x, 10))
        for j, c in enumerate(cols):
            d.rectangle([x + j * 34, height + 22, x + j * 34 + 28, height + 50], fill=c)
            d.text((x + j * 34, height + 54), c[1:], fill="#333333")
        d.text((x, height + 80), os.path.basename(p), fill="#333333")
        x += t.width + 20
    sheet.save(out)
    return out, palettes


# ------------------------------------------------------------ caption check ---
NOTE_NOISE = [  # (what the reader does not need, pattern): a caption says what is shown, not how it was made
    ("how the artwork was made",
     r"\b(generated|drawn|created|made|produced|rendered|illustrated)\s+(with|by|using|in)\b[^.;]{0,30}"
     r"\b(codex|chatgpt|dall-?e|midjourney|stable diffusion|gpt-image|image[- ]generation)|\brecolou?red by\b"
     r"|\b(icons?|illustrations?|images?|artwork|drawings?|vignettes?|pictures?)\s+(were|was|are|is)\s+"
     r"(generated|drawn|created|made|produced|rendered)\b"),
    ("how marks are drawn",
     r"\b(offset|nudged|jittered|dodged|moved apart|spread apart)\b[^.;:]{0,40}\b(marks?|markers?|points?|labels?|dots?)\b"
     r"|\b(marks?|markers?|points?|labels?|dots?)\b[^.;:]{0,40}\b(offset|nudged|jittered|dodged|moved apart|spread apart)\b"
     r"|\bleast amount\b"),
    ("procedure that belongs in the methods",
     r"\bbefore any (model )?(call|run|experiment|evaluation)s?\b|\bfixed (in advance|beforehand|before)\b"),
    ("disclaimer that changes no reading",
     r"\b(names?|examples?|people|persons?|users?|personas?|characters?)\s+(are|is)\s+"
     r"(illustrative|fictional|fictitious|invented|made[- ]up|hypothetical)\b"),
]


def note_issues(text):
    """Phrases in a caption or note that narrate production, drawing mechanics or protocol instead of content."""
    import re
    return [(why, m.group(0)) for why, pat in NOTE_NOISE for m in re.finditer(pat, text, re.I)]


def counts(pdf):
    """Text sizes and stroke widths actually in a figure PDF, each with its number of uses, for the budgets
    of visual-craft section 14 (2-3 sizes, 1-2 weights). Needs PyMuPDF, like check_figure.py. Math subscripts
    (0.7 x a base size) and strokes inside icons show up too; read the list with that in mind."""
    import fitz  # PyMuPDF
    from collections import Counter
    pages = list(fitz.open(pdf))  # a figure PDF is one page; count them all if there are more
    sizes = Counter(round(s["size"], 1) for page in pages for b in page.get_text("dict")["blocks"]
                    for ln in b.get("lines", []) for s in ln["spans"] if s["text"].strip())
    strokes = Counter(round(d["width"], 2) for page in pages for d in page.get_drawings()
                      if d.get("width") and "s" in d.get("type", ""))
    return dict(sorted(sizes.items(), reverse=True)), dict(sorted(strokes.items(), reverse=True))


if __name__ == "__main__" and len(__import__("sys").argv) > 1:
    import sys
    cmd, args = sys.argv[1], sys.argv[2:]
    USAGE = ("usage: paperkit.py [density PNG... | compare ORIGINAL NEW OUT | parity ORIGINAL NEW | "
             "swatches PNG... OUT | caption FILE_OR_TEXT | grey PNG OUT | counts PDF... | "
             "fill PNG WIDTH_MM [chart]]")
    if len(args) < {"density": 1, "compare": 3, "parity": 2, "swatches": 2, "caption": 1, "grey": 2,
                    "counts": 1, "fill": 2}.get(cmd, 0):
        sys.exit(USAGE)
    if cmd == "counts":  # what the budgets count: text sizes and stroke widths in the exported PDF
        for p in args:
            sizes, strokes = counts(p)
            print(p)
            print("  text sizes (pt: spans)    ", "  ".join(f"{k}: {v}" for k, v in sizes.items()))
            print("  stroke widths (pt: paths) ", "  ".join(f"{k}: {v}" for k, v in strokes.items()))
    elif cmd == "density":
        for p in args:
            wh, ti, ink = density(p)
            print(p, "white/tint/ink %", (wh, ti, ink))
            if wh < 40:  # 41 measured award figures: white 41-96 %, median ~71 % (venue-study-2026-11)
                print(f"  crowded: {wh}% white. Tinted panel bodies and frames around everything are the usual "
                      "cause; let the page be the ground and tint only what the tint explains")
    elif cmd == "fill":  # paperkit.py fill fig.png 178 [chart]: exit 1 if the placement is mostly blank
        empty, limit, advice = fill(args[0], float(args[1]), chart="chart" in args[2:])
        print(f"FAIL {advice}" if advice else f"ok: {empty}% blank (limit {limit}%)")
        sys.exit(1 if advice else 0)
    elif cmd == "grey":  # what a greyscale printout shows: every series must still be told apart
        _open_rgb(args[0]).convert("L").save(args[1])
        print(args[1])
    elif cmd == "compare":
        # a first argument from assets/models is a model figure, not an original being redesigned
        model = "models" in _P(args[0]).parts
        print(compare(*args[:3], labels=("model", "yours") if model else ("original", "redesign")))
    elif cmd == "caption":  # paperkit.py caption caption.txt|"text": exit 1 if it narrates production
        for a in args:  # a missing caption file must not pass as an empty, clean caption
            if not os.path.isfile(a) and re.fullmatch(r"\S+\.(txt|tex|md)", a):
                sys.exit(f"caption file not found: {a}")
        text = " ".join(_P(a).read_text() if os.path.isfile(a) else a for a in args)
        hits = note_issues(text)
        for why, phrase in hits:
            print(f"cut ({why}): {phrase!r}")
        sys.exit(1 if hits else 0)
    elif cmd == "parity":
        stats, warn = parity(*args[:2])
        print("            empty  colour  picture")
        for k, v in stats.items():
            print(f"{k:<10} {v['empty']:>6} {v['colour']:>7} {v['picture']:>8}")
        print("\n".join("WARN " + w for w in warn) or "ok: not emptier, greyer or less illustrated")
        sys.exit(1 if warn else 0)
    elif cmd == "swatches":
        out, pals = swatches(args[:-1], args[-1])
        for p, c in zip(args[:-1], pals):
            print(os.path.basename(p), " ".join(c))
        print(out)
    else:
        sys.exit(USAGE)
elif __name__ == "__main__":  # smoke test: one of every primitive, asserted to export
    import tempfile
    cv = Canvas(120, 60)
    cv.group(2, 2, 116, 56, "neutral", "paperkit primitives", band=True)
    cv.box(6, 34, 26, 10, "frozen", "Frozen block", "$\\mathbf{H}^{(l)}$", icon="snow", shadow=True)
    cv.box(36, 34, 26, 10, "amber", "Trainable", "$\\tilde{\\mathbf{W}}_Q$")
    cv.icon_flame(59, 41.5, 2.4)
    cv.matrix(68, 32, 12, 10, depth=3, r="memory")
    cv.op(90, 39, "+"); cv.op(96, 39, "."); cv.op(102, 39, "σ", r="purple")
    cv.tokens(6, 22, 6, fills=["blue"] * 3 + ["purple"] * 3, labels=list("abcdef"))
    cv.doc(30, 18, 8, 10, "blue", title="spec")
    cv.stack(44, 18, 12, 8, 3, "teal", title="heads")
    cv.cylinder(62, 17, 10, 10, "coral", title="DB")
    cv.diamond(76, 17, 14, 10, "amber", title="gate")
    cv.chip(100, 24, "ADD", "memory"); cv.chip(100, 19, "DEL", "coral", solid=True)
    cv.arrow([(32, 39), (36, 39)]); cv.arrow([(19, 34), (19, 28), (29.6, 28)], color=ROLE["memory"]["mark"])
    cv.block_arrow(6, 10, 30, 10, 3.5); cv.icon_lock(40, 10, 3); cv.icon_cycle(48, 10, 3.2)
    cv.icon_robot(56, 10, 4); cv.icon_clock(64, 10, 3); cv.brace(74, 6, 14, "right")
    cv.label(80, 13, "a", "Label")
    cv.flow_chips(["Update knowledge", "Refine preferences", "Calibrate thresholds"], 84, 116, 48, "teal", size=5.6)
    assert not cv.overlaps(), cv.overlaps()
    t = Canvas(40, 20)
    t.box(10, 5, 10, 8, "blue", "B")
    t.arrow([(2, 9), (10, 9)])
    assert not t.wire_crossings(), t.wire_crossings()
    t.arrow([(2, 7), (30, 7)])
    assert len(t.wire_crossings()) == 1, t.wire_crossings()
    d = tempfile.mkdtemp()
    sv = Canvas(150, 62)  # architecture-register primitives
    sv.section(2, 18, 70, 42, "blue", "Module A", letter="a")
    sv.section(76, 18, 72, 42, "coral", "Module B", tab="bottom")
    sv.cuboid(8, 24, 4, 22, d=2.4, r="blue", title="Conv 3×3", rotate=True, size=6)
    sv.cuboid(16, 30, 9, 9, r="purple", grad=("#CFE0F5", "#F6D2C4"))
    sv.fmap(30, 28, 12, 12, n=3, cmap="viridis")
    sv.num_matrix(48, 26, [[0.87, 0.11], [0.05, 0.93]], cell=5.0, r="blue", hi=[(0, 0), (1, 1)])
    sv.graph(90, 42, 5, 5, "coral")
    sv.mini_plot(100, 32, 16, 8, [np.exp(-np.linspace(-3, 3, 50) ** 2)], ["coral"])
    sv.mini_plot(122, 32, 14, 8, [np.array([5, 3, 2, 1.5])], ["purple"], bars=True)
    sv.phase_bar(12.5, [(2, 72, "blue", "Encoding"), (76, 148, "coral", "Decoding")])
    sv.legend(2, 1, 146, [("op", "+", "Addition"), ("op", "C", "Concat"), ("snow", None, "Frozen"),
                          ("flame", None, "Trainable"), ("dash", None, "Train only"), ("cuboid", "blue", "Feature"),
                          ("abbr", "FFT2D", "2-D Fourier transform")])
    sv.save(os.path.join(d, "arch"))
    ws = Canvas(80, 34)  # workspace-state primitives
    ws.turn_strip(4, 29, 72, 42, 31)
    ws.filetree(4, 26, 72, [(0, "artifacts/", None, "neutral"), (1, "plan_v4.md", "superseded", "amber"),
                            (1, "plan_v5.md", "current", "memory"), (1, "section3_final.md", "stale", "coral")],
                title="/workspace @ T31")
    assert not ws.text_overlaps(), ws.text_overlaps()
    ws.save(os.path.join(d, "ws"))
    sc = Canvas(110, 52)  # showcase primitives: plate, tiles, radar
    pl = sc.plate(4, 14, 44, 16, r="blue", label="Tool layer", size=6.5)
    for k, (g, name) in enumerate((("doc", "Read"), ("cycle", "Update"), ("lock", "Guard"))):
        sc.tile(*pl.at(0.2 + 0.3 * k, 0.5), 7.0, glyph=g, label=name, inside=True, r="blue", size=5.8)
    sc.radar(82, 25, 13, ["Plan", "Code", "Search", "Math", "Chat"],
             [("ours", [70, 62, 55, 48, 81], "blue"), ("base", [52, 66, 40, 30, 77], "amber"),
              ("other", [45, 50, 49, 20, 60], "neutral")], size=6.0)
    assert not sc.text_overlaps(), sc.text_overlaps()
    sc.save(os.path.join(d, "sc"))
    from PIL import Image, ImageDraw
    src = Image.new("RGB", (512, 512), "white")
    ImageDraw.Draw(src).ellipse((60, 60, 452, 452), fill="#5A8BCB", outline="#333333", width=12)
    src.save(os.path.join(d, "icon.png"))
    cv.image(os.path.join(d, "icon.png"), 110, 10, 6)  # two neighbours: matplotlib would merge them into one composite
    cv.image(os.path.join(d, "icon.png"), 110, 4, 5, fit="cover", h=4, radius=0.8)
    outs = cv.save(os.path.join(d, "smoke"))  # raises if either icon left the PDF resampled
    assert all(os.path.getsize(p) > 1000 for p in outs), outs
    for im in cv.ax.get_images():  # the old placement mode plus matplotlib's export defaults: 100 dpi, composited
        im.set_interpolation("nearest")
    cv.fig.savefig(os.path.join(d, "plain.pdf"))
    try:
        check_embedded(os.path.join(d, "plain.pdf"), cv.rasters)
        raise AssertionError("check_embedded missed a resampled PDF")
    except RuntimeError:
        pass
    assert note_issues("The icons were generated with Codex CLI and recoloured by the authors.")
    g = Canvas(84, 40, family="serif", size=6.5)  # column-width small multiples with one shared legend
    axs = g.axes_grid(16, 7, 66, 25, 2, 3, col_titles=["read", "write", "scan"], row_titles=["low", "high"],
                      xlabel="threads", ylabel="ops / s")
    xs_ = np.arange(1, 9)
    for row in axs:
        for ax in row:
            hs = [ax.plot(xs_, xs_ ** (1 - 0.2 * k), **series_kw(k))[0] for k in range(4)]
    g.chart_legend(hs, ["ours", "A", "B", "C"], 49, 34.5)
    curve_label(axs[0][0], xs_, xs_.astype(float), 5, "linear", size=5.2)
    g.box(2, 1, 8, 4, "line", "ctl", radius=0)
    g.hexagon(70, 35, 10, 3.6, title="API", size=5.8)
    tx = Canvas(84, 30, family="sans", size=6.8)  # annotated example, listing, callout, greeked text
    tx.rich(3, 26, [("import pandas", "black", "normal", "memory"), (" as pd  ", "black"),
                    ("import pylinreg", "black", "normal", "coral")], family="monospace")
    assert not any(t.get_text().startswith(" ") for t in tx.ax.texts), "a run starts with a space: SVG drops it"
    hgt = tx.listing(3, 22, ["lock(pt)", "unmap(pt, va)", "unlock(pt)"], hi={8: "coral"}, start=7)
    tx.callout(60, 20, "A", to=(40, 22 - hgt / 2))
    tx.greek(50, 12, 28, rows=3)
    yb, ex = tx.para(3, 11, 40, [("Finish[", "black"), ("keyboard function keys", "black", "normal", "memory"),
                                 ("] after three searches of one page", "black")], size=6.0, family="monospace")
    assert 2.0 < yb <= 11 - 2 * 1.2 * 6.0 / PT_PER_MM + 1e-6 and ex <= 43.5, (yb, ex)  # wrapped, inside the width
    assert [r[0] for ln in wrap_marked([("aa bb", "k", "normal", "m"), (" cc", "k", "normal", None)],
                                       len, 5) for r in ln] == ["aa bb", "cc"]  # the break eats the space
    y0 = tx.head(50, 5, "b", "Plain head", note="no band", size=7.0, rule=30)
    assert 0 < y0 < 5
    tx.arrow([(46, 20), (46, 14)], color="black", lw=0.6, head=1.0, dotted=True, both=True)
    assert not tx.text_overlaps(), tx.text_overlaps()
    tx.save(os.path.join(d, "text"))
    assert not g.text_overlaps(), g.text_overlaps()
    g.save(os.path.join(d, "grid"))
    a = Canvas(40, 20)  # audits must not report clean on these (each was a false pass)
    a.text(20, 10, "HELLO WORLD", size=8)
    a.icon_flame(20, 10, 3); a.icon_check(8, 10, 3)
    assert len(a.text_overlaps()) == 1, a.text_overlaps()
    a.box(10, 2, 10, 5, "blue", "B"); a.diamond(26, 2, 10, 6, "amber")
    a.arrow([(2, 5), (15, 5), (15, 1)])            # bends inside the box
    a.arrow([(22, 5), (38, 5), (38, 5)])           # through the diamond, repeated last point
    assert len(a.wire_crossings()) == 3, a.wire_crossings()  # two box segments + the diamond
    Image.new("RGBA", (64, 64), (0, 0, 0, 0)).save(os.path.join(d, "clear.png"))
    assert density(os.path.join(d, "clear.png"))[0] == 100.0
    assert not note_issues("Points: mean over 8 seeds; bars: 95% intervals. Claude Sonnet 5.5 as reader.")
    print("ok", outs)
