"""
Publication-quality figure builders for the paper.

Each function returns a matplotlib Figure so the caller can save it in
whichever format IJDRR requires for that figure (typically PDF vector
for line plots, TIFF at 300+ dpi for maps).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .figure_specs import (
    apply_ijdrr_style, COLORBLIND_PALETTE, DIVERGING_CMAP,
)
from ..analysis.trends import mann_kendall, sens_slope
from ..analysis.extremes import INDEX_COLUMNS


def figure_1_trend(annual_df: pd.DataFrame, dataset_label: str = "CHIRPS"):
    """Figure 1: pre-monsoon rainfall time series with Sen's slope + MK p-value."""
    import matplotlib.pyplot as plt
    apply_ijdrr_style()

    years = annual_df["year"].values
    vals = annual_df["premonsoon_mm"].values

    mk = mann_kendall(vals)
    slope = sens_slope(years, vals)

    y_med = np.median(vals); x_med = np.median(years)
    trend_line = slope * (years - x_med) + y_med

    # 5-year rolling mean for context
    rolling = pd.Series(vals).rolling(5, center=True, min_periods=3).mean().values

    fig, ax = plt.subplots(figsize=(7.48, 4.0))
    ax.plot(years, vals, marker="o", markersize=3.5, lw=1.2,
            color=COLORBLIND_PALETTE[0], label=f"Pre-monsoon rainfall (Mar-May), {dataset_label}")
    ax.plot(years, rolling, lw=1.8, color=COLORBLIND_PALETTE[1],
            label="5-year moving average")
    ax.plot(years, trend_line, "--", lw=1.6, color=COLORBLIND_PALETTE[3],
            label=f"Sen's slope: {slope:+.2f} mm/yr (MK p={mk['p_value']:.3f}, {mk['trend']})")

    ax.set_xlabel("Year")
    ax.set_ylabel("Pre-monsoon rainfall (mm)")
    ax.set_title(f"Figure 1. Sylhet pre-monsoon rainfall, {dataset_label} "
                 f"{int(years.min())}-{int(years.max())}")
    ax.grid(True, alpha=0.3, ls=":")
    ax.legend(loc="upper right", frameon=True, framealpha=0.9)
    fig.tight_layout()
    return fig


def figure_1b_indices_heatmap(annual_df: pd.DataFrame):
    """Decadal % change heatmap for all ETCCDI indices vs 1981-1990 baseline."""
    import matplotlib.pyplot as plt
    apply_ijdrr_style()

    y_min, y_max = int(annual_df["year"].min()), int(annual_df["year"].max())
    edges = list(range(y_min - 1, y_max + 5, 10))
    if edges[-1] < y_max:
        edges.append(y_max + 1)
    labels = [f"{edges[i]+1}-{min(edges[i+1], y_max)}" for i in range(len(edges) - 1)]

    decades = pd.cut(annual_df["year"], bins=edges, labels=labels)
    dec_means = annual_df.groupby(decades, observed=False)[INDEX_COLUMNS].mean()
    baseline = dec_means.iloc[0]
    pct_change = (dec_means - baseline) / baseline.replace(0, np.nan) * 100.0

    fig, ax = plt.subplots(figsize=(7.48, 3.8))
    im = ax.imshow(pct_change.T, aspect="auto", cmap=DIVERGING_CMAP,
                   vmin=-50, vmax=50)
    ax.set_xticks(range(len(pct_change.index)))
    ax.set_xticklabels(pct_change.index, rotation=30, ha="right")
    ax.set_yticks(range(len(INDEX_COLUMNS)))
    ax.set_yticklabels(INDEX_COLUMNS)
    ax.set_title(f"Decadal % change in extreme rainfall indices vs {labels[0]}")

    # Annotate each cell with the % value
    for i in range(pct_change.T.shape[0]):
        for j in range(pct_change.T.shape[1]):
            v = pct_change.T.iloc[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:+.1f}", ha="center", va="center",
                        fontsize=7, color="black")

    plt.colorbar(im, ax=ax, label="% change")
    fig.tight_layout()
    return fig


def figure_4_skill_curves(cal_all: pd.DataFrame,
                          roc: pd.DataFrame,
                          val_df: pd.DataFrame):
    """Figure 4: four-panel skill score summary."""
    import matplotlib.pyplot as plt
    apply_ijdrr_style()

    fig, axes = plt.subplots(2, 2, figsize=(7.48, 6.0))

    # A: CSI vs threshold per window
    ax = axes[0, 0]
    for i, (w, g) in enumerate(cal_all.groupby("window_days")):
        g = g.sort_values("threshold_mm")
        ax.plot(g["threshold_mm"], g["CSI"], label=f"{int(w)}-day",
                color=COLORBLIND_PALETTE[i % len(COLORBLIND_PALETTE)])
    ax.set_xlabel("Threshold (mm)"); ax.set_ylabel("CSI (calibration)")
    ax.set_title("A. CSI vs threshold by window")
    ax.legend(); ax.grid(True, alpha=0.3)

    # B: ROC per window
    ax = axes[0, 1]
    for i, (w, g) in enumerate(roc.groupby("window_days")):
        g = g.sort_values("FPR")
        ax.plot(g["FPR"], g["POD"], label=f"{int(w)}-day",
                color=COLORBLIND_PALETTE[i % len(COLORBLIND_PALETTE)])
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="No skill")
    ax.set_xlabel("False Positive Rate"); ax.set_ylabel("POD")
    ax.set_title("B. ROC curves (calibration)")
    ax.legend(); ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    # C: HSS vs threshold per window
    ax = axes[1, 0]
    for i, (w, g) in enumerate(cal_all.groupby("window_days")):
        g = g.sort_values("threshold_mm")
        ax.plot(g["threshold_mm"], g["HSS"], label=f"{int(w)}-day",
                color=COLORBLIND_PALETTE[i % len(COLORBLIND_PALETTE)])
    ax.set_xlabel("Threshold (mm)"); ax.set_ylabel("HSS (calibration)")
    ax.set_title("C. HSS vs threshold by window")
    ax.legend(); ax.grid(True, alpha=0.3)

    # D: validation CSI with 95% CI
    ax = axes[1, 1]
    x = np.arange(len(val_df))
    labels = [f"{int(r.window_days)}d\n{r.threshold_mm:.0f}mm" for r in val_df.itertuples()]
    csi_lo = val_df["CSI"] - val_df["CSI_lo"]
    csi_hi = val_df["CSI_hi"] - val_df["CSI"]
    ax.bar(x, val_df["CSI"], yerr=[csi_lo, csi_hi], capsize=4,
           color=COLORBLIND_PALETTE[0])
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("CSI (validation, 95% bootstrap CI)")
    ax.set_title("D. Validation CSI by window")
    ax.grid(True, alpha=0.3, axis="y")

    fig.suptitle("Figure 4. Trigger threshold performance", fontsize=11, y=1.02)
    fig.tight_layout()
    return fig
