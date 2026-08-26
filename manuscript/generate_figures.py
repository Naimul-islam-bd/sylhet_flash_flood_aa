"""
generate_figures.py  (v2 - dual format output)
================================================
Generate all 5 IJDRR-compliant manuscript figures in BOTH formats:
  - PDF (vector, for final IJDRR submission upload)
  - JPG at 300 dpi (raster, for embedding in Word docx)

Usage from project root:
    python manuscript\generate_figures.py --outdir outputs\figures

Requires: matplotlib, numpy, pandas, rasterio
"""

from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- IJDRR-compliant matplotlib defaults ---
mpl.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.titlesize": 11,
    "lines.linewidth": 1.2,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

COLORS = {
    "blue":    "#1f77b4",
    "orange":  "#ff7f0e",
    "green":   "#2ca02c",
    "red":     "#d62728",
    "purple":  "#9467bd",
    "brown":   "#8c564b",
    "gray":    "#7f7f7f",
}


def save_both(fig, outdir: Path, stem: str, dpi_jpg=300):
    """Save current figure as both PDF and JPG."""
    pdf_path = outdir / f"{stem}.pdf"
    jpg_path = outdir / f"{stem}.jpg"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(jpg_path, bbox_inches="tight", dpi=dpi_jpg, format="jpg")
    print(f"  Wrote: {pdf_path.name}  +  {jpg_path.name}")


# =====================================================================
# FIGURE 1 - Study area map
# =====================================================================
def figure_1_study_area(outdir: Path) -> None:
    fig = plt.figure(figsize=(7.48, 4.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 2, 0.03])
    ax_inset = fig.add_subplot(gs[0, 0])
    ax_main = fig.add_subplot(gs[0, 1])

    ax_inset.set_xlim(87, 96)
    ax_inset.set_ylim(20, 27)
    ax_inset.add_patch(plt.Rectangle((88.0, 20.7), 4.6, 5.4,
                                      fill=False, edgecolor="black", linewidth=1))
    ax_inset.add_patch(plt.Rectangle((90.9, 24.0), 1.5, 1.2,
                                      fill=True, facecolor=COLORS["red"],
                                      alpha=0.4, edgecolor="black", linewidth=0.8))
    ax_inset.text(90.5, 23.7, "Bangladesh", fontsize=7, ha="center")
    ax_inset.text(91.6, 25.4, "Sylhet\nDivision", fontsize=6.5, ha="center",
                   color="darkred", fontweight="bold")
    ax_inset.set_title("(a) Regional locator", fontsize=9)
    ax_inset.set_xlabel("Longitude ($^\\circ$E)")
    ax_inset.set_ylabel("Latitude ($^\\circ$N)")
    ax_inset.grid(alpha=0.3)

    ax_main.set_xlim(89.0, 95.0)
    ax_main.set_ylim(22.5, 26.5)
    ax_main.add_patch(plt.Rectangle((89.5, 22.7), 4.5, 3.3,
                                     fill=True, facecolor=COLORS["blue"],
                                     alpha=0.15, edgecolor=COLORS["blue"],
                                     linewidth=1.5, linestyle="--",
                                     label="Trans-boundary Barak-Meghna"))
    ax_main.add_patch(plt.Rectangle((90.9, 24.0), 1.6, 1.2,
                                     fill=True, facecolor=COLORS["red"],
                                     alpha=0.35, edgecolor="black", linewidth=1.2,
                                     label="Sylhet Division (FAO GAUL L1)"))
    districts = [
        ("Sunamganj",   90.9, 24.6, 0.8, 0.6),
        ("Sylhet",      91.7, 24.6, 0.8, 0.6),
        ("Habiganj",    90.9, 24.0, 0.8, 0.6),
        ("Maulvibazar", 91.7, 24.0, 0.8, 0.6),
    ]
    for name, x, y, w, h in districts:
        ax_main.add_patch(plt.Rectangle((x, y), w, h, fill=False,
                                          edgecolor="black", linewidth=0.5))
        ax_main.text(x + w/2, y + h/2, name, fontsize=7, ha="center", va="center")
    ax_main.text(92.0, 25.7, "Meghalaya (India)\norographic zone", fontsize=7,
                  ha="center", style="italic", color=COLORS["gray"])
    ax_main.set_title("(b) Sylhet Division and trans-boundary catchment", fontsize=9)
    ax_main.set_xlabel("Longitude ($^\\circ$E)")
    ax_main.set_ylabel("Latitude ($^\\circ$N)")
    ax_main.legend(loc="lower right", fontsize=7)
    ax_main.grid(alpha=0.3)

    fig.suptitle("Figure 1. Study area", fontweight="bold", y=1.02)
    fig.text(0.5, -0.02,
             "Map lines delineate study areas and do not necessarily depict accepted national boundaries.",
             ha="center", fontsize=7, style="italic")
    plt.tight_layout()
    save_both(fig, outdir, "Figure_1")
    plt.close()


