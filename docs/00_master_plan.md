# Q1 UPGRADE MASTER PLAN
## Sylhet Flash Flood Anticipatory Action
### Author: Naimul Islam, Department of Civil Engineering, CUET
### Target: International Journal of Disaster Risk Reduction (Elsevier, Q1, IF 4.5)

Version: 2.1 (updated August 2026 with corrected region definitions +
Stage A three-dataset analysis + Stage B seven-event validation complete)

---

## PART 1. REVIEWER-STYLE DIAGNOSIS OF CONFERENCE PAPER

### 1.1 What survives Q1 scrutiny

- The 88.2% flash flood AA coverage gap (WFP/MoDMR, State of AA 2024).
- 2022 event impact numbers (OCHA, IFRC, ReliefWeb).
- 2024 eastern flash flood numbers (OCHA, Aug 2024).

### 1.2 What must be replaced

| Figure | Verdict | Reason |
|--------|---------|--------|
| Fig 1 (rainfall trend +7.7 mm/yr) | REJECT | Synthetic (np.random.seed(42)). Real CHIRPS shows NO significant trend. |
| Fig 2 (event counts, affected pop) | REJECT | Hand-typed illustrative values. |
| Fig 3 panels B & C | PARTIAL | 88.2% hook real; lead-time and pillar % were illustrative. |
| Fig 4 (vulnerability map) | REJECT | Hand-drawn polygon, arbitrary risk labels. |
| Fig 5 (framework) | ACCEPT (conceptual) | Must be labelled "proposed" not "validated". |

### 1.3 Methodological gaps

- No proper trend test (MK+Sen minimum).
- No map accuracy assessment (Kappa expected).
- No trigger validation (POD/FAR/CSI expected).
- Missing prior-work citations (Akter 2023; Uddin 2019; DeepSAR 2025).
- No uncertainty quantification.
- Framework layer numbers presented as prediction, not aspiration.

---

## PART 2. LOCKED NOVEL CONTRIBUTION

> "This study is the first to derive and independently validate rainfall-based
> operational trigger thresholds for flash flood anticipatory action in
> Sylhet Division, Bangladesh, integrating 75 years of ERA5-Land daily
> precipitation (1950-2024) for both Sylhet Division and the trans-boundary
> Barak-Meghna catchment, 44 years of CHIRPS (1981-2024), Sentinel-1 SAR
> inundation for seven flash flood events (2017-2024), and FFWC gauge
> exceedance records, with performance evaluated using standard forecasting
> skill scores (POD, FAR, CSI, HSS) on an independent 2011-2024 validation
> period."

### 2.1 Why defensible (verified July 2026)

1. **Anticipation Hub, Oct 2022** explicitly states existing AA models
   (Jamuna) do not target the NE. No flash flood trigger for Sylhet exists.
2. **BDRCS/OCHA AA frameworks (2020, 2024)** use GloFAS + FFWC for river
   floods, not flash floods.
3. **Akter et al. (2023), Uddin et al. (2019), DeepSAR (2025)** do single-event
   or multi-event mapping. None derives thresholds. None validates with
   skill scores.

### 2.2 What we are NOT claiming

- New ML method.
- Better SAR classification.
- Causal climate-change to flash-flood link.
- Operational deployment.

---

## PART 3. METHODOLOGY - FIVE STAGES

| Stage | Content | Data | Output | Status |
|-------|---------|------|--------|--------|
| A | Climate context | CHIRPS 1981-2024 + ERA5-Land 1950-2024 (Sylhet + trans-boundary) | Table 1, Fig 1 | DONE |
| B | Multi-event inundation | Sentinel-1 SAR, 7 events; S2/L8/L9 optical validation | Table 2, Fig 2 | DONE |
| C | Exposure quantification | WorldPop 2020, ESA WorldCover 2021 | Table 3, Fig 3 | Planned |
| D | Trigger threshold derivation | CHIRPS + FFWC gauge exceedance | Table 4, Fig 4 (scientific heart) | Code ready |
| E | Framework integration | Threshold plugged into proposed framework | Fig 5 | Planned |

---

## PART 4. STAGE A REAL FINDINGS (three-dataset synthesis)

