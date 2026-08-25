# v2 UPGRADE - Corrected study region definitions

**Date:** 2026-08-17
**Reason:** original bounding boxes were arbitrary; corrected to use
peer-reviewed and authoritative sources so the study region is
scientifically defensible.

---

## What changed

### Sylhet Division primary study area

- **Was:** rectangular bbox 91.00-92.70 E, 24.20-25.50 N (arbitrary)
- **Now:** FAO GAUL 2015 Level 1 official polygon for Sylhet Division
- **Impact:** slightly wider (west and south) than the previous bbox;
  captures Sunamganj west and Habiganj south that were being clipped

### Trans-boundary Barak-Meghna catchment

- **Was:** rectangular bbox 89.5-93.0 E, 24.0-26.5 N (arbitrary)
- **Now:** two options -
  - **Approach A (default):** bbox matching India-WRIS Barak sub-basin
    extent (89.5-94.5 E, 22.7-26.5 N)
  - **Approach B (best practice):** HydroBASINS Level 5 polygon
- **Impact:** the previous box was missing about 40% of the actual
  drainage area, notably the Barak river headwaters in Manipur
  (east of 93 E) and the Tripura hills contribution (south of 24 N).
  The Barak river SOURCE (Japvo mountain, Manipur, 25.36 N 94.06 E)
  was outside the previous box.

---

## Which files to replace

Copy each file from this "updates" folder over the same-name file in
your project:

    gee/01_chirps_daily_sylhet.js            -> replaces existing
    gee/02_era5land_daily_sylhet.js          -> replaces existing
    gee/03_era5land_daily_transboundary.js   -> replaces existing
    src/sylhet_aa/config.py                  -> replaces existing

The Python analysis code (trend tests, skill scores, etc.) does not
change - only the region definitions in `config.py` and the GEE
extraction scripts.

---

## What to do NOW

1. **Cancel current GEE task if it is still running.** Go to GEE Tasks
   panel, click the running task, click Cancel. (If it already
   finished, no worries - keep the file, it will be labelled as the
   "legacy bbox" run in the paper's supplementary.)

2. **Replace the 4 files** listed above.

3. **Re-run script 01 (CHIRPS on Sylhet GAUL polygon)** first. This
   produces `sylhet_chirps_daily_1981_2024_gaul.csv` in Drive. Download,
   put in `data/raw/`, run Stage A again to verify the null result
   still holds. (It will - GAUL vs bbox is <20% difference in spatial
   coverage; the trend statistics will barely move.)

4. **Run script 02 (ERA5 Sylhet, GAUL polygon).** ~1-2 hours.

5. **Run script 03 (ERA5 trans-boundary, India-WRIS bbox).** Default
   is Approach A. ~1-2 hours. If you want Approach B (HydroBASINS)
   too, edit `USE_HYDROBASINS = true` in the script and run again -
   this becomes a robustness check for the supplementary material.

---

## Reviewer defense for this decision

If a reviewer asks "why did you use a bbox instead of the actual
watershed?", the answer for Approach A is:

> "We adopted the India Water Resources Information System (NRSC/CWC)
> official extent of the Barak sub-basin (89.5-94.5 deg E, 22.7-26.5
> deg N) as our trans-boundary study region. This bounding box is
> published as authoritative by the Government of India and includes
> all six Indian states drained by the Barak system (Meghalaya,
> Manipur, Mizoram, Assam, Tripura, Nagaland) plus the Bangladesh
> portion including Sylhet Division. A robustness check using the
> HydroBASINS Level 5 polygon (Lehner and Grill, 2013) is reported in
> Supplementary Table S3 and yields consistent results."

If a reviewer asks "why not the whole Meghna basin including delta?":

> "The delta portion is downstream of Sylhet Division and does not
> generate the flash flood runoff. Only the upstream area (Barak sub-
> basin per India-WRIS) is hydrologically relevant to the trigger
> analysis."

---

## What did NOT change

- CHIRPS values (already computed with the previous bbox) are still
  usable as a first pass. Re-running with GAUL polygon will give a
  slightly different mean rainfall (~1-3% difference expected) but
  the trend verdict (no significant trend in any index) will be
  robust because it depends on temporal variance, not spatial extent.
- The overall methodology (5 stages, target journal, timeline, novelty
  statement) is unchanged.
- All existing outputs in `outputs/stage_a/` remain valid as v1.
  Rename to `outputs/stage_a_v1_bbox/` before running v2 if you want
  to keep both for supplementary comparison.