# =====================================================================
# FIGURE 2 - Three-dataset climate trends
# =====================================================================
def figure_2_trends(outdir: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(7.48, 3.0), sharey=False)
    datasets = [
        ("CHIRPS Sylhet 1981-2024",
         Path("outputs/stage_a/annual_indices.csv"),
         COLORS["blue"], "-0.45 mm/yr, p=0.895"),
        ("ERA5-Land Sylhet 1950-2024",
         Path("outputs/stage_a_era5/annual_indices.csv"),
         COLORS["orange"], "-8.89 mm/yr, p=0.012"),
        ("ERA5-Land trans-boundary 1950-2024",
         Path("outputs/stage_a_transboundary/annual_indices.csv"),
         COLORS["green"], "-3.87 mm/yr, p=0.012"),
    ]
    for ax, (label, path, color, slope_label) in zip(axes, datasets):
        if path.exists():
            df = pd.read_csv(path)
            pm_col = [c for c in df.columns if "premonsoon" in c.lower()
                       or "pre_monsoon" in c.lower() or "MAM" in c]
            if pm_col:
                y = df[pm_col[0]].values
                x = df["year"].values if "year" in df.columns else np.arange(len(y)) + df.index.min()
                ax.plot(x, y, color=color, linewidth=1.0, alpha=0.7)
                mask = ~np.isnan(y)
                if mask.sum() > 5:
                    slope, intercept = np.polyfit(x[mask], y[mask], 1)
                    ax.plot(x, slope * x + intercept, color=color,
                             linewidth=1.5, linestyle="--")
        else:
            ax.text(0.5, 0.5, f"Missing:\n{path.name}", ha="center", va="center",
                     transform=ax.transAxes, fontsize=8, color="gray")
        ax.set_title(label, fontsize=8)
        ax.set_xlabel("Year")
        ax.set_ylabel("Pre-monsoon rainfall (mm)")
        ax.text(0.02, 0.97, slope_label, transform=ax.transAxes,
                fontsize=7, verticalalignment="top",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                           edgecolor="gray", alpha=0.8))
        ax.grid(alpha=0.3)
    fig.suptitle("Figure 2. Pre-monsoon rainfall trends across three datasets",
                 fontweight="bold", y=1.02)
    plt.tight_layout()
    save_both(fig, outdir, "Figure_2")
    plt.close()


