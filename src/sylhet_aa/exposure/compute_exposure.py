"""
Exposure quantification: overlay flood extent rasters with population
(WorldPop 2020) and land cover (ESA WorldCover 2021) to compute per-event
exposure metrics.

Approach: reproject flood extent to the population/landcover grid using
nearest neighbour (preserves binary values), then aggregate. This ensures
population totals are preserved without oversampling artifacts.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


# ESA WorldCover v200 class codes
WORLDCOVER_CLASSES = {
    10: "Tree cover",
    20: "Shrubland",
    30: "Grassland",
    40: "Cropland",
    50: "Built-up",
    60: "Bare / sparse vegetation",
    70: "Snow and ice",
    80: "Permanent water bodies",
    90: "Herbaceous wetland",
    95: "Mangroves",
    100: "Moss and lichen",
}


def reproject_to_match(source_path: str | Path, target_path: str | Path,
                       resampling: str = "nearest") -> np.ndarray:
    """
    Reproject a source raster onto the grid of a target raster.

    Returns a 2D numpy array with the same shape as the target raster
    band 1. Requires rasterio.
    """
    try:
        import rasterio
        from rasterio.warp import reproject, Resampling
    except ImportError as exc:
        raise ImportError("rasterio required for exposure computation.") from exc

    resampling_enum = {
        "nearest": Resampling.nearest,
        "bilinear": Resampling.bilinear,
        "average": Resampling.average,
        "sum": Resampling.sum,
        "mode": Resampling.mode,
    }[resampling]

    with rasterio.open(target_path) as tgt:
        target_transform = tgt.transform
        target_crs = tgt.crs
        target_shape = (tgt.height, tgt.width)

    with rasterio.open(source_path) as src:
        src_data = src.read(1)
        src_transform = src.transform
        src_crs = src.crs
        src_dtype = src.dtypes[0]

    dst = np.zeros(target_shape, dtype=src_dtype)
    reproject(
        source=src_data,
        destination=dst,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=target_transform,
        dst_crs=target_crs,
        resampling=resampling_enum,
    )
    return dst


def exposed_population(flood_raster_path: str | Path,
                       population_raster_path: str | Path) -> dict:
    """
    Compute population exposed to a flood event.

    Flood raster is binary (0/1). Population raster is per-pixel count
    (people per 100m pixel from WorldPop).

    Method: reproject flood extent to the population raster grid using
    nearest-neighbour (preserves binary values); sum population where
    flood = 1.
    """
    try:
        import rasterio
    except ImportError as exc:
        raise ImportError("rasterio required.") from exc

    # Reproject flood onto population grid (nearest to preserve binary)
    flood_on_pop = reproject_to_match(flood_raster_path,
                                        population_raster_path,
                                        resampling="nearest")

    with rasterio.open(population_raster_path) as pop_src:
        pop = pop_src.read(1)

    # Handle NoData in population (WorldPop uses negative fill for no-data)
    pop = np.where(np.isnan(pop) | (pop < 0), 0.0, pop).astype(np.float64)

    flood_mask = flood_on_pop > 0
    exposed = float(np.sum(pop[flood_mask]))
    total_area_pop = float(np.sum(pop))

    return {
        "total_population_in_region": total_area_pop,
        "exposed_population": exposed,
        "exposure_fraction": (exposed / total_area_pop) if total_area_pop > 0 else float("nan"),
    }


def landcover_breakdown(flood_raster_path: str | Path,
                         worldcover_raster_path: str | Path,
                         pixel_area_m2: float = 100.0) -> dict:
    """
    Compute area of flood extent by land cover class.

    WorldCover pixels are 10m x 10m = 100 m2. Reproject flood extent to
    the WorldCover 10m grid (nearest-neighbour), then count flood pixels
    per class. Multiply by pixel_area_m2 to get area in m2.

    Returns dict with:
        by_class_km2         : dict {class_code: area_km2}
        by_class_name_km2    : dict {class_name: area_km2}
        total_flooded_km2    : total flooded area (km2)
    """
    try:
        import rasterio
    except ImportError as exc:
        raise ImportError("rasterio required.") from exc

    # Reproject flood to WorldCover 10m grid using nearest neighbour
    flood_on_wc = reproject_to_match(flood_raster_path,
                                       worldcover_raster_path,
                                       resampling="nearest")

    with rasterio.open(worldcover_raster_path) as wc_src:
        wc = wc_src.read(1)

    flood_mask = flood_on_wc > 0
    total_pixels = int(np.sum(flood_mask))
    total_km2 = total_pixels * pixel_area_m2 / 1e6

    result_code = {}
    result_name = {}
    for code, name in WORLDCOVER_CLASSES.items():
        cls_mask = flood_mask & (wc == code)
        n_pix = int(np.sum(cls_mask))
        area_km2 = n_pix * pixel_area_m2 / 1e6
        result_code[code] = area_km2
        result_name[name] = area_km2

    return {
        "total_flooded_km2": total_km2,
        "by_class_km2": result_code,
        "by_class_name_km2": result_name,
    }
