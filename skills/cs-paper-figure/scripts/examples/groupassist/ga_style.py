"""Shared visual system for the two GroupAssistBench figures (arXiv:2611.04867, Figs. 1 and 2).

Both render scripts import this module, so a concept keeps one colour and one object in the pair:

* slate  = the group conversation and the benchmark's own structure (windows, step frames);
* blue   = task level L1, memory recall;          purple = task level L2, memory use;
* amber  = an anchor, i.e. a required memory and its verbatim evidence span;
* red    = a superseded value, a penalty, a dropped candidate;
* green  = the current value, a kept candidate, a passed check;
* `message`  = one chat message: avatar, mono id, speaker, mono text with highlighted spans;
* `strip`    = the thread as cells of ten messages with a cut: history, the cut, what is not visible;
* `key_row`  = one line of an answer key: a tick (reference fact) or a signed weight (rubric criterion);
* `avatar`   = one illustrated family (five members and the assistant) with a vector stand-in each;
* gear / sparkle / person = a step done by rules, by a language model, by humans.

The running example is the trip-planning thread of the paper's Figs. 1 and 2: messages #34, #35, #104,
#342, #343, #363, #372 and #452 keep their numbers, speakers and wording in both figures (THREAD).
"""
import math
import os
import sys
import textwrap

from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Polygon, Rectangle, Wedge

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from paperkit import INK, LINE, MUTED, ROLE, _round_top_rect  # noqa: E402

ICONS = os.path.join(HERE, "icons")
VECTOR = False  # --vector-icons sets this: every raster avatar is replaced by its vector stand-in

STRUCT, L1, L2, ANCHOR, OLD, CUR = "frozen", "blue", "purple", "amber", "coral", "memory"
MONO = dict(family="monospace")
SLATE = ROLE[STRUCT]["ink"]          # solid headers
HL = {ANCHOR: "#FBD58E", OLD: "#F6A892", CUR: "#9BD9AE"}   # span highlights behind text
N_CELLS, PER_CELL = 48, 10           # the thread strip: 48 cells of ten messages (#1-#480 of 2,236)

# Speakers and wording as printed in the paper's Fig. 1 (translated and abridged there).
MEMBERS = {"zhou_yue": "Zhou Yue", "lu_ye": "Lu Ye", "li_lei": "Li Lei", "jiang_chen": "Jiang Chen",
           "lin_xi": "Lin Xi"}
THREAD = {
    34: ("zhou_yue", "Let's meet at 7:30 am on May 1 for now.", [("7:30 am on May 1", ANCHOR)]),
    35: ("lu_ye", "Rule: whoever doesn't show up on departure day sends the group ¥500 cash gift.",
         [("sends the group ¥500 cash gift", ANCHOR)]),
    104: ("li_lei", "@Agent on departure day, remind the no-shows to pay up.", []),
    "proposal": ("jiang_chen", "How about leaving on Apr 30 to avoid the May 1 rush? About ¥50 more each.",
                 [("May 1", OLD)]),
    342: ("zhou_yue", "No objections, so approved: we leave on Apr 30, +¥50 each.", [("Apr 30", CUR)]),
    363: ("lin_xi", "A window seat, not squeezed in the middle, would be great for me.",
          [("A window seat, not squeezed in the middle, would be great for me.", ANCHOR)]),
}
QUERY_B = "@Agent Post a reminder on ticket booking and travel costs."   # authored request, cut #452


def cell_of(mid):
    """1-based strip cell that holds message #mid."""
    return (mid - 1) // PER_CELL + 1


# ------------------------------------------------------------------ text ---
def mono_w(cv, size):
    """Advance of one monospace character in mm."""
    key = ("mono", size)
    if key not in cv.nodes:
        t = cv.ax.text(0, 0, "M" * 40, fontsize=size, **MONO)
        cv.nodes[key] = t.get_window_extent(cv._renderer()).width / cv.fig.dpi * 25.4 / 40
        t.remove()
    return cv.nodes[key]


