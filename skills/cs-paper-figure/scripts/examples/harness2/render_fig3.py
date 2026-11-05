"""Redesign of Harness^2 (arXiv 2610.14224) Figure 3: the recursive harnessing pipeline.

Facts (Sec. 2.2-2.3):
  Task-level recursion, one contrastive step Phi on task q_t:
    Propose: reference execution e0 ~ A(q_t; M, H); conditioned on task, harness, reference, history and
      the library in R_t, propose an invariant candidate (agentic deficiencies: planning, tool use, context
      management, delegation) and a domain-specific candidate (knowledge, procedures, constraints).
    Probe: run each candidate on the same task under matched model/environment; behavioural contrast
      with the reference: mitigates the deficiency, leaves it unchanged, or regresses.
    Compose: merge supported changes, revise conflicting edits, adopt one candidate, or preserve the
      current harness; execute the successor H' -> e'; record the step in xi.
    Parallel recursion: k candidates per scope and k compositions; sequential: k chained steps.
  Harnessing-level recursion after each task: reflect on the improvement record D_t; keep lessons only
    when supported by execution contrasts; R_{t+1} = Update(R_t, H*_t, D_t); library entries are an
    executable harness + EXPERIENCE.md. The next task starts from H_0, guided by R_{t+1}.
    Model weights, stage instructions and the decision rule stay fixed; the library evolves.

    python render_fig3.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, INK, MUTED, LINE  # noqa: E402
from render_fig2 import lift, mark  # noqa: E402
from matplotlib.patches import Circle, PathPatch, Rectangle  # noqa: E402
from paperkit import _round_top_rect as _top_band  # noqa: E402

EXE = dict(fill="#EBF2FC", soft="#D2E2F7", stroke="#5A8BCB", ink="#1C4C8C", mark="#2F6FC0")   # executor
EDT = dict(fill="#FFF5E2", soft="#FBE2B4", stroke="#D29A3C", ink="#7A4B0C", mark="#C27C12")   # editor
RFL = dict(fill="#F3EFFB", soft="#E1D6F4", stroke="#8C6CC8", ink="#47297F", mark="#6A45B0")   # reflector / library
INV = dict(fill="#E7F5F2", soft="#C3E5DD", stroke="#3D9C8B", ink="#0E5A4F", mark="#14897A")   # invariant edits
DOM = dict(fill="#FBEFF3", soft="#F3D5E0", stroke="#C27896", ink="#7A2E4A", mark="#A84C72")   # domain edits
GOOD = dict(fill="#ECF5EC", soft="#CFE6CF", stroke="#5E9E62", ink="#25592A", mark="#3F7F44")
BAD = dict(fill="#FDEEEA", soft="#F8D6CC", stroke="#D9826B", ink="#86321F", mark="#D9583B")
NEU = dict(fill="#F3F4F6", soft="#E4E7EB", stroke="#8F98A4", ink="#353C47", mark="#6B7480")
CMP = dict(fill="#F3F5E4", soft="#E2E8BF", stroke="#9AA24A", ink="#4B5217", mark="#7A8424")   # compose stage
W, H = 178, 118
KEY, LA, HB = 8.0, 4.0, 34.0  # key strip under (b); extra lift of (a) over its old frame; height of (b)
NO_ICONS = False


def harness(cv, x, y, c, label, w=7.0, h=9.0, above=False):
    """A harness = a stack of editable component files."""
    for i in (2, 1, 0):
        cv.doc(x + i * 0.9, y + i * 0.9, w, h, c, lines=3, fold=2.0, lw=0.5, z=6 - i * 0.1)
    cv.text(x + w / 2 + 0.9, y + h + 4.0 if above else y - 2.2, label, size=6.6, color=c["ink"])


def run_doc(cv, x, y, label, c=NEU, w=5.6, h=7.2):
    cv.doc(x, y, w, h, c, lines=3, fold=1.6, lw=0.5)
    cv.text(x + w / 2, y - 2.0, label, size=6.3, color=INK)


ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")


def robot(cv, x, y, c, label, s=6.2):
    """Agent role glyph: the bundled illustrated icon when present (icons/<role>.png,
    generated once as a matched set), else the vector robot."""
    name = {id(EXE): "executor", id(EDT): "editor", id(RFL): "reflector"}.get(id(c))
    png = os.path.join(ICON_DIR, f"{name}.png") if name else None
    if png and os.path.exists(png) and not NO_ICONS:
        # the illustrated set carries its role colour itself; no disc behind it
        h = cv.image(png, x, y, s * 1.15, z=12, fit="height")
    else:
        h = s * 1.24
        cv.ax.add_patch(Circle((x, y), s * 0.62, fc=c["fill"], ec=c["stroke"], lw=0.5, zorder=11))
        cv.icon_robot(x, y - 0.2, s * 0.78, color=c["mark"], z=12)
    if label:
        cv.text(x, y - h / 2 - 1.7, label, size=6.2, color=c["ink"], weight="bold")


def diff_lines(cv, x, y, w=8.0):
    """Tiny file diff: two added (+) and one removed (-) line."""
    for k, (sgn, c) in enumerate((("+", GOOD), ("+", GOOD), ("-", BAD))):
        yy = y - k * 1.6
        # the sign as two strokes, not text: stacked 5.6 pt glyph boxes would collide at this line pitch
        cv.ax.plot([x + 0.1, x + 1.0], [yy, yy], color=c["mark"], lw=0.7, zorder=9)
        if sgn == "+":
            cv.ax.plot([x + 0.55] * 2, [yy - 0.45, yy + 0.45], color=c["mark"], lw=0.7, zorder=9)
        cv.ax.plot([x + 1.4, x + w * (0.9 if k < 2 else 0.6)], [yy] * 2, color=c["stroke"], lw=0.8, zorder=9,
                   solid_capstyle="round")


def stage(cv, x0, x1, y0, y1, k, name, c):
    """Stage column: tinted dashed section in the stage hue, named on a pill tab with a numbered badge."""
    cv.section(x0, y0, x1 - x0, y1 - y0, c, name, tab="top", size=7.6, radius=1.6, lw=0.7)
    tw = cv.text_width(name, 7.6, "bold") + 4.0
    cv.badge((x0 + x1) / 2 - tw / 2 - 2.0, y1, k, c, d=3.4, size=6.4)


def panel_task(cv):
    cv.section(2, 34.5, 174, 69.5, NEU, r"Task-level recursion: one contrastive step on task $q_t$", tab="corner",
               letter="a", size=7.6, radius=2.0, fill="white")
    # one tinted column per stage, in the hue of the agent that runs it (Compose: its own olive)
    for k, (x0, x1, c, n) in enumerate(((4.4, 82.6, EDT, "Propose"), (83.6, 127.6, EXE, "Probe"),
                                        (128.6, 172.8, CMP, "Compose")), 1):
        stage(cv, x0, x1, 36.6, 92.0, k, n, c)
    cv.text(12.8, 87.4, "reference run, then two candidates", size=6.0, color=EDT["ink"], ha="left", style="italic")
    # 1 reference run
    harness(cv, 6.4, 70.0, NEU, r"current $\mathcal{H}$")
    cv.arrow([(15.4, 76.0), (21.0, 76.0)], head=1.1)
    robot(cv, 25.5, 76.0, EXE, "executor", s=8.0)
    cv.icon_snow(32.4, 81.8, 2.2, color=EXE["stroke"])
    cv.arrow([(25.5, 67.2), (25.5, 59.6)], head=1.1)
    run_doc(cv, 22.7, 52.0, r"$e_0=(\tau_0, y_0)$")
    cv.text(20.5, 44.4, "how the harness behaves,", size=5.9, color=MUTED, style="italic")
    cv.text(20.5, 41.9, "not whether it is correct", size=5.9, color=MUTED, style="italic")
    # 2 propose
    cv.arrow([(28.3, 55.6), (34.5, 55.6), (34.5, 82.0), (42.5, 82.0)], head=1.1, radius=1.2)
    robot(cv, 46.5, 82.0, EDT, None, s=8.0)
    cv.text(52.4, 84.0, "editor reads task, harness,", size=5.9, color=MUTED, ha="left", style="italic")
    cv.text(52.4, 81.4, r"$e_0$, history, library in $\mathcal{R}_t$", size=5.9, color=MUTED, ha="left", style="italic")
    cv.line([(46.5, 77.0), (46.5, 75.4)])
    cv.dot(46.5, 75.4)
    for (yc, c, title, sub) in ((66.5, INV, "Invariant", "planning · tool use · context · delegation"),
                                 (51.0, DOM, "Domain-specific", "knowledge · procedures · constraints")):
        cv.stack(41.0, yc - 5.4, 39.0, 10.8, n=3, r=c, dx=0.7, dy=0.7, fill="white", lw=0.6, radius=1.3)
        cv.text(43.0, yc + 2.4, title, size=6.9, color=c["ink"], weight="bold", ha="left")
        cv.text(43.0, yc - 2.2, sub, size=5.9, color=INK, ha="left")
        diff_lines(cv, 69.0, yc + 4.0, w=8.6)
    cv.arrow([(46.5, 75.4), (46.5, 72.6)], head=1.0)
    cv.arrow([(46.5, 75.4), (38.0, 75.4), (38.0, 51.0), (41.0, 51.0)], head=1.0, radius=1.0)
    cv.chip(52.0, 43.2, r"parallel: $\times k$ per scope", NEU, size=5.9, pad=0.6)
    # candidates + their diffs also go to Compose (over the empty top of the Probe column)
    cv.arrow([(78.0, 72.6), (78.0, 88.2), (135.2, 88.2), (135.2, 86.9)], color=LINE, lw=0.55, head=1.0, radius=1.0)
    cv.text(105.0, 85.9, "candidate harnesses + diffs", size=5.9, color=MUTED, style="italic")
    # 3 probe under matched conditions
    for (yc, c, lab) in ((66.5, INV, r"$e_{\mathrm{inv}}$"), (51.0, DOM, r"$e_{\mathrm{dom}}$")):
        cv.arrow([(80.7, yc), (86.2, yc)], color=c["mark"], head=1.0)
        robot(cv, 90.2, yc, EXE, None, s=6.4)
        cv.arrow([(94.2, yc), (97.0, yc)], head=1.0)
        run_doc(cv, 97.0, yc - 3.6, lab, c=c, w=5.0, h=7.0)
        cv.arrow([(102.4, yc), (106.4, yc)], head=1.0)
    cv.text(105.6, 78.0, "same model, same environment", size=5.9, color=EXE["ink"], style="italic")
    # the hero: behavioural contrast with the reference run, three possible verdicts per candidate
    cv.box(106.4, 45.4, 20.2, 25.6, EXE, fill="white", lw=0.8, radius=1.3, shadow=True)
    cv.ax.add_patch(PathPatch(_top_band(106.4, 66.4, 20.2, 4.6, 1.3), fc=EXE["mark"], ec="none", zorder=5.6))
    cv.text(116.5, 68.7, "contrast", size=6.6, color="white", weight="bold")
    cv.doc(110.0, 59.4, 3.6, 4.6, NEU, lines=2, fold=1.0, lw=0.4)
    cv.text(115.0, 61.7, r"with $e_0$", size=6.0, color=INK, ha="left")
    for yy, s, c, ic in ((55.2, "mitigates", GOOD, "check"), (51.4, "no change", NEU, None),
                         (47.6, "regresses", BAD, "cross")):
        cv.chip(111.0, yy, s, c, size=6.0, pad=0.8, ha="left")
        if ic:
            getattr(cv, f"icon_{ic}")(109.0, yy, 1.8, color=c["mark"])
        else:
            cv.ax.plot([108.2, 109.8], [yy, yy], color=c["mark"], lw=0.8, zorder=12, solid_capstyle="round")
    # 4 compose
    cv.arrow([(126.6, 58.5), (129.4, 58.5)], head=1.0)
    robot(cv, 135.2, 82.0, EDT, None, s=8.0)
    cv.text(135.2, 75.0, "composer", size=6.0, color=EDT["ink"], weight="bold")
    cv.text(141.2, 83.0, "decisions tied to", size=5.9, color=MUTED, ha="left", style="italic")
    cv.text(141.2, 80.4, "observed contrasts", size=5.9, color=MUTED, ha="left", style="italic")
    for k, s in enumerate(("merge supported", "revise conflicts", "adopt one", "keep current")):
        cv.chip(130.6, 70.0 - k * 4.6, s, CMP, size=6.0, ha="left", pad=0.8)
    tip = cv.brace(152.4, 54.6, 72.2, side="right", depth=1.2)
    cv.arrow([(tip[0] + 0.2, 63.0), (157.4, 63.0)], head=1.1)
    harness(cv, 157.4, 58.0, EDT, r"successor $\mathcal{H}'$", above=True)
    cv.arrow([(161.8, 57.6), (161.8, 50.6)], head=1.0)
    robot(cv, 161.8, 47.2, EXE, None, s=5.6)
    cv.arrow([(165.2, 47.2), (167.4, 47.2)], head=1.0)
    run_doc(cv, 167.4, 43.6, r"$e'$", w=4.8, h=7.0)
    cv.text(129.6, 45.2, r"adopted $\mathcal{H}^{\star}_t$ (selected", size=5.9, color=MUTED, style="italic", ha="left")
    cv.text(129.6, 41.8, r"if $k>1$); deliverable", size=5.9, color=MUTED, style="italic", ha="left")
    cv.text(129.6, 38.4, r"returned; record $\xi$", size=5.9, color=MUTED, style="italic", ha="left")
    # sequential recursion: H' becomes the next step's H. Its legs run inside the Compose / Propose columns
    # (between H' and the frame; over H) and cross each frame top once, never along a frame border
    cv.arrow([(166.4, 64.0), (170.0, 64.0), (170.0, 97.0), (10.8, 97.0), (10.8, 81.2)], color=EDT["stroke"],
             lw=0.6, head=1.0, dashed=True, radius=1.2)
    cv.chip(130.0, 97.0, r"sequential recursion: $\mathcal{H}'$ seeds the next step ($k$ steps)", EDT, size=5.9, pad=0.8)
    cv.chip(129.6, 49.6, r"parallel: $\times k$", NEU, size=5.9, pad=0.6, ha="left")


def panel_harnessing(cv):
    cv.section(2, 2, 174, HB, RFL, "Harnessing-level recursion, after each task", tab="corner", letter="b",
               size=7.6, radius=2.0)
    # improvement record D_t (right, under Compose)
    # drop centred in the 3.2 gap between the Compose frame (172.8) and the panel border (176)
    cv.arrow([(173.0, 47.2 + LA), (174.4, 47.2 + LA), (174.4, 30.0), (158.0, 30.0), (158.0, 27.0)], color=RFL["mark"],
             lw=0.9, head=1.3, radius=1.2)
    cv.text(172.8, 32.0, r"$\mathcal{H}^{\star}_t$, $\xi$", size=6.2, color=RFL["ink"], ha="right")
    # improvement record D_t: one row per kind of entry, marked in the hue of the stage that produced it
    cv.stack(145.0, 4.4, 26.0, 22.4, n=2, r=NEU, dx=0.8, dy=0.8, fill="white", lw=0.5, radius=1.2)
    cv.text(147.0, 23.6, r"$\mathcal{D}_t$", size=7.4, color=INK, ha="left")
    cv.text(151.4, 23.4, "improvement record", size=6.0, color=MUTED, ha="left", style="italic")
    cv.line([(146.0, 21.4), (170.0, 21.4)], color="#D5DAE0", lw=0.4)
    for k, (s_, c) in enumerate((("references", EDT), ("candidates", EDT), ("probes", EXE), ("decisions", CMP),
                                 ("selected result", CMP))):
        yy = 19.2 - k * 3.1
        cv.ax.add_patch(Rectangle((147.0, yy - 1.0), 2.0, 2.0, fc=c["soft"], ec=c["stroke"], lw=0.4, zorder=7))
        cv.text(150.6, yy, s_, size=5.9, color=c["ink"], ha="left")
    # reflect
    cv.arrow([(145.0, 15.0), (135.2, 15.0)], color=RFL["mark"], lw=0.9, head=1.3)
    robot(cv, 130.0, 16.4, RFL, "reflector", s=8.0)
    cv.text(107.5, 19.6, "keeps a lesson only if", size=6.0, color=INK)
    cv.text(107.5, 16.8, "execution contrasts support it", size=6.0, color=INK)
    cv.text(107.5, 11.6, r"$\mathcal{R}_{t+1}=\mathrm{Update}(\mathcal{R}_t,\ \mathcal{H}^{\star}_t,\ \mathcal{D}_t)$",
            size=6.8, color=RFL["ink"])
    cv.arrow([(124.8, 15.0), (92.0, 15.0)], color=RFL["mark"], lw=0.9, head=1.3)
    # library (under Propose)
    cy0, ch = 3.8, 21.2
    cv.cylinder(57.0, cy0, 35.0, ch, RFL)
    rim = cy0 + ch - min(ch * 0.22, 35.0 * 0.22)  # lowest point of the top ellipse's front rim
    for k in range(3):
        xx = 61.0 + k * 8.4
        cv.doc(xx, 7.6, 3.4, 4.6, RFL, lines=2, fold=1.0, lw=0.4)
        cv.doc(xx + 3.6, 7.6, 3.4, 4.6, EDT, lines=2, fold=1.0, lw=0.4)
    cv.text(74.5, rim - 2.6, r"improvement harness $\mathcal{R}$", size=6.4, color=RFL["ink"], weight="bold")
    cv.text(74.5, rim - 6.0, "library: harness + EXPERIENCE.md", size=5.9, color=RFL["ink"])
    cv.icon_cycle(87.6, 10.0, 2.6, color=RFL["mark"])
    # guides proposals of the next task
    cv.arrow([(78.0, cy0 + ch - 0.6), (78.0, 44.6 + LA)], color=RFL["mark"], lw=0.9, head=1.3, dashed=True)
    cv.text(94.0, 28.4, r"guides $q_{t+1}$ (Propose, Probe, Compose),", size=5.9, color=RFL["ink"], ha="left", style="italic")
    cv.text(94.0, 25.2, r"which starts again from $\mathcal{H}_0$", size=5.9, color=RFL["ink"], ha="left", style="italic")
    cv.text(6.0, 26.4, "agent roles", size=6.0, color=MUTED, ha="left", style="italic")
    for x, c, lab in ((14.0, EXE, "executor"), (28.0, EDT, "editor /\ncomposer"), (42.0, RFL, "reflector")):
        robot(cv, x, 16.8, c, None, s=6.0)
        cv.text(x, 12.0, lab, size=5.8, color=c["ink"], linespacing=0.95, va="top")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    ap.add_argument("--vector-icons", action="store_true", help="ignore icons/*.png and draw vector robots")
    a = ap.parse_args()
    global NO_ICONS
    NO_ICONS = a.vector_icons
    cv = Canvas(W, H, family="serif", size=7.0)
    m = mark(cv)
    panel_task(cv)
    lift(cv, LA, m)  # (a) sits LA higher than its old frame, making room for a taller (b)
    panel_harnessing(cv)
    lift(cv, KEY)
    cv.legend(2, 1.0, 174, [("snow", "#4A90C8", "fixed: model weights, stage instructions, decision rule"),
                            ("cycle", RFL["mark"], "evolves: the library"),
                            ("dash", EDT["stroke"], r"$\mathcal{H}'$ seeds the next step"),
                            ("dash", RFL["mark"], r"$\mathcal{R}_{t+1}$ guides the next task"),
                            ("abbr", "+ \u2212", "lines added / removed")], size=6.0, gap=3.6)
    assert not cv.wire_crossings(), cv.wire_crossings()
    print("\n".join(cv.save(os.path.join(a.out, "harness2_fig3_pipeline"))))
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()


if __name__ == "__main__":
    main()
