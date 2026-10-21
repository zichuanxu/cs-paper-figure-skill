"""Restyled 'evidence-guided memory refinement' method figure (cs-paper-figure example).

All values come from the old example's fixture (dense-method-fixture.json); the
transaction (selection under conflicts + budget, deterministic toy executor,
assertion replay, P2 counterfactual) is recomputed here and asserted.

    python render_method.py --fixture <dense-method-fixture.json> --out <dir>
"""
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, ROLE, INK, MUTED, LINE  # noqa: E402

MEMR, PROP, VAL = ROLE["blue"], ROLE["purple"], ROLE["amber"]
ACC, REJ, NEU, FZ = ROLE["memory"], ROLE["coral"], ROLE["neutral"], ROLE["frozen"]
DOCN = dict(ROLE["neutral"], stroke="#69717D")  # trace/data documents: darker outline
W, H = 178, 134
DEFAULT_FIXTURE = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "method"), "data", "dense-method-fixture.json")


# ------------------------------------------------------------------ data ---
def evaluate(f):
    """Same deterministic semantics as the original example (render_dense_method.py)."""
    base, props = dict(f["base_record"]), f["proposals"]
    assert f["validation_trace"]["id"] not in {p["evidence"] for p in props}, "V01 must not propose edits"
    rejected = {r["proposal_id"] for r in f.get("rejection_history", [])}
    chosen, claimed = [], set()
    for p in sorted(props, key=lambda p: -p["priority"]):
        assert (p["operation"] == "ADD") != (p["key"] in base), p["id"]
        if p["id"] not in rejected and p["key"] not in claimed and len(chosen) < f["edit_budget"]:
            chosen.append(p)
            claimed.add(p["key"])
    cand = {**base, **{p["key"]: p["value"] for p in chosen}}
    vt = f["validation_trace"]

    def execute(m):
        return {"value": vt["source_value"] if m.get("units") == "value + unit" else vt["baseline_answer"],
                "source_date": vt["source_date"] if m.get("freshness") == "source date" else None,
                "citation": "URL" if m.get("citation") == "URL" else None}

    def checks(o):
        return [o.get(a["key"]) == a["expected"] for a in f["assertions"]]

    alt = {**base, props[1]["key"]: props[1]["value"]}
    outs = {"v12": execute(base), "alt": execute(alt), "v13": execute(cand)}
    return dict(selected=[p["id"] for p in chosen], base=base, cand=cand, outs=outs,
                checks={k: checks(o) for k, o in outs.items()},
                conflicts=[[i != j and a["key"] == b["key"] for j, b in enumerate(props)]
                           for i, a in enumerate(props)],
                hash=hashlib.sha256(json.dumps(cand, sort_keys=True).encode()).hexdigest()[:8])


# ------------------------------------------------------------ local glyphs ---
def card(cv, x, y, w, h, r, title):
    cv.group(x, y, w, h, r, title, band=True, size=7.6, radius=2.0, lw=0.7, fill="white")


def doc_stack(cv, x, y, w, h, r, n=3, d=0.9, lines=3):
    for k in range(n - 1, -1, -1):
        cv.doc(x + k * d, y + k * d, w, h, r, lines=lines if k == 0 else 0, z=6 - k * 0.05)


def record(cv, x, y, w, ver, rows, hero=False):
    """Memory record glyph: version header strip + key/value field rows.
    rows = [(key, value, tag)] where tag in {None, 'REP', 'ADD', 'absent'}."""
    rh, hh = 2.9, 3.4
    h = hh + rh * len(rows) + 0.6
    cv.box(x, y, w, h, "blue", fill="white", lw=0.9 if hero else 0.6, radius=1.0, shadow=hero, z=6)
    cv.ax.add_patch(__import__("matplotlib.patches", fromlist=["Rectangle"]).Rectangle(
        (x + 0.3, y + h - hh), w - 0.6, hh - 0.3, fc=MEMR["soft"], ec="none", zorder=6.1))
    cv.text(x + 1.4, y + h - hh / 2 - 0.1, ver, size=7.0, weight="bold", color=MEMR["ink"], ha="left", z=7)
    for i, (k, v, tag) in enumerate(rows):
        yy = y + h - hh - rh * (i + 0.5) - 0.2
        cv.text(x + 1.4, yy, k, size=6.2, color=MUTED, ha="left", z=7)
        col = MUTED if tag == "absent" else (MEMR["ink"] if tag else INK)
        cv.text(x + 13.2, yy, v, size=6.4, color=col, ha="left", z=7,
                weight="bold" if tag in ("REP", "ADD") else "normal")
        if tag in ("REP", "ADD"):
            cv.chip(x + w - 1.0, yy, tag, PROP, size=6.2, pad=0.5, h=2.5, ha="right", z=8)
    return h


