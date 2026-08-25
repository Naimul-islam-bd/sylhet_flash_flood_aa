# data/raw/

Original satellite exports and manually curated catalogues go here.

## Files expected

| File | How to produce | Size |
|------|---------------|------|
| `sylhet_chirps_daily_1981_2024.csv` | GEE: `gee/01_chirps_daily_sylhet.js` | ~400 KB |
| `sylhet_era5land_daily_1950_2024.csv` | GEE: `gee/02_era5land_daily_sylhet.js` | ~700 KB |
| `transboundary_era5land_daily_1950_2024.csv` | GEE: `gee/03_era5land_daily_transboundary.js` | ~700 KB |
| `events_catalogue.csv` | Copy `events_catalogue.template.csv`, fill in real events from EM-DAT / DDM / OCHA / IFRC / FFWC / peer-reviewed | 5-10 KB |
| `ev_YYYY_MMM_flood_extent.tif` (x6) | GEE: `gee/04_sentinel1_flood_multievent.js` per event | ~50 MB each |
| `ev_YYYY_MMM_s2_reference_water.tif` (x6) | GEE: `gee/05_sentinel2_validation.js` per event | ~50 MB each |

## Do NOT commit large raster files

The .gitignore already excludes `*.tif` and other large binary files. Keep them
here locally and reference them by DOI in the Data Availability statement of
the manuscript (deposit at Zenodo before submission).

## CHIRPS is included

`sylhet_chirps_daily_1981_2024.csv` IS committed to git so anyone cloning the
repository can immediately reproduce Stage A. It is small (~400 KB), stable,
and cited as an intermediate product of the analysis.
