"""Statistical analysis functions."""

from .trends import mann_kendall, sens_slope, pettitt
from .extremes import compute_indices_per_year, INDEX_COLUMNS
from .thresholds import antecedent_series, sweep_thresholds, pick_optimum, roc_points, auc_per_window
from .skill import contingency, skill_scores, block_bootstrap_ci

__all__ = [
    "mann_kendall",
    "sens_slope",
    "pettitt",
    "compute_indices_per_year",
    "INDEX_COLUMNS",
    "antecedent_series",
    "sweep_thresholds",
    "pick_optimum",
    "roc_points",
    "auc_per_window",
    "contingency",
    "skill_scores",
    "block_bootstrap_ci",
]
