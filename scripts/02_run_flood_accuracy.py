"""
Stage B: Sentinel-1 flood map accuracy assessment against a Sentinel-2 reference.

Both rasters must be co-registered (same CRS, same grid). If not, first run:

    gdalwarp -tr 30 30 -te <bounds> -r near ref.tif ref_resampled.tif

Usage:
    python scripts/02_run_flood_accuracy.py \\
        --predicted data/raw/ev_2022_jun_flood_extent.tif \\
        --reference data/raw/ev_2022_jun_s2_reference_water.tif \\
        --event_id ev_2022_jun \\
        --outdir outputs/stage_b
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sylhet_aa.flood_mapping import (   # noqa: E402
    load_binary_raster,
    confusion_matrix_binary,
    accuracy_report,
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage B: Sentinel-1 flood accuracy")
    ap.add_argument("--predicted", required=True, help="S1 flood raster (GeoTIFF)")
    ap.add_argument("--reference", required=True, help="S2 MNDWI water raster (GeoTIFF)")
    ap.add_argument("--event_id", required=True, help="Event label used in the report")
    ap.add_argument("--outdir", required=True, help="Output directory")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for p in (args.predicted, args.reference):
        if not Path(p).exists():
            print(f"ERROR: file not found: {p}")
            return 1

    print(f"[Stage B] Loading rasters for event: {args.event_id}")
    pred = load_binary_raster(args.predicted)
    ref = load_binary_raster(args.reference)

    tp, fp, tn, fn = confusion_matrix_binary(pred, ref)
    result = accuracy_report(args.event_id, tp, fp, tn, fn)

    # Print human-readable report
    print(f"\n=== Accuracy report: {args.event_id} ===")
    print("Confusion matrix (rows: predicted, columns: reference)")
    print("                   Water_ref   Non-water_ref")
    print(f"Water_pred      {tp:>12d}    {fp:>12d}")
    print(f"Non-water_pred  {fn:>12d}    {tn:>12d}")
    print(f"Total pixels           : {tp + fp + tn + fn}")
    print(f"Overall accuracy       : {result['overall_accuracy']:.4f}")
    print(f"Producer's accuracy    : {result['producer_accuracy']:.4f}  (recall for water)")
    print(f"User's accuracy        : {result['user_accuracy']:.4f}  (precision for water)")
    print(f"Kappa coefficient      : {result['kappa']:.4f}")
    print(f"Assessment             : {result['verdict']}")

    out_csv = outdir / f"accuracy_{args.event_id}.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(result.keys()))
        w.writeheader()
        w.writerow(result)
    print(f"\nSaved: {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