def mono_para(cv, x, ytop, text, chars, size=5.9, hl=(), color=INK, pitch=None, z=20, weight="normal"):
    """Monospace paragraph wrapped at `chars`, top at ytop; hl = [(substring, role)] paints the span behind the
    text (it may wrap). Mono marks words that come from the conversation. Returns the bottom y."""
    cw = mono_w(cv, size)
    pitch = pitch or size * 0.415
    lines = textwrap.wrap(text, chars, break_long_words=False, break_on_hyphens=False)
    starts, pos = [], 0
    for ln in lines:
        pos = text.index(ln, pos)
        starts.append(pos)
        pos += len(ln)
    for k, (ln, s0) in enumerate(zip(lines, starts)):
        y = ytop - pitch * (k + 0.5)
        for sub, r in hl:
            a = text.find(sub)
            if a < 0:
                continue
            lo, hi = max(a, s0), min(a + len(sub), s0 + len(ln))
            if hi > lo:
                cv.ax.add_patch(Rectangle((x + (lo - s0) * cw - 0.15, y - pitch * 0.46), (hi - lo) * cw + 0.3,
                                          pitch * 0.92, fc=HL[r], ec="none", zorder=z - 1))
        cv.text(x, y - 0.05, ln, size=size, color=color, ha="left", z=z, weight=weight, **MONO)
    return ytop - pitch * len(lines)


def n_lines(text, chars):
    return len(textwrap.wrap(text, chars, break_long_words=False, break_on_hyphens=False))


def sans_para(cv, x, ytop, text, w, size=6.2, color=INK, pitch=None, z=20, style="normal", weight="normal"):
    """Text-face paragraph wrapped to w mm by measured word widths. Returns the bottom y."""
    pitch = pitch or size * 0.40
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if cur and cv.text_width(t, size, weight) > w:
            lines.append(cur)
            cur = word
        else:
            cur = t
    lines.append(cur)
    for k, ln in enumerate(lines):
        cv.text(x, ytop - pitch * (k + 0.5), ln, size=size, color=color, ha="left", z=z, style=style, weight=weight)
    return ytop - pitch * len(lines)


def seg_line(cv, x, y, segs, size=6.2, z=20):
    """One line of text-face segments [(text, colour, weight, highlight role or None, mono?)]; a highlight
    paints the value's state behind it. Returns the end x."""
    cx = x
    for seg in segs:
        s, col, wt = seg[0], seg[1], seg[2]
        r = seg[3] if len(seg) > 3 else None
        mono = len(seg) > 4 and seg[4]
        ms = max(size - 0.3, 5.8)
        if mono:
            w = mono_w(cv, ms) * len(s)
        else:
            w = cv.text_width("|" + s + "|", size, wt) - cv.text_width("||", size, wt)
        if r:
            lead = len(s) - len(s.lstrip())
            off = (cv.text_width("|" + s[:lead] + "|", size, wt) - cv.text_width("||", size, wt)) if lead else 0
            cv.ax.add_patch(Rectangle((cx + off - 0.2, y - size * 0.19), w - off + 0.4, size * 0.38, fc=HL[r],
                                      ec="none", zorder=z - 1))
        if mono:
            cv.text(cx, y - 0.05, s, size=ms, color=col, weight=wt, ha="left", z=z, **MONO)
        else:
            cv.text(cx, y, s, size=size, color=col, weight=wt, ha="left", z=z)
        cx += w
    return cx


# ----------------------------------------------------------------- icons ---
def _mark(cv, x, y, s, kind):
    cv.icons.append([x - s / 2, y - s / 2, x + s / 2, y + s / 2, kind + " icon", len(cv.ax.get_children())])


def avatar(cv, name, x, y, s, z=12, disc=True):
    """Member or assistant avatar centred at (x, y), s mm across, on a white disc. With VECTOR (or a missing
    PNG) the stand-in is drawn: initials in a slate ring for a member, a robot head for the assistant."""
    if disc:
        cv.ax.add_patch(Circle((x, y), s / 2, fc="white", ec=ROLE[STRUCT]["stroke"], lw=0.45, zorder=z - 0.5))
    png = os.path.join(ICONS, name + ".png")
    if not VECTOR and os.path.exists(png):
        cv.image(png, x, y - s * 0.02, s * 0.86, fit="box", z=z)
        return
    if name == "assistant":
        _mark(cv, x, y, s * 0.8, name)
        cv.icon_robot(x, y - s * 0.03, s * 0.62, color=ROLE["teal"]["mark"], fill=ROLE["teal"]["fill"], z=z, lw=0.7)
        return
    c = ROLE[STRUCT]
    cv.ax.add_patch(Circle((x, y), s * 0.40, fc=c["soft"], ec="none", zorder=z))
    ini = "".join(p[0] for p in MEMBERS[name].split())
    cv.text(x, y - 0.05, ini, size=max(s * 1.05, 5.8), color=c["ink"], weight="bold", z=z + 1)