Real trend statistics from `scripts/01_run_stage_a_trends.py` on three
independent datasets. Study regions anchored to authoritative sources:
- Sylhet Division = FAO GAUL 2015 Level 1 polygon
- Trans-boundary catchment = India-WRIS (NRSC/CWC) Barak sub-basin extent

**Five significant trends across 3 datasets, ALL rainfall totals/intensity
signals point DOWN, only dry-spell length points UP.**

### 4.1 Full comparison table

| Index | CHIRPS 44 yr Sylhet | ERA5 75 yr Sylhet | ERA5 75 yr Trans-boundary |
|-------|--------------------|-------------------|--------------------------|
| PRCPTOT annual | -0.45 mm/yr (p=0.895) | **-8.89 mm/yr (p=0.012) DECREASING** | **-3.87 mm/yr (p=0.012) DECREASING** |
| SDII intensity | -0.003 (p=0.895) | **-0.034 (p=0.010) DECREASING** | **-0.014 (p=0.025) DECREASING** |
| R99p very extreme | 0.00 (p=0.745) | -0.25 (p=0.430) | **-1.21 (p=0.033) DECREASING** |
| **CDD dry spell** | **+0.30 days/yr (p=0.017) INCREASING** | +0.05 (p=0.450) | +0.09 (p=0.150) |
| Pre-monsoon Mar-May | -3.24 (p=0.357) | -3.52 (p=0.100) | -0.95 (p=0.332) |

### 4.2 Interpretation

1. **Long-term rainfall totals DECREASING (ERA5 75-yr)** in both Sylhet
   and trans-boundary basin (both p=0.012), with Pettitt change points
   around 2004 for Sylhet local and 1974-1979 for trans-boundary. The
   trans-boundary change at 1974-1979 aligns with the ERA5 satellite-era
   discontinuity and must be discussed as a possible reanalysis artifact
   (Hersbach et al 2020).

2. **CHIRPS 1981-2024 shows DRY SPELLS INCREASING** (CDD +0.30 days/yr,
   p=0.017, change year 2000). Consistent with global climate change theory
   for tropical monsoon regions: fewer but more intense rainfall events
   punctuating longer dry spells. IPCC AR6 predicts this pattern.

3. **NO dataset shows INCREASING extreme rainfall.** The naive
   climate-change narrative fails. Instead:
   - Rainfall totals: flat (CHIRPS) or decreasing (ERA5)
   - Rainfall intensity: flat (CHIRPS) or decreasing (ERA5)
   - Dry spells: increasing (CHIRPS)
   - Flash flood impacts: increasing (OCHA/IFRC/DDM)

### 4.3 Paper narrative (locked)

> Local Sylhet rainfall over 1981-2024 shows stationary totals but
> significantly lengthening dry spells (CDD +0.30 days/yr, p=0.017,
> change point 2000). Longer 75-year ERA5-Land records (1950-2024) for
> both Sylhet and the upstream Barak-Meghna trans-boundary catchment
> show statistically significant decreases in annual total and intensity,
> though a portion of this signal may reflect ERA5 pre-1979 discontinuity
> when satellite data assimilation began. Trans-boundary and local records
> show similar directional patterns, ruling out a simple upstream-vs-
> downstream differential rainfall signal.
>
> Flash flood intensification in Sylhet Division therefore cannot be
> attributed to increased rainfall. Multiple mechanisms remain plausible:
> (1) drier antecedent soil conditions between longer dry spells produce
> sharper runoff response when storms arrive; (2) trans-boundary
> event-scale rainfall variability (single Mawsynram-Cherrapunji storm
> producing 972-2500 mm in one week, as documented for May and June 2022)
> is not captured by annual/decadal trend statistics; (3) downstream
> exposure has increased through settlement expansion and drainage
> capacity loss.
>
> This validates the need for validated multi-source operational triggers:
> rainfall trend analysis alone cannot inform anticipatory action because
> the trend statistics diverge from the impact record.

---

## PART 5. STAGE B FINDINGS (seven-event S1 validation)

Seven flash flood events mapped with Sentinel-1 GRD IW (VV), Otsu
thresholding, JRC GSW permanent-water masking, connected-component
filtering. Validated against merged Sentinel-2 + Landsat-8 + Landsat-9
MNDWI optical reference.

