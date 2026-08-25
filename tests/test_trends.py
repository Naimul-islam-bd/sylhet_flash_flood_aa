"""Unit tests for the trends module."""

import math

import numpy as np
import pytest

from sylhet_aa.analysis.trends import mann_kendall, sens_slope, pettitt


class TestMannKendall:
    def test_strong_increasing_trend(self):
        x = list(range(1, 51))    # perfectly monotonic
        result = mann_kendall(x)
        assert result["trend"] == "increasing"
        assert result["S"] > 0
        assert result["Z"] > 0
        assert result["p_value"] < 0.001

    def test_strong_decreasing_trend(self):
        x = list(range(50, 0, -1))
        result = mann_kendall(x)
        assert result["trend"] == "decreasing"
        assert result["S"] < 0
        assert result["Z"] < 0
        assert result["p_value"] < 0.001

    def test_no_trend_random(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=100)
        result = mann_kendall(x)
        assert result["trend"] == "no significant trend"

    def test_short_series(self):
        result = mann_kendall([1, 2, 3])
        assert result["trend"] == "n/a"
        assert math.isnan(result["S"])

    def test_handles_nans(self):
        x = [1, 2, np.nan, 4, 5, 6, np.nan, 8, 9, 10]
        result = mann_kendall(x)
        assert result["n_used"] == 8
        assert result["trend"] == "increasing"


class TestSensSlope:
    def test_slope_of_perfect_line(self):
        years = list(range(2000, 2020))
        vals = [2.5 * y - 4995 for y in years]     # slope = 2.5
        slope = sens_slope(years, vals)
        assert abs(slope - 2.5) < 1e-9

    def test_slope_negative(self):
        years = list(range(2000, 2020))
        vals = [-3.0 * y + 6100 for y in years]
        slope = sens_slope(years, vals)
        assert abs(slope - (-3.0)) < 1e-9

    def test_slope_ignores_nans(self):
        years = list(range(2000, 2020))
        vals = [2.5 * y - 4995 if i % 3 else float("nan")
                for i, y in enumerate(years)]
        slope = sens_slope(years, vals)
        assert abs(slope - 2.5) < 1e-9

    def test_slope_of_short_series(self):
        assert math.isnan(sens_slope([2000], [5.0]))


class TestPettitt:
    def test_step_change_detected(self):
        rng = np.random.default_rng(1)
        # 50 values around 10, then 50 values around 20 -> clear change point at index 50
        x = np.concatenate([rng.normal(10, 1, 50), rng.normal(20, 1, 50)])
        result = pettitt(x)
        assert not math.isnan(result["K"])
        assert 45 <= result["change_index"] <= 55
        assert result["p_value"] < 0.05

    def test_no_change(self):
        rng = np.random.default_rng(2)
        x = rng.normal(0, 1, 100)
        result = pettitt(x)
        assert not math.isnan(result["K"])
        assert result["p_value"] > 0.05

    def test_short_series(self):
        result = pettitt(list(range(5)))
        assert math.isnan(result["K"])
