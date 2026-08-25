"""
Contingency-table forecast verification metrics.

References:
    Wilks, D.S. (2011). Statistical Methods in the Atmospheric Sciences,
        3rd ed. Academic Press. Chapter 8.
    Jolliffe, I.T. and Stephenson, D.B. (2012). Forecast Verification: A
        Practitioner's Guide in Atmospheric Science, 2nd ed. Wiley.
    Kunsch, H.R. (1989). The jackknife and the bootstrap for general
        stationary observations. Annals of Statistics 17:1217-1241.

2x2 contingency table for a binary event (Event vs No event):

                            Event      No event
    Rain >= threshold       Hit (H)    False alarm (F)
    Rain <  threshold       Miss (M)   Correct negative (C)

Skill scores computed:
    POD (Probability of Detection)  = H / (H + M)
    FAR (False Alarm Ratio)         = F / (H + F)
    CSI (Critical Success Index)    = H / (H + M + F)
    HSS (Heidke Skill Score)        = 2(HC - MF) / [(H+M)(M+C)+(H+F)(F+C)]
    ETS (Equitable Threat Score)    = (H - Hrand) / (H + M + F - Hrand)
                                       where Hrand = (H+M)(H+F)/N
    FPR (False Positive Rate)       = F / (F + C)     [for ROC]
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from ..config import DECORR_BLOCK_DAYS, N_BOOTSTRAP


def contingency(predicted_pos: Sequence[bool], actual_pos: Sequence[bool]) -> tuple[int, int, int, int]:
    """Return (H, F, M, C) from two boolean arrays."""
    p = np.asarray(predicted_pos, dtype=bool)
    a = np.asarray(actual_pos, dtype=bool)
    if p.shape != a.shape:
        raise ValueError(f"Shape mismatch: predicted {p.shape} vs actual {a.shape}")
    H = int(np.sum(p & a))
    F = int(np.sum(p & ~a))
    M = int(np.sum(~p & a))
    C = int(np.sum(~p & ~a))
    return H, F, M, C


def skill_scores(H: int, F: int, M: int, C: int) -> dict:
    """Compute POD, FAR, CSI, HSS, ETS, FPR from a 2x2 contingency table."""
    total = H + F + M + C

    def safe_div(num, den):
        return num / den if den else float("nan")

    pod = safe_div(H, H + M)
    far = safe_div(F, H + F)
    csi = safe_div(H, H + M + F)
    fpr = safe_div(F, F + C)

    if (H + M) and (M + C) and (H + F) and (F + C):
        num = 2.0 * (H * C - M * F)
        den = (H + M) * (M + C) + (H + F) * (F + C)
        hss = num / den if den else float("nan")
    else:
        hss = float("nan")

    if total and (H + M + F):
        Hrand = (H + M) * (H + F) / total
        ets_den = H + M + F - Hrand
        ets = (H - Hrand) / ets_den if ets_den else float("nan")
    else:
        ets = float("nan")

    return {"POD": pod, "FAR": far, "CSI": csi, "HSS": hss, "ETS": ets, "FPR": fpr}


def _block_bootstrap_indices(n: int, block_len: int, n_iter: int, rng):
    """Yield index arrays of length n produced by circular block bootstrap."""
    starts_per_iter = math.ceil(n / block_len)
    for _ in range(n_iter):
        starts = rng.integers(0, n - block_len + 1, size=starts_per_iter)
        idx = np.concatenate([np.arange(s, s + block_len) for s in starts])[:n]
        yield idx


def block_bootstrap_ci(
    accum: Sequence[float],
    labels: Sequence[bool],
    threshold: float,
    block_len: int = DECORR_BLOCK_DAYS,
    n_iter: int = N_BOOTSTRAP,
    seed: int = 42,
    ci: float = 0.95,
) -> dict:
    """
    Block bootstrap 95% confidence intervals for POD, FAR, CSI, HSS, ETS
    at a given threshold.

    Uses non-overlapping block bootstrap (Kunsch 1989) with block length
    equal to the decorrelation scale of daily rainfall to avoid
    over-confident intervals from naive resampling.
    """
    rng = np.random.default_rng(seed)
    accum = np.asarray(accum, dtype=float)
    labels = np.asarray(labels, dtype=bool)
    n = len(accum)

    scores = {"POD": [], "FAR": [], "CSI": [], "HSS": [], "ETS": []}
    for idx in _block_bootstrap_indices(n, block_len, n_iter, rng):
        pred = accum[idx] >= threshold
        act = labels[idx]
        H, F, M, C = contingency(pred, act)
        s = skill_scores(H, F, M, C)
        for k in scores:
            scores[k].append(s[k])

    alpha_lo = (1 - ci) / 2 * 100
    alpha_hi = 100 - alpha_lo
    out = {}
    for k, v in scores.items():
        arr = np.asarray(v, dtype=float)
        arr = arr[~np.isnan(arr)]
        if len(arr) == 0:
            out[k + "_lo"] = float("nan")
            out[k + "_hi"] = float("nan")
        else:
            out[k + "_lo"] = float(np.percentile(arr, alpha_lo))
            out[k + "_hi"] = float(np.percentile(arr, alpha_hi))
    return out
