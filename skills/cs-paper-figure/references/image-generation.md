# Generated illustrations (icons, avatars, emblems) with Codex CLI

Optional stage. The skill never depends on it: `paperkit`'s vector icons (`icon_robot`, `icon_snow`, ...)
are the fallback and are always acceptable. Use generated art only when it does a job the vector
glyphs cannot do as well, and only if `python scripts/codex_icons.py check` exits 0.

## 1. What top-lab figures actually do (study of 11 overview figures, 2026-10)

| Paper (lab) | Raster / illustrated elements | Job | Style |
|---|---|---|---|
| Janus (DeepSeek), CLIP (OpenAI), SAM (Meta) | none, or only real photos as *data* | — | pure vector diagram |
| RT-2 (Google DeepMind), Qwen2-VL (Alibaba) | real photos, screenshots, video frames | show the input modality / real capability | photo; colour of the sample = colour of its tokens (Qwen2-VL) |
| Magentic-One (Microsoft) | 7 monoline glyphs, one per agent label; real screenshots in the example | identify actors; show real artefacts | one outline family, roles carried by box colour |
| Eureka (NVIDIA) | line glyphs in stage headers; one real simulator render | label stages; show the environment | glyph colour = stage colour |
| AutoGen (Microsoft) | one flat robot avatar, recoloured per role, reused ~10× | identify agent types | flat pastel; robot colour = role frame colour |
| AppAgent (Tencent) | line robot + emoji + phone screenshots | actor, actions, environment | **mixed registers — the counter-example** |
| Voyager (NVIDIA), Generative Agents | game sprites / the simulator's own tilemap | the environment *is* the subject | native pixel style throughout |

Three of eleven use no illustration at all; every paper keeps labels, numbers, code and arrows as live
vector text; photos and screenshots are always real artefacts, never illustrations of data.

## 2. Decide whether to generate (in this order)

1. **Is the noun real data or a real system?** (an input image, a web page, a robot frame, a game)
   → use the real artefact (photo, screenshot, render), not a generated picture. Never generate
   something that could be read as a result or a sample.
2. **Is the figure an architecture of tensors/modules?** → stay vector (Janus, CLIP). No icons.
3. **Does the reader need to tell actors, roles, tools or stages apart at a glance?** → a matched set
   of 3–7 icons may help (AutoGen, Magentic-One, Eureka). Otherwise skip.
4. **Would a paperkit vector glyph say the same thing?** → use the vector glyph.

## 3. Rules for a generated set

1. **One set, one prompt, one style.** Generate all icons of a figure in one Codex run from one style
   spec; never mix with emoji, stock clip-art or a second style (AppAgent's mix reads as clutter).
2. **3–7 distinct icons per figure.** Reuse one asset (with a colour change) instead of generating
   variants. One shared character for actors: vary only pose, prop and accent (AutoGen).
3. **Size by role.** Header/label glyphs ≈ 1–1.5× text height; actor avatars ≈ 3–4× cap height
   (6–9 mm at 7 pt); scene thumbnails ≈ one box width. Never larger than the hero block.
4. **Colour = role colour.** Give each icon the stroke/mark hex of the box or band it belongs to
   (`accent` in the spec). Neutral grey for frozen or shared parts. One meaning per hue still holds.
5. **No text in pixels.** Labels, numbers, code, formulas, arrows and boxes stay vector. The prompt
   forbids letters; reject any output that has them.
6. **Icons never replace labels and never sit on connectors.** Every icon has a text label beside it
   and lives in a header, a box corner or a gutter.
7. **Extend from a reference.** To add icons to an existing set (or keep two figures of one paper
   consistent), pass an existing icon with `--ref`; the prompt marks it as a style reference.
8. **Check at print size.** Read the contact sheet's 48 px previews; if the prop that carries the
   meaning (laptop, pencil, magnifier) is not readable at 8 mm, simplify the subject or enlarge.
9. **Record provenance.** `manifest.json` keeps the prompt, tool version and date; many venues ask
   authors to disclose generated imagery, so mention it in the acknowledgements or caption notes.
10. **Keep a vector fallback in the script.** Render scripts must still run without the PNGs
    (`--vector-icons`, or a missing file falls back to `cv.icon_*`).

## 4. Workflow

```bash
python scripts/codex_icons.py check                       # codex installed + logged in?
python scripts/codex_icons.py prompt spec.json            # read the prompt before spending a run
python scripts/codex_icons.py generate spec.json --out figs/icons [--ref figs/icons/old.png]
# review figs/icons/_sheet.png, regenerate single icons with a narrower spec if one drifts
```

`spec.json`:

```json
{"set": "my-fig2", "style": "flat-pastel",
 "character": "a friendly robot with a rounded head, two round eyes and a small antenna",
 "icons": [{"name": "planner",  "subject": "the robot holding a checklist", "accent": "#5A8BCB"},
           {"name": "executor", "subject": "the robot typing on a laptop",  "accent": "#3D9C8B"}]}
```

Styles: `flat-pastel` (role mascots, the AutoGen register), `line` (header pictograms, the
Magentic-One / Eureka register), `soft-3d` (objects and stores with gentle depth). Set `character` only
when every icon is the same actor; otherwise describe the shared character inside the subjects that
need it and pass a reference image.

The helper runs `codex exec` in a throw-away directory with `-s workspace-write`, asks for Codex's
built-in `image_gen` tool (no API key needed with a ChatGPT login), then flattens each PNG onto white,
trims, pads to a square and resizes to 512 px. A Codex run for 3–6 icons takes a few minutes.

Place icons with `cv.image(path, cx, cy, w)` (knocks out the white, so icons sit on tinted bands).
Pattern used in `examples/harness2/render_fig3.py`:

```python
def robot(cv, x, y, c, name, s):
    png = os.path.join(ICON_DIR, f"{name}.png")
    if os.path.exists(png) and not NO_ICONS:
        cv.image(png, x, y, s)
    else:
        cv.icon_robot(x, y, s, color=c["mark"])      # vector fallback
```

## 5. Prompt anatomy (what `build_prompt` writes)

1. Tool + set framing: "use your built-in image generation tool ... ONE consistent set for a figure in a
   scientific paper; one image_gen call per icon".
2. Style line from the preset (outline weight, fill treatment, what is banned: gradients, shadows).
3. Canvas rules: pure white, 1024², centred, ~12% margin, readable at 8 mm, no text/logos/frames.
4. Shared character (optional) and references, each labelled as a style reference, not an edit target.
5. One line per icon: `name.png: subject, accent colour #hex` — subject = noun + the one prop or pose
   that carries the meaning (laptop = executes, pencil over a diff = edits, magnifier = reflects).
6. Delivery: exact file names in the working directory, no post-editing.
