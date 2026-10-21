"""Render two original modern research-figure recipes with explicit provenance.

Run: python render_modern_examples.py --out /path/to/output

Uses measured visual principles from Harness² (2026, Figures 2/3) and Cosmos 3
(2026, Figure 5), not their artwork, architecture, or experimental results.
The architecture preserves the original demonstration's seven declared edges.
All quantitative observations are newly constructed synthetic data.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.path import Path as MplPath
import numpy as np

from figure_style import export_figure, style_context
from diagram_geometry import Rect, Node, Port, Route, Label, port_point, validate_diagram

SEED = 20261021
P = {
    'ink': '#273449', 'muted': '#647083', 'grid': '#E4E9EF',
    'blue': '#2F5597', 'blue_tint': '#E3EBF6', 'blue_line': '#AFC1DE',
    'green': '#4F7D58', 'green_tint': '#E9F0E7', 'green_line': '#B5CDB3',
    'amber': '#AD6A30', 'amber_tint': '#FFF0DE', 'amber_line': '#E1BD90',
    'purple': '#7B5FB5', 'purple_tint': '#F1ECF8', 'purple_line': '#C9B9E2',
}


def select_fonts():
    """Require real regular/bold TrueType faces for Matplotlib's Type 42 export.

    CFF OpenType fonts can look correct on screen while this backend labels their
    PDF resources as TrueType. Prefer verified TrueType programs to avoid that
    format mismatch; a different production backend may support CFF correctly.
    """
    for path in [
        '/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf',
        '/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf',
        '/usr/share/fonts/opentype/urw-base35/NimbusMonoPS-Regular.otf',
    ]:
        if Path(path).is_file():
            font_manager.fontManager.addfont(path)
    def true_type(path):
        return Path(path).read_bytes()[:4] in (b'\x00\x01\x00\x00', b'true')

    for family in ('Liberation Sans', 'DejaVu Sans'):
        try:
            regular = font_manager.findfont(font_manager.FontProperties(family=family, weight='normal'), fallback_to_default=False)
            bold = font_manager.findfont(font_manager.FontProperties(family=family, weight='bold'), fallback_to_default=False)
            if regular != bold and true_type(regular) and true_type(bold):
                break
        except ValueError:
            continue
    else:
        raise RuntimeError('A real regular/bold TrueType font pair is required.')
    for mono in ('Liberation Mono', 'DejaVu Sans Mono'):
        try:
            mono_regular = font_manager.findfont(font_manager.FontProperties(family=mono), fallback_to_default=False)
            mono_bold = font_manager.findfont(font_manager.FontProperties(family=mono, weight='bold'), fallback_to_default=False)
            if mono_regular != mono_bold and true_type(mono_regular) and true_type(mono_bold):
                break
        except ValueError:
            continue
    else:
        raise RuntimeError('A real regular/bold monospace TrueType font pair is required.')
    return family, mono, {'family': family, 'regular_file': regular, 'bold_file': bold, 'monospace': mono,
                         'monospace_regular_file': mono_regular, 'monospace_bold_file': mono_bold,
                         'pdf_font_strategy': 'Verified TrueType programs with Matplotlib pdf.fonttype=42'}


def rounded_box(ax, x, y, w, h, *, fill='white', edge=None, lw=.7, radius=1.5, zorder=2):
    patch = FancyBboxPatch((x, y), w, h,
                          boxstyle=f'round,pad=0,rounding_size={radius}',
                          facecolor=fill, edgecolor=edge or P['blue_line'],
                          linewidth=lw, zorder=zorder)
    ax.add_patch(patch)
    return patch


def write_package(fig, out, stem, data, caption, alt, metadata, extra_sources=()):
    source = out / f'{stem}.data.json'
    source.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
    (out / f'{stem}.caption.md').write_text(caption + '\n', encoding='utf-8')
    (out / f'{stem}.alt.txt').write_text(alt + '\n', encoding='utf-8')
    paths = export_figure(fig, out / stem,
                         source_files=(source, Path(__file__), Path(__file__).with_name('figure_style.py'), *extra_sources),
                         metadata={**metadata, 'caption': caption, 'alt_text': alt}, dpi=360)
    plt.close(fig)
    return paths


def architecture(out, fonts):
    W, H = 178, 118
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, W), ylim=(0, H))
    ax.axis('off')
    labels = []

    def xy(x, y):
        return x, H-y

    def text(x, y, s, size=8, color=None, weight='normal', ha='left', family=None, route_label=False, **kw):
        artist = ax.text(*xy(x, y), s, va='center', ha=ha, fontsize=size,
                         color=color or P['ink'], fontweight=weight,
                         fontfamily=family or fonts[0], zorder=7, **kw)
        labels.append((s, artist))
        return artist

    def box(x, y, w, h, **kw):
        return rounded_box(ax, x, H-y-h, w, h, **kw)

    text(7, 6.5, 'A versioned memory loop for tool-using agents', size=11, weight='bold')
    text(171, 6.5, 'SCHEMATIC', size=7.2, color=P['muted'], ha='right')
    text(7, 12, 'An original example with distinct data, observation, and update routes', size=7.6, color=P['muted'])

    # A group is a semantic region, not a node obstacle: internal routes cross it.
    box(6, 18, 166, 52, fill='#F4F7FC', edge=P['blue_line'], lw=.65, radius=2.2, zorder=0)
    text(10, 22.4, '01', size=7.8, weight='bold', color=P['blue'])
    text(17, 22.4, 'RUNTIME', size=8.1, weight='bold', color=P['blue'])
    text(167, 22.4, 'One task and its tool loop', size=7.1, color=P['muted'], ha='right')

    layouts = {
        'query': (12, 46, 32, 16), 'controller': (61, 42, 54, 22),
        'tools': (139, 46, 27, 16), 'answer': (75, 28, 26, 8),
        'memory': (20, 85, 67, 26), 'update': (109, 85, 57, 26),
    }
    nodes = [Node(k, Rect(x, H-y-h, x+w, H-y)) for k, (x,y,w,h) in layouts.items()]
    box(*layouts['query'], fill='white', edge=P['blue_line'], radius=1.4)
    text(16, 51, 'Query', size=8.8, weight='bold')
    text(16, 57, 'task + context', size=7.2, color=P['muted'])

    box(*layouts['controller'], fill='white', edge=P['purple'], lw=.9, radius=1.8)
    text(65, 47.2, 'Agent controller', size=9.4, weight='bold', color=P['purple'])
    for x, w, label, role in [(65, 14.5, 'query', 'blue'), (81, 15, 'memory', 'green'), (97.5, 13.5, 'tools', 'purple')]:
        box(x, 53.1, w, 6.3, fill=P[role+'_tint'], edge='none', radius=.8, lw=0)
        text(x+w/2, 56.3, label, size=7.2, color=P[role], ha='center')

    box(*layouts['tools'], fill='white', edge=P['blue'], radius=1.4, lw=.8)
    text(143, 51, 'Tools', size=8.8, weight='bold', color=P['blue'])
    text(143, 57, 'API / files', size=7.2, color=P['muted'])
    box(*layouts['answer'], fill='white', edge=P['purple_line'], radius=1.2, lw=.7)
    text(88, 32, 'Answer', size=8.1, weight='bold', ha='center')

    text(10, 79.7, '02', size=7.8, weight='bold', color=P['green'])
    text(17, 79.7, 'PERSISTENT STATE', size=8.1, weight='bold', color=P['green'])
    box(*layouts['memory'], fill=P['green_tint'], edge=P['green'], lw=.8, radius=1.8)
    text(24, 90, 'Memory store', size=9, weight='bold', color=P['green'])
    box(24, 94.5, 59, 12.4, fill='white', edge=P['green_line'], lw=.55, radius=1.0)
    text(27, 98, 'record_07', size=7.2, family=fonts[1])
    text(79.5, 98, 'rev. 2', size=7, family=fonts[1], ha='right', color=P['green'])
    text(27, 103.6, 'source: tool observation', size=7, family=fonts[1], color=P['muted'])

    box(*layouts['update'], fill=P['amber_tint'], edge=P['amber'], lw=.8, radius=1.8)
    text(113, 90, 'Update rule', size=9, weight='bold', color=P['amber'])
    box(113, 94.5, 22, 12.4, fill='white', edge=P['amber_line'], lw=.55, radius=1.0)
    box(139, 94.5, 23, 12.4, fill='white', edge=P['amber_line'], lw=.55, radius=1.0)
    text(124, 98, 'Resolve', size=7.6, ha='center', weight='bold')
    text(150.5, 98, 'Version', size=7.6, ha='center', weight='bold')
    # Two evidence strands converge; a version pair summarizes the second operation.
    for y in (102.5, 104.5):
        ax.plot([117,120.3,123], [H-y,H-y,H-103.5], color=P['amber'], lw=.8, zorder=5)
    ax.plot([123,130.5], [H-103.5,H-103.5], color=P['amber'], lw=.8, zorder=5)
    text(143.9, 103.6, 'v1', size=7, family=fonts[1], ha='center', color=P['amber'])
    text(157.1, 103.6, 'v2', size=7, family=fonts[1], ha='center', color=P['amber'])
    ax.add_patch(FancyArrowPatch(xy(147,103.6),xy(153.6,103.6),arrowstyle='-|>',
                                mutation_scale=6.5,lw=.7,color=P['amber'],shrinkA=0,shrinkB=0,zorder=5))

    routes = []
    def port(node, side, offset_from_top_or_left=.5, kind='data'):
        offset = 1-offset_from_top_or_left if side in ('left','right') else offset_from_top_or_left
        return Port(node, side, offset, kind=kind)
    def route(name, source, target, middle=(), color=None, feedback=False):
        points = (port_point(source,nodes), *(xy(x,y) for x,y in middle), port_point(target,nodes))
        r = Route(name,source,target,points,kind=source.kind)
        routes.append(r)
        path = MplPath(points, [MplPath.MOVETO]+[MplPath.LINETO]*(len(points)-1))
        ax.add_patch(FancyArrowPatch(path=path, arrowstyle='-|>', mutation_scale=8.2,
                                    linewidth=1.05, linestyle=(0,(3.2,2.1)) if feedback else '-',
                                    color=color or P['blue'], shrinkA=0, shrinkB=0,
                                    joinstyle='round', capstyle='round', zorder=4))
        for pt in (points[0],points[-1]):
            ax.add_patch(Circle(pt, .42, facecolor='white', edgecolor=color or P['blue'], lw=.65,zorder=6))
        return r
    route('input',port('query','right'),port('controller','left',12/22))
    route('output',port('controller','top'),port('answer','bottom'),color=P['purple'])
    route('call',port('controller','right',15/22),port('tools','left',11/16))
    route('observation',port('tools','top',kind='feedback'),port('controller','right',5/22,kind='feedback'),
          [(152.5,35),(124,35),(124,47)],color=P['purple'],feedback=True)
    route('read',port('memory','top',48/67),port('controller','bottom',7/54),color=P['green'])
    route('update_feedback',port('controller','bottom',44/54,kind='feedback'),port('update','top',kind='feedback'),
          [(105,75),(137.5,75)],color=P['amber'],feedback=True)
    route('write',port('update','left',16/26),port('memory','right',16/26),color=P['amber'])
    text(126.9,53.5,'call',size=7.4,ha='center',color=P['blue'],route_label=True)
    text(138,31.9,'observation',size=7.4,ha='center',color=P['purple'],route_label=True)
    text(64.5,73.1,'read',size=7.4,ha='right',color=P['green'],route_label=True)
    text(121.3,71.7,'feedback',size=7.4,ha='center',color=P['amber'],route_label=True)
    text(98,97.5,'write',size=7.4,ha='center',color=P['amber'],route_label=True)
    text(7,115.2,'Solid: data flow     Dashed: feedback',size=7,color=P['muted'])
    text(171,115.2,'Illustrative architecture; no evaluated system is implied',size=7,color=P['muted'],ha='right')

    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    measured_labels=[]
    for index, (name, artist) in enumerate(labels):
        bounds=artist.get_window_extent(renderer).transformed(ax.transData.inverted())
        measured_labels.append(Label(f'{index}: {name}',Rect(*map(float,bounds.extents))))
    report=validate_diagram(nodes,routes,measured_labels,clearance=.45,units='mm')
    geometry_path=out/'01_modern_memory_architecture.geometry.json'
    geometry_path.write_text(json.dumps(report.to_dict(),indent=2)+'\n')
    if not report.passed:
        raise ValueError('Diagram routing failed: '+json.dumps(report.to_dict()))
    data={'status':'schematic','nodes':[asdict(n) for n in nodes],
          'routes':[asdict(r) for r in routes], 'record_miniature':'constructed schematic record, not user data',
          'edge_semantics':{'input':'query to controller','output':'controller to answer','call':'controller to tools',
                            'observation':'tools to controller feedback','read':'memory to controller',
                            'update_feedback':'controller to update rule feedback','write':'update rule to memory'},
          'fonts':fonts[2],'palette':P,'physical_size_mm':[W,H]}
    caption=('Original schematic of a tool-using agent with a versioned memory update loop. A query enters the controller, '
             'which reads records from memory, calls tools, receives their observations, and returns an answer. '
             'A distinct feedback path supplies evidence to an update rule, whose resolve and version operations precede a write to memory. '
             'The observation route leaves the top of Tools, travels through a reserved upper corridor, and enters a separate upper controller port; '
             'it does not lie on the Tools border. Solid arrows indicate data flow and dashed arrows indicate feedback. '
             'The record and version miniatures are constructed explanatory examples. This is an illustrative architecture, not an implemented or evaluated system.')
    alt=('A blue runtime region contains a query at left, a purple-outlined controller at center, tools at right, and an answer above. '
         'A solid lower arrow sends calls to tools. A separate dashed purple observation route exits the top of tools, rises, turns left, '
         'and enters the upper-right controller port. Below, a green memory store contains a record/provenance miniature; an amber update rule '
         'contains Resolve and Version cards. Memory reads upward to the controller; amber dashed feedback reaches the update rule; '
         'a solid write arrow returns leftward to memory.')
    return write_package(fig,out,'01_modern_memory_architecture',data,caption,alt,
                         {'status':'schematic','synthetic':False,'seed':None,'fonts':fonts[2],
                          'source_inspiration':['Harness² 2610.14224v1 Fig.2/3: semantic tints, nested hierarchy, separate feedback scale',
                                                'Cosmos 3 2606.02800v4 Fig.5: aligned levels and consistent semantic color'],
                          'originality':'Original composition, no source artwork or results copied',
                          'geometry_report':str(geometry_path),'minimum_label_font_pt':7},
                         extra_sources=(Path(__file__).with_name('diagram_geometry.py'),geometry_path))


def empirical(out, fonts):
    W,H=178,100
    fig=plt.figure(figsize=(W/25.4,H/25.4))
    def ft(x,y,s,**kw):
        return fig.text(x/W,1-y/H,s,va='center',**kw)
    ft(7,6.4,'Memory systems across a tool budget',fontsize=11,fontweight='bold',color=P['ink'])
    ft(171,6.4,'SYNTHETIC DATA',fontsize=7.2,color=P['muted'],ha='right')
    conditions=[('Base agent','blue','s',(0,(3,2))),('Retrieve only','green','^',(0,(1.5,1.5))),
                ('Versioned memory','amber','o','-')]
    handles=[Line2D([0],[0],color=P[role],marker=marker,ls=ls,lw=1.8 if i==2 else 1.35,
                    markersize=4,markerfacecolor='white',markeredgewidth=1.0,label=name)
             for i,(name,role,marker,ls) in enumerate(conditions)]
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(7/W,1-11.3/H),ncol=3,
               fontsize=8.1,frameon=False,columnspacing=2.4,handlelength=2.1,borderaxespad=0)
    axes=[]
    for i,(x,w) in enumerate([(15,64),(103,64)]):
        ax=fig.add_axes([x/W,(H-75)/H,w/W,48/H]);axes.append(ax)
        ax.set_ylim(40,94)
        ax.set_yticks([40,50,60,70,80,90])
        ax.grid(axis='y',color=P['grid'],lw=.55)
        ax.tick_params(axis='both',labelsize=7.6,length=2.5,width=.55,pad=2)
        for side in ('top','right'):ax.spines[side].set_visible(False)
        for side in ('left','bottom'):
            ax.spines[side].set_color('#B7C1CE');ax.spines[side].set_linewidth(.65)
        ax.set_ylabel('Success (%)',fontsize=8.1,labelpad=4)
        ft(x-1,22.8,'a' if i==0 else 'b',fontsize=9.3,fontweight='bold',color=P['ink'])
    ft(20,22.8,'Quality across budgets',fontsize=9.1,fontweight='bold',color=P['ink'])
    ft(108,22.8,'Quality–cost tradeoff',fontsize=9.1,fontweight='bold',color=P['ink'])
    budgets=np.array([1,2,4,8,16])
    base_means={'Base agent':[51,58,63,66,67], 'Retrieve only':[56,66,74,78,82],
                'Versioned memory':[58,70,82,86,89]}
    compute={'Base agent':[1,1.7,2.8,4.8,8.7], 'Retrieve only':[1.25,2.05,3.3,5.4,9.1],
             'Versioned memory':[1.6,2.4,3.9,6.2,10.2]}
    rng=np.random.default_rng(SEED)
    samples={name:rng.normal(np.array(base_means[name])[:,None],2.0,size=(5,8)) for name,_,_,_ in conditions}
    means={n:values.mean(axis=1) for n,values in samples.items()}
    sd={n:values.std(axis=1,ddof=1) for n,values in samples.items()}
    for i,(name,role,marker,ls) in enumerate(conditions):
        color=P[role]
        axes[0].fill_between(budgets,means[name]-sd[name],means[name]+sd[name],color=color,alpha=.13,lw=0,zorder=1)
        for ax,x in [(axes[0],budgets),(axes[1],compute[name])]:
            ax.plot(x,means[name],color=color,marker=marker,ls=ls,lw=1.8 if i==2 else 1.3,
                    markersize=4.3 if i==2 else 4,markerfacecolor='white',markeredgewidth=1.1,
                    zorder=3+i,label=name)
    axes[0].set_xscale('log',base=2)
    axes[0].set_xlim(.85,19)
    axes[0].set_xticks(budgets,labels=[str(v) for v in budgets])
    axes[0].set_xlabel('Tool-call budget (log scale)',fontsize=8.1,labelpad=4)
    axes[1].set_xlim(.3,11.2)
    axes[1].set_xticks([1,3,5,7,9,11])
    axes[1].set_xlabel('Compute (relative units)',fontsize=8.1,labelpad=4)
    axes[1].axhline(80,color='#A6ADBA',ls=(0,(3,2)),lw=.75,zorder=2)
    axes[1].text(.55,81.5,'80% reference',fontsize=7.1,color=P['muted'],ha='left',va='bottom',
                 bbox={'facecolor':'white','edgecolor':'none','pad':1.5},zorder=8)
    # Derived annotations are arithmetic on the preserved synthetic inputs.
    delta=float(means['Versioned memory'][-1]-means['Base agent'][-1])
    first={}
    for name in ('Retrieve only','Versioned memory'):
        indexes=np.flatnonzero(means[name]>=80)
        first[name]=float(compute[name][indexes[0]]) if len(indexes) else None
    if first['Versioned memory'] is None or first['Retrieve only'] is None:
        raise ValueError('This fixed-seed demonstration needs observed >=80% points for its annotation.')
    # Data-related takeaway strips sit outside axes and cannot occlude observations.
    for x,w in [(14,66),(102,66)]:
        fig.add_artist(FancyBboxPatch((x/W,1-94/H),w/W,7/H,transform=fig.transFigure,
                                     boxstyle='round,pad=0,rounding_size=.009',
                                     facecolor='#F8F2E9',edgecolor='none',zorder=0))
    ft(17,90.5,f'+{delta:.1f} pp vs base at 16 calls',fontsize=7.6,color=P['amber'],fontweight='bold')
    ft(105,89.2,'First sampled point ≥80%',fontsize=7.2,color=P['amber'],fontweight='bold')
    ft(105,92.1,f'Versioned {first["Versioned memory"]:g} / Retrieve {first["Retrieve only"]:g} units',
       fontsize=7.0,color=P['amber'])
    ft(7,97.3,'Illustrative data · 8 synthetic runs per budget · bands: mean ± 1 sample SD',fontsize=7.2,color=P['muted'])
    data={'status':'illustrative','seed':SEED,'independent_unit':'synthetic run','n_runs_per_budget':8,
          'tool_budget':budgets.tolist(),'success_samples_pct':{n:v.tolist() for n,v in samples.items()},
          'relative_compute':compute,'condition_order':[c[0] for c in conditions],
          'means':{n:v.tolist() for n,v in means.items()},'sample_sd':{n:v.tolist() for n,v in sd.items()},
          'band_semantics':'mean plus/minus one sample SD, ddof=1, not a confidence interval',
          'derived_annotations':{'delta_versioned_minus_base_at_budget16_pp':delta,'first_sampled_compute_at_80pct':first},
          'fonts':fonts[2],'palette':P,'physical_size_mm':[W,H]}
    caption=('Illustrative synthetic study of three named conditions. (a) Each marker is the mean of eight independent synthetic runs '
             'at the stated tool-call budget; shaded bands are mean ± one sample standard deviation (ddof=1), not confidence intervals. '
             'The budget axis is logarithmic with explicit observed values. (b) The same means are paired with constructed relative compute '
             'values; lines connect successive measured budget settings within each synthetic condition and do not estimate a Pareto frontier. '
             'The dashed 80% reference identifies the first sampled setting at or above that level; the annotation compares Versioned memory '
             'with Retrieve only, without interpolation. The left annotation is the descriptive difference between Versioned memory and '
             'Base agent at 16 calls. The seed, all constructed observations, summaries and compute coordinates are preserved. '
             'No real-system performance, significance, or efficiency claim is made.')
    alt=('Two side-by-side plots share blue squares for Base agent, green triangles for Retrieve only, and amber circles for Versioned memory. '
         'The left plot shows synthetic success versus five tool budgets, with translucent ±1 sample-SD bands. The right shows the same means '
         'against constructed relative compute, with a dashed 80% reference. Takeaway strips below report the derived final-budget difference '
         'and the first sampled compute coordinates that cross 80%. The figure is prominently labeled Synthetic Data.')
    return write_package(fig,out,'02_modern_synthetic_study',data,caption,alt,
                         {'status':'illustrative','synthetic':True,'seed':SEED,'fonts':fonts[2],
                          'source_inspiration':['Harness² 2610.14224v1 Fig.1: muted semantic colors, outlined markers, direct quantitative annotations'],
                          'originality':'All data and composition are original synthetic demonstrations',
                          'minimum_label_font_pt':7})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    fonts=select_fonts()
    with style_context(font_size=8), mpl.rc_context({'font.family':fonts[0], 'font.weight':'normal',
                                                    'axes.titleweight':'bold','mathtext.default':'regular'}):
        for recipe in (architecture,empirical):
            paths=recipe(args.out,fonts)
            print(paths['manifest'])


if __name__=='__main__':
    main()
