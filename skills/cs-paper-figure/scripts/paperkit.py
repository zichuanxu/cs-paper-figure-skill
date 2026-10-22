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

Design rules baked in (see references/visual-craft.md):
* role colours come as (fill, soft, stroke, ink, mark) families: pale fill,
  same-hue mid stroke, dark same-hue text, saturated mark for data/hero;
* corner radius scales with box height; strokes form a 3-level hierarchy;
* arrows are dark neutral by default, coloured only when colour encodes a
  path type (read / write / feedback); heads are filled and proportional;
* glyphs (matrices, token strips, documents, icons) carry the content so that
  boxes need fewer words.
"""
from __future__ import annotations

import math
import os
from pathlib import Path as _P

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import colors as mcolors  # noqa: E402
from matplotlib.patches import (Arc, Circle, Ellipse, FancyArrowPatch,  # noqa: E402
                                FancyBboxPatch, PathPatch, Polygon, Rectangle)
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
INK = "#262B33"      # body text
MUTED = "#6B7480"    # secondary text
LINE = "#4A4F57"     # default connector ink
HAIR = "#C9CED6"     # hairlines / grid


# Hue order for taxonomy series: maximally distinct neighbours, colour-blind-safe enough with labels.
SERIES_ORDER = ("memory", "blue", "purple", "amber", "coral", "teal", "rose", "frozen")


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
                                "axes.unicode_minus": False})
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
        self._r = None

    def _renderer(self):
        if self._r is None:
            self.fig.canvas.draw()
            self._r = self.fig.canvas.get_renderer()
        return self._r

    def axes(self, x, y, w, h, **kw):
        """A data axes placed at (x, y, w, h) mm on the canvas (plot area, excluding tick labels)."""
        return chart_axes(self.fig.add_axes([x / self.w, y / self.h, w / self.w, h / self.h], **kw),
                          size=self.size)

    # ---- text -------------------------------------------------------------
    def text(self, x, y, s, size=None, color=INK, weight="normal", ha="center", va="center",
             style="normal", z=20, **kw):
        return self.ax.text(x, y, s, fontsize=size or self.size, color=color, weight=weight,
                            ha=ha, va=va, style=style, zorder=z, **kw)

    def text_width(self, s, size, weight="normal"):
        t = self.ax.text(0, 0, s, fontsize=size, weight=weight)
        bb = t.get_window_extent(self._renderer())
        t.remove()
        return bb.width / self.fig.dpi * 25.4

    def rich(self, x, y, segments, size=None, ha="left", va="center", z=20):
        """Inline multi-colour text/math: segments = [(str, color[, weight])].
        Use to colour-code terms of one equation by role. Returns end x."""
        size = size or self.size
        widths = [self.text_width(s[0], size, s[2] if len(s) > 2 else "normal") for s in segments]
        cx = x - (sum(widths) if ha == "right" else sum(widths) / 2 if ha == "center" else 0)
        for s, w in zip(segments, widths):
            self.text(cx, y, s[0], size=size, color=s[1], weight=s[2] if len(s) > 2 else "normal",
                      ha="left", va=va, z=z)
            cx += w
        return cx

    def label(self, x, y, letter, title=None, size=8.0, color=INK):
        """Panel label '(a) Title': bold letter + bold title, top-left anchored."""
        self.text(x, y, f"({letter})", size=size, weight="bold", ha="left", va="top", color=color)
        if title:
            dx = self.text_width(f"({letter})", size, "bold") + 1.0
            self.text(x + dx, y, title, size=size, weight="bold", ha="left", va="top", color=color)

    # ---- containers -------------------------------------------------------
    def box(self, x, y, w, h, r="neutral", title=None, sub=None, *, fill=None, stroke=None,
            lw=0.6, radius=None, dashed=False, shadow=False, size=None, tsize=None, icon=None,
            weight="bold", z=5, title_color=None, align="center", name=None, alpha=1.0, gap=None):
        """Rounded node. Title bold in role ink, optional sub-line (math welcome)."""
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

    def chip(self, x, y, s, r="amber", size=None, h=None, pad=0.9, solid=False, z=8, ha="center", region=None):
        """Pill badge; width measured from the rendered text. Returns (x0, w). Every chip is recorded for
        cv.overlaps(); pass region=(x0, y0, x1, y1) when it must stay inside a card, band or cloud."""
        c = role(r)
        size = size or self.size - 0.8
        h = h or size * 0.55
        w = self.text_width(s, size) + 2 * pad
        x0 = x - w / 2 if ha == "center" else (x if ha == "left" else x - w)
        self.chips.append((x0, y - h / 2, w, h, s, region))
        self.ax.add_patch(FancyBboxPatch((x0, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h/2}",
                          lw=0.5, ec=c["stroke"], fc=c["mark"] if solid else c["soft"], zorder=z))
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
            (x0, y0), (x1, y1) = inv.transform(tx.get_window_extent(r).get_points())
            boxes.append((x0, y0, x1, y1, tx.get_text().replace("\n", " ")[:28]))
        bad = [f"'{s}' is cut by the canvas edge" for x0, y0, x1, y1, s in boxes
               if x0 < -tol or y0 < -tol or x1 > self.w + tol or y1 > self.h + tol]
        for i, (a0, b0, a1, b1, s) in enumerate(boxes):
            for c0, d0, c1, d1, s2 in boxes[i + 1:]:
                if a0 < c1 - tol and c0 < a1 - tol and b0 < d1 - tol and d0 < b1 - tol:
                    bad.append(f"'{s}' overlaps '{s2}'")
        return bad

    # ---- figure-series and narrative devices ----------------------------------
    def badge(self, x, y, k, r="neutral", d=3.0, z=12, size=None):
        """Numbered disc for steps or sub-mechanisms (solid role mark, white numeral)."""
        c = role(r)
        self.ax.add_patch(Circle((x, y), d / 2, fc=c["mark"], ec="white", lw=0.5, zorder=z))
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
        self.ax.add_patch(Ellipse((x + w / 2, y + e / 2), w, e, fc=c["fill"], ec=c["stroke"], lw=lw, zorder=z))
        self.ax.add_patch(Rectangle((x, y + e / 2), w, h - e, fc=c["fill"], ec="none", zorder=z + 0.01))
        for xx in (x, x + w):
            self.ax.plot([xx, xx], [y + e / 2, y + h - e / 2], color=c["stroke"], lw=lw, zorder=z + 0.02)
        self.ax.add_patch(Ellipse((x + w / 2, y + h - e / 2), w, e, fc=c["soft"], ec=c["stroke"], lw=lw, zorder=z + 0.03))
        if title:
            self.text(x + w / 2, y + (h - e) / 2, title, color=c["ink"], weight="bold", z=z + 1)

    def diamond(self, x, y, w, h, r="amber", title=None, z=6, lw=0.7):
        """Decision / gate."""
        c = role(r)
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
        Use only for illustrative content (agent mascots, scene photos), never for labels or data.
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
        self.rasters.append((path, tw, th))
        self.ax.set_xlim(0, self.w)
        self.ax.set_ylim(0, self.h)
        return h

    # ---- icons (pure vector) -------------------------------------------------
    def icon_snow(self, x, y, s, color=LINE, lw=0.55, z=12):
        """Snowflake = frozen / not trained."""
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
        self.ax.plot([x - s * 0.45, x - s * 0.1, x + s * 0.5], [y, y - s * 0.38, y + s * 0.42], color=color, lw=lw,
                     zorder=z, solid_capstyle="round", solid_joinstyle="round")

    def icon_cross(self, x, y, s, color=LINE, lw=0.8, z=12):
        """Cross drawn as vectors (font-independent ✗)."""
        for sg in (1, -1):
            self.ax.plot([x - s * 0.4, x + s * 0.4], [y - sg * s * 0.4, y + sg * s * 0.4], color=color, lw=lw,
                         zorder=z, solid_capstyle="round")

    def icon_flame(self, x, y, s, color="#E0702A", z=12):
        """Flame = trainable."""
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
        bw, bh = s * 0.74, s * 0.52
        self.ax.add_patch(Arc((x, y - s / 2 + bh), bw * 0.6, s * 0.7, theta1=0, theta2=180, ec=color,
                              lw=lw * 1.5, zorder=z))
        self.ax.add_patch(FancyBboxPatch((x - bw / 2, y - s / 2), bw, bh,
                          boxstyle=f"round,pad=0,rounding_size={s * 0.08}", fc=color, ec="none", zorder=z + 0.05))
        self.ax.add_patch(Circle((x, y - s / 2 + bh * 0.52), s * 0.075, fc="white", ec="none", zorder=z + 0.1))

    def icon_cycle(self, x, y, s, color=LINE, z=12, lw=0.6):
        """Circular arrows = evolves online / recurrent."""
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
        hw, hh = s * 0.8, s * 0.62
        self.ax.add_patch(FancyBboxPatch((x - hw / 2, y - hh / 2 - s * 0.08), hw, hh,
                          boxstyle=f"round,pad=0,rounding_size={s * 0.16}", fc=fill, ec=color, lw=lw, zorder=z))
        for sx in (-1, 1):
            self.ax.add_patch(Circle((x + sx * hw * 0.22, y - s * 0.08), s * 0.07, fc=color, ec="none", zorder=z + 0.1))
        self.ax.plot([x, x], [y + hh / 2 - s * 0.08, y + s * 0.42], color=color, lw=lw, zorder=z)
        self.ax.add_patch(Circle((x, y + s * 0.44), s * 0.07, fc=color, ec="none", zorder=z))

    def icon_clock(self, x, y, s, color=LINE, z=12, lw=0.55):
        self.ax.add_patch(Circle((x, y), s / 2, fc="white", ec=color, lw=lw, zorder=z))
        self.ax.plot([x, x], [y, y + s * 0.32], color=color, lw=lw, zorder=z + 0.1, solid_capstyle="round")
        self.ax.plot([x, x + s * 0.24], [y, y], color=color, lw=lw, zorder=z + 0.1, solid_capstyle="round")

    def icon_doc(self, x, y, s, r="neutral"):
        self.doc(x - s * 0.38, y - s / 2, s * 0.76, s, r, lines=3, fold=s * 0.28, z=12)

    # ---- connectors ---------------------------------------------------------
    def arrow(self, pts, color=LINE, lw=0.7, head=1.4, dashed=False, radius=1.2, z=8, both=False,
              start_dot=False, halo=False):
        """Polyline arrow with rounded elbows and a filled head (head in mm).
        Route orthogonally; end exactly on the target border. halo=True lays a white casing under the
        line so an unavoidable crossing reads as a bridge over the other wire (draw it with a higher z)."""
        pts = [tuple(p) for p in pts]
        if halo:
            self.ax.add_patch(PathPatch(_rounded_path(pts[:-1] + [pts[-1]], radius), fc="none", ec="white",
                                        lw=lw + 2.6, zorder=z - 0.05, capstyle="butt"))
        style = f"{'<|-|>' if both else '-|>'},head_length={head * 0.95},head_width={head * 0.42}"
        a = FancyArrowPatch(path=_rounded_path(pts, radius), arrowstyle=style, mutation_scale=PT_PER_MM,
                            lw=lw, color=color, zorder=z, linestyle=(0, (3.2, 1.8)) if dashed else "-",
                            shrinkA=0, shrinkB=0, joinstyle="miter", capstyle="butt")
        self.ax.add_patch(a)
        if start_dot:
            self.ax.add_patch(Circle(pts[0], 0.45, fc=color, ec="none", zorder=z))
        return a

    def line(self, pts, color=LINE, lw=0.6, dashed=False, z=7, radius=1.0, alpha=1):
        self.ax.add_patch(PathPatch(_rounded_path([tuple(p) for p in pts], radius), fc="none", ec=color,
                                    lw=lw, zorder=z, ls=(0, (3.2, 1.8)) if dashed else "-", alpha=alpha,
                                    capstyle="round", joinstyle="round"))

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


def _round_top_rect(x, y, w, h, r):
    r = min(r, h)
    v = [(x, y), (x + w, y), (x + w, y + h - r), (x + w, y + h), (x + w - r, y + h),
         (x + r, y + h), (x, y + h), (x, y + h - r), (x, y)]
    c = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3,
         Path.CURVE3, Path.CLOSEPOLY]
    return Path(v, c)


# ------------------------------------------------------------- chart style ---
def chart_axes(ax, grid="x", size=7.0):
    """Editorial chart defaults: no top/right spines, light grid on the value axis only,
    short outward ticks, muted tick labels."""
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9AA0A8")
        ax.spines[s].set_linewidth(0.6)
    ax.tick_params(length=2.2, width=0.6, color="#9AA0A8", labelsize=size - 0.5, labelcolor="#4A5059", pad=1.5)
    if grid:
        ax.grid(axis=grid, color="#E3E6EA", lw=0.5, zorder=0)
        ax.set_axisbelow(True)
    return ax


def density(png):
    """(white, tint, ink) percentages of a rendered figure: grey >=250, 200-249, <120."""
    from PIL import Image
    a = np.asarray(Image.open(png).convert("L"), float)
    return tuple(round(100 * float(v), 1) for v in ((a >= 250).mean(), ((a >= 200) & (a < 250)).mean(), (a < 120).mean()))


def compare(original, new, out, width=1600):
    """Stack two renders at the same pixel width (original on top) for a side-by-side review."""
    from PIL import Image, ImageDraw
    ims = []
    for p in (original, new):
        im = Image.open(p).convert("RGB")
        ims.append(im.resize((width, round(im.height * width / im.width))))
    canvas = Image.new("RGB", (width, sum(i.height for i in ims) + 60), "white")
    y = 0
    for lab, im in zip(("original", "redesign"), ims):
        ImageDraw.Draw(canvas).text((8, y + 4), lab, fill=(200, 40, 40))
        canvas.paste(im, (0, y + 24))
        y += im.height + 30
    canvas.save(out)
    return out


def visual_stats(png, width=1600):
    """At a fixed pixel width: empty % (16 px blocks that are flat white), colour % (saturated pixels),
    picture % (blocks with illustration-like texture: many distinct tones)."""
    from PIL import Image
    im = Image.open(png).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)))
    g = np.asarray(im.convert("L"), float)
    hsv = np.asarray(im.convert("HSV"), float)
    b = 16
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


if __name__ == "__main__" and len(__import__("sys").argv) > 1:
    import sys
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "density":
        for p in args:
            print(p, "white/tint/ink %", density(p))
    elif cmd == "compare":
        print(compare(*args[:3]))
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
        sys.exit("usage: paperkit.py [density PNG... | compare ORIGINAL NEW OUT | parity ORIGINAL NEW | swatches PNG... OUT]")
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
    d = tempfile.mkdtemp()
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
    print("ok", outs)
