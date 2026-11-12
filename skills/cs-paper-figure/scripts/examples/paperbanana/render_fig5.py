"""PaperBanana Figure 5: code generation versus image generation for statistical plots.

Source: Zhu et al., "PaperBanana: Automating Academic Illustration for AI Scientists",
arXiv:2601.23265, Figure 5 (values read from the bar labels of the figure).

Content kept from the source
  * Win rate against human-made plots (%) of the code route and the image-generation route on
    Faithfulness, Conciseness, Readability, Aesthetic and Overall: all ten values.
  * The human reference at 50.

Design decisions
  * One row per dimension with both routes on a shared axis, so the comparison the figure is about
    (code against image, per dimension) is a distance along one line, not two bar heights. The marks
    are dots, so the axis can span 37-63 around the reference without a zero baseline.
  * The axis is centred on 50, the human reference, and the side where the human-made plot is
    preferred is darker: Faithfulness is the only row where both routes fall on it.
  * Rows are grouped as the paper reads them, content (Faithfulness, Conciseness) and presentation
    (Readability, Aesthetic). Each group is a band in the colour of the route that leads in it, so
    the trade-off reads as a blue block over an amber block; Overall is its own neutral row because
    it is judged separately and is not the mean of the four.
  * One colour and one shape per route: blue squares for code, amber discs for image generation.
    The bar between the marks and the lead on the right take the colour of the route that leads.
  * Every lead and every "leads" verdict is computed below from the transcribed values and asserted.
"""
import argparse
import os
import sys

from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import INK, MUTED, ROLE, Canvas, mix  # noqa: E402

STEM = "paperbanana_fig5"

# ---------------------------------------------------------------- data (reported) ---
# win rate against human-made plots, %: (code, image)
SCORES = {
    "Faithfulness": (45.4, 39.6),
    "Conciseness": (62.3, 55.0),
    "Readability": (51.3, 57.1),
    "Aesthetic": (54.4, 62.4),
    "Overall": (56.0, 56.8),
}
HUMAN = 50.0
GROUPS = [("Content", ("Faithfulness", "Conciseness")), ("Presentation", ("Readability", "Aesthetic"))]

# ---------------------------------------------------------------- derived, asserted ---
LEAD = {d: round(c - i, 1) for d, (c, i) in SCORES.items()}  # > 0: code leads
WINNER = {d: "code" if v > 0 else "image" for d, v in LEAD.items()}
assert LEAD == {"Faithfulness": 5.8, "Conciseness": 7.3, "Readability": -5.8, "Aesthetic": -8.0, "Overall": -0.8}
VERDICT = {}
for _g, _dims in GROUPS:
    assert len({WINNER[d] for d in _dims}) == 1, _g  # a group verdict needs every row to agree
    VERDICT[_g] = WINNER[_dims[0]]
assert VERDICT == {"Content": "code", "Presentation": "image"}
BELOW = [d for d, v in SCORES.items() if max(v) < HUMAN]
assert BELOW == ["Faithfulness"] and all(min(v) > HUMAN for d, v in SCORES.items() if d not in BELOW)
assert abs(sum(SCORES[d][0] for _, ds in GROUPS for d in ds) / 4 - SCORES["Overall"][0]) > 1  # not a mean

ROUTE = {"code": ROLE["blue"], "image": ROLE["amber"]}
T, B, A = 8.0, 7.0, 6.2   # title, body, annotation (pt)


