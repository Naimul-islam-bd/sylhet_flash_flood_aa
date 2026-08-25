# Sylhet Flash Flood Anticipatory Action

Rainfall trigger thresholds for flash flood anticipatory action in Sylhet
Division, Bangladesh - derivation and independent skill-score validation.

**Target journal:** International Journal of Disaster Risk Reduction (IJDRR),
Elsevier, Q1, IF ~4.5.

**Author:** Naimul Islam, Department of Civil Engineering, Chittagong
University of Engineering and Technology (CUET), Chattogram 4349, Bangladesh.

---

## What this repository contains

```
sylhet_flash_flood_aa/
├── src/sylhet_aa/       Python package (analysis, viz, data, flood_mapping)
├── scripts/             Thin CLI entry points for each pipeline stage
├── gee/                 Google Earth Engine JavaScript export scripts
├── data/raw/            Original inputs (CSVs committed; TIFFs local only)
├── outputs/             Generated tables, figures, and stage artifacts
├── docs/                Master plan, reviewer defense, manuscript outline
├── tests/               Unit tests (pytest, 21 tests currently passing)
├── notebooks/           Exploratory Jupyter notebooks
├── pyproject.toml       Package definition and dependencies
├── Makefile             Common pipeline commands
└── STEP_BY_STEP.md      Guided walkthrough for the whole workflow
```

---

## Novel contribution

> First derivation and independent skill-score validation of rainfall-based
> operational trigger thresholds for flash flood AA in Sylhet Division,
> integrating 75 years of ERA5-Land (1950-2024), 44 years of CHIRPS
> (1981-2024), Sentinel-1 SAR inundation for seven flash flood events, and
> FFWC gauge exceedance records - with POD, FAR, CSI, HSS, and ETS
> evaluated on an independent 2011-2024 validation period.

Novelty gap confirmed against Anticipation Hub (October 2022), Akter et al.
(2023), Uddin et al. (2019), DeepSAR (2025). See `docs/00_master_plan.md`
Part 2 for full justification.

---

## Quick start

Requires Python 3.10+ and Git.

```bash
# 1. Clone / unzip and enter the project
cd sylhet_flash_flood_aa

# 2. (Recommended) create and activate a virtual environment
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows cmd:
.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate

# 3. Install the package (editable mode - your code edits take effect immediately)
pip install -e .
# For dev tools (pytest, ruff, black) instead:
pip install -e ".[dev]"

# 4. Verify tests pass
pytest tests/

# 5. Run Stage A on the committed CHIRPS CSV (GAUL polygon version)
python scripts/01_run_stage_a_trends.py \
    --input data/raw/sylhet_chirps_daily_1981_2024_gaul.csv \
    --outdir outputs/stage_a

# or with Make
make stage-a
```

Windows users without make can run the underlying Python commands
directly (all shown in the Makefile).

---

## Data sources

| Product | Period | Provider | How obtained |
|---------|--------|----------|--------------|
| CHIRPS v2.0 daily | 1981-2024 | UCSB Climate Hazards Group | GEE, `gee/01_chirps_daily_sylhet.js` |
| ERA5-Land daily (Sylhet) | 1950-2024 | ECMWF Copernicus | GEE, `gee/02_era5land_daily_sylhet.js` |
| ERA5-Land daily (trans-boundary Barak-Meghna) | 1950-2024 | ECMWF Copernicus | GEE, `gee/03_era5land_daily_transboundary.js` |
| Sentinel-1 GRD IW VV | 2015-2024, 7 events | ESA Copernicus | GEE, `gee/04_sentinel1_flood_multievent.js` |
| Sentinel-2 SR + Landsat 8/9 | Per event window | ESA / USGS | GEE, `gee/05_sentinel2_validation.js` |
| WorldPop 2020 | 2020 | University of Southampton | GEE / direct download |
| ESA WorldCover 2021 | 2021 | ESA | GEE / direct download |
| FFWC daily water levels | 1981-2024 | FFWC Bangladesh | Historical data request |
| Flood events catalogue | 1988-2024 | EM-DAT / DDM / OCHA / IFRC / FFWC | Manual curation, verification via EM-DAT |

Study region definitions are anchored to authoritative sources:
- Sylhet Division: FAO GAUL 2015 Level 1 administrative polygon
- Trans-boundary Barak-Meghna catchment: India-WRIS (NRSC/CWC) official
  Barak sub-basin extent, 89.5-94.5 deg E, 22.7-26.5 deg N
- Robustness check: HydroBASINS Level 5 polygon (Lehner and Grill, 2013)

---

## Reproducing the results

```bash
make test           # 21 unit tests
make stage-a        # trends + Fig 1 + Fig 1b (CHIRPS)
make stage-a-era5   # trends on ERA5-Land 1950-2024 (needs GEE export first)
make stage-b        # multi-event flood accuracy (needs S1 and S2 rasters)
make stage-d        # trigger threshold derivation and validation
make figures        # regenerate all publication-quality figures
```

Every number in the paper is reproducible from these scripts + the raw
inputs in `data/raw/`. Nothing is fabricated or hard-coded.

---

## Current status

- Stage A: DONE with real CHIRPS + ERA5 data. Three-dataset comparison
  complete. See `docs/05_stage_a_findings.md`.
- Stage B: DONE. Seven events assessed against S2 + L8/9 reference.
  See `outputs/stage_b/`.
- Stage C: Planned.
- Stage D: Code ready, awaiting EM-DAT-verified events catalogue.
- Stage E: Planned.

Full timeline in `docs/00_master_plan.md` Part 5. Estimated 24 weeks to
submission.

---

## Documentation

Read in this order:

1. `STEP_BY_STEP.md` - what to do next, in order.
2. `docs/00_master_plan.md` - overall plan, novelty, timeline.
3. `docs/05_stage_a_findings.md` - Stage A results synthesis.
4. `docs/01_reviewer_defense.md` - anticipated Q1 reviewer questions.
5. `docs/02_manuscript_outline.md` - IJDRR-formatted manuscript structure.
6. `docs/03_em_registration.md` - Editorial Manager submission guide.
7. `docs/04_ijdrr_rules_checklist.md` - format rules from Guide for Authors.

---

## Contact

Naimul Islam
naimul.islam.bangladesh@gmail.com
ORCID: 0009-0002-3442-8980
Department of Civil Engineering, CUET, Chattogram 4349, Bangladesh

---

## Licence

MIT (see LICENSE). Code is open. Manuscript will be Gold Open Access
under CC-BY at IJDRR.
