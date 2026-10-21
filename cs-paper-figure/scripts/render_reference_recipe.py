#!/usr/bin/env python3
"""Render an original evidence-to-state mechanism figure with explicit topology.

This is a schematic illustration, not a proposed or evaluated research method.
The original composition applies three studied principles: diagram/code semantic
bindings (AlphaEvolve Fig. 2), typed objects and a reserved return corridor (SAM 3
Fig. 4), and muted context with a local changed region (Circuit Tracing).
No source artwork, system architecture, or empirical results are reproduced.

Run: python render_reference_recipe.py --out /path/to/figures
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from matplotlib.path import Path as MplPath

from diagram_geometry import Node, Rect, Port, Route, Label, port_point, validate_diagram
from figure_style import export_figure, style_context
from render_modern_examples import select_fonts


COLORS = {
    "ink": "#25333F", "muted": "#586571", "line": "#A6B1B9",
    "context": "#F5F7F8", "blue": "#315F8E", "blue_fill": "#E8F0F8",
    "purple": "#74549B", "purple_fill": "#F0EAF7",
    "green": "#47795A", "green_fill": "#EAF3EC",
    "amber": "#9C5C20", "amber_fill": "#FBEACF",
    "old_fill": "#F6F0E5", "white": "#FFFFFF",
}


def render(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    fonts = select_fonts()
    W, H = 178.0, 140.0
    with style_context(8), mpl.rc_context({"font.family": fonts[0], "font.weight": "normal"}):
        fig = plt.figure(figsize=(W / 25.4, H / 25.4))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set(xlim=(0, W), ylim=(0, H)); ax.axis("off")
        text_artists = []

        def xy(x, y):
            return x, H - y

        def text(x, y, value, size=8, color="ink", weight="normal", ha="left", mono=False):
            artist = ax.text(*xy(x, y), value, ha=ha, va="center", fontsize=size,
                             color=COLORS.get(color, color), fontweight=weight,
                             fontfamily=fonts[1] if mono else fonts[0], zorder=8)
            text_artists.append(artist)
            return artist

        def box(x, y, w, h, fill="white", edge="line", lw=.65, radius=1.4):
            patch = FancyBboxPatch((x, H-y-h), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={radius}",
                                  facecolor=COLORS.get(fill, fill),
                                  edgecolor=COLORS.get(edge, edge), linewidth=lw, zorder=2)
            ax.add_patch(patch)
            return patch

        def rect(x, y, w, h):
            return Rect(x, H-y-h, x+w, H-y)

        def section(x, y, letter, title):
            text(x, y, letter, 9.5, weight="bold")
            text(x+5.2, y, title, 9.3, weight="bold")

        text(5, 7, "A verified edit changes one payload field", 11.2, weight="bold")
        text(173, 7, "SCHEMATIC", 7.3, "muted", ha="right")
        section(5, 18, "a", "Evidence and control")
        section(71, 18, "b", "Inspect the exact state change")
        box(5, 23, 55, 88, "context", "context", lw=0, radius=2)

        # A folded document has the same rectangular painted extent registered
        # below; its top-right fold is not used as an arrow port.
        x, y, w, h, fold = 11, 29, 43, 17, 3
        vertices = [(x,y), (x+w-fold,y), (x+w,y+fold), (x+w,y+h), (x,y+h)]
        ax.add_patch(Polygon([xy(a,b) for a,b in vertices], closed=True,
                             facecolor=COLORS["blue_fill"], edgecolor=COLORS["blue"], lw=.8, zorder=3))
        ax.plot([x+w-fold,x+w-fold,x+w], [H-y,H-y-fold,H-y-fold], color=COLORS["blue"], lw=.65, zorder=4)
        text(15, 34, "Evidence e12", 8.4, "blue", "bold")
        text(15, 40.8, "timeout = 45 s", 8.0, "ink", mono=True)

        box(11, 55, 43, 14, "purple_fill", "purple", .8)
        text(32.5, 59.6, "Propose patch", 8.5, "purple", "bold", ha="center")
        text(32.5, 65, "edit + evidence + base", 7.3, ha="center")

        box(11, 78, 43, 14, "green_fill", "green", .8)
        text(32.5, 82.6, "Verify patch", 8.5, "green", "bold", ha="center")
        text(32.5, 88.1, "evidence support + scope", 7.3, ha="center")
        box(11, 101, 43, 9, "white", "line", .65, radius=.8)
        text(32.5, 105.5, "Hold for review", 7.8, "muted", ha="center")

        original = {"timeout": "20 s", "retries": "3", "backend": "local", "schema": "1"}
        patch = {"timeout": "45 s"}
        updated = {**original, **patch}
        unchanged = [key for key in original if original[key] == updated[key]]
        assert len(unchanged) == 3 and list(patch) == ["timeout"]
        records = [(75, original, "Memory v7", "old_fill"), (129, updated, "Memory v8", "amber_fill")]
        for x, record, heading, changed_fill in records:
            box(x, 29, 38, 47, "white", "line", .75, radius=1.1)
            ax.add_patch(Rectangle((x+.25, H-38), 37.5, 8.75, facecolor=COLORS["context"], edgecolor="none", zorder=3))
            text(x+3, 33.5, heading, 8.2, weight="bold")
            for row, (key, value) in enumerate(record.items()):
                row_y = 42.5 + row*8
                if key in patch:
                    ax.add_patch(Rectangle((x+1.3, H-row_y-3.6), 35.4, 7.2,
                                           facecolor=COLORS[changed_fill], edgecolor="none", zorder=3))
                    ax.add_patch(Rectangle((x+1.3, H-row_y-3.6), .8, 7.2,
                                           facecolor=COLORS["amber"], edgecolor="none", zorder=4))
                text(x+3.6, row_y, key, 7.5, "ink", mono=True)
                text(x+34.8, row_y, value, 7.5, "amber" if key in patch else "muted",
                     weight="bold" if key in patch else "normal", ha="right", mono=True)
            text(x+3, 72.4, "one key edited" if heading.endswith("8") else "four payload keys", 7.2, "muted")

        # The receipt makes the example inspectable without adding measured
        # performance claims. Payload state and audit metadata are distinct.
        box(75, 84, 92, 18, "context", "context", lw=0, radius=1)
        text(78, 88.2, "Commit receipt", 8.1, weight="bold")
        text(78, 93.6, "evidence e12   base v7   checks 2/2", 7.5, "muted", mono=True)
        text(78, 98.6, "preserved: retries, backend, schema", 7.5, "muted", mono=True)

        nodes = [Node("evidence", rect(11,29,43,17)), Node("propose", rect(11,55,43,14)),
                 Node("verify", rect(11,78,43,14)), Node("review", rect(11,101,43,9)),
                 Node("memory", rect(75,29,38,47)), Node("next", rect(129,29,38,47))]
        routes = []

        def route(name, source, target, via=(), *, color="muted", dashed=False):
            points = (port_point(source,nodes), *[xy(a,b) for a,b in via], port_point(target,nodes))
            item = Route(name, source, target, points, kind=source.kind)
            routes.append(item)
            path = MplPath(points, [MplPath.MOVETO] + [MplPath.LINETO]*(len(points)-1))
            ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=8.5,
                                        linewidth=.9,
                                        linestyle=(0,(3,2)) if dashed else "-",
                                        color=COLORS[color], shrinkA=0, shrinkB=0, zorder=5))

        route("evidence_to_proposal", Port("evidence","bottom"), Port("propose","top"), color="blue")
        route("state_to_proposal", Port("memory","left",.5), Port("propose","right",.5),
              [(65,52.5),(65,62)], color="muted")
        route("proposal_to_verification", Port("propose","bottom",kind="candidate"),
              Port("verify","top",kind="candidate"), color="purple")
        route("rejected_patch", Port("verify","bottom",kind="reject"),
              Port("review","top",kind="reject"), color="muted", dashed=True)
        route("payload_state", Port("memory","right",.5,kind="state"),
              Port("next","left",.5,kind="state"), color="muted")
        route("verified_patch", Port("verify","right",.5,kind="verified_patch"),
              Port("next","right",.5,kind="verified_patch"),
              [(65,85),(65,111),(173,111),(173,52.5)], color="amber")
        text(121, 48.5, "state", 7.4, "muted", ha="center")
        text(29, 96.5, "reject", 7.3, "muted", ha="right")
        text(120, 107.2, "pass: commit verified patch", 7.4, "amber", ha="center")

        # Diagram and code share semantic colors. The update rule is executable
        # pseudocode, not a second unverified architecture.
        box(5, 119, 168, 16, "#F4F5F6", "#F4F5F6", lw=0, radius=1)
        text(10, 124, "Update rule", 8.0, weight="bold")

        def code_line(x, y, chunks):
            for content, color in chunks:
                a = text(x, y, content, 7.5, color, mono=True)
                fig.canvas.draw()
                x += a.get_window_extent(fig.canvas.get_renderer()).width * W / fig.bbox.width

        code_line(39, 124, [("patch = ","ink"),("propose","purple"),("(","ink"),
                              ("evidence","blue"),(", memory)","ink")])
        code_line(39, 130, [("next = ","ink"),("commit","amber"),("(memory, patch) if ","ink"),
                              ("verify","green"),("(patch) else memory","ink")])

        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        labels = []
        for i, artist in enumerate(text_artists):
            bounds = artist.get_window_extent(renderer).transformed(ax.transData.inverted())
            labels.append(Label(f"text_{i}", Rect(*map(float,bounds.extents))))
        review = validate_diagram(nodes, routes, labels, clearance=.35, units="mm")
        if not review.passed:
            raise ValueError(json.dumps(review.to_dict(),indent=2))

        stem = out / "verified_memory_patch"
        data = {"status":"schematic", "empirical_measurements":False, "before":original,
                "candidate_patch":patch, "after":updated, "unchanged_payload_keys":unchanged,
                "candidate_context":{"evidence":"e12: timeout = 45 s", "base_snapshot":original, "base_version":"v7"},
                "evidence_id":"e12", "base_version":"v7", "next_version":"v8",
                "example_assumptions":["The evidence supports timeout=45 s.","The patch is restricted to the timeout payload key.","Both checks pass; committing also advances audit metadata.","A rejected patch leaves payload state unchanged and goes to review."],
                "nodes":[asdict(n) for n in nodes],"routes":[asdict(r) for r in routes],
                "palette_status":"Original adapted production palette; not copied source RGB values.",
                "palette":COLORS,"fonts":fonts[2],"physical_size_mm":[W,H]}
        data_path = stem.with_suffix(".data.json")
        data_path.write_text(json.dumps(data,indent=2)+"\n")
        stem.with_suffix(".geometry.json").write_text(json.dumps(review.to_dict(),indent=2)+"\n")
        caption = ("Schematic illustration of a verified memory edit using hypothetical configuration records. "
                   "(a) A proposal carries the edit, supporting evidence and current memory snapshot. Verification checks that bundled evidence and edit scope. "
                   "A rejected patch is held for review; a passing patch reaches the commit through a separate outer corridor. "
                   "(b) The original state and verified patch are distinct inputs to the next state. Only the timeout payload key changes from 20 s to 45 s; "
                   "three other payload keys remain identical. The version and receipt are audit metadata and also change at commit. "
                   "The displayed rule preserves the original memory when verification fails. Colors bind operations to the corresponding code identifiers; "
                   "shapes distinguish evidence, computation and structured state. This is an original design demonstration, not an evaluated method or empirical result.")
        alt = ("A two-panel schematic pairs an evidence/propose/verify path on the left with before-and-after memory records on the right. "
               "The current record also feeds the proposer. A dashed rejection path goes to review; a separate outer passing route enters the new state. "
               "An amber-highlighted timeout row changes from 20 to 45 seconds while retries, backend and schema remain unchanged. "
               "A receipt states the evidence and version; a bottom code strip uses matching operation colors.")
        stem.with_suffix(".caption.md").write_text(caption+"\n")
        stem.with_suffix(".alt.txt").write_text(alt+"\n")
        paths = export_figure(fig, stem, source_files=[data_path,Path(__file__),
            Path(__file__).with_name("figure_style.py"),Path(__file__).with_name("diagram_geometry.py"),
            Path(__file__).with_name("render_modern_examples.py")],
            metadata={"status":"schematic","empirical_measurements":False,"caption":caption,"alt_text":alt,
                      "design_sources":["AlphaEvolve 2506.13131v1 Figure 2: component-to-code binding", "SAM 3 Figure 4: typed shapes and lower return corridor", "Anthropic Circuit Tracing methods diagram: muted context and selected path"],
                      "minimum_font_pt":7.2,"fonts":fonts[2],"geometry_check":review.to_dict()}, dpi=300)
        plt.close(fig)
        return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render(args.out),indent=2))


if __name__ == "__main__":
    main()
