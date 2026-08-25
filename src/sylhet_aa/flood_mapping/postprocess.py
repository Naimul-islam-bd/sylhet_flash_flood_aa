"""
Sentinel-1 flood map accuracy assessment against a Sentinel-2 reference.

References:
    Cohen, J. (1960). A coefficient of agreement for nominal scales.
        Educ. Psychol. Meas. 20(1):37-46.
    Congalton, R.G. (1991). A review of assessing the accuracy of
        classifications of remotely sensed data. Remote Sens. Environ.
        37:35-46.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


def load_binary_raster(path: str | Path) -> np.ndarray:
    """
    Load a single-band GeoTIFF as a binary uint8 array (0 = non-water,
    1 = water). Requires rasterio.
    """
    try:
        import rasterio
    except ImportError as exc:
        raise ImportError(
            "rasterio is required for flood accuracy assessment. "
            "Install with: pip install rasterio"
        ) from exc

    with rasterio.open(path) as src:
        arr = src.read(1)
        nodata = src.nodata

    binary = (arr > 0).astype(np.uint8)
    if nodata is not None:
        binary[arr == nodata] = 0
    return binary


def confusion_matrix_binary(predicted: np.ndarray, reference: np.ndarray) -> tuple[int, int, int, int]:
    """Return (TP, FP, TN, FN). Class 1 = water/flood."""
    if predicted.shape != reference.shape:
        raise ValueError(
            f"Shape mismatch: predicted {predicted.shape} vs reference {reference.shape}. "
            f"Reproject the reference to the predicted grid before calling this."
        )
    p = predicted.astype(bool)
    r = reference.astype(bool)
    return (
        int(np.sum(p & r)),
        int(np.sum(p & ~r)),
        int(np.sum(~p & ~r)),
        int(np.sum(~p & r)),
    )


def kappa_coefficient(tp: int, fp: int, tn: int, fn: int) -> float:
    """Cohen's kappa coefficient of agreement."""
    total = tp + fp + tn + fn
    if total == 0:
        return float("nan")
    po = (tp + tn) / total
    marg_p = ((tp + fp) * (tp + fn) + (tn + fn) * (tn + fp)) / (total ** 2)
    if abs(1 - marg_p) < 1e-12:
        return float("nan")
    return (po - marg_p) / (1 - marg_p)


def accuracy_report(event_id: str, tp: int, fp: int, tn: int, fn: int,
                     kappa_target: float = 0.70,
                     overall_target: float = 0.85) -> dict:
    """Compute overall accuracy, producer's, user's, kappa; return a dict."""
    total = tp + fp + tn + fn
    overall = (tp + tn) / total if total else float("nan")
    producer = tp / (tp + fn) if (tp + fn) else float("nan")   # sensitivity
    user = tp / (tp + fp) if (tp + fp) else float("nan")       # precision
    kappa = kappa_coefficient(tp, fp, tn, fn)

    if kappa >= kappa_target and overall >= overall_target:
        verdict = "GOOD"
    elif kappa >= 0.5:
        verdict = "MARGINAL"
    else:
        verdict = "POOR - flag in Table 2"

    return {
        "event_id": event_id,
        "TP": tp, "FP": fp, "TN": tn, "FN": fn,
        "overall_accuracy": overall,
        "producer_accuracy": producer,
        "user_accuracy": user,
        "kappa": kappa,
        "verdict": verdict,
    }
