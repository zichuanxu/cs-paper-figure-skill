"""Method figure: evidence-guided memory refinement (fast loop, slow loop, one worked transaction).

Source: gallery/before/method.png, a three-panel schematic (a: frozen runtime with a fast loop and an
epoch loop; b: three competing edits arbitrated into one transaction; c: paired replay of a separate
case and an audit receipt), plus the bundled fixture data/method/data/dense-method-fixture.json.
The fixture is a deterministic toy, not an evaluated system, so the figure marks its worked values
as illustrative in the key strip.

Content kept from the source
- Topology: D_train -> frozen agent (reads memory M) -> trace ledger T -> parallel proposers P1-P3
  (sharing a proposer context) -> arbitration under an edit budget -> candidate record (base ID +
  patch set) -> paired replay on a fixed validation case -> commit (atomic write to M) or reject
  (exact proposal IDs blocked at the arbiter). D_val is used by the gate only; D_test stays sealed.
  Slow loop: epoch replay of the ledger -> reflection (improved / regressed / unchanged) -> proposer
  context for the next epoch. Model weights never change.
- Values: traces T08 and T11, proposals P1-P3 with operation, key, value, priority and evidence,
  budget 2, base record v12, assertions U / D / C on V01, versions v12 -> v13.
- Derived in this script and asserted: the conflict relation (same target key), the kept set
  (P1 + P3), the candidate record, the per-assertion replay outputs, the scores 1/3 and 3/3, the
  guard 3 > 1, and the tie of the P2-only alternative.

Design decisions
- One plate drawn as the loop itself instead of an overview plus two tables: every stage shows its
  real artifact (ledger rows, edit cards, conflict matrix, record fields, assertion outcomes), so the
  worked example and the system diagram are the same picture. Stages are numbered 1-6 clockwise.
- Hero: the memory record. It sits between the reader above (agent) and the gate below; v12 and v13
  are aligned field by field, the two patches enter the fields they change, and the green commit
  arrow from the gate's decision diamond is the only way into v13.
- Colour = role: slate frozen runtime, green memory state / accepted, purple proposed edits, amber
  validation gate, coral conflict / rejection, teal epoch-rate proposer context.
- The two timescales are named on the state each loop writes (tab of M, tab of C).
- Monospace = data from the fixture; serif = the figure's own words.

    python render_method.py --out figures/method [--fixture path.json]
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))

from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

from paperkit import INK, LINE, MUTED, ROLE, Canvas, mix  # noqa: E402

FIXTURE = os.path.join(HERE, "data", "method", "data", "dense-method-fixture.json")
STEM = "method"
W, H = 178.0, 139.0

GREEN, PURPLE, AMBER, CORAL, TEAL, SLATE = (ROLE[k] for k in ("memory", "purple", "amber", "coral", "teal", "frozen"))
CARD = mix("#FFFFFF", PURPLE["soft"], 0.62)   # edit cards: a block tone on the section tint


# ------------------------------------------------------------------ fixture logic ---
def arbitrate(proposals, budget, rejected=()):
    """Conflict = same target key. Greedy by priority within the budget; exact rejected IDs are excluded."""
    conflict = {(a["id"], b["id"]) for a in proposals for b in proposals
                if a["id"] != b["id"] and a["key"] == b["key"]}
    kept = []
    for p in sorted(proposals, key=lambda q: -q["priority"]):
        if p["id"] in rejected or len(kept) >= budget:
            continue
        if not any((p["id"], k["id"]) in conflict for k in kept):
            kept.append(p)
    return conflict, [p for p in proposals if p in kept]


def apply(record, edits):
    out = dict(record)
    for e in edits:
        out[e["key"]] = e["value"]
    return out


def execute(record, case):
    """The fixture's toy executor (execution_semantics)."""
    return {"value": case["source_value"] if record.get("units") == "value + unit" else case["baseline_answer"],
            "source_date": case["source_date"] if record.get("freshness") == "source date" else None,
            "citation": "URL" if record.get("citation") == "URL" else None}


def replay(record, case, assertions):
    out = execute(record, case)
    return [(out[a["key"]], out[a["key"]] == a["expected"]) for a in assertions]