def check(cv, x, y, ok, s=1.1):
    c = ACC["mark"] if ok else REJ["mark"]
    if ok:
        cv.ax.plot([x - s * 0.5, x - s * 0.1, x + s * 0.6], [y, y - s * 0.45, y + s * 0.5], color=c,
                   lw=0.9, zorder=12, solid_capstyle="round", solid_joinstyle="round")
    else:
        for sg in (1, -1):
            cv.ax.plot([x - s * 0.45, x + s * 0.45], [y - sg * s * 0.45, y + sg * s * 0.45], color=c,
                       lw=0.9, zorder=12, solid_capstyle="round")


# ------------------------------------------------------------------ panels ---
def panel_a(cv, f, r):
    card(cv, 2, 58, 174, 74, "neutral", "(a) Refinement loop")
    # versioned memory band (state as a horizontal pillar: read at left, write at right)
    cv.group(4, 108.5, 170, 18, "blue", None, radius=1.6, lw=0.5)
    cv.text(6.0, 124.6, "Versioned memory", size=7.0, weight="bold", color=MEMR["ink"], ha="left")
    cv.icon_cycle(171.0, 124.3, 2.6, color=MEMR["mark"])
    keys = ["units", "freshness", "citation"]
    v12 = [(k, r["base"].get(k, "—"), None if k in r["base"] else "absent") for k in keys]
    sel = {p["key"]: p["operation"][:3] for p in f["proposals"] if p["id"] in r["selected"]}
    v13 = [(k, r["cand"][k], sel.get(k)) for k in keys]
    record(cv, 9, 110, 34, f["base_version"], v12)
    record(cv, 115, 110, 38, f["next_version"], v13, hero=True)
    cv.block_arrow(46, 116.4, 112.5, 116.4, width=4.2, color=MEMR["soft"])
    cv.text(79, 120.6, "one atomic write", size=6.2, color=MEMR["ink"], style="italic")
    x0 = 70.0
    for pid in r["selected"]:
        x0 += cv.chip(x0, 116.4, pid, PROP, size=6.2, pad=0.7, h=2.6, solid=True, ha="left")[1] + 1.2

    yc = 95.0
    # training data -> frozen agent -> trace ledger
    doc_stack(cv, 5.5, 89, 9, 11.5, DOCN)
    cv.text(11.4, 86.2, r"$\mathcal{D}_{\mathrm{train}}$", size=6.8)
    cv.text(11.4, 83.6, "source-tagged", size=6.2, color=MUTED, style="italic")
    cv.arrow([(16.8, yc), (21, yc)])
    cv.box(21, 88.5, 18, 13, "frozen", lw=0.7, icon="snow")
    cv.icon_robot(30, 97.4, 5.0, color=FZ["ink"], fill=FZ["soft"])
    cv.text(30, 91.0, "agent", size=7.0, color=FZ["ink"], weight="bold")
    cv.arrow([(26, 110), (26, 101.5)], color=MEMR["mark"], lw=0.9)
    cv.text(27.0, 105.6, "read", size=6.2, color=MEMR["ink"], style="italic", ha="left")
    cv.arrow([(39, yc), (44.5, yc)])
    doc_stack(cv, 44.5, 89, 9, 11.5, DOCN)
    cv.text(50.4, 86.2, r"ledger $T$", size=7.0)
    cv.text(50.4, 83.6, "traces", size=6.2, color=MUTED, style="italic")
    # fan-out to parallel proposals
    bus = 59.5
    cv.line([(56.3, yc), (bus, yc)])
    cv.dot(bus, yc)
    ys = [103.5, 95.0, 86.5]
    cv.line([(bus, ys[-1]), (bus, ys[0])], radius=0)
    for p, y in zip(f["proposals"], ys):
        cv.arrow([(bus, y), (63, y)], head=1.1)
        cv.box(63, y - 3.25, 23, 6.5, "purple", lw=0.6, radius=1.0)
        cv.chip(64.0, y, p["id"], PROP, size=6.2, pad=0.6, h=2.8, solid=True, ha="left")
        cv.text(70.6, y, p["key"], size=6.8, color=PROP["ink"], ha="left")
        cv.text(85.0, y, p["evidence"], size=6.2, color=MUTED, ha="right")
    # merge bar = arbiter under conflicts + budget
    cv.box(90, 83, 4.2, 24, "purple", fill=PROP["mark"], stroke=PROP["ink"], radius=1.0, lw=0.5)
    cv.text(92.1, 95, f"arbiter · budget {f['edit_budget']}", size=6.2, color="white", rotation=90, z=12)
    for y in ys:
        cv.arrow([(86, y), (90, y)], head=1.0)
    cv.arrow([(94.2, yc), (99.5, yc)])
    cv.doc(99.5, 89, 10, 12, "blue", lines=3)
    cv.text(104.5, 86.2, "candidate", size=7.0, color=MEMR["ink"])
    cv.text(104.5, 83.6, "base + patch", size=6.2, color=MUTED, style="italic")
    cv.arrow([(109.5, yc), (116, yc)])
    # hero: validation gate
    gx, gw, gh = 116, 26, 19
    cv.ax.add_patch(__import__("matplotlib.patches", fromlist=["Polygon"]).Polygon(
        [(gx + 0.4, yc - 0.4), (gx + gw / 2 + 0.4, yc + gh / 2 - 0.4), (gx + gw + 0.4, yc - 0.4),
         (gx + gw / 2 + 0.4, yc - gh / 2 - 0.4)], fc="#1A2230", alpha=0.08, ec="none", zorder=5.8))
    cv.diamond(gx, yc - gh / 2, gw, gh, "amber", lw=1.1)
    gc = gx + gw / 2
    cv.text(gc, yc + 1.5, "paired replay", size=7.0, weight="bold", color=VAL["ink"])
    cv.text(gc, yc - 1.6, "strict gain?", size=6.4, color=VAL["ink"], style="italic")
    # validation and test splits (fixed during selection)
    cv.doc(148.5, 89, 10, 12, "amber", lines=3)
    cv.icon_lock(153.6, 99.4, 2.2, color=VAL["stroke"])
    cv.text(153.5, 86.2, r"$\mathcal{D}_{\mathrm{val}}$", size=6.8, color=VAL["ink"])
    cv.text(153.5, 83.6, "fixed cases", size=6.2, color=MUTED, style="italic")
    cv.arrow([(148.5, yc), (gx + gw, yc)], color=VAL["mark"], lw=0.8)
    cv.doc(162.5, 89, 10, 12, "frozen", lines=3)
    cv.icon_lock(167.6, 99.4, 2.2, color=FZ["stroke"])
    cv.text(167.5, 86.2, r"$\mathcal{D}_{\mathrm{test}}$", size=6.8, color=FZ["ink"])
    cv.text(167.5, 83.6, "sealed", size=6.2, color=MUTED, style="italic")
    # accept -> commit into the hero record; reject -> rejection buffer -> arbiter
    cv.arrow([(gc, yc + gh / 2), (gc, 110)], color=ACC["mark"], lw=1.1, head=1.5)
    cv.text(gc + 1.2, 107.2, "accept", size=6.4, color=ACC["ink"], style="italic", ha="left")
    cv.arrow([(gc, yc - gh / 2), (gc, 70.5), (111.9, 70.5)], color=REJ["mark"], lw=0.8, dashed=True)
    cv.text(gc + 1.2, 78.0, "reject", size=6.4, color=REJ["ink"], style="italic", ha="left")
    cv.stack(100, 66, 10, 7.5, 3, "coral", dx=0.9, dy=0.9, lw=0.6)
    cv.text(105, 69.75, "rejected", size=6.2, color=REJ["ink"], z=12)
    cv.icon_cycle(113.6, 75.6, 2.2, color=REJ["mark"])
    cv.text(106, 62.4, "blocks exact retry IDs", size=6.2, color=MUTED, style="italic")
    cv.arrow([(100, 69.75), (92.1, 69.75), (92.1, 83)], color=REJ["mark"], lw=0.8, dashed=True, head=1.2)
    # epoch loop: replay T, reflect, update proposer context
    cv.group(4, 60, 86, 19.5, "neutral", None, dashed=True, lw=0.55, radius=1.6, fill="#FAFAFB")
    cv.text(6.0, 77.4, "Epoch loop", size=7.0, weight="bold", color=NEU["ink"], ha="left")
    doc_stack(cv, 7, 63, 7, 9, DOCN, n=2, lines=2)
    cv.text(17.0, 69.3, r"replay $T$", size=6.8, ha="left")
    cv.text(17.0, 66.6, r"prev. vs current $M$", size=6.2, color=MUTED, ha="left", style="italic")
    cv.arrow([(39.5, 68), (44, 68)])
    for k, s in enumerate(("improved", "regressed", "unchanged")):
        cv.chip(44.5, 73.0 - k * 3.6, s, NEU, size=6.2, pad=0.7, h=2.8, ha="left")
    cv.arrow([(58.5, 68), (63.5, 68)])
    cv.doc(63.5, 62.5, 8.5, 10.5, "purple", lines=3)
    cv.text(73.4, 69.3, "proposer", size=6.8, color=PROP["ink"], ha="left")
    cv.text(73.4, 66.6, "context", size=6.8, color=PROP["ink"], ha="left")
    cv.icon_cycle(85.5, 68.0, 2.4, color=PROP["mark"])
    # state key: what is frozen, fixed, or updated
    kx, ky = 146.0, 76.0
    cv.text(kx, ky + 1.0, "State", size=7.0, weight="bold", color=NEU["ink"], ha="left")
    for k, (ic, lab) in enumerate((("snow", "frozen weights"), ("lock", "fixed during selection"),
                                   ("cycle", "updated online"))):
        yy = ky - 4.0 - k * 3.6
        getattr(cv, f"icon_{ic}")(kx + 1.2, yy, 2.4, color=NEU["ink"])
        cv.text(kx + 3.6, yy, lab, size=6.2, color=INK, ha="left")
    cv.arrow([(67.75, 73), (67.75, ys[-1] - 3.25)], color=PROP["mark"], lw=0.8, dashed=True, head=1.2)
    cv.text(69.0, 80.9, "next epoch", size=6.2, color=PROP["ink"], style="italic", ha="left")


