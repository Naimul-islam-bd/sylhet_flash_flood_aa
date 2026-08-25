"""
Stage A: climate trend analysis on daily rainfall.

Runs Mann-Kendall + Sen's slope + Pettitt change-point on 8 ETCCDI
extreme rainfall indices plus the pre-monsoon (Mar-May) total.

Works with either CHIRPS (1981-2024) or ERA5-Land (1950-2024) input CSV.

Usage:
    python scripts/01_run_stage_a_trends.py \\
        --input data/raw/sylhet_chirps_daily_1981_2024.csv \\
        --outdir outputs/stage_a

    python scripts/01_run_stage_a_trends.py \\
        --input data/raw/sylhet_era5land_daily_1950_2024.csv \\
        --outdir outputs/stage_a_era5 \\
        --label "ERA5-Land"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

# Make src/ importable when running the script directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sylhet_aa.data import load_daily_rainfall, print_summary   # noqa: E402
from sylhet_aa.analysis.extremes import compute_indices_per_year, run_all_trend_tests  # noqa: E402
from sylhet_aa.viz.figures import figure_1_trend, figure_1b_indices_heatmap  # noqa: E402
from sylhet_aa.viz import save_line_drawing  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage A: climate trend analysis")
    ap.add_argument("--input", required=True, help="Daily rainfall CSV")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--label", default="CHIRPS",
                    help="Dataset label shown in figures (default: CHIRPS)")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- Load and validate ----
    print(f"[Stage A] Loading rainfall from: {args.input}")
    df = load_daily_rainfall(args.input)
    print_summary(df, name=args.label)

    # ---- Compute annual indices ----
    print("\n[Stage A] Computing ETCCDI extreme indices per year ...")
    annual, q95, q99 = compute_indices_per_year(df)
    annual.to_csv(outdir / "annual_indices.csv", index=False)
    (annual[["year", "premonsoon_mm"]]
        .to_csv(outdir / "premonsoon_series.csv", index=False))
    print(f"  Wet-day 95th percentile (baseline 1981-2010): {q95:.2f} mm")
    print(f"  Wet-day 99th percentile (baseline 1981-2010): {q99:.2f} mm")

    # ---- Run trend tests ----
    print("\n[Stage A] Running Mann-Kendall + Sen's slope + Pettitt ...")
    trend_table = run_all_trend_tests(annual)
    trend_table.to_csv(outdir / "table1_trend_statistics.csv",
                       index=False, float_format="%.4f")

    print("\n===== TABLE 1: TREND STATISTICS =====")
    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(trend_table.to_string(index=False))
    print("=====================================\n")

    # ---- Figures ----
    print("[Stage A] Generating figures ...")
    fig1 = figure_1_trend(annual, dataset_label=args.label)
    save_line_drawing(fig1, outdir / "Figure_1.pdf")
    print(f"  Wrote: {outdir / 'Figure_1.pdf'}")

    fig1b = figure_1b_indices_heatmap(annual)
    save_line_drawing(fig1b, outdir / "Figure_1b.pdf")
    print(f"  Wrote: {outdir / 'Figure_1b.pdf'}")

    print(f"\n[Stage A] Done. All outputs in: {outdir.resolve()}")
    print("Every value is computed from the input CSV. Nothing fabricated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
