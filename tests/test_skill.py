"""Unit tests for the skill scores module."""

import math

import numpy as np
import pytest

from sylhet_aa.analysis.skill import contingency, skill_scores, block_bootstrap_ci


class TestContingency:
    def test_perfect_forecast(self):
        pred = [True, True, False, False]
        act = [True, True, False, False]
        H, F, M, C = contingency(pred, act)
        assert (H, F, M, C) == (2, 0, 0, 2)

    def test_all_wrong(self):
        pred = [True, True, False, False]
        act = [False, False, True, True]
        H, F, M, C = contingency(pred, act)
        assert (H, F, M, C) == (0, 2, 2, 0)

    def test_shape_mismatch_raises(self):
        with pytest.raises(ValueError):
            contingency([True, False], [True, False, True])


class TestSkillScores:
    def test_perfect_scores(self):
        s = skill_scores(H=10, F=0, M=0, C=10)
        assert s["POD"] == 1.0
        assert s["FAR"] == 0.0
        assert s["CSI"] == 1.0
        assert s["HSS"] == 1.0
        assert s["ETS"] == 1.0
        assert s["FPR"] == 0.0

    def test_no_skill_random(self):
        # Equal hits, misses, false alarms, correct negatives = pure chance
        s = skill_scores(H=25, F=25, M=25, C=25)
        assert abs(s["POD"] - 0.5) < 1e-9
        assert abs(s["FAR"] - 0.5) < 1e-9
        assert abs(s["CSI"] - (25 / 75)) < 1e-9
        assert abs(s["HSS"]) < 1e-9      # no skill
        assert abs(s["ETS"]) < 1e-9      # no skill

    def test_zero_denominators_return_nan(self):
        s = skill_scores(H=0, F=0, M=0, C=100)
        assert math.isnan(s["POD"])
        assert math.isnan(s["FAR"])
        assert math.isnan(s["CSI"])

    def test_known_example_from_wilks(self):
        # From Wilks (2011) chapter 8, made-up worked example
        # H=82, F=38, M=23, C=222 -> POD=0.781, FAR=0.317, CSI=0.573
        s = skill_scores(H=82, F=38, M=23, C=222)
        assert abs(s["POD"] - 82 / 105) < 1e-9
        assert abs(s["FAR"] - 38 / 120) < 1e-9
        assert abs(s["CSI"] - 82 / (82 + 23 + 38)) < 1e-9


class TestBlockBootstrap:
    def test_reproducibility_with_seed(self):
        rng = np.random.default_rng(0)
        accum = rng.exponential(5, 500)
        labels = rng.random(500) < 0.1
        r1 = block_bootstrap_ci(accum, labels, threshold=10.0, n_iter=50, seed=42)
        r2 = block_bootstrap_ci(accum, labels, threshold=10.0, n_iter=50, seed=42)
        assert r1 == r2

    def test_returns_confidence_bounds(self):
        rng = np.random.default_rng(0)
        accum = rng.exponential(5, 500)
        labels = rng.random(500) < 0.1
        r = block_bootstrap_ci(accum, labels, threshold=10.0, n_iter=50)
        for key in ("POD", "FAR", "CSI", "HSS", "ETS"):
            assert f"{key}_lo" in r
            assert f"{key}_hi" in r
