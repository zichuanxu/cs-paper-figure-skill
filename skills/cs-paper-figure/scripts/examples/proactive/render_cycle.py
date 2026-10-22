"""Redesign of Fig. 6 of "Proactive AI for Superintelligent Agents": six interacting capacities.

Content from the source figure: Awareness -> Anticipation -> Agenda -> Arbitration -> Action -> Awareness,
Adaptation exchanging with all five, and the household running example (owner stressed, groceries low,
dishwasher full, meeting at 6 PM, rain tonight -> forecasts -> candidate goals -> four checks -> prepare
dinner now, others later -> learning updates).

Kept from the original: the ring with Adaptation at its centre, one illustrated household scene per
capacity, the running example as short items. Fixed: each capacity keeps its series colour (shared with
every other figure via sixa.py), headers are solid with white titles, the forecasts sit as vector text
inside the robot's thought cloud instead of pixels, and all text is at least 6.2 pt.

    python render_cycle.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sixa import SIXA  # noqa: E402
from paperkit import Canvas, INK  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402

VIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vignettes")
FLOW = "#3F4652"
W, CW, CH, GX, GY, LANE = 178, 56.0, 49.0, 4.0, 7.0, 6.0
H = 1.0 + CH + GY + CH + LANE


def rbox(cv, x, y, w, h, fc, ec="none", lw=0.0, r=1.4, z=5, alpha=1.0):
    cv.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw,
                                   zorder=z, alpha=alpha))


def card(cv, x, y, w, h, k, name, sub):
    c = SIXA[name]
    rbox(cv, x, y, w, h, c["fill"], c["stroke"], 0.7, r=2.2, z=3)
    rbox(cv, x, y + h - 7.2, w, 7.2, c["mark"], r=2.2, z=4)
    rbox(cv, x, y + h - 7.2, w, 3.0, c["mark"], r=0.0, z=4)  # square the band's lower corners
    cv.ax.add_patch(Circle((x + 4.4, y + h - 3.6), 2.2, fc="white", ec="none", zorder=5))
    cv.text(x + 4.4, y + h - 3.65, str(k), size=8.0, weight="bold", color=c["mark"], z=6)
    cv.text(x + 7.8, y + h - 3.6, name, size=10.0, weight="bold", color="white", ha="left", z=6)
    cv.text(x + 2.0, y + h - 10.0, sub, size=7.0, color=c["ink"], ha="left", style="italic", z=6)
    return c


def white_region(path, aspect, focus, seed, inset=(0.1, 0.1, 0.1, 0.08)):
    """Box (fractions of the cropped vignette, y from the top) inside the white thought cloud, found by
    flood-filling the near-white pixels from `seed` after the same cover crop cv.image applies; `inset`
    (left, top, right, bottom) keeps chips off the cloud's bumpy outline."""
    from PIL import Image, ImageDraw
    im = Image.open(path).convert("L")
    if im.width / im.height > aspect:
        cw = round(im.height * aspect)
        x = round(min(max(focus[0] * im.width - cw / 2, 0), im.width - cw))
        im = im.crop((x, 0, x + cw, im.height))
    else:
        ch = round(im.width / aspect)
        y = round(min(max(focus[1] * im.height - ch / 2, 0), im.height - ch))
        im = im.crop((0, y, im.width, y + ch))
    m = im.point(lambda v: 255 if v >= 236 else 0)
    ImageDraw.floodfill(m, (round(seed[0] * m.width), round(seed[1] * m.height)), 128)
    x0, y0, x1, y1 = m.point(lambda v: 255 if v == 128 else 0).getbbox()
    w, h = x1 - x0, y1 - y0
    return ((x0 + inset[0] * w) / m.width, (y0 + inset[1] * h) / m.height,
            (x1 - inset[2] * w) / m.width, (y1 - inset[3] * h) / m.height)


