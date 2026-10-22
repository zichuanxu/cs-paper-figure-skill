"""Generate a matched raster icon set for a paper figure with Codex CLI's built-in image tool.

Optional: everything in the skill works without it (paperkit's vector icons are the fallback).
Use it only for illustrative nouns (agent roles, environments, objects), never for labels or data.

    python codex_icons.py check                          # exit 0 if codex is installed and logged in
    python codex_icons.py prompt SPEC.json [--ref a.png] # print the prompt only
    python codex_icons.py generate SPEC.json --out DIR [--ref a.png ...] [--model M] [--timeout 1200]
    python codex_icons.py tidy DIR                        # re-run post-processing on DIR/*.png
    python codex_icons.py sheet DIR                       # DIR/_sheet.png contact sheet for review
    python codex_icons.py selftest

SPEC.json:
    {"set": "harness2-fig3", "style": "flat-pastel",
     "character": "a friendly robot with a rounded head, two round eyes and a small antenna",
     "icons": [{"name": "executor", "subject": "the robot typing on a laptop", "accent": "#5A8BCB"}, ...]}

`character` is optional; give it when the icons are the same actor in different roles. Pass an
existing icon with --ref to extend a set so new icons match it. Outputs are DIR/<name>.png (512 px,
square, white background, trimmed) plus DIR/manifest.json recording the prompt for disclosure.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

STYLES = {
    # flat role mascots, the most common style in agent-system overviews
    "flat-pastel": ("clean flat vector illustration, uniform thin dark-grey outlines, soft pastel fills with "
                    "the accent colour as the main hue, at most one lighter tint for highlights, no gradients, "
                    "no drop shadows, no texture"),
    # monochrome pictograms that sit inside small boxes or headers
    "line": ("minimal line pictogram, single uniform stroke weight in dark grey, rounded caps and joins, "
             "the accent colour only as one small flat fill, no gradients, no shadows, no background shape"),
    # small objects or environments with gentle depth (data stores, devices, scenes)
    "soft-3d": ("soft isometric 3D object illustration, matte clay-like material, gentle ambient occlusion, "
                "pastel colours led by the accent colour, no hard shadows on the ground, no reflections"),
    # small narrative scenes (a person and an agent doing something), the survey/position-paper register
    "scene": ("flat vector editorial illustration of a small scene, clean dark-grey outlines, soft pastel palette, "
              "simple uncluttered background with a few props, gentle flat shading only, no gradients, no photo realism"),
}
RULES = ("Pure white (#FFFFFF) background, square 1024x1024 canvas, the subject centred with about 12% empty "
         "margin on every side. It will be printed 6-9 mm wide, so use bold outlines (about 2.5% of the canvas "
         "width), large simple shapes and few small details; it must stay clear at 64x64 px. No text, letters, numbers, logos, "
         "watermarks, UI chrome, borders or frames anywhere in the image.")


def check():
    exe = shutil.which("codex")
    if not exe:
        return False, "codex not found on PATH; use paperkit vector icons"
    try:
        r = subprocess.run([exe, "login", "status"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, f"codex login status failed: {e}"
    msg = (r.stdout + r.stderr).strip()
    if r.returncode != 0 or "not logged in" in msg.lower():
        return False, f"codex is not logged in ({msg}); run `codex login`, or use vector icons"
    return True, f"{exe}: {msg}"


def load_spec(path):
    with open(path) as f:
        spec = json.load(f)
    icons = spec.get("icons") or []
    assert icons, "spec needs a non-empty 'icons' list"
    names = [i["name"] for i in icons]
    assert len(set(names)) == len(names), f"duplicate icon names: {names}"
    assert all(n.replace("-", "").replace("_", "").isalnum() for n in names), "names must be file-safe"
    assert spec.get("style", "flat-pastel") in STYLES, f"style must be one of {sorted(STYLES)}"
    return spec


SCENE_RULES = ("Landscape 1536x1024 canvas on a plain white or very light background. Absolutely no readable text: "
               "screens, documents, signs and tablets show only blank bars, simple shapes, ticks or charts, because every "
               "label in the figure is added later as vector text. No logos, watermarks, borders, frames or speech "
               "bubbles. Leave a calm empty area near the top of the scene where a speech bubble can be overlaid.")


def build_prompt(spec, refs=()):
    style = STYLES[spec.get("style", "flat-pastel")]
    n = len(spec["icons"])
    if spec.get("style") == "scene":
        lines = [f"Use your built-in image generation tool to create {n} separate landscape PNG illustrations that form "
                 f"ONE consistent set of scenes for a figure in a scientific paper. Make one image_gen call per scene.",
                 f"Style for every scene: {style}.", SCENE_RULES]
    else:
        lines = [f"Use your built-in image generation tool to create {n} separate square PNG icons that form ONE "
                 f"consistent set for a figure in a scientific paper. Make one image_gen call per icon.",
                 f"Style for every icon: {style}.", RULES]
    if spec.get("character"):
        lines.append(f"Every image shows the exact same character(s): {spec['character']}. Keep proportions, "
                     "faces, clothing, line weight and colours identical across the set; only pose, props and setting change.")
    for k, ref in enumerate(refs, 1):
        lines.append(f"Image {k} ({os.path.basename(ref)}) is a STYLE REFERENCE from the same figure set, not an "
                     "edit target: match its character design, outline weight, fill treatment and margin.")
    lines.append("Icons:")
    for k, ic in enumerate(spec["icons"], 1):
        acc = f", accent colour {ic['accent']}" if ic.get("accent") else ""
        lines.append(f"({k}) {ic['name']}.png: {ic['subject']}{acc}.")
    lines.append("Copy each final image into the current directory with exactly those file names, overwrite "
                 "nothing else, do not edit the images afterwards, then list the directory.")
    return "\n".join(lines)


def tidy(path, size=512, margin=0.06, scene=False):
    """Flatten onto white, trim to the ink, pad to a square with a small margin, resize.
    Scenes keep their aspect ratio and are only flattened and resized to `size` * 2 px wide."""
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, "white")
    im = Image.alpha_composite(bg, im).convert("RGB")
    if scene:
        w = size * 2
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(path)
        return im
    gray = im.convert("L").point(lambda v: 255 if v < 240 else 0)
    box = gray.getbbox()
    if box:
        im = im.crop(box)
    side = int(max(im.size) * (1 + 2 * margin))
    sq = Image.new("RGB", (side, side), "white")
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    sq = sq.resize((size, size), Image.LANCZOS)
    sq.save(path)
    return sq


def sheet(out_dir, names=None):
    from PIL import Image, ImageDraw
    names = names or sorted(f[:-4] for f in os.listdir(out_dir) if f.endswith(".png") and not f.startswith("_"))
    tiles = [Image.open(os.path.join(out_dir, n + ".png")).convert("RGB").resize((256, 256)) for n in names]
    W = 256 * len(tiles) + 16 * (len(tiles) + 1)
    sh = Image.new("RGB", (W, 300), "#F3F4F6")
    d = ImageDraw.Draw(sh)
    for k, (n, t) in enumerate(zip(names, tiles)):
        x = 16 + k * 272
        sh.paste(t, (x, 16))
        # small preview too: icons must read at print size
        sh.paste(t.resize((48, 48)), (x + 200, 230))
        d.text((x, 278), n, fill="#353C47")
    p = os.path.join(out_dir, "_sheet.png")
    sh.save(p)
    return p


def generate(spec_path, out_dir, refs=(), model=None, timeout=1200):
    ok, msg = check()
    if not ok:
        sys.exit(f"[codex_icons] {msg}")
    spec = load_spec(spec_path)
    prompt = build_prompt(spec, refs)
    os.makedirs(out_dir, exist_ok=True)
    work = tempfile.mkdtemp(prefix="codex_icons_")
    cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "workspace-write", "-C", work]
    if model:
        cmd += ["-m", model]
    for r in refs:
        cmd += ["-i", os.path.abspath(r)]
    cmd.append("-")  # prompt from stdin: -i takes several values and would swallow a positional prompt
    log = os.path.join(out_dir, "_codex_log.txt")
    with open(log, "w") as f:
        r = subprocess.run(cmd, input=prompt, stdout=f, stderr=subprocess.STDOUT, text=True, timeout=timeout)
    names = [i["name"] for i in spec["icons"]]
    missing = [n for n in names if not os.path.exists(os.path.join(work, n + ".png"))]
    if r.returncode != 0 or missing:
        sys.exit(f"[codex_icons] codex exit {r.returncode}, missing {missing}; see {log}. "
                 "Fall back to paperkit vector icons.")
    for n in names:
        dst = os.path.join(out_dir, n + ".png")
        shutil.copy(os.path.join(work, n + ".png"), dst)
        tidy(dst, scene=spec.get("style") == "scene")
    ver = subprocess.run(["codex", "--version"], capture_output=True, text=True).stdout.strip()
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump({"set": spec.get("set"), "generator": f"{ver} built-in image_gen",
                   "date": datetime.date.today().isoformat(), "refs": [os.path.basename(x) for x in refs],
                   "prompt": prompt, "icons": spec["icons"]}, f, indent=2)
    shutil.rmtree(work, ignore_errors=True)
    print(f"[codex_icons] wrote {len(names)} icons to {out_dir}; review {sheet(out_dir, names)}")


def selftest():
    from PIL import Image, ImageDraw
    spec = {"style": "line", "character": "a robot", "icons": [{"name": "a", "subject": "x", "accent": "#123456"}]}
    p = build_prompt(spec, ["ref.png"])
    assert "No text" in p and "a.png" in p and "STYLE REFERENCE" in p and "#123456" in p
    d = tempfile.mkdtemp()
    im = Image.new("RGB", (1024, 1024), (252, 252, 250))  # off-white noise like real generations
    ImageDraw.Draw(im).ellipse((100, 300, 500, 600), fill="#5A8BCB")
    im.save(os.path.join(d, "a.png"))
    out = tidy(os.path.join(d, "a.png"))
    assert out.size == (512, 512) and out.getpixel((2, 2)) == (255, 255, 255)
    assert out.getpixel((256, 256))[2] > 150  # the blue disc is now centred
    assert os.path.exists(sheet(d))
    shutil.rmtree(d)
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("selftest")
    for name in ("prompt", "generate"):
        s = sub.add_parser(name)
        s.add_argument("spec")
        s.add_argument("--ref", action="append", default=[])
        if name == "generate":
            s.add_argument("--out", required=True)
            s.add_argument("--model")
            s.add_argument("--timeout", type=int, default=1200)
    for name in ("tidy", "sheet"):
        sub.add_parser(name).add_argument("dir")
    a = ap.parse_args()
    if a.cmd == "check":
        ok, msg = check()
        print(msg)
        sys.exit(0 if ok else 1)
    elif a.cmd == "selftest":
        selftest()
    elif a.cmd == "prompt":
        print(build_prompt(load_spec(a.spec), a.ref))
    elif a.cmd == "generate":
        generate(a.spec, a.out, a.ref, a.model, a.timeout)
    elif a.cmd == "tidy":
        for f in sorted(os.listdir(a.dir)):
            if f.endswith(".png") and not f.startswith("_"):
                tidy(os.path.join(a.dir, f))
    elif a.cmd == "sheet":
        print(sheet(a.dir))


if __name__ == "__main__":
    main()
