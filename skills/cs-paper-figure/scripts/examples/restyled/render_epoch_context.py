"""Restyle of the epoch-context example: matched replay -> outcome groups -> context C0->C1 -> next proposal.

Every case, output string, verdict, context field, evidence ID and proposal field is read from
analysis.json / epoch_fixture.json and asserted below; nothing is typed in by hand except
display labels. Status (deterministic illustrative rule system, nothing applied or validated)
lives in the caption, not in the art.

    python render_epoch_context.py --out <dir>
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle  # noqa: E402
from paperkit import Canvas, ROLE, INK, MUTED, LINE  # noqa: E402

OLD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "epoch-context")
W, H = 178, 106
MONO = "DejaVu Sans Mono"   # bundled with matplotlib: literal output strings / field values only
GR = {"improved": ROLE["memory"], "regressed": ROLE["coral"],
      "unchanged": dict(ROLE["neutral"], mark="#5E6875")}
CTX, PRO = ROLE["purple"], ROLE["amber"]
MS = 6.0     # mono size
SS = 6.3     # small serif size


# ------------------------------------------------------------------ helpers ---
def mw(cv, s, size=MS):
    t = cv.ax.text(0, 0, s, fontsize=size, family=MONO)
    bb = t.get_window_extent(cv._renderer())
    t.remove()
    return bb.width / cv.fig.dpi * 25.4


def mono(cv, x, y, s, color=INK, size=MS, ha="left", **kw):
    return cv.text(x, y, s, size=size, color=color, ha=ha, family=MONO, **kw)


def card(cv, x, y, w, h, r, title):
    cv.group(x, y, w, h, r, title, band=True, size=7.6, radius=2.0, lw=0.7, fill="white")


def folded(cv, x, y, w, h, r, title, lw=0.6, fill="white", shadow=False, f=2.6):
    c = r
    pts = [(x, y), (x + w, y), (x + w, y + h - f), (x + w - f, y + h), (x, y + h)]
    if shadow:
        cv.ax.add_patch(Polygon([(px + 0.45, py - 0.45) for px, py in pts], fc="#1A2230", alpha=0.10,
                                ec="none", zorder=4.8))
    cv.ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=c["stroke"], lw=lw, zorder=5, joinstyle="round"))
    cv.ax.add_patch(Polygon([(x + w - f, y + h), (x + w - f, y + h - f), (x + w, y + h - f)], closed=True,
                            fc=c["soft"], ec=c["stroke"], lw=lw * 0.8, zorder=5.1))
    cv.text(x + 1.6, y + h - 2.3, title[0], size=7.0, weight="bold", color=c["ink"], ha="left", z=7)
    if len(title) > 1:
        dx = cv.text_width(title[0], 7.0, "bold") + 1.2
        cv.text(x + 1.6 + dx, y + h - 2.3, title[1], size=SS, color=c["ink"], ha="left", z=7, style="italic")


def verdict(cv, x, y, ok):
    """PASS / FAIL chips stay neutral so that hue is reserved for outcome groups."""
    if ok:
        return cv.chip(x, y, "PASS", dict(ROLE["neutral"], soft="white", stroke="#8C95A1", ink=INK),
                       size=6.0, ha="right", h=3.1, pad=0.8, z=9)
    return cv.chip(x, y, "FAIL", dict(ROLE["neutral"], mark="#3A4250", stroke="#3A4250"),
                   size=6.0, ha="right", h=3.1, pad=0.8, solid=True, z=9)


def opchip(cv, x, y, op, r):
    """ADD solid / DEL outlined / REP outlined pill in the document's role colour."""
    return cv.chip(x, y, op, r, size=6.0, h=2.9, pad=0.6, solid=(op == "ADD"), ha="left", z=9)


def values(cv, x, y, items, struck=(), color=INK, strike=LINE):
    """Mono list 'a, b, c'; struck items get a strike-through. Returns end x."""
    if not items:
        mono(cv, x, y, "[]", color=MUTED)
        return x + mw(cv, "[]")
    cx = x
    for i, it in enumerate(items):
        s = it + (", " if i < len(items) - 1 else "")
        mono(cv, cx, y, s, color=MUTED if it in struck else color)
        if it in struck:
            ww = mw(cv, it)
            cv.ax.plot([cx - 0.2, cx + ww + 0.2], [y, y], color=strike, lw=0.75, zorder=22)
        cx += mw(cv, s)
    return cx


