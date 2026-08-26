"""Exposure quantification (Stage C) - population and land cover intersection with flood extents."""

from .compute_exposure import (
    reproject_to_match,
    exposed_population,
    landcover_breakdown,
    WORLDCOVER_CLASSES,
)

__all__ = [
    "reproject_to_match",
    "exposed_population",
    "landcover_breakdown",
    "WORLDCOVER_CLASSES",
]
