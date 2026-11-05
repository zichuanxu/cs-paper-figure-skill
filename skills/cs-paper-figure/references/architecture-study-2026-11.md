# Architecture-register study (2026-11): 23 method figures

Sources: the user's three uploads (Holmes Fig. 2, a continual thermal-IR restoration framework with
SEP/SKMM modules, and a degradation-aware TIR restoration network with DENet/SE-ROS), plus the
20-figure 科研绘图 01–20 set: PCF-Lift Fig. 2, DySeT Fig. 1, ProEmoTrans Fig. 2, ReSet Fig. 2, LFBNet
Fig. 5, CHAL Fig. 3, HFF-Net Fig. 2, MAGRPP Fig. 5, Holmes Fig. 2, DOLPHIN Fig. 1, ViRefSAM Fig. 4,
S2TA-Fuse, RoofX-Net Fig. 2, SemDiff, MMFformer Fig. 1, CoPS Fig. 2, SMC-Mamba Fig. 1, C2R Fig. 3,
VideoFusion Fig. 4, STDD Fig. 3. Venues: ECCV, CVPR, AAAI, EMNLP, TGRS, TCSVT, ISPRS, Nat. Commun.

These are vision / multimodal / CV-style method figures. They are denser, more colourful and more
object-rich than the LLM-lab figures studied in [craft-study-2026-10.md](craft-study-2026-10.md), and
several things they do were missing from this skill. The previous gallery outputs all used one
template (grey header band, white card, flat 2D boxes, muted fills); next to these figures they read as
tidy but generic. What follows is what the strong ones share, with the figure that shows it best.

## 1. Layout skeleton: overview row + detail row + key strip

18 of 23 use the same plate: **one overview pipeline across the top (55–65 % of height), a row of
2–4 equal-height detail panels below it, and a glyph key along the bottom** (TIR-continual, TIR-DENet,
LFBNet, HFF-Net, SemDiff, SMC-Mamba, VideoFusion, C2R, MMFformer, Holmes, STDD). The overview names
each module once; the detail panels open the 2–4 modules that are new. Zoom is shown by two dashed
rays from the module's footprint in the overview to the detail panel's top corners (TIR-continual,
RoofX-Net), or simply by matching the detail panel's hue to the module's fill (SemDiff, VideoFusion).
Detail panels sit on one baseline and share a height even when their content differs.

Variant: three stacked **full-width tinted rows**, one per stage, each with its title at a corner
in the stage hue (CHAL: pink neural fields, green anomaly learning, blue causal guiding), plus an
inputs/outputs column at the left in neutral grey.

## 2. Section frames carry the colour, not the boxes

- Each module region is a **tinted field + dashed border in the same hue** (ReSet blue/green,
  CoPS yellow/red/purple, Holmes dashed maroon, SMC-Mamba blue/yellow). Inside it, the blocks can be
  quiet because the region already says which module they belong to.
- Title placement, in decreasing frequency: a **pill tab sitting on the top border** (ReSet "Text-
  Anchored Semantic Mask (TSMa)", CoPS), a **bold caption strip along the bottom edge** of the panel
  (HFF-Net "(b) Adaptive Laplacian Convolution", STDD, VideoFusion), or **bold-italic in the top-left
  corner in the region's hue** (SemDiff, C2R "(a) Training at s-th Stage", CHAL).
- Titles name the module with its acronym in parentheses: "Bi-temporal Co-attention Module",
  "(c) Dynamic Co-Evidential Aggregator". The acronym is what the overview boxes say.
- A "for training only" region is a tinted band with an italic label (SemDiff), not a footnote.

`paperkit`: `cv.section(..., tab="top"|"bottom"|"corner", letter=)`.

## 3. Draw tensors and layers in pseudo-3D

- **Feature tensors are cuboids** with a visible top and side face, often stacked 2–4 deep for
  channels/scales, with `H×W×C` in italic math beside them (SemDiff, RoofX-Net, C2R z-vectors,
  ViRefSAM F_t / F_r, CoPS token cubes).
- **Layers are tall thin slabs with vertical text** (TIR "Feature Extractor", "Conv", "GNorm", "GELU",
  MMFformer "Multi-head Attention", HFF-Net "FDCA", VideoFusion "Conv/FFN"). A run of slabs reads as
  depth through the network; it also lets a 6-layer block fit in 25 mm of width.
- **Encoders and backbones are trapezoids** (wide→narrow), with a snowflake or flame in the corner
  (ReSet DINOv2/CLIP, MAGRPP I3D, C2R old/new model, ViRefSAM image encoder).
- A **fused feature gets a gradient** between its two sources' hues (HFF-Net blue→orange fusion
  block, SMC-Mamba F_mc). The colour itself says "both".

`paperkit`: `cv.cuboid(..., rotate=True)` for slabs, `cv.cuboid(...)` for tensors, `grad=(c0, c1)`
for fused features, `cv.trap` for encoders.

## 4. Show the data, not only the operators

- Inputs and outputs are **real thumbnails**, frames as an offset stack (TIR, CHAL, VideoFusion,
  SMC-Mamba, MMFformer). Results repeat the input with the prediction drawn on it (box, mask).
