"""Redesign of MemT-1.0 (arXiv 2610.26825v2) Figure 4: architecture of native memory.

Content is taken from Sec. 2 of the paper only:
  theta_t = {backbone theta_b (unchanged), hyper memory phi (trained offline, fixed online),
             local memory M_t^(l) in R^{H_kv x d_k x d_v} (M = 0 at a new trajectory)}
  A = A_ori + A_mem;  A_mem = Concat_h[RMSNorm(Q M / sqrt(d_k)) ⊙ SoftCapSiLU(G)]
  Q = L2Norm(H~ W~_Q);  G = H~ W_g/d W_g/u
  storage at turn end over S_t = X_t || Y_t, token level i = 1..L_t:
  M~_i = [I - U_i^T U_i] D_i M~_{i-1} + U_i^T (w_i ⊙ V_i),  U_i = sqrt(b_i) ⊙ K_i,  D_i = Diag(exp(l_i))
  M~_0 = M_t,  M_{t+1} = M~_{L_t}
Matrix cell shading is an illustrative texture, not data.

    python render_fig4.py --out <dir>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, ROLE, INK, MUTED, LINE  # noqa: E402

FZ, MEM, WR, PHI = ROLE["frozen"], ROLE["memory"], ROLE["purple"], ROLE["amber"]
ER, DC = ROLE["coral"], ROLE["teal"]
GEN = dict(ROLE["neutral"], soft="#C9CED6", stroke="#7F8894")  # generated tokens: darker neutral
W, H = 170, 108


def card(cv, x, y, w, h, r, title):
    cv.group(x, y, w, h, r, title, band=True, size=7.4, radius=2.0, lw=0.7,
             fill="white" if r != "memory" or w > 30 else None)


def panel_a(cv):
    card(cv, 2, 30, 32, 76, "frozen", "(a) MemT-1.0")
    cx = 18
    cv.text(cx, 34.2, r"$S_{t,k}=X_t\,\|\,Y_{t,<k}$", size=6.8)
    cv.arrow([(cx, 36.4), (cx, 39.5)])
    cv.box(7, 39.5, 22, 5.2, "frozen", "Embedding", weight="normal")
    blocks = []
    for y0 in (48.5, 66.5):
        cv.box(6.5, y0, 23, 13.5, "frozen", lw=0.7, shadow=y0 > 60)
        cv.text(cx, y0 + 10.4, "Transformer block", size=6.6, color=FZ["ink"])
        cv.box(8.3, y0 + 1.6, 19.4, 5.6, "memory", "Native memory", weight="bold", size=6.6, lw=0.7)
        blocks.append((6.5, y0, 23, 13.5))
    cv.arrow([(cx, 44.7), (cx, 48.5)])
    cv.arrow([(cx, 62), (cx, 63.2)], head=1.1)
    cv.text(cx, 64.5, r"$\vdots$", size=7, color=LINE)
    cv.arrow([(cx, 65.3), (cx, 66.5)], head=1.1)
    cv.brace(5.4, 48.5, 80, side="left", depth=1.2)
    cv.text(3.6, 64.3, r"$\times L$", size=6.6, ha="center", rotation=90)
    cv.arrow([(cx, 80), (cx, 83.5)])
    cv.box(7, 83.5, 22, 5.2, "frozen", "Norm", weight="normal")
    cv.arrow([(cx, 88.7), (cx, 91.2)])
    cv.box(7, 91.2, 22, 5.2, "frozen", "LM head", weight="normal")
    cv.arrow([(cx, 96.4), (cx, 99.0)])
    cv.text(cx, 100.4, r"$y_{t,k}$", size=7)
    return blocks[1]


def panel_b(cv):
    card(cv, 37, 30, 42, 76, "frozen", r"(b) Transformer block $l$")
    cx = 58
    cv.text(cx, 33.6, r"$\mathbf{H}^{(l-1)}$", size=7)
    cv.arrow([(cx, 35.5), (cx, 40)])
    cv.box(45, 40, 26, 6, "frozen", "Pre-Attention", weight="normal", icon="snow")
    cv.line([(cx, 46), (cx, 51.5)])
    cv.dot(cx, 51.5)
    cv.text(cx + 1.0, 49.0, r"$\tilde{\mathbf{H}}^{(l)}$", size=6.8, ha="left")
    cv.arrow([(cx, 51.5), (48.5, 51.5), (48.5, 56)])
    cv.arrow([(cx, 51.5), (68, 51.5), (68, 56)])
    cv.box(39.5, 56, 18, 10.5, "frozen", "Original", "attention", icon="snow")
    cv.box(59, 56, 18, 10.5, "memory", "Memory attn.", r"see (c), (d)", lw=0.9, shadow=True)
    cv.op(cx, 71.5, "+", d=3.0)
    cv.arrow([(48.5, 66.5), (48.5, 71.5), (cx - 1.5, 71.5)])
    cv.arrow([(68, 66.5), (68, 71.5), (cx + 1.5, 71.5)], color=MEM["mark"], lw=0.8)
    cv.text(44.6, 69.0, r"$\mathbf{A}_{\mathrm{ori}}$", size=6.4, color=FZ["ink"])
    cv.text(72.4, 69.0, r"$\mathbf{A}_{\mathrm{mem}}$", size=6.4, color=MEM["ink"])
    cv.arrow([(cx, 73), (cx, 77.5)])
    cv.text(cx + 1.2, 75.2, r"$\mathbf{A}^{(l)}$", size=6.4, ha="left")
    cv.box(45, 77.5, 26, 6, "frozen", "Post-Attention", weight="normal", icon="snow")
    cv.arrow([(cx, 37.5), (41.2, 37.5), (41.2, 80.5), (45, 80.5)], color="#8C96A3", lw=0.55, head=1.15)
    cv.dot(cx, 37.5, color="#8C96A3", d=0.8)
    cv.arrow([(cx, 83.5), (cx, 87.6)])
    cv.text(cx, 89.2, r"$\mathbf{H}^{(l)}$", size=7)
    cv.rich(cx, 95.4, [(r"$\mathbf{A}^{(l)}=$", INK), (r"$\mathbf{A}^{(l)}_{\mathrm{ori}}$", FZ["ink"]),
                       (r"$\,+\,$", INK), (r"$\mathbf{A}^{(l)}_{\mathrm{mem}}$", MEM["ink"])], size=7.2, ha="center")
    cv.text(cx, 92.2, "backbone ops unchanged", size=5.9, color=MUTED, style="italic")
    return (37, 30, 42, 76)


def pillar(cv):
    card(cv, 82, 30, 19.5, 76, "memory", "Local memory")
    cv.text(91.7, 96.2, r"$\mathbf{M}_t^{(l)}$", size=9, color=MEM["ink"])
    cv.matrix(85.3, 76.5, 9.6, 9.6, rows=5, cols=5, depth=3, r="memory", dx=1.2, dy=1.2, seed=3)
    cv.text(91.7, 72.6, r"$\in\mathbb{R}^{H_{kv}\times d_k\times d_v}$", size=6.4, color=MEM["ink"])
    cv.text(91.7, 68.4, r"$H_{kv}$ channels", size=6.2, color=MUTED)
    cv.icon_cycle(86.2, 60.2, 3.0, color=MEM["mark"])
    cv.text(88.6, 61.1, "evolves", size=6.1, color=MEM["ink"], ha="left")
    cv.text(88.6, 58.7, "online", size=6.1, color=MEM["ink"], ha="left")
    cv.text(91.7, 52.8, r"$\mathbf{M}_1=\mathbf{0}$", size=6.6, color=INK)
    cv.text(91.7, 50.0, "at a new", size=6.2, color=MUTED)
    cv.text(91.7, 47.6, "trajectory", size=6.2, color=MUTED)


def panel_c(cv):
    card(cv, 104.5, 76, 63.5, 30, "memory", "(c) Utilization: read at every token")
    yq, yg = 92.4, 82.0
    cv.text(106.6, 87.2, r"$\tilde{\mathbf{H}}_t$", size=7.2, ha="left")
    cv.line([(110.2, 87.2), (111.4, 87.2)])
    cv.dot(111.4, 87.2)
    cv.arrow([(111.4, 87.2), (111.4, yq), (113.4, yq)])
    cv.arrow([(111.4, 87.2), (111.4, yg), (113.4, yg)])
    # query lane: amber trapezoid = hyper-memory projection (phi)
    cv.trap(113.4, yq - 3.2, 7.0, 6.4, "amber", narrow="right", title=r"$\tilde{\mathbf{W}}_Q$", size=6.6)
    cv.arrow([(120.4, yq), (123.0, yq)], head=1.1)
    cv.vec(123.0, yq - 0.75, n=3, cell=1.5, r="memory", seed=7)
    cv.text(125.25, yq + 2.2, r"$\mathbf{Q}$", size=6.8, color=MEM["ink"])
    cv.text(125.25, yq - 2.4, "L2Norm", size=6.0, color=MUTED)
    cv.arrow([(127.5, yq), (130.4, yq)], head=1.1)
    cv.box(130.4, yq - 3.6, 16.2, 7.2, "memory", "Readout", r"$\mathbf{Q}\mathbf{M}_t/\sqrt{d_k}$",
           fill=MEM["soft"], size=6.7, gap=1.55, lw=0.85, shadow=True)
    cv.arrow([(146.6, yq), (148.8, yq)], head=1.1)
    cv.box(148.8, yq - 2.8, 10.6, 5.6, "memory", "RMSNorm", fill="white", weight="normal", size=6.3)
    # gate lane: low-rank pair W_g/d, W_g/u
    cv.trap(113.4, yg - 3.0, 4.6, 6.0, "amber", narrow="right")
    cv.trap(118.4, yg - 3.0, 4.6, 6.0, "amber", narrow="left")
    cv.text(118.2, yg - 4.5, r"$\mathbf{W}_{g/d}\,\mathbf{W}_{g/u}$", size=6.2, color=PHI["ink"])
    cv.text(125.25, yg + 1.6, r"$\mathbf{G}$", size=6.8, color=MEM["ink"])
    cv.arrow([(123.0, yg), (130.4, yg)], head=1.1)
    cv.box(130.4, yg - 3.6, 19.0, 7.2, "memory", "SoftCapSiLU", r"$\tau\tanh(\mathrm{SiLU}(x)/\tau)$",
           fill="white", size=6.5, gap=1.55)
    ox = 155.0
    cv.op(ox, yg, ".", d=2.8)
    cv.arrow([(ox, yq - 2.8), (ox, yg + 1.4)], head=1.1)
    cv.arrow([(149.4, yg), (ox - 1.4, yg)], head=1.0)
    cv.arrow([(ox + 1.4, yg), (166.4, yg)], head=1.3, color=MEM["mark"], lw=0.9)
    cv.text(166.6, yg + 2.3, r"$\mathbf{A}_{\mathrm{mem}}\!\rightarrow\!$(b)", size=6.7, color=MEM["ink"], ha="right")
    cv.text(166.6, yg - 2.5, r"concat $H_q$ heads", size=6.1, color=MUTED, ha="right")
    # the state is read here only
    cv.arrow([(101.5, 98.4), (138.5, 98.4), (138.5, yq + 3.6)], color=MEM["mark"], lw=1.0, head=1.4)
    cv.chip(121.0, 98.4, r"read $\mathbf{M}_t$", "memory", size=6.0, pad=0.8)


def panel_d(cv):
    card(cv, 104.5, 30, 63.5, 43, "purple", "(d) Storage: write once per turn, token by token")
    ym = 56.4
    cv.text(106.0, 64.4, r"$\tilde{\mathbf{H}}_t$ of $S_t=X_t\,\|\,Y_t$", size=6.3, color=MUTED, ha="left")
    xs_op = [131.0, 150.5]
    for x, lab in zip(xs_op, (r"$\tilde{\mathbf{H}}_{t,i}$", r"$\tilde{\mathbf{H}}_{t,L_t}$")):
        cv.text(x, 64.4, lab, size=6.4, color=INK)
        cv.trap(x - 1.8, 58.6, 3.6, 2.8, "amber", narrow="bottom", lw=0.5)
        cv.line([(x, 62.6), (x, 61.4)], color=WR["stroke"], lw=0.5)
        cv.arrow([(x, 58.6), (x, ym + 1.5)], color=WR["stroke"], lw=0.5, head=0.9)
    cv.text(133.0, 60.0, r"$\mathbf{K},\mathbf{V},\boldsymbol{\beta},\boldsymbol{\omega},\boldsymbol{\lambda}$",
            size=6.3, color=WR["ink"], ha="left")
    mats = [(108.0, r"$\mathbf{M}_t$"), (120.6, r"$\tilde{\mathbf{M}}_{i-1}$"), (135.2, r"$\tilde{\mathbf{M}}_i$"),
            (155.6, r"$\tilde{\mathbf{M}}_{L_t}$")]
    for k, (x, lab) in enumerate(mats):
        cv.matrix(x, ym - 2.6, 5.2, 5.2, rows=4, cols=4, r="memory", seed=10 + k, lw=0.3)
        cv.text(x + 2.6, ym - 4.5, lab, size=6.4, color=MEM["ink"])
    cv.text(110.6, ym + 4.2, r"$\tilde{\mathbf{M}}_0$", size=6.4, color=MEM["ink"])
    for x in xs_op:
        cv.op(x, ym, "u", r="purple", d=3.0)
    cv.line([(113.2, ym), (114.6, ym)], color=WR["mark"])
    cv.text(116.6, ym, r"$\cdots$", size=7, color=MUTED)
    for x0, x1 in ((118.4, 120.6), (125.8, 129.5), (132.5, 135.2), (148.0, 149.0), (152.0, 155.6)):
        cv.arrow([(x0, ym), (x1, ym)], color=WR["mark"], head=1.0)
    cv.line([(140.4, ym), (142.0, ym)], color=WR["mark"])
    cv.text(144.4, ym, r"$\cdots$", size=7, color=MUTED)
    cv.arrow([(101.5, ym), (108.0, ym)], color=MEM["mark"], lw=1.0, head=1.3)
    # callout: one update u drawn on the state grid
    cx0, cy0, cw, chh = 106.3, 38.6, 54.6, 10.4
    cv.ax.add_patch(__import__("matplotlib.patches", fromlist=["FancyBboxPatch"]).FancyBboxPatch(
        (cx0, cy0), cw, chh, boxstyle="round,pad=0,rounding_size=1.2", fc="white", ec=WR["stroke"],
        lw=0.5, ls=(0, (2.5, 1.5)), zorder=3))
    for xx in (cx0, cx0 + cw):
        cv.line([(131.0, ym - 1.5), (xx, cy0 + chh)], color=WR["stroke"], lw=0.4, dashed=True, z=2)
    yc, g = 42.6, 4.6
    gx = [108.2, 119.6, 131.0, 155.2]
    cv.matrix(gx[0], yc, g, g, rows=4, cols=4, r="memory", seed=11, lw=0.3)
    cv.matrix(gx[1], yc, g, g, rows=4, cols=4, r="memory", seed=11, lw=0.3, fade=0.45)
    cv.matrix(gx[2], yc, g, g, rows=4, cols=4, r="memory", seed=11, lw=0.3, fade=0.45, band=("row", 1))
    cv.matrix(gx[3], yc, g, g, rows=4, cols=4, r="memory", seed=12, lw=0.3)
    for (x0, x1), (name, c) in zip(((112.8, 119.6), (124.2, 131.0)), (("forget", DC), ("erase", ER))):
        cv.arrow([(x0 + 0.4, yc + g / 2), (x1 - 0.2, yc + g / 2)], color=LINE, lw=0.55, head=0.95)
        cv.chip((x0 + x1) / 2, yc + g + 1.5, name, c, size=6.1, pad=0.6)
    cv.text(116.2, yc - 1.5, r"$\mathbf{D}_i$", size=6.4, color=DC["ink"])
    cv.text(127.6, yc - 1.5, r"$\mathbf{I}-\mathbf{U}_i^{\!\top}\mathbf{U}_i$", size=6.0, color=ER["ink"])
    cv.op(138.8, yc + g / 2, "+", d=2.4)
    cv.line([(135.6, yc + g / 2), (137.6, yc + g / 2)], color=LINE, lw=0.55)
    # write = outer product of U (row) and omega*V (column)
    cv.vec(141.6, yc, n=3, cell=1.5, r="purple", vertical=True, seed=4)
    cv.text(144.1, yc + 2.2, r"$\times$", size=6.5, color=WR["ink"])
    cv.vec(145.4, yc + 1.5, n=4, cell=1.5, r="purple", seed=5)
    cv.chip(146.0, yc + g + 1.5, "write", WR, size=6.1, pad=0.6)
    cv.text(146.0, yc - 1.5, r"$\mathbf{U}_i^{\!\top}(\boldsymbol{\omega}_i\odot\mathbf{V}_i)$", size=6.0, color=WR["ink"])
    cv.arrow([(151.6, yc + g / 2), (155.0, yc + g / 2)], color=LINE, lw=0.55, head=0.95)
    cv.text(157.5, yc - 1.5, r"$\tilde{\mathbf{M}}_i$", size=6.4, color=MEM["ink"])
    cv.text(110.5, yc - 1.5, r"$\tilde{\mathbf{M}}_{i-1}$", size=6.4, color=MEM["ink"])
    cv.rich(136.3, 35.2, [(r"$\mathbf{U}_i=\sqrt{\boldsymbol{\beta}_i}\odot\mathbf{K}_i,\quad$", ER["ink"]),
                          (r"$\mathbf{D}_i=\mathrm{Diag}(e^{\boldsymbol{\lambda}_i})$", DC["ink"])], size=6.4, ha="center")
    # write-back M_{t+1} to the pillar
    cv.arrow([(160.8, ym), (166.0, ym), (166.0, 32.0), (101.5, 32.0)], color=MEM["mark"], lw=1.0, head=1.5)
    cv.text(116.0, 33.3, r"$\mathbf{M}_{t+1}=\tilde{\mathbf{M}}_{L_t}$", size=6.4, color=MEM["ink"])


def panel_e(cv):
    card(cv, 2, 2, 166, 25, "neutral", r"(e) Parameters across interaction steps:  $\theta_t=\{\theta_b,\ \phi,\ \mathbf{M}_t\}$")
    rows = [(18.0, "snow", FZ, r"$\theta_b$", "backbone", "kept frozen"),
            (12.2, "lock", PHI, r"$\phi$", "hyper memory", r"$\tilde{\mathbf{W}}_{Q,K,V}$, gates: trained offline, fixed online"),
            (6.4, "cycle", MEM, r"$\mathbf{M}_t$", "local memory", "rewritten at every turn end")]
    for y, ic, c, sym, name, desc in rows:
        getattr(cv, f"icon_{ic}")(5.6, y, 2.8, color=c["mark"] if ic != "snow" else c["stroke"])
        cv.text(8.6, y, sym, size=7.2, color=c["ink"], ha="left")
        cv.text(13.6, y, name, size=6.6, color=c["ink"], weight="bold", ha="left")
        cv.text(31.0, y, desc, size=6.2, color=INK, ha="left")
    x0s = [76.0, 108.5, 141.0]
    heads = [("turn 1", r"$\mathbf{M}_1=\mathbf{0}$"), ("turn 2", r"$\mathbf{M}_2$"), ("turn 3", r"$\mathbf{M}_3$")]
    for k, (x0, (hd, ml)) in enumerate(zip(x0s, heads)):
        cv.text(x0 + 12.5, 19.6, hd, size=6.6, weight="bold", color=INK)
        cv.matrix(x0, 7.2, 4.6, 4.6, rows=4, cols=4, r="memory", seed=20 + k, lw=0.3, empty=(k == 0))
        cv.text(x0 + 2.3, 14.1, ml, size=6.2, color=MEM["ink"])
        cs = cv.tokens(x0 + 7.0, 8.2, 7, w=2.3, h=2.3, gap=0.45, fills=["neutral"] * 3 + [GEN] * 4)
        cv.text(x0 + 10.1, 5.6, r"$X$", size=6.0, color=MUTED)
        cv.text(x0 + 18.4, 5.6, r"$Y$ (generated)", size=6.1, color=MUTED)
        cv.arrow([(x0 + 4.6, 11.0), (x0 + 6.0, 11.0), (x0 + 6.0, 12.7), (cs[-1][0], 12.7), (cs[-1][0], 10.5)],
                 color=MEM["mark"], lw=0.55, head=0.9, dashed=True, radius=0.6)
        for cx_, _ in cs[:-1]:
            cv.line([(cx_, 12.7), (cx_, 10.5)], color=MEM["mark"], lw=0.45, dashed=True)
        cv.text(x0 + 15.5, 14.2, "read all tokens", size=6.0, color=MEM["ink"], style="italic")
        if k < 2:
            xe = x0s[k + 1]
            cv.arrow([(cs[-1][0] + 1.4, 9.35), (xe, 9.35)], color=WR["mark"], lw=0.9, head=1.3)
            cv.text((cs[-1][0] + 1.4 + xe) / 2, 7.4, "write", size=6.1, color=WR["ink"], style="italic")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="serif", size=7.0)
    src = panel_a(cv)
    dst = panel_b(cv)
    cv.zoom(src, dst, color=FZ["stroke"], fill=FZ["soft"], alpha=0.45)
    pillar(cv)
    panel_c(cv)
    panel_d(cv)
    panel_e(cv)
    print("\n".join(cv.save(os.path.join(a.out, "memt_fig4_architecture"))))


if __name__ == "__main__":
    main()