def render(out):
    W, H = 140.0, 64.0
    cv = Canvas(W, H, size=B)
    cv.group(0.4, 0.4, W - 0.8, H - 0.8, "neutral", "Statistical plots: code vs. image generation", band=True,
             size=T, fill="white", stroke="#B4BBC5")
    cv.text(2.4, H - 0.4 - T * 0.62 - 2.9, "win rate against human-made plots; 50 = parity with the human-made plot",
            size=A, color=MUTED, style="italic", ha="left")

    bx0, bx1 = 2.4, W - 2.4            # row bands
    xg, xd = 4.6, 23.0                 # group label, dimension label
    px0, px1, lo, hi = 40.0, 112.0, 37.0, 63.0
    xlead = px1 + 9.4
    assert HUMAN - lo == hi - HUMAN and lo < min(min(v) for v in SCORES.values())

    def X(v):
        return px0 + (v - lo) / (hi - lo) * (px1 - px0)

    # one band per group in the colour of the route that leads there; Overall is neutral
    pitch, pad, gap, ytop = 6.6, 3.6, 1.4, 49.8
    rows, bands, y = {}, [], ytop
    for g, dims in GROUPS + [("Overall", ("Overall",))]:
        head = 2.2 if g == GROUPS[0][0] else 0.0  # room for the route names over the first row
        h = head + 2 * pad + pitch * (len(dims) - 1)
        for k, d in enumerate(dims):
            rows[d] = y - head - pad - pitch * k
        fill = mix(ROUTE[VERDICT[g]]["fill"], ROUTE[VERDICT[g]]["soft"], 0.2) if g in VERDICT else "#F1F2F5"
        bands.append((g, y - h, h, fill))
        y -= h + gap
    ybot = y + gap

    for g, yb, h, fill in bands:
        cv.ax.add_patch(FancyBboxPatch((bx0, yb), bx1 - bx0, h, boxstyle="round,pad=0,rounding_size=1.4",
                                       fc=fill, ec="none", zorder=1.5))
        # the side where the human-made plot is preferred is darker
        cv.ax.add_patch(Rectangle((px0, yb), X(HUMAN) - px0, h, fc="#1A2230", ec="none", alpha=0.07, zorder=1.6))
        for v in range(40, 61, 5):
            if v != HUMAN:
                cv.ax.plot([X(v)] * 2, [yb, yb + h], color="white", lw=0.6, zorder=2)
        mid = yb + h / 2 - (1.1 if g == GROUPS[0][0] else 0.0)
        if g in VERDICT:
            cv.text(xg, mid + 1.6, g, size=B, color=INK, weight="bold", ha="left")
            cv.text(xg, mid - 1.6, f"{VERDICT[g]} leads", size=A, color=ROUTE[VERDICT[g]]["ink"], style="italic",
                    ha="left")
        else:
            cv.text(xg, mid, g, size=B, color=INK, weight="bold", ha="left")
    for v in range(40, 61, 5):
        cv.text(X(v), ybot - 2.5, str(v), size=A if v != HUMAN else B, color="#5A626D" if v != HUMAN else INK,
                weight="bold" if v == HUMAN else "normal")
    cv.text((px0 + px1) / 2, ybot - 5.9, "win rate (%)", size=A, color="#5A626D")
    yd = ytop + 2.4
    cv.ax.plot([X(HUMAN)] * 2, [ybot - 0.7, yd + 1.9], color="#3A4250", lw=0.9, zorder=3)
    cv.text(X(HUMAN) - 2.0, yd, "human-made plot preferred", size=A, color=MUTED, style="italic", ha="right")
    cv.text(X(HUMAN) + 2.0, yd, "generated plot preferred", size=A, color=MUTED, style="italic", ha="left")
    wl = cv.text_width("human-made plot preferred", A) + 3.2
    wr = cv.text_width("generated plot preferred", A) + 3.2
    cv.arrow([(X(HUMAN) - wl, yd), (X(HUMAN) - wl - 4.0, yd)], color="#9AA0A8", lw=0.6, head=1.2)
    cv.arrow([(X(HUMAN) + wr, yd), (X(HUMAN) + wr + 4.0, yd)], color="#9AA0A8", lw=0.6, head=1.2)
    cv.text(xlead, yd, "lead, points", size=A, color=MUTED, style="italic", ha="left")

    # rows: a bar from the trailing to the leading route, a mark for each route, both values
    def mark(route, x, y, z):
        c = ROUTE[route]["mark"]
        if route == "code":
            cv.ax.add_patch(FancyBboxPatch((x - 1.1, y - 1.1), 2.2, 2.2, boxstyle="round,pad=0,rounding_size=0.4",
                                           fc=c, ec="white", lw=0.7, zorder=z))
        else:
            cv.ax.add_patch(Circle((x, y), 1.2, fc=c, ec="white", lw=0.7, zorder=z))

    for d, (code, image) in SCORES.items():
        y, win = rows[d], WINNER[d]
        vals = {"code": code, "image": image}
        a, b = sorted(vals, key=vals.get)  # a trails, b leads
        assert b == win
        cv.ax.add_patch(FancyBboxPatch((X(vals[a]), y - 1.1), X(vals[b]) - X(vals[a]), 2.2,
                                       boxstyle="round,pad=0,rounding_size=1.1",
                                       fc=mix(ROUTE[win]["mark"], "#FFFFFF", 0.55), ec="none", zorder=4))
        mark(a, X(vals[a]), y, 6)
        mark(b, X(vals[b]), y, 7)
        xa = X(vals[a]) - 2.2
        if xa - cv.text_width(f"{vals[a]:.1f}", B) < X(HUMAN) + 0.8 < xa + 0.8:
            # the usual spot would straddle the reference line, and left of the line would put a value above
            # 50 on the "human preferred" side: set it over its own mark instead
            cv.text(X(vals[a]), y + 3.0, f"{vals[a]:.1f}", size=B, color=ROUTE[a]["ink"], ha="center")
        else:
            cv.text(xa, y, f"{vals[a]:.1f}", size=B, color=ROUTE[a]["ink"], ha="right")
        cv.text(X(vals[b]) + 2.2, y, f"{vals[b]:.1f}", size=B, color=ROUTE[b]["ink"], ha="left", weight="bold")
        cv.text(xlead, y, f"{win} +{abs(LEAD[d]):.1f}", size=B, color=ROUTE[win]["ink"], weight="bold", ha="left")
        if d != "Overall":
            cv.text(xd, y, d, size=B, color=INK, ha="left")
        if d == "Faithfulness":  # the routes are named once, over the first row
            for r in ("code", "image"):
                cv.text(X(vals[r]), y + 3.3, r, size=A, color=ROUTE[r]["ink"], weight="bold")

    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=".")
    print("\n".join(render(ap.parse_args().out)))
