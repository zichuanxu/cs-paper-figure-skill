#!/usr/bin/env python3
"""Render a concrete scene or context-update example outside the installed skill.

These are deterministic worked illustrations, not trained models or empirical
results. Copy the preserved fixture and editable source to --out, then run the
example there. Inspect its PDF after changing inputs, source, fonts or libraries.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


EXAMPLES = {
    "scene-planning": ("scene-planning-example", "render_figure.py", "scene_planning_figure"),
    "epoch-context": ("epoch-context-example", "source/render_figure.py", "epoch_context_update"),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("example", choices=EXAMPLES)
    parser.add_argument("--out", type=Path, required=True,
                        help="Output directory outside the installed skill; includes editable source and inputs.")
    args = parser.parse_args(argv)
    skill_root = Path(__file__).resolve().parents[1]
    asset_name, renderer, stem = EXAMPLES[args.example]
    assets = skill_root / "assets" / asset_name
    out = args.out.expanduser().resolve()
    if out == skill_root or skill_root in out.parents:
        parser.error("--out must be outside the installed skill")
    files = sorted(p for p in assets.rglob("*") if p.is_file()
                   and "__pycache__" not in p.parts and p.suffix != ".pyc")
    if not files or not (assets / renderer).is_file():
        raise FileNotFoundError(f"Incomplete bundled example: {assets}")
    source_hashes = {p.relative_to(assets).as_posix(): digest(p) for p in files}
    out.mkdir(parents=True, exist_ok=True)
    for path in files:
        target = out / path.relative_to(assets)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    env = dict(os.environ)
    env["MPLCONFIGDIR"] = str(out / ".matplotlib-cache")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run([sys.executable, str(out / renderer), "--out", str(out)],
                   check=True, cwd=out, env=env)
    if args.example == "scene-planning":
        subprocess.run([sys.executable, str(out / "validate_figure.py"), "--out", str(out)],
                       check=True, cwd=out, env=env)
    if source_hashes != {p.relative_to(assets).as_posix(): digest(p) for p in files}:
        raise RuntimeError("Bundled source changed during execution")
    exports = {ext: out / f"{stem}.{ext}" for ext in ("pdf", "svg", "png")}
    for path in exports.values():
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Missing export: {path}")
    result = {"example": args.example, "data_status": "deterministic illustration",
              "output_directory": str(out), "installed_bundle_unchanged": True,
              "source_sha256": source_hashes,
              "exports": {kind: {"path": path.name, "sha256": digest(path)}
                          for kind, path in exports.items()},
              "review_scope": "The bundled fixture was reviewed. Reinspect changed source, data, fonts or dependencies."}
    (out / "bundle_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