# ---------------------------------------------------------------- local helpers ---
def mono(cv, x, y, s, size=5.9, color=INK, weight="normal", ha="left", **kw):
    return cv.text(x, y, s, size=size, color=color, weight=weight, ha=ha, family="monospace", **kw)


def frame(cv, x, y, w, h, r, title, anchor="left", badge=None, size=7.4, fill=None, solid=False):
    """Tinted dashed module frame with its title on a pill that sits on the top border at one end,
    so wires can cross the border elsewhere."""
    c = ROLE[r]
    cv.section(x, y, w, h, r, None, fill=fill)
    extra = 3.5 if badge else 0.0
    tw, th = cv.text_width(title, size, "bold") + 3.8 + extra, size * 0.56
    x0 = x + 3.0 if anchor == "left" else x + w - 3.0 - tw
    cv.ax.add_patch(FancyBboxPatch((x0, y + h - th / 2), tw, th, boxstyle=f"round,pad=0,rounding_size={th / 2}",
                                   fc=c["mark"] if solid else c["soft"], ec=c["mark"] if solid else c["stroke"],
                                   lw=0.6, zorder=1.3))
    if badge:
        cv.badge(x0 + 2.4, y + h, badge, r, d=3.1, z=1.5)
    cv.text(x0 + 1.9 + extra, y + h - 0.05, title, size=size, weight="bold", color="white" if solid else c["ink"],
            ha="left", z=1.4)


def dashed_arrow(cv, pts, color, lw=0.8, head=1.4):
    """Dashed wire with a solid head (a dashed FancyArrowPatch also dashes its head, which prints ragged)."""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    t = min(0.9, (head * 0.95 + 0.5) / math.hypot(x1 - x0, y1 - y0))
    pre = (x1 - (x1 - x0) * t, y1 - (y1 - y0) * t)
    if len(pts) > 2 or t < 0.9:
        cv.line(list(pts[:-1]) + [pre], color=color, lw=lw, dashed=True, radius=1.2, z=8)
    cv.arrow([pre, pts[-1]], color=color, lw=lw, head=head)


def key_strip(cv, x, y, items, size=6.0, h=5.6, gap=3.6, pad=2.0):
    """Glyph key in a dashed strip sized to its content. items = [(glyph width, draw(x, y), label)]."""
    xx = x + pad
    for gw, fn, lab in items:
        fn(xx, y + h / 2)
        cv.text(xx + gw + 1.1, y + h / 2, lab, size=size, ha="left")
        xx += gw + 1.1 + cv.text_width(lab, size) + gap
    cv.ax.add_patch(FancyBboxPatch((x, y), xx - gap + pad - x, h, boxstyle="round,pad=0,rounding_size=1.6", fc="none",
                                   ec=ROLE["neutral"]["stroke"], lw=0.6, ls=(0, (3, 2)), zorder=3))
    return h


def mark(cv, x, y, ok, s=2.7):
    c = GREEN if ok else CORAL
    cv.ax.add_patch(FancyBboxPatch((x - s / 2, y - s / 2), s, s, boxstyle="round,pad=0,rounding_size=0.5",
                                   fc=c["soft"], ec=c["stroke"], lw=0.4, zorder=7))
    (cv.icon_check if ok else cv.icon_cross)(x, y, s * 0.55, color=c["ink"], lw=0.85, z=8)


def record(cv, x, y, w, h, ver, gloss, rows, row_y, hero=False):
    """Memory record: version chip + one aligned row per field. rows = [(key, value, state)]."""
    cv.box(x, y, w, h, "memory", fill="white", lw=0.95 if hero else 0.6, radius=1.2, shadow=hero)
    hy = y + h - 2.7
    cv.chip(x + 1.5, hy, ver, "memory", size=6.2, solid=True, ha="left", z=7)
    cv.text(x + w - 1.6, hy, gloss, size=5.8, style="italic", color=MUTED, ha="right")
    cv.ax.plot([x + 0.9, x + w - 0.9], [y + h - 5.3] * 2, color=GREEN["soft"], lw=0.5, zorder=6)
    for key, val, state in rows:
        cy = row_y[key]
        if state == "edit":
            cv.ax.add_patch(Rectangle((x + 0.7, cy - 2.05), w - 1.4, 4.1, fc=PURPLE["soft"], ec="none", zorder=5.5))
        kc = MUTED if state == "absent" else INK
        mono(cv, x + 2.0, cy, key, color=kc, weight="bold" if state != "absent" else "normal")
        if state == "absent":
            cv.text(x + 15.2, cy, "absent", size=5.9, style="italic", color=MUTED, ha="left")
        else:
            mono(cv, x + 15.2, cy, val, color=PURPLE["ink"] if state == "edit" else INK,
                 weight="bold" if state == "edit" else "normal")