def items(cv, x, ytop, rows, c, w, check=False, size=6.4, lh=4.6, fill_h=None):
    """White list panel with one row per running-example item; fill_h stretches the row pitch so the
    panel ends level with the scene beside it (no half-empty card)."""
    n = sum(r.count("\n") + 1 for r in rows)
    if fill_h:
        lh = (fill_h - 3.0 - n * 2.9) / (len(rows) - 1) + 2.9
    h = n * 2.9 + (len(rows) - 1) * (lh - 2.9) + 3.0
    rbox(cv, x, ytop - h, w, h, "white", c["stroke"], 0.45, r=1.2, z=6)
    y = ytop - 2.4
    for r in rows:
        nl = r.count("\n")
        yy = y - nl * 1.45
        if check:
            cv.icon_check(x + 2.1, y, 1.6, color=c["mark"], lw=0.8, z=8)
        else:
            cv.ax.add_patch(Circle((x + 2.0, y), 0.7, fc=c["mark"], ec="none", zorder=8))
        cv.text(x + 3.8, yy, r, size=size, color=INK, ha="left", z=8, linespacing=1.05)
        y -= lh + nl * 2.9
    return ytop - h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="sans", size=7.4)
    xs = [1.0, 1.0 + CW + GX, 1.0 + 2 * (CW + GX)]
    yt, yb = LANE + CH + GY, LANE
    body = CH - 13.0  # content height under header and subtitle
    # 1 Awareness: scene + what it notices
    c = card(cv, xs[0], yt, CW, CH, 1, "Awareness", "continuously monitor the situation")
    cv.image(os.path.join(VIG, "h_aware.jpg"), xs[0] + 1.6 + 14.5, yt + 1.6 + body / 2, 29.0, fit="cover", h=body,
             radius=1.4, focus=(0.55, 0.5), z=5)
    items(cv, xs[0] + 32.0, yt + 1.6 + body, ["Owner stressed", "Groceries low", "Dishwasher full", "Meeting at 6 PM",
                                              "Rain tonight"], c, CW - 33.6, fill_h=body)
    # 2 Anticipation: forecasts inside the robot's thought cloud (vector text, not pixels)
    c = card(cv, xs[1], yt, CW, CH, 2, "Anticipation", "predict future needs and outcomes")
    vw = CW - 3.2
    cv.image(os.path.join(VIG, "h_anticipate.jpg"), xs[1] + 1.6 + vw / 2, yt + 1.6 + body / 2, vw, fit="cover", h=body,
             radius=1.4, focus=(0.42, 0.33), z=5)
    # the forecasts go inside the cloud, measured from the picture, flowed so they cannot collide or spill
    fx0, fy0, fx1, fy1 = white_region(os.path.join(VIG, "h_anticipate.jpg"), vw / body, (0.42, 0.33), seed=(0.6, 0.22))
    rx0, rx1 = xs[1] + 1.6 + fx0 * vw, xs[1] + 1.6 + fx1 * vw
    ry1, ry0 = yt + 1.6 + body * (1 - fy0), yt + 1.6 + body * (1 - fy1)
    fc = ["Owner may work late", "Groceries will run out", "Dinner time approaching", "Dishwasher will fill up",
          "Rain expected tonight"]
    for size in (6.2, 6.0, 5.8, 5.6, 5.4):  # largest size whose rows fit the cloud
        h, rg = size * 0.52, 0.5
        widths = [cv.text_width(s, size) + 1.4 for s in fc]
        rows, cur = 1, 0.0
        for wd in widths:
            if cur and cur + 0.8 + wd > rx1 - rx0:
                rows, cur = rows + 1, 0.0
            cur += wd + (0.8 if cur else 0.0)
        if rows * h + (rows - 1) * rg <= ry1 - ry0:
            break
    else:
        raise SystemExit("forecasts do not fit the thought cloud at >= 5.4 pt; shorten them or enlarge the card")
    top = (ry0 + ry1) / 2 + (rows * h + (rows - 1) * rg) / 2
    cv.flow_chips(fc, rx0, rx1, top, c, size=size, h=h, pad=0.7, gap=0.8, row_gap=rg, region=(rx0, ry0, rx1, ry1))
    # 3 Agenda: candidate goals
    c = card(cv, xs[2], yt, CW, CH, 3, "Agenda", "generate candidate goals to address gaps")
    cv.image(os.path.join(VIG, "h_agenda.jpg"), xs[2] + 1.6 + 13.5, yt + 1.6 + body / 2, 27.0, fit="cover", h=body,
             radius=1.4, focus=(0.6, 0.45), z=5)
    items(cv, xs[2] + 30.0, yt + 1.6 + body, ["Prepare dinner", "Order groceries", "Start dishwasher",
                                              "Close windows\nbefore rain", "Bring in laundry"], c, CW - 31.6, fill_h=body)
    # 4 Arbitration: the four checks pass for one goal
    c = card(cv, xs[2], yb, CW, CH, 4, "Arbitration", "decide whether, when and how to act")
    cv.image(os.path.join(VIG, "h_arbitrate.jpg"), xs[2] + 1.6 + 11.0, yb + 1.6 + body / 2, 22.0, fit="cover", h=body,
             radius=1.4, focus=(0.45, 0.45), z=5)
    bot = items(cv, xs[2] + 25.0, yb + 1.6 + body, ["Enough confidence", "Worthwhile", "Good timing",
                                                    "Safe & reversible"], c, CW - 26.6, check=True, lh=4.2)
    rbox(cv, xs[2] + 25.0, yb + 1.6, CW - 26.6, bot - yb - 3.6, c["mark"], r=1.4, z=6)
    cv.text(xs[2] + 25.0 + (CW - 26.6) / 2, (yb + 1.6 + bot - 2.0) / 2 + 1.6, "Prepare dinner now",
            size=7.0, weight="bold", color="white", z=8)
    cv.text(xs[2] + 25.0 + (CW - 26.6) / 2, (yb + 1.6 + bot - 2.0) / 2 - 1.8, "others later", size=6.4, color="white", z=8)
    # 5 Action: the chosen action, carried out
    c = card(cv, xs[0], yb, CW, CH, 5, "Action", "execute the chosen action appropriately")
    cv.image(os.path.join(VIG, "h_act.jpg"), xs[0] + 1.6 + vw / 2, yb + 1.6 + body / 2, vw, fit="cover", h=body,
             radius=1.4, focus=(0.5, 0.42), z=5)
    cv.chip(xs[0] + CW - 3.0, yb + 5.0, "Now: preparing dinner", c, size=6.8, h=4.0, pad=1.2, solid=True, z=8, ha="right")
    # 6 Adaptation in the centre, exchanging with all five
    ax_, aw, ah = xs[1] + 2.0, CW - 4.0, CH - 6.0
    ay = yb + 3.0
    c = card(cv, ax_, ay, aw, ah, 6, "Adaptation", "learn from outcomes and feedback")
    ab = ah - 13.0
    cv.image(os.path.join(VIG, "h_adapt.jpg"), ax_ + 1.6 + 11.5, ay + 1.6 + ab / 2, 23.0, fit="cover", h=ab,
             radius=1.4, focus=(0.55, 0.45), z=5)
    items(cv, ax_ + 26.0, ay + 1.6 + ab, ["Update knowledge", "Refine preferences", "Calibrate thresholds",
                                          "Improve actions"], c, aw - 27.6, fill_h=ab)
    ad = dict(color=c["mark"], lw=0.9, head=1.2, dashed=True, both=True)
    cv.arrow([(xs[1] + CW / 2, ay + ah + 0.3), (xs[1] + CW / 2, yt - 0.3)], **ad)
    cv.arrow([(ax_ - 0.3, ay + ah / 2), (xs[0] + CW + 0.3, ay + ah / 2)], **ad)
    cv.arrow([(ax_ + aw + 0.3, ay + ah / 2), (xs[2] - 0.3, ay + ah / 2)], **ad)
    cv.arrow([(ax_ + 3.0, ay + ah + 0.3), (xs[0] + CW - 3.0, yt - 0.3)], **ad)
    cv.arrow([(ax_ + aw - 3.0, ay + ah + 0.3), (xs[2] + 3.0, yt - 0.3)], **ad)
    # the main cycle (solid): 1 -> 2 -> 3 -> 4 -> 5 -> 1
    f = dict(color=FLOW, lw=1.6, head=1.8)
    yy = yt + CH * 0.62
    cv.arrow([(xs[0] + CW + 0.2, yy), (xs[1] - 0.4, yy)], **f)
    cv.arrow([(xs[1] + CW + 0.2, yy), (xs[2] - 0.4, yy)], **f)
    cv.arrow([(xs[2] + CW * 0.5, yt - 0.2), (xs[2] + CW * 0.5, yb + CH + 0.4)], **f)
    cv.arrow([(xs[2] + CW * 0.5, yb - 0.2), (xs[2] + CW * 0.5, 1.6), (xs[0] + CW * 0.5, 1.6), (xs[0] + CW * 0.5, yb - 0.4)],
             radius=2.0, **f)
    cv.arrow([(xs[0] + CW * 0.5, yb + CH + 0.2), (xs[0] + CW * 0.5, yt - 0.4)], **f)
    assert not cv.overlaps() and not cv.text_overlaps(), cv.overlaps() + cv.text_overlaps()
    print("\n".join(cv.save(os.path.join(a.out, "proactive_cycle"))))


if __name__ == "__main__":
    main()
