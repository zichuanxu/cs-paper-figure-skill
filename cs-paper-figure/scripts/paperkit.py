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
        fam = [n for n in ("Helvetica", "Arial", "Liberation Sans", "DejaVu Sans") if n in names]
        matplotlib.rcParams.update({"font.family": "sans-serif", "font.sans-serif": fam,
                                    "mathtext.fontset": "stixsans"})
    matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
                                "axes.unicode_minus": False})
    return fam[0]


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

    def chip(self, x, y, s, r="amber", size=None, h=None, pad=0.9, solid=False, z=8, ha="center"):
        """Pill badge; width measured from the rendered text. Returns (x0, w)."""
        c = role(r)
        size = size or self.size - 0.8
        h = h or size * 0.55
        w = self.text_width(s, size) + 2 * pad
        x0 = x - w / 2 if ha == "center" else (x if ha == "left" else x - w)
        self.ax.add_patch(FancyBboxPatch((x0, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h/2}",
                          lw=0.5, ec=c["stroke"], fc=c["mark"] if solid else c["soft"], zorder=z))
        self.text(x0 + w / 2, y, s, size=size, color="white" if solid else c["ink"], z=z + 1)
        return x0, w

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
              start_dot=False):
        """Polyline arrow with rounded elbows and a filled head (head in mm).
        Route orthogonally; end exactly on the target border."""
        pts = [tuple(p) for p in pts]
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
    def save(self, stem, png_dpi=300, formats=("pdf", "svg", "png")):
        _P(stem).parent.mkdir(parents=True, exist_ok=True)
        out = []
        for f in formats:
            p = f"{stem}.{f}"
            kw = {"dpi": png_dpi} if f == "png" else {}
            if f == "pdf":
                kw["metadata"] = {"Creator": "paperkit", "CreationDate": None}
            self.fig.savefig(p, **kw)
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


if __name__ == "__main__" and len(__import__("sys").argv) > 1:
    import sys
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "density":
        for p in args:
            print(p, "white/tint/ink %", density(p))
    elif cmd == "compare":
        print(compare(*args[:3]))
    else:
        sys.exit("usage: paperkit.py [density PNG... | compare ORIGINAL NEW OUT]")
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
    d = tempfile.mkdtemp()
    outs = cv.save(os.path.join(d, "smoke"))
    assert all(os.path.getsize(p) > 1000 for p in outs), outs
    print("ok", outs)
