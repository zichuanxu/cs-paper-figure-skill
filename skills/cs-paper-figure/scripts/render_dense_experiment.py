#!/usr/bin/env python3
"""Build the rich synthetic memory-policy example outside the installed skill.

The bundle contains a frozen configuration, independent seed manifest and source
snapshots. It generates raw observations, runs paired seed-block inference, and
exports an exact-size four-panel PDF/SVG/PNG with captions and numerical QA.
Every value is SYNTHETIC DATA; this is not evidence about real agents.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path,
                        help='Output folder outside the installed skill; source and input snapshots are copied here.')
    args=parser.parse_args(argv)
    skill_root=Path(__file__).resolve().parents[1]
    asset_root=skill_root/'assets/experimental-example'
    out=args.out.expanduser().resolve()
    if out==skill_root or skill_root in out.parents:
        parser.error('--out must be outside the installed skill so generated data and caches never modify it')
    expected=json.loads((asset_root/'expected_summary.json').read_text())
    files=sorted(p for p in asset_root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    before={str(p.relative_to(asset_root)):digest(p) for p in files}
    out.mkdir(parents=True,exist_ok=True)
    (out/'qa').mkdir(exist_ok=True)
    for path in files:
        dest=out/path.relative_to(asset_root)
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,dest)
    seed_hash=digest(out/'inputs/seed_manifest.json')
    # Both subprocesses import only source snapshots in the output directory.
    # The renderer invokes analyze.py on the preserved raw observations.
    subprocess.run([sys.executable,str(out/'source/make_data.py')],check=True,cwd=out)
    subprocess.run([sys.executable,str(out/'source/render_figure.py')],check=True,cwd=out)
    analysis=json.loads((out/'analysis.json').read_text())
    export=json.loads((out/'qa/export_checks.json').read_text())
    pdf=json.loads((out/'qa/pdf_checks.json').read_text())
    caption=json.loads((out/'qa/caption_fit.json').read_text())
    actual={'data_status':'SYNTHETIC DATA','primary_effect_pp':analysis['contrasts'][0]['mean'],
        'primary_ci_pp':[analysis['contrasts'][0]['lo'],analysis['contrasts'][0]['hi']],
        'history_ablation_effect_pp':analysis['contrasts'][1]['mean'],
        'history_ablation_ci_pp':[analysis['contrasts'][1]['lo'],analysis['contrasts'][1]['hi']],
        'independent_seed_blocks':analysis['config']['n_seeds'],
        'shared_scenarios':analysis['shared_scenario_count'],'outcome_rows':analysis['raw_observation_count'],
        'dimensions_mm':[export['width_mm'],export['height_mm']],
        'min_font_pt':export['minimum_pdf_font_pt'],'caption_word_count':caption['caption_word_count']}
    if actual!=expected:
        raise RuntimeError('The regenerated fixture differs from its frozen expected summary: '+json.dumps(actual))
    if seed_hash!=digest(out/'inputs/seed_manifest.json'):
        raise RuntimeError('The generated independent-seed manifest differs from its preserved snapshot')
    if before!={str(p.relative_to(asset_root)):digest(p) for p in files}:
        raise RuntimeError('The installed source asset bundle was unexpectedly modified')
    if not pdf['automated_checks_passed'] or not export['all_vector_pdf']:
        raise RuntimeError('The regenerated export failed its numerical/font/vector checks')
    check={'expected_summary_matches':True,'seed_manifest_matches':True,
        'installed_bundle_unchanged':True,'pdf_checks_pass':True,'pdf_is_all_vector':True,
        'asset_sha256':before,'actual_summary':actual,
        'visual_review_scope':'The frozen fixture was visually reviewed in the bundled reference environment. Inspect regenerated PDF/grayscale after any source, data, font or dependency change.'}
    (out/'qa/bundled_example_checks.json').write_text(json.dumps(check,indent=2)+'\n')
    print(json.dumps({'out':str(out),'summary':actual,
        'primary_outputs':[str(out/f'memory_policy_study.{ext}') for ext in ['pdf','svg','png']],
        'caption_fit_mm':{str(s['font_pt']):s['artwork_gap_caption_height_mm'] for s in caption['sizes']}},indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
