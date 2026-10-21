#!/usr/bin/env python3
"""Execute and render a deterministic training-replay/context-update fixture.

Run from any directory: python source/render_figure.py --out .
No model, benchmark, validation set, statistical estimator, or network is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import csv
from datetime import date
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image
import fitz

from figure_style import style_context, export_figure
from figure_scene import FigureScene
from check_figure import check_pdf

WIDTH, HEIGHT = 178.0, 158.0
INK = "#243443"
MUTED = "#596C7B"
RULE = "#C6D2DB"
BLUE = "#315F8B"
TEAL = "#176F6C"
GREEN = "#2C7458"
RUST = "#A74835"
SLATE = "#62717F"
PALES = {"improved": "#EAF5EE", "regressed": "#F9ECE6", "unchanged": "#F2F5F7"}
COLORS = {"improved": GREEN, "regressed": RUST, "unchanged": SLATE}


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fmt_num(value):
    return str(value) if isinstance(value, int) else f"{value:g}"


def short_date(value):
    item = date.fromisoformat(value)
    # Fixed English month names make the fixture independent of host locale.
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{item.day} {months[item.month - 1]}"


def execute(case, memory):
    """A deliberately small formatter; returns the actual output artifact."""
    src, kind = case["source"], case["format"]
    if kind == "scalar":
        text = fmt_num(src["value"])
        if memory["unit_mode"] == "inline_all":
            text += " " + src["unit"]
        if memory["scalar_date"]:
            text += " | " + short_date(src["date"])
        return text
    if kind == "csv":
        cell = fmt_num(src["value"])
        if memory["unit_mode"] == "inline_all":
            cell += " " + src["unit"]
        return src["field"] + "_" + src["unit"] + "\n" + cell
    if kind == "score":
        return fmt_num(src["value"])
    if kind == "range":
        # Modeled persistent limitation: the formatter drops the upper bound.
        # This is disclosed in the input contract and the figure design note.
        return fmt_num(src["lower"]) + " " + src["unit"]
    raise ValueError(f"Unknown format {kind}")


def evaluate(case, output):
    """Inspect output text against each case's explicit task contract."""
    src, kind = case["source"], case["format"]
    if kind == "scalar":
        checks = {
            "scalar.unit": output.split(" | ")[0] == fmt_num(src["value"]) + " " + src["unit"],
            "scalar.date": output.endswith(" | " + short_date(src["date"]))
        }
    elif kind == "csv":
        rows = list(csv.reader(io.StringIO(output)))
        good_shape = len(rows) == 2 and all(len(r) == 1 for r in rows)
        numeric = False
        parsed = None
        if good_shape:
            try:
                parsed = float(rows[1][0])
                numeric = True
            except ValueError:
                pass
        checks = {
            "csv.header": good_shape and rows[0][0] == src["field"] + "_" + src["unit"],
            "csv.numeric": numeric,
            "csv.value": numeric and parsed == float(src["value"])
        }
    elif kind == "score":
        checks = {"score.value": output == fmt_num(src["value"])}
    elif kind == "range":
        expected = fmt_num(src["lower"]) + "-" + fmt_num(src["upper"]) + " " + src["unit"]
        checks = {"range.end": output == expected}
    else:
        raise ValueError(kind)
    assert set(checks) == set(case["required_checks"])
    return {"checks": checks, "pass": all(checks.values())}


def replay(data):
    rows = []
    for case in data["cases"]:
        results = {}
        for state_id, memory in data["memory_states"].items():
            output = execute(case, memory)
            results[state_id] = {"output": output, **evaluate(case, output)}
        delta = int(results["M1"]["pass"]) - int(results["M0"]["pass"])
        group = "improved" if delta > 0 else "regressed" if delta < 0 else "unchanged"
        rows.append({"case_id": case["id"], "format": case["format"], "split": case["split"],
                     "states": results, "group": group})
    return rows


