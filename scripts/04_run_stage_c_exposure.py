"""
Stage C: exposure quantification for 7 flash flood events.

Overlays each event's S1 flood extent with WorldPop 2020 population and
ESA WorldCover 2021 land cover to produce:
  - Table 3a: exposed population per event
  - Table 3b: land cover breakdown per event

Usage:
    python scripts/04_run_stage_c_exposure.py \\
        --pop data/raw/sylhet_worldpop_2020.tif \\
        --landcover data/raw/sylhet_worldcover_2021.tif \\
        --outdir outputs/stage_c
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sylhet_aa.exposure import exposed_population, landcover_breakdown, WORLDCOVER_CLASSES  # noqa: E402


EVENTS = [
    "ev_2017_apr", "ev_2019_jul", "ev_2020_jul",
    "ev_2022_may", "ev_2022_jun", "ev_2023_may", "ev_2024_jul",
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage C: exposure quantification")
    ap.add_argument("--pop", required=True, help="WorldPop 2020 raster")
    ap.add_argument("--landcover", required=True, help="ESA WorldCover 2021 raster")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--flood-dir", default="data/raw",
                    help="Directory containing per-event flood_extent.tif files")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for p in (args.pop, args.landcover):
        if not Path(p).exists():
            print(f"ERROR: file not found: {p}")
            return 1

    pop_rows = []
    lc_rows = []

    for ev in EVENTS:
        flood_path = Path(args.flood_dir) / f"{ev}_flood_extent.tif"
        if not flood_path.exists():
            print(f"[Stage C] {ev}: flood extent missing at {flood_path}, skipping.")
            continue

        print(f"\n[Stage C] Processing {ev} ...")

        # Population exposure
        pop_result = exposed_population(flood_path, args.pop)
        exposed = int(round(pop_result["exposed_population"]))
        frac = pop_result["exposure_fraction"] * 100
        print(f"  Exposed population: {exposed:,}  ({frac:.1f}% of Sylhet Division)")

        # Landcover breakdown
        lc_result = landcover_breakdown(flood_path, args.landcover)
        total_km2 = lc_result["total_flooded_km2"]
        print(f"  Total flooded (WorldCover grid): {total_km2:.0f} km2")

        top_classes = sorted(lc_result["by_class_name_km2"].items(),
                              key=lambda kv: -kv[1])[:5]
        print("  Top 5 land cover classes flooded:")
        for name, km2 in top_classes:
            if km2 > 0:
                print(f"    {name:<35} {km2:>8.1f} km2")

        pop_rows.append({
            "event_id": ev,
            "exposed_population": exposed,
            "total_pop_in_region": int(round(pop_result["total_population_in_region"])),
            "exposure_fraction_pct": round(frac, 2),
        })
        lc_row = {"event_id": ev, "total_flooded_km2": round(total_km2, 1)}
        for code, name in WORLDCOVER_CLASSES.items():
            lc_row[f"{name}_km2"] = round(lc_result["by_class_km2"][code], 1)
        lc_rows.append(lc_row)

    # Save
    if pop_rows:
        pop_df = pd.DataFrame(pop_rows)
        pop_df.to_csv(outdir / "table3a_exposed_population.csv", index=False)
        print(f"\nSaved: {outdir / 'table3a_exposed_population.csv'}")
        print(pop_df.to_string(index=False))

    if lc_rows:
        lc_df = pd.DataFrame(lc_rows)
        lc_df.to_csv(outdir / "table3b_landcover_breakdown.csv", index=False)
        print(f"\nSaved: {outdir / 'table3b_landcover_breakdown.csv'}")

    print(f"\n[Stage C] Done. Outputs in: {outdir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
