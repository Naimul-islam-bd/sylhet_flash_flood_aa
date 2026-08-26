"""Exposure quantification (Stage C) - population and land cover intersection with flood extents."""

from .compute_exposure import (
    reproject_to_match,
    exposed_population,
    landcover_breakdown,
    WORLDCOVER_CLASSES,
)
from .districts import (
    load_districts_geojson,
    mask_raster_by_polygon,
    district_exposure,
)

__all__ = [
    "reproject_to_match",
    "exposed_population",
    "landcover_breakdown",
    "WORLDCOVER_CLASSES",
    "load_districts_geojson",
    "mask_raster_by_polygon",
    "district_exposure",
]
