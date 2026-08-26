"""
Stage C district-level exposure: per-district x per-event exposure metrics.

For each of the 4 Sylhet districts (Sylhet, Sunamganj, Habiganj,
Moulvibazar), compute exposed population + cropland/built-up/haor
flooded area per event. Produces Table 3c (7 events x 4 districts).

Optimized: does costly raster reprojection ONCE per event, then applies
district polygon masks to the reprojected result.

Usage:
    python scripts/06_run_stage_c_district.py \
        --pop data/raw/sylhet_worldpop_2020.tif \
        --landcover data/raw/sylhet_worldcover_2021.tif \
        --districts data/raw/sylhet_districts_gaul2.geojson \
        --outdir outputs/stage_c
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sylhet_aa.exposure import load_districts_geojson
from sylhet_aa.exposure.compute_exposure import reproject_to_match


EVENTS = [
    "ev_2017_apr", "ev_2019_jul", "ev_2020_jul",
    "ev_2022_may", "ev_2022_jun", "ev_2023_may", "ev_2024_jul",
]


def _rasterize_districts(districts, raster_path):
    """Return dict of district_name -> boolean mask on the given raster's grid."""
    import rasterio
    from rasterio.features import geometry_mask
    masks = {}
    with rasterio.open(raster_path) as src:
        for d in districts:
            m = ~geometry_mask(
                [d["geometry"].__geo_interface__],
                out_shape=(src.height, src.width),
                transform=src.transform,
                invert=False,
            )
            masks[d["name"]] = m
    return masks


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage C district-level exposure")
    ap.add_argument("--pop", required=True)
    ap.add_argument("--landcover", required=True)
    ap.add_argument("--districts", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--flood-dir", default="data/raw")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for p in (args.pop, args.landcover, args.districts):
        if not Path(p).exists():
            print(f"ERROR: {p} not found")
            return 1

    print(f"[Stage C-district] Loading districts ...")
    districts = load_districts_geojson(args.districts)
    print(f"  Found {len(districts)} districts: {[d['name'] for d in districts]}")

    print("[Stage C-district] Rasterizing district polygons ...")
    print("  ... onto population grid")
    pop_district_masks = _rasterize_districts(districts, args.pop)
    print("  ... onto worldcover grid")
    wc_district_masks = _rasterize_districts(districts, args.landcover)

    import rasterio
    with rasterio.open(args.pop) as src:
        pop = src.read(1).astype(np.float64)
        pop = np.where(np.isnan(pop) | (pop < 0), 0.0, pop)
    with rasterio.open(args.landcover) as src:
        wc = src.read(1)

    rows = []
    for ev in EVENTS:
        flood_path = Path(args.flood_dir) / f"{ev}_flood_extent.tif"
        if not flood_path.exists():
            print(f"[{ev}] flood extent missing, skipping.")
            continue

        print(f"\n[{ev}] reprojecting flood extent ...")
        flood_on_pop = reproject_to_match(flood_path, args.pop, "nearest") > 0
        flood_on_wc = reproject_to_match(flood_path, args.landcover, "nearest") > 0

        for d in districts:
            name = d["name"]
            pop_mask = pop_district_masks[name]
            wc_mask = wc_district_masks[name]

            in_flood_district = flood_on_pop & pop_mask
            exposed = float(np.sum(pop[in_flood_district]))
            total_district = float(np.sum(pop[pop_mask]))
            expo_frac = exposed / total_district if total_district > 0 else 0.0

            flood_in_dist_wc = flood_on_wc & wc_mask
            pixel_area_m2 = 100.0
            flooded_km2 = float(np.sum(flood_in_dist_wc)) * pixel_area_m2 / 1e6
            cropland_km2 = float(np.sum(flood_in_dist_wc & (wc == 40))) * pixel_area_m2 / 1e6
            built_up_km2 = float(np.sum(flood_in_dist_wc & (wc == 50))) * pixel_area_m2 / 1e6
            haor_km2 = float(np.sum(flood_in_dist_wc & (wc == 90))) * pixel_area_m2 / 1e6

            r = {
                "event_id": ev, "district": name,
                "exposed_population": int(round(exposed)),
                "total_population_district": int(round(total_district)),
                "exposure_fraction_pct": round(expo_frac * 100, 2),
                "flooded_km2": round(flooded_km2, 1),
                "cropland_km2": round(cropland_km2, 1),
                "built_up_km2": round(built_up_km2, 2),
                "haor_km2": round(haor_km2, 1),
            }
            rows.append(r)
            print(f"  {name:<15} exposed {r['exposed_population']:>10,} "
                  f"({r['exposure_fraction_pct']:>5.1f}%)  "
                  f"flood {r['flooded_km2']:>6.0f} km2  crop {r['cropland_km2']:>6.0f} km2")

    if not rows:
        return 1

    df = pd.DataFrame(rows)
    df.to_csv(outdir / "table3c_district_exposure.csv", index=False)
    print(f"\nSaved: {outdir / 'table3c_district_exposure.csv'}")

    pivot = df.pivot_table(index="event_id", columns="district",
                            values="exposed_population", aggfunc="first")
    pivot.to_csv(outdir / "table3c_pivot_exposed_pop.csv")
    print(f"Saved: {outdir / 'table3c_pivot_exposed_pop.csv'}")

    print("\n===== TABLE 3c pivot: exposed population per event per district =====")
    print(pivot.to_string())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