def field(cv, x, yc, w, name, items, *, op=None, ev=None, g=None, struck=(), r=CTX, h=7.0,
          strike=None):
    """Two-line document row: italic key + op chip + evidence ID, then mono values.
    Row tint = outcome group of the evidence case (cause shown on the effect)."""
    if g:
        cv.ax.add_patch(FancyBboxPatch((x + 0.8, yc - h / 2), w - 1.6, h, boxstyle="round,pad=0,rounding_size=0.8",
                                       fc=GR[g]["fill"], ec=GR[g]["soft"], lw=0.5, zorder=5.5))
    y1, y2 = yc + 1.55, yc - 1.75
    cv.text(x + 1.8, y1, name, size=SS, style="italic", color=r["ink"], ha="left")
    if op:
        opchip(cv, x + 2.6 + cv.text_width(name, SS), y1, op, r)
    if ev:
        cv.text(x + w - 1.8, y1, ev, size=SS, weight="bold", color=GR[g]["ink"], ha="right")
    values(cv, x + 1.8, y2, items, struck, strike=strike or (GR[g]["mark"] if g else LINE))


# ------------------------------------------------------------------- panels ---
COL = dict(id=(4.6, 21.5), m0=(22.5, 45.4), m1=(47.0, 74.3))


def case_card(cv, y, h, rec, src, g):
    x0, x1 = 4.6, 75.6
    c = GR[g]
    cv.ax.add_patch(FancyBboxPatch((x0, y), x1 - x0, h, boxstyle="round,pad=0,rounding_size=1.3",
                                   fc="white", ec=c["stroke"], lw=0.6, zorder=5))
    cv.ax.add_patch(Rectangle((x0 + 0.05, y + 1.3), 0.9, h - 2.6, fc=c["mark"], ec="none", zorder=5.2))
    cv.text(x0 + 2.2, y + h - 3.4, rec["case_id"], size=7.2, weight="bold", color=c["ink"], ha="left")
    cv.text(x0 + 2.2 + cv.text_width(rec["case_id"], 7.2, "bold") + 1.0, y + h - 3.4, rec["format"], size=SS,
            color=c["ink"], ha="left", style="italic")
    cv.text(x0 + 2.2, y + 3.4, src, size=6.0, color=MUTED, ha="left")
    for st, (a, b) in (("M0", COL["m0"]), ("M1", COL["m1"])):
        s = rec["states"][st]
        lines = s["output"].split("\n")
        tw = max(mw(cv, ln) for ln in lines)
        lh = 2.55
        yc = y + h / 2 + 1.0
        top = yc + (len(lines) - 1) * lh / 2
        bh = len(lines) * lh + 1.3
        cv.ax.add_patch(FancyBboxPatch((a, yc - bh / 2), tw + 2.0, bh, boxstyle="round,pad=0,rounding_size=0.7",
                                       fc="#F2F3F6", ec="#DADDE3", lw=0.4, zorder=6))
        for i, ln in enumerate(lines):
            mono(cv, a + 1.0, top - i * lh, ln)
        verdict(cv, b, yc, s["pass"])
        failed = [k.split(".", 1)[1] for k, v in s["checks"].items() if not v]
        if failed:
            cv.text(b, y + 2.2, "fails " + ", ".join(failed), size=6.0, style="italic",
                    color=MUTED, ha="right")
    return (x1, y + h / 2)


