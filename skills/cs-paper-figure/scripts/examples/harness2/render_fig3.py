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
from matplotlib.patches import Circle  # noqa: E402

EXE = dict(fill="#EBF2FC", soft="#D2E2F7", stroke="#5A8BCB", ink="#1C4C8C", mark="#2F6FC0")   # executor
EDT = dict(fill="#FFF5E2", soft="#FBE2B4", stroke="#D29A3C", ink="#7A4B0C", mark="#C27C12")   # editor
RFL = dict(fill="#F3EFFB", soft="#E1D6F4", stroke="#8C6CC8", ink="#47297F", mark="#6A45B0")   # reflector / library
INV = dict(fill="#E7F5F2", soft="#C3E5DD", stroke="#3D9C8B", ink="#0E5A4F", mark="#14897A")   # invariant edits
DOM = dict(fill="#FBEFF3", soft="#F3D5E0", stroke="#C27896", ink="#7A2E4A", mark="#A84C72")   # domain edits
GOOD = dict(fill="#ECF5EC", soft="#CFE6CF", stroke="#5E9E62", ink="#25592A", mark="#3F7F44")
BAD = dict(fill="#FDEEEA", soft="#F8D6CC", stroke="#D9826B", ink="#86321F", mark="#D9583B")
NEU = dict(fill="#F3F4F6", soft="#E4E7EB", stroke="#8F98A4", ink="#353C47", mark="#6B7480")
W, H = 178, 106


def harness(cv, x, y, c, label, w=7.0, h=9.0):
    """A harness = a stack of editable component files."""
    for i in (2, 1, 0):
        cv.doc(x + i * 0.9, y + i * 0.9, w, h, c, lines=3, fold=2.0, lw=0.5, z=6 - i * 0.1)
    cv.text(x + w / 2 + 0.9, y - 2.2, label, size=6.6, color=c["ink"])


def run_doc(cv, x, y, label, c=NEU, w=5.6, h=7.2):
    cv.doc(x, y, w, h, c, lines=3, fold=1.6, lw=0.5)
    cv.text(x + w / 2, y - 2.0, label, size=6.3, color=INK)


def robot(cv, x, y, c, label, s=6.2):
    cv.ax.add_patch(Circle((x, y), s * 0.62, fc=c["fill"], ec=c["stroke"], lw=0.5, zorder=11))
    cv.icon_robot(x, y - 0.2, s * 0.78, color=c["mark"], z=12)
    if label:
        cv.text(x, y - s * 0.62 - 2.0, label, size=6.2, color=c["ink"], weight="bold")


def diff_lines(cv, x, y, w=8.0):
    """Tiny file diff: two added (+) and one removed (-) line."""
    for k, (sgn, c) in enumerate((("+", GOOD), ("+", GOOD), ("-", BAD))):
        yy = y - k * 1.5
        cv.text(x, yy, sgn, size=5.6, color=c["mark"], weight="bold", ha="left")
        cv.ax.plot([x + 1.4, x + w * (0.9 if k < 2 else 0.6)], [yy] * 2, color=c["stroke"], lw=0.8, zorder=9,
                   solid_capstyle="round")


def stage(cv, x, y, k, name):
    cv.ax.add_patch(Circle((x, y), 1.6, fc=INK, ec="none", zorder=12))
    cv.text(x, y - 0.05, str(k), size=6.2, color="white", weight="bold", z=13)
    cv.text(x + 2.4, y, name, size=7.4, color=INK, weight="bold", ha="left")


