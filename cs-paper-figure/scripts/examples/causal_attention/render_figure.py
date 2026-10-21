#!/usr/bin/env python3
"""Regenerate an original causal-cache attention figure from preserved inputs.

Usage: python <skill-root>/scripts/examples/causal_attention/render_figure.py
       [--out OUTPUT_DIRECTORY]
Default output: ./figures/causal_attention/ under the caller's working directory.
Dependencies: Python >=3.10, matplotlib, numpy, Pillow, PyMuPDF.
Shared helpers are resolved from the skill's scripts/ directory. The installed
example directory is read-only input; no output or runtime cache is stored there.
"""
from __future__ import annotations
import argparse
import os
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import platform
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SCRIPTS_ROOT = ROOT.parents[1]
# Reuse shared skill helpers without creating bytecode beside installed sources.
sys.dont_write_bytecode = True
sys.path.insert(0, str(SCRIPTS_ROOT))
if not os.environ.get('MPLCONFIGDIR'):
    os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp(prefix='cs-paper-figure-mpl-')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Polygon
import numpy as np
from PIL import Image
import fitz
from figure_scene import FigureScene, COLORS
from figure_style import style_context, export_figure

INK = '#243343'
MUTED = '#526170'
GRID = '#CAD3DC'
ROLES = {
    'prefix': ('#E9EFF8', '#365E91'),
    'summary': ('#EEEAF6', '#6C4E90'),
    'local': ('#E5F2EF', '#246D62'),
    'blocked': ('#F0F2F4', '#76818D'),
    'compute': ('#F2F5F8', '#344A63'),
}
COLORS.update(ROLES)
W, H = 178, 210


def derive(data):
    """One content source for tables, matrix, labels, and exact computations."""
    keys = data['key_order']
    queries = data['query_indices']
    fixed = set(data['prefix_keys']) | {s['id'] for s in data['completed_summaries']}
    permitted = [[(key in fixed) or (key.startswith('t') and int(key[1:]) <= i)
                  for key in keys] for i in queries]
    example = data['example']
    with localcontext() as ctx:
        ctx.prec = 60
        logits = list(map(Decimal, example['scaled_logits_decimal']))
        exps = [x.exp() for x in logits]
        normalizer = sum(exps)
        weights = [x / normalizer for x in exps]
        values = [[Decimal(v) for v in row] for row in example['value_vectors']]
        contributions = [[a * v for v in row] for a, row in zip(weights, values)]
        output = [sum(row[d] for row in contributions) for d in range(2)]
        results = {
            'precision_decimal_digits': 60,
            'exp_logits': [str(x) for x in exps],
            'softmax_normalizer': str(normalizer),
            'softmax_weights': [str(x) for x in weights],
            'weighted_value_contributions': [[str(x) for x in row] for row in contributions],
            'weighted_output': [str(x) for x in output],
            'weight_sum': str(sum(weights)),
        }
    mask = np.array(permitted, bool)
    numerical = {
        'schema_version': 1,
        'key_order': keys,
        'query_indices': queries,
        'permitted_mask': mask.astype(int).tolist(),
        'additive_mask': [[0 if v else '-Infinity' for v in row] for row in permitted],
        'permitted_counts': mask.sum(axis=1).tolist(),
        'q10_full_attention': [*results['softmax_weights'], '0', '0'],
        'q10': results,
    }
    q_index = queries.index(example['query_index'])
    assert [k for k, ok in zip(keys, mask[q_index]) if ok] == example['allowed_keys']
    assert mask.shape == (4, 8)
    assert mask.sum(axis=1).tolist() == [5, 6, 7, 8]
    assert np.all(mask[:, :4])
    assert np.array_equal(mask[:, 4:], np.tril(np.ones((4, 4), dtype=bool)))
    assert data['excluded_summary']['id'] not in keys
    assert set(data['excluded_summary']['excluded_from_queries']) == set(queries)
    w = np.array([float(v) for v in results['softmax_weights']])
    z = np.array(example['scaled_logits_decimal'], float)
    stable = np.exp(z - z.max()) / np.exp(z - z.max()).sum()
    out = w @ np.array(example['value_vectors'])
    assert np.allclose(w, stable, atol=1e-15, rtol=0)
    assert abs(float(sum(map(Decimal, results['softmax_weights']))) - 1) < 1e-15
    assert np.allclose(out, np.array(results['weighted_output'], float), atol=1e-15, rtol=0)
    numerical['checks'] = {
        'passed': True,
        'conditions': ['4 × 8 mask', '4 always-available columns', 'self-inclusive causal local block',
                       'row counts 5, 6, 7, 8', 'S3 absent from key bank for all four queries',
                       'q10 allowed-key identity', '60-digit decimal softmax agrees with stable float64 softmax',
                       'normalized positive weights', 'weighted result from preserved vectors'],
        'scope': 'Deterministic content checks; this is not an experiment or benchmark.'
    }
    return numerical



