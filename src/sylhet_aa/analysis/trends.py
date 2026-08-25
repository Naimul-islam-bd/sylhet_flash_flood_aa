"""
Non-parametric trend tests used in hydrological time series.

References:
    Mann, H.B. (1945). Nonparametric tests against trend. Econometrica.
    Kendall, M.G. (1975). Rank Correlation Methods. Griffin, London.
    Sen, P.K. (1968). Estimates of the regression coefficient based on
        Kendall's tau. J. Am. Stat. Assoc. 63(324):1379-1389.
    Pettitt, A.N. (1979). A non-parametric approach to the change-point
        problem. J. R. Stat. Soc. C 28(2):126-135.
    Hamed, K.H. (2008). Trend detection in hydrologic data: The MK test
        under the scaling hypothesis. J. Hydrology 349(3-4):350-363.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def _norm_cdf(z: float) -> float:
    """Standard normal CDF via the error function (no scipy dependency)."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def mann_kendall(series: Sequence[float]) -> dict:
    """
    Mann-Kendall trend test with tie correction and continuity correction.

    Parameters
    ----------
    series : sequence of float
        Time-ordered values (missing values will be dropped).

    Returns
    -------
    dict with keys:
        trend     'increasing' / 'decreasing' / 'no significant trend' / 'n/a'
        S         Mann-Kendall S statistic
        Z         standard normal test statistic (continuity corrected)
        p_value   two-sided p-value
        n_used    number of non-missing observations
        note      informational message
    """
    x = np.asarray(series, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)

    if n < 8:
        return {"trend": "n/a", "S": float("nan"), "Z": float("nan"),
                "p_value": float("nan"), "n_used": int(n),
                "note": "fewer than 8 non-missing values"}

    # S statistic (sign of all pairwise differences)
    s = 0.0
    for i in range(n - 1):
        s += float(np.sum(np.sign(x[i + 1:] - x[i])))

    # Variance with tie correction
    _, counts = np.unique(x, return_counts=True)
    tie_term = float(np.sum(counts * (counts - 1) * (2 * counts + 5)))
    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0

    # Continuity-corrected Z
    if s > 0:
        z = (s - 1) / math.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / math.sqrt(var_s)
    else:
        z = 0.0

    p = 2.0 * (1.0 - _norm_cdf(abs(z)))

    if p < 0.05:
        trend = "increasing" if s > 0 else "decreasing"
    else:
        trend = "no significant trend"

    return {"trend": trend, "S": float(s), "Z": float(z),
            "p_value": float(p), "n_used": int(n), "note": ""}


def sens_slope(years: Sequence[float], values: Sequence[float]) -> float:
    """
    Sen's slope estimator (median of pairwise slopes; Theil-Sen).

    Returns slope in units of `values` per unit of `years` (typically per year).
    Returns nan if fewer than two valid pairs.
    """
    y = np.asarray(years, dtype=float)
    v = np.asarray(values, dtype=float)
    mask = ~np.isnan(v)
    y, v = y[mask], v[mask]

    n = len(v)
    if n < 2:
        return float("nan")

    slopes = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            dt = y[j] - y[i]
            if dt != 0:
                slopes.append((v[j] - v[i]) / dt)
    return float(np.median(slopes)) if slopes else float("nan")


def pettitt(series: Sequence[float]) -> dict:
    """
    Pettitt (1979) non-parametric change-point test.

    Returns
    -------
    dict with keys:
        K              test statistic
        change_index   0-based index into the input series (nan if n<10)
        p_value        approximate two-sided p-value
    """
    x = np.asarray(series, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)

    if n < 10:
        return {"K": float("nan"), "change_index": float("nan"),
                "p_value": float("nan")}

    # U statistic at each t: cumulative rank comparison. O(n^2) but n typically small.
    U = np.zeros(n)
    for t in range(1, n):
        s = 0
        for i in range(t + 1):
            for j in range(t + 1, n):
                s += np.sign(x[i] - x[j])
        U[t] = s

    K = float(np.max(np.abs(U)))
    tau = int(np.argmax(np.abs(U)))
    # Approximate asymptotic p-value (Pettitt 1979)
    p = 2.0 * math.exp(-6.0 * K ** 2 / (n ** 3 + n ** 2))
    p = min(1.0, p)
    return {"K": K, "change_index": tau, "p_value": p}
