"""
Project-wide configuration and constants.

Every path and every numeric constant used across the pipeline lives here.
When something needs to change (e.g. moving to a new study region), you
edit this file only.

Study region definitions are now anchored to published authoritative
sources rather than arbitrary bounding boxes. See STUDY_REGION_NOTES
at the bottom of this file for reviewer-facing justifications.
"""

from pathlib import Path

# ------------------------------------------------------------------
# Paths (resolved relative to the project root)
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_INTERIM = DATA_DIR / "interim"
DATA_EXTERNAL = DATA_DIR / "external"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUTS_STAGE_A = OUTPUTS_DIR / "stage_a"
OUTPUTS_STAGE_A_ERA5 = OUTPUTS_DIR / "stage_a_era5"
OUTPUTS_STAGE_B = OUTPUTS_DIR / "stage_b"
OUTPUTS_STAGE_D = OUTPUTS_DIR / "stage_d"
OUTPUTS_FIGURES = OUTPUTS_DIR / "figures"
OUTPUTS_TABLES = OUTPUTS_DIR / "tables"

# Default input filenames.
# Files with "_gaul" suffix use the FAO GAUL admin boundary (corrected v2).
# Legacy bbox files (without suffix) may exist from earlier runs; prefer _gaul.
CHIRPS_DAILY_CSV = DATA_RAW / "sylhet_chirps_daily_1981_2024_gaul.csv"
CHIRPS_DAILY_CSV_LEGACY = DATA_RAW / "sylhet_chirps_daily_1981_2024.csv"

ERA5_DAILY_CSV = DATA_RAW / "sylhet_era5land_daily_1950_2024_gaul.csv"
ERA5_TRANSBOUNDARY_CSV = DATA_RAW / "transboundary_era5land_daily_1950_2024_iwrs.csv"
ERA5_TRANSBOUNDARY_HYBAS_CSV = DATA_RAW / "transboundary_era5land_daily_1950_2024_hybas5.csv"

EVENTS_CATALOGUE_CSV = DATA_RAW / "events_catalogue.csv"


# ------------------------------------------------------------------
# Study regions (documented and reviewer-defensible)
# ------------------------------------------------------------------

# Sylhet Division: FAO GAUL 2015 Level 1 administrative boundary
# (Bangladesh, ADM1_NAME = 'Sylhet'). Roughly 12,600 km2.
# Approximate bbox for reference only; actual extraction uses the
# GAUL polygon in GEE (script gee/02_era5land_daily_sylhet.js).
SYLHET_BBOX = {
    "min_lon": 90.90, "max_lon": 92.50,
    "min_lat": 24.00, "max_lat": 25.20,
    "name": "Sylhet Division, Bangladesh",
    "authority": "FAO GAUL 2015 Level 1 (used as polygon, bbox for reference)",
    "extraction_geometry": "polygon",
}

# Trans-boundary Barak-Meghna catchment: two definitions supported.
#
# Definition A (default in scripts): India-WRIS official Barak sub-basin
# extent, 89.5-94.5 E, 22.7-26.5 N. This is a rectangular bbox that
# fully contains the Indian portion of the basin plus the Bangladesh
# portion including Sylhet Division.
# Source: India Water Resources Information System (NRSC/CWC),
#         http://india-wris.nrsc.gov.in - Barak & Others page.
TRANSBOUNDARY_BBOX = {
    "min_lon": 89.50, "max_lon": 94.50,
    "min_lat": 22.70, "max_lat": 26.50,
    "name": "Barak-Meghna trans-boundary catchment (India-WRIS extent)",
    "authority": "India-WRIS (NRSC/CWC), Barak & Others sub-basin",
    "extraction_geometry": "bbox",
}

# Definition B (alternate): HydroSHEDS Level 5 basin polygon
# containing Sylhet. Preferred by top hydrology journals.
# Source: Lehner, B., Grill G. (2013). Global river hydrography and
#         network routing. Hydrol. Process. 27(15): 2171-2186.
TRANSBOUNDARY_HYBAS = {
    "hydrosheds_level": 5,
    "reference_point_lon": 91.87,
    "reference_point_lat": 24.90,
    "name": "Barak-Meghna trans-boundary catchment (HydroBASINS L5)",
    "authority": "Lehner & Grill (2013) HydroBASINS",
    "extraction_geometry": "polygon",
}


# ------------------------------------------------------------------
# Analysis parameters
# ------------------------------------------------------------------
WET_DAY_THRESHOLD_MM = 1.0          # ETCCDI standard
PRE_MONSOON_MONTHS = (3, 4, 5)      # March, April, May
MONSOON_MONTHS = (6, 7, 8, 9)       # June-September

# ETCCDI baseline period for percentile-based indices (R95p, R99p).
# WMO recommendation is a 30-year fixed baseline.
BASELINE_START = 1981
BASELINE_END = 2010

# Contingency-table skill score parameters
ACCUMULATION_WINDOWS_DAYS = (1, 2, 3, 5, 7)
EVENT_HALO_DAYS = 3                 # +/- days around reported event
CAL_END_YEAR_DEFAULT = 2010
VAL_START_YEAR_DEFAULT = 2011
DECORR_BLOCK_DAYS = 3               # block bootstrap block length
N_BOOTSTRAP = 1000

# Flood-mapping accuracy targets (IJDRR reviewer expectations).
KAPPA_TARGET = 0.70
OVERALL_ACC_TARGET = 0.85


# ------------------------------------------------------------------
# STUDY_REGION_NOTES - reviewer-facing text for the Methods section
# ------------------------------------------------------------------
STUDY_REGION_NOTES = """
Study region definitions (reviewer-facing text for Methods):

Sylhet Division (primary study area):
    Defined by the FAO Global Administrative Unit Layers (GAUL) 2015
    Level 1 polygon for Sylhet Division, Bangladesh. Total area
    approximately 12,600 km^2. Basin-averaged daily rainfall is
    computed within this polygon at each dataset's native resolution.

Trans-boundary Barak-Meghna catchment (upstream study area):
    Defined by the India Water Resources Information System (India-WRIS,
    NRSC/CWC) Barak sub-basin extent, 89.5-94.5 deg E, 22.7-26.5 deg N.
    This rectangle encompasses the full Indian portion of the Barak
    (Meghna) drainage basin, which spans the states of Meghalaya,
    Manipur, Mizoram, Assam, Tripura and Nagaland, plus the Bangladesh
    portion including Sylhet Division. A robustness check using the
    HydroBASINS Level 5 polygon (Lehner and Grill, 2013) is reported
    in supplementary material.

    The trans-boundary extent is justified because Sylhet flash floods
    are generated by orographic rainfall on the Khasi and Jaintia Hills
    of the Shillong Plateau (Meghalaya), on the Barak river headwaters
    in Manipur (Japvo mountain, source elevation approximately 2,331 m),
    and on the Tripura Hills. Downstream, the Surma and Kushiyara
    rivers convey this runoff through Sylhet Division. Local Sylhet
    rainfall alone is therefore insufficient to characterise the flash
    flood signal.

References:
    India-WRIS. Barak & Others Sub-basin. India Water Resources
        Information System, NRSC/CWC. http://india-wris.nrsc.gov.in
    Lehner, B., Grill G. (2013). Global river hydrography and network
        routing: baseline data and new approaches to study the world's
        large river systems. Hydrological Processes 27(15): 2171-2186.
        doi:10.1002/hyp.9740
    FAO (2015). Global Administrative Unit Layers (GAUL) 2015. Food and
        Agriculture Organization of the United Nations.
"""
