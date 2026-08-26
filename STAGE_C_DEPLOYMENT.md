# STAGE C DEPLOYMENT

Exposure quantification: overlay flood extents (from Stage B) with
population (WorldPop 2020) and land cover (ESA WorldCover 2021) to
produce Table 3.

---

## What is new in this update

**GEE scripts (2 new, run once):**
- `gee/06_worldpop_sylhet.js` - export population count 100m for Sylhet
- `gee/07_worldcover_sylhet.js` - export land cover 10m for Sylhet

**Python code (1 new module + 1 new script + 1 new test):**
- `src/sylhet_aa/exposure/` - new module for exposure computation
- `scripts/04_run_stage_c_exposure.py` - CLI to run Stage C on 7 events
- `tests/test_exposure.py` - unit tests

---

## Deployment steps

### 1. Extract files into project

Extract this zip into your project root. Files placed will be:
```
gee/06_worldpop_sylhet.js
gee/07_worldcover_sylhet.js
src/sylhet_aa/exposure/__init__.py
src/sylhet_aa/exposure/compute_exposure.py
scripts/04_run_stage_c_exposure.py
tests/test_exposure.py
```

### 2. Verify install (no re-install needed - editable mode)

```
python -c "from sylhet_aa.exposure import exposed_population, landcover_breakdown; print('exposure module OK')"
```

Expected: `exposure module OK`

### 3. Run tests

```
pytest tests/test_exposure.py -v
```

Expected: 4 tests pass.

### 4. Queue 2 GEE tasks

**Task A - WorldPop:**
1. Open https://code.earthengine.google.com
2. NEW - File - name `06_worldpop_sylhet`
3. Paste content from `gee/06_worldpop_sylhet.js`, Save, Run
4. Tasks tab - blue RUN
5. ~5 min - produces `sylhet_worldpop_2020.tif` in Google Drive (5-10 MB)

**Task B - WorldCover:**
1. NEW - File - name `07_worldcover_sylhet`
2. Paste content from `gee/07_worldcover_sylhet.js`, Save, Run
3. Tasks tab - blue RUN
4. ~10 min - produces `sylhet_worldcover_2021.tif` in Google Drive
   (100-300 MB because 10m resolution)

### 5. Download both files

Save to your project `data/raw/`:
- `data/raw/sylhet_worldpop_2020.tif`
- `data/raw/sylhet_worldcover_2021.tif`

### 6. Run Stage C on all 7 events

```
python scripts/04_run_stage_c_exposure.py --pop data/raw/sylhet_worldpop_2020.tif --landcover data/raw/sylhet_worldcover_2021.tif --outdir outputs/stage_c
```

Runtime: 2-5 minutes (reprojection is I/O heavy).

Outputs:
- `outputs/stage_c/table3a_exposed_population.csv` - Table 3a
- `outputs/stage_c/table3b_landcover_breakdown.csv` - Table 3b

### 7. Commit + push

```
git add -A
git commit -m "stage c: exposure quantification for 7 events (WorldPop + WorldCover)"
git push
```

---

## Expected results

### Table 3a - Exposed population

Sylhet Division total population from WorldPop 2020 ~ 10-12 million.

Per event:
| Event | Expected exposed (rough) | % of Division |
|-------|--------------------------|---------------|
| 2017 apr | 2-4 million | 20-35% |
| 2019 jul | 0.5-1 million | 5-10% |
| 2020 jul | 0.2-0.5 million | 2-5% |
| 2022 may | 1.5-3 million | 15-30% |
| 2022 jun | **4-7 million** | **40-60%** (catastrophic) |
| 2023 may | 0.2-0.5 million | 2-5% |
| 2024 jul | 3-6 million | 30-50% |

Numbers will vary based on actual flood extent overlay.

### Table 3b - Land cover breakdown

For each event, area (km2) of flood extent by land cover class. Expected
dominant classes:
- Cropland (class 40) - largest by area
- Herbaceous wetland (class 90) - haor areas
- Built-up (class 50) - villages, small towns
- Tree cover (class 10) - hill fringes