def panel_b(cv, f, r):
    card(cv, 2, 2, 111, 53, "purple", "(b) Edit arbitration")
    tr = {t["id"]: t for t in [f["worked_trace"]] + f["other_evidence"]}
    # evidence documents
    t08 = f["worked_trace"]
    cv.doc(5, 27.5, 30, 18.5, DOCN, lines=0)
    cv.text(6.4, 43.4, t08["id"], size=6.8, weight="bold", ha="left")
    cv.text(6.4, 39.4, "source", size=6.2, color=MUTED, ha="left")
    cv.text(15.4, 39.4, f"{t08['source_value']} · {t08['source_date']}", size=6.4, ha="left")
    cv.text(6.4, 35.6, "answer", size=6.2, color=MUTED, ha="left")
    cv.text(15.4, 35.6, t08["baseline_answer"], size=6.4, ha="left")
    cv.text(6.4, 31.0, t08["omission"], size=6.2, color=REJ["ink"], style="italic", ha="left")
    t11 = tr["T11"]
    col, cell = [s.split(": ", 1)[1] for s in t11["source_form"].split("; ")]
    cv.doc(5, 6, 30, 18.5, DOCN, lines=0)
    cv.text(6.4, 21.9, t11["id"], size=6.8, weight="bold", ha="left")
    # tiny table: header cell + value cell
    cv.box(7.0, 9.0, 18, 8.4, "neutral", fill="white", radius=0.5, lw=0.5)
    cv.ax.plot([7.0, 25.0], [13.2, 13.2], color=NEU["stroke"], lw=0.5, zorder=7)
    cv.text(16.0, 15.3, col, size=6.2, color=INK, weight="bold")
    cv.text(16.0, 11.1, cell, size=6.4, color=INK)
    cv.text(12.0, 21.9, "table column", size=6.2, color=MUTED, ha="left", style="italic")
    # proposals sorted by priority
    cv.text(77.5, 47.6, "priority · evidence", size=6.2, color=MUTED, style="italic", ha="right")
    ys = [41.0, 29.5, 18.0]
    for p, y in zip(f["proposals"], ys):
        cv.box(40, y - 4.6, 38.5, 9.2, "purple", lw=0.6, radius=1.2)
        cv.chip(41.2, y, p["id"], PROP, size=6.4, pad=0.6, h=3.0, solid=True, ha="left")
        cv.text(47.6, y + 1.8, f"{p['operation']} {p['key']}", size=6.8, weight="bold",
                color=PROP["ink"], ha="left")
        cv.text(47.6, y - 1.9, p["value"], size=6.4, color=INK, ha="left")
        cv.text(77.0, y + 1.8, str(p["priority"]), size=7.0, weight="bold", color=PROP["mark"], ha="right")
        cv.text(77.0, y - 1.9, p["evidence"], size=6.2, color=MUTED, ha="right")
    # conflict matrix
    n, cs = 3, 4.6
    mx, my = 89.0, 22.0
    ids = [p["id"] for p in f["proposals"]]
    for i in range(n):
        cv.text(mx - 1.2, my + (n - i - 0.5) * cs, ids[i], size=6.2, color=PROP["ink"], ha="right")
        cv.text(mx + (i + 0.5) * cs, my + n * cs + 1.6, ids[i], size=6.2, color=PROP["ink"])
        for j in range(n):
            x0, y0 = mx + j * cs, my + (n - i - 1) * cs
            clash = r["conflicts"][i][j]
            fc = NEU["soft"] if i == j else (REJ["soft"] if clash else "white")
            cv.box(x0, y0, cs, cs, "neutral", fill=fc, stroke=NEU["stroke"], radius=0, lw=0.45, z=6)
            if clash:
                check(cv, x0 + cs / 2, y0 + cs / 2, False, s=2.0)
    cv.text(mx + n * cs / 2, my - 2.4, "× same key", size=6.2, color=REJ["ink"], style="italic")
    cv.text(mx + n * cs / 2, my + n * cs + 5.0, "conflicts", size=6.8, weight="bold", color=INK)
    # budget selection: two slots
    cv.text(mx + n * cs / 2, 12.4, f"budget {f['edit_budget']}", size=6.8, weight="bold", color=PROP["ink"])
    x0 = mx + n * cs / 2 - 9.6
    for k, pid in enumerate(r["selected"]):
        sx = x0 + k * 10.2
        cv.box(sx, 4.6, 9.0, 4.8, "purple", fill="white", dashed=True, radius=1.0, lw=0.5)
        cv.chip(sx + 4.5, 7.0, pid, PROP, size=6.4, pad=0.6, h=3.0, solid=True)
    cv.arrow([(mx + n * cs / 2, my - 4.0), (mx + n * cs / 2, 14.6)], head=1.1)


