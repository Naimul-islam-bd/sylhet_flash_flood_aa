"""
Stage D: derive and validate rainfall trigger thresholds for flash floods.

Sweeps thresholds across multiple accumulation windows, computes
POD/FAR/CSI/HSS/ETS on a calibration period, then applies the selected
thresholds blindly on an independent validation period. Reports block
bootstrap 95% CIs.

Usage:
    python scripts/03_run_stage_d_thresholds.py \\
        --rain data/raw/sylhet_chirps_daily_1981_2024.csv \\
        --events data/raw/events_catalogue.csv \\
        --outdir outputs/stage_d
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sylhet_aa.data import load_daily_rainfall, load_events_catalogue  # noqa: E402
from sylhet_aa.analysis.thresholds import (   # noqa: E402
    build_event_labels, sweep_thresholds, pick_optimum,
    roc_points, auc_per_window, antecedent_series,
)
from sylhet_aa.analysis.skill import contingency, skill_scores, block_bootstrap_ci  # noqa: E402
from sylhet_aa.viz.figures import figure_4_skill_curves  # noqa: E402
from sylhet_aa.viz import save_line_drawing  # noqa: E402
from sylhet_aa.config import CAL_END_YEAR_DEFAULT, VAL_START_YEAR_DEFAULT  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage D: trigger threshold derivation")
    ap.add_argument("--rain", required=True, help="Daily rainfall CSV")
    ap.add_argument("--events", required=True, help="Events catalogue CSV")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--seasonal",
                    choices=["all", "premonsoon", "monsoon", "premonsoon_monsoon"],
                    default="premonsoon_monsoon",
                    help="Restrict analysis to season(s). Default: Mar-Sep")
    ap.add_argument("--cal_end", type=int, default=CAL_END_YEAR_DEFAULT,
                    help="Last year of calibration period (inclusive).")
    ap.add_argument("--val_start", type=int, default=VAL_START_YEAR_DEFAULT,
                    help="First year of validation period (inclusive).")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- Load ----
    print(f"[Stage D] Loading rain from: {args.rain}")
    rain = load_daily_rainfall(args.rain)
    print(f"[Stage D] Loading events from: {args.events}")
    events = load_events_catalogue(args.events)
    print(f"  {len(rain)} rainfall days ({rain['date'].min().date()} to "
          f"{rain['date'].max().date()}), {len(events)} events")

    if len(events) < 5:
        print(f"  WARNING: only {len(events)} events. Aim for >= 15 for stable results.")

    labels = build_event_labels(rain, events)
    print(f"  Labelled positive days: {int(labels.sum())} of {len(labels)}")

    # ---- Seasonal mask ----
    months = rain["date"].dt.month.values
    season_map = {
        "premonsoon": {3, 4, 5},
        "monsoon": {6, 7, 8, 9},
        "premonsoon_monsoon": {3, 4, 5, 6, 7, 8, 9},
        "all": set(range(1, 13)),
    }
    smask = np.isin(months, list(season_map[args.seasonal]))
    print(f"  Seasonal filter '{args.seasonal}' keeps {int(smask.sum())} days")

    # ---- Split ----
    years = rain["date"].dt.year.values
    cal_mask = smask & (years <= args.cal_end)
    val_mask = smask & (years >= args.val_start)

    for name, mask in [("calibration", cal_mask), ("validation", val_mask)]:
        if int(mask.sum()) == 0:
            print(f"ERROR: no rainfall days in {name} period. Adjust --cal_end/--val_start.")
            return 1

    if int((labels & cal_mask).sum()) == 0:
        print("ERROR: no positive event days in calibration period. Cannot fit thresholds.")
        return 1

    # ---- Calibration sweep ----
    print(f"\n--- CALIBRATION PERIOD ({years.min()}-{args.cal_end}) ---")
    cal_all = sweep_thresholds(rain, labels, cal_mask)
    if cal_all.empty:
        print("ERROR: threshold sweep produced no rows. Not enough wet days.")
        return 1
    cal_all.to_csv(outdir / "sweep_calibration.csv",
                   index=False, float_format="%.4f")

    cal_best_csi = pick_optimum(cal_all, "CSI")
    print("Best CSI thresholds (calibration):")
    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(cal_best_csi[["window_days", "threshold_mm", "POD", "FAR",
                             "CSI", "HSS"]].to_string(index=False))

    # ---- Validation with block-bootstrap CIs ----
    print(f"\n--- VALIDATION PERIOD ({args.val_start}-{years.max()}) ---")
    val_rows = []
    for _, row in cal_best_csi.iterrows():
        w = int(row["window_days"]); v = float(row["threshold_mm"])
        accum = antecedent_series(rain, w)
        pred = (accum >= v) & val_mask
        act = labels & val_mask
        H, F, M, C = contingency(pred, act)
        s = skill_scores(H, F, M, C)
        ci = block_bootstrap_ci(accum[val_mask], labels[val_mask], v)
        val_rows.append({"window_days": w, "threshold_mm": v,
                          "H": H, "F": F, "M": M, "C": C, **s, **ci,
                          "period": "validation", "selection_criterion": "CSI"})
    val_df = pd.DataFrame(val_rows)
    val_df.to_csv(outdir / "validation_skill_scores.csv",
                  index=False, float_format="%.4f")

    print("Validation skill scores (thresholds selected on calibration, "
          "applied blind):")
    with pd.option_context("display.max_columns", None, "display.width", 220):
        print(val_df[["window_days", "threshold_mm", "POD", "FAR", "CSI", "HSS",
                       "POD_lo", "POD_hi", "CSI_lo", "CSI_hi"]].to_string(index=False))

    # ---- ROC / AUC ----
    roc = roc_points(cal_all)
    roc.to_csv(outdir / "roc_curves.csv", index=False, float_format="%.4f")
    auc = auc_per_window(roc)
    auc.to_csv(outdir / "auc_calibration.csv", index=False, float_format="%.4f")
    print("\nAUC by window (calibration):")
    print(auc.to_string(index=False))

    # ---- Combined Table 4 ----
    combined = val_df.copy()
    combined["cal_CSI"] = combined["window_days"].map(
        dict(zip(cal_best_csi["window_days"], cal_best_csi["CSI"])))
    combined["cal_HSS"] = combined["window_days"].map(
        dict(zip(cal_best_csi["window_days"], cal_best_csi["HSS"])))
    combined = combined[["window_days", "threshold_mm",
                          "cal_CSI", "cal_HSS",
                          "POD", "FAR", "CSI", "HSS", "ETS",
                          "POD_lo", "POD_hi", "CSI_lo", "CSI_hi", "HSS_lo", "HSS_hi"]]
    combined.to_csv(outdir / "table4_skill_scores.csv",
                    index=False, float_format="%.4f")

    print("\n===== TABLE 4: SKILL SCORES =====")
    with pd.option_context("display.max_columns", None, "display.width", 260):
        print(combined.to_string(index=False))
    print("=================================\n")

    # ---- Figure 4 ----
    fig4 = figure_4_skill_curves(cal_all, roc, val_df)
    save_line_drawing(fig4, outdir / "Figure_4.pdf")
    print(f"Wrote: {outdir / 'Figure_4.pdf'}")

    print(f"\n[Stage D] Done. Every value from the input CSVs. Outputs: {outdir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
