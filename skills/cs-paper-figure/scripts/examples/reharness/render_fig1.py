"""Redesign of Fig. 1 of ReHarness (arXiv 2610.12668): from stateful harnesses to backward revision.

Content from the source figure: the same sorting toy example in both panels (tau_{t-1}: sort descending
{3,7,4} -> {7,4,3}, correct; tau_t: sort ascending {2,9,5} -> {9,5,2}, wrong; tau_{t+1}: sort ascending
{3,7,4}); memory states h written by the memory agent pi_M and read by the decision agent pi_D; in (b) a
revision agent pi_R refines R_{t-1} into R'_{t-1} using feedback from tau_t, so tau_{t+1} becomes correct.
Edge numbers and legend text follow the source.

Changes: one shared column grid for both panels (the eye compares straight down), the revision layer as
its own row that exists only in (b), numbered badges sitting on their arrows, the legend beside each
panel, and the headline outcome at tau_{t+1} marked by the card border. Architecture register (2026-11):
each panel is a dashed section frame with a pill tab, each row a tinted lane with its own side tab, the
toy example drawn as number tokens (input -> output, output coloured correct/wrong), the revision agent
as the one solid hero tab, and a key strip at the bottom.

    python render_fig1.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import Canvas, INK, MUTED, ROLE  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

FWD = dict(fill="#E3F1F8", soft="#C6E3F0", stroke="#2C7FA8", ink="#0F4C6B", mark="#1F6F9A")   # forward write/read
REV = dict(fill="#FBE7E3", soft="#F5CEC6", stroke="#C0604E", ink="#7E2A1C", mark="#B04A36")   # backward revision
NEU = ROLE["neutral"]
GOOD, BAD = "#2E8B57", "#B5523F"
W, H = 178, 159
COLS = [15.0, 56.0, 97.0]  # left edges of the three instance columns
CW = 35.0


def node(cv, cx, cy, label, c, d=5.4, dashed=False):
    cv.ax.add_patch(Circle((cx, cy), d / 2, fc=c["fill"], ec=c["stroke"], lw=0.8, zorder=9,
                           ls=(0, (2, 1.4)) if dashed else "-"))
    cv.text(cx, cy, label, size=7.2, color=c["ink"], z=10)


GOODR = dict(fill="#E6F3EA", soft="#CDE8D6", stroke="#3E8E5E", ink="#1E5B36", mark=GOOD)
BADR = dict(fill="#FBEAE6", soft="#F4D2CA", stroke="#C0604E", ink="#7E2A1C", mark=BAD)


def card(cv, x, y, h, tau, task, xs, ys, ylab, ok, outcome_border=False):
    """Instance card: the task line, then the toy example as tokens (input -> output, output coloured by
    correctness), with y labelled under the output."""
    cv.box(x, y, CW, h, "neutral", fill="white", stroke=(GOOD if ok else BAD) if outcome_border else "#4B5563",
           lw=1.3 if outcome_border else 0.6, radius=1.6, shadow=outcome_border)
    node(cv, x + 2.4, y + h, tau, NEU, d=5.0)
    cv.tab(x + CW - 19.0, y + h - 2.0, 18.0, 4.0, NEU, r"decision agent $\pi_D$", size=5.9)
    cv.text(x + 2.0, y + h - 5.4, task, size=6.4, color=INK, ha="left")
    tw, tg, ty = 3.2, 0.4, y + h - 11.6
    cv.tokens(x + 2.0, ty, 3, w=tw, h=tw, gap=tg, r=NEU, labels=[str(v) for v in xs], size=6.4)
    ox = x + 2.0 + 3 * tw + 2 * tg
    cv.arrow([(ox + 0.8, ty + tw / 2), (ox + 3.6, ty + tw / 2)], head=1.0, lw=0.6)
    cv.tokens(ox + 4.4, ty, 3, w=tw, h=tw, gap=tg, r=GOODR if ok else BADR, labels=[str(v) for v in ys], size=6.4)
    cv.text(ox + 4.4 + (3 * tw + 2 * tg) / 2, ty - 2.2, ylab, size=6.2, color=MUTED)
    bx, by = x + CW - 4.0, y + 3.2
    cv.ax.add_patch(Circle((bx, by), 1.9, fc=GOOD if ok else BAD, ec="none", zorder=9))
    (cv.icon_check if ok else cv.icon_cross)(bx, by, 1.6, color="white", lw=0.8, z=10)


def lane(cv, y, h, c, name, fill=None):
    """Tinted full-width row with its name on a vertical side tab in the row's hue."""
    cv.box(9.0, y, 127.0, h, "neutral", fill=fill or c["fill"], stroke=c["stroke"], lw=0.4, radius=1.4, z=1.5,
           alpha=0.9, container=True)
    cv.tab(3.6, y, 4.4, h, c, name, size=6.2, rotate=True, z=2)


