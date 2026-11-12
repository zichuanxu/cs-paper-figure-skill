#!/usr/bin/env python3
"""MemT-1.0 Figure 4 (model architecture), drawn with paperkit.

Source: MemT-1.0, arXiv:2610.26825v2, Figure 4 and Section 2 (Model Architecture), Appendix C (stable GDN-2).

Content kept from the source
  * LM stack: input S_{t,k} = X_t || Y_{t,<k} -> Embedding -> L Transformer blocks -> Norm -> LM Head -> y_{t,k}.
  * A selected block l: Pre-Attention -> (Original Attention || Memory Attention) -> A = A_ori + A_mem ->
    Post-Attention, with the backbone parts unchanged (frozen during memory training, Sec. 3).
  * theta_t = {theta_b, phi, M_t}: local memory M_t in R^{H_kv x d_k x d_v} (zero at a new trajectory, evolves
    online); hyper memory phi (trained offline, fixed online) = every projection drawn as an amber trapezoid:
    W~_Q, W~_K, W~_V, W_beta, W_omega, W_f, W_lambda, b_lambda, s, W_g/d, W_g/u.
  * Utilization, every token:  Q = L2Norm(H~ W~_Q),  R = Q M / sqrt(d_k),  G = H~ W_g/d W_g/u,
    A_mem = Concat_h[ RMSNorm(R) (.) SoftCapSiLU(G) ],  SoftCapSiLU(x) = tau tanh(SiLU(x)/tau), tau = 2.
  * Storage, at turn end, token by token:  K = L2Norm(H~ W~_K),  V = H~ W~_V,  beta = sigma(H~ W_beta),
    omega = sigma(H~ W_omega),  lambda = -exp(s) (.) Softplus(H~ W_f W_lambda + b_lambda),  U = sqrt(beta) (.) K,
    M~_i = [I - U^T U] D M~_{i-1} + U^T (omega (.) V),  D = Diag[exp(lambda)],  M~_0 = M_t,  M_{t+1} = M~_{L_t}.

Design
  * Claim to read in five seconds: the memory M is a state inside the forward pass; every token of a turn
    reads it, and the turn's hidden states rewrite it once at the turn end. Panel (b) says this on a time
    axis (state rail M_1 = 0 ... M_t -> M_{t+1}, read arrows under every token, one write per turn).
  * Plate: (a) where the memory sits, (b) when it is read and written, (c) how it is read, (d) how it is
    written; a one-line key underneath. One hue per meaning: grey = backbone, green = the state M, blue =
    read path, purple = write path, amber = hyper-memory parameters phi (owned in place, no inventory box).
  * The state is a drawn 4 x 5 grid (rows = key dim d_k, columns = value dim d_v; offset slabs = H_kv
    channels). Its cells are not a texture: one toy trajectory is pushed through the paper's update rule
    and the same matrices appear in (a), (b), (c) and (d). Panel (d) shows one token-level step on the
    grid itself: forget fades a row (D), erase clears the addressed row (I - U^T U), write adds the outer
    product U^T(omega (.) V). Cell shade = |value|; the numbers are illustrative, the rule is the paper's.
  * The read in (c) is drawn as the product it is: Q weights the rows of M, R is the resulting row.
  * Print size 178 x 117 mm. Text is 5.9 pt or larger, math is 6.5 pt or larger (subscripts >= 4.5 pt).
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import Canvas, ROLE, INK, MUTED  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
import matplotlib.colors as mcolors  # noqa: E402

STEM = "memt_fig4_architecture"
B, P, G, A, N = (ROLE[k] for k in ("blue", "purple", "memory", "amber", "neutral"))
GEN = dict(fill="#E3E6EB", soft="#BFC6D0", stroke="#6B7480", ink="#2F3640", mark="#5E6875")  # generated tokens
T, S, AN = 6.6, 6.2, 5.9  # body and math / small words / annotation, pt at print size (math never below 6.5)
SIG = r"$\sigma$"
DK, DV = 4, 5             # toy key / value dimensions of the drawn state
RAMP = {"memory": ["#F6FBF7", "#A9D6B7", "#2E8B57", "#1B5231"],   # |value| ramps: state, write-path operands
        "purple": ["#FAF7FE", "#C9B6EA", "#7A54C2", "#472A7C"],
        "blue": ["#F6F9FE", "#A9C7EC", "#2F6FC0", "#1F4E8C"]}


# ---------------------------------------------------------------- toy trajectory under the paper's update rule
def sgdn2_step(M, k, beta, lam, omega, v):
    """One stable GDN-2 token update (Sec. 2.2.2): M_i = [I - U^T U] D M_{i-1} + U^T (omega . V)."""
    u = np.sqrt(beta) * k
    D = np.diag(np.exp(lam))
    E = np.eye(DK) - np.outer(u, u)
    Mf = D @ M
    Me = E @ Mf
    Wr = np.outer(u, omega * v)
    return dict(u=u, D=D, E=E, Mf=Mf, Me=Me, W=Wr, ov=omega * v, M=Me + Wr)


def toy_token(rng, row, forget=None):
    """Key near one address (row), strong erase gate there, optional strong forget on another row."""
    k = np.full(DK, 0.07)
    k[row] = 1.0
    k /= np.linalg.norm(k)                      # K is L2-normalised
    beta = np.full(DK, 0.45)
    beta[row] = 0.96                            # sigma(.) in (0, 1)
    lam = np.full(DK, -0.02)                    # lambda <= 0, so D = exp(lambda) in (0, 1]
    if forget is not None:
        lam[forget] = -1.2
    omega = rng.uniform(0.6, 1.0, DV)
    v = rng.uniform(0.45, 1.0, DV) * rng.choice([1.0, 1.0, 1.0, 0.25], DV)
    return k, beta, lam, omega, v


def toy_trajectory():
    rng = np.random.default_rng(11)
    M1 = np.zeros((DK, DV))                     # new trajectory: M = 0
    M = M1
    for row in (0, 2):                          # earlier turns
        M = sgdn2_step(M, *toy_token(rng, row))["M"]
    Mt = M
    shown = None
    for i, (row, forget) in enumerate([(3, None), (0, 2), (1, None), (2, None)], start=1):  # turn t
        st = sgdn2_step(M, *toy_token(rng, row, forget))
        if i == 2:
            shown = dict(st, prev=M)            # the step drawn in panel (d)
        M = st["M"]
    # the drawn step must be the paper's rule, and the symmetrised erase must not expand the state
    s = shown
    assert np.allclose(s["M"], (np.eye(DK) - np.outer(s["u"], s["u"])) @ s["D"] @ s["prev"] + np.outer(s["u"], s["ov"]))
    assert np.linalg.norm(s["E"], 2) <= 1 + 1e-9 and not M1.any()
    q = np.array([0.2, 0.12, 0.95, 0.15])
    q /= np.linalg.norm(q)                      # Q is L2-normalised
    return dict(M1=M1, Mt=Mt, Mt1=M, step=shown, q=q, R=q @ Mt / np.sqrt(DK))


def shade(vals, vmax=1.0):
    return np.clip(np.abs(np.asarray(vals, float)) / vmax, 0, 1)


def strip(cv, x, y, vals, cw, ch, r, vertical=False, z=7):
    """Vector as a strip of cells shaded by |value| (first element on top / left)."""
    c = ROLE[r] if isinstance(r, str) else r
    cm = mcolors.LinearSegmentedColormap.from_list("s", RAMP.get(r, [c["fill"], c["soft"], c["mark"]]))
    n = len(vals)
    w, h = (cw, ch * n) if vertical else (cw * n, ch)
    cv.solids.append((x, y, w, h, "strip", None))
    for i, v in enumerate(shade(vals)):
        xx, yy = (x, y + (n - 1 - i) * ch) if vertical else (x + i * cw, y)
        cv.ax.add_patch(Rectangle((xx, yy), cw, ch, fc=cm(v), ec=c["stroke"], lw=0.3, zorder=z))
    cv.ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=c["ink"], lw=0.55, zorder=z + 0.1))
    return (x, y, w, h)


def grid(cv, x, y, vals, cell, r="memory", depth=1, **kw):
    v = np.asarray(vals)
    cm = mcolors.LinearSegmentedColormap.from_list("g", RAMP[r])
    return cv.matrix(x, y, cell * v.shape[1], cell * v.shape[0], rows=v.shape[0], cols=v.shape[1], depth=depth,
                     r=r, values=shade(vals), cmap=cm, dx=kw.pop("dx", 0.9), dy=kw.pop("dy", 0.9), **kw)


def key_strip(cv, x, y, w, items, h=6.0):
    """One-row glyph key: items = [(glyph width, draw(cx, cy), label)], spread evenly."""
    cv.box(x, y, w, h, "neutral", fill="white", dashed=True, radius=1.6, container=True, z=1)
    widths = [gw + 1.0 + cv.text_width(lab, S) for gw, _, lab in items]
    gap = (w - 4.0 - sum(widths)) / (len(items) - 1)
    assert gap >= 1.5, f"key does not fit in one row (gap {gap:.1f} mm)"
    xx = x + 2.0
    for (gw, draw, lab), iw in zip(items, widths):
        draw(xx + gw / 2, y + h / 2)
        cv.text(xx + gw + 1.0, y + h / 2, lab, size=S, ha="left")
        xx += iw + gap


def draw(out):
    toy = toy_trajectory()
    W, H = 178.0, 117.0
    cv = Canvas(W, H, size=T)
    blue, purp, green = B["mark"], P["mark"], G["mark"]
    it = dict(style="italic", size=AN)

    # =================================================================== (a) where: stack and block l
    ay, ah = 68.4, 45.5
    cv.section(1, ay, 84, ah, "neutral", "Native memory in the model", letter="a")
    cx = 17.0
    cv.text(cx, 70.7, r"$S_{t,k}=X_t\,\Vert\,Y_{t,<k}$", size=6.5)
    cv.tokens(cx - 8.2, 72.4, 6, w=2.4, h=2.4, gap=0.4, fills=["neutral"] * 3 + [GEN] * 3)
    cv.arrow([(cx, 75.0), (cx, 76.6)], head=1.1)
    cv.box(9, 76.6, 16, 3.4, "neutral", "Embedding", size=S, fill=N["soft"], weight="normal")
    cv.arrow([(cx, 80.0), (cx, 81.6)], head=1.1)
    cv.box(8, 81.6, 18, 15.0, "neutral", fill="white", radius=1.4, container=True)
    cv.box(9, 82.4, 16, 3.8, "neutral", "Block $l{-}1$", size=S, fill=N["soft"], weight="normal")
    cv.box(9, 87.2, 16, 3.8, "neutral", fill=N["soft"], stroke=N["ink"], lw=0.9)
    cv.text(15.3, 89.1, "Block $l$", size=S, weight="bold", color=N["ink"])
    grid(cv, 20.6, 87.9, toy["Mt"], 0.6, lw=0.25)
    cv.box(9, 92.0, 16, 3.8, "neutral", "Block $l{+}1$", size=S, fill=N["soft"], weight="normal")
    cv.brace(7.4, 82.0, 96.2, "left")
    cv.text(3.9, 89.1, r"$\times L$", size=S)
    cv.arrow([(cx, 96.6), (cx, 98.2)], head=1.1)
    cv.box(9, 98.2, 16, 3.2, "neutral", "Norm", size=S, fill=N["soft"], weight="normal")
    cv.arrow([(cx, 101.4), (cx, 102.8)], head=1.1)
    cv.box(9, 102.8, 16, 3.2, "neutral", "LM Head", size=S, fill=N["soft"], weight="normal")
    cv.arrow([(cx, 106.0), (cx, 107.6)], head=1.1)
    cv.text(cx, 109.2, r"$y_{t,k}$", size=T)

    card = (31, 69.8, 51, 41.4)
    cv.zoom((9, 87.2, 16, 3.8), card, fill=N["soft"], alpha=0.5)
    cv.box(*card, "neutral", fill="white", radius=2.0, container=True, lw=0.7, z=2.5)
    cv.text(33.0, 109.3, "Block $l$", size=S, weight="bold", ha="left", color=N["ink"])
    xs = 51.0
    cv.text(xs, 72.2, r"$\mathbf{H}^{(l-1)}$", size=T)
    cv.arrow([(xs, 73.8), (xs, 76.2)], head=1.1)
    cv.dot(xs, 74.6, color="#9AA1AB", d=0.8)
    cv.arrow([(xs, 74.6), (33.0, 74.6), (33.0, 104.1), (41.0, 104.1)], color="#9AA1AB", lw=0.55, head=1.2)
    cv.box(41, 76.2, 20, 3.8, "neutral", "Pre-Attention", size=S, fill=N["soft"], weight="normal")
    cv.icon_snow(59.2, 78.1, 2.0, color=N["stroke"])
    cv.line([(xs, 80.0), (xs, 83.6)])
    cv.text(xs - 1.0, 81.9, r"$\tilde{\mathbf{H}}^{(l)}$", size=T, ha="right")
    cv.arrow([(xs, 83.6), (42.5, 83.6), (42.5, 86.8)])
    cv.arrow([(xs, 83.6), (59.2, 83.6), (59.2, 86.8)])
    cv.dot(xs, 83.6, d=0.8)
    cv.box(34.4, 84.8, 46.6, 15.6, "neutral", fill="none", stroke=N["ink"], dashed=True, radius=1.6,
           container=True, lw=0.6, z=3)
    cv.box(35.5, 86.8, 14, 7.8, "neutral", "Original\nAttention", size=S, fill=N["soft"], weight="normal")
    cv.icon_snow(47.9, 93.0, 2.0, color=N["stroke"])
    cv.box(52.5, 86.8, 13.4, 7.8, "blue", "Memory\nAttention", size=S, fill=B["soft"], lw=0.95, shadow=True)
    cv.arrow([(42.5, 94.6), (42.5, 98.0), (xs - 1.4, 98.0)])
    cv.arrow([(59.2, 94.6), (59.2, 98.0), (xs + 1.4, 98.0)], color=blue, lw=0.9)
    cv.op(xs, 98.0, "+", d=2.8)
    cv.text(41.7, 96.5, r"$\mathbf{A}_{\mathrm{ori}}$", size=T, ha="right", color=N["ink"])
    cv.text(60.1, 96.5, r"$\mathbf{A}_{\mathrm{mem}}$", size=T, ha="left", color=B["ink"])
    cv.arrow([(xs, 99.4), (xs, 102.2)], head=1.1)
    cv.box(41, 102.2, 20, 3.8, "neutral", "Post-Attention", size=S, fill=N["soft"], weight="normal")
    cv.icon_snow(59.2, 104.1, 2.0, color=N["stroke"])
    cv.arrow([(xs, 106.0), (xs, 107.5)], head=1.1)
    cv.text(xs, 109.2, r"$\mathbf{H}^{(l)}$", size=T)
    tw = cv.text_width("Native memory block", 6.0, "bold") + 2.4
    cv.tab(80.0 - tw, 99.1, tw, 2.6, "neutral", "Native memory block", size=6.0)
    # the state beside the block: read by memory attention, rewritten from the turn's hidden states
    grid(cv, 71.8, 88.0, toy["Mt"], 1.4, depth=2, dx=0.8, dy=0.8)
    cv.text(75.7, 97.0, r"$\mathbf{M}^{(l)}_t$", size=T, color=G["ink"])
    cv.arrow([(71.8, 90.8), (65.9, 90.8)], color=blue, lw=0.9)
    cv.text(68.85, 92.6, "read", color=B["ink"], **it)
    cv.dot(xs, 81.3, color=purp, d=0.9)
    cv.arrow([(xs, 81.3), (75.3, 81.3), (75.3, 88.0)], color=purp, lw=0.9)
    cv.text(70.8, 79.5, "write at turn end", color=P["ink"], **it)

    # =================================================================== (b) when: the state across turns
    cv.section(88, ay, 89, ah, "memory", "Memory across turns", letter="b")
    cv.phase_bar(69.6, [(89.4, 111.0, "neutral", "new trajectory"), (111.0, 147.0, "neutral", "turn $t$"),
                        (147.0, 175.6, "neutral", "turn $t{+}1$")], h=3.4, size=S)
    my, mc = 77.0, 2.2                                    # matrix bottom, cell
    ry, mtop = my + 2 * mc, my + 4 * mc + 1.8             # rail height, top of the back slab
    grid(cv, 95.0, my, toy["M1"], mc, depth=3, empty=True)
    grid(cv, 112.5, my, toy["Mt"], mc, depth=3)
    grid(cv, 148.5, my, toy["Mt1"], mc, depth=3)
    cv.text(100.5, 74.9, r"$\mathbf{M}_1=\mathbf{0}$", size=T, color=G["ink"])
    cv.text(118.0, 74.9, r"$\mathbf{M}_t$", size=T, color=G["ink"])
    cv.text(154.0, 74.9, r"$\mathbf{M}_{t+1}$", size=T, color=G["ink"])
    cv.text(110.2, ry, r"$\cdots$", size=8, color=G["ink"])
    cv.arrow([(125.3, ry), (135.2, ry)], color=green, lw=1.0)
    cv.box(135.2, ry - 4.6, 10, 9.2, "purple", "Stable\nGDN-2\nupdate", size=S, fill=P["soft"], lw=0.9)
    cv.arrow([(145.2, ry), (148.5, ry)], color=green, lw=1.0)
    cv.arrow([(161.3, ry), (168.6, ry)], color=green, lw=1.0)
    cv.text(172.0, ry, r"$\cdots$", size=8, color=G["ink"])
    for k, (tx, lab, note) in enumerate([(112.0, "t", "read at every token"), (149.6, "t{+}1", None)]):
        cs = cv.tokens(tx, 99.4, 8, w=2.4, h=2.6, gap=0.8, fills=["neutral"] * 4 + [GEN] * 4)
        x0, x1 = cs[0][0] - 1.8, cs[-1][0] + 1.8
        cv.box(x0, 94.0, x1 - x0, 4.4, "neutral", fill=N["soft"])
        cv.icon_snow(x0 + 2.2, 96.2, 2.2, color=N["stroke"])
        cv.text(x0 + 3.8, 96.2, r"$\theta_b$", size=T, ha="left", color=N["ink"])
        cv.icon_lock(x0 + 9.4, 96.2, 2.2, color=A["mark"])
        cv.text(x0 + 11.0, 96.2, r"$\phi$", size=T, ha="left", color=A["ink"])
        cv.text(x1 - 1.0, 96.2, "fixed online", ha="right", color=MUTED, **it)
        cv.text((cs[0][0] + cs[3][0]) / 2, 104.0, f"$X_{{{lab}}}$", size=T)
        cv.text((cs[4][0] + cs[7][0]) / 2, 104.0, f"$Y_{{{lab}}}$", size=T)
        cv.line([(cs[0][0], 91.0), (cs[-1][0], 91.0)], color=blue, lw=0.9)
        cv.line([(cs[1][0], mtop), (cs[1][0], 91.0)], color=blue, lw=0.9)
        for c in cs:
            cv.arrow([(c[0], 91.0), (c[0], 94.0)], color=blue, lw=0.8, head=1.1)
        if note:
            cv.text(cs[1][0] + 2.0, 89.4, note, ha="left", color=B["ink"], **it)
            cv.arrow([(x0, 105.8), (x0, 106.8), (140.2, 106.8), (140.2, ry + 4.6)], color=purp, lw=0.9)
            cv.line([(x1, 105.8), (x1, 106.8)], color=purp, lw=0.9)
            cv.text((x0 + x1) / 2, 108.9, r"write at turn end ($L_t$ tokens)", color=P["ink"], style="italic", size=6.5)
    # theta_t = {theta_b, phi, M_t}
    cv.box(90.2, 90.8, 19.6, 19.6, "neutral", fill="white", radius=1.4)
    cv.tab(96.8, 109.0, 6.4, 2.8, "neutral", r"$\theta_t$", size=6.5)
    for yy, icon, col, sym, name, status in [
            (105.4, cv.icon_snow, N["stroke"], r"$\theta_b$", "backbone", "frozen"),
            (99.8, cv.icon_lock, A["mark"], r"$\phi$", "hyper memory", "fixed online"),
            (94.2, cv.icon_cycle, green, r"$\mathbf{M}_t$", "local memory", "evolves online")]:
        icon(93.0, yy + 1.2, 2.4, color=col)
        cv.text(93.0, yy - 1.5, sym, size=6.5, color=INK)
        cv.text(96.0, yy + 1.1, name, size=S, ha="left", color=INK)
        cv.text(96.0, yy - 1.3, status, ha="left", color=MUTED, **it)

    # =================================================================== (c) how it is read
    dy0, dh = 9.6, 54.0
    cv.section(1, dy0, 84, dh, "blue", "Memory utilization: read at every token", letter="c")
    yq, yr, yg = 46.4, 34.1, 19.5
    strip(cv, 4.6, 27.5, [0.5, 0.9, 0.3, 0.7, 0.45], 2.2, 2.2, "neutral", vertical=True)
    cv.text(5.7, 40.9, r"$\tilde{\mathbf{H}}^{(l)}_t$", size=T)
    cv.line([(6.8, 33.0), (9.6, 33.0)])
    cv.dot(9.6, 33.0, d=0.8)
    cv.arrow([(9.6, 33.0), (9.6, yq), (12.0, yq)])
    cv.arrow([(9.6, 33.0), (9.6, yg), (12.0, yg)])
    cv.trap(12, yq - 4, 10, 8, "amber", narrow="right", title=r"$\tilde{\mathbf{W}}_{Q,h}$", size=T)
    cv.text(17.0, 52.3, "query", color=B["ink"], **it)
    cx0, cw = cv.chip(29.4, yq, "L2Norm", "blue", size=AN)
    cv.arrow([(22.0, yq), (cx0, yq)], color=blue, lw=0.9)
    cv.arrow([(cx0 + cw, yq), (36.8, yq)], color=blue, lw=0.9)
    mc = 3.4
    strip(cv, 36.8, 39.6, toy["q"], 2.4, mc, "blue", vertical=True)
    grid(cv, 41.0, 39.6, toy["Mt"], mc, depth=3, dx=1.0, dy=1.0, lw=0.45)
    cv.text(38.0, 55.4, r"$\mathbf{Q}_{t,h}$", size=T, color=B["ink"])
    cv.text(51.5, 58.8, r"$\mathbf{M}^{(l)}_t$:  $H_{kv}\times d_k\times d_v$", size=T, color=G["ink"])
    cv.text(61.2, yq, "$d_k$", size=6.5, color=MUTED, ha="left")
    cv.arrow([(49.5, 39.6), (49.5, yr + 1.2)], color=blue, lw=0.9)
    strip(cv, 41.0, yr - 1.2, toy["R"], mc, 2.4, "blue")
    cv.text(49.5, yr - 3.1, "$d_v$", size=6.5, color=MUTED)
    cv.rich(39.4, yr, [(r"$\mathbf{R}_{t,h}=\mathbf{Q}_{t,h}\,$", B["ink"]), (r"$\mathbf{M}_{t,h}$", G["ink"]),
                       (r"$/\sqrt{d_k}$", INK)], size=T, ha="right")
    cx0, cw = cv.chip(66.2, yr, "RMSNorm", "blue", size=AN)
    cv.arrow([(58.0, yr), (cx0, yr)], color=blue, lw=0.9)
    cv.arrow([(cx0 + cw, yr), (74.6, yr)], color=blue, lw=0.9)
    cv.op(76.0, yr, ".", r="blue", d=2.8)
    cv.arrow([(76.0, yr + 1.4), (76.0, 41.1)], color=blue, lw=0.9)
    cv.op(76.0, 42.8, "C", r="blue", d=3.4)
    cv.text(73.7, 42.8, "$H_q$ channels", ha="right", color=B["ink"], style="italic", size=6.5)
    cv.arrow([(76.0, 44.5), (76.0, 48.2)], color=blue, lw=0.9)
    cv.text(76.0, 50.0, r"$\mathbf{A}_{\mathrm{mem},t}$", size=T, color=B["ink"])
    cv.text(76.0, 53.2, r"to $\oplus$ in (a)", color=MUTED, **it)
    # output gate: low-rank projection, soft-capped
    cv.trap(12, yg - 4, 10, 8, "amber", narrow="right", title=r"$\mathbf{W}_{g/d}$", size=T)
    cv.trap(23.5, yg - 4, 10, 8, "amber", narrow="left", title=r"$\mathbf{W}_{g/u,h}$", size=T)
    cv.line([(22.0, yg), (23.5, yg)], color=blue, lw=0.9)
    cv.text(22.75, 25.4, "output gate", color=B["ink"], **it)
    cv.arrow([(33.5, yg), (37.0, yg)], color=blue, lw=0.9)
    strip(cv, 37.0, yg - 0.9, [0.3, 0.8, 0.55, 0.2, 0.7], 1.8, 1.8, "blue")
    cv.text(41.5, 22.7, r"$\mathbf{G}_{t,h}$", size=T, color=B["ink"])
    cv.arrow([(46.0, yg), (50.0, yg)], color=blue, lw=0.9)
    cv.box(50.0, 13.0, 19.5, 13.0, "blue", fill="white")
    cv.text(59.75, 23.7, "SoftCapSiLU", size=S, weight="bold", color=B["ink"])
    xv = np.linspace(-4, 7, 120)
    tau = 2.0
    fv = tau * np.tanh(xv / (1 + np.exp(-xv)) / tau)          # tau tanh(SiLU(x) / tau)
    px = lambda v: 52.5 + (v + 4) / 11 * 14.5                 # noqa: E731
    py = lambda v: 15.3 + (v + 0.4) / 2.6 * 5.8               # noqa: E731
    cv.ax.plot([px(-4), px(7)], [py(0)] * 2, color="#9AA0A8", lw=0.5, zorder=8)
    cv.ax.plot([px(0)] * 2, [py(-0.4), py(2.2)], color="#9AA0A8", lw=0.5, zorder=8)
    cv.ax.plot([px(-4), px(7)], [py(tau)] * 2, color=B["stroke"], lw=0.5, ls=(0, (2, 1.5)), zorder=8)
    cv.ax.plot(px(xv), py(fv), color=blue, lw=1.1, zorder=9)
    cv.text(px(-3.6), py(tau) - 1.2, r"$\tau$", size=6.5, color=B["ink"], ha="left")
    cv.arrow([(69.5, yg), (76.0, yg), (76.0, yr - 1.4)], color=blue, lw=0.9)

    # =================================================================== (d) how it is written
    cv.section(88, dy0, 89, dh, "purple", "Memory storage: written at turn end", letter="d")
    st = toy["step"]
    mx, ym, cell = [100.0, 121.5, 143.0, 164.5], 48.5, 2.2
    yo = ym + 2 * cell
    for x, vals in zip(mx, [st["prev"], st["Mf"], st["Me"], st["M"]]):
        grid(cv, x, ym, vals, cell, lw=0.45)
    ox = [(mx[i] + 5 * cell + mx[i + 1]) / 2 for i in range(3)]
    for i, (o, sym, name) in enumerate(zip(ox, "xx+", ["forget", "erase", "write"])):
        cv.arrow([(mx[i] + 5 * cell, yo), (o - 1.4, yo)], color=green, lw=0.9, head=1.2)
        cv.arrow([(o + 1.4, yo), (mx[i + 1], yo)], color=green, lw=0.9, head=1.2)
        cv.op(o, yo, sym, r="purple", d=2.8)
        tw = cv.text_width(name, S, "bold")
        cv.badge(o - tw / 2 - 0.6, 59.6, i + 1, "purple", d=3.0)
        cv.text(o - tw / 2 + 1.8, 59.6, name, size=S, weight="bold", ha="left", color=P["ink"])
    cv.text(mx[0] + 5.5, 59.7, r"$\tilde{\mathbf{M}}_{t,i-1}$", size=T, color=G["ink"])
    cv.text(mx[3] + 5.5, 59.7, r"$\tilde{\mathbf{M}}_{t,i}$", size=T, color=G["ink"])
    cv.text(mx[0] + 5.5, 46.3, r"$=\mathbf{M}_t$ at $i=1$", size=6.5, color=MUTED)
    cv.text(175.6, 46.3, r"$=\mathbf{M}_{t+1}$ at $i=L_t$", size=6.5, color=MUTED, ha="right")
    # operands, each under its operator
    yb, c2 = 34.0, 1.5
    grid(cv, ox[0] - 3.0, yb, st["D"], c2, r="purple")
    grid(cv, ox[1] - 3.0, yb, st["E"], c2, r="purple")
    grid(cv, ox[2] - 3.75, yb, st["W"], c2, r="purple")
    strip(cv, ox[2] - 6.35, yb, st["u"], c2, c2, "purple", vertical=True)
    strip(cv, ox[2] - 3.75, yb - 2.6, st["ov"], c2, c2, "purple")
    for o, lab in zip(ox, [r"$\mathbf{D}=\mathrm{Diag}[e^{\boldsymbol{\lambda}}]$",
                           r"$\mathbf{I}-\mathbf{U}^{\!\top}\mathbf{U}$",
                           r"$\mathbf{U}^{\!\top}(\boldsymbol{\omega}\odot\mathbf{V})$"]):
        cv.arrow([(o, yb + 6.0), (o, yo - 1.4)], color=purp, lw=0.9)
        cv.text(o + 1.2, 42.9, lab, size=T, ha="left", color=P["ink"])
    # projections (phi) of the token's hidden state
    ybus, yt = 13.0, 16.0
    cs = cv.tokens(90.6, 30.0, 8, w=1.9, h=2.2, gap=0.4, fills=["neutral", "purple"] + ["neutral"] * 2 + [GEN] * 4)
    cv.text(99.6, 34.3, r"turn $t$,  $i=1,\dots,L_t$", color=P["ink"], style="italic", size=6.5)
    xi = cs[1][0]
    cv.arrow([(xi, 30.0), (xi, 19.9)], color=purp, lw=0.9)
    cv.text(xi + 1.0, 25.0, "token $i$", ha="left", color=P["ink"], **it)
    cv.text(xi, 18.0, r"$\tilde{\mathbf{H}}^{(l)}_{t,i}$", size=T)
    xk, xb, xv_, xw = ox[1] - 4.75, ox[1] + 4.75, ox[2] - 4.75, ox[2] + 4.75
    cv.line([(xi, 16.2), (xi, ybus), (xw, ybus), (xw, yt - 1.4)], color=purp, lw=0.9)
    for x in (ox[0], xk, xb, xv_, xw):
        cv.arrow([(x, ybus), (x, yt)], color=purp, lw=0.9, head=1.1)
        if x != xw:
            cv.dot(x, ybus, color=purp, d=0.8)
    cv.trap(ox[0] - 5.0, yt, 10, 4.2, "amber", narrow="top", title=r"$\mathbf{W}_f$", size=6.5)
    cv.trap(ox[0] - 5.75, yt + 5.0, 11.5, 4.2, "amber", narrow="bottom", title=r"$\mathbf{W}_\lambda,\mathbf{b}_\lambda$",
            size=6.5)
    cv.line([(ox[0], yt + 4.2), (ox[0], yt + 5.0)], color=purp, lw=0.9)
    cv.chip(ox[0], 28.2, r"$-e^{\mathbf{s}}\odot\mathrm{Softplus}$", "purple", size=6.5, h=3.3)
    cv.line([(ox[0], yt + 9.2), (ox[0], 26.55)], color=purp, lw=0.9)
    cv.arrow([(ox[0], 29.85), (ox[0], yb)], color=purp, lw=0.9, head=1.2)
    cv.text(ox[0] + 1.0, 31.9, r"$\boldsymbol{\lambda}$", size=T, ha="left", color=P["ink"])
    for x, lab in [(xk, r"$\tilde{\mathbf{W}}_K$"), (xb, r"$\mathbf{W}_\beta$"), (xv_, r"$\tilde{\mathbf{W}}_V$"),
                   (xw, r"$\mathbf{W}_\omega$")]:
        cv.trap(x - 4.25, yt, 8.5, 5.0, "amber", narrow="top", title=lab, size=6.5)
    ys = yt + 7.8                                             # nonlinearity row
    cx0, cw = cv.chip(xk, ys, "L2Norm", "purple", size=AN)
    cv.line([(xk, yt + 5.0), (xk, ys - 1.62)], color=purp, lw=0.9)
    cv.op(xb, ys, SIG, r="purple", d=3.4)
    cv.line([(xb, yt + 5.0), (xb, ys - 1.7)], color=purp, lw=0.9)
    yu = 29.0
    cv.arrow([(xk, ys + 1.62), (xk, yu), (ox[1] - 1.4, yu)], color=purp, lw=0.9, head=1.2)
    cv.arrow([(xb, ys + 1.7), (xb, yu), (ox[1] + 1.4, yu)], color=purp, lw=0.9, head=1.2)
    cv.op(ox[1], yu, ".", r="purple", d=2.8)
    cv.text(xk - 0.9, 27.6, r"$\mathbf{K}$", size=T, ha="right", color=P["ink"])
    cv.text(xb + 0.9, 27.6, r"$\sqrt{\boldsymbol{\beta}}$", size=T, ha="left", color=P["ink"])
    cv.arrow([(ox[1], yu + 1.4), (ox[1], yb)], color=purp, lw=0.9, head=1.2)
    cv.dot(ox[1], 32.0, color=purp, d=0.8)
    cv.arrow([(ox[1], 32.0), (ox[2] - 8.8, 32.0), (ox[2] - 8.8, 37.0), (ox[2] - 6.35, 37.0)], color=purp, lw=0.9,
             head=1.2)
    cv.text(ox[1] + 6.8, 33.6, r"$\mathbf{U}$", size=T, color=P["ink"])
    yv = 27.6
    cv.arrow([(xv_, yt + 5.0), (xv_, yv), (ox[2] - 1.4, yv)], color=purp, lw=0.9, head=1.2)
    cv.op(xw, 23.3, SIG, r="purple", d=3.4)
    cv.line([(xw, yt + 5.0), (xw, 21.6)], color=purp, lw=0.9)
    cv.arrow([(xw, 25.0), (xw, yv), (ox[2] + 1.4, yv)], color=purp, lw=0.9, head=1.2)
    cv.op(ox[2], yv, ".", r="purple", d=2.8)
    cv.arrow([(ox[2], yv + 1.4), (ox[2], yb - 2.6)], color=purp, lw=0.9, head=1.2)
    cv.text(xv_ - 0.9, 24.2, r"$\mathbf{V}$", size=T, ha="right", color=P["ink"])
    cv.text(xw + 1.2, 27.4, r"$\boldsymbol{\omega}$", size=T, ha="left", color=P["ink"])

    # =================================================================== key
    key_strip(cv, 1, 1.0, 176, [
        (4.6, lambda x, y: cv.trap(x - 2.3, y - 1.4, 4.6, 2.8, "amber", narrow="right", z=11),
         r"learned projection in $\phi$ (trained offline)"),
        (2.8, lambda x, y: cv.op(x, y, "+", d=2.6, z=11), "add"),
        (2.8, lambda x, y: cv.op(x, y, ".", d=2.6, z=11), "elementwise product"),
        (2.8, lambda x, y: cv.op(x, y, "x", d=2.6, z=11), "matrix product"),
        (3.4, lambda x, y: cv.op(x, y, "C", d=3.4, z=11), "concatenate channels"),
        (3.4, lambda x, y: cv.op(x, y, SIG, d=3.4, z=11), "sigmoid"),
        (4.5, lambda x, y: strip(cv, x - 2.25, y - 0.75, [0.1, 0.5, 0.95], 1.5, 1.5, "memory", z=11),
         "cell shade = |value|, toy example"),
    ])

    small = sorted({(round(t.get_fontsize(), 2), t.get_text()) for t in cv.ax.texts if t.get_fontsize() < 5.8})
    assert not small, small
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    assert not cv.wire_crossings(), cv.wire_crossings()
    return cv.save(os.path.join(out, STEM))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=".")
    print("\n".join(draw(ap.parse_args().out)))