def reflect(before, rows):
    context = deepcopy(before)
    trace = []
    def add(field, value, case_id, rule):
        if value not in context[field]:
            context[field].append(value)
        if case_id not in context["evidence"][field]:
            context["evidence"][field].append(case_id)
        trace.append({"rule": rule, "case_id": case_id, "field": field, "action": "add", "value": value})
    for row in rows:
        old, new = row["states"]["M0"], row["states"]["M1"]
        if row["group"] == "improved" and row["format"] == "scalar":
            for field in old["checks"]:
                if not old["checks"][field] and new["checks"][field]:
                    add("retain", field, row["case_id"], "R1")
        if row["group"] == "regressed" and row["format"] == "csv" and not new["checks"]["csv.numeric"]:
            if "csv" in context["allow_inline"]:
                context["allow_inline"].remove("csv")
            context["evidence"]["allow_inline"].append(row["case_id"])
            trace.append({"rule": "R2", "case_id": row["case_id"], "field": "allow_inline", "action": "remove", "value": "csv"})
            add("protect", "csv.numeric", row["case_id"], "R2")
        if not old["pass"] and not new["pass"]:
            for field in old["checks"]:
                if not old["checks"][field] and not new["checks"][field]:
                    add("open", field, row["case_id"], "R3")
        if old["pass"] and new["pass"]:
            trace.append({"rule": "R4", "case_id": row["case_id"], "action": "no new rule"})
    return context, trace


def propose(request, context):
    return {
        "request_id": request["id"],
        "patch": {"op": request["operation"], "target": request["target"], "value": request["value"],
                  "scope": [x for x in request["formats"] if x in context["allow_inline"]]},
        "keep": deepcopy(context["retain"]),
        "guards": deepcopy(context["protect"]),
        "deferred": deepcopy(context["open"]),
        "evidence": deepcopy(context["evidence"]),
        "status": "proposed only; not applied or validated"
    }


def analyze(data):
    assert data["split"] == "training_replay"
    assert all(c["split"] == "training_replay" for c in data["cases"])
    assert len({c["id"] for c in data["cases"]}) == len(data["cases"])
    rows = replay(data)
    context, trace = reflect(data["context_before"], rows)
    result = {"evidence_status": data["evidence_status"], "split": data["split"], "replay": rows,
              "groups": {g: [r["case_id"] for r in rows if r["group"] == g]
                         for g in ["improved", "regressed", "unchanged"]},
              "counts": dict(Counter(r["group"] for r in rows)),
              "context_before": data["context_before"], "context_after": context,
              "reflection_trace": trace,
              "proposal_before": propose(data["next_request"], data["context_before"]),
              "proposal_after": propose(data["next_request"], context)}
    expected = data["expected_fixture"]
    for case, row in zip(data["cases"], rows):
        assert row["group"] == case["expected_transition"]
        for state_id, state in row["states"].items():
            assert state["output"] == expected["outputs"][case["id"]][state_id]
    assert context == expected["context_after"]
    assert result["proposal_after"]["patch"]["scope"] == ["scalar"]
    assert result["proposal_before"]["patch"]["scope"] == ["scalar", "csv"]
    assert result["proposal_after"]["guards"] == ["csv.numeric"]
    assert result["proposal_after"]["deferred"] == ["range.end"]
    return result


def memory_label(identifier, state):
    unit = "header units" if state["unit_mode"] == "header" else "inline scalar/CSV units"
    dates = "scalar date" if state["scalar_date"] else "no scalar date"
    return f"{identifier}   {unit}; {dates}"


def list_text(values):
    if not values:
        return "[]"
    if values == ["scalar.unit", "scalar.date"]:
        return "scalar: unit,date"
    return ",".join(values)


