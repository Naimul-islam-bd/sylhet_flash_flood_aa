"""
Rainfall trigger threshold derivation.

Given daily rainfall and a catalogue of documented flash flood events,
sweep candidate thresholds across multiple accumulation windows and
compute contingency-table skill scores for each.

Used by scripts/03_run_stage_d_thresholds.py.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import ACCUMULATION_WINDOWS_DAYS, EVENT_HALO_DAYS
from .skill import contingency, skill_scores


def antecedent_series(rain_df: pd.DataFrame, window: int,
                       precip_col: str = "precip_mm") -> np.ndarray:
    """Rolling-sum antecedent rainfall over `window` days."""
    return rain_df[precip_col].rolling(window, min_periods=1).sum().values


def build_event_labels(
    rain_df: pd.DataFrame,
    events_df: pd.DataFrame,
    halo_days: int = EVENT_HALO_DAYS,
    date_col: str = "date",
) -> np.ndarray:
    """
    Return a boolean array aligned with rain_df rows: True if the row falls
    within halo_days of any documented event (inclusive of event start to
    end range, extended by halo_days on both sides).
    """
    labels = np.zeros(len(rain_df), dtype=bool)
    dates = rain_df[date_col].values.astype("datetime64[D]")
    halo = np.timedelta64(halo_days, "D")
    for _, ev in events_df.iterrows():
        start = np.datetime64(ev["event_date"].date()) - halo
        end = np.datetime64(ev["end_date"].date()) + halo
        labels |= (dates >= start) & (dates <= end)
    return labels


def sweep_thresholds(
    rain_df: pd.DataFrame,
    labels: np.ndarray,
    seasonal_mask: np.ndarray | None = None,
    windows: tuple[int, ...] = ACCUMULATION_WINDOWS_DAYS,
    percentiles: np.ndarray | None = None,
    precip_col: str = "precip_mm",
) -> pd.DataFrame:
    """
    For every (window, threshold) combination, compute contingency and
    skill scores. Returns a long-format DataFrame.
    """
    if percentiles is None:
        percentiles = np.arange(50, 99.6, 0.5)

    if seasonal_mask is None:
        seasonal_mask = np.ones(len(rain_df), dtype=bool)

    rows = []
    for w in windows:
        accum = antecedent_series(rain_df, w, precip_col)
        wet_days = accum[(accum >= 1.0) & seasonal_mask]
        if len(wet_days) < 30:
            continue

        thresh_values = np.percentile(wet_days, percentiles)
        thresh_values = np.unique(np.round(thresh_values, 1))

        for v in thresh_values:
            pred = (accum >= v) & seasonal_mask
            act = labels & seasonal_mask
            H, F, M, C = contingency(pred, act)
            s = skill_scores(H, F, M, C)
            rows.append({
                "window_days": int(w), "threshold_mm": float(v),
                "H": H, "F": F, "M": M, "C": C, **s,
            })
    return pd.DataFrame(rows)


def pick_optimum(sweep_df: pd.DataFrame, criterion: str = "CSI") -> pd.DataFrame:
    """Row with max value of `criterion` per window."""
    if sweep_df.empty:
        return sweep_df
    best = sweep_df.loc[sweep_df.groupby("window_days")[criterion].idxmax()].copy()
    return best.reset_index(drop=True)


def roc_points(sweep_df: pd.DataFrame) -> pd.DataFrame:
    """Extract ROC coordinates (FPR, POD) per window, ordered by threshold."""
    df = sweep_df.sort_values(["window_days", "threshold_mm"], ascending=[True, False])
    return df[["window_days", "threshold_mm", "FPR", "POD"]].copy()


def auc_per_window(roc_df: pd.DataFrame) -> pd.DataFrame:
    """AUC by trapezoidal rule per window."""
    trap = getattr(np, "trapezoid", None) or getattr(np, "trapz")
    out = []
    for w, g in roc_df.groupby("window_days"):
        g = g.sort_values("FPR")
        x = g["FPR"].values; y = g["POD"].values
        mask = ~np.isnan(x) & ~np.isnan(y)
        x = x[mask]; y = y[mask]
        auc = float(trap(y, x)) if len(x) >= 2 else float("nan")
        out.append({"window_days": int(w), "AUC": auc})
    return pd.DataFrame(out)
