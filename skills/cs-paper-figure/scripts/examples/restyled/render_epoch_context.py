"""Epoch-context figure: how one epoch replay changes the next proposal, traced case by case.

Source: gallery/before/epoch-context.png (a: a table of four cases replayed under memory M0 and M1
with PASS/FAIL badges and a verdict change; b: a context diff C0 -> C1 with evidence IDs; c: the
same request P04 rendered under C0 and under C1), plus the bundled data
data/epoch-context/analysis.json and data/epoch-context/inputs/epoch_fixture.json. The data is a
constructed rule system on four hand-built cases (no learned model), so the key strip says so.

Content kept from the source
- The four cases T08, T11, T03, T14 with their formats and sources, the exact outputs under M0 and
  M1, the verdict groups (1 improved, 1 regressed, 2 unchanged), the context fields before and
  after with their evidence case, and both versions of proposal P04 (scope, keep, guard, defer).
- Added from the same data, not invented: the per-requirement check outcomes behind each task
  verdict and the reflection rule (R1-R4) that fired for each case.
- Derived in this script and asserted against the data: task verdicts from the checks, the
  group of every case and the group counts, the token-level diff of every context field, and
  the agreement between context C1 and the clauses of the proposal.

Design decisions
- One lane per replayed case, running through all three stages, replaces three separate tables:
  the reader follows a colour (green improved, coral regressed, grey unchanged) from the replay
  outcome to the rule, the context edit and the clause of the next proposal.
- Two levels on one line grid: the first line of a lane is the task level (case, task verdict,
  verdict change, rule); the lines below are the requirement level, where a check that flipped,
  the context token it produced and the proposal clause that cites it share a baseline.
- The state before the replay (C0 and P04 under C0) sits above the lanes in the same columns and
  with the same tokens, so "before" is read downwards against "after".
- Hero: the proposal column. Under C0 it is one unguarded scope line; under C1 every lane adds a
  solid clause chip.
- Colour = role: teal context, purple proposal, slate replay runtime, green / coral / grey the
  verdict change of a lane. Monospace = data; serif = the figure's own words.

    python render_epoch_context.py --out figures/epoch [--analysis a.json] [--fixture f.json]
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))

from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402

from paperkit import INK, MUTED, ROLE, Canvas, mix  # noqa: E402

DATA = os.path.join(HERE, "data", "epoch-context")
ANALYSIS = os.path.join(DATA, "analysis.json")
FIXTURE = os.path.join(DATA, "inputs", "epoch_fixture.json")
STEM = "epoch-context"
W, H = 178.0, 102.6

GREEN, CORAL, GREY, TEAL, PURPLE, SLATE = (ROLE[k] for k in ("memory", "coral", "neutral", "teal", "purple", "frozen"))
GROUP_ROLE = {"improved": "memory", "regressed": "coral", "unchanged": "neutral"}
LANE_TINT = {"improved": GREEN["fill"], "regressed": CORAL["fill"], "unchanged": mix(GREY["fill"], GREY["soft"], 0.6)}
RULE_VERB = {"R1": "keep the gain", "R2": "guard the regression", "R3": "carry the failure", "R4": "no new rule"}
CLAUSE = {"retain": ("keep", "KEEP"), "protect": ("guards", "GUARD"), "open": ("deferred", "DEFER")}
FIELDS = ("allow_inline", "retain", "protect", "open")
MS = 5.8          # monospace size (pt); also the smallest text in the figure
PITCH = 4.3       # line pitch inside a lane (mm)


# ------------------------------------------------------------------ data logic ---
def source_text(case):
    s = case["source"]
    if case["format"] == "scalar":
        d = datetime.date.fromisoformat(s["date"])
        return f"{s['value']} {s['unit']}, {d.day} {d:%b}"
    if case["format"] == "csv":
        return f"{s['field']} {s['value']} {s['unit']}"
    if case["format"] == "range":
        return f"{s['lower']}–{s['upper']} {s['unit']}"
    return str(s["value"])


def group_of(p0, p1):
    return "improved" if (not p0 and p1) else "regressed" if (p0 and not p1) else "unchanged"


def diff(before, after):
    """Token-level diff of a list-valued field: [(token, 'same' | 'del' | 'add')]."""
    return ([(t, "same" if t in after else "del") for t in before] + [(t, "add") for t in after if t not in before])


# ---------------------------------------------------------------- local helpers ---
def mono(cv, x, y, s, size=MS, color=INK, weight="normal", ha="left", **kw):
    return cv.text(x, y, s, size=size, color=color, weight=weight, ha=ha, family="monospace", **kw)


def mono_w(cv, s, size=MS, weight="normal"):
    t = cv.ax.text(0, 0, s, fontsize=size, weight=weight, family="monospace")
    w = t.get_window_extent(cv._renderer()).width / cv.fig.dpi * 25.4
    t.remove()
    return w


def frame(cv, x, y, w, h, r, title, letter, solid=False, size=7.4):
    """Dashed module frame on a near-white tint; the title pill sits on the top border at the left."""
    c = ROLE[r]
    cv.section(x, y, w, h, r, None, fill=mix(c["fill"], "#FFFFFF", 0.45))
    tw, th = cv.text_width(title, size, "bold") + 3.8 + 3.5, size * 0.56
    x0 = x + 3.0
    cv.ax.add_patch(FancyBboxPatch((x0, y + h - th / 2), tw, th, boxstyle=f"round,pad=0,rounding_size={th / 2}",
                                   fc=c["mark"] if solid else c["soft"], ec=c["mark"] if solid else c["stroke"],
                                   lw=0.6, zorder=1.3))
    cv.ax.add_patch(Circle((x0 + 2.4, y + h), 1.55, fc="white" if solid else c["mark"], ec="none", zorder=1.5))
    cv.text(x0 + 2.4, y + h - 0.05, letter, size=6.4, weight="bold", color=c["mark"] if solid else "white", z=1.6)
    cv.text(x0 + 5.4, y + h - 0.05, title, size=size, weight="bold", color="white" if solid else c["ink"], ha="left",
            z=1.4)


def mark(cv, x, y, ok, solid=False, s=3.0):
    c = GREEN if ok else CORAL
    cv.ax.add_patch(FancyBboxPatch((x - s / 2, y - s / 2), s, s, boxstyle="round,pad=0,rounding_size=0.55",
                                   fc=c["mark"] if solid else "white", ec=c["mark"] if solid else c["stroke"], lw=0.45,
                                   zorder=7))
    (cv.icon_check if ok else cv.icon_cross)(x, y, s * 0.52, color="white" if solid else c["mark"], lw=0.95, z=8)


def tok(cv, x, y, s, kind="same", r="neutral", h=3.3):
    """Monospace token chip. kind: 'same' (plain), 'add' (+, tinted), 'del' (struck through). Returns its right x."""
    c = ROLE[r]
    label = "+" + s if kind == "add" else s
    w = mono_w(cv, label) + 1.5
    fc = {"same": "white", "add": c["soft"], "del": "white"}[kind]
    cv.chips.append((x, y - h / 2, w, h, label, None))
    cv.ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.7", fc=fc,
                                   ec=c["stroke"], lw=0.45, zorder=7, ls=(0, (2, 1.2)) if kind == "del" else "-"))
    mono(cv, x + w / 2, y, label, ha="center", color=c["ink"] if kind != "same" else INK,
         weight="bold" if kind == "add" else "normal", z=8)
    if kind == "del":
        cv.ax.plot([x + 0.7, x + w - 0.7], [y, y], color=c["mark"], lw=0.7, zorder=9)
    return x + w


def strip(cv, x, y, w, h, fill, edge):
    cv.box(x, y, w, h, fill=fill, stroke=edge, lw=0.45, radius=1.2, container=True, z=3)


def key_strip(cv, x, y, items, size=6.0, h=5.6, gap=3.6, pad=2.0):
    """Glyph key in a dashed strip sized to its content. items = [(glyph width, draw(x, y), label)]."""
    xx = x + pad
    for gw, fn, lab in items:
        fn(xx, y + h / 2)
        cv.text(xx + gw + 1.1, y + h / 2, lab, size=size, ha="left")
        xx += gw + 1.1 + cv.text_width(lab, size) + gap
    cv.ax.add_patch(FancyBboxPatch((x, y), xx - gap + pad - x, h, boxstyle="round,pad=0,rounding_size=1.6", fc="none",
                                   ec=GREY["stroke"], lw=0.6, ls=(0, (3, 2)), zorder=3))
    return h


def draw(out, analysis=ANALYSIS, fixture=FIXTURE):
    an, fx = json.load(open(analysis)), json.load(open(fixture))
    cases = {c["id"]: c for c in fx["cases"]}
    c0, c1 = an["context_before"], an["context_after"]
    p0, p1 = an["proposal_before"], an["proposal_after"]
    states = list(fx["memory_states"])                                   # M0, M1

    # ---- derive and check everything that is printed ------------------------------------
    lanes = []
    for r in an["replay"]:
        cid, st = r["case_id"], r["states"]
        checks = cases[cid]["required_checks"]
        ok = {m: all(st[m]["checks"][k] for k in checks) for m in states}
        assert all(ok[m] == st[m]["pass"] for m in states), cid            # a task passes iff every check passes
        grp = group_of(ok[states[0]], ok[states[1]])
        assert grp == r["group"] == cases[cid]["expected_transition"], cid
        rules = {t["rule"] for t in an["reflection_trace"] if t["case_id"] == cid}
        assert len(rules) == 1, cid
        lanes.append(dict(id=cid, fmt=r["format"], src=source_text(cases[cid]), checks=checks, st=st, ok=ok, grp=grp,
                          rule=rules.pop(), fields=[f for f in FIELDS if cid in c1["evidence"][f]]))
    counts = {g: sum(l["grp"] == g for l in lanes) for g in ("improved", "regressed", "unchanged")}
    assert counts == an["counts"], counts
    assert c1 == fx["expected_fixture"]["context_after"]
    for f, (key, _) in CLAUSE.items():                                    # C1 fields reappear as proposal clauses
        assert p1[key] == c1[f] and p0[key] == c0[f] == [], f
    assert p0["patch"]["scope"] == c0["allow_inline"] and p1["patch"]["scope"] == c1["allow_inline"]
    assert p1["evidence"] == c1["evidence"] and p0["request_id"] == p1["request_id"] == fx["next_request"]["id"]
    assert set(RULE_VERB) == {r["id"] for r in fx["reflection_rules"]}
    req = p1["request_id"]

    cv = Canvas(W, H)
    A, B, C = (2.0, 99.5), (105.0, 38.0), (146.5, 29.5)                   # (x, width) of the three stage frames
    y0, top = 10.0, 99.0
    frame(cv, A[0], y0, A[1], top - y0, "frozen", "Matched replay", "a")
    frame(cv, B[0], y0, B[1], top - y0, "teal", "Context update", "b")
    frame(cv, C[0], y0, C[1], top - y0, "purple", "Next proposal", "c", solid=True)
    ax0, ax1 = A[0] + 1.8, A[0] + A[1] - 1.8                              # lane strip extents per frame
    bx0, bx1 = B[0] + 1.8, B[0] + B[1] - 1.8
    cx0, cx1 = C[0] + 1.7, C[0] + C[1] - 1.7
    X_OUT = (24.0, 40.5)                                                  # output boxes for M0, M1
    W_OUT = (15.4, 19.6)
    X_CHK, X_MK, X_PILL = 62.2, (78.7, 83.1), 92.4
    X_FLD, X_TOK = bx0 + 1.4, bx0 + 17.4
    X_CL, X_VAL, X_STK = cx0 + 1.2, cx0 + 11.3, cx0 + 8.6

    # ---- header rows: the state before the replay, in the same columns as the lanes ------
    r1, r2, r3, r4 = 94.4, 90.5, 86.8, 82.5
    cv.text(6.2, r1, fx["split"].replace("_", " "), size=6.0, style="italic", color=SLATE["ink"], ha="left")
    cv.text(6.2, r2, f"{len(lanes)} constructed cases", size=6.0, style="italic", color=SLATE["ink"], ha="left")
    for m, x in zip(states, X_OUT):
        ms = fx["memory_states"][m]
        cv.chip(x + 0.2, r1, m, "memory", size=6.2, solid=True, ha="left")
        cv.text(x + 0.2, r2, {"header": "units in header", "inline_all": "units inline, all formats"}[ms["unit_mode"]],
                size=5.8, style="italic", color=GREEN["ink"], ha="left")
        cv.text(x + 0.2, r3, "scalar date kept" if ms["scalar_date"] else "no scalar date", size=5.8, style="italic",
                color=GREEN["ink"], ha="left")
        cv.text(x + 0.2, r4, "output", size=5.8, style="italic", color=MUTED, ha="left")
    cv.text(6.2, r4, "case and source", size=5.8, style="italic", color=MUTED, ha="left")
    cv.text(X_CHK, r4, "required check", size=5.8, style="italic", color=MUTED, ha="left")
    for m, x in zip(states, X_MK):
        cv.text(x, r4, m, size=5.8, weight="bold", color=GREEN["ink"])
    cv.text(X_PILL, r4, "verdict change", size=5.8, style="italic", color=MUTED)

    cv.text(X_FLD, r1, r"Context $\mathbf{C}_0$", size=6.6, weight="bold", color=TEAL["ink"], ha="left")
    strip(cv, bx0, r3 - 2.0, bx1 - bx0, r2 - r3 + 4.2, "white", TEAL["soft"])
    mono(cv, X_FLD, r2, FIELDS[0], weight="bold")
    x = X_TOK
    for t in c0[FIELDS[0]]:
        x = tok(cv, x, r2, t) + 0.8
    empty = [f for f in FIELDS if not c0[f]]
    cv.text(X_FLD, r3, ", ".join(empty) + ": empty", size=5.8, style="italic", color=MUTED, ha="left")
    cv.text(X_FLD, r4, r"Edits giving $\mathbf{C}_1$", size=6.6, weight="bold", color=TEAL["ink"], ha="left")

    cv.text(X_CL, r1, rf"{req} under $\mathbf{{C}}_0$", size=6.6, weight="bold", color=PURPLE["ink"], ha="left")
    strip(cv, cx0, r3 - 2.0, cx1 - cx0, r2 - r3 + 4.2, "white", PURPLE["soft"])
    mono(cv, X_CL, r2, "scope", weight="bold")
    x = X_STK
    for t in p0["patch"]["scope"]:
        x = tok(cv, x, r2, t) + 0.8
    cv.text(X_CL, r3, "nothing attached", size=5.8, style="italic", color=MUTED, ha="left")
    cv.text(X_CL, r4, rf"{req} under $\mathbf{{C}}_1$", size=6.6, weight="bold", color=PURPLE["ink"], ha="left")

    # ---- lanes ---------------------------------------------------------------------------
    ytop = 79.1
    for ln in lanes:
        role, c = GROUP_ROLE[ln["grp"]], ROLE[GROUP_ROLE[ln["grp"]]]
        n = 1 + len(ln["checks"])
        h = n * PITCH + 2.6
        yb = ytop - h
        ly = [ytop - 1.3 - PITCH / 2 - i * PITCH for i in range(n)]       # line centres, top down
        mid = yb + h / 2
        tint = LANE_TINT[ln["grp"]]
        for x_a, x_b in ((ax0, ax1), (bx0, bx1), (cx0, cx1)):
            strip(cv, x_a, yb, x_b - x_a, h, tint, c["soft"])
        cv.ax.add_patch(FancyBboxPatch((ax0, yb), 1.5, h, boxstyle="round,pad=0,rounding_size=0.7", fc=c["mark"],
                                       ec="none", zorder=3.5))

        # (a) case, outputs, task verdict and required checks
        x0, w0 = cv.chip(ax0 + 2.6, ly[0], ln["id"], role, size=6.0, solid=True, ha="left")
        cv.text(x0 + w0 + 1.0, ly[0], ln["fmt"], size=6.0, style="italic", color=c["ink"], ha="left")
        mono(cv, ax0 + 2.8, ly[1], ln["src"])
        for m, x, w in zip(states, X_OUT, W_OUT):
            rows = ln["st"][m]["output"].split("\n")
            bh = len(rows) * 3.5 + 1.7
            cv.box(x, mid - bh / 2, w, bh, fill="white", stroke=c["stroke"], lw=0.5, radius=0.9)
            for k, s in enumerate(rows):
                mono(cv, x + 1.1, mid + (len(rows) - 1) * 1.75 - k * 3.5, s)
        cv.text(X_CHK, ly[0], "task", size=6.2, weight="bold", style="italic", color=c["ink"], ha="left")
        cv.ax.plot([X_CHK - 0.3, X_MK[1] + 2.0], [ly[0] - PITCH / 2] * 2, color=c["stroke"], lw=0.45, zorder=4)
        for m, x in zip(states, X_MK):
            mark(cv, x, ly[0], ln["ok"][m], solid=True)
            for i, k in enumerate(ln["checks"]):
                mark(cv, x, ly[1 + i], ln["st"][m]["checks"][k])
        for i, k in enumerate(ln["checks"]):
            mono(cv, X_CHK, ly[1 + i], k)
        cv.chip(X_PILL, ly[0], ln["grp"], role, size=6.2, solid=True, h=3.7)

        # (b) rule, then one line per context edit, on the line of the check it restates when there is one
        cv.arrow([(ax1, ly[0]), (bx0, ly[0])], color=c["mark"], lw=1.0, head=1.4)
        x0, w0 = cv.chip(bx0 + 1.3, ly[0], ln["rule"], "teal", size=6.0, solid=True, ha="left")
        cv.text(x0 + w0 + 1.1, ly[0], RULE_VERB[ln["rule"]], size=6.0, style="italic", color=TEAL["ink"], ha="left")
        free = list(range(1, n))
        placed = []                                                        # (line, field, tokens, first line of field)
        for f in ln["fields"]:
            d = diff(c0[f], c1[f])
            hits = [(ln["checks"].index(t) + 1, [(t, k)]) for t, k in d if t in ln["checks"]]
            if len(hits) == len(d):                                        # every token restates a check: align them
                rows = hits
            else:                                                          # otherwise the field takes one free line
                rows = [(next(i for i in free if i not in [r_[0] for r_ in hits]), d)]
            for j, (i, toks) in enumerate(sorted(rows)):
                free.remove(i)
                placed.append((i, f, toks, j == 0))
        for i, f, toks, first in placed:
            y = ly[i]
            if first:
                mono(cv, X_FLD, y, f, weight="bold")
            x = X_TOK
            for t, k in toks:
                x = tok(cv, x, y, t, k, role if k != "same" else "neutral") + 0.8
            assert x - 0.8 <= bx1 - 0.5, (f, x)
            # (c) the clause of the next proposal that carries this edit
            cv.arrow([(bx1, y), (cx0, y)], color=c["mark"], lw=1.0, head=1.4)
            if f == "allow_inline":
                mono(cv, X_CL, y, "scope", weight="bold")
                x = X_STK
                for t, k in diff(p0["patch"]["scope"], p1["patch"]["scope"]):
                    x = tok(cv, x, y, t, k, role if k != "same" else "neutral") + 0.8
                assert x - 0.8 <= cx1 - 0.5, x
            else:
                if first:
                    cv.chip(X_CL, y, CLAUSE[f][1], role, size=5.9, solid=True, ha="left", pad=0.8)
                for t, _ in toks:
                    mono(cv, X_VAL, y, t)
        if ln["fields"]:
            ex = cv.rich(X_CL, ly[0], [("cites", MUTED)], size=5.9)
            cv.chip(ex + 1.2, ly[0], ln["id"], role, size=5.9, solid=True, ha="left")
        else:
            cv.text((cx0 + cx1) / 2, mid, "no clause", size=5.9, style="italic", color=MUTED)
        ytop = yb - 1.8

    # ---- footers ---------------------------------------------------------------------------
    fy = 12.9
    segs = [("Derived groups:  ", INK)]
    for g in ("improved", "regressed", "unchanged"):
        segs += [(f"{counts[g]} {g}", ROLE[GROUP_ROLE[g]]["ink"], "bold"), ("  ·  ", MUTED)]
    cv.rich(6.2, fy, segs[:-1], size=6.2)
    cv.text(ax1 - 0.5, fy, "a task passes only if every check does", size=5.8, style="italic", color=MUTED, ha="right")
    cv.text((bx0 + bx1) / 2, fy, "fixed rules R1–R4, one per case", size=5.8, style="italic", color=MUTED)
    cv.text((cx0 + cx1) / 2, fy, "proposed only, not validated", size=5.8, style="italic", color=MUTED)

    # ---- key strip -------------------------------------------------------------------------
    kh = key_strip(cv, 2, 1.6, [
        (3.2, lambda x, y: mark(cv, x + 1.6, y, True, solid=True), "task verdict"),
        (6.8, lambda x, y: (mark(cv, x + 1.5, y, True), mark(cv, x + 5.3, y, False)), "required check passes / fails"),
        (7.6, lambda x, y: tok(cv, x, y, "new", "add", "memory") and None, "token added"),
        (6.4, lambda x, y: tok(cv, x, y, "old", "del", "coral") and None, "token removed")])
    cv.text(176, 1.6 + kh / 2 + 1.5, "Constructed cases and a fixed rule system:", size=5.9, style="italic",
            color=MUTED, ha="right")
    cv.text(176, 1.6 + kh / 2 - 1.5, "illustrative only, no learned model, not measured results", size=5.9,
            style="italic", color=MUTED, ha="right")

    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="figures/epoch")
    ap.add_argument("--analysis", default=ANALYSIS)
    ap.add_argument("--fixture", default=FIXTURE)
    a = ap.parse_args()
    print("\n".join(draw(a.out, a.analysis, a.fixture)))
