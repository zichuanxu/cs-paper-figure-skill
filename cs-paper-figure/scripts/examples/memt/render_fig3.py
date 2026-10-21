"""Redesign of MemT-1.0 (arXiv 2610.26825v2) Figure 3: inference efficiency and storage.

All values are copied from the paper's Figure 3 (MemT-1.0-Nano):
  end-to-end latency (s; history preparation + 128-token response)
  storage overhead per trajectory (MiB); Full Context at 1M is reported only as "too large".
Ratios and growth factors are derived here and asserted below.

    python render_fig3.py --out <dir>
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from paperkit import Canvas, ROLE, INK, MUTED  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

LAT = {  # seconds
    "Temp-LoRA":     {"128K": 700.82, "256K": 1400.88},
    "Full Context":  {"128K": 30.07, "256K": 94.47},
    "MemT-1.0-Nano": {"128K": 16.19, "256K": 23.69},
}
STORE_MIB = {"Full Context": 5.061 * 1024, "Temp-LoRA": 172.5, "MemT-1.0-Nano": 40.00}  # 256K
UNIT = STORE_MIB["MemT-1.0-Nano"]                                                   # one waffle cell

HERO = ROLE["blue"]
COL = {"MemT-1.0-Nano": HERO["mark"], "Full Context": "#8E99A8", "Temp-LoRA": "#5E6875"}
W, H = 170, 66


def fmt(v):
    return f"{v:,.1f}" if v < 100 else f"{v:,.0f}"


def panel_latency(cv):
    cv.group(2, 2, 76, 62, "neutral", "(a) End-to-end latency", band=True, size=7.6, radius=2.0, lw=0.6,
             fill="white")
    cv.text(4.0, 54.6, "history preparation + 128-token response", size=6.2, color=MUTED, ha="left", style="italic")
    x0, x1, y0, hh = 21.0, 45.0, 11.5, 38.0
    lo, hi = 10, 3000

    def Y(v):
        return y0 + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * hh

    for v, lab in ((10, "10"), (30, None), (100, "100"), (300, None), (1000, "1,000"), (3000, None)):
        cv.ax.plot([15.5, 48.0], [Y(v)] * 2, color="#E6E9ED" if lab else "#F1F3F5", lw=0.5, zorder=1)
        if lab:
            cv.text(14.6, Y(v), lab, size=6.2, color="#5A626D", ha="right")
    cv.text(5.0, y0 + hh / 2, "seconds (log scale)", size=6.3, color=MUTED, rotation=90)
    for x, lab in ((x0, "128K"), (x1, "256K")):
        cv.ax.plot([x, x], [y0 - 0.6, Y(hi)], color="#EEF0F3", lw=0.5, zorder=1)
        cv.text(x, y0 - 2.6, lab, size=6.8, color=INK)
    for m in ("Temp-LoRA", "Full Context", "MemT-1.0-Nano"):
        a, b = LAT[m]["128K"], LAT[m]["256K"]
        hero = m == "MemT-1.0-Nano"
        c = COL[m]
        ink = HERO["ink"] if hero else c
        cv.ax.plot([x0, x1], [Y(a), Y(b)], color=c, lw=1.9 if hero else 1.0, zorder=5 if hero else 4,
                   solid_capstyle="round")
        for x, v in ((x0, a), (x1, b)):
            cv.ax.add_patch(Circle((x, Y(v)), 1.05 if hero else 0.8, fc=c, ec="white", lw=0.6, zorder=6))
        cv.text(x0 - 1.6, Y(a), fmt(a), size=6.2, color=ink, ha="right", weight="bold" if hero else "normal",
                bbox=dict(fc="white", ec="none", pad=0.4))
        cv.text(x1 + 1.6, Y(b), fmt(b), size=6.4, color=ink, ha="left", weight="bold" if hero else "normal")

    def mid(m):
        return Y(math.sqrt(LAT[m]["128K"] * LAT[m]["256K"]))
    cv.text((x0 + x1) / 2, mid("Temp-LoRA") + 2.6, "Temp-LoRA", size=6.6, color=COL["Temp-LoRA"])
    cv.text((x0 + x1) / 2, mid("Full Context") + 2.6, "Full Context", size=6.6, color=COL["Full Context"])
    cv.text((x0 + x1) / 2, mid("MemT-1.0-Nano") - 2.9, "MemT-1.0-Nano", size=6.8, color=HERO["ink"], weight="bold")
    # ratio brackets at 256K
    m, fc, tl = LAT["MemT-1.0-Nano"]["256K"], LAT["Full Context"]["256K"], LAT["Temp-LoRA"]["256K"]
    for xb, top, lab, sub in ((55.5, fc, f"{fc / m:.2f}×", "vs Full\nContext"),
                              (65.0, tl, f"{tl / m:.0f}×", "vs\nTemp-LoRA")):
        cv.line([(xb - 0.9, Y(m)), (xb, Y(m)), (xb, Y(top)), (xb - 0.9, Y(top))], color=HERO["mark"], lw=0.7,
                radius=0.3)
        ym = (Y(m) + Y(top)) / 2
        cv.text(xb + 0.9, ym + 1.4, lab, size=7.6, color=HERO["ink"], weight="bold", ha="left")
        cv.text(xb + 0.9, ym - 2.2, sub, size=5.6, color=MUTED, ha="left", linespacing=0.95)
    cv.text(61.0, Y(16.0), "speed-up at 256K", size=6.2, color=HERO["ink"], style="italic")
    g = {k: LAT[k]["256K"] / LAT[k]["128K"] for k in LAT}
    pct = {k: round(100 * (v - 1)) for k, v in g.items()}
    cv.rich(40.0, 5.0, [("128K→256K latency:  ", MUTED), (f"MemT +{pct['MemT-1.0-Nano']}%", HERO["ink"], "bold"),
                        ("  ·  Full Context ", MUTED), (f"+{pct['Full Context']}%", COL["Full Context"]),
                        ("  ·  Temp-LoRA ", MUTED), (f"+{pct['Temp-LoRA']}%", COL["Temp-LoRA"])], size=5.9,
            ha="center")
    return g


def waffle(cv, x, y, n, cols, cell, gap, fc, ec, z=5):
    """n (fractional) cells, filled row-major from the top-left; the last cell partially."""
    full, frac = int(n), n - int(n)
    rows = math.ceil(n / cols)
    p = cell + gap
    for k in range(full + (1 if frac > 1e-6 else 0)):
        r, c = divmod(k, cols)
        cx, cy = x + c * p, y + (rows - 1 - r) * p
        f = frac if k == full else 1.0
        cv.ax.add_patch(Rectangle((cx, cy), cell, cell, fc="white", ec=ec, lw=0.35, zorder=z))
        cv.ax.add_patch(Rectangle((cx, cy), cell * f, cell, fc=fc, ec="none", zorder=z + 0.1))
    return rows * p - gap, min(n, cols) * p - gap


def panel_storage(cv):
    cv.group(81, 2, 87, 62, "neutral", "(b) Persistent storage per trajectory", band=True, size=7.6,
             radius=2.0, lw=0.6, fill="white")
    cv.text(83.0, 54.6, "area to scale:", size=6.2, color=MUTED, ha="left", style="italic")
    cv.ax.add_patch(Rectangle((99.6, 53.5), 2.2, 2.2, fc=HERO["mark"], ec="none", zorder=6))
    cv.text(102.6, 54.6, "= 40 MiB (one MemT-1.0-Nano memory)", size=6.2, color=MUTED, ha="left", style="italic")
    n_fc = STORE_MIB["Full Context"] / UNIT
    n_tl = STORE_MIB["Temp-LoRA"] / UNIT
    cell, gap = 2.55, 0.42
    hh, ww = waffle(cv, 84.0, 9.5, n_fc, 13, cell, gap, "#C9D0DA", "#AEB7C3")
    cv.text(84.0, 9.5 + hh + 5.6, "Full Context", size=7.0, color=INK, weight="bold", ha="left")
    cv.text(84.0, 9.5 + hh + 2.4, f"{STORE_MIB['Full Context'] / 1024:.3f} GiB at 256K  ·  ≈{n_fc:.0f} MemT memories",
            size=6.2, color=MUTED, ha="left")
    cv.text(84.0 + ww + 0.8, 9.5 + hh + 5.6, "at 1M: too large", size=6.4, color="#A04A3A", ha="right",
            style="italic", weight="bold")
    xr = 125.5
    cv.text(xr, 47.0, "Temp-LoRA", size=7.0, color=INK, weight="bold", ha="left")
    cv.text(xr, 43.8, f"{STORE_MIB['Temp-LoRA']:.1f} MiB  ·  256K and 1M", size=6.2, color=MUTED, ha="left")
    waffle(cv, xr, 38.6, n_tl, 13, cell, gap, "#7E8896", "#5E6875")
    cv.text(xr, 33.0, "MemT-1.0-Nano", size=7.0, color=HERO["ink"], weight="bold", ha="left")
    cv.text(xr, 29.8, f"{STORE_MIB['MemT-1.0-Nano']:.2f} MiB  ·  256K and 1M", size=6.2, color=HERO["ink"], ha="left")
    cv.ax.add_patch(Rectangle((xr, 24.6), cell, cell, fc=HERO["mark"], ec=HERO["ink"], lw=0.35, zorder=6))
    cv.box(xr, 9.5, 40.0, 11.4, HERO, fill=HERO["fill"], stroke=HERO["stroke"], lw=0.6, radius=1.2)
    cv.rich(xr + 1.8, 18.2, [(f"{n_fc:.0f}×", HERO["ink"], "bold"), (" less than Full Context (256K)", INK)], size=6.6)
    cv.rich(xr + 1.8, 14.8, [(f"{n_tl:.1f}×", HERO["ink"], "bold"), (" less than Temp-LoRA", INK)], size=6.6)
    cv.text(xr + 1.8, 11.4, "fixed-size state: no growth with context", size=6.0, color=HERO["ink"],
            style="italic", ha="left")
    return n_fc, n_tl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    cv = Canvas(W, H, family="serif", size=7.0)
    g = panel_latency(cv)
    r_fc, r_tl = panel_storage(cv)
    # derived numbers stay tied to the copied inputs
    assert f"{LAT['Full Context']['256K'] / LAT['MemT-1.0-Nano']['256K']:.2f}" == "3.99"
    assert round(LAT["Temp-LoRA"]["256K"] / LAT["MemT-1.0-Nano"]["256K"]) == 59
    assert round(r_fc) == 130 and abs(r_tl - 4.31) < 0.01 and abs(g["MemT-1.0-Nano"] - 1.46) < 0.01
    print("\n".join(cv.save(os.path.join(a.out, "memt_fig3_efficiency"))))


if __name__ == "__main__":
    main()
