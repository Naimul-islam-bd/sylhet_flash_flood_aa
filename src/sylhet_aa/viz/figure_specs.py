"""
Publication-grade figure defaults for IJDRR (Elsevier).

Rules encoded here (verified from IJDRR Guide for Authors, July 2026):

    Vector drawings (line-only plots) -> EPS or PDF, fonts embedded
    Halftones (photos, raster maps)   -> TIFF/JPG/PNG, min 300 dpi
                                          single col >= 1063 px
                                          full page >= 2244 px
    Bitmapped line drawings           -> TIFF/JPG/PNG, min 1000 dpi
                                          single col >= 3543 px
                                          full page >= 7480 px
    Combinations line + halftone      -> TIFF/JPG/PNG, min 500 dpi
                                          single col >= 1772 px
                                          full page >= 3740 px

Filename convention: Figure_1, Figure_2, ..., Figure_5 (underscore, no space)
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---- Physical page widths (inches) used by Elsevier journals ----
SINGLE_COL_WIDTH_IN = 3.54     # ~ 90 mm
FULL_PAGE_WIDTH_IN = 7.48      # ~ 190 mm

# ---- Resolution requirements (dpi), enforced by helper functions ----
HALFTONE_DPI = 300
LINE_RASTER_DPI = 1000
COMBINATION_DPI = 500

# ---- Colourblind-safe palette (Tableau 10, ordered) ----
COLORBLIND_PALETTE = [
    "#1f77b4",  # blue
    "#ff7f0e",  # orange
    "#2ca02c",  # green
    "#d62728",  # red
    "#9467bd",  # purple
    "#8c564b",  # brown
    "#17becf",  # cyan
    "#7f7f7f",  # grey
]
SEQUENTIAL_CMAP = "viridis"
DIVERGING_CMAP = "RdBu_r"


def apply_ijdrr_style() -> None:
    """Set matplotlib rcParams to IJDRR-friendly defaults."""
    plt.rcdefaults()
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.titlesize": 11,
        "lines.linewidth": 1.2,
        "lines.markersize": 4.0,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "grid.linewidth": 0.4,
        "grid.alpha": 0.3,
        "figure.dpi": 100,
        "savefig.pad_inches": 0.05,
        # Embedded fonts for Elsevier typesetting
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "text.usetex": False,
        "mathtext.fontset": "stixsans",
    })


def _prepare_path(path: str | Path, allowed_exts: set[str]) -> None:
    ext = Path(path).suffix.lower().lstrip(".")
    if ext not in allowed_exts:
        raise ValueError(
            f"Filename '{path}' does not have an allowed extension "
            f"({'/'.join(allowed_exts)}). IJDRR requires one of these for this "
            f"artwork type."
        )
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def _verify_min_pixels(width_in: float, dpi: int,
                        min_full: int, min_single: int) -> None:
    actual = int(width_in * dpi)
    if width_in >= FULL_PAGE_WIDTH_IN * 0.9:
        needed, label = min_full, "full page"
    else:
        needed, label = min_single, "single column"
    if actual < needed:
        print(f"WARNING: figure width is {actual} px ({label}), below IJDRR "
              f"minimum {needed} px for {label}. Increase dpi or width_in.")


def save_line_drawing(fig, path: str | Path,
                       width_in: float = FULL_PAGE_WIDTH_IN) -> None:
    """Vector output (EPS or PDF) for line-only figures."""
    _prepare_path(path, {"pdf", "eps"})
    h_in = fig.get_size_inches()[1]
    fig.set_size_inches(width_in, h_in)
    fig.savefig(path, format=Path(path).suffix.lstrip("."),
                bbox_inches="tight", pad_inches=0.05)


def save_halftone(fig, path: str | Path,
                   width_in: float = FULL_PAGE_WIDTH_IN,
                   dpi: int = HALFTONE_DPI) -> None:
    """Raster output for photograph-like figures (>= 300 dpi)."""
    _prepare_path(path, {"tif", "tiff", "jpg", "jpeg", "png"})
    if dpi < HALFTONE_DPI:
        raise ValueError("IJDRR requires >= 300 dpi for halftones.")
    h_in = fig.get_size_inches()[1]
    fig.set_size_inches(width_in, h_in)
    fig.savefig(path, dpi=dpi, bbox_inches=None, pad_inches=0.05)
    _verify_min_pixels(width_in, dpi, 2244, 1063)


def save_combination(fig, path: str | Path,
                      width_in: float = FULL_PAGE_WIDTH_IN,
                      dpi: int = COMBINATION_DPI) -> None:
    """Raster output for figures mixing line drawings and halftones (>= 500 dpi)."""
    _prepare_path(path, {"tif", "tiff", "jpg", "jpeg", "png"})
    if dpi < COMBINATION_DPI:
        raise ValueError("IJDRR requires >= 500 dpi for combination line/halftone.")
    h_in = fig.get_size_inches()[1]
    fig.set_size_inches(width_in, h_in)
    fig.savefig(path, dpi=dpi, bbox_inches=None, pad_inches=0.05)
    _verify_min_pixels(width_in, dpi, 3740, 1772)


def save_bitmapped_line(fig, path: str | Path,
                         width_in: float = FULL_PAGE_WIDTH_IN,
                         dpi: int = LINE_RASTER_DPI) -> None:
    """Raster output for bitmapped line drawings (>= 1000 dpi). Prefer vector."""
    _prepare_path(path, {"tif", "tiff", "jpg", "jpeg", "png"})
    if dpi < LINE_RASTER_DPI:
        raise ValueError("IJDRR requires >= 1000 dpi for bitmapped line drawings.")
    h_in = fig.get_size_inches()[1]
    fig.set_size_inches(width_in, h_in)
    fig.savefig(path, dpi=dpi, bbox_inches=None, pad_inches=0.05)
    _verify_min_pixels(width_in, dpi, 7480, 3543)