def mem(cv, x, y, h, label, tab, lines, c, hero=False):
    cv.box(x, y, CW, h, "neutral", fill=c["soft"], stroke=c["stroke"], lw=0.8, radius=1.6, shadow=True)
    node(cv, x + 2.4, y + h, label, c, d=5.0)
    cv.tab(x + CW - 19.0, y + h - 2.0, 18.0, 4.0, c, tab, size=5.9, solid=hero)
    for j, t in enumerate(lines):
        cv.text(x + 2.0, y + h - 5.0 - j * 3.3, t, size=6.2, color=c["ink"], ha="left")


def edge(cv, pts, c, k=None, seg=-1, at=0.5, lw=0.8, z=8, halo=False):
    """Arrow with its number badge sitting on segment `seg` (the legend explains the number)."""
    cv.arrow(pts, color=c["mark"], lw=lw, head=1.1, z=z, halo=halo)
    if k is not None:
        (x0, y0), (x1, y1) = pts[seg - 1] if seg != 0 else pts[0], pts[seg]
        bx, by = x0 + (x1 - x0) * at, y0 + (y1 - y0) * at
        cv.ax.add_patch(Circle((bx, by), 1.55, fc="white", ec=c["mark"], lw=0.7, zorder=z + 4))
        cv.text(bx, by - 0.05, str(k), size=5.9, color=c["ink"], weight="bold", z=z + 5)


def legend(cv, x, y, items):
    """Typed-edge legend: numbered badge, edge type in its colour, then what happens."""
    for k, (c, typ, src, text) in enumerate(items, 1):
        cv.ax.add_patch(Circle((x + 1.6, y), 1.55, fc="white", ec=c["mark"], lw=0.7, zorder=12))
        cv.text(x + 1.6, y - 0.05, str(k), size=5.9, color=c["ink"], weight="bold", z=13)
        cv.text(x + 4.2, y, typ, size=6.5, color=c["ink"], weight="bold", ha="left")
        cv.text(x + 4.2 + cv.text_width(typ, 6.5, "bold") + 1.2, y, src, size=6.3, color=MUTED, ha="left")
        for j, t in enumerate(text):
            cv.text(x + 4.2, y - 3.4 - j * 3.2, t, size=6.2, color=INK, ha="left")
        y -= 3.6 + 3.2 * len(text) + 1.2


