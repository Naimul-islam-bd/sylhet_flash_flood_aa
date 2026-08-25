"""Publication-quality figure utilities for IJDRR."""

from .figure_specs import (
    apply_ijdrr_style,
    save_line_drawing,
    save_halftone,
    save_combination,
    save_bitmapped_line,
    SINGLE_COL_WIDTH_IN,
    FULL_PAGE_WIDTH_IN,
    COLORBLIND_PALETTE,
    SEQUENTIAL_CMAP,
    DIVERGING_CMAP,
)

__all__ = [
    "apply_ijdrr_style",
    "save_line_drawing",
    "save_halftone",
    "save_combination",
    "save_bitmapped_line",
    "SINGLE_COL_WIDTH_IN",
    "FULL_PAGE_WIDTH_IN",
    "COLORBLIND_PALETTE",
    "SEQUENTIAL_CMAP",
    "DIVERGING_CMAP",
]