# =====================================================================
# FIGURE 3 - Seven-event flood extent panels
# =====================================================================
def figure_3_flood_panels(outdir: Path) -> None:
    try:
        import rasterio
    except ImportError:
        print("  rasterio not installed - skipping Fig 3")
        return
    events = [
        ("2017 April",   "data/raw/ev_2017_apr_flood_extent.tif", 3157),
        ("2019 July",    "data/raw/ev_2019_jul_flood_extent.tif", 965),
        ("2020 July",    "data/raw/ev_2020_jul_flood_extent.tif", 448),
        ("2022 May",     "data/raw/ev_2022_may_flood_extent.tif", 2777),
        ("2022 June",    "data/raw/ev_2022_jun_flood_extent.tif", 5963),
        ("2023 May",     "data/raw/ev_2023_may_flood_extent.tif", 422),
        ("2024 July",    "data/raw/ev_2024_jul_flood_extent.tif", 5292),
    ]
    fig, axes = plt.subplots(2, 4, figsize=(7.48, 4.5))
    axes = axes.flatten()
    for ax, (label, path, area) in zip(axes[:7], events):
        p = Path(path)
        if p.exists():
            with rasterio.open(p) as src:
                arr = src.read(1)
            ax.imshow(arr, cmap="Blues", vmin=0, vmax=1)
        else:
            ax.text(0.5, 0.5, "missing", ha="center", va="center",
                     transform=ax.transAxes, color="gray")
        ax.set_title(f"{label}\n{area} km$^2$", fontsize=8)
        ax.set_xticks([]); ax.set_yticks([])
        ax.spines[:].set_visible(False)
    axes[7].axis("off")
    axes[7].text(0.05, 0.95, "Sentinel-1 GRD IW VV\nOtsu threshold",
                  transform=axes[7].transAxes, fontsize=8,
                  verticalalignment="top", fontweight="bold")
    axes[7].add_patch(plt.Rectangle((0.05, 0.5), 0.2, 0.15,
                                     facecolor=COLORS["blue"],
                                     transform=axes[7].transAxes))
    axes[7].text(0.3, 0.57, "Detected flood", transform=axes[7].transAxes,
                  fontsize=7, verticalalignment="center")
    axes[7].add_patch(plt.Rectangle((0.05, 0.3), 0.2, 0.15,
                                     facecolor="lightgray",
                                     transform=axes[7].transAxes))
    axes[7].text(0.3, 0.37, "Non-flood", transform=axes[7].transAxes,
                  fontsize=7, verticalalignment="center")
    fig.suptitle("Figure 3. Sentinel-1 SAR flood extents for seven documented events",
                 fontweight="bold", y=1.00)
    plt.tight_layout()
    save_both(fig, outdir, "Figure_3", dpi_jpg=500)
    plt.close()


