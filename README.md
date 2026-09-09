# Sylhet Flash Flood Anticipatory Action

Rainfall trigger thresholds for flash flood anticipatory action in Sylhet Division, Bangladesh — derivation and independent skill-score validation with benefit-cost analysis.

**Target journal:** Climate Risk Management (Elsevier), Q1, IF ~5.0.

**Author:** Naimul Islam, Independent Researcher, Chattogram 4349, Bangladesh.

## What this repository contains

```
sylhet_flash_flood_aa/
├── src/sylhet_aa/           Python package (analysis, viz, data, flood_mapping, exposure)
├── scripts/                 Thin CLI entry points for each pipeline stage
├── gee/                     Google Earth Engine JavaScript export scripts
├── data/raw/                Original inputs (CSVs committed; TIFFs local only)
├── tests/                   Unit tests (pytest, 21 tests currently passing)
├── notebooks/               Exploratory Jupyter notebooks
├── pyproject.toml           Package definition and dependencies
├── Makefile                 Common pipeline commands
```

## Novel contribution

First derivation and independent skill-score validation of season-stratified rainfall trigger thresholds for flash flood anticipatory action in Sylhet Division, integrating 75 years of ERA5-Land (1950-2024), 44 years of CHIRPS (1981-2024), Sentinel-1 SAR inundation for seven flash flood events, WorldPop and ESA WorldCover exposure quantification, and benefit-cost analysis of anticipatory action interventions — with POD, FAR, CSI, HSS, and ETS evaluated on an independent 2011-2024 validation period using block bootstrap 95 percent confidence intervals.

**Novelty gap confirmed** against Anticipation Hub (October 2022), Akter et al. (2023), Uddin et al. (2019), and Rahman et al. (2023). See `docs/00_master_plan.md` Part 2 for full justification.

## Key findings

- **Pre-monsoon trigger:** trans-boundary 3-day rainfall ≥ 19 mm → POD 0.63 (95 percent CI 0.51-0.74), CSI 0.20, HSS 0.32
- **Monsoon trigger:** local 7-day rainfall ≥ 206 mm → POD 0.35, CSI 0.16, HSS 0.27
- **Season stratification** improves overall CSI by 34 percent versus a single trigger
- **Rainfall totals stationary** over 1981-2024, but **consecutive dry days lengthen** at 0.30 days/year (p = 0.017)
- **Exposure:** 4.01 million people affected in June 2022 alone (Sunamganj dominant at 63 percent exposure)
- **Cost-benefit:** benefit-cost ratio near 7:1 across seven documented events; approximately USD 1 billion in avoidable damages

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

Windows users without `make` can run the underlying Python commands directly (all shown in the Makefile).

## Data sources

| Product | Period | Provider | How obtained |
|---------|--------|----------|--------------|
| CHIRPS v2.0 daily | 1981-2024 | UCSB Climate Hazards Group | GEE, `gee/01_chirps_daily_sylhet.js` |
| ERA5-Land daily (Sylhet) | 1950-2024 | ECMWF Copernicus | GEE, `gee/02_era5land_daily_sylhet.js` |
| ERA5-Land daily (trans-boundary Barak-Meghna) | 1950-2024 | ECMWF Copernicus | GEE, `gee/03_era5land_daily_transboundary.js` |
| Sentinel-1 GRD IW VV | 2017-2024, 7 events | ESA Copernicus | GEE, `gee/04_sentinel1_flood_multievent.js` |
| Sentinel-2 SR + Landsat 8/9 | Per event window | ESA / USGS | GEE, `gee/05_sentinel2_validation.js` |
| WorldPop 2020 | 2020 | University of Southampton | GEE, `gee/06_worldpop_sylhet.js` |
| ESA WorldCover 2021 | 2021 | ESA | GEE, `gee/07_worldcover_sylhet.js` |
| FAO GAUL 2015 Level 2 (districts) | 2015 | FAO | GEE, `gee/08_gaul2_sylhet_districts.js` |
| Flood events catalogue | 1988-2024 | OCHA / IFRC / peer-reviewed literature | Manual curation |

**Study region definitions** are anchored to authoritative sources:

- Sylhet Division: FAO GAUL 2015 Level 1 administrative polygon
- Four Sylhet districts (Sylhet, Sunamganj, Habiganj, Maulvibazar): FAO GAUL 2015 Level 2
- Trans-boundary Barak-Meghna catchment: India-WRIS (NRSC/CWC) official Barak sub-basin extent, 89.5-94.5 deg E, 22.7-26.5 deg N
- Robustness check: HydroBASINS Level 5 polygon (Lehner and Grill, 2013)

```

Every number in the paper is reproducible from these scripts and the raw inputs in `data/raw/`. Nothing is fabricated or hard-coded.

## Current status

- **Stage A** (climate trends, 3 datasets): DONE. CDD +0.30 days/yr, p=0.017 across CHIRPS 44-year record. See `docs/05_stage_a_findings.md`.
- **Stage B** (Sentinel-1 SAR flood mapping, 7 events): DONE. Cleanest F1 scores 0.50-0.67. See `outputs/stage_b/`.
- **Stage C** (WorldPop + ESA WorldCover exposure): DONE. 2022 June peak exposure 4.01 million people, Sunamganj dominant. See `outputs/stage_c/`.
- **Stage C enhancements** (district breakdown + cost-benefit): DONE. BCR 7:1, approximately USD 1 billion avoidable damages across 7 events.
- **Stage D** (season-stratified triggers): DONE. Pre-monsoon POD 0.63, monsoon POD 0.35, both blind-validated on 2011-2024.
- **Stage E** (framework figure + manuscript): DONE. All 5 main figures and 3 supplementary figures generated. Manuscript ready .

**Submission status:**
- **First submission** (IJDRR, Ms. No. IJDRR-D-26-02732): Desk-rejected on 31 August 2026 by Editor-in-Chief Carmine Galasso. Rejection cited insufficient methodological novelty for the journal's international readership priorities, not technical concerns.
- **Current submission** (Climate Risk Management, Elsevier): Submission package prepared with reframing toward climate risk management scope (seasonal forecasting application, benefit-cost analysis, monitoring and evaluation).


## Contact

Naimul Islam  
Email: naimul.islam.bangladesh@gmail.com  
ORCID: [0009-0002-3442-8980](https://orcid.org/0009-0002-3442-8980)  
Independent Researcher, Chattogram 4349, Bangladesh

## Licence

MIT (see `LICENSE`). Code is open. Manuscript will be Gold Open Access under CC-BY at Climate Risk Management (Research4Life Group A automatic APC waiver applies for Bangladesh-based corresponding author until November 2026).
