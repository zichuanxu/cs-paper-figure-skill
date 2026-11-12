"""Shared visual system for the two Harness² figures (arXiv:2610.14224, Figs. 2 and 3).

Both render scripts import this module, so a concept keeps one colour and one object in the pair:

* slate  = the frozen model M, the executor that wraps it, and harness content inherited unchanged;
* blue / green / rose / amber = the four component groups of the execution harness (Fig. 2 only);
* purple = the improver (improvement harness R_t and its editor, composer and reflector sessions);
* teal / coral = the invariant and the domain-specific candidate (Fig. 3 only);
* `rack`   = a harness H = (c1..c8): eight labelled cells, one per component file;
* `record` = an execution record e = (tau, y): a page with a trajectory path and a deliverable bar;
* `icon`   = one illustrated family (file pages, robots, model block) with a vector stand-in for each.
"""
import math
import os
import sys
import tempfile

import numpy as np
from matplotlib import colors as mcolors
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from paperkit import INK, LINE, MUTED, ROLE  # noqa: E402

ICONS = os.path.join(HERE, "icons")
VECTOR = False  # --vector-icons sets this: every raster icon is replaced by its vector stand-in

MODEL, CONTEXT, TOOLS, ORCH, MID = "frozen", "blue", "memory", "rose", "amber"
IMPROVER, INV, DOM = "purple", "teal", "coral"
GROUP = {1: CONTEXT, 2: CONTEXT, 3: CONTEXT, 6: CONTEXT, 4: TOOLS, 7: TOOLS, 5: ORCH, 8: MID}  # Table 5
MONO = dict(family="monospace")
_TMP = None


def retint(name, r):
    """Path of icon `name` with its accent hue moved to role r's stroke colour (the set was generated with
    one accent per icon; the series palette assigns some of them another role). Only pixels near the
    icon's dominant saturated hue change; outlines, cream fills and other accents stay."""
    global _TMP
    from PIL import Image
    _TMP = _TMP or tempfile.mkdtemp(prefix="h2icons_")
    out = os.path.join(_TMP, f"{name}_{r}.png")
    if os.path.exists(out):
        return out
    a = np.asarray(Image.open(os.path.join(ICONS, name + ".png")).convert("RGB"), float) / 255.0
    hsv = mcolors.rgb_to_hsv(a)
    sat = hsv[..., 1] > 0.22
    h0 = (np.bincount((hsv[..., 0][sat] * 72).astype(int), minlength=73).argmax() + 0.5) / 72
    m = sat & (np.abs((hsv[..., 0] - h0 + 0.5) % 1 - 0.5) < 0.085)
    th, ts, tv = mcolors.rgb_to_hsv(mcolors.to_rgb(ROLE[r]["stroke"]))
    hsv[..., 0][m] = th
    hsv[..., 1][m] = np.clip(hsv[..., 1][m] * ts / np.median(hsv[..., 1][m]), 0, 1)
    hsv[..., 2][m] = np.clip(hsv[..., 2][m] * tv / np.median(hsv[..., 2][m]), 0, 1)
    Image.fromarray((mcolors.hsv_to_rgb(hsv) * 255).round().astype("uint8")).save(out)
    return out


