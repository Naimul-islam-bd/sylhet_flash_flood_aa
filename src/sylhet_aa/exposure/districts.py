"""
District-level exposure computation.

Extends the exposure module with per-district masking using a vector
polygon file (GeoJSON) of Sylhet Division districts.

Approach: for each district polygon, mask the flood extent + population
+ landcover rasters, then compute exposure metrics.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import numpy as np


def load_districts_geojson(geojson_path: str | Path) -> list[dict]:
    """
    Load a GeoJSON FeatureCollection of district polygons.

    Returns a list of dicts each containing:
        name : district name (from ADM2_NAME property)
        geometry : shapely geometry object
    """
    try:
        from shapely.geometry import shape
    except ImportError as exc:
        raise ImportError("shapely required for district masking.") from exc

    with open(geojson_path, encoding="utf-8") as f:
        gj = json.load(f)

    if gj.get("type") != "FeatureCollection":
        raise ValueError(f"Expected FeatureCollection, got {gj.get('type')}")

    districts = []
    for feat in gj["features"]:
        props = feat.get("properties", {})
        # Try common admin-name fields (GAUL uses ADM2_NAME)
        name = (props.get("ADM2_NAME") or props.get("adm2_name")
                or props.get("NAME_2") or props.get("name") or "unknown")
        districts.append({
            "name": name,
            "geometry": shape(feat["geometry"]),
        })
    return districts


def mask_raster_by_polygon(raster_path: str | Path, geometry) -> np.ndarray:
    """
    Return the raster array masked to a polygon (values outside = 0).
    Preserves raster grid and returns the same-shape array.
    """
    try:
        import rasterio
        from rasterio.mask import mask
    except ImportError as exc:
        raise ImportError("rasterio required.") from exc

    with rasterio.open(raster_path) as src:
        try:
            out, _ = mask(src, [geometry.__geo_interface__],
                          crop=False, filled=True, nodata=0)
        except ValueError:
            # geometry does not overlap raster - return zero array
            out = np.zeros((src.count, src.height, src.width), dtype=src.dtypes[0])
    return out[0]  # single band


def district_exposure(district_name: str, geometry,
                       flood_raster_path: str | Path,
                       population_raster_path: str | Path,
                       worldcover_raster_path: str | Path | None = None) -> dict:
    """
    Compute exposure metrics for a single district.

    Returns dict with:
        district              : name
        exposed_population    : people flooded in this district
        total_population_district : total district population
        exposure_fraction     : exposed / total (0-1)
        flooded_km2           : flood area in this district
        cropland_km2          : flooded cropland area (if worldcover provided)
    """
    # Reproject flood to population grid
    from .compute_exposure import reproject_to_match

    try:
        import rasterio
    except ImportError as exc:
        raise ImportError("rasterio required.") from exc

    # Get flood mask on population grid
    flood_on_pop = reproject_to_match(flood_raster_path,
                                        population_raster_path,
                                        resampling="nearest") > 0

    # Get district mask on population grid
    with rasterio.open(population_raster_path) as pop_src:
        pop = pop_src.read(1)
        pop_meta = pop_src.meta
    pop = np.where(np.isnan(pop) | (pop < 0), 0.0, pop).astype(np.float64)

    # Rasterize district polygon onto population grid
    from rasterio.features import geometry_mask
    with rasterio.open(population_raster_path) as pop_src:
        district_mask_pop = ~geometry_mask(
            [geometry.__geo_interface__],
            out_shape=pop.shape,
            transform=pop_src.transform,
            invert=False,
        )

    exposed = float(np.sum(pop[flood_on_pop & district_mask_pop]))
    total_district_pop = float(np.sum(pop[district_mask_pop]))
    exposure_frac = exposed / total_district_pop if total_district_pop > 0 else 0.0

    result = {
        "district": district_name,
        "exposed_population": exposed,
        "total_population_district": total_district_pop,
        "exposure_fraction": exposure_frac,
    }

    # Optional: land cover breakdown per district
    if worldcover_raster_path is not None:
        flood_on_wc = reproject_to_match(flood_raster_path,
                                           worldcover_raster_path,
                                           resampling="nearest") > 0
        with rasterio.open(worldcover_raster_path) as wc_src:
            wc = wc_src.read(1)
            district_mask_wc = ~geometry_mask(
                [geometry.__geo_interface__],
                out_shape=wc.shape,
                transform=wc_src.transform,
                invert=False,
            )
        flood_in_district = flood_on_wc & district_mask_wc
        # Cropland = class 40, 10m pixels = 100 m2
        pixel_area_m2 = 100.0
        result["flooded_km2"] = float(np.sum(flood_in_district)) * pixel_area_m2 / 1e6
        result["cropland_km2"] = float(np.sum(flood_in_district & (wc == 40))) * pixel_area_m2 / 1e6
        result["built_up_km2"] = float(np.sum(flood_in_district & (wc == 50))) * pixel_area_m2 / 1e6
        result["haor_km2"] = float(np.sum(flood_in_district & (wc == 90))) * pixel_area_m2 / 1e6

    return result