def gear(cv, x, y, s=2.6, color=LINE, z=12):
    """Step done by deterministic rules."""
    _mark(cv, x, y, s, "gear")
    pts = []
    for k in range(16):
        a = math.pi * k / 8
        for da, rr in ((-0.11, 0.5), (0.11, 0.5)) if k % 2 == 0 else ((-0.14, 0.36), (0.14, 0.36)):
            pts.append((x + s * rr * math.cos(a + da), y + s * rr * math.sin(a + da)))
    cv.ax.add_patch(Polygon(pts, closed=True, fc=color, ec=color, lw=0.3, zorder=z, joinstyle="round"))
    cv.ax.add_patch(Circle((x, y), s * 0.16, fc="white", ec="none", zorder=z + 0.1))


def sparkle(cv, x, y, s=2.6, color=LINE, z=12):
    """Step done by a language-model call."""
    _mark(cv, x, y, s, "model")
    pts = [(x + s * (0.5 if k % 2 == 0 else 0.13) * math.cos(math.pi * k / 4 + math.pi / 2),
            y + s * (0.5 if k % 2 == 0 else 0.13) * math.sin(math.pi * k / 4 + math.pi / 2)) for k in range(8)]
    cv.ax.add_patch(Polygon(pts, closed=True, fc=color, ec=color, lw=0.3, zorder=z, joinstyle="round"))


def person(cv, x, y, s=2.6, color=LINE, z=12):
    """Step done by human annotators."""
    _mark(cv, x, y, s, "human")
    cv.ax.add_patch(Circle((x, y + s * 0.22), s * 0.2, fc=color, ec="none", zorder=z))
    cv.ax.add_patch(Wedge((x, y - s * 0.48), s * 0.42, 0, 180, fc=color, ec="none", zorder=z))


DOER = {"rule": gear, "model": sparkle, "human": person}


def swatch(cv, x, y, r, w=3.6, h=2.2, z=11):
    cv.ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.4",
                                   fc=HL[r], ec=ROLE[r]["stroke"], lw=0.4, zorder=z))


def tick(cv, x, y, ok=True, s=2.0, z=12):
    """Verdict mark: green tick (kept, passed) or red cross (dropped)."""
    if ok:
        cv.icon_check(x, y, s, color=ROLE[CUR]["mark"], lw=1.0, z=z)
    else:
        cv.icon_cross(x, y, s * 0.85, color=ROLE[OLD]["mark"], lw=1.0, z=z)


