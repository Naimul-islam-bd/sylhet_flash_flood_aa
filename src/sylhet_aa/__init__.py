"""
sylhet_aa - Rainfall trigger thresholds for flash flood anticipatory action
in Sylhet Division, Bangladesh.

Modules:
    config              Paths and shared constants
    data.load           Data loading utilities
    data.validate       Integrity checks
    analysis.trends     Mann-Kendall, Sen's slope, Pettitt change-point
    analysis.extremes   ETCCDI extreme rainfall indices
    analysis.thresholds Rainfall trigger derivation
    analysis.skill      POD, FAR, CSI, HSS, ETS contingency-table skill scores
    flood_mapping.postprocess  Sentinel-1 flood accuracy assessment
    viz.figure_specs    Publication-quality figure defaults for IJDRR
    viz.figures         Paper figure builders
"""

__version__ = "0.1.0"
__authors__ = ["Naimul Islam", "Nawshaba Ahmed"]