def panel_task(cv):
    cv.group(2, 35, 174, 69, NEU, r"(a) Task-level recursion: one contrastive step on task $q_t$", band=True,
             size=7.6, radius=2.0, lw=0.7, fill="white")
    for i, (x, name) in enumerate(((5.0, "Propose"), (86.0, "Probe"), (131.0, "Compose")), 1):
        stage(cv, x, 92.6, i, name)
    cv.text(18.6, 92.6, "reference run, then two candidates", size=6.0, color=MUTED, ha="left", style="italic")
    for x in (83.0, 128.0):
        cv.ax.plot([x, x], [40.5, 95.0], color="#E6E9ED", lw=0.6, zorder=1)
    # 1 reference run
    harness(cv, 5.0, 70.0, NEU, r"current $\mathcal{H}$")
    cv.arrow([(14.2, 76.0), (21.0, 76.0)], head=1.1)
    robot(cv, 25.5, 76.0, EXE, "executor")
    cv.icon_snow(31.4, 80.6, 2.2, color=EXE["stroke"])
    cv.arrow([(25.5, 68.6), (25.5, 59.6)], head=1.1)
    run_doc(cv, 22.7, 52.0, r"$e_0=(\tau_0, y_0)$")
    cv.text(20.5, 44.4, "how the harness behaves,", size=5.9, color=MUTED, style="italic")
    cv.text(20.5, 41.9, "not whether it is correct", size=5.9, color=MUTED, style="italic")
    # 2 propose
    cv.arrow([(28.3, 55.6), (34.5, 55.6), (34.5, 82.0), (42.5, 82.0)], head=1.1, radius=1.2)
    robot(cv, 46.5, 82.0, EDT, None)
    cv.text(51.6, 84.0, "editor reads task, harness,", size=5.9, color=MUTED, ha="left", style="italic")
    cv.text(51.6, 81.4, r"$e_0$, history, library in $\mathcal{R}_t$", size=5.9, color=MUTED, ha="left", style="italic")
    cv.line([(46.5, 78.2), (46.5, 75.4)])
    cv.dot(46.5, 75.4)
    for (yc, c, title, sub) in ((66.5, INV, "Invariant", "planning · tool use · context · delegation"),
                                 (51.0, DOM, "Domain-specific", "knowledge · procedures · constraints")):
        cv.stack(41.0, yc - 5.4, 39.0, 10.8, n=3, r=c, dx=0.7, dy=0.7, fill="white", lw=0.6, radius=1.3)
        cv.text(43.0, yc + 2.4, title, size=6.9, color=c["ink"], weight="bold", ha="left")
        cv.text(43.0, yc - 2.2, sub, size=5.9, color=INK, ha="left")
        diff_lines(cv, 69.0, yc + 3.4, w=8.6)
    cv.arrow([(46.5, 75.4), (46.5, 72.6)], head=1.0)
    cv.arrow([(46.5, 75.4), (38.0, 75.4), (38.0, 51.0), (41.0, 51.0)], head=1.0, radius=1.0)
    cv.chip(52.0, 43.2, r"parallel: $\times k$ per scope", NEU, size=5.9, pad=0.6)
    # candidates + their diffs also go to Compose (over the empty top of the Probe column)
    cv.arrow([(78.0, 72.6), (78.0, 87.0), (139.0, 87.0), (139.0, 85.6)], color=LINE, lw=0.55, head=1.0, radius=1.0)
    cv.text(105.0, 88.6, "candidate harnesses + diffs", size=5.9, color=MUTED, style="italic")
    # 3 probe under matched conditions
    for (yc, c, lab) in ((66.5, INV, r"$e_{\mathrm{inv}}$"), (51.0, DOM, r"$e_{\mathrm{dom}}$")):
        cv.arrow([(80.7, yc), (86.6, yc)], color=c["mark"], head=1.0)
        robot(cv, 90.2, yc, EXE, None, s=5.4)
        cv.arrow([(93.8, yc), (97.0, yc)], head=1.0)
        run_doc(cv, 97.0, yc - 3.6, lab, c=c, w=5.0, h=7.0)
        cv.arrow([(102.4, yc), (106.4, yc)], head=1.0)
    cv.text(105.0, 78.0, "same model, same environment", size=5.9, color=MUTED, style="italic")
    cv.box(106.4, 45.4, 20.2, 25.6, NEU, fill="#FAFAFB", lw=0.5, radius=1.3)
    cv.text(116.5, 68.6, "contrast", size=6.4, color=INK, weight="bold")
    cv.doc(110.0, 61.6, 3.6, 4.6, NEU, lines=2, fold=1.0, lw=0.4)
    cv.text(115.0, 63.9, r"with $e_0$", size=6.0, color=MUTED, ha="left")
    for yy, s in ((57.4, "mitigates"), (52.9, "no change"), (48.4, "regresses")):
        cv.chip(116.5, yy, s, NEU, size=6.0, pad=0.8)
    # 4 compose
    cv.arrow([(126.6, 58.5), (129.4, 58.5)], head=1.0)
    robot(cv, 135.2, 82.0, EDT, None)
    cv.text(135.2, 76.4, "composer", size=6.0, color=EDT["ink"], weight="bold")
    cv.text(140.3, 83.0, "decisions tied to", size=5.9, color=MUTED, ha="left", style="italic")
    cv.text(140.3, 80.4, "observed contrasts", size=5.9, color=MUTED, ha="left", style="italic")
    for k, s in enumerate(("merge supported", "revise conflicts", "adopt one", "keep current")):
        cv.chip(130.6, 70.0 - k * 4.6, s, NEU, size=6.0, ha="left", pad=0.8)
    tip = cv.brace(152.4, 54.6, 72.2, side="right", depth=1.2)
    cv.arrow([(tip[0] + 0.2, 63.0), (157.4, 63.0)], head=1.1)
    harness(cv, 157.4, 58.0, EDT, r"successor $\mathcal{H}'$")
    cv.arrow([(161.8, 55.2), (161.8, 50.6)], head=1.0)
    robot(cv, 161.8, 47.2, EXE, None, s=5.0)
    cv.arrow([(165.2, 47.2), (167.4, 47.2)], head=1.0)
    run_doc(cv, 167.4, 43.6, r"$e'$", w=4.8, h=7.0)
    cv.text(129.6, 44.4, r"adopted $\mathcal{H}^{\star}_t$ (selected", size=5.9, color=MUTED, style="italic", ha="left")
    cv.text(129.6, 41.8, r"if $k>1$); deliverable", size=5.9, color=MUTED, style="italic", ha="left")
    cv.text(129.6, 39.2, r"returned; record $\xi$", size=5.9, color=MUTED, style="italic", ha="left")
    # sequential recursion: H' becomes the next step's H
    cv.arrow([(167.2, 64.0), (173.6, 64.0), (173.6, 95.8), (3.6, 95.8), (3.6, 75.0), (5.0, 75.0)], color=EDT["stroke"],
             lw=0.6, head=1.0, dashed=True, radius=1.2)
    cv.chip(108.0, 95.8, r"sequential recursion: $\mathcal{H}'$ seeds the next step ($k$ steps)", EDT, size=5.9, pad=0.8)
    cv.chip(129.6, 49.6, r"parallel: $\times k$", NEU, size=5.9, pad=0.6, ha="left")