def proposal_lines(proposal):
    lines = [("INLINE [" + ",".join(proposal["patch"]["scope"]) + "]", INK, "allow_inline")]
    if proposal["guards"]:
        lines.append(("GUARD " + ",".join(proposal["guards"]), RUST, "protect"))
    if proposal["keep"]:
        lines.append(("KEEP " + list_text(proposal["keep"]).replace(": ", "."), GREEN, "retain"))
    if proposal["deferred"]:
        lines.append(("DEFER " + ",".join(proposal["deferred"]), SLATE, "open"))
    return lines


def render(data, result, out):
    with style_context(font_size=7.5):
        scene = FigureScene(WIDTH, HEIGHT)
        ax = scene.ax
        def txt(x, y, text, size=7.2, bold=False, color=INK, mono=False, ha="left", owner=None, tag=None):
            return scene.text(x, HEIGHT-y, text, size=size, weight="bold" if bold else "normal", color=color,
                              mono=mono, ha=ha, owner=owner, tag=tag)
        def rect(x, y, w, h, fill="white", stroke=None, lw=.55, radius=0):
            if radius:
                p = FancyBboxPatch((x,HEIGHT-y-h),w,h,boxstyle=f"round,pad=0,rounding_size={radius}",
                                  facecolor=fill,edgecolor=stroke or fill,linewidth=lw,zorder=0)
            else:
                p = Rectangle((x,HEIGHT-y-h),w,h,facecolor=fill,edgecolor=stroke or fill,linewidth=lw,zorder=0)
            ax.add_patch(p)
        def line(x0,y0,x1,y1,color=RULE,lw=.5):
            scene.line([(x0,HEIGHT-y0),(x1,HEIGHT-y1)], color=color,width=lw)
        def status(x,y,passed):
            color=GREEN if passed else RUST
            rect(x,y-1.6,7.9,3.2,"#EDF6EF" if passed else "#FCF0EB",color,.4,.5)
            txt(x+3.95,y,"PASS" if passed else "FAIL",7.2,True,color,ha="center")
        def case_chip(x,y,label,color=TEAL):
            rect(x,y-1.8,8.1,3.6,"white",color,.45,.5)
            txt(x+4.05,y,label,7.2,True,color,ha="center")
        def document(identifier,x,y,w,h,role="consolidation",fill="white"):
            scene.node(identifier,x,HEIGHT-y-h,w,h,role=role,shape="document",fill=fill)

        txt(4,5.5,data["title"],10.5,True)
        txt(174,5.5,"ILLUSTRATIVE RULE SYSTEM",7.2,True,TEAL,ha="right")
        txt(4,12.1,"Training replay only. A fixed formatter and fixed reflection rules; no learned-model result.",7.2,color=MUTED)
        line(4,16.5,174,16.5)
        txt(4,21.8,"a",9.5,True)
        txt(10,21.8,"Replay matched cases; classify the change in task verdict",9.0,True)
        rect(4,27.2,80.8,9.0,"#F2F5F8",RULE,.5,.7)
        rect(88,27.2,86,9.0,"#EAF2F9",BLUE,.5,.7)
        txt(7,31.7,memory_label("M0",data["memory_states"]["M0"]),7.2,True,SLATE)
        txt(91,31.7,memory_label("M1",data["memory_states"]["M1"]),7.2,True,BLUE)

        columns=[4,59,95,136,174]
        rect(4,40,170,7,"#F2F5F7")
        for x,text in [(6,"Case and required contract"),(61,"M0 output"),(97,"M1 output"),(139,"Verdict change")]:
            txt(x,43.4,text,7.5,True)
        row_h=11.6
        for index,(case,row) in enumerate(zip(data["cases"],result["replay"])):
            top=47+index*row_h
            rect(4,top,170,row_h,PALES[row["group"]])
            rect(4,top,1.0,row_h,COLORS[row["group"]])
            line(5,top+row_h,174,top+row_h,color="white",lw=.8)
            txt(7,top+3.9,case["id"],7.5,True,COLORS[row["group"]])
            source=case["source"]
            if case["format"]=="scalar":
                contract="scalar: unit + source date"
                excerpt=f"source: {fmt_num(source['value'])} {source['unit']}, {short_date(source['date'])}"
            elif case["format"]=="csv":
                contract="CSV: numeric cell"
                excerpt=f"header: {source['field']}_{source['unit']}"
            elif case["format"]=="score":
                contract="score: preserve value"
                excerpt="source: " + fmt_num(source["value"])
            else:
                contract="range: keep both endpoints"
                excerpt=f"source: {source['lower']}-{source['upper']} {source['unit']}"
            txt(18,top+3.9,contract,7.2)
            txt(18,top+8.0,excerpt,7.2,color=MUTED)
            for state_id,left,status_x in [("M0",61,84.5),("M1",97,126)]:
                output=row["states"][state_id]["output"]
                for j,text in enumerate(output.splitlines()):
                    txt(left,top+(3.8 if "\n" in output else 5.8)+j*3.8,text,7.2,mono=True)
                status(status_x,top+5.8,row["states"][state_id]["pass"])
            txt(139,top+4.2,row["group"].capitalize(),7.6,True,COLORS[row["group"]])
            before="pass" if row["states"]["M0"]["pass"] else "fail"
            after="pass" if row["states"]["M1"]["pass"] else "fail"
            txt(139,top+8.2,before+" → "+after,7.2,color=MUTED)
        for x in columns[1:-1]:
            line(x,40,x,93.4,color="white",lw=1)
        counts=result["counts"]
        txt(4,97.6,"Derived groups: "+" · ".join(f"{counts.get(g,0)} {g}" for g in ["improved","regressed","unchanged"]),7.5,True)
        txt(174,97.6,"PASS requires every listed contract check.",7.2,color=MUTED,ha="right")
        line(4,102,174,102)

        txt(4,107.1,"b",9.5,True)
        txt(10,107.1,"Update the context: C0 → C1",8.8,True)
        txt(109,107.1,"c",9.5,True)
        txt(115,107.1,"The same next request",8.8,True)
        txt(4,112.4,"Keep gains; guard regressions; carry failures.",7.2,color=MUTED)
        requested=data["next_request"]
        txt(109,112.4,requested["id"]+": “add inline units”",7.2,color=MUTED)

        document("context_diff",4,116.0,100,33.0,fill="#F7FBFA")
        fields=[("allow_inline",RUST),("retain",GREEN),("protect",RUST),("open",SLATE)]
        for i,(field,color) in enumerate(fields):
            cy=120.4+i*8.0
            if i: line(6,cy-4.1,102,cy-4.1)
            txt(6,cy,field,7.2,True,mono=True,owner="context_diff")
            txt(29.5,cy,list_text(result["context_before"][field]),7.2,mono=True,color=MUTED,owner="context_diff")
            txt(51,cy,"→",7.2,color=MUTED,ha="center",owner="context_diff")
            txt(55,cy,list_text(result["context_after"][field]),7.2,mono=True,color=color,owner="context_diff")
            evidence=result["context_after"]["evidence"][field]
            case_chip(94.1,cy,",".join(evidence),color)

        document("proposal_C0",109,116,65,9.8,role="neutral",fill="#F6F7F9")
        txt(111,120.8,"C0",7.2,True,color=SLATE,owner="proposal_C0")
        before_lines=proposal_lines(result["proposal_before"])
        for j,(text,color,field) in enumerate(before_lines):
            txt(119,120.8+j*3.8,text,7.2,mono=True,color=color,owner="proposal_C0")
        document("proposal_C1",109,128.0,65,21.0,role="consolidation",fill="#EDF7F4")
        txt(111,132.2,"C1",7.2,True,color=TEAL,owner="proposal_C1")
        after_lines=proposal_lines(result["proposal_after"])
        for j,(text,color,field) in enumerate(after_lines):
            txt(119,132.2+j*4.0,text,7.2,mono=True,color=color,owner="proposal_C1")

        txt(4,154,"Executed illustration; proposals are neither committed nor validated. No test cases enter the update.",7.2,color=MUTED)
        scene.correspondences=[
            {"source":"replay."+r["case_id"],"target":"context_after."+t["field"],"rule":t["rule"]}
            for r in result["replay"] for t in result["reflection_trace"]
            if t.get("case_id")==r["case_id"] and "field" in t]
        audit=scene.audit(out/"qa/geometry_checks.json")
        scene.write_spec(out/"scene.json")
        if audit["text_findings"] or audit["route_report"].get("issues"):
            print(json.dumps(audit,indent=2))
            raise RuntimeError("Resolve text/geometry findings before export")
        metadata={"evidence_status":data["evidence_status"],"physical_dimensions_mm":[WIDTH,HEIGHT],
                  "minimum_type_pt":7.2,"split":"training_replay","claim":"Derived replay groups change proposer context and the next proposal scope",
                  "fonts":{k:font_manager.findfont(font_manager.FontProperties(family=family,weight=weight),fallback_to_default=False)
                           for k,family,weight in [("regular","DejaVu Sans","normal"),("bold","DejaVu Sans","bold"),("mono","DejaVu Sans Mono","normal"),("mono_bold","DejaVu Sans Mono","bold")]}}
        source_files=[Path(__file__),ROOT/"inputs/epoch_fixture.json"]
        source_files.extend(ROOT/"source"/name for name in ["figure_style.py","figure_scene.py","diagram_geometry.py","check_figure.py"])
        paths=export_figure(scene.fig,out/"epoch_context_update",source_files=source_files,metadata=metadata)
        plt.close(scene.fig)
    return paths


