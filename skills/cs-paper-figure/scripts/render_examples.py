"""Render four original figure recipes from explicitly synthetic source values.

Run: python render_examples.py --out /path/to/output
Only numpy and matplotlib are required. No paper figures or measurements are used.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path as MplPath
import numpy as np

from figure_style import PALETTE, export_figure, make_figure, style_context, validate_intervals

SEED = 1701


def footer(fig, text="ILLUSTRATIVE SYNTHETIC DATA"):
    fig.text(0.99, 0.018, text, ha="right", va="bottom", fontsize=7,
             color=PALETTE["reference"])


def save(fig, out, name, data, caption, seed=SEED):
    source = out / (name + ".data.json")
    source.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    paths = export_figure(fig, out / name,
                         source_files=(source, Path(__file__), Path(__file__).with_name("figure_style.py")),
                         metadata={"synthetic": True, "seed": seed, "caption": caption})
    plt.close(fig)
    return paths


def curves(out):
    rng = np.random.default_rng(SEED)
    budget = np.array([1, 2, 4, 8, 16])
    means = {"Baseline": np.array([49, 57, 62, 66, 67]),
             "Memory": np.array([50, 62, 72, 79, 82])}
    compute = {"Baseline": np.array([1.0, 1.6, 2.7, 4.7, 8.5]),
               "Memory": np.array([1.2, 1.9, 3.0, 4.9, 8.6])}
    samples = {key: rng.normal(mean[:, None], 2.3, size=(5, 8)) for key, mean in means.items()}
    fig, axes = make_figure(178, 72, ncols=2)
    fig.get_layout_engine().set(rect=(0, 0.09, 1, 0.91))
    for key, role, marker in [("Baseline", "reference", "s"), ("Memory", "focus", "o")]:
        mean = samples[key].mean(axis=1)
        spread = samples[key].std(axis=1, ddof=1)
        axes[0].plot(budget, mean, color=PALETTE[role], marker=marker, label=key)
        axes[0].fill_between(budget, mean-spread, mean+spread, color=PALETTE[role], alpha=0.12, linewidth=0)
        axes[1].plot(compute[key], mean, color=PALETTE[role], marker=marker, label=key)
    for ax in axes:
        ax.set_ylim(40, 90)
        ax.set_ylabel("Success (%)")
        ax.set_xscale("log", base=2)
        ax.grid(axis="y")
    axes[0].set(title="(a) Performance by tool budget", xlabel="Tool calls allowed")
    axes[0].set_xticks(budget, labels=[str(x) for x in budget])
    axes[0].legend(loc="lower right")
    axes[1].set(title="(b) Performance and compute", xlabel="Inference compute (relative units)")
    axes[1].set_xticks([1, 2, 4, 8], labels=["1", "2", "4", "8"])
    footer(fig)
    caption = ("Illustrative synthetic data. Each tool budget has eight independent synthetic runs; "
               "points show their mean and bands in (a) show plus/minus one sample standard deviation, "
               "not confidence intervals. Panel (b) pairs the same means with invented relative compute "
               "values; lines connect ordered budgets within a method. No empirical or inferential claim.")
    return save(fig, out, "01_budget_and_tradeoff",
                {"tool_budget": budget.tolist(), "success_samples_pct": {k: v.tolist() for k,v in samples.items()},
                 "relative_compute": {k: v.tolist() for k,v in compute.items()}}, caption)


def intervals(out):
    rng = np.random.default_rng(SEED + 1)
    labels = ["Short history", "Conflicting update", "Delayed feedback", "Tool interruption", "Long horizon", "Transfer"]
    samples = rng.normal(np.array([2, 9, 5, -3, 12, 0])[:, None],
                         np.array([3, 4, 3, 4, 5, 4])[:, None], size=(6, 24))
    mid = np.median(samples, axis=1)
    lo, hi = np.quantile(samples, [0.1, 0.9], axis=1)
    validate_intervals(mid, lo, hi)
    fig, ax = make_figure(85, 76)
    fig.get_layout_engine().set(rect=(0, 0.09, 1, 0.91))
    rows = np.arange(len(labels))
    ax.axvline(0, color=PALETTE["reference"], lw=0.7, zorder=0)
    ax.hlines(rows, lo, hi, color=PALETTE["focus"], linewidth=1.5)
    ax.plot(mid, rows, "o", color=PALETTE["focus"], markersize=4)
    ax.set_yticks(rows, labels=labels)
    ax.invert_yaxis()
    ax.set_ylim(5.7, -0.7)
    ax.set_xlim(-12, 22)
    ax.set_xticks([-10, 0, 10, 20])
    ax.set(title="Paired episode differences", xlabel="Success change (percentage points)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    footer(fig)
    caption = ("Illustrative synthetic data. Each row contains 24 synthetic paired episode differences. "
               "Dots are medians; horizontal intervals span the 10th to 90th percentiles of episode "
               "differences. These show dispersion, not confidence intervals or statistical significance. "
               "Zero denotes no difference, and negative values remain visible.")
    return save(fig, out, "02_paired_intervals",
                {"condition": labels, "paired_episode_deltas_pp": samples.tolist(),
                 "median": mid.tolist(), "q10": lo.tolist(), "q90": hi.tolist()}, caption, SEED + 1)


def heatmaps(out):
    rng = np.random.default_rng(SEED + 2)
    labels = ["Preference", "Constraint", "Fact", "Tool state"]
    delays = [0, 4, 16, 64]
    values = np.array([[[2, 0, -4, -9], [3, 1, -3, -8], [1, -2, -6, -11], [0, -3, -8, -13]],
                       [[3, 5, 7, 9], [2, 7, 9, 12], [3, 4, 8, 10], [1, 5, 10, 13]]], dtype=float)
    values += rng.integers(-1, 2, size=values.shape)
    fig, axes = make_figure(178, 66, ncols=2)
    fig.get_layout_engine().set(rect=(0, 0.10, 1, 0.90))
    cmap = LinearSegmentedColormap.from_list("delta_orange_blue",
                                           [PALETTE["alternative"], "#F9FAFB", PALETTE["focus"]])
    norm = TwoSlopeNorm(vmin=-15, vcenter=0, vmax=15)
    for index, (ax, title) in enumerate(zip(axes, ["(a) Read-only memory", "(b) Read and update"])):
        plot = ax.imshow(values[index], cmap=cmap, norm=norm, aspect="auto", interpolation="nearest")
        ax.set_xticks(range(4), labels=[str(x) for x in delays])
        ax.set_yticks(range(4), labels=labels)
        ax.set(title=title, xlabel="Intervening turns")
        ax.tick_params(length=0)
        for spine in ax.spines.values(): spine.set_visible(False)
        for row in range(4):
            for col in range(4):
                value = values[index,row,col]
                ax.text(col,row,f"{value:+.0f}",ha="center",va="center",fontsize=7.5,
                        color="white" if abs(value) >= 11 else PALETTE["ink"])
    colorbar = fig.colorbar(plot, ax=axes, fraction=0.035, pad=0.035, ticks=[-15,0,15])
    colorbar.set_label("Success change (percentage points)")
    colorbar.outline.set_visible(False)
    footer(fig)
    caption = ("Illustrative synthetic cell summaries relative to an invented common baseline. "
               "Both panels use the same success metric, symmetric -15 to +15 percentage-point scale, "
               "zero center, row order, and delay values. Cells are constructed values, not estimates "
               "from trials; no uncertainty or inferential claim is implied.")
    return save(fig, out, "03_shared_scale_heatmaps",
                {"rows":labels,"delay_turns":delays,"conditions":["read_only","read_update"],
                 "success_delta_pp":values.tolist(),"shared_scale_pp":[-15,15]},caption, SEED + 2)


def method(out):
    fig, ax = make_figure(178, 86)
    fig.get_layout_engine().set(rect=(0, 0.07, 1, 0.93))
    ax.set(xlim=(0,100),ylim=(0,100))
    ax.axis("off")
    nodes = [
        (3,57,16,12,"Query",PALETTE["reference"],"#F5F6F7"),
        (31,57,22,12,"Agent controller",PALETTE["focus"],"#EAF3F8"),
        (72,57,20,12,"Tools",PALETTE["reference"],"#F5F6F7"),
        (31,86,22,10,"Answer",PALETTE["reference"],"#F5F6F7"),
        (22,14,27,14,"Memory store\nrecords + provenance",PALETTE["teal"],"#ECF7F2"),
        (66,14,26,14,"Update rule\nresolve + version",PALETTE["alternative"],"#FFF4E9"),
    ]
    for x,y,w,h,text,color,fill in nodes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=1.2",
                                   facecolor=fill,edgecolor=color,linewidth=0.9))
        ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=8)
    def arrow(start,end,*,color="reference",style="-",connection="arc3,rad=0"):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle="-|>",mutation_scale=8,
                                    linewidth=0.9,color=PALETTE[color],linestyle=style,
                                    connectionstyle=connection,shrinkA=2,shrinkB=2))
    arrow((19,63),(31,63)); arrow((42,69),(42,86))
    arrow((53,63),(72,63))
    ax.text(62.5,66,"call",ha="center",fontsize=7.5)
    # Explicit boundary ports and a reserved upper return corridor.
    # The former near-collinear bend rode along the Tools top border.
    return_path = MplPath([(82,69),(82,80),(50,80),(50,69)],
                          [MplPath.MOVETO,MplPath.LINETO,MplPath.LINETO,MplPath.LINETO])
    ax.add_patch(FancyArrowPatch(path=return_path,arrowstyle="-|>",mutation_scale=8,
                                linewidth=0.9,color=PALETTE["reference"],linestyle="--"))
    ax.text(68,82,"observation",ha="center",fontsize=7.5)
    arrow((35,28),(35,57),color="teal")
    ax.text(33,42,"read",ha="right",va="center",fontsize=7.5,color=PALETTE["ink"])
    arrow((48,57),(75,28),color="alternative",style="--")
    ax.text(62,43,"update",ha="center",va="center",fontsize=7.5,
            bbox={"facecolor":"white","edgecolor":"none","pad":1.4})
    arrow((66,21),(49,21),color="alternative")
    ax.text(57.5,24.5,"write",ha="center",fontsize=7.5)
    ax.text(50,5,"Solid: task/data flow    Dashed: feedback",ha="center",fontsize=7,
            color=PALETTE["reference"])
    footer(fig,"SYNTHETIC EXAMPLE - SCHEMATIC ONLY")
    caption = ("Original illustrative architecture, not an implemented or evaluated system. "
               "A query enters the controller; stored context is read before generating an answer. "
               "Tool calls return observations through a distinct dashed feedback path. New evidence "
               "passes through a versioned update rule before records are written. Colored node labels "
               "are redundant with their text; arrow styles distinguish feedback from task/data flow.")
    data = {"nodes":[{"label":n[4],"x":n[0],"y":n[1],"width":n[2],"height":n[3]} for n in nodes],
            "edges":[["query","controller","input"],["controller","answer","output"],
                     ["controller","tools","call"],["tools","controller","observation"],
                     ["memory","controller","read"],["controller","update","update"],
                     ["update","memory","write"]]}
    return save(fig,out,"04_agent_memory_method",data,caption,seed=None)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    with style_context():
        for recipe in (curves, intervals, heatmaps, method):
            result=recipe(args.out)
            print(result["manifest"])


if __name__ == "__main__":
    main()