- **Intermediate feature maps appear as colormapped images** (viridis/plasma/jet): LFBNet, CHAL,
  ReSet low/mid/high features, CoPS spatial weighting. They prove that the tensor is spatial and
  show where the signal is.
- **Numbers live in cells**: similarity matrices with values (ProEmoTrans 0.52/0.73, Holmes
  calibration 0.87/0.88/0.93, CoPS 0.4/0.7/1.0), with the winning cell bold-bordered.
- **Mini plots inside a card**: distributions (PCF-Lift PP kernel with ↑/↓), class-score bars
  (ReSet), decay weights (CHAL), loss-weight curves. Shape only, no ticks.
- **Math objects are drawn as what they are**: the Dirichlet simplex as a triangle with a density
  inside (Holmes), the Gaussian latent as concentric ellipses (CoPS), a graph as nodes and edges
  (PCF-Lift similarity graph, TIR-DENet feature-similarity graph and coding tree, DOLPHIN).

`paperkit`: `cv.fmap(n=3)`, `cv.num_matrix(hi=)`, `cv.mini_plot(bars=)`, `cv.graph()`, `cv.image()`.
Illustrative maps are stated once in the caption.

## 5. One identity per branch, carried everywhere

- Each branch/modality/factor has one hue that appears on its blocks, its wires, its tokens **and
  in the text that names it** (Holmes frame branch pink vs clip branch purple; TIR-DENet d_n/d_b/d_c
  discs coloured as the three DRM cylinders they route to, with curved arrows in the same colours;
  ReSet "Low-/Mid-/High-Level" with the level word coloured; STDD temporal orange vs spatial blue
  t−δ/t/t+δ windows).
- Wires take the branch colour when two branches run in parallel (Holmes, VideoFusion green/blue,
  SMC-Mamba), and are neutral black elsewhere.
- Legend entries for the colours are not needed when the coloured word appears in a label.

`paperkit`: `cv.rich()` for coloured words inside a label; `ROLE` families per branch.

## 6. Operators and keys

- Every elementwise op is a circled glyph: ⊕ ⊗ ⊙ ⓒ σ, plus paper-specific letters (Ⓡ ROI align,
  Ⓖ gating, DC deformable conv, Σ). They are defined once in a **dashed key strip** across the bottom
  (LFBNet, HFF-Net, SMC-Mamba, TIR ×2, ViRefSAM, CoPS at the right edge).
- The key also defines snowflake = frozen, flame = trainable (12 of 23 use this pair), solid vs
  dashed arrows = train/test vs train-only (CoPS), and abbreviations (FFT2D, ACn, FGOP).
- Thus panel text can be one or two words; the key is the glossary.

`paperkit`: `cv.legend([...])` with kinds op / snow / flame / dash / cuboid / box / fmap / abbr.

## 7. Phase and time bars

- A **coloured strip under the columns** names the phases once (DySeT "Scene Encoding | Dynamic
  Sampling | Masked Self-Distillation"), so the panels above need no long titles.
- A **time axis** runs under sessions or stages with tick marks at each one (MAGRPP "Session Time
  Axis"; C2R "Data Stream" arrow from old to new data).

`paperkit`: `cv.phase_bar()`.

## 8. Typography and weight

- Times-family serif (14/23) or a heavy sans (TIR-DENet, VideoFusion). Module names bold, 9–10 pt
  at print; math italic with sub/superscripts on every symbol (F_t, F^r_X, z^o).
- Text inside a slab is rotated 90° rather than shrunk.
- Panel letters are bold "(a)", always with a module name, never alone.

## 9. What they get wrong (do not copy)

- Microtype: HFF-Net, S2TA-Fuse and VideoFusion's lower detail rows go below 5 pt at print.
- Clipart emoji and mixed icon styles (ProEmoTrans emoji, SMC-Mamba people illustrations, CHAL
  network clip-art): one matched icon set or none.
- Over-saturated, many-hue fills where colour encodes nothing (VideoFusion uses six hues for
  six block types; CHAL's jet maps beside viridis maps).
- Wires crossing through text (MMFformer K/V wires, CHAL "Block" crossing).
- 3-D perspective for the whole pipeline (RoofX-Net): it reads as decoration and makes
  dimensions unreadable; use pseudo-3D for individual tensors only.

## 10. Transfer rules (what changed in this skill)

1. Use the overview + detail-row + key-strip plate for any method with 2+ new modules.
2. Give every module a section frame in its own hue; do not put a grey header band on every card.
3. Draw tensors as cuboids, layers as slabs, encoders as trapezoids; fuse with gradients.
4. Put at least one *data object* in each detail panel: a feature map, a numeric matrix, a mini plot,
   a graph, real tokens or a real thumbnail.
5. Colour the words that name a branch in that branch's hue.
6. End the figure with a key strip that defines every glyph and abbreviation.
7. Keep this skill's existing discipline: ≥ 5.8 pt text, no crossings, one meaning per hue, caption
   says what is shown.