def panel_a(cv, A, F):
    card(cv, 2, 2, 76, 102, "neutral", "(a) Matched replay, M0 vs M1")
    ms = F["memory_states"]
    assert ms["M0"] == {"unit_mode": "header", "scalar_date": False}
    assert ms["M1"] == {"unit_mode": "inline_all", "scalar_date": True}
    heads = (("M0", "units in header, no date", COL["m0"]), ("M1", "units inline, scalar date", COL["m1"]))
    cv.text(COL["id"][0] + 0.6, 94.6, "case", size=7.0, weight="bold", color=INK, ha="left")
    cv.text(COL["id"][0] + 0.6, 91.6, "source", size=6.0, color=MUTED, ha="left")
    for k, sub, (a, b) in heads:
        cv.text(a + 0.2, 94.6, k, size=7.0, weight="bold", color=INK, ha="left")
        cv.text(a + 0.2, 91.6, sub, size=6.0, color=MUTED, ha="left")
    src = {c["id"]: c["source"] for c in F["cases"]}
    fmt_src = {"T08": "{value} {unit}, {date}", "T11": "{field}: {value} {unit}", "T03": "{value}",
               "T14": "{lower}–{upper} {unit}"}
    recs = {r["case_id"]: r for r in A["replay"]}
    grp = {cid: g for g, ids in A["groups"].items() for cid in ids}
    ends = {}
    ch = 14.0
    yt = 88.0
    pill = {"improved": "fail → pass", "regressed": "pass → fail", "unchanged": "no verdict change"}
    for g in ("improved", "regressed", "unchanged"):
        ids = A["groups"][g]
        n = len(ids)
        rh = 4.0 + n * ch + (n - 1) * 2.0 + 1.6
        y0 = yt - rh
        c = GR[g]
        cv.ax.add_patch(FancyBboxPatch((3.4, y0), 73.4, rh, boxstyle="round,pad=0,rounding_size=1.8",
                                       fc=c["fill"], ec=c["stroke"], lw=0.55, ls=(0, (3, 1.8)), zorder=2))
        x0, w = cv.chip(5.2, yt, f"{g} ×{A['counts'][g]}", dict(c, mark=c["mark"]), size=6.4, h=3.3,
                        pad=1.0, solid=True, ha="left", z=9)
        cv.text(x0 + w + 1.2, yt - 0.05, pill[g], size=6.0, style="italic", color=c["ink"], ha="left",
                bbox=dict(fc=c["fill"], ec="none", pad=0.6))
        cy = yt - 4.0 - ch
        for cid in ids:
            assert grp[cid] == g
            ends[cid] = case_card(cv, cy, ch, recs[cid], fmt_src[cid].format(**src[cid]), g)
            cy -= ch + 2.0
        yt = y0 - 3.4
    return ends


CX0, CW = 90.5, 38.5       # context docs
PX0, PW = 135.0, 39.5      # proposal docs