def draw(out, fixture=FIXTURE):
    fx = json.load(open(fixture))
    props, budget, asserts = fx["proposals"], fx["edit_budget"], fx["assertions"]
    t08, v01, t11 = fx["worked_trace"], fx["validation_trace"], fx["other_evidence"][0]
    v_old, v_new = fx["base_version"], fx["next_version"]

    # ---- derive everything that is printed -------------------------------------------------
    conflict, kept = arbitrate(props, budget, fx["rejection_history"])
    kept_ids = [p["id"] for p in kept]
    assert kept_ids == ["P1", "P3"], kept_ids
    base = dict(fx["base_record"])
    cand = apply(base, kept)
    r_old, r_new = replay(base, v01, asserts), replay(cand, v01, asserts)
    n_old, n_new, n_all = sum(ok for _, ok in r_old), sum(ok for _, ok in r_new), len(asserts)
    assert (n_old, n_new) == (1, 3) and n_new > n_old           # the gate: strict improvement
    alt = [p for p in props if p["id"] not in kept_ids]          # the dropped alternative, replayed alone
    n_alt = sum(ok for _, ok in replay(apply(base, alt), v01, asserts))
    assert len(alt) == 1 and n_alt == n_old                      # a tie is not a strict improvement
    fields = list(dict.fromkeys(list(cand) + list(base)))        # units, citation, freshness
    fields = [k for k in ("units", "freshness", "citation") if k in fields]
    max_pri = max(p["priority"] for p in props)

    cv = Canvas(W, H)

    # ======================================================== 1-2  frozen runtime (top left)
    frame(cv, 2, 105, 89, 30, "frozen", "Frozen runtime", anchor="right")
    for i in (2, 1, 0):
        cv.doc(5.5 + i * 0.9, 115.2 + i * 0.9, 8, 10, "neutral", lines=4, fold=2.2, z=6 - i * 0.1)
    cv.text(10.4, 112.3, r"$D_{\mathrm{train}}$", size=6.8, weight="bold", color=ROLE["neutral"]["ink"])
    cv.text(10.6, 109.0, "source-tagged", size=5.8, style="italic", color=MUTED)
    cv.box(21.5, 113.5, 23, 14, "frozen", "Agent execution", "frozen weights", icon="snow", size=6.3, tsize=6.8,
           fill=SLATE["soft"], lw=0.7)
    cv.badge(21.9, 127.3, 1, "frozen")
    cv.arrow([(15.6, 120.5), (21.5, 120.5)])
    cv.arrow([(44.5, 120.5), (48.5, 120.5)])

    # ledger: real trace rows
    lx, ly, lw_, lh = 48.5, 107.3, 40.5, 24.4
    cv.box(lx, ly, lw_, lh, "frozen", fill="white", radius=1.0, lw=0.7)
    cv.ax.add_patch(Rectangle((lx + 0.35, ly + lh - 4.4), lw_ - 0.7, 4.05, fc=SLATE["soft"], ec="none", zorder=5.5))
    cv.badge(lx + 0.4, ly + lh - 0.2, 2, "frozen")
    cv.text(lx + 3.0, ly + lh - 2.35, r"Trace ledger $\mathbf{T}$", size=6.8, weight="bold", color=SLATE["ink"], ha="left")
    hy = ly + lh - 6.5
    for xx, s in ((lx + 1.6, "case"), (lx + 9.6, "source"), (lx + lw_ - 1.6, "answer")):
        cv.text(xx, hy, s, size=5.8, style="italic", color=MUTED, ha="right" if s == "answer" else "left")
    y1 = hy - 3.7
    cv.chip(lx + 1.4, y1, t08["id"], "frozen", size=5.9, solid=True, ha="left")
    mono(cv, lx + 9.6, y1, f"{t08['source_value']} · {t08['source_date']}")
    mono(cv, lx + lw_ - 1.8, y1, t08["baseline_answer"], ha="right", weight="bold", color=CORAL["ink"])
    cv.icon_cross(lx + 10.6, y1 - 3.5, 1.5, color=CORAL["mark"], lw=0.8)
    cv.text(lx + 12.2, y1 - 3.5, t08["omission"], size=5.8, style="italic", color=CORAL["ink"], ha="left")
    ys = y1 - 5.6
    cv.ax.plot([lx + 1.2, lx + lw_ - 1.2], [ys, ys], color=SLATE["soft"], lw=0.5, zorder=6)
    # T11: its source is a table column, drawn as one
    col, cell = t11["source_form"].split(";")
    col, cell = col.split(":")[1].strip(), cell.split(":")[1].strip()
    cv.chip(lx + 1.4, ys - 2.4, t11["id"], "frozen", size=5.9, solid=True, ha="left")
    tw = 16.4
    for k, (s, fc) in enumerate(((col, SLATE["soft"]), (cell, "white"))):
        yy = ys - 0.9 - (k + 1) * 3.1
        cv.ax.add_patch(Rectangle((lx + 9.6, yy), tw, 3.1, fc=fc, ec=SLATE["stroke"], lw=0.4, zorder=6))
        mono(cv, lx + 9.6 + tw / 2, yy + 1.5, s, ha="center", size=5.8)
    cv.text(lx + lw_ - 1.6, ys - 2.4, "table", size=5.8, style="italic", color=MUTED, ha="right")
    cv.text(lx + lw_ - 1.6, ys - 5.3, "column", size=5.8, style="italic", color=MUTED, ha="right")

    # ======================================================== slow loop: proposer context (top right)
    frame(cv, 97, 120, 79, 15, "teal", r"Proposer context $\mathbf{C}$ · slow loop, per epoch")
    cv.box(99.5, 122, 26, 9.2, "teal", "Epoch replay", r"same cases, old vs. new $\mathbf{M}$", size=6.2, tsize=6.8,
           fill=TEAL["soft"])
    cv.box(129.5, 122, 31.5, 9.2, "teal", fill=TEAL["soft"])
    cv.text(145.25, 128.6, "Reflect", size=6.8, weight="bold", color=TEAL["ink"])
    cv.rich(145.25, 124.6, [("improved", GREEN["ink"]), (" · ", MUTED), ("regressed", CORAL["ink"]), (" · ", MUTED),
                            ("unchanged", ROLE["neutral"]["ink"])], size=5.9, ha="center")
    cv.doc(165.2, 121.7, 8, 10, "teal", lines=0, fold=2.4, lw=0.8)
    cv.text(168.9, 126.2, r"$\mathbf{C}$", size=8.0, color=TEAL["ink"])
    tm = TEAL["mark"]
    cv.arrow([(lx + lw_, 126.6), (99.5, 126.6)], color=tm, lw=0.9)
    cv.arrow([(125.5, 126.6), (129.5, 126.6)], color=tm, lw=0.9)
    cv.arrow([(161, 126.6), (165.2, 126.6)], color=tm, lw=0.9)
    cv.arrow([(169.2, 121.7), (169.2, 114)], color=tm, lw=0.9)
    cv.text(167.8, 117.0, "shared by P1–P3", size=5.8, style="italic", color=TEAL["ink"], ha="right")

    # ======================================================== 3  parallel proposals
    frame(cv, 97, 71, 79, 43, "purple", "Parallel proposals", badge=3)
    cv.arrow([(lx + lw_, 110.2), (97, 110.2)])
    px, pw, ph = 99.5, 74.0, 9.6
    cv.text(px + 1.6, 108.5, "atomic edit", size=5.8, style="italic", color=MUTED, ha="left")
    cv.text(px + 58.4, 108.5, "priority", size=5.8, style="italic", color=MUTED)
    cv.text(px + 69.2, 108.5, "evidence", size=5.8, style="italic", color=MUTED)
    for i, p in enumerate(props):
        y = 96.4 - i * (ph + 2.0)
        cy = y + ph / 2
        cv.box(px, y, pw, ph, "purple", fill=CARD, radius=1.3)
        x0, w0 = cv.chip(px + 1.6, cy, p["id"], "purple", size=6.4, solid=True, ha="left", h=4.0, pad=1.1)
        x1, w1 = cv.chip(x0 + w0 + 1.3, cy, p["operation"], dict(PURPLE, soft="#FFFFFF"), size=5.8, ha="left")
        mono(cv, px + 20.2, cy, p["key"], weight="bold")
        cv.arrow([(px + 33.0, cy), (px + 35.8, cy)], lw=0.6, head=1.0, color=PURPLE["stroke"])
        mono(cv, px + 36.8, cy, p["value"])
        for k in range(max_pri):                               # priority pips
            cv.ax.add_patch(Rectangle((px + 54.0 + k * 1.75, cy - 0.75), 1.35, 1.5, zorder=7, lw=0.35,
                                      fc=PURPLE["mark"] if k < p["priority"] else "white", ec=PURPLE["stroke"]))
        cv.text(px + 62.4, cy, str(p["priority"]), size=6.4, weight="bold", color=PURPLE["ink"])
        cv.chip(px + 69.2, cy, p["evidence"], "frozen", size=5.9, solid=True)

    # ======================================================== 4  arbitration
    frame(cv, 131, 25, 45, 40, "purple", "Arbitrate", badge=4)
    cv.arrow([(165, 71), (165, 65)])
    mx, mtop, mc = 142.0, 56.2, 5.4
    ids = [p["id"] for p in props]
    for j, pid in enumerate(ids):
        cv.text(mx + (j + 0.5) * mc, mtop + 1.9, pid, size=6.2, weight="bold", color=PURPLE["ink"])
        cy = mtop - (j + 0.5) * mc
        cv.text(mx - 1.3, cy, pid, size=6.2, weight="bold", color=PURPLE["ink"], ha="right")
        for k, qid in enumerate(ids):
            hit = (pid, qid) in conflict
            fc = ROLE["neutral"]["soft"] if pid == qid else CORAL["soft"] if hit else "white"
            cv.ax.add_patch(Rectangle((mx + k * mc, mtop - (j + 1) * mc), mc, mc, fc=fc, ec=PURPLE["stroke"], lw=0.45,
                                      zorder=6))
            if hit:
                cv.icon_cross(mx + (k + 0.5) * mc, cy, 2.3, color=CORAL["mark"], lw=1.0)
        ok = pid in kept_ids
        (cv.icon_check if ok else cv.icon_cross)(161.2, cy, 1.9, color=(GREEN if ok else CORAL)["mark"], lw=1.0)
        cv.text(163.2, cy, "kept" if ok else "dropped", size=6.2, ha="left", color=(GREEN if ok else CORAL)["ink"],
                weight="bold" if ok else "normal")
    cv.icon_cross(134.6, 35.4, 1.7, color=CORAL["mark"], lw=0.9)
    cv.text(136.4, 35.4, "same target key", size=5.9, style="italic", color=CORAL["ink"], ha="left")
    ex = cv.rich(133.6, 30.3, [(f"edit budget {budget}  →", INK)], size=6.2)
    for pid in kept_ids:
        x0, w0 = cv.chip(ex + 1.4, 30.3, pid, "purple", size=6.0, solid=True, ha="left")
        ex = x0 + w0

    # ======================================================== candidate record
    cx0, cy0, cw, ch = 100.0, 48.5, 24.0, 19.0
    cv.doc(cx0, cy0, cw, ch, "purple", lines=0, fold=3.0, lw=0.7)
    cv.text(cx0 + 1.8, cy0 + ch - 3.2, "Candidate", size=6.8, weight="bold", color=PURPLE["ink"], ha="left")
    mono(cv, cx0 + 1.8, cy0 + 9.5, "base")
    cv.chip(cx0 + 9.6, cy0 + 9.5, v_old, "memory", size=6.0, solid=True, ha="left")
    mono(cv, cx0 + 1.8, cy0 + 4.2, "patch")
    ex = cx0 + 9.6
    for pid in kept_ids:
        x0, w0 = cv.chip(ex, cy0 + 4.2, pid, "purple", size=6.0, solid=True, ha="left")
        ex = x0 + w0 + 1.0
    gy = 58.0                                                  # header row of the gate
    cv.arrow([(131, gy), (cx0 + cw, gy)])
    cv.arrow([(cx0, gy), (88, gy)])

    # ======================================================== 5  paired replay gate
    frame(cv, 2, 25, 89, 40, "amber", "Paired replay", anchor="right", badge=5, fill="#FFF1DA")
    cv.box(5, gy - 3.5, 28, 7, "amber", fill=AMBER["soft"], radius=1.2)
    cv.box(60, gy - 3.5, 28, 7, "amber", fill=AMBER["soft"], radius=1.2)
    cv.chip(6.5, gy, v_old, "memory", size=6.2, solid=True, ha="left")
    cv.rich(31.4, gy, [(f"{n_old}/{n_all}", INK, "bold"), (" pass", MUTED)], size=6.8, ha="right")
    cv.rich(61.6, gy, [(f"{n_new}/{n_all}", GREEN["mark"], "bold"), (" pass", MUTED)], size=6.8, ha="left")
    cv.chip(86.5, gy, v_new, "memory", size=6.2, solid=True, ha="right")
    cv.diamond(39.0, gy - 4.2, 15.0, 8.4, "amber")
    cv.text(46.5, gy, f"{n_new} > {n_old}", size=7.0, weight="bold", color=AMBER["ink"])
    cv.arrow([(33, gy), (39.0, gy)], lw=0.6, head=1.1)
    cv.arrow([(60, gy), (54.0, gy)], lw=0.6, head=1.1)
    for i, (a, (vo, oko), (vn, okn)) in enumerate(zip(asserts, r_old, r_new)):
        cy = 49.4 - i * 5.1
        cv.ax.plot([5, 88], [cy - 2.55] * 2, color=AMBER["stroke"], lw=0.45, alpha=0.55, zorder=4)
        mono(cv, 27.6, cy, vo or "absent", ha="right", color=INK if oko else CORAL["ink"])
        mark(cv, 31.0, cy, oko)
        cv.text(46.5, cy, a["label"], size=6.2, color=AMBER["ink"])
        mark(cv, 62.0, cy, okn)
        mono(cv, 65.4, cy, vn or "absent", color=INK if (okn and vn == vo) else GREEN["ink"],
             weight="normal" if vn == vo else "bold")
    cv.box(5, 28.3, 38, 6.2, "amber", fill=AMBER["soft"], radius=1.0)
    cv.chip(6.4, 31.4, v01["id"], "amber", size=6.0, solid=True, ha="left")
    mono(cv, 14.2, 31.4, f"{v01['source_value']} · {v01['source_date']}")
    cv.box(51, 28.3, 37, 6.2, "coral", radius=1.0, dashed=True)
    x0, w0 = cv.chip(52.4, 31.4, alt[0]["id"], "purple", size=6.0, solid=True, ha="left")
    cv.text(x0 + w0 + 1.0, 31.4, f"alone: {n_alt}/{n_all} vs {n_old}/{n_all}, a tie", size=6.0, color=CORAL["ink"],
            ha="left")

    # ======================================================== 6  memory (hero)
    frame(cv, 2, 71, 89, 28, "memory", r"Memory $\mathbf{M}$ · fast loop, per rollout batch", anchor="right",
          fill="#E3F1E7", solid=True)
    row_y = {"units": 86.5, "freshness": 81.9, "citation": 77.3}
    rows_old = [(k, base.get(k), "same" if k in base else "absent") for k in fields]
    rows_new = [(k, cand[k], "same" if cand.get(k) == base.get(k) else "edit") for k in fields]
    record(cv, 4.5, 73.4, 34, 21.2, v_old, "base", rows_old, row_y)
    record(cv, 54.5, 73.4, 34, 21.2, v_new, "after commit", rows_new, row_y, hero=True)
    cv.box(42.0, 79.2, 9.0, 10.0, "purple", fill=PURPLE["soft"], radius=1.2, lw=0.6, container=True)
    for p in kept:
        cv.chip(46.5, row_y[p["key"]], p["id"], "purple", size=6.0, solid=True)
        cv.arrow([(51.0, row_y[p["key"]]), (54.5, row_y[p["key"]])], color=PURPLE["mark"], lw=0.8, head=1.1)
    cv.arrow([(38.5, 84.2), (42.0, 84.2)], lw=0.7, head=1.1)
    cv.text(46.5, 92.0, "atomic write", size=5.8, style="italic", color=PURPLE["ink"])
    gm = GREEN["mark"]
    cv.arrow([(46.5, gy + 4.2), (46.5, 79.2)], color=gm, lw=1.1, head=1.6)
    cv.badge(49.6, 68.0, 6, "memory")
    cv.text(51.8, 68.0, "commit", size=6.8, weight="bold", color=GREEN["ink"], ha="left")
    cv.arrow([(21.5, 73.4), (21.5, gy + 3.5)])
    cv.text(22.8, 68.0, "baseline", size=5.9, style="italic", color=MUTED, ha="left")
    cv.arrow([(36.0, 94.6), (36.0, 113.5)])
    cv.text(34.9, 102.0, "read", size=5.9, style="italic", color=MUTED, ha="right")

    # ======================================================== rail: splits, rejection buffer
    cv.doc(5.5, 12.0, 6, 7.5, "amber", lines=3, fold=1.8)
    cv.arrow([(8.5, 19.5), (8.5, 28.3)], color=AMBER["mark"], lw=0.8, head=1.2)
    cv.text(13.2, 17.6, r"$D_{\mathrm{val}}$", size=6.8, weight="bold", color=AMBER["ink"], ha="left")
    cv.text(13.2, 14.2, "fixed cases, gate only", size=5.8, style="italic", color=MUTED, ha="left")
    cv.doc(38.0, 12.0, 6, 7.5, "neutral", lines=3, fold=1.8)
    ex = cv.rich(45.7, 17.6, [(r"$D_{\mathrm{test}}$", ROLE["neutral"]["ink"], "bold")], size=6.8)
    cv.icon_lock(ex + 2.2, 17.7, 2.4, color=ROLE["neutral"]["mark"])
    cv.text(45.7, 14.2, "sealed, final use only", size=5.8, style="italic", color=MUTED, ha="left")
    cm = CORAL["mark"]
    cv.box(99, 11.4, 28, 9.2, "coral", "Rejected IDs", "exact retries blocked", size=6.2, tsize=6.8)
    dashed_arrow(cv, [(72, 28.3), (72, 16), (99, 16)], cm)
    cv.text(85.5, 17.7, "reject", size=5.9, style="italic", color=CORAL["ink"])
    dashed_arrow(cv, [(127, 16), (153.5, 16), (153.5, 25)], cm)
    cv.text(140.2, 17.7, "excluded", size=5.9, style="italic", color=CORAL["ink"])

    # ======================================================== key strip
    kh = key_strip(cv, 2, 1.6, [
        (3.0, lambda x, y: cv.icon_snow(x + 1.5, y, 2.7, color=SLATE["stroke"]), "weights never change"),
        (3.0, lambda x, y: cv.icon_lock(x + 1.5, y, 2.6, color=ROLE["neutral"]["mark"]), "sealed split"),
        (7.6, lambda x, y: (cv.badge(x + 1.5, y, 1, "neutral", d=2.9), cv.badge(x + 6.1, y, 6, "neutral", d=2.9),
                            cv.ax.plot([x + 3.3, x + 4.3], [y, y], color=LINE, lw=0.6)), "fast-loop order"),
        (4.4, lambda x, y: cv.arrow([(x, y), (x + 4.4, y)], color=gm, lw=1.0, head=1.3), "commit"),
        (4.4, lambda x, y: dashed_arrow(cv, [(x, y), (x + 4.4, y)], cm, head=1.2), "reject"),
        (4.4, lambda x, y: cv.arrow([(x, y), (x + 4.4, y)], color=tm, lw=0.9, head=1.3), "slow-loop update")])
    cv.text(176, 1.6 + kh / 2 + 1.5, "Worked values: a deterministic toy fixture,", size=5.9, style="italic",
            color=MUTED, ha="right")
    cv.text(176, 1.6 + kh / 2 - 1.5, "illustrative only, not measured results", size=5.9, style="italic",
            color=MUTED, ha="right")

    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="figures/method")
    ap.add_argument("--fixture", default=FIXTURE)
    a = ap.parse_args()
    print("\n".join(draw(a.out, a.fixture)))