def panel_harnessing(cv):
    cv.group(2, 2, 174, 30.5, RFL, r"(b) Harnessing-level recursion, after each task",
             band=True, size=7.6, radius=2.0, lw=0.7, fill="white")
    # improvement record D_t (right, under Compose)
    cv.arrow([(173.0, 47.2), (174.4, 47.2), (174.4, 27.2), (152.0, 27.2), (152.0, 22.6)], color=RFL["mark"], lw=0.9, head=1.3,
             radius=1.2)
    cv.text(172.8, 36.4, r"$\mathcal{H}^{\star}_t$, $\xi$", size=6.2, color=RFL["ink"], ha="right")
    cv.stack(145.0, 9.4, 13.0, 11.0, n=3, r=NEU, dx=0.8, dy=0.8, fill="white", lw=0.5, radius=1.2)
    cv.text(151.5, 17.6, r"$\mathcal{D}_t$", size=7.4, color=INK)
    cv.text(151.5, 13.4, "record", size=6.0, color=MUTED)
    for k, s_ in enumerate(("references", "candidates", "probes", "decisions", "selected result")):
        cv.text(161.6, 21.4 - k * 2.9, s_, size=5.9, color=MUTED, ha="left")
    # reflect
    cv.arrow([(145.0, 15.0), (134.6, 15.0)], color=RFL["mark"], lw=0.9, head=1.3)
    robot(cv, 130.0, 16.0, RFL, "reflector")
    cv.text(107.5, 19.6, "keeps a lesson only if", size=6.0, color=INK)
    cv.text(107.5, 16.8, "execution contrasts support it", size=6.0, color=INK)
    cv.text(107.5, 11.6, r"$\mathcal{R}_{t+1}=\mathrm{Update}(\mathcal{R}_t,\ \mathcal{H}^{\star}_t,\ \mathcal{D}_t)$",
            size=6.8, color=RFL["ink"])
    cv.arrow([(125.4, 15.0), (92.0, 15.0)], color=RFL["mark"], lw=0.9, head=1.3)
    # library (under Propose)
    cv.cylinder(57.0, 6.0, 35.0, 18.4, RFL)
    for k in range(3):
        xx = 62.0 + k * 9.0
        cv.doc(xx, 9.6, 3.4, 4.6, RFL, lines=2, fold=1.0, lw=0.4)
        cv.doc(xx + 3.6, 9.6, 3.4, 4.6, EDT, lines=2, fold=1.0, lw=0.4)
    cv.text(74.5, 19.8, r"improvement harness $\mathcal{R}$", size=6.4, color=RFL["ink"], weight="bold")
    cv.text(74.5, 16.4, "library: harness + EXPERIENCE.md", size=5.9, color=RFL["ink"])
    cv.icon_cycle(89.0, 9.0, 2.6, color=RFL["mark"])
    # guides proposals of the next task
    cv.arrow([(78.0, 23.6), (78.0, 44.6)], color=RFL["mark"], lw=0.9, head=1.3, dashed=True)
    cv.text(94.0, 25.4, r"guides $q_{t+1}$ (Propose, Probe, Compose),", size=5.9, color=RFL["ink"], ha="left", style="italic")
    cv.text(94.0, 22.8, r"which starts again from $\mathcal{H}_0$", size=5.9, color=RFL["ink"], ha="left", style="italic")
    # fixed vs evolving
    cv.icon_snow(6.4, 20.0, 2.4, color=NEU["stroke"])
    cv.text(8.8, 20.0, "fixed: model weights,", size=6.0, color=INK, ha="left")
    cv.text(8.8, 17.0, "stage instructions,", size=6.0, color=INK, ha="left")
    cv.text(8.8, 14.0, "decision rule", size=6.0, color=INK, ha="left")
    cv.icon_cycle(6.4, 8.6, 2.6, color=RFL["mark"])
    cv.text(8.8, 8.6, "evolves: the library", size=6.0, color=RFL["ink"], ha="left")
    for x, c, lab in ((35.0, EXE, "executor"), (44.0, EDT, "editor /\ncomposer"), (53.0, RFL, "reflector")):
        robot(cv, x, 16.2, c, None, s=4.6)
        cv.text(x, 10.4, lab, size=5.8, color=c["ink"], linespacing=0.95)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="serif", size=7.0)
    panel_task(cv)
    panel_harnessing(cv)
    print("\n".join(cv.save(os.path.join(a.out, "harness2_fig3_pipeline"))))


if __name__ == "__main__":
    main()