def panel(cv, y0, letter, title, revised, bottom):
    cv.section(1.0, bottom, W - 2.0, y0 + 5.5 - bottom, REV if revised else FWD, title, letter=letter, tab="top",
               size=8.0, fill="#FFFFFF" if not revised else "#FFFBFA")
    ch, cy = 18.0, y0 - 21.0          # trajectory cards
    mh, my = 12.0, cy - 33.0          # memory row, with a 21 mm channel for reads and writes
    # lane tops sit 4 mm above the row so the state circles and agent pills clear the lane edge
    lane(cv, cy - 2.0, ch + 6.0, NEU, "instance", fill="white")
    lane(cv, my - 1.2, mh + 5.2, FWD, "memory")
    card(cv, COLS[0], cy, ch, r"$\tau_{t-1}$", "$x_{t-1}$: sort descending", (3, 7, 4), (7, 4, 3), "$y_{t-1}$", True)
    card(cv, COLS[1], cy, ch, r"$\tau_t$", "$x_t$: sort ascending", (2, 9, 5), (9, 5, 2), "$y_t$", False)
    card(cv, COLS[2], cy, ch, r"$\tau_{t+1}$", "$x_{t+1}$: sort ascending", (3, 7, 4),
         (3, 4, 7) if revised else (7, 4, 3), "$y_{t+1}$", revised, outcome_border=True)
    hx, mid = COLS[0] + CW / 2, my + mh / 2
    node(cv, hx, mid, r"$h_{t-1}$", FWD, d=6.4)
    mem(cv, COLS[1], my, mh, r"$h_t$", r"memory agent $\pi_M$", ["$R_{t-1}$: put larger numbers first"], FWD)
    mem(cv, COLS[2], my, mh, r"$h_{t+1}$", r"memory agent $\pi_M$",
        [r"$R^{\prime}_{t-1}$: larger first only if descending", "$R_t$: smaller first only if ascending"] if revised
        else ["$R_{t-1}$: put larger numbers first", "$R_t$: put smaller numbers first"], FWD)
    a = dict(color=FWD["mark"], lw=0.8, head=1.0)
    cv.arrow([(hx - 8.0, mid), (hx - 3.4, mid)], **a)
    cv.arrow([(hx, mid + 3.2), (hx, cy)], **a)
    cv.arrow([(hx + 3.2, mid), (COLS[1], mid)], **a)
    cv.arrow([(COLS[1] + CW, mid), (COLS[2], mid)], **a)
    cv.arrow([(COLS[2] + CW, mid), (COLS[2] + CW + 3.0, mid)], **a)
    # writes leave the card's right side and drop through the gutter; reads rise from the memory box
    wy = my + mh + 6.5
    for k, col in ((1, 0), ((4 if revised else 3), 1)):
        gx = COLS[col] + CW + (2.0 if col == 0 else 4.0)
        edge(cv, [(COLS[col] + CW, cy + 11.0), (gx, cy + 11.0), (gx, wy), (COLS[col + 1] + 8.0, wy),
                  (COLS[col + 1] + 8.0, my + mh)], FWD, k, seg=2, at=0.843)  # badge in the open channel
    for k, col in ((2, 1), ((5 if revised else 4), 2)):
        edge(cv, [(COLS[col] + 13.0, my + mh), (COLS[col] + 13.0, cy)], FWD, k)
    if revised:
        rh, ry = 11.0, my - 17.5
        rmid = ry + rh / 2
        lane(cv, ry - 1.2, rh + 5.2, REV, "revision")
        node(cv, hx, rmid, r"$h^{\prime}_{t-1}$", REV, d=6.4)
        mem(cv, COLS[1], ry, rh, r"$h^{\prime}_t$", r"revision agent $\pi_R$",
            [r"$R^{\prime}_{t-1}$: larger first only if descending"], REV, hero=True)
        node(cv, COLS[2] + CW / 2, rmid, r"$h^{\prime}_{t+1}$", REV, d=6.4)
        r = dict(color=REV["mark"], lw=0.8, head=1.0)
        cv.arrow([(hx, mid - 3.2), (hx, rmid + 3.2)], **r)                      # h_{t-1} -> h'_{t-1}
        cv.arrow([(hx + 3.2, rmid), (COLS[1] - 2.2, rmid), (COLS[1] - 2.2, my + 2.4), (COLS[1], my + 2.4)],
                 radius=0.8, **r)                                                # h'_{t-1} -> h_t
        cv.arrow([(COLS[1] + 13.0, my), (COLS[1] + 13.0, ry + rh)], **r)        # h_t -> pi_R
        # (3) backward revision: feedback from tau_t, down the right gutter, bridging the memory chain
        gx = COLS[1] + CW + 1.8
        edge(cv, [(COLS[1] + CW, cy + 5.0), (gx, cy + 5.0), (gx, ry + rh - 3.0), (COLS[1] + CW, ry + rh - 3.0)],
             REV, 3, seg=2, at=0.232, lw=1.1, z=11)  # above badge 4, not beside it
        # white casing only where it bridges the memory chain (a full-length halo cut the box borders)
        cv.ax.add_patch(Rectangle((gx - 0.65, mid - 1.0), 1.3, 2.0, fc="white", ec="none", zorder=10.9))
        cv.arrow([(COLS[1] + CW, ry + 2.6), (COLS[2] + 3.4, ry + 2.6), (COLS[2] + 3.4, my)], radius=0.8, lw=1.0,
                 color=REV["mark"], head=1.1)                                    # h'_t -> h_{t+1}
        cv.arrow([(COLS[2] + CW / 2, my), (COLS[2] + CW / 2, rmid + 3.2)], **r)  # h_{t+1} -> h'_{t+1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="serif", size=7.0)
    ya, yb = H - 8.5, 84.5
    panel(cv, ya, "a", "Stateful harness", False, 92.0)
    panel(cv, yb, "b", "ReHarness", True, 11.0)
    LX = 138.0
    legend(cv, LX, ya - 6.0, [
        (FWD, "Forward write", r"$\tau_{t-1}\to h_t$", [r"$\pi_M$ adds $R_{t-1}$ to $h_t$"]),
        (FWD, "Forward read", r"$h_t\to\tau_t$", [r"retrieves $R_{t-1}$, misleading $\pi_D$"]),
        (FWD, "Forward write", r"$\tau_t\to h_{t+1}$", [r"$\pi_M$ adds $R_t$ to $h_{t+1}$"]),
        (FWD, "Forward read", r"$h_{t+1}\to\tau_{t+1}$", [r"retrieves $R_{t-1}$ again, misleading $\pi_D$"]),
    ])
    legend(cv, LX, yb - 6.0, [
        (FWD, "Forward write", r"$\tau_{t-1}\to h_t$", [r"$\pi_M$ adds $R_{t-1}$ to $h_t$"]),
        (FWD, "Forward read", r"$h_t\to\tau_t$", [r"retrieves $R_{t-1}$, misleading $\pi_D$"]),
        (REV, "Backward revision", r"$\tau_t\to h^{\prime}_t$", [r"$\pi_R$ refines $R_{t-1}$ into $R^{\prime}_{t-1}$", r"using feedback from $\tau_t$"]),
        (FWD, "Forward write", r"$\tau_t\to h_{t+1}$", [r"$\pi_M$ adds $R_t$, using $R^{\prime}_{t-1}$", "as demonstrations"]),
        (FWD, "Forward read", r"$h_{t+1}\to\tau_{t+1}$", [r"retrieves $R^{\prime}_{t-1}$, guiding $\pi_D$ correctly"]),
    ])
    cv.legend(1.0, 1.0, W - 2.0, [
        ("line", FWD["mark"], "forward write / read"), ("line", REV["mark"], "backward revision (only in ReHarness)"),
        ("box", FWD, r"memory state $h$"), ("box", REV, r"revised state $h^{\prime}$")], size=6.4)
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    print("\n".join(cv.save(os.path.join(a.out, "reharness_fig1"))))


if __name__ == "__main__":
    main()
