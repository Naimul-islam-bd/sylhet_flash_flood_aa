"""
ETCCDI extreme precipitation indices (Zhang et al. 2011, WIREs Climate Change).

Computed annually from daily rainfall:
    PRCPTOT    annual total wet-day precipitation (mm)
    RX1day     max 1-day precipitation (mm)
    RX5day     max 5-day precipitation (mm)
    R95p       total precip on days above 95th percentile of wet days (mm)
    R99p       total precip on days above 99th percentile of wet days (mm)
    SDII       simple daily intensity index (mm/wet day)
    CDD        max consecutive dry days
    CWD        max consecutive wet days

Also computes the season-specific total (default: pre-monsoon Mar-May).

Percentiles for R95p / R99p use a WMO-standard 1981-2010 baseline (30 years).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import (
    WET_DAY_THRESHOLD_MM, PRE_MONSOON_MONTHS,
    BASELINE_START, BASELINE_END,
)


INDEX_COLUMNS = [
    "PRCPTOT", "RX1day", "RX5day", "R95p", "R99p",
    "SDII", "CDD", "CWD", "premonsoon_mm",
]


def _consecutive_runs(condition):
    """Lengths of consecutive True runs in a boolean array."""
    runs = []
    count = 0
    for c in condition:
        if c:
            count += 1
        else:
            if count > 0:
                runs.append(count)
                count = 0
    if count > 0:
        runs.append(count)
    return runs


def compute_indices_per_year(
    daily_df: pd.DataFrame,
    precip_col: str = "precip_mm",
    date_col: str = "date",
    baseline_start: int = BASELINE_START,
    baseline_end: int = BASELINE_END,
    season_months: tuple[int, ...] = PRE_MONSOON_MONTHS,
) -> tuple[pd.DataFrame, float, float]:
    """
    Compute all ETCCDI indices per calendar year.

    Returns
    -------
    (indices_df, q95, q99)
        indices_df : DataFrame with columns ['year', ...INDEX_COLUMNS]
        q95, q99   : wet-day percentiles from the baseline (mm)
    """
    df = daily_df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)
    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month

    # Baseline percentiles from wet days only
    base = df[(df["year"] >= baseline_start) & (df["year"] <= baseline_end)]
    wet_base = base[base[precip_col] >= WET_DAY_THRESHOLD_MM][precip_col]
    if len(wet_base) < 30:
        q95 = float("nan"); q99 = float("nan")
    else:
        q95 = float(np.percentile(wet_base, 95))
        q99 = float(np.percentile(wet_base, 99))

    records = []
    for year, g in df.groupby("year"):
        vals = g[precip_col].values
        wet = vals >= WET_DAY_THRESHOLD_MM

        prcptot = float(np.sum(vals[wet])) if wet.any() else 0.0
        rx1 = float(np.max(vals)) if len(vals) else float("nan")
        rx5 = float(pd.Series(vals).rolling(5).sum().max()) if len(vals) >= 5 else float("nan")
        r95p = float(np.sum(vals[vals > q95])) if not np.isnan(q95) else float("nan")
        r99p = float(np.sum(vals[vals > q99])) if not np.isnan(q99) else float("nan")
        sdii = float(np.mean(vals[wet])) if wet.any() else 0.0

        cdd = max(_consecutive_runs(vals < WET_DAY_THRESHOLD_MM), default=0)
        cwd = max(_consecutive_runs(wet), default=0)

        season_mask = g["month"].isin(season_months).values
        season_total = float(np.sum(vals[season_mask])) if season_mask.any() else 0.0

        records.append({
            "year": int(year),
            "PRCPTOT": prcptot, "RX1day": rx1, "RX5day": rx5,
            "R95p": r95p, "R99p": r99p, "SDII": sdii,
            "CDD": int(cdd), "CWD": int(cwd),
            "premonsoon_mm": season_total,
        })

    return pd.DataFrame(records), q95, q99


def run_all_trend_tests(annual_df: pd.DataFrame) -> pd.DataFrame:
    """
    Run Mann-Kendall + Sen's slope + Pettitt on every ETCCDI index in
    an annual DataFrame. Returns a summary DataFrame suitable for Table 1.
    """
    from .trends import mann_kendall, sens_slope, pettitt

    years = annual_df["year"].values
    rows = []
    for col in INDEX_COLUMNS:
        vals = annual_df[col].values
        mk = mann_kendall(vals)
        slope = sens_slope(years, vals)
        pt = pettitt(vals)
        if np.isnan(pt["change_index"]):
            change_year = float("nan")
        else:
            change_year = int(years[int(pt["change_index"])])
        rows.append({
            "index": col,
            "n_years": mk["n_used"],
            "mean": float(np.nanmean(vals)),
            "MK_S": mk["S"],
            "MK_Z": mk["Z"],
            "MK_p": mk["p_value"],
            "trend": mk["trend"],
            "Sens_slope_per_year": slope,
            "Pettitt_K": pt["K"],
            "Pettitt_change_year": change_year,
            "Pettitt_p": pt["p_value"],
        })
    return pd.DataFrame(rows)