def write_caption_files(data, outdir, figure_pdf, font_file):
    """Export matched captions and a font-metric-based full-width fit proof.

    These are explicit layout assumptions, not a claim about a venue template:
    full 178 mm width, DejaVu Sans regular, 120% leading, 3 mm figure gap.
    """
    caption = data['caption'].strip()
    extended = data['extended_caption'].strip()
    (outdir / 'caption.txt').write_text(caption + '\n')
    (outdir / 'extended_caption.txt').write_text(extended + '\n')
    font = fitz.Font(fontfile=str(font_file))
    pt_per_mm = 72 / 25.4
    width_pt = W * pt_per_mm
    gap_mm, leading_ratio = 3.0, 1.2
    proof = fitz.open()
    artwork = fitz.open(figure_pdf)
    cases = []
    for font_size in (8.0, 9.0):
        lines = []
        current = ''
        for word in caption.split():
            candidate = f'{current} {word}'.strip()
            if current and font.text_length(candidate, fontsize=font_size) > width_pt:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        leading_pt = font_size * leading_ratio
        allocated_mm = len(lines) * leading_pt / pt_per_mm
        total_mm = H + gap_mm + allocated_mm
        page = proof.new_page(width=width_pt, height=240 * pt_per_mm)
        page.show_pdf_page(fitz.Rect(0, 0, width_pt, H * pt_per_mm), artwork, 0)
        writer = fitz.TextWriter(page.rect)
        first_baseline = (H + gap_mm) * pt_per_mm + font.ascender * font_size
        for i, line in enumerate(lines):
            writer.append((0, first_baseline + i * leading_pt), line,
                          font=font, fontsize=font_size)
        writer.write_text(page, color=(36/255, 51/255, 67/255))
        spans = [sp for block in page.get_text('dict')['blocks'] if 'lines' in block
                 for ln in block['lines'] for sp in ln['spans']
                 if sp['bbox'][1] >= (H + gap_mm - .1) * pt_per_mm]
        assert spans, 'Caption proof contains no extractable caption text'
        painted_bottom = max(sp['bbox'][3] for sp in spans) / pt_per_mm
        assert painted_bottom <= total_mm + .05
        cases.append({
            'font_size_pt': font_size,
            'leading_pt': leading_pt,
            'line_count': len(lines),
            'wrapped_lines': lines,
            'longest_line_width_mm': max(font.text_length(x, fontsize=font_size) for x in lines) / pt_per_mm,
            'allocated_caption_height_mm': allocated_mm,
            'measured_caption_height_mm': (max(sp['bbox'][3] for sp in spans) - min(sp['bbox'][1] for sp in spans)) / pt_per_mm,
            'artwork_plus_gap_plus_allocated_caption_mm': total_mm,
            'measured_bottom_from_page_top_mm': painted_bottom,
            'remaining_in_235_mm_block': 235 - total_mm,
            'remaining_in_240_mm_block': 240 - total_mm,
            'fits_235_mm_block': total_mm <= 235,
            'fits_240_mm_block': total_mm <= 240,
            'proof_page': len(cases) + 1,
        })
    proof.set_metadata({'title': 'Causal cache attention: caption-fit proof',
                        'author': '', 'subject': '8 pt and 9 pt captions at full 178 mm width',
                        'keywords': '', 'creator': 'cs-paper-figure', 'producer': ''})
    proof.save(outdir / 'caption_fit_proof.pdf', deflate=True)
    proof.close()
    artwork.close()
    report = {
        'schema_version': 1,
        'caption_word_count': len(caption.split()),
        'extended_caption_word_count': len(extended.split()),
        'artwork_dimensions_mm': [W, H],
        'caption_width_mm': W,
        'gap_mm': gap_mm,
        'font_family': 'DejaVu Sans',
        'font_weight': 'regular',
        'font_file': str(font_file),
        'font_sha256': hashlib.sha256(Path(font_file).read_bytes()).hexdigest(),
        'font_ascender_em': font.ascender,
        'font_descender_em': font.descender,
        'leading_ratio': leading_ratio,
        'method': 'Greedy word wrapping from actual TrueType advance widths; 120% baseline leading; reserve one leading interval per line. Verify painted caption bounds in a two-page PDF proof.',
        'conditions': cases,
        'limitation': 'This is an approximate manuscript-fit calculation for the stated font, full width, gap and leading. A real template can use different fonts, bold caption labels, indentation, margins, leading or float spacing. Verify in the actual template. The extended caption is a companion interpretation and is not intended to fit beneath this full-height artwork.',
        'proof_pdf': 'caption_fit_proof.pdf',
    }
    (outdir / 'caption_fit.json').write_text(json.dumps(report, indent=2) + '\n')
    rows = '\n'.join(
        f"| {c['font_size_pt']:.0f} pt | {c['leading_pt']:.1f} pt | {c['line_count']} | "
        f"{c['allocated_caption_height_mm']:.2f} mm | "
        f"{c['artwork_plus_gap_plus_allocated_caption_mm']:.2f} mm | "
        f"{c['remaining_in_235_mm_block']:.2f} mm | {c['remaining_in_240_mm_block']:.2f} mm |"
        for c in cases)
    note = (
        '# Caption fit at manuscript width\n\n'
        f'The main caption contains **{len(caption.split())} words**. The complete '
        f'**{len(extended.split())}-word** interpretation is preserved verbatim in '
        '`extended_caption.txt`. The artwork remains **178 × 210 mm**.\n\n'
        'The calculation uses the actual DejaVu Sans regular TrueType program, '
        'a full **178 mm** caption width, **120% leading**, and a **3 mm** gap after '
        'the artwork. Word wrapping uses measured glyph advances, not a characters-per-line estimate. '
        'The two-page proof uses these same settings and confirms the painted caption bounds.\n\n'
        '| Caption font | Leading | Lines | Reserved caption height | Artwork + gap + caption | Space in 235 mm block | Space in 240 mm block |\n'
        '|---|---|---|---|---|---|---|\n' + rows + '\n\n'
        'The reserved height is one leading interval per line; the JSON also records '
        'the measured painted bounds. Proof page 1 uses 8 pt and page 2 uses 9 pt.\n\n'
        '**Template limitation:** this is an approximate fit under explicit assumptions. '
        'A real template may change the caption font, label weight, indent, width, '
        'leading or float spacing. Verify the assembled figure in that template. '
        'The extended caption is a companion interpretation, not an under-figure caption '
        'for a 235–240 mm text block.\n')
    (outdir / 'caption_fit.md').write_text(note)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--out', type=Path, default=Path.cwd() / 'figures' / 'causal_attention',
        help='Output directory (default: ./figures/causal_attention/).')
    args = parser.parse_args()
    outdir = args.out.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT / 'inputs.json').read_text())
    nums = derive(data)
    (outdir / 'numerical_checks.json').write_text(json.dumps(nums, indent=2) + '\n')
    family = 'DejaVu Sans'
    regular = font_manager.findfont(font_manager.FontProperties(family=family, weight='normal'), fallback_to_default=False)
    bold = font_manager.findfont(font_manager.FontProperties(family=family, weight='bold'), fallback_to_default=False)
    assert Path(regular).suffix.lower() == '.ttf' and Path(bold).suffix.lower() == '.ttf'

    with style_context(font_size=7.8):
        s = FigureScene(W, H, family=family)
        ax = s.ax
        shift = 0

        def T(x, y, value, size=7.6, weight='normal', color=INK, ha='left', owner=None, tag=None, **kw):
            return s.text(x, H-(y-shift), value, size=size, weight=weight, color=color, ha=ha, owner=owner, tag=tag, **kw)

        def rect(x, y, w, h, fill='white', edge=GRID, lw=.55, radius=0, hatch=None, z=1):
            if radius:
                patch = FancyBboxPatch((x,H-(y-shift)-h), w,h, boxstyle=f'round,pad=0,rounding_size={radius}',
                                      facecolor=fill, edgecolor=edge, linewidth=lw, hatch=hatch, zorder=z)
            else:
                patch = Rectangle((x,H-(y-shift)-h),w,h,facecolor=fill,edgecolor=edge,linewidth=lw,hatch=hatch,zorder=z)
            ax.add_patch(patch)
            return patch

        def line(points, color=GRID, width=.55, style='-', z=3):
            s.line([(x,H-(y-shift)) for x,y in points], color=color, width=width, style=style, zorder=z)

        def node(id, x,y,w,h,role='compute',fill='white',shape='process'):
            return s.node(id,x,H-(y-shift)-h,w,h,role=role,shape=shape,fill=fill)

        def panel(letter, title, y, note=None):
            T(4, y, letter, size=10, weight='bold')
            T(10, y, title, size=9.4, weight='bold')
            if note: T(174,y,note,size=7.2,color=MUTED,ha='right')

        def glyph_token(x,y,w,h,label,role,owner=None,split=False):
            fill,ink=ROLES[role]
            rect(x,y,w,h,fill,ink,lw=.75,radius=.75,z=4)
            if split:
                line([(x,y+h*.54),(x+w,y+h*.54)],color=ink,width=.4,z=5)
                T(x+w/2,y+h*.28,label,size=8.0,weight='bold',color=ink,ha='center',owner=owner)
                T(x+w/2,y+h*.78,'k | v',size=7.2,color=ink,ha='center',owner=owner)
            else:
                T(x+w/2,y+h/2,label,size=7.2,color=ink,ha='center',owner=owner)

        # A: source provenance -> canonical key/value bank -> operator.
        panel('a','Canonical cache slots and read operator',6,'SCHEMATIC')
        T(23,12.5,'Prefix',size=8.4,weight='bold',color=ROLES['prefix'][1],ha='center')
        T(69,12.5,'Completed-chunk summaries',size=8.4,weight='bold',color=ROLES['summary'][1],ha='center')
        T(136,12.5,'Current chunk: local keys',size=8.4,weight='bold',color=ROLES['local'][1],ha='center')
        T(23,21,'Always available',size=7.2,color=MUTED,ha='center')
        T(136,21,'Only tokens at or before the query',size=7.2,color=MUTED,ha='center')
        # Raw token slots are provenance for the summaries, not extra keys.
        for sid,start,cx in [('S1',1,57),('S2',5,81)]:
            x=cx-10.2
            node('source_'+sid,x,18,20.4,6,role='summary',shape='data',fill='white')
            for j in range(4):
                if j: line([(x+j*5.1,18),(x+j*5.1,24)],color=ROLES['summary'][1],width=.35)
                T(x+j*5.1+2.55,21,f't{start+j}',size=7.2,color=ROLES['summary'][1],ha='center',owner='source_'+sid)
        node('cache',6,27,166,10.4,role='compute',shape='state',fill='#FAFBFC')
        positions=[16,34,57,81,108,126,144,162]
        for key,cx in zip(data['key_order'],positions):
            role = 'prefix' if key.startswith('P') else 'summary' if key.startswith('S') else 'local'
            glyph_token(cx-6.5,27.8,13,8.8,key,role,owner='cache',split=True)
        for sid,cx in [('S1',57),('S2',81)]:
            s.connect('compress_'+sid,('source_'+sid,'bottom'),('cache','top',(cx-6)/166),role='summary')
        T(6,40.5,'Each slot stores a key k and a value v.',size=7.2,color=MUTED)
        T(173,40.5,'K: 8 × dₖ    V: 8 × dᵥ',size=7.6,color=MUTED,ha='right')
        node('queries',6,44.5,47,10.8,role='local',fill='white')
        T(29.5,48,'Q = [q9, q10, q11, q12]',size=8.0,weight='bold',ha='center',owner='queries')
        T(29.5,52.3,'4 queries × dₖ',size=7.2,color=MUTED,ha='center',owner='queries')
        node('attention',69,44.5,54,10.8,role='compute',fill='role')
        T(96,48,'Masked attention',size=8.5,weight='bold',ha='center',owner='attention')
        T(96,52.3,'Mask (b) · worked q10 (c)',size=7.2,color=MUTED,ha='center',owner='attention')
        node('output',141,44.5,31,10.8,role='compute',fill='white')
        T(156.5,48,'O = AV',size=8.5,weight='bold',ha='center',owner='output')
        T(156.5,52.3,'4 × dᵥ',size=7.2,color=MUTED,ha='center',owner='output')
        s.connect('query_read',('queries','right'),('attention','left'),role='local',width=.95)
        s.connect('cache_read',('cache','bottom',(96-6)/166),('attention','top'),role='compute',width=.95)
        s.connect('attention_output',('attention','right'),('output','left'),role='compute',width=.95)
        line([(4,59),(174,59)],width=.55)

        # B: explicit indexed additive mask, with q10 registered to panel C.
        shift = 8.5
        panel('b','Indexed additive mask M: 4 queries × 8 keys',73)
        x0,y0,cw,ch = 24,87,10.4,5.5
        groups=[('Prefix',0,2,'prefix'),('Completed',2,2,'summary'),('Local causal block',4,4,'local')]
        for label,j,n,role in groups:
            xx=x0+j*cw
            T(xx+n*cw/2,79,label,size=7.6,weight='bold',color=ROLES[role][1],ha='center')
            line([(xx+.5,82),(xx+n*cw-.5,82)],color=ROLES[role][1],width=1)
        T(6,85,'Query',size=7.2,color=MUTED)
        for j,key in enumerate(data['key_order']):
            role='prefix' if j<2 else 'summary' if j<4 else 'local'
            T(x0+(j+.5)*cw,84.5,key,size=7.7,weight='bold',color=ROLES[role][1],ha='center')
        for row,q in enumerate(data['query_indices']):
            cy=y0+(row+.5)*ch
            if q==10:
                rect(6,cy-2.7,13,5.4,INK,INK,lw=.7,radius=.65,z=6)
                T(12.5,cy,'q10',size=7.8,weight='bold',color='white',ha='center')
            else:
                T(18,cy,f'q{q}',size=7.8,ha='right')
            for col,ok in enumerate(nums['permitted_mask'][row]):
                role='prefix' if col<2 else 'summary' if col<4 else 'local'
                fill=ROLES[role][0] if ok else ROLES['blocked'][0]
                rect(x0+col*cw,y0+row*ch,cw,ch,fill,GRID,lw=.4,hatch=None if ok else '///')
                T(x0+(col+.5)*cw,cy,'0' if ok else '−∞',size=7.6,color=INK,ha='center')
        # Block boundaries and q10's complete row are visibly encoded without hue.
        for j in [0,2,4,8]:
            line([(x0+j*cw,y0),(x0+j*cw,y0+4*ch)],color='#8B98A5',width=.75)
        rect(x0,y0+ch,8*cw,ch,'none',INK,lw=1.15,z=5)
        T(111,y0+1.5*ch,'c',size=8.0,weight='bold',ha='center')
        line([(108.2,y0+1.5*ch),(109.2,y0+1.5*ch)],color=INK,width=.9)
        rect(24,112,3,3,ROLES['local'][0],GRID,lw=.4)
        T(29,113.5,'0: permitted',size=7.2,color=MUTED)
        rect(60,112,3,3,ROLES['blocked'][0],GRID,lw=.4,hatch='///')
        T(65,113.5,'−∞: blocked',size=7.2,color=MUTED)
        T(119,80,'Read set for query i',size=8.2,weight='bold')
        T(119,86,'{P0, P1, S1, S2,',size=7.8)
        T(119,90.8,'  t9, …, ti},  i = 9…12',size=7.8)
        T(119,97,'Local rule: token index ≤ i',size=7.2,color=MUTED)
        T(119,104,'L = QKᵀ / √dₖ   [4 × 8]',size=8.0)
        T(119,109.8,'A = rowsoftmax(L + M)',size=8.0)
        T(119,115.6,'O = AV   [4 × dᵥ]',size=8.0)
        line([(4,118),(174,118)],width=.55)

        # C: supplied logits -> exact softmax -> 2D contribution ledger + value plane.
        shift = 10.5
        panel('c','q10: normalize six logits, then combine six values',126,'NUMERICAL ILLUSTRATION')
        table_x, edges = 6,[6,21,33,53,72,93,114]
        centers=[(a+b)/2 for a,b in zip(edges[:-1],edges[1:])]
        headers=['Key','Logit ℓ','Weight a','Value v','a · v₁','a · v₂']
        rect(6,131,108,6,'#F4F6F8',edge='none')
        for cx,label in zip(centers,headers): T(cx,134,label,size=7.2,weight='bold',ha='center')
        weights=np.array(nums['q10']['softmax_weights'],float)
        values=np.array(data['example']['value_vectors'],float)
        contributions=np.array(nums['q10']['weighted_value_contributions'],float)
        for r,(key,z,w,v,cv) in enumerate(zip(data['example']['allowed_keys'],data['example']['scaled_logits_decimal'],weights,values,contributions)):
            cy=140.1+5.2*r
            role='prefix' if key.startswith('P') else 'summary' if key.startswith('S') else 'local'
            rect(6,cy-2.6,15,5.2,ROLES[role][0],edge='none')
            for cx,value,size,col,bolded in [
                (centers[0],key,8.0,ROLES[role][1],True),
                (centers[1],z,7.8,INK,False),
                (centers[2],f'{w:.6f}',7.6,INK,False),
                (centers[3],f'({v[0]:.0f}, {v[1]:.0f})',7.6,INK,False),
                (centers[4],f'{cv[0]:.6f}',7.2,INK,False),
                (centers[5],f'{cv[1]:.6f}',7.2,INK,False)]:
                T(cx,cy,value,size=size,color=col,weight='bold' if bolded else 'normal',ha='center')
            line([(6,cy+2.6),(114,cy+2.6)],width=.35)
        for x in [21,53,72]: line([(x,131),(x,168.7)],width=.4)
        T(6,173.5,'a = exp(ℓ) / Z;  Z = Σ exp(ℓ) = 14.323370484364…',size=7.4)
        ox,oy=map(float,nums['q10']['weighted_output'])
        T(6,178.5,f'o10 = Σ a · v = ({ox:.6f}, {oy:.6f})',size=8.6,weight='bold')
        T(6,183.4,'Σ a = 1.  Masked t11 and t12 receive weight 0.  Displayed decimals are rounded.',size=7.2,color=MUTED)

        # Editable value-space inset; this reuses the table's numerical inputs.
        T(147,134,'Permitted values: 6 × 2',size=7.8,weight='bold',ha='center')
        px,py,pw,ph=122,139,49,35
        # Map [-1.3, 2.3] × [-0.3, 2.3] into the physical canvas.
        def xy(vx,vy): return px+(vx+1.3)/3.6*pw, py+ph-(vy+.3)/2.6*ph
        for k in [-1,0,1,2]:
            x,_=xy(k,0); yb=xy(0,0)[1]
            line([(x,yb-.6),(x,yb+.6)],color='#7E8B98',width=.45)
            T(x,yb+2.8,str(k),size=7.2,color=MUTED,ha='center')
        for k in [1,2]:
            xx,yy=xy(0,k)
            line([(xx-.6,yy),(xx+.6,yy)],color='#7E8B98',width=.45)
            T(xx-2.2,yy,str(k),size=7.2,color=MUTED,ha='right')
        line([xy(-1.3,0),xy(2.3,0)],color='#7E8B98',width=.55)
        line([xy(0,-.3),xy(0,2.3)],color='#7E8B98',width=.55)
        T(172,xy(0,0)[1]+2.8,'v₁',size=7.5,ha='left')
        T(xy(0,0)[0]-2.5,137.5,'v₂',size=7.5,ha='right')
        offsets={'P0':(1.8,-3.4),'P1':(-4,-2.7),'S1':(1.6,-3.5),'S2':(-.2,-3.5),'t9':(1.5,-3.4),'t10':(5,-.5)}
        for key,v in zip(data['example']['allowed_keys'],values):
            role='prefix' if key.startswith('P') else 'summary' if key.startswith('S') else 'local'
            x,y=xy(*v); sx,sy=xy(0,0)
            line([(sx,sy),(x,y)],color=ROLES[role][1],width=.55,z=2)
            marker={'prefix':'s','summary':'^','local':'o'}[role]
            ax.plot(x,H-(y-shift),marker=marker,markersize=4.4,markerfacecolor=ROLES[role][0],markeredgecolor=ROLES[role][1],markeredgewidth=.8,zorder=6)
            dx,dy=offsets[key]
            T(x+dx,y+dy,key,size=7.2,color=ROLES[role][1],ha='center')
        sx,sy=xy(0,0); ex,ey=xy(ox,oy)
        ax.add_patch(FancyArrowPatch((sx,H-(sy-shift)),(ex,H-(ey-shift)),arrowstyle='-|>',mutation_scale=9,linewidth=1.3,color=INK,shrinkA=0,shrinkB=0,zorder=7))
        ax.plot(ex,H-(ey-shift),'o',ms=3.3,color=INK,zorder=8)
        T(ex+4.4,ey+3.5,'o10',size=7.8,weight='bold',ha='center')
        T(147,178.5,'2D value space, dᵥ = 2',size=7.2,color=MUTED,ha='center')
        line([(4,187),(174,187)],width=.55)

        # D: the availability boundary is explicit, and S3 has no current-chunk read edge.
        shift = 16.5
        panel('d','A current-chunk summary is withheld until finalization',198)
        for j,q in enumerate(data['query_indices']):
            x=6+j*27
            node(f'stream_q{q}',x,202.5,17,7,role='local',fill='role')
            T(x+8.5,206,f'q{q}',size=8.0,weight='bold' if q==10 else 'normal',color=ROLES['local'][1],ha='center',owner=f'stream_q{q}')
            if j:
                s.connect(f'advance_{q}',(f'stream_q{q-1}','right'),(f'stream_q{q}','left'),role='local',width=.85)
        rect(6,214,98,8,ROLES['blocked'][0],ROLES['blocked'][1],lw=.6,radius=.8,hatch='///')
        rect(11.5,215.7,87,4.6,ROLES['blocked'][0],edge='none',z=5)
        T(55,218,'S3 ∉ K for every query q9–q12',size=7.8,weight='bold',ha='center')
        line([(114,202.5),(114,224)],color='#778593',width=.85,style=(0,(3,2)))
        T(114,211,'Seal',size=7.2,weight='bold',ha='center',bbox=dict(facecolor='white',edgecolor='none',pad=1.3))
        node('finalize',124,202.5,48,7,role='summary',fill='white')
        T(148,206,'Form S3 from t9–t12',size=8.0,weight='bold',color=ROLES['summary'][1],ha='center',owner='finalize')
        s.connect('seal_then_finalize',('stream_q12','right'),('finalize','left'),role='compute',width=.85)
        node('summary3',124,214.5,16,7,role='summary',shape='data',fill='role')
        T(132,218,'S3',size=8.0,weight='bold',color=ROLES['summary'][1],ha='center',owner='summary3')
        s.connect('publish_S3',('finalize','bottom',(132-124)/48),('summary3','top'),role='summary',width=.9)
        T(144,216.3,'Eligible for',size=7.2,color=MUTED)
        T(144,220.3,'later reads',size=7.2,color=MUTED)
        # A scope label makes the barrier semantic rather than a computational edge.
        s.correspondences=[
            {'object':'K/V canonical slot order','panels':['a','b','c'],'meaning':'Same identifiers and order; panel c instantiates only the q10 permitted subset.'},
            {'object':'q10','panels':['a','b','c','d'],'meaning':'Highlighted mask row, six-row ledger, output and streaming read.'},
            {'object':'S3','panels':['a','b','d'],'meaning':'Absent from a/b key bank; only the after-seal finalization makes it eligible for subsequent reads.'}
        ]
        audit=s.audit(outdir/'geometry_checks.json',label_clearance_mm=.22)
        s.write_spec(outdir/'scene.json')
        # Record rather than suppress any geometry finding; the handoff requires a clean audit.
        sources=[ROOT/'render_figure.py', ROOT/'inputs.json',
                 SCRIPTS_ROOT/'figure_style.py', SCRIPTS_ROOT/'figure_scene.py',
                 SCRIPTS_ROOT/'diagram_geometry.py']
        metadata={
            'data_status':data['evidence_status'],
            'claim':'Prefix and completed summaries are always visible; local keys use a self-inclusive causal mask; S3 is unavailable to its source chunk.',
            'font':{'intended':family,'actual':family,'regular_file':regular,'bold_file':bold,'weights':['normal','bold'],'svg_font_dependency':family,'minimum_pt':7.2},
            'palette':ROLES,
            'inputs':str(ROOT/'inputs.json'),
            'renderer':str(ROOT/'render_figure.py'),
            'shared_helper_root':str(SCRIPTS_ROOT),
            'numerical_checks':'numerical_checks.json','geometry_checks':'geometry_checks.json',
            'caption':'caption.txt','extended_caption':'extended_caption.txt','caption_fit':'caption_fit.json',
            'source_references':[
                {'paper':'Fast Byte Latent Transformer','figure':'Figure 5','pdf_page':9,'version':'2605.08044v1','job':'A compact overview linked to exact mask views with the same token identities.'},
                {'paper':'Wan-Animate-2','figure':'Figure 1','pdf_page':5,'version':'2608.06009v1','job':'Overview, representation, and operator presented as connected explanatory levels.'}
            ],
            'geometry_summary':{'text_findings':len(audit['text_findings']), 'route_report':audit['route_report']},
            'limitations':['Original conceptual operator, not a claim about either reference architecture.','The summarization function and Q/K projections are intentionally unspecified.','All numerical inputs are illustrative.']
        }
        files=export_figure(s.fig,outdir/'causal_cache_attention',source_files=sources,metadata=metadata,dpi=300)
        plt.close(s.fig)

    # Render the exported PDF, not the matplotlib preview, for independent visual review.
    doc=fitz.open(files['pdf'])
    page=doc[0]
    pix=page.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
    pix.save(outdir/'pdf_render.png')
    Image.open(outdir/'pdf_render.png').convert('L').save(outdir/'grayscale.png')
    spans=[span for block in page.get_text('dict')['blocks'] if 'lines' in block for line_ in block['lines'] for span in line_['spans']]
    pdfcheck={
        'width_mm':page.rect.width*25.4/72,'height_mm':page.rect.height*25.4/72,
        'text_span_count':len(spans),'minimum_text_span_pt':min(x['size'] for x in spans),
        'fonts':page.get_fonts(full=True),
        'svg_has_editable_text':'<text' in Path(files['svg']).read_text(),
        'pdf_raster_image_count':len(page.get_images()),
        'actual_pdf_render':'pdf_render.png','grayscale_render':'grayscale.png',
    }
    assert abs(pdfcheck['width_mm']-178)<.01
    assert pdfcheck['minimum_text_span_pt'] >= 7.19
    assert pdfcheck['svg_has_editable_text']
    (outdir/'export_checks.json').write_text(json.dumps(pdfcheck,indent=2)+'\n')
    caption_fit = write_caption_files(data, outdir, files['pdf'], regular)
    print(json.dumps({'exports':files,'text_findings':audit['text_findings'],'route_report':audit['route_report'],'pdf_checks':pdfcheck,'caption_fit':caption_fit['conditions']},indent=2))

if __name__=='__main__': main()
