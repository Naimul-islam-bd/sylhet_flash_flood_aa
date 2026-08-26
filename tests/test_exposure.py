"""Unit tests for the exposure module."""

import pytest
import numpy as np

from sylhet_aa.exposure import WORLDCOVER_CLASSES


class TestWorldcoverClasses:
    def test_all_expected_classes_present(self):
        expected = {10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100}
        assert set(WORLDCOVER_CLASSES.keys()) == expected

    def test_cropland_class(self):
        assert WORLDCOVER_CLASSES[40] == "Cropland"

    def test_built_up_class(self):
        assert WORLDCOVER_CLASSES[50] == "Built-up"

    def test_water_class(self):
        assert WORLDCOVER_CLASSES[80] == "Permanent water bodies"


class TestReprojection:
    """Smoke tests requiring rasterio; skipped if not installed."""

    def test_import_exists(self):
        from sylhet_aa.exposure import reproject_to_match, exposed_population, landcover_breakdown
        assert callable(reproject_to_match)
        assert callable(exposed_population)
        assert callable(landcover_breakdown)
