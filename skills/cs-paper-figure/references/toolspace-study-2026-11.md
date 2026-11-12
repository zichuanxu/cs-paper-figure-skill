# ToolSpace Figure 1 (2026-11): what a showcase figure does well, and how a redesign lost it

Source: Dong et al., *ToolSpace: Scaling Tool-Centric Environment Synthesis for Long-Horizon Agents*
(arXiv 2611.05036), Figure 1: (a) a tool-space layer between agent and MCP servers, (b) the
tool-composition graph with one walk, (c) two radar charts, (d) bars on two Pro benchmarks.

The first redesign made with this skill replaced the layered plates by a flat box, the product logos by
text-labelled cylinders, and the radars by eight-row dot charts. It passed every audit and `parity`, and
the user's verdict was: "Sometimes this kind of figure is better. And logo can be used as good things.
[...] You are making the figure more ugly now." This file records what the original does well, what it
does badly, and the rules that keep a redesign from trading attraction for tidiness.

## 1. Strengths of the original

- **A layer drawn as a layer.** The claim "a tool space sits between the agent and the environments"
  is two isometric plates, one floating above the other. Depth carries the relation: above, below,
  between. The tools stand on the upper plate as tiles, the servers on the lower one, and the paired
  down/up arrows live in the gap between the plates. The plate names itself on its front edge.
- **Logos as identity marks.** Ten product marks (GitHub, Slack, Notion, Drive, Postgres, ...) in
  white rounded tiles, each with its name underneath. A reader recognises them in well under a second,
  they say "real services" more convincingly than ten words do, and they bring colour that claims no
  meaning. The same holds for the model marks over the bars in (d).
- **A radar for an envelope claim.** Panel (c) claims that one model is ahead on nearly every
  benchmark. The outermost polygon enclosing the others shows that before any number is read. There are
  only four polygons, the hero's value is printed at every vertex in the hero's colour, and seven
  benchmarks with very different score ranges fit one compact glyph.
- **Bars with an identity on top.** In (d) each bar carries the model's mark above its value, so the
  legend is a lookup of last resort.
- **Surface.** Soft gradients on plates and bars, pastel cluster blobs, one bold serif title per
  dashed rounded panel. A third of the area is picture, not text.

## 2. Flaws of the original (fix these, keep §1)

- The radar's scale is unstated: each axis runs to its own best score. The baselines' values are not
  printed, and the envelope hides the one benchmark the hero does not win (tau^3-Bench Banking, 43.3
  against 46.9).
- The hero is red in the left radar, light blue in the right one, and the bars in (d) use a third
  scheme: ToolSpace has no colour of its own.
- (d) draws Pro scores for six of the seven models in the table and no Standard scores, so the "drop"
  the text claims is not in the figure.
- Tool names on the plate are about 3.5 pt at print size; several tiles on the plate are unnamed
  decoration.

## 3. What the first redesign got wrong

- It treated depth, logos and radars as decoration to be cleaned away. They were the figure's
  argument and its attraction.
- Dot rows are more exact than a radar, but eight rows of four overlapping marks read as a table.
  The envelope, which is the claim, was gone.
- `parity` reported "ok" (more picture share than the original) for a figure a reader found plainer.
  The metric counts textured blocks; it does not see that a recognisable thing was replaced by a
  generic one.

## 4. Rules

1. **Strengths first.** Before listing an original's defects, list three to five things it does well
   that a reader would miss if they were gone. Each one is kept, or replaced by something visibly
   stronger. A redesign that is more correct but plainer has failed.
2. **Change an encoding only when the claim needs it.** An envelope or profile claim with at most
   four series keeps its radar (`cv.radar`); repair its honesty instead: say how the axes are scaled,
   print the hero's value at each vertex, print the winner's value on any axis the hero loses, one
   hero colour in every panel. Gap, ratio and ranking claims go to aligned marks.
3. **Logos are identity marks, and they are welcome** when the figure names real products, services,
   models or datasets that readers know by sight.
   - Use the official mark, unmodified, in its own colours: do not redraw it, recolour it to the
     palette or crop it.
   - Put it in a white tile (`cv.tile(image=...)`), all marks of one row at one size, never larger
     than a technical object beside it.
   - Pair it with the name unless the mark is a wordmark. A logo alone is a riddle for some readers.
   - Sources: the paper's own assets when redesigning its figure; the owner's press kit or an open
     icon set otherwise. Keep the files beside the script and a text fallback in the code.
   - Marks stay the property of their owners; say so where the figure is published, and check the
     venue's rules before submission.
   - Not for: a logo as the focal point of a mechanism, a lab's logo to borrow authority, or a mark
     for something the reader would not recognise.
4. **A layering relation gets depth.** "X sits between A and B", "built on", "wraps": stack plates
   (`cv.plate`) with tiles standing on them and the traffic in the gaps. Depth is for the relation
   only; charts and step lists stay flat.
5. **Bars may carry identity.** A mark above each bar plus the value on it; a ghost outline for the
   reference condition when the claim is a drop or a gain.
6. **`parity` is necessary, not sufficient.** Put original and redesign side by side at one width and
   ask which one a reader would choose for a slide. If the original wins the first glance, find out
   why before shipping.

## 5. paperkit devices added

| Device | Call |
| --- | --- |
| Isometric plate with a labelled front edge; `at(u, v)` places objects on it | `cv.plate(x, y, w, d, r=..., label=...)` |
| Upright rounded tile with a logo or glyph, name under or inside | `cv.tile(cx, cy, s, image=... / glyph=..., label=...)` |
| Radar with hero emphasis, vertex values and a printed rival value where the hero loses | `cv.radar(cx, cy, R, axes, series, hero=0, scale="axis")` |

Worked example: [`scripts/examples/toolspace/render_fig1.py`](../scripts/examples/toolspace/render_fig1.py).