def icon(cv, name, x, y, s, r="neutral", tint=False, fit="box", z=12):
    """Icon `name` centred at (x, y), longer side s mm; tint=True moves its accent to role r.
    With VECTOR (or a missing PNG) the stand-in is drawn: a page for f_*, a robot head for agents,
    a node grid for the model, a prompt window for tools."""
    png = os.path.join(ICONS, name + ".png")
    if not VECTOR and os.path.exists(png):
        cv.image(retint(name, r) if tint else png, x, y, s, fit=fit, z=z)
        return
    c = ROLE[r]
    if name.startswith("f_"):
        cv.doc(x - s * 0.36, y - s / 2, s * 0.72, s, r, lines=3, z=z)
        cv.ax.add_patch(Circle((x + s * 0.3, y - s * 0.3), s * 0.2, fc=c["mark"], ec="white", lw=0.5, zorder=z + 2))
    elif name == "model":
        cv.ax.add_patch(FancyBboxPatch((x - s / 2, y - s / 2), s, s, boxstyle=f"round,pad=0,rounding_size={s * 0.16}",
                                       fc=c["ink"], ec=INK, lw=0.6, zorder=z))
        pts = [(x + (i - 1) * s * 0.3, y + (j - 1) * s * 0.3) for i in range(3) for j in range(3)]
        for i in range(6):
            for j in range(3):
                p, q = pts[i], pts[3 * (i // 3 + 1) + j]
                cv.ax.plot([p[0], q[0]], [p[1], q[1]], color=c["stroke"], lw=0.4, zorder=z + 0.1)
        for p in pts:
            cv.ax.add_patch(Circle(p, s * 0.085, fc=c["soft"], ec=INK, lw=0.4, zorder=z + 0.2))
    elif name == "tools":
        cv.ax.add_patch(FancyBboxPatch((x - s / 2, y - s * 0.36), s, s * 0.72, boxstyle=f"round,pad=0,rounding_size={s * 0.1}",
                                       fc=c["soft"], ec=c["ink"], lw=0.6, zorder=z))
        cv.text(x, y, ">_", size=s * 1.25, color=c["ink"], weight="bold", z=z + 1, **MONO)
    else:
        cv.icon_robot(x, y, s * 0.82, color=c["mark"], fill="white", z=z, lw=0.8)


def rack(cv, x, y, edits=None, cell=(3.5, 3.3), groups=False, labels=True, name="", z=6):
    """A harness H = (c1..c8) as a rack of its eight component files, C1-C4 over C5-C8.
    Grey cell = inherited content; edits = {i: role} paints component i in that role's mark (an edited
    file); groups=True paints every cell in its Fig. 2 group colour. Returns (x, y, w, h)."""
    edits = edits or {}
    cw, ch = cell
    pad = 0.14 * cw
    w, h = 4 * cw + 2 * pad, 2 * ch + 2 * pad
    cv.solids.append((x, y, w, h, f"rack {name}", None))
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={0.2 * cw}", fc="white",
                                   ec=ROLE[MODEL]["ink"], lw=0.6 if labels else 0.45, zorder=z))
    for i in range(8):
        k = i + 1
        cx, cy = x + pad + (i % 4) * cw, y + pad + (1 - i // 4) * ch
        if k in edits:
            fc, tc, wt = ROLE[edits[k]]["mark"], "white", "bold"
        elif groups:
            fc, tc, wt = ROLE[GROUP[k]]["soft"], ROLE[GROUP[k]]["ink"], "bold"
        else:
            fc, tc, wt = "#E3E6EB", "#7C8592", "normal"
        cv.ax.add_patch(Rectangle((cx, cy), cw, ch, fc=fc, ec="white", lw=0.5, zorder=z + 0.1))
        if labels:
            cv.text(cx + cw / 2, cy + ch / 2 - 0.05, f"C{k}", size=5.8, color=tc, weight=wt, z=z + 1)
    return (x, y, w, h)


def record(cv, x, y, r="neutral", w=5.2, h=6.6, z=6, ghost=False):
    """An execution record e = (tau, y): a page carrying the trajectory (dotted path) and the
    deliverable (bar). ghost=True draws a pale second copy of a record shown elsewhere."""
    c = ROLE[r]
    cv.doc(x, y, w, h, r, lines=0, z=z, lw=0.45 if ghost else 0.6)
    col = c["stroke"] if ghost else c["mark"]
    xs = [x + w * f for f in (0.2, 0.52, 0.3, 0.62)]
    ys = [y + h * f for f in (0.74, 0.62, 0.48, 0.36)]
    cv.ax.plot(xs, ys, color=col, lw=0.55, zorder=z + 1, solid_capstyle="round")
    for px, py in zip(xs, ys):
        cv.ax.add_patch(Circle((px, py), 0.34, fc=col, ec="none", zorder=z + 1.1))
    cv.ax.plot([x + w * 0.2, x + w * 0.8], [y + h * 0.17] * 2, color=col, lw=1.5, zorder=z + 1, solid_capstyle="butt")
    return (x, y, w, h)


def tag(cv, x, y, s, r, dashed=False, ha="right", size=5.8, z=9):
    """Activation tag: a pill in the role's tint; dashed outline = reached on demand, solid = every call."""
    c = ROLE[r]
    h = 3.1
    w = cv.text_width(s, size) + 2.2
    x0 = x - w if ha == "right" else x - w / 2 if ha == "center" else x
    cv.chips.append((x0, y - h / 2, w, h, s, None))
    cv.ax.add_patch(FancyBboxPatch((x0, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                   fc="white" if dashed else c["soft"], ec=c["stroke"] if dashed else c["ink"], lw=0.6,
                                   ls=(0, (2.2, 1.4)) if dashed else "-", zorder=z))
    cv.text(x0 + w / 2, y - 0.05, s, size=size, color=c["ink"], z=z + 1)
    return x0, w


def darrow(cv, pts, color=LINE, lw=0.8, head=1.3, radius=1.2):
    """Dashed connector with a solid head (a dashed arrow patch breaks its own head into dashes)."""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    L = math.hypot(x1 - x0, y1 - y0)
    t = min(head * 1.15, L * 0.5) / L
    q = (x1 - (x1 - x0) * t, y1 - (y1 - y0) * t)
    cv.line(list(pts[:-1]) + [q], color=color, lw=lw, dashed=True, radius=radius, z=8)
    cv.arrow([q, pts[-1]], color=color, lw=lw, head=head)


def key(cv, x, y, w, items, h=6.4, size=6.0, gap=4.5):
    """Key strip: items = [(draw, glyph_width, label)], draw(cx, cy) paints the glyph centred there.
    Items are spread evenly over the strip."""
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.4", fc="white",
                                   ec=ROLE["neutral"]["stroke"], lw=0.55, ls=(0, (3, 2)), zorder=2))
    widths = [gw + 1.1 + cv.text_width(lab, size) for _, gw, lab in items]
    free = w - sum(widths)
    assert free > gap * (len(items) + 1) * 0.5, f"key strip too narrow by {gap * (len(items) + 1) - free:.1f} mm"
    g = free / (len(items) + 1)
    xx = x + g
    for (draw, gw, lab), iw in zip(items, widths):
        draw(xx + gw / 2, y + h / 2)
        cv.text(xx + gw + 1.1, y + h / 2 - 0.05, lab, size=size, ha="left", z=12)
        xx += iw + g


__all__ = ["ICONS", "MODEL", "CONTEXT", "TOOLS", "ORCH", "MID", "IMPROVER", "INV", "DOM", "GROUP", "MONO",
           "icon", "rack", "record", "tag", "key", "darrow", "retint", "INK", "LINE", "MUTED", "ROLE"]
