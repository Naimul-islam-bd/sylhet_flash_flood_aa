# MANUSCRIPT OUTLINE (IJDRR)

Follow the section structure implied by the IJDRR Guide for Authors: numbered
sections 1, 1.1, 1.1.1; abstract <= 250 words; keywords 1-7 English (no
"and"/"of"); highlights 3-5 bullets each <= 85 characters.

Word budget: ~7,000-9,000 words body + references. Tables <= 8, Figures <= 8.

---

## Title (single line, no colons if possible)

> "Rainfall trigger thresholds for flash flood anticipatory action in Sylhet
> Division, Bangladesh: derivation and independent skill-score validation
> from 44 years of CHIRPS and Sentinel-1 SAR (1981-2024)"

Alternative shorter title:

> "Skill-validated rainfall triggers for flash flood anticipatory action in
> Sylhet, Bangladesh"

---

## Highlights (3-5 bullets, each <= 85 characters)

1. First skill-validated rainfall triggers for Sylhet flash flood
   anticipatory action.
2. 44 yr CHIRPS shows no rainfall total trend but dry spells lengthen
   (CDD +0.3 d/yr).
3. Seven Sentinel-1 events mapped with Otsu; Kappa 0.56 on cleanest
   validation cases.
4. Blind 2011-2024 validation: [POD/CSI numbers from Stage D].
5. Thresholds ready to integrate into BDRCS-FFWC operational AA
   framework.

(Adjust highlight 4 to real numbers after Stage D.)

---

## Abstract (<= 250 words, unstructured)

Paragraph 1 (Problem): Flash floods in Sylhet Division cause repeated
displacement; no validated trigger threshold exists (Anticipation Hub 2022).

Paragraph 2 (What was done): 44 years CHIRPS + 75 years ERA5-Land (Sylhet
+ trans-boundary) + seven Sentinel-1 events + FFWC gauges.

Paragraph 3 (Findings): Sylhet local rainfall totals stationary but dry
spells lengthening; Kappa 0.56 on cleanest events; Stage D thresholds
(fill after Stage D).

Paragraph 4 (Significance): First operational rainfall triggers for
Sylhet-Sunamganj flash flood AA, ready for integration.

---

## Keywords (7, no "and"/"of")

flash flood; anticipatory action; Sylhet; CHIRPS; Sentinel-1; skill score;
Bangladesh

---

## 1. Introduction (~800 words)

- 1.1 Global context of anticipatory action.
- 1.2 Bangladesh-specific status (Jamuna AA success, 88.2% flash flood gap).
- 1.3 Sylhet-Sunamganj flash flood characteristics (rapid onset,
  trans-boundary origin).
- 1.4 Literature gap statement: Akter 2023 / Uddin 2019 / DeepSAR 2025
  cover mapping; none derives + validates operational triggers.
- 1.5 Study objectives, three bullets.
- 1.6 Novelty statement (from Master Plan Part 2).

## 2. Study area and data (~600 words)

- 2.1 Study area (map). Add Elsevier boundary caption: "Map lines
  delineate study areas and do not necessarily depict accepted national
  boundaries." Sylhet Division defined by FAO GAUL 2015 Level 1 polygon;
  trans-boundary catchment defined by India-WRIS (NRSC/CWC) official
  Barak sub-basin extent.
- 2.2 Data sources (Table with columns Product / Period / Resolution /
  DOI or Source):
  - CHIRPS v2.0 daily 1981-2024
  - ERA5-Land daily 1950-2024 (Sylhet + trans-boundary)
  - Sentinel-1 GRD IW (7 events)
  - Sentinel-2 SR + Landsat 8/9 (multi-satellite optical validation)
  - WorldPop 2020, ESA WorldCover 2021
  - FFWC daily water levels (data availability)
  - EM-DAT / DDM / OCHA / IFRC events catalogue

## 3. Methodology (~1,500 words, numbered subsections)

- 3.1 Climate trend analysis: Mann-Kendall + Sen's slope + Pettitt
  (equations, references to Zhang 2011, Sen 1968, Mann 1945, Pettitt 1979).
- 3.2 SAR flood mapping: Sentinel-1 preprocessing, Otsu thresholding,
  permanent water masking, connected component filter.
- 3.3 Accuracy assessment: confusion matrix, Kappa (Congalton 1991);
  multi-satellite optical reference (S2 + L8 + L9); interpretation
  caveat for change-based vs total-water comparison.
- 3.4 Exposure quantification: population and land-cover extraction.
- 3.5 Trigger derivation: multi-window accumulation sweep, event labels
  with halo, threshold selection criterion.
- 3.6 Skill-score validation: POD, FAR, CSI, HSS, ETS with 2x2
  contingency; calibration 1981-2010, blind validation 2011-2024;
  block bootstrap 95% CI.

## 4. Results (~1,800 words)

- 4.1 Climate trends (Table 1, Fig 1, Fig 1b).
- 4.2 Multi-event inundation extent and accuracy (Table 2, Fig 2).
- 4.3 Exposure quantification (Table 3, Fig 3).
- 4.4 Threshold derivation and validation (Table 4, Fig 4).
- 4.5 Framework integration (Fig 5).

## 5. Discussion (~1,200 words)

- 5.1 What the trend patterns mean: stationary totals but lengthening
  dry spells; potential role of ERA5 pre-1979 discontinuity; trans-
  boundary vs local rainfall.
- 5.2 Comparison to prior work (Akter, Uddin, DeepSAR; positional).
- 5.3 Operational implications: integration path with FFWC + BDRCS +
  Anticipation Hub.
- 5.4 Limitations: 7 SAR events, cloud cover for optical validation,
  no soil moisture, ERA5 pre-1979 discontinuity, limited FFWC record
  for some stations.
- 5.5 Future work: soil moisture, ML classifier comparison, cost-benefit
  study, adding pre-2015 events using Landsat-only SAR-substitute.

## 6. Conclusions (~300 words)

Direct restatement of contributions and next steps. No new material.

## Author contributions (CRediT - single author)

Naimul Islam: Conceptualization, Methodology, Software, Validation,
Formal Analysis, Investigation, Data Curation, Writing - Original Draft,
Writing - Review & Editing, Visualization, Project Administration.

## Declaration of competing interest

None.

## Data availability

Datasets and code available at Zenodo [DOI to be assigned] and GitHub
(https://github.com/Naimul-islam-bd/sylhet_flash_flood_aa). Includes:
CHIRPS extraction, ERA5-Land extractions (Sylhet + trans-boundary),
S1 flood rasters (7 events), events catalogue, Python analysis package.

## Acknowledgements

FFWC for gauge data. OCHA/ReliefWeb for event documentation. Google
Earth Engine for satellite data access.

---

## Table and figure list (target counts)

Tables (7 max recommended):

1. Data sources.
2. ETCCDI trends across three datasets (real data, done).
3. Event-by-event SAR accuracy (7 events, done).
4. Threshold performance (calibration + validation with CIs).
5. Exposure by district.
6. Sensitivity to key parameters.
7. Comparison to prior local studies.

Figures (5 max recommended):

1. Study area map with Sylhet Division polygon + trans-boundary catchment
   (single column, TIFF halftone 300 dpi).
2. Seven-event flood extent panels (full page, combination 500 dpi).
3. Exposure map (single column, TIFF 300 dpi).
4. Skill score curves (full page, PDF vector).
5. Proposed framework (full page, PDF vector).
