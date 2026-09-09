# STEP BY STEP - PC te ki krbe

Ei file ta sequential. Ekta step complete kore, tarpor porer ta shuru
korba. Confusion hole ei file e phire ashba.

Working directory: wherever tumi zip unzip korecho.

---

## STEP 0 - Unzip and check

**Ki krbe:**
1. Zip file `sylhet_flash_flood_aa.zip` download koro.
2. Desktop ba Documents e ekta folder unzip koro.
3. Terminal / PowerShell / cmd khuli.
4. `cd sylhet_flash_flood_aa` diye folder e dhoko.
5. `dir` (Windows) ba `ls` (Mac/Linux) - dekho eigulo ache:
   - `pyproject.toml`, `README.md`, `Makefile`
   - `src/`, `scripts/`, `gee/`, `docs/`, `tests/`, `data/`, `outputs/`

Sob thakle STEP 0 done.

---

## STEP 1 - Python virtual environment ban ao

**Keno:** tomar XGBoost project er package gulor sathe conflict na hoy,
alada environment.

**Ki krbe (Windows PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Prompt shurute `(.venv)` dekhale sob thik ache. Error hole:

- "cannot be loaded because running scripts is disabled" -> ekta script
  policy issue. Run this once as admin:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

- "python not found" -> Python install nai. https://python.org theke
  Python 3.11 ba 3.12 install koro. Install korar shomoy checkbox
  "Add Python to PATH" oboshoi tick koro.

**Mac / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Done hole STEP 2.

---

## STEP 2 - Package install koro

```bash
pip install -e .
```

Ei command er 4-5 minute lagbe (pandas, numpy, rasterio download hobe).
Rasterio Windows e onek shomoy fail kore. Fail korle:

```bash
pip install --only-binary :all: rasterio
pip install -e .
```

Verify:
```bash
python -c "import sylhet_aa; print(sylhet_aa.__version__)"
```

`0.1.0` dekhale success.

---

## STEP 3 - Tests chalao

```bash
pytest tests/
```

Expected output er ses line:

> ============================== 21 passed in 1.0s ==============================

21 pass hole go to STEP 4. Fail hole message ta amake pathao.

---

## STEP 4 - Stage A - CHIRPS trend analysis (already inside)

CHIRPS CSV committed - direct chalao:

```bash
python scripts/01_run_stage_a_trends.py \
    --input data/raw/sylhet_chirps_daily_1981_2024.csv \
    --outdir outputs/stage_a
```

(Windows PowerShell e backslash er poriborte "`" backtick use koro
line-break jonno, ba ekta line e likho.)

Terminal e Table 1 print hobe (same as ei zip er outputs/stage_a er
mote). Outputs generate hobe:

- `outputs/stage_a/Figure_1.pdf`
- `outputs/stage_a/Figure_1b.pdf`
- `outputs/stage_a/table1_trend_statistics.csv`
- `outputs/stage_a/annual_indices.csv`
- `outputs/stage_a/premonsoon_series.csv`

Same values ashle Stage A verified.

---



## STEP 6 - GEE scripts run koro (5 tas)

`gee/` folder e 5 ta JavaScript file. Ekta ekta kore:

1. Chrome / Firefox e https://code.earthengine.google.com khulo.
   Google account diye login (kono account fee lagbe na).
2. Left panel Scripts tab e "New Script" click koro.
3. Naam dao (e.g. "01_chirps_sylhet").
4. `gee/01_chirps_daily_sylhet.js` er content copy-paste koro.
5. "Save" click.
6. "Run" click.
7. Right panel Tasks tab kholo. Blue "Run" button dekhale click.
8. Popup e Drive folder confirm koro (default: gee_exports_sylhet).
9. Task queue e chole gele nichhe ekta green tick hobe (10-30 min).
10. Google Drive theke CSV download.

Ei order e run koro:

- `01_chirps_daily_sylhet.js` - already output ache CHIRPS CSV file.
   (Just verify same result ashche kina.)
- `02_era5land_daily_sylhet.js` - Sylhet ERA5 1950-2024 (1-2 hr).
- `03_era5land_daily_transboundary.js` - trans-boundary ERA5 (1-2 hr).
- `04_sentinel1_flood_multievent.js` - EVENT_ID variable change kore 6
   bar run: `ev_2017_apr`, `ev_2019_jul`, `ev_2020_jul`, `ev_2022_jun`,
   `ev_2023_may`, `ev_2024_jul`. Each ~15 min task queue + 30 min run.
- `05_sentinel2_validation.js` - same 6 EVENT_ID gulo run.

Sob download hoye elle `data/raw/` folder e rakho.

---

## STEP 7 - Stage A on ERA5-Land (long-term context)

STEP 6 er ERA5 CSV download hoye gele:

```bash
python scripts/01_run_stage_a_trends.py \
    --input data/raw/sylhet_era5land_daily_1950_2024.csv \
    --outdir outputs/stage_a_era5 \
    --label "ERA5-Land"
```

Trend jodi ekhaneo not significant hoy -> confirms CHIRPS finding.
Trend jodi significant hoy -> paper e discuss koro: "44 vs 75 year window
matters".

Trans-boundary o same:

```bash
python scripts/01_run_stage_a_trends.py \
    --input data/raw/transboundary_era5land_daily_1950_2024.csv \
    --outdir outputs/stage_a_transboundary \
    --label "ERA5-Land trans-boundary"
```

Ei ta paper er potentially most interesting comparison.

---

## STEP 8 - Events catalogue fill koro

`data/raw/events_catalogue.template.csv` khulo Excel e. Delete hedar
comment lines (# diye shuru). 15-25 verified events add koro. Sources:

- **EM-DAT:** emdat.be - free registration, download Bangladesh flood
  events, filter Sylhet Division, filter "Flash".
- **DDM annual reports:** ddm.gov.bd - Bangladesh Department of Disaster
  Management, event tables per year.
- **OCHA / ReliefWeb:** reliefweb.int - search "Bangladesh flash flood",
  filter by date range.
- **IFRC DREF appeals:** ifrc.org - specific event fact-finding.
- **FFWC bulletins:** ffwc.gov.bd - danger level exceedance days.

Save as `events_catalogue.csv` (no .template).

---

## STEP 9 - Stage B - Sentinel-1 flood accuracy

Per event:

```bash
python scripts/02_run_flood_accuracy.py \
    --predicted data/raw/ev_2022_jun_flood_extent.tif \
    --reference data/raw/ev_2022_jun_s2_reference_water.tif \
    --event_id ev_2022_jun \
    --outdir outputs/stage_b
```

6 event er jonno chalao. Kappa >= 0.7 chai (target). Kono event fail
korle S2 er poriborte Landsat-8 fallback try koro (dekho `gee/05_...js`
er comment section).

---

## STEP 10 - Stage D - trigger thresholds

```bash
python scripts/03_run_stage_d_thresholds.py \
    --rain data/raw/sylhet_chirps_daily_1981_2024.csv \
    --events data/raw/events_catalogue.csv \
    --outdir outputs/stage_d
```

Output: Table 4 (calibration + validation with 95% CIs), Figure 4 (four
panel skill curves), CSV files er sob intermediate results.

**GO / NO-GO gate:** Validation period CSI >= 0.4 hole Stage E te jaao.
CSI < 0.4 hole paper narrative flip: "why rainfall-only triggers are
insufficient - need to include gauge / soil moisture". Etao publishable,
just angle alada.

---

## STEP 11 - Stage E - framework figure

Not scripted (design work). Use Inkscape ba draw.io. Real threshold
numbers (Stage D theke) figure e boshaao. Save as PDF (vector, IJDRR
compliant).

---

## STEP 12 - Manuscript writing

`docs/02_manuscript_outline.md` follow koro. Word file banao (single
column). IJDRR checklist `docs/04_ijdrr_rules_checklist.md` er sob item
mark koro submit korar age.

---

## STEP 13 - Submit

`docs/03_em_registration.md` follow koro. Editorial Manager e submit
koro. APC waiver auto-apply hoye jabe (Bangladesh Group A). Waiver check
konfirm hole submit finalize koro.

---

## Confusion hole

- Ei file re-read koro.
- Terminal er full error message pathao amake.
- Kono step e technical detail chai hole `docs/00_master_plan.md` Part
  ke read koro.

Every step er kaje amar test-verified. Kono script er expected output er
sathe tomar output milbe. Milche na hole real problem, pathao.
