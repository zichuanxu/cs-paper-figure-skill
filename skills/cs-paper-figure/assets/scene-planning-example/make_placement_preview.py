#!/usr/bin/env python3
"""Render a PNG-only manuscript placement proof; do not modify the artwork."""
import argparse
import json
import os
from pathlib import Path

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--out',type=Path,default=HERE)
args=parser.parse_args(); out=args.out.resolve()
os.environ.setdefault('MPLCONFIGDIR',str(out/'_work'/'mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
import matplotlib.image as mpimg

manifest=json.loads((out/'scene_planning_figure.manifest.json').read_text())
font=FontProperties(fname=manifest['metadata']['font_programs']['regular'],size=8)
caption=(HERE/'caption_short.txt').read_text().strip()
lines=[]; current=''
for word in caption.split():
    probe=(current+' '+word).strip()
    width=TextPath((0,0),probe,prop=font).get_extents().width*25.4/72
    if current and width>178:
        lines.append(current); current=word
    else:
        current=probe
if current: lines.append(current)
page_w,page_h=210,250
art_x,art_y,art_w,art_h=16,6,178,203
gap=3
leading=10*25.4/72
caption_y=art_y+art_h+gap+8*25.4/72
fig=plt.figure(figsize=(page_w/25.4,page_h/25.4))
ax=fig.add_axes([0,0,1,1]); ax.set(xlim=(0,page_w),ylim=(page_h,0)); ax.axis('off')
img=mpimg.imread(out/'pdf_render_review.png')
ax.imshow(img,extent=(art_x,art_x+art_w,art_y+art_h,art_y),aspect='auto')
for i,line in enumerate(lines):
    ax.text(art_x,caption_y+i*leading,line,fontproperties=font,color='#233746',va='baseline')
assert caption_y+(len(lines)-1)*leading+1<page_h-6
fig.savefig(out/'manuscript_placement_preview.png',dpi=180,facecolor='white')
plt.close(fig)
report={'page_mm':[page_w,page_h],'artwork_mm':[art_w,art_h],
        'artwork_placement_mm':[art_x,art_y],'caption_gap_mm':gap,
        'caption_font_pt':8,'caption_leading_pt':10,'caption_lines':len(lines),
        'caption_words':len(caption.split()),'caption_region_height_mm':len(lines)*leading,
        'artwork_plus_gap_plus_caption_mm':art_h+gap+len(lines)*leading,
        'scope':'Illustrative placement proof, not a claim about a particular venue template.'}
(out/'placement_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
