#!/usr/bin/env python3
"""Render an original four-panel publication figure from preserved SYNTHETIC inputs.

Run from any directory: python source/render_figure.py
No data are fabricated inside the renderer. The analysis module loads the raw
observations, computes all summaries, and supplies every numerical callout.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', '/tmp/memory-study-mplconfig')
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Circle
from matplotlib.text import Text
from analyze import analyze
from figure_style import style_context, export_figure
from check_figure import check_pdf

WIDTH, HEIGHT = 178, 181
INK = '#23333F'
MUTED = '#53616B'
GRID = '#DEE5E8'
COLORS = {'none':'#59616C', 'unfiltered':'#B46B24', 'verified':'#176E71', 'no_history':'#806196'}
LABEL_INKS = {**COLORS, 'unfiltered':'#91531D'}
MARKERS = {'none':'s', 'unfiltered':'^', 'verified':'o', 'no_history':'D'}
LINES = {'none':'-', 'unfiltered':(0,(3,1.5)), 'verified':'-', 'no_history':(0,(1.5,1.2))}
NAMES = {'none':'No memory', 'unfiltered':'Unfiltered', 'verified':'Verified', 'no_history':'Verified (no history)'}


def main():
    a = analyze()
    cfg = a['config']
    regular = font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans', weight='normal'), fallback_to_default=False)
    bold = font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans', weight='bold'), fallback_to_default=False)
    assert Path(regular).read_bytes()[:4] == b'\x00\x01\x00\x00'
    assert Path(bold).read_bytes()[:4] == b'\x00\x01\x00\x00'
    with style_context(8.0), mpl.rc_context({'font.family':'DejaVu Sans',
        'text.color':INK, 'axes.labelcolor':INK, 'xtick.color':MUTED, 'ytick.color':MUTED,
        'font.size':8.0, 'xtick.labelsize':7.3, 'ytick.labelsize':7.3,
        'axes.labelsize':8.0, 'legend.fontsize':7.7, 'axes.linewidth':.55}):
        fig = plt.figure(figsize=(WIDTH/25.4, HEIGHT/25.4), dpi=160)
        texts = []

        def text(x,y,s, size=8, weight='normal', color=INK, ha='left', va='center', **kw):
            t=fig.text(x/WIDTH,1-y/HEIGHT,s,fontsize=size,fontweight=weight,color=color,
                       ha=ha,va=va,**kw)
            texts.append(t)
            return t

        def line(x0,y0,x1,y1,color=GRID,lw=.65):
            fig.add_artist(Line2D([x0/WIDTH,x1/WIDTH],[1-y0/HEIGHT,1-y1/HEIGHT],
                                 transform=fig.transFigure,color=color,lw=lw))

        def axes(x,y,w,h):
            return fig.add_axes([x/WIDTH,1-(y+h)/HEIGHT,w/WIDTH,h/HEIGHT])

        def panel(x,y,letter,title):
            text(x,y,letter,9.5,'bold',COLORS['verified'])
            text(x+5,y,title,9.5,'bold')

        text(4,6.5,'Memory policy evaluation',10.6,'bold')
        text(174,6.5,'SYNTHETIC DATA',8.7,'bold','#8E4B17',ha='right',
             bbox={'facecolor':'#FFF1E4','edgecolor':'#E3C5A9','linewidth':.6,'pad':3.1})
        text(4,13.4,f"{cfg['n_seeds']} matched seed blocks · {len(cfg['task_families'])} task families · {len(cfg['budgets_tokens'])} budgets · {cfg['episodes_per_stream']} episodes per stream",7.7,color=MUTED)
        # Stable policy key: color, marker and line pattern all carry identity.
        legend_x = [5, 43, 83, 119]
        for x,policy in zip(legend_x,cfg['policies']):
            fig.add_artist(Line2D([(x+.4)/WIDTH,(x+7.0)/WIDTH],[1-21.3/HEIGHT]*2,
                transform=fig.transFigure,color=COLORS[policy],linestyle=LINES[policy],lw=1.25,
                marker=MARKERS[policy],markevery=[1],markersize=4.2,
                markeredgecolor='white',markeredgewidth=.45))
            text(x+9.3,21.3,NAMES[policy],7.7)
        line(4,27,174,27)

        # A. Paired independent-unit effects, with a dedicated numerical rail.
        panel(4,33,'a','Paired success changes')
        text(4,39,'Dots = seed effects; bars = paired 95% CI',7.5,color=MUTED)
        text(102,39,'Mean [CI]',7.25,color=MUTED,ha='right')
        axa=axes(38,46,44,39)
        axa.patch.set_alpha(0)
        axa.set_xlim(-3.1,12.6)
        axa.set_ylim(3.52,-.52)
        axa.set_yticks([])
        axa.set_xticks([0,5,10])
        axa.set_xticklabels(['0','+5','+10'])
        axa.spines[['left','top','right']].set_visible(False)
        axa.spines['bottom'].set_color('#9EAAB1')
        axa.grid(axis='x',lw=.45,color=GRID,zorder=0)
        axa.axvline(0,color='#839098',lw=.8,zorder=1)
        labels=['Verified − unfiltered','Verified − no history¹','Verified − no memory','Unfiltered − no memory']
        row_y=[]
        for i,c in enumerate(a['contrasts']):
            y_mm=46+(i+.52)/4.04*39
            row_y.append(y_mm)
            if i==0:
                fig.add_artist(Rectangle((3/WIDTH,1-(y_mm+4.2)/HEIGHT),100/WIDTH,8.4/HEIGHT,
                    transform=fig.transFigure,facecolor='#EAF4F3',edgecolor='none',zorder=-2))
            color=COLORS[c['left']]
            vals=np.array(c['seed_values'])
            # Deterministic rank-based vertical spread: no stochastic data jitter.
            rank=np.argsort(np.argsort(vals,kind='stable'),kind='stable')
            jitter=np.array([-.22,-.11,.0,.11,.22])[rank%5]
            axa.scatter(vals,np.full(len(vals),i)+jitter,s=7.8,facecolors='white',edgecolors=color,
                        linewidths=.45,alpha=.75,zorder=3)
            axa.plot([c['lo'],c['hi']],[i,i],color=color,lw=2.4,solid_capstyle='round',zorder=5)
            axa.plot(c['mean'],i,MARKERS[c['left']],markersize=4.5,color=color,
                     markeredgecolor='white',markeredgewidth=.7,zorder=6)
            text(4,y_mm,labels[i],7.35,'bold' if i==0 else 'normal')
            text(102,y_mm-1.4,f"{c['mean']:+.1f}",8.3,'bold',LABEL_INKS[c['left']],ha='right')
            text(102,y_mm+2.1,f"[{c['lo']:+.1f}, {c['hi']:+.1f}]",7.25,color=MUTED,ha='right')
        text(60,93,'Success difference (percentage points)',7.7,ha='center')
        text(4,100,'Equal weight to every family × budget cell.',7.25,color=MUTED)
        text(4,104.2,'¹ Verified minus verified without rejection history.',7.25,color=MUTED)

        # B. A shared, explicitly signed scale; each value is the same paired estimand.
        panel(108,33,'b','Where the effect varies')
        text(108,39,'Verified − unfiltered, pp',7.5,color=MUTED)
        axb=axes(129,46,45,39)
        delta=np.asarray(a['heterogeneity']['mean'])
        lo=np.asarray(a['heterogeneity']['lo'])
        hi=np.asarray(a['heterogeneity']['hi'])
        norm=TwoSlopeNorm(vmin=-14,vcenter=0,vmax=14)
        cmap=LinearSegmentedColormap.from_list('effect', ['#B67A69','#FFFFFF','#216F74'])
        edges=np.arange(5)-.5
        image=axb.pcolormesh(edges,edges,delta,cmap=cmap,norm=norm,shading='flat',
                            rasterized=False,edgecolors='white',linewidth=.5)
        axb.set_xlim(-.5,3.5)
        axb.set_ylim(3.5,-.5)
        axb.set_xticks(range(4),[f'{b:,}' for b in cfg['budgets_tokens']])
        axb.xaxis.tick_top()
        axb.tick_params(axis='x',length=0,pad=4,labelsize=7.25)
        axb.set_yticks(range(4),[f['name'] for f in cfg['task_families']])
        axb.tick_params(axis='y',length=0,pad=3,labelsize=7.35)
        for spine in axb.spines.values(): spine.set_visible(False)
        axb.set_xticks(np.arange(-.5,4,.1)[::10],minor=True)
        axb.set_yticks(np.arange(-.5,4,1),minor=True)
        axb.grid(which='minor',color='white',lw=1)
        axb.tick_params(which='minor',length=0)
        for r in range(4):
            for c in range(4):
                label_color='white' if delta[r,c]>=12.1 else '#111111'
                axb.text(c,r,f'{delta[r,c]:+.1f}',ha='center',va='center',fontsize=8.0,
                         color=label_color,fontweight='bold' if delta[r,c]>=8.4 else 'normal')
                if lo[r,c]<=0<=hi[r,c]:
                    axb.add_patch(Circle((c+.34,r-.30),.045,facecolor='none',edgecolor=INK,lw=.65))
        cax=axes(129,90,45,2.2)
        cb=fig.colorbar(image,cax=cax,orientation='horizontal',ticks=[-14,0,14])
        cb.solids.set_rasterized(False)
        cb.solids.set_edgecolor('face')
        cb.ax.set_xticklabels(['−14','0','+14'])
        cb.outline.set_visible(False)
        cb.ax.tick_params(length=2,width=.5,labelsize=7.25,pad=2)
        text(108,101,'○ Pointwise CI includes zero',7.25,color=MUTED)
        text(108,105.2,'Columns: memory budget (tokens)',7.25,color=MUTED)
        line(4,110,174,110)

        # C. Quality/resource trajectories connect only observed configurations.
        panel(4,116,'c','Quality has a resource cost')
        text(4,122,'Mean success vs total model tokens',7.5,color=MUTED)
        axc=axes(15,130,82,34)
        axc.set_xlim(2.92,4.65)
        axc.set_ylim(50,70.5)
        axc.set_xticks([3,3.5,4,4.5])
        axc.set_yticks([50,55,60,65,70])
        axc.set_ylabel('Success (%)',labelpad=3)
        axc.set_xlabel('Model tokens / episode (×10³)',labelpad=4)
        axc.grid(axis='y',color=GRID,lw=.45)
        for policy in cfg['policies']:
            d=a['tradeoff'][policy]
            xx=np.array(d['tokens']['mean'])
            yy=np.array(d['success']['mean'])
            xlo,xhi=np.array(d['tokens']['lo']),np.array(d['tokens']['hi'])
            ylo,yhi=np.array(d['success']['lo']),np.array(d['success']['hi'])
            if policy=='none': xx,yy,xlo,xhi,ylo,yhi=[v[:1] for v in [xx,yy,xlo,xhi,ylo,yhi]]
            color=COLORS[policy]
            axc.hlines(yy,xlo,xhi,color=color,lw=.5,alpha=.65,zorder=2)
            axc.vlines(xx,ylo,yhi,color=color,lw=.65,alpha=.7,zorder=2)
            axc.plot(xx,yy,color=color,linestyle=LINES[policy],lw=1.25,zorder=3)
            axc.plot(xx,yy,linestyle='none',marker=MARKERS[policy],markersize=4.1,
                     color=color,markeredgecolor='white',markeredgewidth=.55,zorder=4)
        dx=[-.17,-.030,-.025,-.030]
        dy=[1.50,-2.45,2.5,2.5]
        d=a['tradeoff']['verified']
        for i,b in enumerate(cfg['budgets_tokens']):
            axc.annotate(f'{b:,}',(d['tokens']['mean'][i],d['success']['mean'][i]),
                xytext=(d['tokens']['mean'][i]+dx[i],d['success']['mean'][i]+dy[i]),
                textcoords='data',ha='center',va='center',fontsize=7.25,color=COLORS['verified'],
                bbox={'facecolor':'white','edgecolor':'none','pad':.2},
                arrowprops={'arrowstyle':'-','color':COLORS['verified'],'lw':.5,'shrinkA':2,'shrinkB':3})
        text(4,174.3,'Labels on verified points give memory budgets.',7.25,color=MUTED)

        # D. Raw event rates expose the constructed mechanism and its capacity tradeoff.
        panel(108,116,'d','Rejection-history diagnostic')
        text(108,122,f"History reserves {cfg['history_fraction']:.0%} of memory capacity.",7.25,color=MUTED)
        text(139.4,129,'Corrupted\nreads',7.4,ha='center',linespacing=1.15)
        text(163.4,129,'Repeat invalid\nwrites',7.4,ha='center',linespacing=1.15)
        diagnostic_axes=[]
        for metric,x,w,max_x,ticks in [('corrupt_read',129,21,21,[0,10,20]),
                                      ('repeat_invalid_write',154,20,16,[0,5,10,15])]:
            ax=axes(x,137,w,25)
            diagnostic_axes.append(ax)
            ax.set_ylim(3.5,-.5)
            ax.set_xlim(-.6,max_x)
            ax.set_yticks([])
            ax.set_xticks(ticks)
            ax.tick_params(axis='x',labelsize=7.25,pad=2,length=2)
            ax.spines[['left','top','right']].set_visible(False)
            ax.grid(axis='x',lw=.4,color=GRID)
            d=a['diagnostics'][metric]
            for j,policy in enumerate(cfg['policies']):
                ax.hlines(j,d['lo'][j],d['hi'][j],color=COLORS[policy],lw=1.7,zorder=3)
                ax.plot(d['mean'][j],j,marker=MARKERS[policy],color=COLORS[policy],markersize=4,
                        markeredgecolor='white',markeredgewidth=.45,zorder=4)
        row_names=['No memory','Unfiltered','Verified','− history']
        for j,name in enumerate(row_names):
            text(108,137+(j+.5)/4*25,name,7.25,
                 weight='bold' if j==2 else 'normal',color=LABEL_INKS[cfg['policies'][j]])
        text(151.5,170,'Events / 100 episodes',7.6,ha='center')
        text(108,174.3,'Fewer errors do not imply a net success gain.',7.25,color=MUTED)
        # An unambiguous disclosure survives excerpting and print.
        text(89,179.0,'Constructed simulation; no real-agent performance claim.',7.25,'bold',MUTED,ha='center')

        fig.canvas.draw()
        # Record all final drawn text in physical units; detect cross-panel or
        # accidentally overlapping fig-level labels before export.
        renderer=fig.canvas.get_renderer()
        scale=72/fig.dpi
        text_boxes=[]
        for t in fig.findobj(match=Text):
            if not t.get_visible() or not t.get_text().strip(): continue
            bbox=t.get_window_extent(renderer)
            if not np.all(np.isfinite(bbox.extents)): continue
            text_boxes.append({'text':t.get_text(),'font_pt':t.get_fontsize(),
                'bbox_pt':[round(float(z)*scale,3) for z in bbox.extents]})
        (ROOT/'qa/text_geometry.json').write_text(json.dumps(text_boxes,indent=2,ensure_ascii=False)+'\n')
        overlaps=[]
        for i,one in enumerate(text_boxes):
            for two in text_boxes[i+1:]:
                b1,b2=one['bbox_pt'],two['bbox_pt']
                ix=min(b1[2],b2[2])-max(b1[0],b2[0])
                iy=min(b1[3],b2[3])-max(b1[1],b2[1])
                if ix>.5 and iy>.5:
                    overlaps.append({'first':one['text'],'second':two['text'],
                                     'intersection_pt':[round(ix,3),round(iy,3)]})
        (ROOT/'qa/geometry_checks.json').write_text(json.dumps({
            'visible_text_boxes_checked':len(text_boxes), 'text_pair_overlap_tolerance_pt':.5,
            'text_pair_overlap_count':len(overlaps),'text_pair_overlaps':overlaps,
            'canvas_containment':'checked by export_figure',
            'scope':'Text rectangles at final export dimensions; marks, leaders and interval readability also visually reviewed.'},indent=2)+'\n')
        assert not overlaps, overlaps
        metadata={'data_status':'SYNTHETIC DATA','independent_seed_blocks':cfg['n_seeds'],
            'primary_estimand':a['primary_estimand'],'interval_method':a['interval_method'],
            'minimum_font_pt':7.25,'actual_fonts':{'regular':regular,'bold':bold},
            'palette':COLORS,'markers':MARKERS,'figure_dimensions_mm':[WIDTH,HEIGHT],
            'panels':['paired success effects','task × budget heterogeneity','quality versus cost','failure diagnostics'],
            'semantic_color':'policy identity; panel b has a separately defined signed quantitative scale',
            'lines':'within-policy links between observed budget settings only; not a frontier or interpolation claim'}
        source_files=[ROOT/'inputs/study_config.json',ROOT/'inputs/scenarios.csv.gz',ROOT/'inputs/observations.csv.gz',
            ROOT/'source/make_data.py',ROOT/'source/analyze.py',ROOT/'source/render_figure.py',ROOT/'source/figure_style.py']
        outputs=export_figure(fig,ROOT/'memory_policy_study',source_files=source_files,metadata=metadata,dpi=400)
        plt.close(fig)
    report=check_pdf(ROOT/'memory_policy_study.pdf',expected_width_mm=WIDTH,min_font_pt=7.2)
    (ROOT/'qa/pdf_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    assert report['automated_checks_passed'],report
    svg=ET.parse(ROOT/'memory_policy_study.svg')
    svg_text=svg.findall('.//{http://www.w3.org/2000/svg}text')
    assert len(svg_text)>80
    import fitz
    from PIL import Image
    doc=fitz.open(ROOT/'memory_policy_study.pdf')
    for dpi,name,cs in [(180,'pdf_render_180dpi',fitz.csRGB),(300,'pdf_grayscale_300dpi',fitz.csGRAY),
                         (96,'final_size_96dpi',fitz.csRGB)]:
        page=doc[0]
        pix=page.get_pixmap(dpi=dpi,colorspace=cs,alpha=False)
        pix.save(ROOT/f'qa/{name}.png')
    font_sizes=[s['size'] for b in doc[0].get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l.get('spans',[])]
    exports={'width_mm':WIDTH,'height_mm':HEIGHT,'minimum_pdf_font_pt':min(font_sizes),
        'svg_editable_text_nodes':len(svg_text),'pdf_image_count':len(doc[0].get_images()),
        'all_vector_pdf':len(doc[0].get_images())==0,'actual_regular_font':regular,'actual_bold_font':bold,
        'true_type_font_signature_verified':True,'outputs_exist':{k:Path(v).exists() for k,v in outputs.items()}}
    assert exports['all_vector_pdf'], exports
    (ROOT/'qa/export_checks.json').write_text(json.dumps(exports,indent=2)+'\n')
    write_docs(a)
    print(json.dumps({'files':outputs,'primary_effect_pp':a['contrasts'][0]['mean'],
                      'pdf_issues':report['issue_count'],'svg_text_nodes':len(svg_text)},indent=2))


def write_docs(a):
    cfg=a['config']; primary=a['contrasts'][0]; ablation=a['contrasts'][1]
    p=lambda c:f"{c['mean']:+.2f} pp (95% CI {c['lo']:+.2f} to {c['hi']:+.2f})"
    corr=a['diagnostics']['corrupt_read']['mean']; rep=a['diagnostics']['repeat_invalid_write']['mean']
    caption=f'''Figure. Synthetic demonstration of a paired memory-policy evaluation. All observations are constructed by the supplied simulator; these are not experimental results from real agents. In this fixture, verification raises macro-average success relative to unfiltered updates by {p(primary)}, while adding rejection history to verification changes success by {p(ablation)}. (a) Within each of 24 independent seed blocks, success is averaged equally across four fixed task families and four fixed memory budgets; the plotted contrasts subtract the paired policy means. Hollow dots show all 24 seed effects, filled markers show their mean, and thick horizontal bars show 95% paired percentile-bootstrap intervals. The highlighted first row is the primary estimand. “Verified (no history)” in the legend denotes verification without a rejection ledger; the second contrast in (a) compares the full verified policy with that ablation. (b) Each cell is the verified-minus-unfiltered success difference in percentage points, averaging the same 24 seed blocks within one family/budget condition. The signed scale is shared by all cells; a small open circle marks a pointwise interval that includes zero. (c) Each point averages the four task families at one memory budget; both horizontal token-cost and vertical success intervals use matched seed-block resampling. Lines connect only the four observed budget settings, and labels on the verified curve give those budgets in tokens. The no-memory baseline is invariant to budget and is shown once. Total model tokens include task execution, resident memory context, verifier checks, writes, and history lookup; they are simulated tokens, not measured latency, money, or hardware cost. (d) Macro-average counts of corrupted reads and repeated invalid writes per 100 episodes diagnose the constructed memory mechanism. Verified and verified-without-history have {corr[2]:.2f} versus {corr[3]:.2f} corrupted reads and {rep[2]:.2f} versus {rep[3]:.2f} repeated invalid writes per 100 episodes. A repeated invalid write accepts an invalid proposal whose identical signature has already appeared earlier in that seed/family stream, irrespective of whether a policy rejected it. These diagnostics are descriptive, not a causal mediation analysis.

The design comprises four policies × four task families × four assigned memory budgets × 24 independent seed blocks × {cfg['episodes_per_stream']} sequential episodes, preserving {a['raw_observation_count']:,} outcome rows and {a['shared_scenario_count']:,} shared scenario rows. The task sequence, key, proposal, difficulty, success variate, and checker variate are identical across policies and budgets within a seed/family block. Episodes are scored before their updates are considered. Full verification reserves 25% of each total memory budget for 16-token rejection signatures; records use 64 tokens, and both stores evict least-recently-used entries. The other memory policies devote their entire budget to records. A fallible checker may falsely accept invalid updates or falsely reject valid updates; all checker rejections, including mistakes, enter the full policy’s history. The no-memory policy ignores the assigned capacity and repeats identical outcomes across the four budget columns; those repetitions do not create additional independent data. All intervals are pointwise 95% percentile-bootstrap intervals from {cfg['bootstrap_replicates']:,} resamples of the 24 intact seed blocks, with all matched conditions retained together. No episodes, task families, or budgets are treated as independent replications; no multiplicity adjustment is applied. The estimand targets only this fixed, equally weighted task/budget suite under the stipulated simulator. All episodes, including early empty-memory episodes and failures, are retained. The figure does not validate a memory method or predict real-world effect sizes.
'''
    (ROOT/'extended_caption.md').write_text(caption)
    main_caption=f'''Figure. SYNTHETIC DATA: a constructed memory-policy evaluation with no real-agent performance claim. (a) Paired success differences show all {cfg['n_seeds']} independent seed-block effects, means and intervals; verified minus unfiltered is {primary['mean']:+.2f} pp [{primary['lo']:.2f}, {primary['hi']:.2f}]. (b) A shared-scale matrix decomposes this contrast by four fixed task families and four memory budgets; open circles mark intervals spanning zero. (c) Success versus simulated model-token cost connects observed budgets, with uncertainty on both axes. (d) Corrupted reads and repeated invalid writes diagnose the stipulated mechanism. Compared with the no-history ablation, rejection history reserves {cfg['history_fraction']:.0%} of total capacity, reducing record storage; fewer errors need not improve success. Policies and budgets share episode streams within seeds. Estimates weight fixed family–budget cells equally and target only this suite. All intervals are pointwise paired 95% percentile-bootstrap intervals from {cfg['bootstrap_replicates']:,} resamples of {cfg['n_seeds']} intact seed blocks; no multiplicity adjustment is applied.'''
    (ROOT/'caption.md').write_text(main_caption+'\n')
    assert 140 <= len(main_caption.split()) <= 160, len(main_caption.split())
    from PIL import ImageFont
    font_path=font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans'))
    caption_fit={'caption_word_count':len(main_caption.split()),'artwork_width_mm':WIDTH,
                 'artwork_height_mm':HEIGHT,'caption_gap_mm':3,'caption_width_mm':WIDTH,
                 'font_family':'DejaVu Sans','assumed_leading_factor':1.2,
                 'method':'Greedy word wrapping using actual font advance widths at 40× sampling; no hyphenation.',
                 'template_caveat':'Approximation only: manuscript font, caption prefix, line spacing, paragraph spacing, float rules and actual text width can change fit.',
                 'sizes':[]}
    for pt in [8,9]:
        face=ImageFont.truetype(font_path,pt*40)
        width_pt=WIDTH/25.4*72
        wrapped=[]; current=''
        for word in main_caption.split():
            trial=(current+' '+word).strip()
            if current and face.getlength(trial)/40>width_pt:
                wrapped.append(current); current=word
            else:
                current=trial
        if current: wrapped.append(current)
        caption_height_mm=len(wrapped)*pt*1.2/72*25.4
        caption_fit['sizes'].append({'font_pt':pt,'line_count':len(wrapped),
              'leading_pt':pt*1.2,'caption_height_mm':round(caption_height_mm,2),
              'artwork_gap_caption_height_mm':round(HEIGHT+3+caption_height_mm,2),
              'wrapped_lines':wrapped})
    (ROOT/'qa/caption_fit.json').write_text(json.dumps(caption_fit,indent=2,ensure_ascii=False)+'\n')
    alt=f'''Four-panel figure labeled SYNTHETIC DATA. Twenty-four matched seed blocks compare no memory, unfiltered updates, verified updates, and verified updates without rejection history. Panel a shows each seed’s paired success differences and a mean with a 95% cluster-bootstrap interval. The primary verified-versus-unfiltered change is {primary['mean']:.1f} percentage points; the full-versus-no-history change is near zero ({ablation['mean']:+.2f} points). Panel b gives a four-task by four-budget matrix: differences are small for fact recall and grow at larger budgets for code repair, tool routing, and long-horizon tasks. Panel c shows higher simulated success at higher token costs; the full policy is worse than its no-history ablation at small budgets and better at large budgets. Panel d shows lower corrupted-read and repeat-invalid-write rates with rejection history. The history consumes one quarter of memory capacity, and the lower diagnostic error rates do not translate to an overall success gain in this fixture. All results are simulated and do not establish real-agent performance.'''
    (ROOT/'alt_text.txt').write_text(alt+'\n')
    readme=f'''# Synthetic memory-policy study

**SYNTHETIC DATA.** These files demonstrate a statistically explicit, publication-scale figure. They are not results from real agents and cannot support a claim about an actual memory system.

## Deliverables

- `memory_policy_study.pdf`: exact {WIDTH} × {HEIGHT} mm, vector master with embedded TrueType regular/bold fonts.
- `memory_policy_study.svg`: editable text and vector marks; requires DejaVu Sans.
- `memory_policy_study.png`: 400 dpi preview.
- `caption.md`, `extended_caption.md`, `alt_text.txt`, `design_note.md`: compact manuscript caption, extended caption, accessible description, and visual/statistical decisions.
- `analysis.json`: all displayed estimates, intervals, and independent-unit values.
- `inputs/`: immutable raw synthetic observations, shared scenarios, configuration and seed manifest.
- `source/`: self-contained Python generation, analysis, rendering and checks.
- `qa/`: numerical/export/geometry reports, actual PDF renders, grayscale review, and print-size reference.

## Reproduce

Requirements: Python 3, NumPy, Matplotlib, Pillow, PyMuPDF, and installed DejaVu Sans regular/bold TrueType fonts. No network is required.

```bash
python source/render_figure.py
```

The renderer reads the preserved observations. To regenerate those observations from the explicit simulator and fixed seeds, run:

```bash
python source/make_data.py
python source/render_figure.py
```

Data are saved as CSV compressed with deterministic gzip metadata. Read with Python’s `gzip.open(..., 'rt')` and `csv.DictReader`. `make_data.py` never writes outside this deliverable folder.

## Estimand and dependence

Let Y(s,f,b,p) be the success fraction across all 96 sequential episodes for seed block s, fixed family f, fixed budget b, and policy p. The primary seed effect is d(s) = (1/16) Σ(f,b) [Y(s,f,b,verified) − Y(s,f,b,unfiltered)]. The displayed primary effect is 100 × mean(s) d(s), in percentage points. This is a macro-average over the fixed 16-condition suite, not a sample-weighted score over an external task population. The other contrasts use the identical procedure.

All policies and budgets share the actual scenario stream and underlying random variates, not merely matching arbitrary seed numbers. Seeds are independent RNG substreams, and the whole seed block is the resampling unit. The same 20,000 sampled block-index arrays are used for all metrics. The 2.5th and 97.5th percentiles of bootstrap means give pointwise 95% intervals. Their interpretation is conditional on the simulator and fixed suite. With 24 blocks, intervals remain finite-sample approximations; 20,000 draws do not increase the experimental sample size. There is no multiplicity adjustment and no family-population inference.

Panel b forms paired differences before averaging seeds in each cell. Panel c first averages families inside seed/budget/policy. Panel d first averages event rates across family/budget inside seed/policy. Resampling episodes would incorrectly ignore serial memory dependence and is deliberately avoided.

## Simulator

Every stream starts empty. Forty possible keys have a shared seeded skewed frequency. Each episode retrieves at most one matching record, is scored with a preserved common success uniform, then offers a shared candidate update. A valid retrieved record increases the constructed success probability; a corrupt record decreases it by the family-specific amount in `study_config.json`. Memory proposals are exogenous to the outcome. The unfiltered policy accepts all proposals. Both verified policies use the same fallible checker. Full verification additionally blocks candidate signatures that its bounded ledger previously rejected. The ledger includes false rejections as well as correct ones; the policy does not observe proposal ground truth. Invalidity is retained only for simulation and diagnostics.

Records cost 64 memory tokens. Rejection signatures cost 16 tokens. Full verification reserves exactly 25% of every configured capacity for the ledger; its record store therefore has 3/6/12/24 slots at 256/512/1024/2048 tokens, versus 4/8/16/32 slots for unfiltered and no-history. Each store uses least-recently-used eviction. This makes the rejection-history ablation a controlled **total-capacity** comparison that also changes the division of capacity between records and history. It does not isolate a zero-cost history mechanism.

Model-token cost sums task execution tokens, resident pre-update memory context, 620 tokens per actual checker call, 64 per accepted write, and 12 per history lookup. These constants and resource scopes are illustrative assumptions, not calibrated measurements. No-memory ignores the memory budget and has identical outcomes/cost across all four assigned budget columns.

## Synthetic findings

- Primary paired contrast: {p(primary)}.
- Full versus no-history ablation: {p(ablation)}.
- Full verification has fewer repeated invalid writes and corrupted reads, but its smaller record store offsets that advantage at small budgets. This tradeoff was built into the simulator; the visual explains it without treating it as a discovered empirical fact.

## Checks and limits

The build checks the complete balanced design, unique rows, baseline identity across budgets, capacity bounds, legal probabilities, write/read invariants, PDF page dimensions and fonts, minimum 7.2 pt exported text, editable SVG text, vector-only PDF content, and canvas containment. Actual PDF and grayscale images are retained for visual review. The source does not claim that automatic checks certify every collision or scientific conclusion.

The intended placement is **178 mm wide**. The 7.25 pt smallest labels become about 3.46 pt if this export is shrunk to 85 mm; it must be recomposed for a single column. A 96 dpi image is a convenient scale reference, not a physical proof of screen or printer calibration. The figure is vector, so final PDF print is the authoritative rendering.
'''
    (ROOT/'README.md').write_text(readme)


if __name__=='__main__':
    main()