def verdict(cv, x, y, ok, label, ha="left", size=6.0, z=9):
    """Keep / drop pill with its tick or cross. Returns (x0, w)."""
    r = CUR if ok else OLD
    c = ROLE[r]
    h = 3.0
    w = cv.text_width(label, size, "bold") + 4.4
    x0 = x if ha == "left" else x - w
    cv.chips.append((x0, y - h / 2, w, h, label, None))
    cv.ax.add_patch(FancyBboxPatch((x0, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                   fc=c["soft"], ec=c["stroke"], lw=0.55, zorder=z))
    tick(cv, x0 + 1.7, y, ok, s=1.7, z=z + 1)
    cv.text(x0 + 3.1, y - 0.05, label, size=size, color=c["ink"], weight="bold", ha="left", z=z + 1)
    return x0, w


# --------------------------------------------------------------- objects ---
def header(cv, x, ytop, w, h, title, sub=None, radius=1.8, size=8.0, fc=SLATE, tx=None, z=3):
    """Solid header band with a rounded top (window chrome, step header): white bold title, light sub-line."""
    cv.ax.add_patch(PathPatch(_round_top_rect(x, ytop - h, w, h, radius), fc=fc, ec="none", zorder=z))
    tx = x + 2.2 if tx is None else tx
    if sub:
        cv.text(tx, ytop - h * 0.34, title, size=size, color="white", weight="bold", ha="left", z=z + 1)
        cv.text(tx, ytop - h * 0.73, sub, size=6.0, color="#D5DCE8", ha="left", z=z + 1)
    else:
        cv.text(tx, ytop - h / 2 - 0.05, title, size=size, color="white", weight="bold", ha="left", z=z + 1)


def frame(cv, x, ytop, w, h, r=STRUCT, fill="white", radius=1.8, lw=0.7, z=1.5):
    """Window / card body (a container: wires may end inside it)."""
    c = ROLE[r]
    cv.ax.add_patch(FancyBboxPatch((x, ytop - h), w, h, boxstyle=f"round,pad=0,rounding_size={radius}", fc=fill,
                                   ec=c["stroke"], lw=lw, zorder=z))


def msg_height(text, chars, size=5.9, name=True):
    return (2.9 if name else 0) + n_lines(text, chars) * size * 0.415 + 1.5


def message(cv, x, ytop, w, mid, who, text, hl=(), r=STRUCT, size=5.9, av=5.2, tag=None, tag_r=None, z=6,
            fill="white"):
    """One chat message: avatar, then a bubble with '#id Speaker' and the mono text. mid None = the paper gives
    no number. tag = a pill on the bubble's top-right corner (the task accent). Returns the bottom y."""
    c = ROLE[r]
    bx, bw = x + av + 1.2, w - av - 1.2
    chars = int((bw - 2.6) / mono_w(cv, size))
    h = msg_height(text, chars, size)
    cv.solids.append((bx, ytop - h, bw, h, f"message {mid}", None))
    cv.ax.add_patch(FancyBboxPatch((bx, ytop - h), bw, h, boxstyle="round,pad=0,rounding_size=1.1", fc=fill,
                                   ec=c["stroke"], lw=0.9 if tag else 0.5, zorder=z))
    avatar(cv, who, x + av / 2, ytop - av / 2 - 0.3, av, z=z + 2)
    segs = ([(f"#{mid} ", MUTED, "normal", None, True)] if mid else []) + [(MEMBERS[who], c["ink"], "bold")]
    seg_line(cv, bx + 1.3, ytop - 1.75, segs, size=6.2, z=z + 2)
    if tag:
        tc = ROLE[tag_r or r]
        tw = cv.text_width(tag, 5.8, "bold") + 2.4
        cv.ax.add_patch(FancyBboxPatch((bx + bw - tw - 1.0, ytop - 3.05), tw, 2.6,
                                       boxstyle="round,pad=0,rounding_size=1.3", fc=tc["mark"], ec="none", zorder=z + 1))
        cv.text(bx + bw - tw / 2 - 1.0, ytop - 1.8, tag, size=5.8, color="white", weight="bold", z=z + 2)
    mono_para(cv, bx + 1.3, ytop - 3.1, text, chars, size=size, hl=hl, z=z + 2)
    return ytop - h


def strip(cv, x, y, w, cut=None, marks=None, accent=L1, h=2.4, n=N_CELLS, z=6):
    """The thread as n cells of ten messages (`cv.turn_strip`): history before the cut in slate, the cut cell
    solid in the instance's accent, later cells grey. marks = {message id: role} recolours the cell that holds
    that message (anchor, superseded, current). Returns x-centre lookup f(message id)."""
    gap = 0.18
    cw = (w - gap * (n - 1)) / n
    cv.turn_strip(x, y, w, n, cell_of(cut) if cut else n + 1, h=h, r=accent, past=STRUCT, gap=gap, z=z)
    for mid, r in (marks or {}).items():
        i = cell_of(mid) - 1
        cv.ax.add_patch(Rectangle((x + i * (cw + gap), y), cw, h, fc=ROLE[r]["mark"], ec=ROLE[r]["ink"], lw=0.3,
                                  zorder=z + 0.5))
    return lambda mid: x + (cell_of(mid) - 1) * (cw + gap) + cw / 2


def strip_label(cv, cx, y, s, color=MUTED, above=True, size=5.8, weight="normal", ha="center", stem=1.0):
    """Message-id label on a strip cell with a short stem."""
    d = 1 if above else -1
    cv.ax.plot([cx, cx], [y, y + d * stem], color=color, lw=0.5, zorder=7, solid_capstyle="butt")
    cv.text(cx, y + d * (stem + 1.15), s, size=size, color=color, weight=weight, ha=ha, z=20, **MONO)


def key_row(cv, x, y, w, kind, segs, mid=None, size=6.2, z=9):
    """One line of an answer key. kind 'fact' = a reference fact (amber tick box); an int = a rubric criterion
    with that signed weight (green chip if positive, red if a penalty). segs as in seg_line; mid = source
    message id, right-aligned in mono."""
    if kind == "fact":
        c = ROLE[ANCHOR]
        cv.ax.add_patch(FancyBboxPatch((x, y - 1.2), 2.4, 2.4, boxstyle="round,pad=0,rounding_size=0.5",
                                       fc=HL[ANCHOR], ec=c["stroke"], lw=0.5, zorder=z))
        cv.icon_check(x + 1.2, y, 1.5, color=c["ink"], lw=0.9, z=z + 1)
        tx = x + 3.5
    else:
        r = CUR if kind > 0 else OLD
        c = ROLE[r]
        cv.ax.add_patch(FancyBboxPatch((x, y - 1.3), 4.3, 2.6, boxstyle="round,pad=0,rounding_size=0.6",
                                       fc=c["mark"], ec="none", zorder=z))
        cv.text(x + 2.15, y - 0.05, f"{'+' if kind > 0 else '−'}{abs(kind)}", size=6.2, color="white",
                weight="bold", z=z + 1)
        tx = x + 5.3
    seg_line(cv, tx, y, segs, size=size, z=z + 2)
    if mid:
        cv.text(x + w, y - 0.05, f"#{mid}", size=max(size - 0.4, 5.8), color=MUTED, ha="right", z=z + 2, **MONO)


def lock_tag(cv, x, y, s="judge only", size=5.8, z=12):
    """Hidden from the evaluated system (required memories and answer key): a lock and its tag, right-aligned at x."""
    w = cv.text_width(s, size)
    cv.text(x, y, s, size=size, color=MUTED, style="italic", ha="right", z=z)
    cv.icon_lock(x - w - 1.5, y + 0.1, 2.0, color=MUTED, z=z)


def letter_badge(cv, x, y, s, r, d=4.0, z=12):
    """Instance badge A / B in its level colour."""
    cv.ax.add_patch(Circle((x, y), d / 2, fc=ROLE[r]["ink"], ec="white", lw=0.6, zorder=z))
    cv.text(x, y - 0.05, s, size=d * 1.75, color="white", weight="bold", z=z + 1)


def darrow(cv, pts, color=LINE, lw=0.8, head=1.3, radius=1.2, z=8):
    """Dashed connector with a solid head."""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    L = math.hypot(x1 - x0, y1 - y0)
    t = min(head * 1.15, L * 0.5) / L
    q = (x1 - (x1 - x0) * t, y1 - (y1 - y0) * t)
    cv.line(list(pts[:-1]) + [q], color=color, lw=lw, dashed=True, radius=radius, z=z)
    cv.arrow([q, pts[-1]], color=color, lw=lw, head=head, z=z)


def key(cv, x, y, w, items, h=6.0, size=6.0):
    """Key strip: items = [(draw, glyph_width, label)], draw(cx, cy) paints the glyph centred there; items are
    spread evenly over the strip."""
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.4", fc="white",
                                   ec=ROLE["neutral"]["stroke"], lw=0.55, ls=(0, (3, 2)), zorder=2))
    widths = [gw + 1.1 + cv.text_width(lab, size) for _, gw, lab in items]
    free = w - sum(widths)
    assert free > 1.6 * (len(items) + 1), f"key strip too narrow by {1.6 * (len(items) + 1) - free:.1f} mm"
    g = free / (len(items) + 1)
    xx = x + g
    for (draw, gw, lab), iw in zip(items, widths):
        draw(xx + gw / 2, y + h / 2)
        cv.text(xx + gw + 1.1, y + h / 2 - 0.05, lab, size=size, ha="left", z=12)
        xx += iw + g
