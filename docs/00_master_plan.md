# Q1 UPGRADE MASTER PLAN
## Sylhet Flash Flood Anticipatory Action
### Authors: Naimul Islam (CUET), Nawshaba Ahmed (BRAC University)
### Target: International Journal of Disaster Risk Reduction (Elsevier, Q1, IF 4.5)

Version: 2.0 (updated August 2026 after real CHIRPS Stage A findings)

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
> precipitation (1950-2024), 44 years of CHIRPS (1981-2024), Sentinel-1 SAR
> inundation for six flash flood events (2015-2024), and FFWC gauge exceedance
> records, with performance evaluated using standard forecasting skill scores
> (POD, FAR, CSI, HSS) on an independent 2011-2024 validation period."

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

| Stage | Content | Data | Output |
|-------|---------|------|--------|
| A | Climate context | CHIRPS 1981-2024 + ERA5-Land 1950-2024 (Sylhet + trans-boundary) | Table 1, Fig 1 |
| B | Multi-event inundation | Sentinel-1 SAR, six events | Table 2, Fig 2 |
| C | Exposure quantification | WorldPop 2020, ESA WorldCover 2021 | Table 3, Fig 3 |
| D | Trigger threshold derivation | CHIRPS + FFWC gauge exceedance | Table 4, Fig 4 (scientific heart) |
| E | Framework integration | Threshold plugged into proposed framework | Fig 5 |

---

## PART 4. STAGE A REAL FINDINGS (August 2026)

Real CHIRPS 1981-2024 diagnosis, computed via `scripts/01_run_stage_a_trends.py`:

**NO statistically significant trend in ANY of the 8 ETCCDI indices for
Sylhet Division.** All Mann-Kendall p-values > 0.05.

| Index | Sen's slope per year | MK p-value | Trend verdict |
|-------|---------------------|------------|---------------|
| PRCPTOT | -2.80 mm | 0.537 | no significant trend |
| RX1day | -0.45 mm | 0.336 | no significant trend |
| RX5day | -0.55 mm | 0.436 | no significant trend |
| R95p | -3.74 mm | 0.378 | no significant trend |
| R99p | -0.36 mm | 0.487 | no significant trend |
| SDII | -0.009 mm/day | 0.678 | no significant trend |
| CDD | +0.13 days | 0.325 | no significant trend |
| CWD | -0.08 days | 0.641 | no significant trend |
| premonsoon | -3.50 mm | 0.279 | no significant trend |

### 4.1 Interpretation

Local Sylhet rainfall (1981-2024) shows no significant trend, yet flash
floods are becoming more frequent and destructive. Two possibilities:

1. **Trans-boundary Meghalaya-Assam rainfall may be trending** (not the
   Sylhet-local record). To test, Stage A also runs on the trans-boundary
   ERA5-Land 1950-2024 series - see `stage_a_era5_transboundary` output.

2. **Non-climatic drivers** (land-use change, drainage capacity loss,
   settlement in flood-prone areas) may explain increased impact even
   without increased rainfall.

Either way, the finding strengthens the paper: rainfall-only forecasting is
insufficient because local rainfall is stationary while impacts are not,
which is exactly why a validated multi-source trigger framework is needed.

### 4.2 Paper narrative (updated)

Old (fake): "Climate change is increasing Sylhet rainfall -> more flash
floods -> need AA."

New (real, defensible): "Local Sylhet rainfall shows no significant trend
over 1981-2024. Trans-boundary Meghalaya-Assam rainfall analysis is the key
climate driver. Flash flood intensification therefore reflects a combination
of trans-boundary rainfall variability and downstream exposure change, which
motivates the derivation of validated basin-outlet rainfall triggers that
this paper delivers."

---

## PART 5. TIMELINE

Assumes ~15 hrs/week. Nawshaba reviews at milestones.

| Weeks | Stage | Deliverable | Gate |
|-------|-------|-------------|------|
| 1-2 | A (CHIRPS) | Done. Table 1, Fig 1. | Reviewed by Nawshaba. |
| 3 | A (ERA5) | Long-term trend for context. | Compare with CHIRPS. |
| 4-7 | B | Six S1 flood maps + accuracy. | Kappa > 0.7 on 4+ events. |
| 8-9 | C | Exposure quantification. | Cross-check against OCHA. |
| 10-14 | D | Thresholds + validation. | CSI > 0.4 on validation. |
| 15-16 | E | Framework integration. | Five figures cohesive. |
| 17-21 | Writing | Full draft. | Nawshaba full review. |
| 22-23 | Revision | Format for IJDRR. | Two external readers. |
| 24 | Submission | Cover letter, submit. | Editorial Manager. |

Total: 24 weeks. Add 3-6 months peer review. Publication: 12-15 months.

**Critical timing:** Bangladesh graduates from LDC in November 2026. APC
waiver may reduce from 100% to 50% after graduation. Aim to submit by
mid-2026 (allowing revision buffer before graduation takes effect).

---

## PART 6. Q1 ACCEPTANCE PROBABILITY

Baseline at IJDRR: 15-25%.
With clear novelty + rigorous methods + traceable numbers: **40-50% if
Stage D produces CSI > 0.5 and HSS > 0.4**.

If Stage D thresholds are weaker: publishable at Q2 (Natural Hazards,
Climate Risk Management, JFRM) with 50-60% chance.

If Stage D fails entirely: pivot to "why rainfall-only triggers are
insufficient" - still publishable at NHESS or JFRM.

---

## PART 7. JOURNAL STRATEGY

**Primary:** IJDRR (Elsevier). Q1, IF 4.5. ISSN 2212-4209.
Gold Open Access from January 2026. APC USD 2,760.

**Waiver:** Bangladesh currently in Research4Life Group A (LDC status).
Corresponding author from CUET receives automatic 100% APC waiver.
Verify at submission portal. LDC graduation November 2026 may reduce to 50%.

**Fallback 1:** NHESS (Copernicus, OA, waiver available), Natural Hazards
(Springer).

**Fallback 2:** Climate Risk Management, JFRM, Geomatics NHR.

---

## PART 8. GUARDRAILS

1. Every number in the paper traces to a source (dataset DOI, or script +
   preserved input).
2. Every figure has a corresponding data file archived in supplementary.
3. If a result contradicts hypothesis, report it. Honest negatives get
   respected.
4. When in doubt about method choice, cite peer-reviewed source and follow
   it. Do not invent.
5. Unresolved methodological concerns escalate to a third reviewer BEFORE
   submission.

END OF MASTER PLAN.