def panel_b(cv, A, ends):
    card(cv, 80.5, 2, 50.5, 102, "purple", "(b) Context update, C0 \u2192 C1")
    before, after = A["context_before"], A["context_after"]
    # C0: compact one-line rows
    y0, h0 = 71.0, 21.0
    folded(cv, CX0, y0, CW, h0, CTX, ("C0", "before replay"))
    order = ["retain", "allow_inline", "protect", "open"]
    for i, k in enumerate(order):
        yy = y0 + h0 - 7.0 - i * 3.6
        cv.text(CX0 + 1.8, yy, k, size=SS, style="italic", color=CTX["ink"], ha="left")
        values(cv, CX0 + 17.5, yy, before[k])
    # C1 (hero): diff rows; derive op / evidence / group from the reflection trace
    trace = {}
    for t in A["reflection_trace"]:
        if "field" in t:
            trace.setdefault(t["field"], []).append(t)
    grp = {cid: g for g, ids in A["groups"].items() for cid in ids}
    y1, h1 = 6.0, 60.0
    folded(cv, CX0, y1, CW, h1, CTX, ("C1", "after replay"), lw=1.0, shadow=True)
    rows_y = {"retain": 56.0, "allow_inline": 47.0, "protect": 38.0, "open": ends["T14"][1]}
    rule_of = {}
    for k in order:
        ts = trace[k]
        ev = after["evidence"][k]
        assert len(ev) == 1 and all(t["case_id"] == ev[0] for t in ts), (k, ev, ts)
        acts = {t["action"] for t in ts}
        assert len(acts) == 1
        op = {"add": "ADD", "remove": "DEL"}[acts.pop()]
        if op == "ADD":
            assert sorted(before[k] + [t["value"] for t in ts]) == sorted(after[k])
            items, struck = after[k], ()
        else:
            gone = [t["value"] for t in ts]
            assert [v for v in before[k] if v not in gone] == after[k]
            items, struck = before[k], gone
        field(cv, CX0, rows_y[k], CW, k, items, op=op, ev=ev[0], g=grp[ev[0]], struck=struck)
        rule_of.setdefault(ev[0], set()).add(ts[0]["rule"])
    # replay -> context arrows, coloured by outcome group, rule chip on each
    xr = 85.2
    lanes = {"T08": 78.9, "T11": 79.7, "T14": 79.7}
    targets = {"T08": ["retain"], "T11": ["allow_inline", "protect"], "T14": ["open"]}
    for cid, fields in targets.items():
        (xe, ye), g = ends[cid], grp[cid]
        col = GR[g]["mark"]
        xl = lanes[cid]
        (rule,) = rule_of[cid]
        for j, fk in enumerate(fields):
            yt = rows_y[fk]
            pts = [(xe, ye), (CX0, yt)] if abs(ye - yt) < 0.05 else [(xe, ye), (xl, ye), (xl, yt), (CX0, yt)]
            cv.arrow(pts, color=col, lw=0.85, head=1.3, radius=1.0)
        if len(fields) > 1:
            cv.dot(xl, rows_y[fields[0]], color=col, d=0.9)
        cv.chip(xr + 1.3, rows_y[fields[0]], rule, dict(GR[g]), size=6.0, h=2.9, pad=0.6, z=10)
        if len(fields) > 1:
            cv.chip(xr + 1.3, rows_y[fields[1]], rule, dict(GR[g]), size=6.0, h=2.9, pad=0.6, z=10)
    # T03: stable pass -> R4, no new rule
    no_rule = [t for t in A["reflection_trace"] if t["action"] == "no new rule"]
    assert [t["case_id"] for t in no_rule] == ["T03"]
    (xe, ye) = ends["T03"]
    cv.line([(xe, ye), (CX0 - 0.9, ye)], color=GR["unchanged"]["mark"], lw=0.7)
    cv.ax.plot([CX0 - 0.9] * 2, [ye - 1.1, ye + 1.1], color=GR["unchanged"]["mark"], lw=0.9, zorder=8)
    cv.chip(xr + 1.3, ye, no_rule[0]["rule"], dict(GR["unchanged"]), size=6.0, h=2.9, pad=0.6, z=10)
    cv.ax.add_patch(FancyBboxPatch((CX0 + 0.8, ye - 2.5), CW - 1.6, 5.0, boxstyle="round,pad=0,rounding_size=0.8",
                                   fc="white", ec=GR["unchanged"]["stroke"], lw=0.5, ls=(0, (2.2, 1.4)), zorder=5.5))
    cv.text(CX0 + 1.8, ye, "no new rule", size=SS, style="italic", color=MUTED, ha="left")
    cv.text(CX0 + CW - 1.8, ye, "T03", size=SS, weight="bold", color=GR["unchanged"]["ink"], ha="right")
    # C0 -> C1
    cv.arrow([(CX0 + CW / 2, y0), (CX0 + CW / 2, y1 + h1)], color=CTX["mark"], lw=0.9, head=1.4)
    return 78.0, rows_y