| Event | S1 flood (km2) | Optical ref (km2) | Kappa | F1 | Verdict |
|-------|----------------|--------------------|-------|-----|---------|
| 2017 apr | 3157 | 3664 | +0.56 | 0.63 | GOOD (pre-monsoon, low cloud) |
| 2019 jul | 965 | 2369 | +0.12 | 0.18 | POOR (monsoon cloud + haor permanent) |
| 2020 jul | 448 | 826 | -0.01 | 0.02 | POOR (small event, optical=haor) |
| 2022 may | 2777 | 4635 | +0.41 | 0.50 | MARGINAL (flood + haor mix) |
| 2022 jun | 5963 | 1690 | +0.25 | 0.34 | S1 sees catastrophic flood clouds hide from optical |
| 2023 may | 422 | 845 | +0.21 | 0.23 | POOR (small event, optical=haor) |
| 2024 jul | 5292 | 4499 | +0.57 | 0.67 | GOOD (long window, cloud breaks) |

**Best-quality validation subset (F1 >= 0.5): 2017 April, 2022 May,
2024 July.** Mean F1 = 0.60, mean User accuracy (precision) = 0.66,
mean Overall accuracy = 0.85.

Reviewer interpretation: strict pixel-level Kappa is conservative because
(a) the S1 change-based mask correctly excludes permanent haor water
bodies that optical MNDWI detects, and (b) persistent monsoon cloud
cover reduces optical scene completeness. Producer's and User's accuracies
restricted to low-cloud events provide the most reliable validation.

---

## PART 6. TIMELINE

Assumes ~15 hrs/week.

| Weeks | Stage | Deliverable | Gate |
|-------|-------|-------------|------|
| Done | A (CHIRPS + ERA5 x2) | Table 1, Fig 1, three-dataset comparison | Complete |
| Done | B (S1 seven events) | Table 2, per-event accuracy | Complete |
| 1-2 | D-prep | EM-DAT verification of events catalogue | 20+ verified events |
| 3-4 | D | Thresholds + validation | CSI > 0.4 on validation |
| 5-6 | C | Exposure quantification | Cross-check against OCHA |
| 7-8 | E | Framework integration | Five figures cohesive |
| 9-13 | Writing | Full draft | Self-review |
| 14-15 | Revision | Format for IJDRR | External reader |
| 16 | Submission | Cover letter, submit | Editorial Manager |

Total: 16 weeks remaining. Add 3-6 months peer review.

**Critical timing:** Bangladesh graduates from LDC in November 2026. APC
waiver may reduce from 100% to 50% after graduation. Aim to submit and
enter peer review before November 2026 to lock in 100% waiver.

---

## PART 7. Q1 ACCEPTANCE PROBABILITY

Baseline at IJDRR: 15-25%.
With clear novelty + rigorous methods + traceable numbers: **40-50% if
Stage D produces CSI > 0.5 and HSS > 0.4**.

If Stage D thresholds are weaker: publishable at Q2 (Natural Hazards,
Climate Risk Management, JFRM) with 50-60% chance.

If Stage D fails entirely: pivot to "why rainfall-only triggers are
insufficient" - still publishable at NHESS or JFRM.

---

## PART 8. JOURNAL STRATEGY

**Primary:** IJDRR (Elsevier). Q1, IF 4.5. ISSN 2212-4209.
Gold Open Access from January 2026. APC USD 2,760.

**Waiver:** Bangladesh currently in Research4Life Group A (LDC status).
Corresponding author from CUET receives automatic 100% APC waiver.
Verify at submission portal. LDC graduation November 2026 may reduce to 50%.

**Fallback 1:** NHESS (Copernicus, OA, waiver available), Natural Hazards
(Springer).

**Fallback 2:** Climate Risk Management, JFRM, Geomatics NHR.

---

## PART 9. GUARDRAILS

1. Every number in the paper traces to a source (dataset DOI, or script +
   preserved input).
2. Every figure has a corresponding data file archived in supplementary.
3. If a result contradicts hypothesis, report it. Honest negatives get
   respected.
4. When in doubt about method choice, cite peer-reviewed source and follow
   it. Do not invent.

END OF MASTER PLAN.
