# REVIEWER DEFENSE DOCUMENT

For every anticipated Q1 reviewer question, prepare the honest,
methodologically defensible answer BEFORE submission. If any of these
cannot be answered, do not submit.

---

## Q1. What is genuinely novel here? Isn't rainfall threshold-based flood
## forecasting well established?

**Answer:** Threshold-based forecasting is established for river floods
using GloFAS + FFWC (e.g. Jamuna BDRCS AA program). It is not established
for flash floods in the NE Bangladesh basin. The Anticipation Hub
(October 2022) explicitly notes existing AA models do not cover the NE.
Prior local work (Akter et al. 2023; Uddin et al. 2019; DeepSAR 2025) does
event-specific inundation mapping but does not derive operational trigger
thresholds and does not report skill-score validation. This paper fills
that specific gap.

---

## Q2. Why does your CHIRPS trend analysis show no significant trend in
## rainfall totals, despite global evidence of increasing extremes?

**Answer:** Two-part answer. First, local Sylhet rainfall totals are
stationary but dry-spell length is INCREASING significantly (CDD +0.30
days/yr, p=0.017), which is consistent with the IPCC AR6 pattern for
tropical monsoon regions: more intermittent rainfall. Second, Sylhet
sits at the tail of the Meghalaya-Assam orographic system, and flash
flood generation depends on trans-boundary rainfall over the Khasi-
Jaintia Hills. Our Stage A analysis on ERA5-Land over the trans-boundary
catchment (India-WRIS Barak sub-basin extent) provides the complementary
picture and shows similar patterns to local Sylhet. Our finding of local
total stationarity is consistent with, e.g., Shahid (2010) J Water
Climate Change, and Uddin (2019).

---

## Q3. Seven flash flood events for SAR validation is a modest set. How
## can you claim robust triggers?

**Answer:** Seven events for Sentinel-1 inundation mapping (Stage B).
For trigger derivation (Stage D) the full 1981-2024 CHIRPS record is used
with a 20+ event catalogue verified against EM-DAT, DDM, OCHA, and IFRC
primary sources. Calibration is 1981-2010, blind validation is 2011-2024.
Confidence intervals use block bootstrap (Kunsch 1989, block length = 3
days matching daily rainfall decorrelation). We report ETS to account for
chance hits given the low event base rate.

---

## Q4. Why CHIRPS and not gauge data?

**Answer:** Gauge networks in Sylhet are sparse and have documented
temporal gaps. CHIRPS has been validated for Bangladesh by Fahad et al.
(2020) and others, correlation r > 0.75 against gauge data at daily scale
for the NE region. ERA5-Land is included as a robustness check
(independent data source, independent processing chain).

---

## Q5. Otsu thresholding for SAR is old. Why not use a modern
## classifier?

**Answer:** Reproducibility. Otsu is deterministic, requires no training
data, and has been validated at scale (e.g. GFM/Copernicus EMS). Machine
learning classifiers (DeepSAR 2025) are more accurate on labelled test
sets but their performance depends on training data quality. Since our
downstream use (trigger derivation) depends on binary flood extent, the
marginal accuracy gain of ML does not justify the reproducibility cost
for this study. Otsu threshold values across our seven events ranged
from -13.7 to -14.75 dB, exactly the published range for C-band VV water
detection - a strong internal consistency signal.

---

## Q6. Speckle filtering with focal mean is crude.

**Answer:** Focal mean at 50 m for 10 m SAR (5-pixel window) preserves
flood edges. We tested Refined Lee and Boxcar; results within 3% for
flood area. Retained focal mean for simplicity and reproducibility. Full
sensitivity in supplementary S3.

---

## Q7. Why exclude permanent water using JRC GSW at 80% occurrence?

**Answer:** JRC GSW (Pekel et al. 2016) is the standard reference for
permanent water. 80% occurrence excludes rivers and lakes while retaining
seasonally flooded areas that are genuinely part of flash flood extent.
Threshold verified against local knowledge of Surma-Kushiyara river
extents and Sylhet haor basin coverage.

---

## Q8. Your Stage B pixel-level Kappa values range from -0.01 to 0.57.
## The lower values look poor. How do you defend the S1 method?

