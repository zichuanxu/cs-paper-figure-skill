#!/usr/bin/env python3
"""Render a layered method / atomic transaction / worked replay figure.

All decisions in the concrete instance are derived from dense-method-fixture.json.
The method is an original schematic, not a reproduction or empirical result.
Run: python render_dense_method.py --out figures/dense
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from figure_scene import FigureScene, COLORS, INK, MUTED
from figure_style import export_figure, style_context
from render_modern_examples import select_fonts


def evaluate_fixture(f):
    base = dict(f['base_record'])
    proposals = f['proposals']
    if f['validation_trace']['id'] in {p['evidence'] for p in proposals}:
        raise ValueError('The validation fixture must not be used as proposal evidence.')
    if len(proposals)!=3 or len(f['assertions'])!=3:
        raise ValueError('This fixed example layout requires three proposals and three assertions; adapt the source for a different content budget.')
    if len({p['id'] for p in proposals}) != len(proposals):
        raise ValueError('Proposal identifiers must be unique.')
    chosen, claimed = [], set()
    rejected_ids={item['proposal_id'] for item in f.get('rejection_history',[])}
    for p in sorted(proposals, key=lambda p: -p['priority']):
        if p['operation'] not in ('ADD','REPLACE'):
            raise ValueError('Fixture supports ADD / REPLACE.')
        if (p['operation']=='ADD') == (p['key'] in base):
            raise ValueError(f"Invalid precondition for {p['id']}")
        if p['id'] not in rejected_ids and p['key'] not in claimed and len(chosen)<f['edit_budget']:
            chosen.append(p); claimed.add(p['key'])
    candidate={**base, **{p['key']:p['value'] for p in chosen}}
    def execute(memory):
        trace=f['validation_trace']
        return {'value':trace['source_value'] if memory.get('units')=='value + unit' else trace['baseline_answer'],
                'source_date':trace['source_date'] if memory.get('freshness')=='source date' else None,
                'citation':'URL' if memory.get('citation')=='URL' else None}
    checks=lambda output:[output.get(a['key'])==a['expected'] for a in f['assertions']]
    base_output,candidate_output=execute(base),execute(candidate)
    before,after=checks(base_output),checks(candidate_output)
    alternate={**base, proposals[1]['key']:proposals[1]['value']}
    alternate_output=execute(alternate)
    alt=checks(alternate_output)
    conflicts=[[i!=j and a['key']==b['key'] for j,b in enumerate(proposals)]
               for i,a in enumerate(proposals)]
    return {'selected':[p['id'] for p in chosen],'conflicts':conflicts,
            'base':base,'candidate':candidate,'before':before,'after':after,
            'alternate':alt,'accepted':sum(after)>sum(before),
            'alternate_accepted':sum(alt)>sum(before),
            'outputs':{'baseline':base_output,'candidate':candidate_output,'alternate':alternate_output},
            'proposal_evidence_ids':sorted({p['evidence'] for p in proposals}),
            'validation_case_id':f['validation_trace']['id'],
            'rejection_rule':f['rejection_rule'],
            'counterfactual_rejection':None if sum(alt)>sum(before) else {'proposal_id':proposals[1]['id'],'reason':'No strict improvement on the illustrative fixture'},
            'candidate_hash':hashlib.sha256(json.dumps(candidate,sort_keys=True).encode()).hexdigest()[:8]}


def draw_overview(s,f):
    s.panel('a','A frozen runtime; two explicit update timescales',214)
    s.scope(3,125,172,84,'runtime')
    s.scope(128.5,157,43,43,'proposal')
    s.text(6,205,'FAST LOOP  /  one rollout batch',size=7.4,weight='bold',color=COLORS['runtime'][1])
    s.node('training',6,183,26,15,role='neutral',shape='document',title='Training cases',subtitle='D_train\nsource-tagged')
    s.node('current',6,166,26,13,role='runtime',shape='document',title='Memory M_t',subtitle='current snapshot',title_size=7.8,body_size=7.2)
    s.node('runtime',43,181,34,17,role='runtime',title='Agent execution',subtitle='frozen weights\nread memory')
    s.node('traces',87,181,32,17,role='runtime',shape='document',title='Trace ledger T',subtitle='case / action\nsource / verdict')
    s.node('trace_detail',54,160,65,17,role='runtime',shape='state')
    trace=f['worked_trace']
    s.text(56,173.7,f"{trace['id']}  /  evidence behind the edits",size=7.7,weight='bold',owner='trace_detail',color=COLORS['runtime'][1])
    s.text(56,168.8,f"Source: {trace['source_value']} · {trace['source_date']}",size=7.4,owner='trace_detail')
    s.text(56,164,f"Answer: {trace['baseline_answer']}  ·  {trace['omission']}",size=7.3,owner='trace_detail')
    s.node('context',132,201,38,5,role='proposal',shape='state',fill='role')
    s.text(151,203.5,'Shared proposer context',size=7.4,weight='bold',ha='center',owner='context',color=COLORS['proposal'][1])
    for p,y in zip(f['proposals'],[188,173,158]):
        identifier=p['id'].lower()
        title=f"{p['id']} · {p['key']}"
        subtitle=f"evidence {p['evidence']}"
        s.node(identifier,132,y,30,10,role='proposal')
        s.text(134,y+7.2,title,size=7.6,weight='bold',owner=identifier,color=COLORS['proposal'][1])
        s.text(134,y+3,subtitle,size=7.2,owner=identifier)
    for i,y in enumerate([193,178,163],1):
        s.junction(f'in{i}',125,y,'proposal')
        s.junction(f'out{i}',168,y,'proposal')
    s.node('merge',132,143,38,13,role='proposal',fill='role',title='Arbitrate + budget',subtitle='conflicts → panel b')
    s.node('candidate',87,143,32,13,role='runtime',shape='document',title='Candidate record',subtitle='base ID + patch set',title_size=7.8,body_size=7.2)
    s.node('gate',44,143,33,13,role='validation',shape='gate',fill='role',title='Paired replay',subtitle='strict improvement',body_size=7.3)
    s.node('accepted',6,143,26,13,role='accept',shape='document',title='Commit',subtitle='atomic snapshot')
    s.node('rejected',44,127,33,10,role='reject',title='Rejected edits',title_size=7.6)
    s.text(46,129.5,'block exact retry IDs',size=7.2,owner='rejected')
    s.node('validation',87,127,32,10,role='validation',shape='document',title='D_val · fixed cases',title_size=7.6)
    s.text(89,129.5,'selection gate only',size=7.2,owner='validation')
    s.node('test',6,127,26,10,role='neutral',shape='document',title='D_test · sealed',title_size=7.6)
    s.text(8,129.5,'final use only',size=7.2,owner='test')

    s.connect('training_to_runtime',('training','right'),('runtime','left',(190.5-181)/17),role='runtime')
    s.connect('memory_read',('current','right',.7),('runtime','bottom',6/34),via=((49,175.1),),role='runtime')
    s.connect('collect_traces',('runtime','right',(193-181)/17),('traces','left',(193-181)/17),role='runtime')
    s.connect('trace_expansion',('traces','bottom'),('trace_detail','top',49/65),role='runtime',kind='correspondence',arrow=False,linestyle=(0,(1,2)),width=.65)
    s.connect('trace_call_input',('traces','right',(193-181)/17),('in1','left'),role='proposal',arrow=False)
    s.connect('context_read',('context','left'),('in1','top'),via=((125,203.5),),role='proposal',arrow=False)
    for i in (1,2,3):
        s.connect(f'call_p{i}',(f'in{i}','right'),(f'p{i}','left'),role='proposal')
        s.connect(f'return_p{i}',(f'p{i}','right'),(f'out{i}','left'),role='proposal',arrow=False)
        if i<3:
            s.connect(f'input_bus_{i}',(f'in{i}','bottom'),(f'in{i+1}','top'),role='proposal',arrow=False)
            s.connect(f'output_bus_{i}',(f'out{i}','bottom'),(f'out{i+1}','top'),role='proposal',arrow=False)
    s.connect('collect_proposals',('out3','bottom'),('merge','top',36/38),role='proposal')
    s.connect('apply_patch',('merge','left'),('candidate','right'),role='runtime')
    s.connect('candidate_replay',('candidate','left'),('gate','right'),role='validation')
    s.connect('baseline_replay',('current','right',.3),('gate','left',9/13),via=((37,169.9),(37,152)),role='runtime')
    s.connect('accept_commit',('gate','left',.3),('accepted','right'),via=((37.5,146.9),(37.5,149.5)),role='accept')
    s.connect('install_snapshot',('accepted','top'),('current','bottom'),role='accept')
    s.text(22,161,'write',size=7.2,color=COLORS['accept'][1])
    s.connect('reject_buffer',('gate','bottom',.3),('rejected','top'),via=((53.9,140),(60.5,140)),role='reject',kind='rejection',linestyle=(0,(3,2)))
    s.connect('validation_read',('validation','top'),('gate','bottom',.7),via=((103,140),(67.1,140)),role='validation')
    s.connect('rejection_reuse',('rejected','right'),('merge','right'),via=((82,132),(82,122),(174,122),(174,149.5)),role='reject',kind='rejection',linestyle=(0,(3,2)))

    s.scope(3,102,172,17,'consolidation',dashed=True)
    s.node('epoch_replay',6,105,52,11,role='consolidation',title='Epoch replay of ledger T',title_size=7.8)
    s.text(8,107.5,'same cases · previous/current memory',size=7.2,owner='epoch_replay')
    s.node('reflection',67,105,47,11,role='consolidation',title='Reflect on state changes',title_size=7.8)
    s.text(69,107.5,'improved / regressed / unchanged',size=7.2,owner='reflection')
    s.node('policy',123,105,47,11,role='consolidation',title='Update proposer context',title_size=7.8)
    s.text(125,107.5,'next epoch; weights stay frozen',size=7.2,owner='policy')
    s.connect('compare_epoch',('epoch_replay','right'),('reflection','left'),role='consolidation')
    s.connect('consolidate',('reflection','right'),('policy','left'),role='consolidation')
    s.connect('epoch_context_update',('policy','right'),('context','right'),via=((176,110.5),(176,203.5)),role='consolidation',kind='epoch',linestyle=(0,(4,2,1,2)))
    s.correspondences.append({'source':'traces','target':'epoch_replay','artifact_id':'T',
                              'meaning':'Epoch snapshot of the same trace ledger; a cross-panel reference, not an additional execution edge.'})


def draw_transaction(s,f,r):
    s.panel('b','Expand the update: competing edits become one transaction',95)
    s.scope(3,48,172,42,'neutral')
    s.text(6,86.5,'1  Proposed atomic edits',size=8.5,weight='bold')
    s.text(67,86.5,'2  Conflict relation',size=8.5,weight='bold')
    s.text(119,86.5,'3  Candidate snapshot',size=8.5,weight='bold')
    s.text(58,83,'priority · source',size=7.2,ha='right',color=MUTED)
    for p,y in zip(f['proposals'],[74.5,63.5,52.5]):
        s.badge(6,y+2,p['id'],'proposal',w=7,h=4)
        s.text(16,y+5.3,f"{p['operation']} {p['key']}",size=7.2,weight='bold')
        s.text(16,y+1.3,p['value'],size=7.4)
        s.text(58,y+1.3,f"{p['priority']} · {p['evidence']}",size=7.2,ha='right',color=MUTED)
        if y>53:s.line([(6,y-1.7),(60,y-1.7)])
    x0,y0,cell=77,61.5,5.4
    for j,p in enumerate(f['proposals']):
        s.text(x0+j*cell+cell/2,y0+3*cell+2.4,p['id'],size=7.2,ha='center')
        s.text(x0-2.4,y0+(2-j)*cell+cell/2,p['id'],size=7.2,ha='right')
        for k in range(3):
            clash=r['conflicts'][j][k]
            face=COLORS['reject'][0] if clash else '#FFFFFF' if j!=k else '#E5E9ED'
            s.ax.add_patch(Rectangle((x0+k*cell,y0+(2-j)*cell),cell,cell,facecolor=face,edgecolor='#C5CED6',lw=.45,zorder=3))
            if clash:s.text(x0+k*cell+cell/2,y0+(2-j)*cell+cell/2,'×',size=9.5,weight='bold',ha='center',color=COLORS['reject'][1])
    s.text(66.5,57.5,'× = same target key',size=7.2,color=COLORS['reject'][1])
    s.text(66.5,52.5,f"Budget {f['edit_budget']} → {' + '.join(r['selected'])}",size=7.5,weight='bold',color=COLORS['proposal'][1])
    s.line([(114.5,51),(114.5,82)],color='#BBC7D2')
    s.text(119,80,'field',size=7.2,weight='bold',color=MUTED)
    s.text(141,80,'before → after',size=7.2,weight='bold',color=MUTED)
    rows=[(key,r['base'].get(key,'absent'),r['candidate'].get(key,'absent')) for key in ('units','freshness','citation')]
    for (key,before,after),y in zip(rows,[72.5,63.5,54.5]):
        s.text(119,y+1.6,key,size=7.4,weight='bold')
        s.text(141,y+3.3,before,size=7.2,color=MUTED)
        s.text(141,y-.2,'→ '+after,size=7.3,color=COLORS['accept' if before!=after else 'neutral'][1])
        if y>55:s.line([(119,y-3.2),(172,y-3.2)])


def draw_replay(s,f,r):
    s.panel('c','Replay a separate case, then commit or retain the baseline',40)
    s.text(6,33.5,f"Case {f['validation_trace']['id']} · output comparison",size=7.8,weight='bold')
    s.text(67,33.5,f['base_version'],size=7.6,weight='bold',ha='center')
    s.text(81,33.5,f['next_version'],size=7.6,weight='bold',ha='center')
    s.line([(6,30.5),(88,30.5)])
    field_names={'value':'Value','source_date':'Date','citation':'Citation'}
    for a,before,after,y in zip(f['assertions'],r['before'],r['after'],[26.5,21.5,16.5]):
        key=a['key']
        original=r['outputs']['baseline'][key]
        revised=r['outputs']['candidate'][key]
        output_label=f"{field_names[key]}: {original if original is not None else 'absent'} → {revised if revised is not None else 'absent'}"
        s.text(6,y,output_label,size=7.4)
        for x,value in [(67,before),(81,after)]:
            s.badge(x-5,y-1.8,'PASS' if value else 'FAIL','accept' if value else 'reject',w=10,h=3.6)
    n=len(f['assertions'])
    s.text(6,10.5,'Passed assertions',size=7.6,weight='bold')
    s.text(67,10.5,f"{sum(r['before'])}/{n}",size=8,ha='center',weight='bold')
    s.text(81,10.5,f"{sum(r['after'])}/{n}",size=8,ha='center',weight='bold',color=COLORS['accept'][1])
    s.scope(97,8,78,28,'accept')
    s.text(100,32,'AUDIT RECEIPT',size=7.4,weight='bold',color=COLORS['accept'][1])
    s.text(100,27,f"Base {f['base_version']}  →  commit {f['next_version']}",size=8.2,weight='bold')
    s.text(100,22,f"Edits: {' + '.join(r['selected'])}   ·   one atomic write",size=7.6)
    s.text(100,17,f"Guard: {sum(r['after'])} > {sum(r['before'])}   ·   record {r['candidate_hash']}",size=7.3,mono=True)
    s.text(100,12,f"P2 alone: {sum(r['alternate'])}/{n} → tie rejected",size=7.4,color=COLORS['reject'][1])
    s.text(4,3.5,'Fixture, not benchmark data. Solid: execution/access; dotted: detail; dashed: reject; dash-dot: epoch update.',size=7.2,color=MUTED)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--fixture',type=Path,default=Path(__file__).resolve().parents[1]/'assets/dense-method-fixture.json')
    ap.add_argument('--height-mm',type=float,default=200,help='Physical height; point-sized typography is preserved and the compacted layout is audited.')
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    f=json.loads(args.fixture.read_text()); result=evaluate_fixture(f)
    if ([p['id'] for p in f['proposals']]!=['P1','P2','P3'] or result['selected']!=['P1','P3']
            or f['edit_budget']!=2 or not result['accepted'] or result['alternate_accepted']
            or [sum(result[k]) for k in ('before','after','alternate')]!=[1,3,1]):
        raise ValueError('This example illustrates accepted P1/P3 and a rejected P2 alternative; adapt the diagram and caption for another protocol outcome.')
    family,mono,font_meta=select_fonts()
    with style_context(8):
        s=FigureScene(178,228,family,mono)
        s.text(4,223,'Evidence-guided memory refinement',size=11.2,weight='bold')
        s.text(174,223,'SCHEMATIC',size=7.8,weight='bold',color=MUTED,ha='right')
        draw_overview(s,f); draw_transaction(s,f,result); draw_replay(s,f,result)
        s.compact_height(args.height_mm)
        stem=args.out/'evidence_guided_memory'
        s.write_spec(stem.with_suffix('.scene.json'))
        audit=s.audit(stem.with_suffix('.audit.json'))
        stem.with_suffix('.fixture-result.json').write_text(json.dumps(result,indent=2)+'\n')
        # Preserve an inspectable preview even while fixing a failed audit.
        if audit['text_findings'] or audit['route_report']['issues']:
            s.fig.savefig(stem.with_suffix('.draft.png'),dpi=180)
            print(json.dumps({'audit':str(stem.with_suffix('.audit.json')),
                              'text_findings':audit['text_findings'],
                              'route_issues':audit['route_report']['issues']},indent=2))
            raise SystemExit('Fix scene audit findings before exporting final vectors.')
        paths=export_figure(s.fig,stem,source_files=[__file__,Path(__file__).with_name('figure_scene.py'),Path(__file__).with_name('figure_style.py'),Path(__file__).with_name('diagram_geometry.py'),Path(__file__).with_name('render_modern_examples.py'),args.fixture],
             metadata={'evidence_status':f['evidence_status'],'font_selection':font_meta,
                       'information_layers':['system','atomic operation','worked replay'],
                       'fixture_result':result,'source_design_jobs':f['source_design_jobs'],
                       'audit':str(stem.with_suffix('.audit.json'))})
        plt.close(s.fig)
    stem.with_suffix('.caption.md').write_text(
        '**Evidence-guided memory refinement (schematic).** (a) A frozen agent reads versioned memory. Parallel proposals are merged under a conflict and edit budget, '
        'replayed on fixed validation cases, then atomically committed or rejected. Rejection history blocks exact retries; the epoch loop updates proposer context. '
        'T identifies the same trace ledger in both scopes. (b) P1 and P2 target one field; priority and a two-edit budget select P1+P3. '
        '(c) A deterministic executor tests a separate toy case V01: the candidate passes 3/3 assertions versus 1/3; P2 alone ties and is rejected. '
        'This fixture illustrates one transaction, not empirical performance or a complete training run. Dotted lines expand details; dashed red and dash-dot teal indicate rejection and epoch updates.\n')
    stem.with_suffix('.design-note.md').write_text(
        '# Design and reproducibility note\n\n'
        'Evidence status: original schematic with a deterministic correctness fixture. No real model is trained and no empirical performance is claimed.\n\n'
        'The overview, exact conflict matrix, before/after record and replay share the same proposal IDs and fixture. The executable example evaluates one transaction '
        'and a P2 counterfactual, not the entire conceptual training loop. V01 has a distinct ID, value and date from the T08/T11 proposal evidence and is not used to propose edits. '
        'This constructed separation demonstrates the protocol, not empirical split generalization. The full loop is described by the scene topology. T11 is a table-header example supporting '
        'the competing units rule and is preserved in the input JSON. The arbiter excludes exactly repeated rejected proposal IDs. A changed proposal requires a new ID.\n\n'
        'The figure combines IdeaScientist Figure 1’s overview-plus-case structure with SkillOpt Figure 2’s parallel proposals and separate update timescales. '
        'The matrix principle is shared with exact-operator diagrams such as Native Sparse Attention. No source artwork or experimental values are copied.\n\n'
        f'Physical size: 178 × {args.height_mm:g} mm; type remains 7.2–11.2 pt. Vertical geometry is compacted without scaling point-sized text, then audited. '
        'The short caption leaves space in a full-page manuscript placement; check the actual venue text block. The long interpretation belongs here, outside the artwork.\n\n'
        'Blue denotes runtime/state, violet proposals, amber validation, teal epoch consolidation, green acceptance and red rejection. Pale scope fills sit behind '
        'white typed artifacts; dark related inks carry labels. Folded documents represent data/state, rounded rectangles computation, double borders a validation gate, '
        'and explicit dots branch buses. Dotted blue connectors indicate detail; dashed red rejection; dash-dot teal epoch updates.\n\n'
        'The scene contains 19 semantic nodes, six junctions and 28 declared routes. These are descriptive counts, not an aesthetic score. The audit checks actual '
        'text bounds, owner containment, text overlap, ports, route centerlines and unintended intersections. It does not certify all painted arrowhead clearances '
        'or scientific validity. Inspect the final PDF and grayscale.\n\n'
        'Regenerate with `python source/render_dense_method.py --fixture data/dense-method-fixture.json --out regenerated`. '
        'The companion fixture-result JSON records selected edits, conflict relations, all outputs, assertion results and a hash derived from the candidate record.\n')
    stem.with_suffix('.alt.txt').write_text(
        'Three-panel schematic. Top: source-tagged training cases and current memory enter a frozen agent, which emits a trace ledger. '
        'Three parallel proposals merge under a conflict budget. A paired validation gate commits an improving candidate or stores rejected edits. '
        'A separate epoch lane updates shared proposer context. Middle: an indexed conflict matrix excludes the competing units proposal, '
        'and a before/after record adds explicit units and source date while preserving citation. Bottom: three labeled assertions show '
        'one baseline pass and three candidate passes; an audit receipt records the two selected edits and atomic version transition.\n')
    print(json.dumps({'outputs':paths,'nodes':audit['semantic_nodes'],'junctions':audit['junctions'],
                      'routes':audit['routes'],'minimum_font_pt':audit['minimum_font_pt']},indent=2))


if __name__=='__main__':
    main()