def write_notes(data, result, out):
    n=len(result["replay"])
    counts=result["counts"]
    caption=("**Epoch replay changes the next proposal (deterministic illustration).** "
             f"(a) The same {n} constructed training cases are executed under M0 and M1; a task passes only when every required check passes. "
             f"The resulting groups are {counts['improved']} improved, {counts['regressed']} regressed, and {counts['unchanged']} unchanged. "
             "(b) Fixed reflection rules preserve scalar unit/date behavior, protect numeric CSV cells, and retain an unresolved range issue, with source case IDs. "
             "(c) The same request yields a narrower proposal under C1. Both proposals remain unapplied and unvalidated. "
             "The formatter, outcomes, context update, and proposals are executable fixtures; no learned model, held-out validation, test result, or real-agent performance is represented.\n")
    (out/"caption.md").write_text(caption,encoding="utf-8")
    alt=("Three-panel training-only illustration of epoch reflection. "
         "A table compares four identical inputs under M0, which puts units in headers and omits scalar dates, and M1, which applies inline units to scalar and CSV outputs and adds scalar dates. "
         "T08 changes from a bare scalar to a unit-and-date answer and passes. T11's numeric CSV cell acquires a unit suffix and fails. "
         "T03 remains a correct unitless score, while T14 still drops a range endpoint. "
         "A context diff cites these cases: inline edits are restricted to scalar format, scalar unit/date requirements are kept, numeric CSV cells are protected, and the range issue remains open. "
         "For the same next request, C0 proposes inline units for scalar and CSV outputs; C1 proposes only scalar inline units and includes the kept requirements, CSV guard, and deferred issue. "
         "All outcomes are deterministic constructed examples; the proposal is not applied or validated.\n")
    (out/"alt_text.txt").write_text(alt,encoding="utf-8")
    brief={"claim":"A slower replay process updates the constraints of the next proposal rather than the execution-model weights.",
           "claim_bearing_operation":{"input":"same training case IDs replayed under M0/M1",
           "operation":"fixed R1-R4 reflection rules on requirement/verdict deltas",
           "output":"C1 actual fields and evidence IDs",
           "consequence":"P04 has narrower scope, protected/retained contracts, and an unresolved issue"},
           "panels":{"a":"inspect matched output artifacts and derived groups","b":"inspect the before/after context fields","c":"inspect the same request under both contexts"},
           "evidence_status":data["evidence_status"],"selection_rule":data["selection_rule"],
           "physical_dimensions_mm":[WIDTH,HEIGHT],"minimum_font_pt":7.2,
           "reference_jobs":{"IdeaScientist Figure 1":"connect a system story to actual structured artifacts and a worked instance",
                             "SkillOpt Figure 2":"replay matched cases at an epoch timescale before updating optimizer context"},
           "key_limit":"Training replay improves and regresses under the constructed policies. Nothing is committed or validated; context generation is a disclosed deterministic rule.",
           "display_aliases":{"scalar: unit,date":["scalar.unit","scalar.date"],"INLINE":"REPLACE unit_placement := inline","KEEP":"retain requirements","GUARD":"protected output contracts","DEFER":"unresolved issues"}}
    dump(out/"figure_brief.json",brief)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,default=ROOT)
    args=p.parse_args()
    out=args.out.resolve(); out.mkdir(parents=True,exist_ok=True); (out/"qa").mkdir(exist_ok=True)
    data=json.loads((ROOT/"inputs/epoch_fixture.json").read_text())
    result=analyze(data)
    dump(out/"analysis.json",result)
    dump(out/"qa/numerical_checks.json",{
        "passed":True,"checks":["same fixed case/source objects under both policies","all cases are training replay","outputs match independent expected fixture strings",
        "contract checks derive task verdicts","verdict deltas derive groups","R1-R4 derive exact expected context fields/evidence IDs","proposal generator uses both contexts with the same request",
        "guarded scope excludes CSV","unresolved interval issue survives into next proposal","no proposal is executed or labeled validated"],
        "group_counts":result["counts"],"source_sha256":hashlib.sha256((ROOT/"inputs/epoch_fixture.json").read_bytes()).hexdigest(),
        "limitations":"Deterministic correctness checks for this fixture; no statistical inference or real-model evaluation."})
    write_notes(data,result,out)
    paths=render(data,result,out)
    report=check_pdf(Path(paths["pdf"]),expected_width_mm=178,min_font_pt=7.2)
    dump(out/"qa/pdf_checks.json",report)
    if not report["automated_checks_passed"]: raise RuntimeError("PDF checks failed")
    with fitz.open(paths["pdf"]) as doc:
        page=doc[0]
        page.get_pixmap(matrix=fitz.Matrix(180/72,180/72),alpha=False).save(out/"qa/pdf_render_180dpi.png")
        page.get_pixmap(matrix=fitz.Matrix(96/72,96/72),alpha=False).save(out/"qa/final_size_96dpi.png")
        span_sizes=[s["size"] for b in page.get_text("dict")["blocks"] for l in b.get("lines",[]) for s in l.get("spans",[]) if s.get("text","").strip()]
        raster_count=len(page.get_images())
    Image.open(out/"qa/pdf_render_180dpi.png").convert("L").save(out/"qa/grayscale.png")
    svg=ET.parse(paths["svg"]).getroot()
    editable_text=len(svg.findall(".//{http://www.w3.org/2000/svg}text"))
    dump(out/"qa/export_checks.json",{"passed":True,"dimensions_mm":[WIDTH,HEIGHT],"minimum_text_pt":min(span_sizes),
        "pdf_raster_objects":raster_count,"svg_editable_text_nodes":editable_text,"pdf_fonts_embedded":all(f["embedded"] for f in report["fonts"]),
        "visual_review":"See visual_review.md; export checks alone do not certify composition."})
    dump(out/"environment.json",{"python":sys.version,"platform":platform.platform(),"matplotlib":matplotlib.__version__,"pymupdf":fitz.VersionBind})
    print(json.dumps({"outputs":paths,"groups":result["counts"],"dimensions_mm":[WIDTH,HEIGHT]},indent=2))


if __name__=="__main__":
    main()
