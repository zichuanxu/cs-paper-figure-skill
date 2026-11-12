"""Epoch-context figure: how one epoch replay changes the next proposal, traced case by case.

Source: gallery/before/epoch-context.png (a: a table of four cases replayed under memory M0 and M1
with PASS/FAIL badges and a verdict change; b: a context diff C0 -> C1 with evidence IDs; c: the
same request P04 rendered under C0 and under C1), plus the bundled data
data/epoch-context/analysis.json and data/epoch-context/inputs/epoch_fixture.json. The data is a
constructed rule system on four hand-built cases (no learned model), and the figure says so.

Content kept from the source
- The four cases T08, T11, T03, T14 with their formats and sources, the exact outputs under M0 and
  M1, the verdict groups (1 improved, 1 regressed, 2 unchanged), the context fields before and
  after with their evidence case, and both versions of proposal P04 (scope, keep, guard, defer).
- Added from the same data, not invented: the per-requirement check outcomes behind each task
  verdict, the reflection rule (R1-R4) that fired for each case, and the text M1 added to each output.
- Derived in this script and asserted against the data: task verdicts from the checks, the
  group of every case and the group counts, the token-level diff of every context field, the
  suffix M1 appends to an output, and the agreement between context C1 and the proposal's clauses.

Design (visual-craft.md; registers.md section 3 grid inside a light plate, section 6)
- Message: the one case that regressed in the replay rewrites the context and narrows the next proposal.
- Hero: case T11. Its lane is the only tinted field and the only one with saturated solid marks; every
  other lane sits on the white page between hairlines with pale chips. Nothing is thickened.
- Skeleton: an example x stage grid. One lane per replayed case crosses the three stages on one line
  grid, so a check that flipped, the context token it produced and the proposal clause that cites it
  share a baseline. The state before the replay (C0, P04 under C0) is the first row of the same
  columns. The lanes align, so the figure has no wires: a triangle in a gutter says "read on", black
  on the head rule for the stage order and coral inside the followed lane.
- Palette, two hues and grey: coral = the regressed case and everything it causes; green = the improved
  case and what it causes; grey = unchanged. A coloured tick or cross is a check that flipped under M1.
- Type: 8.0 pt stage heads, 6.5 pt labels and monospace data, 5.8 pt italic annotations.
  Monospace = text from the fixture; serif = the figure's own words.
- Strokes: 0.5 pt outlines and hairlines, 0.9 pt rules, glyphs and strike-throughs.

    python render_epoch_context.py --out figures/epoch [--analysis a.json] [--fixture f.json]
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))

from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle  # noqa: E402

from paperkit import HAIR, INK, MUTED, PT_PER_MM, ROLE, Canvas  # noqa: E402

DATA = os.path.join(HERE, "data", "epoch-context")
ANALYSIS = os.path.join(DATA, "analysis.json")
FIXTURE = os.path.join(DATA, "inputs", "epoch_fixture.json")
STEM = "epoch-context"
W = 178.0

GROUP_ROLE = {"improved": "memory", "regressed": "coral", "unchanged": "neutral"}
VER_HEAD = "verdict change"
HERO = "regressed"                                   # the lane the figure follows
GREY = ROLE["neutral"]
RULE_VERB = {"R1": "keep the gain", "R2": "guard the regression", "R3": "carry the failure", "R4": "no new rule"}
CLAUSE = {"retain": ("keep", "KEEP"), "protect": ("guards", "GUARD"), "open": ("deferred", "DEFER")}
FIELDS = ("allow_inline", "retain", "protect", "open")
HS, LS, FS = 8.0, 6.5, 5.8      # the type scale (pt): stage heads / labels and monospace data / annotations
THIN, HEAVY = 0.5, 0.9          # the two stroke weights (pt)
PITCH, PAD, RGAP = 4.2, 1.5, 1.2  # line pitch in a lane, lane padding, gap between lanes (mm)
M, INSET, G1 = 1.5, 2.0, 2.4    # outer margin, content inset inside a stage, gutter inside a stage (mm)


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


def appended(o0, o1):
    """Per output line, (text shared with the M0 output, text M1 appended). M1 only ever appends here."""
    l0, l1 = o0.split("\n"), o1.split("\n")
    assert len(l0) == len(l1) and all(b.startswith(a) for a, b in zip(l0, l1)), (o0, o1)
    return [(a, b[len(a):]) for a, b in zip(l0, l1)]


# ---------------------------------------------------------------- local helpers ---
def mono(cv, x, y, s, color=INK, weight="normal", ha="left", **kw):
    return cv.text(x, y, s, size=LS, color=color, weight=weight, ha=ha, family="monospace", **kw)


def mark(cv, x, y, ok, c, task=False, solid=False):
    """Tick or cross. task=True sets it in a rounded square (the task verdict); bare = one required check."""
    glyph = cv.icon_check if ok else cv.icon_cross
    if not task:
        return glyph(x, y, 1.9, color=c["mark"], lw=HEAVY, z=8)
    s = 3.1
    cv.ax.add_patch(FancyBboxPatch((x - s / 2, y - s / 2), s, s, boxstyle="round,pad=0,rounding_size=0.6",
                                   fc=c["mark"] if solid else c["soft"], ec="none", zorder=7))
    glyph(x, y, 1.7, color="white" if solid else c["ink"], lw=HEAVY, z=8)


def pill(cv, x, y, s, r, solid):
    """Left-anchored pill; a solid one is outlined in its own fill (cv.chip keeps the pale role stroke)."""
    x0, w = cv.chip(x, y, s, r, size=LS, solid=solid, ha="left")
    if solid:
        cv.ax.patches[-1].set_edgecolor(ROLE[r]["mark"])
    return x0, w


def tok_w(s, kind, cw):
    return (len(s) + (kind == "add")) * cw + 1.5


def tok(cv, x, y, s, kind, c, cw, h=3.4):
    """Monospace token. kind: 'same' (plain), 'add' (+, tinted), 'del' (dashed, struck through). Returns right x."""
    label = "+" + s if kind == "add" else s
    w = tok_w(s, kind, cw)
    cv.chips.append((x, y - h / 2, w, h, label, None))
    cv.ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.7",
                                   fc=c["soft"] if kind == "add" else "white", lw=THIN, zorder=7,
                                   ec=GREY["stroke"] if kind == "same" else c["stroke"],
                                   ls=(0, (2, 1.2)) if kind == "del" else "-"))
    mono(cv, x + w / 2, y, label, ha="center", color=INK if kind == "same" else c["ink"],
         weight="bold" if kind == "add" else "normal", z=8)
    if kind == "del":
        cv.ax.plot([x + 0.7, x + w - 0.7], [y, y], color=c["mark"], lw=HEAVY, zorder=9)
    return x + w


def run_w(toks, cw):
    return sum(tok_w(t, k, cw) for t, k in toks) + 0.8 * (len(toks) - 1)


def rule(cv, x0, x1, y, lw=THIN, color=INK):
    cv.ax.plot([x0, x1], [y, y], color=color, lw=lw, zorder=4, solid_capstyle="butt")


def chevron(cv, x, y, color, s=1.9):
    """Filled triangle centred on (x, y) in a gutter between two stages: 'read on to the right'."""
    cv.ax.add_patch(Polygon([(x - s / 2, y + s * 0.48), (x + s / 2, y), (x - s / 2, y - s * 0.48)], fc=color,
                            ec="none", zorder=6))


def key_row(cv, x, y, items, gap=4.2):
    """Frameless key: items = [(glyph width, draw(x, y), label)], laid out like words. Returns the end x."""
    for gw, fn, lab in items:
        fn(x, y)
        cv.text(x + gw + 1.0, y, lab, size=FS, ha="left")
        x += gw + 1.0 + cv.text_width(lab, FS) + gap
    return x - gap


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
                          rule=rules.pop(), fields=[f for f in FIELDS if cid in c1["evidence"][f]],
                          added=appended(st[states[0]]["output"], st[states[1]]["output"])))
    counts = {g: sum(ln["grp"] == g for ln in lanes) for g in ("improved", "regressed", "unchanged")}
    assert counts == an["counts"], counts
    assert counts[HERO] == 1                                               # one lane is followed
    assert c1 == fx["expected_fixture"]["context_after"]
    for f, (key, _) in CLAUSE.items():                                    # C1 fields reappear as proposal clauses
        assert p1[key] == c1[f] and p0[key] == c0[f] == [], f
    assert p0["patch"]["scope"] == c0["allow_inline"] and p1["patch"]["scope"] == c1["allow_inline"]
    assert p1["evidence"] == c1["evidence"] and p0["request_id"] == p1["request_id"] == fx["next_request"]["id"]
    assert set(RULE_VERB) == {r["id"] for r in fx["reflection_rules"]}
    req = p1["request_id"]

    # ---- canvas: the height follows the number of lines ----------------------------------
    n_lines = sum(1 + len(ln["checks"]) for ln in lanes)
    body = n_lines * PITCH + len(lanes) * 2 * PAD + (len(lanes) - 1) * RGAP
    head, foot = 23.4, 12.6
    H = head + 1.0 + body + foot
    cv = Canvas(W, H, size=LS)
    cw = cv.text_width("0" * 20, LS, family="monospace") / 20             # monospace advance (mm)

    def pill_w(s):
        return cv.text_width(s, LS) + 1.8

    # ---- columns from measured content; the slack goes to the two gutters between stages ----
    MK, MG = 3.1, 1.5                                                     # mark size and gap
    case_w = max(max(len(ln["src"]) * cw for ln in lanes),
                 max(pill_w(ln["id"]) + 1.0 + cv.text_width(ln["fmt"], LS, style="italic") for ln in lanes))
    out_w = [max(len(r) for ln in lanes for r in ln["st"][m]["output"].split("\n")) * cw + 2.4 for m in states]
    chk_w = max(len(k) for ln in lanes for k in ln["checks"]) * cw
    X_CASE = M + INSET
    X_OUT = [X_CASE + case_w + G1]
    X_OUT.append(X_OUT[0] + out_w[0] + 1.6)
    X_CHK = X_OUT[1] + out_w[1] + G1
    X_MK = [X_CHK + chk_w + MG + MK / 2]
    X_MK.append(X_MK[0] + MK + MG)
    X_VER = X_MK[1] + MK / 2 + G1
    a_end = X_VER + max([pill_w(g) for g in counts] + [cv.text_width(VER_HEAD, FS, style="italic")])

    fld_w = max(len(f) for f in FIELDS) * cw
    all_checks = {k for ln in lanes for k in ln["checks"]}

    def widest(f):                                                        # a token that restates a check gets its own line
        d = diff(c0[f], c1[f])
        return max(tok_w(t, k, cw) for t, k in d) if all(t in all_checks for t, _ in d) else run_w(d, cw)
    b_w = fld_w + 1.6 + max(widest(f) for f in FIELDS)
    chip_w = max(pill_w(lab) for _, lab in CLAUSE.values())
    scope_w = len("scope") * cw + 1.6
    c_w = max(chip_w + 1.2 + max(len(t) for f in CLAUSE for t in c1[f]) * cw,
              scope_w + run_w(diff(p0["patch"]["scope"], p1["patch"]["scope"]), cw))
    cx0 = W - M - INSET - c_w
    G2 = (cx0 - a_end - b_w) / 2                                          # gutter between stages (content edges)
    assert G2 >= 4.0, G2
    bx0 = a_end + G2
    X_TOK, X_VAL, X_STK = bx0 + fld_w + 1.6, cx0 + chip_w + 1.2, cx0 + scope_w
    stages = [(X_CASE, a_end), (bx0, bx0 + b_w), (cx0, cx0 + c_w)]        # rules run flush with the content

    # ---- stage heads and the state before the replay, in the columns the lanes use ----------
    yH, yR1, b1, b2, b3, yL, yR2 = (H - d for d in (3.1, 5.8, 9.0, 13.0, 17.0, 21.4, head))
    for (x0, x1), xt, t in zip(stages, (X_CASE, bx0, cx0),
                               ("(a) Matched replay", "(b) Context update", "(c) Next proposal")):
        cv.text(xt, yH, t, size=HS, weight="bold", ha="left")
        rule(cv, x0, x1, yR1, HEAVY)
        rule(cv, x0, x1, yR2)
    gut = [(stages[k][1] + stages[k + 1][0]) / 2 for k in (0, 1)]         # centres of the two gutters
    for x in gut:
        chevron(cv, x, yR1, INK)
    cv.text(X_CASE, b1, fx["split"].replace("_", " "), size=FS, style="italic", color=MUTED, ha="left")
    cv.text(X_CASE, b2, f"{len(lanes)} constructed cases", size=FS, style="italic", color=MUTED, ha="left")
    for m, x, xm in zip(states, X_OUT, X_MK):
        ms = fx["memory_states"][m]
        cv.text(x, b1, f"Memory {m}", ha="left")
        cv.text(x, b2, {"header": "units in header", "inline_all": "units inline, all formats"}[ms["unit_mode"]],
                size=FS, style="italic", color=MUTED, ha="left")
        cv.text(x, b3, "scalar date kept" if ms["scalar_date"] else "no scalar date", size=FS, style="italic",
                color=MUTED, ha="left")
        cv.text(x, yL, f"output under {m}", size=FS, style="italic", color=MUTED, ha="left")
        cv.text(xm, yL, m, size=FS, weight="bold")
    cv.text(X_CASE, yL, "case and source", size=FS, style="italic", color=MUTED, ha="left")
    cv.text(X_CHK, yL, "required check", size=FS, style="italic", color=MUTED, ha="left")
    cv.text(X_VER, yL, VER_HEAD, size=FS, style="italic", color=MUTED, ha="left")
    cv.text(X_CHK, b3, "a task passes only if every check does", size=FS, style="italic", color=MUTED, ha="left")

    cv.text(bx0, b1, "Context C0", ha="left")
    mono(cv, bx0, b2, FIELDS[0], weight="bold")
    x = X_TOK
    for t in c0[FIELDS[0]]:
        x = tok(cv, x, b2, t, "same", GREY, cw) + 0.8
    cv.text(bx0, b3, ", ".join(f for f in FIELDS if not c0[f]) + ": empty", size=FS, style="italic", color=MUTED,
            ha="left")
    cv.text(bx0, yL, "Edits giving C1", ha="left")

    cv.text(cx0, b1, f"{req} under C0", ha="left")
    mono(cv, cx0, b2, "scope", weight="bold")
    x = X_STK
    for t in p0["patch"]["scope"]:
        x = tok(cv, x, b2, t, "same", GREY, cw) + 0.8
    cv.text(cx0, b3, "nothing attached", size=FS, style="italic", color=MUTED, ha="left")
    cv.text(cx0, yL, f"{req} under C1", ha="left")

    # ---- lanes ---------------------------------------------------------------------------
    ytop = yR2 - 1.0
    for li, ln in enumerate(lanes):
        role, c, hero = GROUP_ROLE[ln["grp"]], ROLE[GROUP_ROLE[ln["grp"]]], ln["grp"] == HERO
        n = 1 + len(ln["checks"])
        h = n * PITCH + 2 * PAD
        yb = ytop - h
        ly = [ytop - PAD - PITCH / 2 - i * PITCH for i in range(n)]       # line centres, top down
        mid = yb + h / 2
        flip = {k: ln["st"][states[0]]["checks"][k] != ln["st"][states[1]]["checks"][k] for k in ln["checks"]}
        if hero:                                                           # the one tinted field: the lane followed
            cv.ax.add_patch(FancyBboxPatch((M, yb), W - 2 * M, h, boxstyle="round,pad=0,rounding_size=1.4",
                                           fc=c["fill"], ec="none", zorder=1))
        elif li + 1 < len(lanes) and lanes[li + 1]["grp"] != HERO:         # hairline to the next plain lane
            rule(cv, X_CASE, W - M - INSET, yb - RGAP / 2, color=HAIR)

        # (a) case, outputs with the text M1 appended marked, task verdict and required checks
        x0, w0 = pill(cv, X_CASE, ly[0], ln["id"], role, hero)
        cv.text(x0 + w0 + 1.0, ly[0], ln["fmt"], style="italic", ha="left")
        mono(cv, X_CASE, ly[1], ln["src"])
        for j, (m, x, w) in enumerate(zip(states, X_OUT, out_w)):
            rows = ln["added"] if j == 1 else [(s, "") for s in ln["st"][m]["output"].split("\n")]
            bh = len(rows) * 3.6 + 1.8
            cv.box(x, mid - bh / 2, w, bh, fill="white", stroke=GREY["stroke"], lw=THIN, radius=0)
            for k, (kept, add) in enumerate(rows):
                yy = mid + (len(rows) - 1) * 1.8 - k * 3.6
                mono(cv, x + 1.2, yy, kept)
                if add:
                    lead = len(add) - len(add.lstrip())
                    xa, bh2 = x + 1.2 + (len(kept) + lead) * cw, 1.2 * LS / PT_PER_MM
                    cv.ax.add_patch(Rectangle((xa - 0.2, yy - bh2 / 2), (len(add) - lead) * cw + 0.4, bh2,
                                              fc=c["soft"], ec="none", zorder=6))
                    mono(cv, xa, yy, add.lstrip(), color=c["ink"], weight="bold")
        cv.text(X_CHK, ly[0], "task", style="italic", ha="left")
        for j, (m, x) in enumerate(zip(states, X_MK)):
            changed = j == 1 and ln["ok"][states[0]] != ln["ok"][m]
            mark(cv, x, ly[0], ln["ok"][m], c if changed else GREY, task=True, solid=changed and hero)
            for i, k in enumerate(ln["checks"]):
                mark(cv, x, ly[1 + i], ln["st"][m]["checks"][k], c if (j == 1 and flip[k]) else GREY)
        for i, k in enumerate(ln["checks"]):
            mono(cv, X_CHK, ly[1 + i], k)
        pill(cv, X_VER, ly[0], ln["grp"], role, hero)

        # (b) the rule, then one line per context edit, on the line of the check it restates when there is one
        if hero:
            chevron(cv, gut[0], ly[0], c["mark"])
        ex = cv.rich(bx0, ly[0], [(ln["rule"], INK, "bold")], size=LS)
        cv.text(ex + 1.2, ly[0], RULE_VERB[ln["rule"]], style="italic", color=c["ink"] if ln["fields"] else MUTED,
                ha="left")
        free = list(range(1, n))
        placed = []                                                        # (line, field, tokens, first line of field)
        for f in sorted(ln["fields"], key=lambda f: not all(t in ln["checks"] for t, _ in diff(c0[f], c1[f]))):
            d = diff(c0[f], c1[f])
            if all(t in ln["checks"] for t, _ in d):                       # every token restates a check: align them
                rows = [(ln["checks"].index(t) + 1, [(t, k)]) for t, k in d]
            else:                                                          # else a free line, a flipped check's first
                rows = [(sorted(free, key=lambda i: not flip[ln["checks"][i - 1]])[0], d)]
            for j, (i, toks) in enumerate(sorted(rows)):
                free.remove(i)
                placed.append((i, f, toks, j == 0))
        for i, f, toks, first in placed:
            y = ly[i]
            if first:
                mono(cv, bx0, y, f, weight="bold")
            x = X_TOK
            for t, k in toks:
                x = tok(cv, x, y, t, k, c, cw) + 0.8
            # (c) the clause of the next proposal that carries this edit, on the same line
            if hero:
                chevron(cv, gut[1], y, c["mark"])
            if f == "allow_inline":
                mono(cv, cx0, y, "scope", weight="bold")
                x = X_STK
                for t, k in diff(p0["patch"]["scope"], p1["patch"]["scope"]):
                    x = tok(cv, x, y, t, k, c, cw) + 0.8
            else:
                if first:
                    pill(cv, cx0, y, CLAUSE[f][1], role, hero)
                for t, _ in toks:
                    mono(cv, X_VAL, y, t)
        if ln["fields"]:
            ex = cv.rich(cx0, ly[0], [("cites", MUTED)], size=LS, style="italic")
            pill(cv, ex + 1.2, ly[0], ln["id"], role, hero)
        else:
            cv.text(cx0, ly[0], "no clause", style="italic", color=MUTED, ha="left")
        ytop = yb - RGAP

    # ---- closing rules and one annotation per stage ------------------------------------------
    yR3 = ytop + RGAP - 1.0
    yF = yR3 - 2.7
    for x0, x1 in stages:
        rule(cv, x0, x1, yR3, HEAVY)
    segs = []
    for g in ("improved", "regressed", "unchanged"):
        segs += [(f"{counts[g]} {g}", ROLE[GROUP_ROLE[g]]["ink"], "bold"), ("  ·  ", MUTED)]
    cv.rich(X_CASE, yF, segs[:-1], size=FS)
    cv.text(bx0, yF, "fixed rules R1–R4, one per case", size=FS, style="italic", color=MUTED, ha="left")
    cv.text(cx0, yF, "proposed only, not validated", size=FS, style="italic", color=MUTED, ha="left")

    # ---- key row: every glyph beside a sample of itself; the evidence status at the right -----
    yK = yF - 5.6
    green, coral = ROLE["memory"], ROLE["coral"]
    key_row(cv, X_CASE, yK, [
        (3.1, lambda x, y: mark(cv, x + 1.55, y, True, GREY, task=True), "task verdict"),
        (5.0, lambda x, y: (mark(cv, x + 1.0, y, True, GREY), mark(cv, x + 4.0, y, False, GREY)),
         "required check passes / fails"),
        (5.0, lambda x, y: (mark(cv, x + 1.0, y, True, green), mark(cv, x + 4.0, y, False, coral)),
         f"changed under {states[1]}"),
        (tok_w("new", "add", cw), lambda x, y: tok(cv, x, y, "new", "add", GREY, cw) and None, "token added"),
        (tok_w("old", "del", cw), lambda x, y: tok(cv, x, y, "old", "del", GREY, cw) and None, "token removed")])
    cv.text(W - M, yK + 1.5, "Constructed cases and a fixed rule system:", size=FS, style="italic", color=MUTED,
            ha="right")
    cv.text(W - M, yK - 1.5, "illustrative only, no learned model, not measured results", size=FS, style="italic",
            color=MUTED, ha="right")

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
