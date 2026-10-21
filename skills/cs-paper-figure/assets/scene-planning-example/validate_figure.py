#!/usr/bin/env python3
"""Independent numerical, spatial, observation, and export checks.

Run after render_figure.py. These checks are specific to the preserved fixture;
they are not a general planner benchmark or proof of aesthetic quality.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scene_model import load_fixture, rollout, segment_aabb, segment_circle

HERE=Path(__file__).resolve().parent


def closed_segments_meet(a,b,c,d):
    def cross(p,q,r):
        return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    def on(p,q,r):
        return abs(cross(p,q,r))<1e-10 and min(p[0],q[0])-1e-10<=r[0]<=max(p[0],q[0])+1e-10 and min(p[1],q[1])-1e-10<=r[1]<=max(p[1],q[1])+1e-10
    o1,o2,o3,o4=cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
    return bool((o1*o2<0 and o3*o4<0) or on(a,b,c) or on(a,b,d) or on(c,d,a) or on(c,d,b))


def independent_aabb(p,q,b):
    inside=lambda a:b[0]<=a[0]<=b[1] and b[2]<=a[1]<=b[3]
    corners=[(b[0],b[2]),(b[1],b[2]),(b[1],b[3]),(b[0],b[3])]
    return inside(p) or inside(q) or any(closed_segments_meet(p,q,corners[k],corners[(k+1)%4]) for k in range(4))


def independent_circle(p,q,center,radius):
    # Solve line/circle quadratic and intersect its interior interval with [0,1].
    p,q,center=map(lambda z:np.asarray(z,float),(p,q,center))
    v=q-p; f=p-center
    aa=float(v@v); bb=float(2*(f@v)); cc=float(f@f-radius**2)
    if aa<1e-24:
        return cc<=1e-12
    disc=bb*bb-4*aa*cc
    if disc < -1e-12:
        return False
    root=math.sqrt(max(0,disc))
    lo,hi=sorted(((-bb-root)/(2*aa),(-bb+root)/(2*aa)))
    return max(0,lo)<=min(1,hi)+1e-12


def validate(out):
    f=load_fixture(); computed=rollout(f)
    saved=json.loads((out/"computed_rollouts.json").read_text())
    assert computed==saved,"Saved rollout is stale"
    cand={r['id']:r for r in computed['candidates']}
    expected_states={
        'D':[[1,3],[3,3],[5,3],[7,3],[9,3]],
        'U':[[1,3],[2.5,4.8],[4.8,4.8],[6.8,5.5],[9,3]],
        'L':[[1,3],[2.5,1.2],[4.8,1.2],[6.8,1.8],[9,3]],
    }
    expected_effort={'D':16.0,'U':26.36,'L':21.42}
    expected_cost={'D':101.6,'U':2.636,'L':2.142}
    tested=0
    for cid,r in cand.items():
        np.testing.assert_allclose(r['states'],expected_states[cid],atol=1e-12,rtol=0)
        assert abs(r['effort']-expected_effort[cid])<1e-12
        assert abs(r['cost']-expected_cost[cid])<1e-12
        assert r['terminal_squared_distance']<1e-24
        for segment in r['segments']:
            assert segment['within_room']
            for obstacle,reported in zip(f['scene']['obstacles'],segment['obstacles']):
                independent=independent_aabb(segment['from'],segment['to'],obstacle['bounds']) if obstacle['type']=='aabb' else independent_circle(segment['from'],segment['to'],obstacle['center'],obstacle['radius'])
                assert independent==reported['hit'],(cid,segment,obstacle)
                tested+=1
    flags={cid:[int(s['collision']) for s in r['segments']] for cid,r in cand.items()}
    assert flags=={'D':[0,1,0,0],'U':[0,0,0,0],'L':[0,0,0,0]}
    direct=cand['D']['segments'][1]
    np.testing.assert_allclose(direct['obstacles'][0]['interval'],[.2,.8],atol=1e-12,rtol=0)
    A=f['scene']['obstacles'][0]['bounds']
    assert not independent_aabb(direct['from'],direct['from'],A)
    assert not independent_aabb(direct['to'],direct['to'],A)
    assert computed['selected_id']=='L'
    assert computed['executed_action_count']==1
    assert len(computed['unexecuted_selected_actions'])==3
    np.testing.assert_allclose(computed['executed_action'],[1.5,-1.8],atol=1e-12)
    np.testing.assert_allclose(computed['next_state']['agent']['position'],[2.5,1.2],atol=1e-12)
    assert computed['initial_state']['obstacles']==computed['next_state']['obstacles']
    assert computed['initial_state']['goal']==computed['next_state']['goal']

    edge_cases=[]
    for name,got,expected in [
        ('aabb parallel outside',segment_aabb([0,0],[8,0],A)['hit'],False),
        ('aabb corner contact',segment_aabb([2.4,.8],[3.4,1.8],A)['hit'],True),
        ('aabb zero inside',segment_aabb([4,3],[4,3],A)['hit'],True),
        ('aabb zero outside',segment_aabb([1,3],[1,3],A)['hit'],False),
        ('circle tangent',segment_circle([-2,1],[2,1],[0,0],1)['hit'],True),
        ('circle near miss',segment_circle([-2,1.00001],[2,1.00001],[0,0],1)['hit'],False),
        ('circle zero inside',segment_circle([.5,0],[.5,0],[0,0],1)['hit'],True),
        ('circle zero outside',segment_circle([2,0],[2,0],[0,0],1)['hit'],False),
    ]:
        assert got==expected,name
        edge_cases.append({'case':name,'passed':True})
    # Demonstrate the exact execution guard and finite-penalty scope. This is a
    # validation fixture only, never used to populate the published figure.
    unsafe=copy.deepcopy(f)
    unsafe['candidates']=[{'id':'X','name':'unsafe first step','actions':[[3,0],[0,0],[0,0],[0,0]]}]
    try:
        rollout(unsafe)
        raise AssertionError('Unsafe first action was not blocked')
    except ValueError as error:
        assert 'unsafe' in str(error).lower()
    finite_penalty=copy.deepcopy(f)
    finite_penalty['objective']['collision_penalty']=.01
    counterexample=rollout(finite_penalty)
    assert counterexample['selected_id']=='D'
    assert next(r for r in counterexample['candidates'] if r['id']=='D')['collision']==1
    # Its first segment is still safe; the guard does not claim that the
    # remainder of a selected finite-penalty trajectory is feasible.
    assert not next(r for r in counterexample['candidates'] if r['id']=='D')['segments'][0]['collision']

    geometry=json.loads((out/'geometry_audit.json').read_text())
    assert not geometry['pairwise_text_overlap']
    assert not geometry['outside_canvas']
    assert min(t['font_pt'] for t in geometry['text_bounds'])>=7.2
    for view in geometry['maps']:
        x,y,w,h=view['rect_mm']; xmin,xmax,ymin,ymax=view['world_bounds']
        sx,sy=view['scale_mm_per_unit']
        assert abs(sx-sy)<1e-12
        border_half_width_mm=.65*25.4/72/2
        assert x-border_half_width_mm>=0 and y-border_half_width_mm>=0 and x+w+border_half_width_mm<W+1e-10 and y+h+border_half_width_mm<H+1e-10
        to_world=lambda uv:[xmin+(uv[0]-x)/sx,ymax-(uv[1]-y)/sy]
        np.testing.assert_allclose(to_world(view['agent_mm']),view['agent_world'],atol=1e-12)
        if view['trajectory_world']:
            np.testing.assert_allclose([to_world(uv) for uv in view['trajectory_mm']],view['trajectory_world'],atol=1e-12)
        for o in view['obstacles']:
            raw=next(z for z in f['scene']['obstacles'] if z['id']==o['id'])
            if o['type']=='aabb':
                bx,by,bw,bh=o['bounds_mm']; a=to_world([bx,by]); b=to_world([bx+bw,by+bh])
                np.testing.assert_allclose([a[0],b[0],b[1],a[1]],raw['bounds'],atol=1e-12)
            else:
                np.testing.assert_allclose(to_world(o['center_mm']),raw['center'],atol=1e-12)
                assert abs(o['radius_mm']/sx-raw['radius'])<1e-12

    obs0=np.asarray(Image.open(out/'observation_o0.png').convert('RGB'))
    obs1=np.asarray(Image.open(out/'observation_o1.png').convert('RGB'))
    assert obs0.shape==obs1.shape==(360,600,3)
    changed=np.any(obs0!=obs1,axis=2)
    yy,xx=np.where(changed)
    centers=[[60,180],[150,288]]
    distance=np.minimum.reduce([(xx-cx)**2+(yy-cy)**2 for cx,cy in centers])
    assert np.max(distance)<=15**2,"Static scene changed outside the old/new point glyphs"
    assert np.any(changed)

    pdf=fitz.open(out/'scene_planning_figure.pdf'); page=pdf[0]
    width_mm=page.rect.width*25.4/72; height_mm=page.rect.height*25.4/72
    assert len(pdf)==1 and abs(width_mm-178)<1e-5 and abs(height_mm-203)<1e-5
    spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for ln in b['lines'] for s in ln['spans'] if s['text'].strip()]
    min_font=min(s['size'] for s in spans)
    assert min_font>=7.2-1e-5
    assert not page.get_images(full=True),'The figure PDF should be vector'
    assert len(page.get_drawings())>50
    pdf_text=page.get_text()
    for literal in ['101.600','2.636','2.142','3.4','4.6','0.55']:
        assert literal in pdf_text, literal
    fonts=[]
    for item in page.get_fonts(full=True):
        xref=item[0]; name,ext,fonttype,buffer=pdf.extract_font(xref)
        assert buffer,'Font is not embedded'
        assert ext=='ttf',f'Unexpected font program {ext}'
        fonts.append({'name':name,'extension':ext,'type':fonttype,'embedded_bytes':len(buffer)})
    pdf.close()
    tree=ET.parse(out/'scene_planning_figure.svg')
    svg_texts=tree.findall('.//{http://www.w3.org/2000/svg}text')
    svg_images=tree.findall('.//{http://www.w3.org/2000/svg}image')
    assert len(svg_texts)>80 and not svg_images
    png=Image.open(out/'scene_planning_figure.png')
    assert png.width==int(178/25.4*300) and png.height==int(203/25.4*300)
    subprocess.run(['pdftoppm','-r','180','-png','-singlefile',str(out/'scene_planning_figure.pdf'),str(out/'pdf_render_review')],check=True,capture_output=True)
    Image.open(out/'pdf_render_review.png').convert('L').save(out/'grayscale_review.png')

    report={
        'passed':True,
        'scope':'Deterministic fixture checks, not real-agent evaluation or a general safety guarantee.',
        'candidate_states':expected_states,
        'effort':expected_effort,'costs':expected_cost,
        'collision_flags_by_segment':flags,
        'independent_segment_obstacle_checks':tested,
        'independent_algorithms':{'aabb':'closed segment/rectangle edge intersection','circle':'quadratic roots on the segment parameter'},
        'direct_segment_hit_interval':[.2,.8],
        'free_endpoints_verified':True,
        'boundary_and_degenerate_cases':edge_cases,
        'unsafe_first_action_guard':'passed',
        'finite_penalty_scope_check':{'collision_penalty':.01,'selected_id':'D','selected_cost':1.61,
                                      'full_horizon_collision':True,'first_segment_safe':True,
                                      'meaning':'A low finite penalty can select a colliding nominal horizon; the execution guard certifies only its first segment. This is a validation counterexample, not the displayed fixture.'},
        'maximum_action_norm':max(n for r in cand.values() for n in r['action_norms']),
        'maximum_allowed_action_norm':f['dynamics']['max_action_norm'],
        'selected_id':computed['selected_id'],'executed_action':computed['executed_action'],
        'next_position':computed['next_state']['agent']['position'],'executed_action_count':1,
        'all_scene_maps_isotropic_and_reversible':True,
        'pairwise_text_overlaps':0,'out_of_canvas_text':0,
        'observation_size_px':[600,360],
        'observation_changed_pixels':int(changed.sum()),
        'observation_changes_confined_to_point_agent_glyphs':True,
        'export':{'pdf_pages':1,'width_mm':width_mm,'height_mm':height_mm,'minimum_pdf_font_pt':min_font,
                  'pdf_embedded_fonts':fonts,'pdf_raster_images':0,'svg_editable_text_elements':len(svg_texts),
                  'svg_raster_images':0,'png_size_px':[png.width,png.height],
                  'pdf_secondary_renderer':'Poppler pdftoppm at 180 dpi'},
        'manual_review_required':['Final color and grayscale appearance','trajectory/label reading order','caption scope and placement'],
        'fixture_sha256':hashlib.sha256((HERE/'scene_fixture.json').read_bytes()).hexdigest()
    }
    (out/'validation_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','costs','collision_flags_by_segment','independent_segment_obstacle_checks','pairwise_text_overlaps','export')},indent=2))


W,H=178,203
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,default=HERE)
    validate(p.parse_args().out.resolve())
