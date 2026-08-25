# EVENTS CATALOGUE - How to verify and expand

This file explains how to take the starter `events_catalogue.csv`
(18 events, all source-cited from peer-reviewed and OCHA/ReliefWeb
sources) and turn it into the final, EM-DAT-verified catalogue for
Stage D trigger derivation.

---

## Current status: 18 documented events (1988-2024)

Every event in `events_catalogue.csv` has:
- Date range (start + end)
- At least one traceable source citation
- Brief notes with impact/context

**Peer-reviewed sources cited:**
- Rahman, N., et al. (2023). Spatiotemporal rainfall variability and
  its relationship to flash flood risk in Northeastern Sylhet Haor
  of Bangladesh. Journal of Water and Climate Change 14(11):3985.
  IWA Publishing. https://iwaponline.com/jwcc/article/14/11/3985
- Kamruzzaman, M., & Shaw, R. (2018).
- Roy et al. (2017).
- Rahman, M.S., et al. (2018). Resilience to flash floods in wetland
  communities of northeastern Bangladesh. Int J Disaster Risk Reduc
  31:478-488. ScienceDirect.
- Uddin, K., et al. (2019).
- Akter, J., et al. (2023). Impact analysis of the 2022 flood event
  in Sylhet and Sunamganj using GEE. ScienceDirect.
- Abedin et al. (2022).

**Grey literature / operational sources cited:**
- Banglapedia. Flood entry.
  https://en.banglapedia.org/index.php/Flood
- ReliefWeb (OCHA) Bangladesh flash flood situation reports 2017,
  2022 (May), 2022 (June).
- Global Policy Institute (2022). Living with Floods in Sylhet.
- Dhaka Tribune (2024). Sylhet flooding article.
- DDM (Bangladesh Dept of Disaster Management) situation reports.

---

## STEP 1 - Verify each event via EM-DAT (primary source)

EM-DAT (Emergency Events Database) run by CRED, Universite catholique
de Louvain, is the international standard for disaster records.
Reviewers will expect at least the major events cross-referenced
with EM-DAT.

**How to access:**

1. Go to https://www.emdat.be/ and register (free, ~2 minutes).
2. Once logged in, go to "Data" -> "Public Table".
3. Filter:
   - Country: Bangladesh
   - Disaster Type: Flood
   - Sub-type: Riverine flood, Flash flood
   - Year range: 1981 to 2024
4. Download the CSV.
5. For each event in `events_catalogue.csv`, look up the matching
   EM-DAT record by year and month.
6. Copy the EM-DAT start_date and end_date exactly.
7. In the `notes` column, append EM-DAT DisNo (unique disaster
   identifier, format YYYY-NNNN-BGD).

**Why this matters:** EM-DAT dates are what reviewers expect. Our
current dates are best-guess from grey literature and may be off by
days or weeks. EM-DAT is the reference.

---

## STEP 2 - Cross-check with FFWC bulletins (operational primary)

FFWC (Flood Forecasting and Warning Centre, Bangladesh) issues daily
water-level bulletins. For each event:

1. Go to https://ffwc.gov.bd/ -> Reports -> Annual reports.
2. Find the year's annual report PDF.
3. Look up "danger level exceedance" dates for Sylhet stations:
   - Kanaighat (Surma)
   - Sylhet (Surma)
   - Sherpur-Sylhet (Kushiyara)
   - Sheola (Kushiyara)
   - Amalshid (Kushiyara)
4. The danger-level exceedance dates are the OPERATIONAL event
   definition for triggers. These are what the trigger threshold
   needs to predict.

If FFWC exceedance dates differ from EM-DAT/OCHA dates by more than
2-3 days, use FFWC (operational source) and note the discrepancy.

---

## STEP 3 - Add events this list may have missed

For each year 1981-2024 not currently in the catalogue, check EM-DAT
for Sylhet-region flood events. Years currently NOT in the catalogue
that may have events:
- 1981-1987 (early CHIRPS period)
- 1989 (Banglapedia mentions Sylhet flood but no dates)
- 1990-1996
- 1999, 2001, 2003
- 2005, 2006, 2008, 2009
- 2011, 2013, 2014
- 2018, 2021

Add rows for any EM-DAT-listed events found in these years. Aim for
final catalogue of 20-30 events for statistically stable trigger
derivation.

---

## STEP 4 - Distinguish flash vs riverine (optional column)

The paper focuses on FLASH FLOODS (rapid-onset, driven by intense
Meghalaya/Assam rainfall over hours-to-days, typically pre-monsoon
Mar-May or early monsoon June-July).

Events classified as MAINLY riverine (slower onset, monsoon-fed
Meghna river swelling): 1988, 1998, 2007, 2012, 2020 (mixed).

Consider running Stage D twice:
  (a) All events combined
  (b) Flash-only subset (exclude clearly riverine events)

If results differ substantially, report both. Otherwise report (a) as
primary and (b) as robustness check.

To do this cleanly, add a column `flood_type` with values `flash`,
`riverine`, or `mixed`. The Stage D script currently ignores extra
columns, so this addition is safe.

---

## STEP 5 - Final QC checklist before running Stage D

- [ ] Every event has an EM-DAT DisNo in notes.
- [ ] Every event has an FFWC exceedance date confirmation.
- [ ] No duplicate events (same date range).
- [ ] Date ranges do not overlap (if two events same year, merge or
      keep separate with clear justification).
- [ ] At least 15 events for statistical stability. Target 20-25.
- [ ] Header comment lines removed (# lines).
- [ ] File saved as `data/raw/events_catalogue.csv` (no .template).

Once QC passed, run:

    python scripts/03_run_stage_d_thresholds.py \
        --rain data/raw/sylhet_chirps_daily_1981_2024_gaul.csv \
        --events data/raw/events_catalogue.csv \
        --outdir outputs/stage_d

---

## Time estimate

- EM-DAT registration + download: 30 min
- Cross-referencing 18 events: 2-3 hours
- Adding missed events: 1-2 hours
- FFWC annual report review: 2-3 hours (main effort)
- Total: ~1 full working day of research

This is boring but essential work. Reviewer will ask "how were events
defined?" - the answer must be a documented, traceable process.