def panel_c(cv, A, F, yc0, rows_y):
    card(cv, 133.5, 2, 42.5, 102, "amber", "(c) Next proposal")
    req = F["next_request"]
    pb, pa = A["proposal_before"], A["proposal_after"]
    for p in (pb, pa):
        assert p["request_id"] == req["id"] and p["patch"]["op"] == req["operation"]
        assert p["patch"]["target"] == req["target"] and p["patch"]["value"] == req["value"]
    # request (input, neutral)
    ry, rh = 88.6, 9.6
    cv.ax.add_patch(FancyBboxPatch((PX0, ry), PW, rh, boxstyle="round,pad=0,rounding_size=1.2",
                                   fc=ROLE["neutral"]["fill"], ec=ROLE["neutral"]["stroke"], lw=0.6, zorder=5))
    cv.text(PX0 + 1.6, ry + rh - 2.2, f"request {req['id']}", size=7.0, weight="bold", color=INK, ha="left")
    opchip(cv, PX0 + 1.4, ry + 4.3, "REP", ROLE["neutral"])
    mono(cv, PX0 + 7.6, ry + 4.3, f"{req['target']} := {req['value']}")
    cv.text(PX0 + 1.6, ry + 1.6, "formats", size=SS, style="italic", color=MUTED, ha="left")
    values(cv, PX0 + 11.0, ry + 1.6, req["formats"])
    # proposal under C0
    y0, h0 = 70.5, 15.5
    folded(cv, PX0, y0, PW, h0, PRO, (f"{pb['request_id']}", "under C0"))
    yy = y0 + h0 - 6.0
    opchip(cv, PX0 + 1.4, yy, "REP", PRO)
    mono(cv, PX0 + 7.6, yy, f"{pb['patch']['target']} := {pb['patch']['value']}")
    cv.text(PX0 + 1.8, yy - 3.5, "scope", size=SS, style="italic", color=PRO["ink"], ha="left")
    values(cv, PX0 + 11.0, yy - 3.5, pb["patch"]["scope"])
    assert pb["keep"] == pb["guards"] == pb["deferred"] == []
    cv.text(PX0 + 1.8, yy - 7.0, "keep, guards, deferred", size=SS, style="italic", color=PRO["ink"], ha="left")
    mono(cv, PX0 + 1.8 + cv.text_width("keep, guards, deferred", SS) + 1.5, yy - 7.0, "[]", color=MUTED)
    # proposal under C1 (diff vs C0)
    y1, h1 = 6.0, 62.5
    folded(cv, PX0, y1, PW, h1, PRO, (f"{pa['request_id']}", "under C1"), lw=0.8)
    yy = y1 + h1 - 6.2
    assert pa["patch"]["target"] == pb["patch"]["target"]
    opchip(cv, PX0 + 1.4, yy, "REP", PRO)
    mono(cv, PX0 + 7.6, yy, f"{pa['patch']['target']} := {pa['patch']['value']}")
    grp = {cid: g for g, ids in A["groups"].items() for cid in ids}
    ev = pa["evidence"]
    gone = [s for s in pb["patch"]["scope"] if s not in pa["patch"]["scope"]]
    assert pa["patch"]["scope"] == [s for s in req["formats"] if s in A["context_after"]["allow_inline"]]
    rows = [("keep", pa["keep"], "ADD", ev["retain"][0], (), "retain"),
            ("scope", pb["patch"]["scope"], "DEL", ev["allow_inline"][0], gone, "allow_inline"),
            ("guards", pa["guards"], "ADD", ev["protect"][0], (), "protect"),
            ("deferred", pa["deferred"], "ADD", ev["open"][0], (), "open")]
    assert pa["keep"] == A["context_after"]["retain"] and pa["guards"] == A["context_after"]["protect"]
    assert pa["deferred"] == A["context_after"]["open"]
    for name, items, op, e, struck, ck in rows:   # each row level with its C1 source row
        yr = rows_y[ck]
        field(cv, PX0, yr, PW, name, items, op=op, ev=e, g=grp[e], struck=struck, r=PRO, h=6.9)
    # context -> proposal (purple: path carries a context)
    cv.arrow([(CX0 + CW, yc0), (PX0 - 0.0, yc0)], color=CTX["mark"], lw=0.9, head=1.4)
    yl = 26.0
    cv.arrow([(CX0 + CW, yl), (PX0, yl)], color=CTX["mark"], lw=0.9, head=1.4)
    # same request feeds both proposals: corridor on the right edge
    xr = PX0 + PW - 5.0
    cv.arrow([(xr, ry), (xr, y0 + h0)], color=LINE, lw=0.7, head=1.2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default=os.path.join(OLD, "inputs", "epoch_fixture.json"))
    ap.add_argument("--analysis", default=os.path.join(OLD, "analysis.json"))
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    A = json.load(open(a.analysis))
    F = json.load(open(a.fixture))
    # ---- facts the art depends on ------------------------------------------
    exp = F["expected_fixture"]
    for r in A["replay"]:
        for st in ("M0", "M1"):
            s = r["states"][st]
            assert s["output"] == exp["outputs"][r["case_id"]][st]
            assert s["pass"] == all(s["checks"].values())
        p0, p1 = r["states"]["M0"]["pass"], r["states"]["M1"]["pass"]
        g = "improved" if (not p0 and p1) else "regressed" if (p0 and not p1) else "unchanged"
        assert r["group"] == g, r["case_id"]
    assert A["counts"] == {"improved": 1, "regressed": 1, "unchanged": 2}
    assert {k: len(v) for k, v in A["groups"].items()} == A["counts"]
    assert A["context_after"] == exp["context_after"]
    assert A["context_before"] == F["context_before"]
    assert A["proposal_before"]["patch"]["scope"] == ["scalar", "csv"]
    assert A["proposal_after"]["patch"]["scope"] == ["scalar"]
    cv = Canvas(W, H, family="serif", size=7.0)
    ends = panel_a(cv, A, F)
    yc0, rows_y = panel_b(cv, A, ends)
    panel_c(cv, A, F, yc0, rows_y)
    print("\n".join(cv.save(os.path.join(a.out, "epoch_context_update"))))


if __name__ == "__main__":
    main()