**Answer:** Kappa here is a conservative metric because S1 change-based
flood mapping and optical MNDWI measure different phenomena: S1 detects
INCREMENTAL flood water (change from pre-event baseline, permanent water
masked via JRC GSW), while optical detects ALL standing water including
permanent haor lakes. Visual overlays (Fig 2 supplementary) show that
where BOTH sensors have valid data (i.e., where optical is not
cloud-obscured), agreement is strong. For events with least confounding
(2017 April, 2022 May, 2024 July - low cloud, moderate haor filling),
mean F1 = 0.60, mean User accuracy = 0.66, mean Overall accuracy = 0.85.
For catastrophic 2022 June, S1 detected 5963 km2 of flood versus 1690 km2
visible through cloud breaks by optical; this cloud-related underestimation
by optical is a known limitation of monsoon-period optical validation
(Ghatak et al 2018), and precisely why SAR was chosen for the primary
mapping.

---

## Q9. Your validation period (2011-2024) includes events that may have
## informed your Stage B threshold choice. Is this circular?

**Answer:** No. Stage B (SAR flood mapping, 7 events) is entirely
independent of Stage D (rainfall trigger). Stage D thresholds are fit on
CHIRPS + FFWC 1981-2010 without any reference to the Stage B SAR maps.
Validation uses 2011-2024 rainfall + FFWC + documented event dates from
independent sources (EM-DAT etc.), not the Stage B S1 rasters.

---

## Q10. What is FFWC gauge exceedance? Which stations?

**Answer:** FFWC (Flood Forecasting and Warning Centre, Bangladesh) daily
water level records for stations at Sunamganj, Sylhet, Amalshid,
Sheola, and Sherpur-Sylhet. Danger level exceedance is the operational
FFWC definition (station-specific). We use exceedance flags supplied in
FFWC annual reports and the historical data request response (data
availability statement).

---

## Q11. Why no antecedent soil moisture in your trigger?

**Answer:** Available operational data for Sylhet is rainfall. Adding
soil moisture (SMAP, GLDAS, or ERA5-Land volumetric water) is the natural
next study. This limitation is flagged as future work. The paper's
scope is deliberately a minimum viable operational trigger from currently
available operational data. Notably, Stage A found increasing dry-spell
length (CDD +0.30 days/yr) which supports soil moisture as a plausible
mechanism for flood intensification despite stationary rainfall totals.

---

## Q12. Your CSI target of 0.4 is low. Real forecasters want 0.6+.

**Answer:** For rare events (< 5% base rate) CSI values of 0.4-0.5 are
consistent with operational skill (Roebber 2009). Our comparison is to
climatology (CSI at climatology = base rate x 1 = ~0.03), not to zero.
ETS is also reported to account for chance. If ETS > 0.3 the trigger
adds value over random guessing.

---

## Q13. Skill scores without confidence intervals are not defensible.

**Answer:** All validation-period skill scores are reported with block
bootstrap 95% CIs (Kunsch 1989, N=1000, block length 3 days). See Table 4
column suffixes _lo, _hi.

---

## Q14. Your framework figure (Fig 5) has specific numbers - lead time
## 3-5 days, cost-per-beneficiary, etc. Where do those come from?

**Answer:** From WFP/MoDMR State of AA in Bangladesh (2024) and BDRCS AA
program financials (2023). Any number not sourced there is labelled
"proposed" not "measured". Fig 5 is a proposed framework, not an
evaluated deployment.

---

## Q15. The paper claims to inform operational AA. What is the
## implementation pathway?

**Answer:** Discussion section outlines: (1) share thresholds with FFWC
and BDRCS for pilot integration; (2) recommend inclusion in the
Anticipation Hub trigger database; (3) update as new events accumulate
(re-fit annually). Explicit that operational deployment requires
institutional decisions beyond the scope of this paper.

---

## GOING TO SUBMISSION READY

Before submission, complete this checklist:

- [ ] Every reviewer question above has a defensible answer with a source.
- [ ] Table 4 shows CSI, HSS, ETS with 95% CIs, calibration and validation.
- [ ] All figures pass IJDRR resolution check (see 04_ijdrr_rules_checklist.md).
- [ ] Data availability statement lists Zenodo DOI for events catalogue and
      Stage B rasters.
- [ ] Code availability statement lists GitHub repository.
- [ ] CRediT contributor statement drafted (single author covers all roles).
- [ ] Cover letter drafted.
- [ ] Self-review pass complete; consider one external reader.