def panel_c(cv, f, r):
    card(cv, 116, 2, 60, 53, "amber", f"(c) Replay on case {f['validation_trace']['id']}")
    vt = f["validation_trace"]
    cv.text(146, 46.2, f"source {vt['source_value']} · {vt['source_date']}", size=6.2, color=MUTED,
            style="italic")
    cols = [("v12", f["base_version"], "base"), ("alt", f"{f['proposals'][1]['id']} only", "alt"),
            ("v13", f["next_version"], "cand")]
    cx = [139.0, 153.5, 168.0]
    cwid, rh = 13.6, 5.6
    for (k, lab, kind), x in zip(cols, cx):
        if kind == "alt":
            cv.box(x - 5.5, 39.6, 11, 3.6, "neutral", lab, fill="white", dashed=True, size=6.4,
                   weight="normal", radius=1.0, lw=0.5)
        else:
            cv.chip(x, 41.4, lab, MEMR, size=6.8, pad=1.2, h=3.6, solid=kind == "cand")
    labels = [("unit", "U"), ("date", "D"), ("citation", "C")]
    keys = [a["key"] for a in f["assertions"]]
    for i, (a, (nm, _)) in enumerate(zip(f["assertions"], labels)):
        y = 34.4 - i * (rh + 0.6)
        cv.text(118.6, y + 1.2, nm, size=6.8, weight="bold", ha="left")
        cv.text(118.6, y - 1.4, a["expected"], size=6.2, color=MUTED, ha="left")
        for (k, _, kind), x in zip(cols, cx):
            ok = r["checks"][k][i]
            v = r["outs"][k][keys[i]]
            c = ACC if ok else REJ
            cv.box(x - cwid / 2, y - rh / 2, cwid, rh, "neutral", fill=c["fill"], stroke=c["stroke"],
                   radius=0.8, lw=0.45 if kind != "cand" else 0.7)
            cv.text(x, y, v if v is not None else "—", size=6.2, color=c["ink"],
                    weight="bold" if (ok and kind == "cand") else "normal")
    # score: pips (area-true) + fraction, hero for v13
    ys = 13.6
    for (k, _, kind), x in zip(cols, cx):
        ch = r["checks"][k]
        for j, ok in enumerate(ch):
            px = x - 2.2 + j * 2.2
            cv.ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle(
                (px, ys + 2.6), 0.8, fc=ACC["mark"] if ok else "white", ec=ACC["mark"] if ok else NEU["stroke"],
                lw=0.5, zorder=9))
        hero = kind == "cand"
        cv.text(x, ys - 0.6, f"{sum(ch)}/{len(ch)}", size=8.4 if hero else 6.8, weight="bold",
                color=ACC["mark"] if hero else INK)
    cv.text(118.6, ys + 1.0, "passed", size=6.4, color=MUTED, ha="left")
    # verdicts relative to base
    nb = sum(r["checks"]["v12"])
    na, nc = sum(r["checks"]["alt"]), sum(r["checks"]["v13"])
    cv.text(cx[1], 7.6, f"{na} = {nb}: reject", size=6.2, color=REJ["ink"], style="italic")
    cv.text(cx[2], 7.6, f"{nc} > {nb}: commit", size=6.2, color=ACC["ink"], style="italic", weight="bold")
    cv.text(cx[0], 7.6, "baseline", size=6.2, color=MUTED, style="italic")




def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default=DEFAULT_FIXTURE)
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    f = json.load(open(a.fixture))
    r = evaluate(f)
    # key derived values (must match the original example's fixture-result.json)
    assert r["selected"] == ["P1", "P3"], r["selected"]
    assert r["conflicts"] == [[False, True, False], [True, False, False], [False, False, False]]
    assert r["checks"]["v12"] == [False, False, True] and r["checks"]["v13"] == [True, True, True]
    assert r["checks"]["alt"] == [False, False, True]
    assert sum(r["checks"]["v13"]) > sum(r["checks"]["v12"]) and not sum(r["checks"]["alt"]) > sum(r["checks"]["v12"])
    assert r["cand"] == {"units": "value + unit", "citation": "URL", "freshness": "source date"}
    assert r["hash"] == "48057a62", r["hash"]
    cv = Canvas(W, H, family="serif", size=7.0)
    panel_a(cv, f, r)
    panel_b(cv, f, r)
    panel_c(cv, f, r)
    print("\n".join(cv.save(os.path.join(a.out, "evidence_guided_memory"))))


if __name__ == "__main__":
    main()
