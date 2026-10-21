"""Physical-unit vector components for dense scientific method figures.

The scene owns explicit nodes, ports, routed edges, and measured text bounds.
Background scopes and internal glyphs are not routing obstacles. It does not
infer a method, validate statistical claims, or replace inspection of the PDF.
"""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path as MplPath
from matplotlib.transforms import Affine2D

from diagram_geometry import Label, Node, Port, Rect, Route, port_point, validate_diagram

INK = '#243343'
MUTED = '#536575'
COLORS = {
    'runtime': ('#EAF1FA', '#35619A'),
    'proposal': ('#F0EAF7', '#7954A1'),
    'validation': ('#FFF1D6', '#956419'),
    'consolidation': ('#E6F3F0', '#24766D'),
    'accept': ('#E9F3E7', '#427540'),
    'reject': ('#FBECE8', '#A74635'),
    'neutral': ('#F2F4F6', '#6B7986'),
}


class FigureScene:
    """A millimetre Cartesian canvas (origin lower left), with editable text."""

    def __init__(self, width_mm, height_mm, family='DejaVu Sans', mono='DejaVu Sans Mono'):
        self.width, self.height = width_mm, height_mm
        self.family, self.mono = family, mono
        self.fig = plt.figure(figsize=(width_mm / 25.4, height_mm / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set(xlim=(0, width_mm), ylim=(0, height_mm))
        self.ax.set_axis_off()
        self.nodes, self.routes, self.texts, self.correspondences = {}, [], [], []
        self.node_roles, self.route_styles = {}, {}

    def text(self, x, y, value, size=7.6, weight='normal', color=INK,
             ha='left', va='center', mono=False, owner=None, tag=None, **kwargs):
        if size < 7:
            raise ValueError('Dense-scene text must be at least 7 pt; reflow content.')
        t = self.ax.text(x, y, value, fontsize=size, fontweight=weight, color=color,
                         ha=ha, va=va, fontfamily=self.mono if mono else self.family,
                         linespacing=1.2, zorder=8, **kwargs)
        self.texts.append((t, owner, tag or f'text-{len(self.texts):03d}'))
        return t

    def scope(self, x, y, w, h, role='neutral', dashed=False, radius=1.6):
        fill, stroke = COLORS[role]
        p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={radius}',
                          facecolor=fill, edgecolor=stroke, linewidth=.55,
                          linestyle=(0, (4, 3)) if dashed else '-', zorder=0)
        self.ax.add_patch(p)
        return p

    def node(self, identifier, x, y, w, h, role='neutral', shape='process', fill='white',
             title=None, subtitle=None, title_size=8, body_size=7.4):
        if identifier in self.nodes:
            raise ValueError(f'Duplicate node {identifier}')
        self.nodes[identifier] = Node(identifier, Rect(x, y, x + w, y + h))
        self.node_roles[identifier] = {'role': role, 'shape': shape}
        pale, stroke = COLORS[role]
        fill = pale if fill == 'role' else fill
        if shape == 'document':
            fold = min(2.4, h / 4)
            self.ax.add_patch(Polygon([(x, y), (x+w, y), (x+w, y+h-fold),
                                      (x+w-fold, y+h), (x, y+h)], closed=True,
                                     facecolor=fill, edgecolor=stroke, linewidth=.75, zorder=3))
            self.ax.plot([x+w-fold, x+w-fold, x+w], [y+h, y+h-fold, y+h-fold],
                         color=stroke, lw=.65, zorder=4)
        elif shape == 'junction':
            self.ax.add_patch(Circle((x+w/2, y+h/2), w/2, color=stroke, linewidth=0, zorder=5))
        else:
            self.ax.add_patch(FancyBboxPatch((x, y), w, h,
                             boxstyle=f'round,pad=0,rounding_size={1.1 if shape == "process" else .15}',
                             facecolor=fill, edgecolor=stroke, linewidth=.8, zorder=3))
            if shape == 'gate':
                self.ax.add_patch(Rectangle((x+.65,y+.65), w-1.3,h-1.3,
                                           fill=False,edgecolor=stroke,linewidth=.4,zorder=4))
        if title:
            self.text(x+2, y+h-3.3, title, size=title_size, weight='bold',
                      color=stroke, owner=identifier)
        if subtitle:
            self.text(x+2, y+h-7.1, subtitle, size=body_size, va='top', owner=identifier)
        return self.nodes[identifier]

    def junction(self, identifier, x, y, role='neutral', diameter=.8):
        return self.node(identifier, x-diameter/2, y-diameter/2, diameter, diameter,
                         role=role, shape='junction')

    def connect(self, identifier, source, target, via=(), role='neutral', kind='data',
                arrow=True, linestyle='-', width=.85):
        """source/target are (node id, side[, fractional offset]); via are mm points."""
        sp, tp = Port(*source, kind=kind), Port(*target, kind=kind)
        points = (port_point(sp, self.nodes), *via, port_point(tp, self.nodes))
        route = Route(identifier, sp, tp, tuple(points), kind=kind)
        self.routes.append(route)
        stroke = COLORS[role][1]
        path = MplPath(points, [MplPath.MOVETO] + [MplPath.LINETO] * (len(points)-1))
        self.ax.add_patch(PathPatch(path, fill=False, edgecolor=stroke, linewidth=width,
                                   linestyle=linestyle, capstyle='round', joinstyle='round', zorder=2))
        if arrow:
            a, b = points[-2:]
            dx, dy = b[0]-a[0], b[1]-a[1]
            length = (dx*dx+dy*dy)**.5
            if length < 1.4:
                raise ValueError(f'{identifier}: final segment too short for an arrowhead')
            start = (b[0]-dx/length*min(length, 2.0), b[1]-dy/length*min(length,2.0))
            self.ax.add_patch(FancyArrowPatch(start, b, arrowstyle='-|>', mutation_scale=7,
                             linewidth=width, color=stroke, shrinkA=0, shrinkB=0, zorder=5))
        self.route_styles[identifier] = {'role':role,'arrow':arrow,'linestyle':str(linestyle)}
        return route

    def line(self, points, color='#C7D1DB', width=.5, style='-', zorder=4):
        """Internal table rules and glyphs, not computational edges."""
        self.ax.plot(*zip(*points), color=color, lw=width, linestyle=style, zorder=zorder)

    def badge(self, x, y, label, role='runtime', w=7, h=4):
        fill, stroke = COLORS[role]
        self.ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=.7',
                                       facecolor=fill,edgecolor=stroke,linewidth=.45,zorder=5))
        self.text(x+w/2,y+h/2,label,size=7.2,weight='bold',color=stroke,ha='center')

    def panel(self, letter, title, y, note=None):
        self.text(4, y, letter, size=10.2, weight='bold')
        self.text(10, y, title, size=9.7, weight='bold')
        if note:
            self.text(self.width-4, y, note, size=7.2, color=MUTED, ha='right')

    def compact_height(self, height_mm):
        """Reposition geometry vertically without shrinking point-sized text.

        Call once after composition and before auditing. This is useful for
        reclaiming vertical whitespace, but may create text collisions; audit
        the new layout and inspect the PDF. Geometry records remain actual mm.
        """
        if getattr(self,'_height_compacted',False):
            raise ValueError('Vertical compaction may be applied only once.')
        if not 0 < height_mm <= self.height:
            raise ValueError('Compacted height must be positive and no larger than the canvas.')
        factor=height_mm/self.height
        affine=Affine2D().scale(1,factor)
        for patch in self.ax.patches:
            patch.set_transform((patch.get_data_transform()-self.ax.transData)+affine+self.ax.transData)
        for line in self.ax.lines:
            line.set_transform((line.get_transform()-self.ax.transData)+affine+self.ax.transData)
        for t,_,_ in self.texts:
            x,y=t.get_position();t.set_position((x,y*factor))
        self.nodes={key:Node(node.id,Rect(node.rect.x0,node.rect.y0*factor,node.rect.x1,node.rect.y1*factor))
                    for key,node in self.nodes.items()}
        self.routes=[Route(r.id,r.source,r.target,tuple((x,y*factor) for x,y in r.points),
                           r.kind,r.allow_crossings_with) for r in self.routes]
        self.height=height_mm
        self.fig.set_size_inches(self.width/25.4,height_mm/25.4)
        self.ax.set_ylim(0,height_mm)
        self._height_compacted=True

    def audit(self, out=None, label_clearance_mm=.35):
        """Audit actual text bounds, owner containment, orthogonal edges and ports.

        Returns all findings instead of silently changing layout. Pairwise text
        overlap uses rectangular extents; inspect any intended typographic overlap.
        """
        self.fig.canvas.draw()
        renderer, inverse = self.fig.canvas.get_renderer(), self.ax.transData.inverted()
        labels, bounds, findings = [], [], []
        for text, owner, tag in self.texts:
            b = text.get_window_extent(renderer).transformed(inverse)
            rect = Rect(*map(float, b.extents))
            labels.append(Label(tag, rect))
            bounds.append((tag, text.get_text(), rect, owner))
            if rect.x0 < 0 or rect.y0 < 0 or rect.x1 > self.width or rect.y1 > self.height:
                findings.append({'kind':'canvas_text_overflow','id':tag,'text':text.get_text()})
            if owner:
                r=self.nodes[owner].rect
                if rect.x0 < r.x0+.5 or rect.x1 > r.x1-.5 or rect.y0 < r.y0+.5 or rect.y1 > r.y1-.5:
                    findings.append({'kind':'owner_text_overflow','id':tag,'owner':owner,'text':text.get_text()})
        for i,(tag,text,r,owner) in enumerate(bounds):
            for tag2,text2,s,owner2 in bounds[i+1:]:
                w,h=min(r.x1,s.x1)-max(r.x0,s.x0),min(r.y1,s.y1)-max(r.y0,s.y0)
                if w>.12 and h>.12:
                    findings.append({'kind':'text_overlap','ids':[tag,tag2],'texts':[text,text2],
                                     'overlap_mm':[round(w,3),round(h,3)]})
        geometry=validate_diagram(self.nodes,self.routes,labels=labels,
                                  clearance=label_clearance_mm,units='mm')
        result={'schema_version':1,'dimensions_mm':[self.width,self.height],
                'semantic_nodes':sum(n['shape']!='junction' for n in self.node_roles.values()),
                'junctions':sum(n['shape']=='junction' for n in self.node_roles.values()),
                'routes':len(self.routes),'text_items':len(self.texts),
                'minimum_font_pt':min(t.get_fontsize() for t,_,_ in self.texts),
                'text_findings':findings,'route_report':asdict(geometry),
                'limitations':['Centerline geometry does not model all arrowhead paint.',
                               'Scientific correctness and aesthetics require human/agent review.',
                               'Node rectangles approximate curved corners; ports must avoid corners.']}
        if out:
            Path(out).write_text(json.dumps(result,indent=2)+'\n')
        return result

    def write_spec(self, out):
        payload={'dimensions_mm':[self.width,self.height], 'nodes':[asdict(n) for n in self.nodes.values()],
                 'node_roles':self.node_roles,'routes':[asdict(r) for r in self.routes],
                 'route_styles':self.route_styles,'cross_panel_correspondences':self.correspondences}
        Path(out).write_text(json.dumps(payload,indent=2)+'\n')
