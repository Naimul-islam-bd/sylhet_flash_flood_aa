"""
Load daily rainfall and event catalogue CSVs into DataFrames.

Supports flexible column names because different GEE exports and manual
datasets use slightly different conventions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


DATE_CANDIDATES = ("date", "time", "system:time_start", "day", "datetime")
PRECIP_CANDIDATES = (
    "precipitation_mm", "precipitation", "precip", "precip_mm",
    "rainfall", "rain_mm", "chirps", "value", "mean", "tp",
    "total_precipitation_sum", "precipitation_m",
)


def _guess_column(columns: Iterable[str], candidates: Iterable[str]) -> str | None:
    """Case-insensitive exact match first, then partial match."""
    lower = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand in lower:
            return lower[cand]
    for c in columns:
        for cand in candidates:
            if cand in c.lower():
                return c
    return None


def load_daily_rainfall(path: str | Path) -> pd.DataFrame:
    """
    Load a daily rainfall CSV.

    Returns a DataFrame with columns ['date', 'precip_mm'] where 'date' is
    datetime64 and 'precip_mm' is float in millimetres per day.

    Automatic handling:
      - ERA5-Land exports precipitation in metres; values are multiplied
        by 1000 when the daily mean is unrealistically small.
      - Values marginally below zero (a known ERA5 daily-aggregation
        numerical artifact from ECMWF's hourly-to-daily rounding) are
        clipped to zero, with the count printed for transparency.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Rainfall CSV not found: {path}")

    df = pd.read_csv(path)
    date_col = _guess_column(df.columns, DATE_CANDIDATES)
    precip_col = _guess_column(df.columns, PRECIP_CANDIDATES)

    if date_col is None or precip_col is None:
        raise ValueError(
            f"Could not identify date/precipitation columns in {path.name}. "
            f"Found columns: {list(df.columns)}. "
            f"Rename them to 'date' and 'precipitation_mm' and retry."
        )

    out = df[[date_col, precip_col]].rename(
        columns={date_col: "date", precip_col: "precip_mm"}
    )
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out = out.dropna(subset=["date", "precip_mm"]).sort_values("date").reset_index(drop=True)

    # ERA5-Land unit fix: total_precipitation_sum is stored in metres.
    # If the daily mean is less than 0.1 mm, assume metres and convert.
    if out["precip_mm"].mean() < 0.1 and out["precip_mm"].max() < 1.0:
        out["precip_mm"] = out["precip_mm"] * 1000.0

    # ERA5-Land numerical artifact: hourly-to-daily aggregation can produce
    # marginally negative values (typically < 1e-5 mm) from float rounding.
    # Clip to zero and report the count. This does not change the physical
    # meaning: precipitation is a positive-only quantity.
    n_negative = int((out["precip_mm"] < 0).sum())
    if n_negative > 0:
        max_negative = float(out["precip_mm"].min())
        print(f"  Note: clipped {n_negative} marginally negative values to 0 "
              f"(min was {max_negative:.6f} mm; ERA5 numerical artifact).")
        out["precip_mm"] = out["precip_mm"].clip(lower=0.0)

    return out


def load_events_catalogue(path: str | Path) -> pd.DataFrame:
    """
    Load the flash flood events catalogue.

    Required columns: 'event_date' (YYYY-MM-DD).
    Optional columns: 'end_date', 'source', 'notes', 'affected_district'.

    If 'end_date' is missing or blank, it defaults to 'event_date'.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Events catalogue not found: {path}")

    df = pd.read_csv(path, comment="#")
    if "event_date" not in df.columns:
        raise ValueError(f"Events CSV missing required column 'event_date'. Found: {list(df.columns)}")

    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    if "end_date" in df.columns:
        df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
    else:
        df["end_date"] = pd.NaT
    df["end_date"] = df["end_date"].fillna(df["event_date"])

    df = df.dropna(subset=["event_date"]).sort_values("event_date").reset_index(drop=True)
    return df
