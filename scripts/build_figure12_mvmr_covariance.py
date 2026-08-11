#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NAVY = "#214F7B"
TEAL = "#2B7A78"
CORAL = "#C95F4A"
CHARCOAL = "#4E5968"
LIGHT_GRID = "#D9DEE5"
TEXT = "#1F2A3A"


def style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#9AA5B1")
    ax.spines["bottom"].set_color("#9AA5B1")
    ax.tick_params(colors=TEXT, labelsize=9)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build manuscript Figure 12.")
    parser.add_argument(
        "--sensitivity",
        type=Path,
        default=REPOSITORY_ROOT
        / "supplementary"
        / "Supplementary_Table_S27_MVMR_covariance_sensitivity.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY_ROOT
        / "figures"
        / "Figure12_MVMR_covariance_sensitivity.png",
    )
    args = parser.parse_args()
    sensitivity = args.sensitivity.resolve()
    output = args.output.resolve()
    if not sensitivity.is_file():
        raise SystemExit(f"Sensitivity table not found: {sensitivity}")
    output.parent.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 10,
            "axes.titleweight": "bold",
            "axes.labelcolor": TEXT,
            "text.color": TEXT,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(12, 7.3),
        gridspec_kw={"width_ratios": [1.18, 1.0], "wspace": 0.38},
    )

    labels = [
        "BMI -> IVDD",
        "BMI -> spinal stenosis",
        "Smoking initiation -> IVDD",
        "Smoking initiation -> spinal stenosis",
    ]
    univ = np.array([1.301, 1.622, 1.229, 1.379])
    univ_lo = np.array([1.197, 1.449, 1.076, 1.127])
    univ_hi = np.array([1.413, 1.816, 1.403, 1.686])
    mvmr = np.array([1.26, 1.59, 1.10, 1.17])
    mvmr_lo = np.array([1.17, 1.43, 0.99, 1.01])
    mvmr_hi = np.array([1.36, 1.77, 1.23, 1.36])

    y = np.arange(len(labels))[::-1]
    offset = 0.12
    ax1.axvline(1.0, color="#687586", linestyle="--", linewidth=1.2, zorder=0)
    for idx in range(len(labels)):
        ax1.errorbar(
            univ[idx],
            y[idx] + offset,
            xerr=[[univ[idx] - univ_lo[idx]], [univ_hi[idx] - univ[idx]]],
            fmt="o",
            color=CHARCOAL,
            ecolor=CHARCOAL,
            elinewidth=1.6,
            capsize=0,
            markersize=5.5,
            zorder=3,
        )
        direct_color = NAVY if idx < 2 else CORAL
        ax1.errorbar(
            mvmr[idx],
            y[idx] - offset,
            xerr=[[mvmr[idx] - mvmr_lo[idx]], [mvmr_hi[idx] - mvmr[idx]]],
            fmt="o",
            color=direct_color,
            ecolor=direct_color,
            elinewidth=1.8,
            capsize=0,
            markersize=6,
            zorder=4,
        )
        ax1.plot(
            [univ[idx], mvmr[idx]],
            [y[idx] + offset, y[idx] - offset],
            color="#B7C0CC",
            linewidth=1,
            zorder=1,
        )

    ax1.set_yticks(y, labels)
    ax1.set_xlim(0.92, 1.92)
    ax1.set_xlabel("Odds ratio for registry-based diagnosis endpoint", labelpad=10)
    ax1.set_title("A  Univariable and mutually adjusted estimates", loc="left", pad=12)
    ax1.grid(axis="x", color=LIGHT_GRID, linewidth=0.8)
    ax1.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                color=CHARCOAL,
                label="Univariable IVW",
                linestyle="-",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color=NAVY,
                label="MVMR direct estimate: BMI",
                linestyle="-",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color=CORAL,
                label="MVMR direct estimate: smoking initiation",
                linestyle="-",
            ),
        ],
        loc="lower right",
        frameon=False,
        fontsize=8.7,
    )
    style_axis(ax1)

    sens = pd.read_csv(sensitivity)
    sens = sens.sort_values("assumed_error_correlation_rho").drop_duplicates(
        ["exposure", "assumed_error_correlation_rho"]
    )
    for exposure, color, marker in [
        ("BMI", NAVY, "o"),
        ("Smoking initiation", CORAL, "s"),
    ]:
        dat = sens[sens["exposure"] == exposure]
        ax2.plot(
            dat["assumed_error_correlation_rho"],
            dat["conditional_F"],
            color=color,
            marker=marker,
            markersize=5.5,
            linewidth=2,
            label=exposure,
        )

    ax2.axhline(10, color=TEAL, linestyle="--", linewidth=1.4)
    ax2.text(
        -0.88,
        10.7,
        "Conventional conditional F = 10",
        color=TEAL,
        fontsize=8.5,
        va="bottom",
    )
    ax2.set_yscale("log")
    ax2.set_ylim(4.8, 360)
    ax2.set_yticks([5, 10, 20, 50, 100, 200])
    ax2.get_yaxis().set_major_formatter(plt.ScalarFormatter())
    ax2.set_xlim(-0.95, 0.95)
    ax2.set_xticks([-0.9, -0.5, 0, 0.5, 0.9])
    ax2.set_xlabel(r"Assumed error correlation, $\rho$")
    ax2.set_ylabel("Conditional F statistic")
    ax2.set_title("B  Covariance-assumption stress test", loc="left", pad=12)
    ax2.grid(axis="y", which="major", color=LIGHT_GRID, linewidth=0.8)
    ax2.legend(loc="upper left", frameon=False, fontsize=9)
    style_axis(ax2)

    fig.text(
        0.5,
        0.025,
        "Panel B varies an assumed constant correlation between SNP-exposure "
        "estimation errors; it does not estimate the true covariance.",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#5F6B7A",
    )
    fig.subplots_adjust(left=0.13, right=0.98, top=0.91, bottom=0.15)
    fig.savefig(output, dpi=300, bbox_inches="tight")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