# =====================================================================
# FIGURE 4 - Skill diagnostics
# =====================================================================
def figure_4_skill_diagnostics(outdir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(7.48, 5.5))
    candidates = [
        Path("outputs/stage_d/sweep_calibration.csv"),
        Path("outputs/stage_d_final_premonsoon/sweep_calibration.csv"),
        Path("outputs/stage_d_premon_trans/sweep_calibration.csv"),
        Path("outputs/stage_d_trans/sweep_calibration.csv"),
    ]
    sweep_path = next((p for p in candidates if p.exists()), None)
    if sweep_path:
        s = pd.read_csv(sweep_path)
        print(f"    (Fig 4 reading sweep from: {sweep_path})")
        for w, c in zip([1, 2, 3, 5, 7],
                        [COLORS["blue"], COLORS["orange"], COLORS["green"],
                         COLORS["red"], COLORS["purple"]]):
            sub = s[s["window_days"] == w].sort_values("threshold_mm")
            axes[0, 0].plot(sub["threshold_mm"], sub["CSI"], color=c,
                             label=f"{w}-day", linewidth=1.0)
    axes[0, 0].set_xlabel("Threshold (mm)")
    axes[0, 0].set_ylabel("Critical Success Index")
    axes[0, 0].set_title("(a) CSI vs threshold (calibration)")
    axes[0, 0].legend(loc="best", fontsize=7)
    axes[0, 0].grid(alpha=0.3)

    if sweep_path:
        for w, c in zip([1, 2, 3, 5, 7],
                        [COLORS["blue"], COLORS["orange"], COLORS["green"],
                         COLORS["red"], COLORS["purple"]]):
            sub = s[s["window_days"] == w].sort_values("threshold_mm")
            axes[0, 1].plot(sub["threshold_mm"], sub["HSS"], color=c,
                             label=f"{w}-day", linewidth=1.0)
    axes[0, 1].set_xlabel("Threshold (mm)")
    axes[0, 1].set_ylabel("Heidke Skill Score")
    axes[0, 1].set_title("(b) HSS vs threshold (calibration)")
    axes[0, 1].legend(loc="best", fontsize=7)
    axes[0, 1].grid(alpha=0.3)

    if sweep_path:
        for w, c in zip([1, 2, 3, 5, 7],
                        [COLORS["blue"], COLORS["orange"], COLORS["green"],
                         COLORS["red"], COLORS["purple"]]):
            sub = s[s["window_days"] == w].sort_values("FAR")
            axes[1, 0].plot(sub["FAR"], sub["POD"], color=c,
                             label=f"{w}-day", linewidth=1.0)
    axes[1, 0].plot([0, 1], [0, 1], color="black", linestyle=":", linewidth=0.8,
                     label="No skill")
    axes[1, 0].set_xlabel("False alarm ratio")
    axes[1, 0].set_ylabel("Probability of detection")
    axes[1, 0].set_title("(c) ROC curves per window")
    axes[1, 0].set_xlim(0, 1); axes[1, 0].set_ylim(0, 1)
    axes[1, 0].legend(loc="lower right", fontsize=7)
    axes[1, 0].grid(alpha=0.3)

    seasons = ["Pre-monsoon\n(3-d ≥ 19 mm)\nTrans-boundary",
                "Monsoon\n(7-d ≥ 206 mm)\nLocal Sylhet"]
    csi = [0.196, 0.163]; csi_lo = [0.134, 0.110]; csi_hi = [0.253, 0.220]
    pod = [0.627, 0.347]; pod_lo = [0.512, 0.253]; pod_hi = [0.744, 0.451]
    x = np.arange(len(seasons))
    width = 0.35
    axes[1, 1].bar(x - width/2, csi, width,
                    yerr=[[c - lo for c, lo in zip(csi, csi_lo)],
                          [hi - c for c, hi in zip(csi, csi_hi)]],
                    color=COLORS["blue"], alpha=0.8, label="CSI",
                    capsize=4, edgecolor="black", linewidth=0.5)
    axes[1, 1].bar(x + width/2, pod, width,
                    yerr=[[p - lo for p, lo in zip(pod, pod_lo)],
                          [hi - p for p, hi in zip(pod, pod_hi)]],
                    color=COLORS["orange"], alpha=0.8, label="POD",
                    capsize=4, edgecolor="black", linewidth=0.5)
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(seasons, fontsize=7)
    axes[1, 1].set_ylabel("Skill score")
    axes[1, 1].set_title("(d) Blind validation 2011-2024 (95% CIs)")
    axes[1, 1].set_ylim(0, 1)
    axes[1, 1].legend(loc="upper right", fontsize=8)
    axes[1, 1].grid(alpha=0.3, axis="y")

    fig.suptitle("Figure 4. Skill diagnostics for season-stratified rainfall triggers",
                 fontweight="bold", y=1.00)
    plt.tight_layout()
    save_both(fig, outdir, "Figure_4")
    plt.close()


