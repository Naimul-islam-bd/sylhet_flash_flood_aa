"""
Integrity and sanity checks on loaded rainfall series.

Every analysis script calls these before doing science, so problems
(missing days, negative rainfall, unit mistakes) surface immediately.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def summarize_series(df: pd.DataFrame, name: str = "rainfall") -> dict[str, Any]:
    """
    Return a short dictionary summarising a daily rainfall DataFrame.
    """
    if not {"date", "precip_mm"}.issubset(df.columns):
        raise ValueError("DataFrame must have 'date' and 'precip_mm' columns.")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    years = df["date"].dt.year

    return {
        "name": name,
        "n_days": int(len(df)),
        "n_years": int(years.max() - years.min() + 1),
        "start_date": df["date"].min().date().isoformat(),
        "end_date": df["date"].max().date().isoformat(),
        "n_missing": int(df["precip_mm"].isna().sum()),
        "n_negative": int((df["precip_mm"] < 0).sum()),
        "annual_mean_mm": float(df.groupby(years)["precip_mm"].sum().mean()),
        "annual_min_mm": float(df.groupby(years)["precip_mm"].sum().min()),
        "annual_max_mm": float(df.groupby(years)["precip_mm"].sum().max()),
        "daily_max_mm": float(df["precip_mm"].max()),
    }


def check_rainfall_integrity(df: pd.DataFrame, name: str = "rainfall",
                              expected_min_annual_mm: float = 1000.0,
                              expected_max_annual_mm: float = 6000.0,
                              raise_on_fail: bool = False) -> tuple[bool, list[str]]:
    """
    Check for common data problems. Returns (ok, list_of_warnings).

    Warnings triggered:
      - Missing values present
      - Negative rainfall values
      - Annual totals outside plausible range for NE Bangladesh (1000-6000 mm)
      - Suspiciously large date gaps (> 2 days)
    """
    summary = summarize_series(df, name)
    problems: list[str] = []

    if summary["n_missing"] > 0:
        problems.append(f"{summary['n_missing']} missing values found.")

    if summary["n_negative"] > 0:
        problems.append(f"{summary['n_negative']} negative rainfall values found.")

    if summary["annual_mean_mm"] < expected_min_annual_mm:
        problems.append(
            f"Annual mean {summary['annual_mean_mm']:.0f} mm is below expected "
            f"minimum {expected_min_annual_mm:.0f} mm for NE Bangladesh. "
            f"Possible unit mistake or wrong region."
        )
    if summary["annual_mean_mm"] > expected_max_annual_mm:
        problems.append(
            f"Annual mean {summary['annual_mean_mm']:.0f} mm exceeds expected "
            f"maximum {expected_max_annual_mm:.0f} mm. Check for double-counting."
        )

    # Date gap check
    df = df.sort_values("date").reset_index(drop=True)
    diffs = df["date"].diff().dt.days.dropna()
    max_gap = int(diffs.max()) if len(diffs) else 0
    if max_gap > 2:
        problems.append(f"Largest inter-record gap is {max_gap} days (should be 1 for daily data).")

    ok = len(problems) == 0
    if not ok and raise_on_fail:
        raise ValueError(f"Integrity check failed for {name}: {problems}")

    return ok, problems


def print_summary(df: pd.DataFrame, name: str = "rainfall") -> None:
    """Convenience: print a summary and any integrity warnings."""
    s = summarize_series(df, name)
    ok, warnings = check_rainfall_integrity(df, name)

    print(f"--- {s['name']} ---")
    print(f"  Days       : {s['n_days']}")
    print(f"  Years      : {s['n_years']} ({s['start_date']} to {s['end_date']})")
    print(f"  Missing    : {s['n_missing']}")
    print(f"  Negatives  : {s['n_negative']}")
    print(f"  Annual mean: {s['annual_mean_mm']:.0f} mm  "
          f"(range {s['annual_min_mm']:.0f} - {s['annual_max_mm']:.0f})")
    print(f"  Daily max  : {s['daily_max_mm']:.1f} mm")
    print(f"  Integrity  : {'OK' if ok else 'WARNINGS'}")
    for w in warnings:
        print(f"    - {w}")