# =====================================================================
# FIGURE 5 - Proposed framework (4-layer)
# =====================================================================
def figure_5_framework(outdir: Path) -> None:
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    fig, ax = plt.subplots(figsize=(7.48, 8.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.set_axis_off()

    layer_colors = [COLORS["blue"], COLORS["orange"], COLORS["green"], COLORS["red"]]
    layer_labels = ["MONITORING", "TRIGGER", "ANTICIPATORY ACTION", "IMPACT"]
    layer_y = [10.0, 7.5, 4.5, 1.5]

    def box(x, y, w, h, text, color, fs=7):
        p = FancyBboxPatch((x, y), w, h,
                            boxstyle="round,pad=0.05,rounding_size=0.15",
                            facecolor=color, alpha=0.25, edgecolor=color,
                            linewidth=1.5)
        ax.add_patch(p)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=fs, wrap=True)

    def arrow(y_top, y_bottom):
        a = FancyArrowPatch((5, y_top), (5, y_bottom),
                             arrowstyle="->,head_width=0.3,head_length=0.4",
                             color="black", linewidth=2)
        ax.add_patch(a)

    for label, y, color in zip(layer_labels, layer_y, layer_colors):
        ax.text(0.05, y + 0.6, label, fontsize=9, fontweight="bold",
                color=color, va="center")

    labels_L1 = [
        "Trans-boundary\nrainfall\n(ERA5-Land, 9 km)",
        "Sylhet local\nrainfall\n(CHIRPS, 5.5 km)",
        "FFWC gauge\nstations\n(5 sites)",
        "Season indicator\n(pre-monsoon or\nmonsoon)",
    ]
    for i, t in enumerate(labels_L1):
        box(0.6 + i*2.3, layer_y[0], 2.0, 1.2, t, layer_colors[0], fs=6.5)

    box(0.9, layer_y[1], 4.0, 1.7,
        "PRE-MONSOON (Mar-May)\n\nTrans-boundary 3-day\nrainfall ≥ 19 mm\n\nPOD 0.63 [0.51-0.74]\nCSI 0.20  |  HSS 0.32",
        layer_colors[1], fs=7)
    box(5.1, layer_y[1], 4.0, 1.7,
        "MONSOON (Jun-Sep)\n\nLocal Sylhet 7-day\nrainfall ≥ 206 mm\n\nPOD 0.35 [0.25-0.45]\nCSI 0.16  |  HSS 0.27",
        layer_colors[1], fs=7)

    labels_L3 = [
        "Cash transfer\nBDT 4,500 per\nhousehold",
        "Livestock\nevacuation to\nhigher ground",
        "Grain and seed\nprotection\n(elevated storage)",
        "Vulnerable\nperson\nevacuation",
        "WASH kit\npre-positioning\n(water, sanitation)",
    ]
    for i, t in enumerate(labels_L3):
        box(0.4 + i*1.9, layer_y[2], 1.7, 1.6, t, layer_colors[2], fs=6.5)

    box(0.6, layer_y[3], 8.6, 1.3,
        "Reduced flash flood impact for 4-7 million people at risk in Sylhet Division\n"
        "Estimated benefit-cost ratio 7:1  |  ~USD 1 billion damages avoidable across 7 events",
        layer_colors[3], fs=8)

    arrow(layer_y[0], layer_y[1] + 1.7)
    arrow(layer_y[1], layer_y[2] + 1.6)
    arrow(layer_y[2], layer_y[3] + 1.3)

    ax.text(5, 11.6,
            "Figure 5. Proposed framework for flash flood anticipatory action\nin Sylhet Division, Bangladesh",
            ha="center", fontsize=10, fontweight="bold")
    ax.text(5, 0.2,
            "Threshold values derived from calibration on 1981 to 2010 and blindly validated on 2011 to 2024 (Table 7).\n"
            "Anticipatory action interventions and unit costs adapted from Bangladesh Red Crescent Society Jamuna programme (2020).\n"
            "Impact estimate combines Stage C exposure (Table 5) with return-on-investment multiplier 7:1 (FAO/WFP/OCHA 2025).",
            ha="center", fontsize=6, style="italic")
    save_both(fig, outdir, "Figure_5")
    plt.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="outputs/figures")
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    print("Generating IJDRR figures (PDF + JPG dual output) ...")
    figure_1_study_area(outdir)
    figure_2_trends(outdir)
    figure_3_flood_panels(outdir)
    figure_4_skill_diagnostics(outdir)
    figure_5_framework(outdir)
    print(f"\nAll figures written to: {outdir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
