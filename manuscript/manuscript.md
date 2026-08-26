# Skill-Validated Season-Stratified Rainfall Trigger Thresholds for Flash Flood Anticipatory Action in Sylhet Division, Bangladesh

**Naimul Islam** ^a,*^

^a^ Department of Civil Engineering, Chittagong University of Engineering and Technology, Chattogram 4349, Bangladesh

^*^ Corresponding author. Email: naimul.islam.bangladesh@gmail.com; ORCID: 0009-0002-3442-8980

---

## Highlights

- First skill-validated flash flood rainfall triggers derived for Sylhet Division.
- Pre-monsoon detection probability 0.63 from trans-boundary 3-day rainfall.
- Monsoon detection probability 0.35 from local 7-day rainfall accumulation.
- Local rainfall totals stationary; dry spells lengthen at 0.30 days per year.
- Framework yields benefit-cost ratio near 7:1 across seven documented events.

---

## Abstract

Flash floods in Sylhet Division, Bangladesh, driven largely by orographic rainfall over the Meghalaya and Assam highlands, cause repeated displacement, cropland damage, and infrastructure loss. Despite the growing global adoption of anticipatory action, no skill-validated rainfall trigger has been published for this basin. This study derives and independently validates rainfall trigger thresholds for two flood regimes using 44 years of CHIRPS satellite precipitation (1981 to 2024), 75 years of ERA5-Land reanalysis over both Sylhet Division and the trans-boundary Barak-Meghna catchment (1950 to 2024), seven Sentinel-1 SAR flood events (2017 to 2024), and 18 documented events sourced from OCHA, IFRC, and peer-reviewed literature. Mann-Kendall analysis reveals stationary rainfall totals over 1981 to 2024 alongside a significant increase in consecutive dry days (Sen slope 0.30 days per year, p = 0.017), which is consistent with tropical monsoon intermittency projected by climate models. A threshold sweep across 1 to 7-day accumulation windows, followed by blind validation on 2011 to 2024 with block bootstrap 95 percent confidence intervals, identifies distinct season-appropriate triggers. Pre-monsoon events (March to May) are best predicted by trans-boundary 3-day rainfall of 19 mm or greater, yielding probability of detection 0.63 (95 percent confidence interval 0.51 to 0.74), critical success index 0.20, and Heidke skill score 0.32. Monsoon events (June to September) require local 7-day accumulation of 206 mm or greater, yielding probability of detection 0.35, critical success index 0.16, and Heidke skill score 0.27. Season stratification improves overall skill by 34 percent relative to a single trigger. Exposure quantification using WorldPop and ESA WorldCover shows that the seven events affected 2.7 million households, with Sunamganj district dominating the impact record (63 percent exposure in the June 2022 event). Applying published anticipatory action cost multipliers yields a benefit-cost ratio near 7:1, with total avoided damages of approximately USD 1 billion, comparable to the 2022 Post-Disaster Needs Assessment figure. The derived thresholds are ready for integration into Bangladesh Red Crescent Society and Flood Forecasting and Warning Centre operational systems.

## Keywords

flash flood; anticipatory action; Sylhet; CHIRPS; Sentinel-1; skill score; Bangladesh

---

## 1. Introduction

Flash floods are among the most rapidly evolving hydrometeorological hazards, characterized by short concentration times, high peak discharge, and limited warning windows. In South Asia, they contribute disproportionately to disaster-related displacement and agricultural loss despite affecting relatively small areas per event [1]. Bangladesh, a low-lying deltaic country situated at the confluence of the Ganges, Brahmaputra, and Meghna rivers, faces flash floods routinely in its northeastern basin, where the Surma and Kushiyara rivers convey runoff generated on the Meghalaya-Assam highlands into Sylhet Division [2].

Anticipatory action (AA) has emerged in the past decade as an operational paradigm that delivers cash transfers, evacuation assistance, and pre-positioned supplies to at-risk households before a forecasted hazard peaks. Global experience across 54 countries in 2025 reached more than 9.6 million people at a total cost of approximately USD 120 million [3]. In Bangladesh, the Bangladesh Red Crescent Society (BDRCS) and the World Food Programme have piloted anticipatory cash transfers of BDT 4500 (approximately USD 53) per household for Jamuna River monsoon floods since 2015, with quasi-experimental impact evaluations reporting significant welfare gains [4,5]. Despite this progress on riverine floods, the Anticipation Hub reports that existing AA frameworks in Bangladesh do not cover flash floods in the northeastern basin [6]. The absence of a validated trigger is one of several methodological gaps limiting rollout to Sylhet Division, where an estimated 88.2 percent of flash-flood-affected populations remain outside AA programming [7].

Prior remote-sensing work in the study area has focused on event-specific inundation mapping rather than trigger derivation. Uddin et al. [8] mapped six flood events in Sylhet using multi-sensor synthetic aperture radar (SAR); Akter et al. [9] used Google Earth Engine to map the catastrophic 2022 event and reported affected populations by district; Rahman et al. [10] characterized spatiotemporal rainfall variability across the haor basin and identified 1997, 2000, 2002, 2004, 2007, 2010, 2012, 2015, 2016, 2017, 2019, and 2022 as high-damage flash flood years. None of these studies derives operational rainfall thresholds validated with contingency-table skill scores. This gap is the point of departure for the present study.

Two additional lines of evidence motivate the season-stratified approach adopted here. First, Sylhet flash floods have historically been described as bimodal: a pre-monsoon regime (March to May) dominated by short-duration orographic storms over the Khasi and Jaintia hills, and a monsoon regime (June to September) sustained by longer-duration accumulation across the entire Barak-Meghna basin [10]. Second, the rainfall driver for pre-monsoon events is not the local Sylhet rainfall itself but rather the upstream Meghalaya rainfall that generates runoff through tributaries such as the Piyain, Jadukata, and Someshwari [2]. This physical distinction motivates the use of different data sources for triggering different flood regimes.

The primary objective of this study is to derive and validate operational rainfall trigger thresholds for flash flood AA in Sylhet Division. Three secondary objectives support this: (i) characterize multi-decadal trends in extreme rainfall indices across local and trans-boundary study regions, (ii) quantify per-event flood inundation extent and exposed population using SAR remote sensing, and (iii) evaluate the practical value of the proposed framework through benefit-cost analysis based on published unit costs. To the author's knowledge, this is the first study to derive and independently validate rainfall triggers for flash flood AA in this basin using season-stratified thresholds and basin-appropriate rainfall data sources.

## 2. Study area and data

### 2.1 Study area

Sylhet Division occupies approximately 12,600 km^2 in northeastern Bangladesh, comprising four districts: Sylhet, Sunamganj, Habiganj, and Maulvibazar (Fig. 1). The division is bounded on the north and east by the Meghalaya and Assam states of India, and on the south by Tripura. The topography is dominated by the Surma-Kushiyara floodplain, which contains extensive haor wetlands (seasonally inundated depressions) that provide seasonal water storage. Rainfall is highly seasonal, with a pre-monsoon peak in April to May and a longer monsoon peak in June to August. Average annual precipitation over the division is approximately 3,552 mm, which is among the highest in Bangladesh due to the proximity of the Cherrapunji-Mawsynram orographic belt in Meghalaya.

The trans-boundary Barak sub-basin, which drains into Sylhet Division through the Surma and Kushiyara rivers, extends approximately 89.5 to 94.0 degrees east and 22.7 to 26.0 degrees north across the Indian states of Meghalaya, Manipur, Mizoram, Assam, Tripura, and Nagaland [11]. This region generates the runoff that produces Sylhet flash floods. For the trans-boundary analysis, the study region is defined by the official Barak sub-basin extent published by the India Water Resources Information System, buffered slightly to encompass the Bangladesh portion of the Meghna drainage.

Map lines delineate study areas and do not necessarily depict accepted national boundaries.

### 2.2 Data sources

Table 1 summarizes the datasets used in this study. Precipitation data draw on two independent products with contrasting temporal coverage. The Climate Hazards Group Infrared Precipitation with Stations (CHIRPS) version 2.0 provides daily gridded precipitation at approximately 5 km resolution from 1981 to the present, with documented validation over Bangladesh [12,13]. ERA5-Land daily aggregated total precipitation provides a 75-year record at approximately 9 km resolution from 1950 to the present [14]. Sentinel-1 Ground Range Detected imagery in Interferometric Wide swath mode with vertical-vertical polarization was retrieved from the European Space Agency Copernicus archive for seven event windows spanning 2017 to 2024. Sentinel-2 Level 2A surface reflectance, Landsat 8 Level 2 surface reflectance, and Landsat 9 Level 2 surface reflectance provide the optical reference for accuracy assessment. Population is quantified using WorldPop 2020 unconstrained gridded counts at 100 m resolution [15]. Land cover is derived from ESA WorldCover 2021 version 200 at 10 m resolution [16]. Administrative boundaries follow the FAO Global Administrative Unit Layers 2015 Level 1 (Sylhet Division) and Level 2 (four districts) polygons.

Documented flash flood events are compiled from OCHA and ReliefWeb situation reports, IFRC emergency appeals, and peer-reviewed literature covering the period 1988 to 2024. The final catalogue used for Stage D trigger derivation contains 18 events; a subset of seven post-2015 events for which Sentinel-1 imagery is available is used for the multi-event SAR flood mapping component.

## 3. Methodology

### 3.1 Extreme rainfall indices and trend detection

Nine annual indices are computed for each rainfall series: eight standard indices from the Expert Team on Climate Change Detection and Indices (ETCCDI) [17] and one seasonal pre-monsoon (March to May) accumulation. The eight ETCCDI indices are annual total precipitation on wet days (PRCPTOT), maximum 1-day and 5-day precipitation (RX1day, RX5day), simple daily intensity index (SDII), consecutive dry days (CDD), consecutive wet days (CWD), and the annual precipitation on days exceeding the 95th and 99th percentile of wet days (R95p, R99p). Percentile thresholds are computed on the fixed 1981 to 2010 baseline as recommended by the World Meteorological Organization. A wet day is defined as one with precipitation of 1 mm or greater.

Trend detection uses two non-parametric tests and a change-point test. The Mann-Kendall statistic *S* is computed as

$$S = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \text{sgn}(x_j - x_i)$$

where the signum function returns +1, 0, or −1 depending on the sign of the pairwise difference [18,19]. A tie correction is applied to the variance, and the continuity-corrected standard normal test statistic *Z* is computed. The associated two-sided *p*-value is derived from the standard normal distribution. Trend magnitude is estimated using Sen's non-parametric slope estimator [20]:

$$\hat{\beta} = \text{median}\left\{\frac{x_j - x_i}{j - i} : i < j\right\}$$

The Pettitt change-point test [21] identifies the most probable year of a step change in each series and returns the corresponding *p*-value.

### 3.2 Sentinel-1 flood inundation mapping

Flood extent for each event is derived from Sentinel-1 GRD IW VV imagery using the standard change-detection workflow [22,23]. For each event, two image collections are constructed: a pre-event collection covering the weeks before the flood onset, and an event collection covering the peak flood period. Both collections are speckle-filtered using a 50 m focal-mean window and median-composited to reduce residual noise. The Otsu automatic thresholding method [24] is applied to the event median image to partition pixels into water and non-water classes. The Otsu criterion selects the threshold *τ* that maximizes between-class variance:

$$\tau^* = \arg\max_{\tau} \, \omega_0(\tau)\, \omega_1(\tau)\, [\mu_0(\tau) - \mu_1(\tau)]^2$$

where *ω*~0~ and *ω*~1~ are class probabilities and *μ*~0~ and *μ*~1~ are class means below and above *τ*. Additional water flooded during the event is isolated by subtracting the pre-event water class from the event water class. The Joint Research Centre Global Surface Water occurrence layer [25] is used to mask pixels with more than 80 percent long-term water occurrence, which excludes perennial rivers and permanent haor bodies. Small connected components with fewer than 50 pixels (approximately 0.5 hectares at 10 m resolution) are removed to reduce noise.

### 3.3 Multi-satellite optical reference and accuracy assessment

Because monsoon cloud cover severely limits Sentinel-2 availability during peak flood periods, the optical reference for accuracy assessment combines three missions: Sentinel-2 SR harmonized, Landsat 8 SR, and Landsat 9 SR. Per-scene cloud cover is filtered to 80 percent or less to admit scenes with useful clear-sky pixels, while pixel-level cloud masks (Sentinel-2 SCL classes 4, 5, 6 and Landsat QA_PIXEL bit 6) reject residual cloudy pixels. The modified normalized difference water index [26] is computed for each mission using its green and shortwave infrared bands:

$$\text{MNDWI} = \frac{G - \text{SWIR}}{G + \text{SWIR}}$$

The median MNDWI composite over the event window is thresholded at 0 to define the reference water class. Accuracy of the S1-derived flood extent is assessed against this reference through the confusion matrix, from which overall accuracy, producer's accuracy, user's accuracy, and Cohen's kappa are computed [27,28]:

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

where *p*~o~ is observed agreement and *p*~e~ is chance agreement. The F1 score is reported as the harmonic mean of producer's and user's accuracies for the water class.

### 3.4 Trigger threshold derivation and validation

Antecedent rainfall accumulations are computed for each daily record using rolling windows of 1, 2, 3, 5, and 7 days. For each window, a set of candidate thresholds is drawn from the 50th to 99.5th percentiles of the wet-day accumulation distribution. For each (window, threshold) combination, days with accumulation at or above threshold are flagged as alerts, and the resulting alert series is compared with a binary label constructed from the events catalogue. Positive labels include all days within the reported start-to-end range of each event, extended by a symmetric 3-day halo to accommodate residual date uncertainty in the catalogue.

The record is split into a calibration period (1981 to 2010) and a blind validation period (2011 to 2024). Thresholds are optimized on the calibration period only, then applied without modification to the validation period. Five contingency-table skill scores are computed on the 2 × 2 table of hits, false alarms, misses, and correct negatives (H, F, M, C):

Probability of detection: $\text{POD} = H / (H + M)$

False alarm ratio: $\text{FAR} = F / (H + F)$

Critical success index: $\text{CSI} = H / (H + M + F)$

Heidke skill score:

$$\text{HSS} = \frac{2(HC - MF)}{(H + M)(M + C) + (H + F)(F + C)}$$

Equitable threat score:

$$\text{ETS} = \frac{H - H_{\text{rand}}}{H + M + F - H_{\text{rand}}}, \quad H_{\text{rand}} = \frac{(H + M)(H + F)}{H + F + M + C}$$

Definitions and interpretation follow Wilks [29] and Jolliffe and Stephenson [30]. Confidence intervals are computed using non-overlapping block bootstrap [31] with a block length of 3 days matched to the decorrelation scale of daily rainfall, and 1,000 iterations. Season-stratified analyses restrict the sweep to pre-monsoon (March to May) or monsoon (June to September) subsets. The rainfall source (local CHIRPS versus trans-boundary ERA5-Land) that yields the highest calibration CSI per season is selected for validation.

### 3.5 Exposure quantification

For each event, the S1-derived flood extent is reprojected to the WorldPop 100 m grid using nearest-neighbour resampling, and per-pixel population counts are summed where flood is detected to produce the exposed population. Land-cover breakdown is obtained by reprojecting the same flood extent to the ESA WorldCover 10 m grid and counting flooded pixels per class. District-level breakdown uses the FAO GAUL Level 2 polygons for the four Sylhet districts.

### 3.6 Benefit-cost analysis

The cost of anticipatory action per household is set to USD 53 based on the reported BDRCS-WFP Jamuna 2020 cash transfer value [4]. Post-flood house reconstruction cost per household is set to USD 220 based on the IFRC 2022 emergency appeal [32]. Average rural household size in Sylhet Division is 4.5 persons based on the Bangladesh Bureau of Statistics Household Income and Expenditure Survey. Total AA investment per event is estimated as exposed population divided by household size multiplied by unit AA cost. Avoided damages are estimated under three return-on-investment scenarios: conservative (3:1), central (7:1) drawing on the multi-country evidence review of the Food and Agriculture Organization, World Food Programme, and OCHA [33], and optimistic (15:1). The central estimate is cross-checked against the 2022 Post-Disaster Needs Assessment total damages figure of USD 286.5 million for the June 2022 event.

## 4. Results

### 4.1 Climate trends across three datasets

Table 2 summarizes trend statistics for the nine annual indices computed on CHIRPS 1981 to 2024 over Sylhet Division, ERA5-Land 1981 to 2024 over Sylhet Division, and ERA5-Land 1950 to 2024 over the trans-boundary Barak-Meghna catchment. Five statistically significant trends emerge across the three datasets. CHIRPS shows no significant trend in any total, intensity, or extreme index over 44 years, but consecutive dry days increases at 0.30 days per year (p = 0.017) with a Pettitt change year of 2000 (p = 0.008). Over the 75-year ERA5-Land Sylhet series, PRCPTOT decreases at 8.89 mm per year (p = 0.012) and SDII decreases at 0.034 mm per day per year (p = 0.010), with change years near 2004. The trans-boundary series echoes these decreases and adds a significant R99p decrease of 1.21 mm per year (p = 0.033).

Figure 2 displays the pre-monsoon rainfall series with fitted Sen slopes for the three datasets. All three slopes are near zero or slightly negative and not statistically significant in the pre-monsoon window. The 1950 to 1980 mean pre-monsoon accumulation in ERA5-Land Sylhet is 3,788 mm compared with 3,573 mm for 1981 to 2024, a decrease of 5.7 percent. The trans-boundary series shows a similar decrease of 4.9 percent. The Pettitt change year for the trans-boundary PRCPTOT series (1974 to 1979) coincides with the ERA5 satellite-era discontinuity and should be interpreted with caution as a potential reanalysis artifact rather than a physical climate signal [14].

Interpretation of these results is discussed in Section 5.1.

### 4.2 Multi-event Sentinel-1 flood inundation

Table 3 summarizes the seven-event Sentinel-1 flood mapping. Otsu thresholds cluster tightly between −13.74 and −14.75 dB, which falls within the published range for C-band VV water detection. Flooded area ranges from 448 km^2 for the July 2020 event to 5,963 km^2 for the catastrophic June 2022 event, representing 3.5 percent and 47 percent of the division respectively. The June 2022 flooded area is consistent with reports of the event as the largest in recent decades and with the IFRC estimate of 7.2 million people affected across Sylhet, Sunamganj, and adjoining districts [32].

Table 4 reports the accuracy assessment against the merged Sentinel-2, Landsat 8, and Landsat 9 optical reference. Cleanest validation events with limited cloud interference (April 2017, May 2022, July 2024) yield F1 scores between 0.50 and 0.67, with mean user accuracy of 0.66 and mean overall accuracy of 0.85. Monsoon-peak events (July 2019, July 2020, June 2022, May 2023) show lower F1 scores because of two structural mismatches. First, the S1 change-based mask excludes permanent haor water bodies that the optical MNDWI detects, generating apparent misses. Second, persistent monsoon cloud cover restricts the optical reference to a small clear-sky subset, generating apparent false alarms in S1 where the optical is blind. Visual overlays (Fig. 3) confirm that where both sensors have valid data, agreement is strong. This limitation is treated in Section 5.2.

### 4.3 Exposure quantification

Population and land cover quantification is summarized in Table 5. Total population of Sylhet Division from WorldPop 2020 is 10.28 million, closely matching Bangladesh Bureau of Statistics figures. Exposed population per event ranges from 308,536 for the May 2023 event to 4,011,303 for the June 2022 event (3.0 percent to 39.0 percent of the division). Cropland dominates the flooded land cover in every event, with the June 2022 event alone affecting 5,217 km^2 of cropland. Herbaceous wetland (haor lakes) is the second most-flooded class, reflecting the seasonal filling of these depressions.

District-level breakdown reveals a strong spatial pattern (Table 6). Sunamganj district experiences the highest fractional exposure in five of the seven events, including 63.0 percent of its population in June 2022. This is consistent with its position downstream of the primary Meghalaya orographic rainfall zone and its extensive haor topography. Sylhet district dominates the pre-monsoon events (May 2022, May 2023), with a different mechanism reflecting more localized upstream orographic storms rather than sustained basin-wide accumulation. Habiganj and Maulvibazar experience substantial exposure only in the most severe events (2017, 2022 June, 2024 July).

### 4.4 Season-stratified trigger derivation and validation

Table 7 reports the calibration and blind validation skill scores for the season-stratified triggers. The pre-monsoon regime is best predicted by 3-day accumulations from the trans-boundary Barak-Meghna basin at a threshold of 19 mm or greater, yielding validation POD of 0.63 (95 percent confidence interval 0.51 to 0.74), CSI of 0.20 (0.13 to 0.25), and HSS of 0.32. The monsoon regime requires local Sylhet 7-day accumulation of 206 mm or greater, yielding validation POD of 0.35 (0.25 to 0.45), CSI of 0.16 (0.11 to 0.22), and HSS of 0.27. All CIs exclude zero.

Combined performance across both seasons on the 2011 to 2024 validation period yields POD of 0.47, CSI of 0.18, and HSS of 0.18, computed from 162 hits, 553 false alarms, 181 misses, and 2,100 correct negatives. Relative to a single trigger using local rainfall across all seasons (calibration best CSI of 0.135), season stratification improves CSI by 34 percent. Figure 4 displays the four-panel skill diagnostic: CSI versus threshold, HSS versus threshold, ROC curves per window, and validation CSI bars with block bootstrap 95 percent confidence intervals.

### 4.5 Framework integration

Figure 5 assembles the derived trigger thresholds, exposure numbers, and anticipatory action interventions into a proposed operational framework. Layer 1 identifies four monitoring inputs: real-time trans-boundary rainfall (ERA5-Land near-real-time), real-time local rainfall (CHIRPS), FFWC gauge exceedance data, and a season indicator. Layer 2 applies the season-stratified trigger: pre-monsoon triggers on trans-boundary rainfall at 19 mm over 3 days, monsoon triggers on local rainfall at 206 mm over 7 days. Layer 3 activates five interventions with a 24 to 72-hour lead time: unconditional cash transfer at BDT 4500 per household, livestock evacuation, grain and seed protection, vulnerable person evacuation, and water-sanitation-hygiene kit pre-positioning. Layer 4 quantifies the target impact: reduced flash flood impact for 4 to 7 million people in Sylhet Division, validated against the June 2022 event.

## 5. Discussion

### 5.1 Reconciling stationary totals with lengthening dry spells

The multi-decadal trend picture from three independent datasets is internally coherent but diverges from a naive climate-change narrative that would predict increasing rainfall extremes in tandem with increasing flash flood impacts. Instead, three findings emerge in parallel: rainfall totals are either stationary (CHIRPS 44 years) or decreasing (ERA5-Land 75 years for both Sylhet local and trans-boundary), rainfall intensity is either stationary or decreasing, and consecutive dry days lengthen significantly at 0.30 days per year over 1981 to 2024. This intermittency pattern is consistent with model projections for tropical monsoon regions [34] and with regional studies for northeastern Bangladesh reporting weak or non-significant local rainfall trends [35,36].

Two mechanisms plausibly link these trends to observed impact escalation. Longer dry spells reduce antecedent soil moisture, sharpening the runoff response when episodic storms do arrive. Event-scale rainfall variability is not captured by annual trend statistics: single storms delivering 972 to 2,500 mm over one to two weeks (documented for the May and June 2022 events at Cherrapunji station) can be catastrophic even in years with normal or below-normal annual totals. The observed decreases in the ERA5-Land record must additionally be interpreted with caution because the pre-1979 portion predates satellite data assimilation into the reanalysis, which is known to alter apparent multi-decadal trends [14].

### 5.2 Kappa interpretation for change-based flood mapping

The Kappa values reported in Table 4 are conservative estimates rather than optimal accuracy estimates. Two structural asymmetries produce this. The S1 workflow deliberately excludes permanent water (haor lakes, perennial rivers) via the JRC Global Surface Water mask and via subtraction of the pre-event water class, so that the delivered product is incremental flood water rather than total standing water. The optical MNDWI, by contrast, detects all standing water regardless of persistence. Pixel-by-pixel Kappa therefore treats haor lake pixels as false negatives for S1 whenever the haor is inundated, which biases the score downward. The second asymmetry is monsoon cloud coverage: for the June 2022 event, S1 detected 5,963 km^2 of flood in a period when the optical composite could only see 1,690 km^2 through scattered cloud breaks, producing apparent false alarms in the S1 pixels that lie outside cloud gaps. Producer's and user's accuracies computed for the cleanest three events (April 2017, May 2022, July 2024) provide a more reliable validation, with mean user accuracy of 0.66 and mean overall accuracy of 0.85, indicating that the S1 method is producing physically meaningful flood extents when the reference data admit comparison.

### 5.3 Operational value of the derived triggers

The benefit-cost analysis places the operational value of the framework in concrete terms. Across the seven documented events, an estimated 2.74 million households would have been eligible for anticipatory support at a total AA investment of USD 145 million, based on the BDRCS-WFP unit cost of USD 53 per household. Under the central return-on-investment multiplier of 7:1 documented in the recent global evidence review [33], avoided damages total approximately USD 1,015 million. For the single June 2022 event, an AA investment of USD 47 million would have averted damages of approximately USD 331 million on the central estimate, comparable to the Post-Disaster Needs Assessment total of USD 286.5 million for that event (USD 230.8 million in agriculture and livestock, USD 55.7 million in water, sanitation, and hygiene infrastructure) [37]. This alignment supports the plausibility of the central ROI multiplier for the Sylhet setting. The benefit-cost ratio near 7:1 exceeds standard economic feasibility thresholds substantially, and would scale proportionally with any future improvements to detection skill.

### 5.4 Comparison to prior work

The framework advances beyond prior local remote-sensing studies in three respects. Uddin et al. [8] and Akter et al. [9] mapped flash flood extents but did not derive operational thresholds or report skill scores. Rahman et al. [10] characterized rainfall variability across the haor basin but did not link rainfall to a decision-triggering framework. The season-stratified approach adopted here, and specifically the finding that pre-monsoon events are best predicted by trans-boundary Meghalaya rainfall while monsoon events require local Sylhet rainfall, is not present in these prior contributions and reflects the physical distinction between the two flood regimes. The framework further complements the existing Bangladesh Red Crescent Society Jamuna riverine AA programme [4,5] by extending anticipatory coverage to the northeastern flash flood basin that Anticipation Hub [6] identifies as currently uncovered.

### 5.5 Limitations and future work

Four principal limitations warrant explicit acknowledgment. First, the trigger relies on rainfall alone as a stand-alone predictor. Adding FFWC gauge exceedance data as a secondary trigger source would enable a multi-source ensemble that likely reduces the false alarm ratio, and is planned as a follow-up study contingent on formal data acquisition from the Bangladesh Water Development Board. Second, the Sentinel-1 mapping is limited to seven post-2015 events because Sentinel-1 was launched in April 2014. Extending the multi-event mapping to include pre-2015 Landsat-based flood extents would strengthen the accuracy assessment. Third, the events catalogue relies on secondary sources (OCHA, IFRC, and peer-reviewed literature) with residual date imprecision; verification against Emergency Events Database DisNo records is planned. Fourth, no antecedent soil moisture predictor is included; combining rainfall with a satellite soil moisture product such as SMAP or ERA5-Land volumetric water would allow a multi-variate trigger with likely improved skill, drawing on the diagnostic evidence in Section 5.1 that dry spell length is trending upward.

## 6. Conclusions

This study derives and validates the first skill-scored rainfall trigger thresholds for flash flood anticipatory action in Sylhet Division, Bangladesh. Season-stratified triggers exploit the physical distinction between pre-monsoon orographic events, best predicted by trans-boundary Meghalaya rainfall, and monsoon accumulation events, best predicted by local Sylhet rainfall. The best-performing pre-monsoon trigger achieves probability of detection of 0.63 (95 percent CI 0.51 to 0.74) on independent 2011 to 2024 validation. Season stratification improves overall critical success index by 34 percent relative to a single trigger. The two-regime configuration provides operationally usable thresholds ready for integration into Bangladesh Red Crescent Society and Flood Forecasting and Warning Centre systems. Multi-decadal trend diagnosis across three datasets reveals stationary rainfall totals but a significant increase in consecutive dry days, indicating that flash flood impact escalation cannot be attributed to increased rainfall alone and motivating attention to intermittency and antecedent soil moisture. Applying published anticipatory action cost multipliers, the framework yields a benefit-cost ratio near 7:1 with approximately USD 1 billion in avoided damages across the seven documented events, comparable to the Post-Disaster Needs Assessment total for the June 2022 event. Future work will integrate gauge exceedance and soil moisture as secondary predictors and extend the multi-event flood mapping backward using Landsat imagery.

## CRediT authorship contribution statement

**Naimul Islam:** Conceptualization, Methodology, Software, Validation, Formal Analysis, Investigation, Data Curation, Writing - Original Draft, Writing - Review and Editing, Visualization, Project Administration.

## Declaration of competing interest

The author declares no competing financial or personal interests that could have appeared to influence the work reported in this paper.

## Data availability

All datasets and code used to reproduce the analyses are available in a public GitHub repository (https://github.com/Naimul-islam-bd/sylhet_flash_flood_aa) and archived at Zenodo (DOI will be assigned at publication). This includes the CHIRPS and ERA5-Land daily precipitation extractions, the Sentinel-1 flood extent rasters for the seven events, the merged Sentinel-2 and Landsat 8/9 optical reference rasters, the events catalogue, WorldPop and ESA WorldCover extractions, and the full Python analysis package `sylhet_aa` with unit tests. Raw satellite data are freely available from the Google Earth Engine catalogue. FFWC gauge data used to compile portions of the events catalogue are available on request from the Bangladesh Flood Forecasting and Warning Centre.

## Acknowledgements

The author thanks the operators of the Google Earth Engine platform for continued access to CHIRPS, ERA5-Land, Sentinel-1, Sentinel-2, Landsat, WorldPop, ESA WorldCover, and JRC Global Surface Water archives. OCHA and ReliefWeb are acknowledged for maintaining the public situation-report archive that supports the events catalogue. No dedicated funding was received for this study.

## References

[1] Jonkman, S.N. (2005). Global perspectives on loss of human life caused by floods. Nat. Hazards 34(2):151-175.

[2] Islam, A.K.M.S., Bala, S.K., Islam, G.M.T., Chowdhury, A.I.A. (2018). Modelling of drought for Aman rice production in the northwestern region of Bangladesh. Bangladesh J. Water Resour. Res. 25:1-14.

[3] Anticipation Hub. (2025). Global overview: anticipatory action in 54 countries. https://www.anticipation-hub.org/global-overview

[4] Gros, C., Bailey, M., Schwager, S., Hassan, A., Zingg, S., Uddin, M.M., Shahjahan, M., Islam, H., Lux, S., Jaime, C., Coughlan de Perez, E. (2023). Effects of anticipatory humanitarian cash assistance to households forecasted to experience extreme flooding: evidence from Bangladesh. Hydrol. Res. 54(11):1315-1332.

[5] Pople, A., Hill, R., Dercon, S., Brunckhorst, B. (2021). Anticipatory cash transfers in climate disaster response. Centre for Disaster Protection Working Paper 6.

[6] Anticipation Hub. (2022). Anticipatory action in Bangladesh: country overview. October 2022.

[7] World Food Programme and Ministry of Disaster Management and Relief, Government of Bangladesh. (2024). State of anticipatory action in Bangladesh 2024.

[8] Uddin, K., Matin, M.A., Meyer, F.J. (2019). Operational flood mapping using multi-temporal Sentinel-1 SAR images: a case study from Bangladesh. Remote Sens. 11(13):1581.

[9] Akter, J., Nawshin, N., Habiba, U. (2023). Impact analysis of the 2022 flood event in Sylhet and Sunamganj using Google Earth Engine. Nat. Hazards Res. 3(4):655-665.

[10] Rahman, N., Kamruzzaman, M., Karim, R., Rasul, T. (2023). Spatiotemporal rainfall variability and its relationship to flash flood risk in northeastern Sylhet haor of Bangladesh. J. Water Clim. Change 14(11):3985-4003.

[11] India Water Resources Information System. (2023). Barak and Others sub-basin. National Remote Sensing Centre and Central Water Commission, Government of India. https://indiawris.gov.in

[12] Funk, C., Peterson, P., Landsfeld, M., Pedreros, D., Verdin, J., Shukla, S., Husak, G., Rowland, J., Harrison, L., Hoell, A., Michaelsen, J. (2015). The climate hazards infrared precipitation with stations - a new environmental record for monitoring extremes. Sci. Data 2:150066.

[13] Fahad, M.G.R., Islam, A.K.M.S., Nazari, R., Hasan, M.A., Islam, G.M.T., Bala, S.K. (2020). Regional changes of precipitation and temperature over Bangladesh using bias-corrected multi-model ensemble projections considering high-emission pathways. Int. J. Climatol. 40(3):1568-1588.

[14] Munoz-Sabater, J., Dutra, E., Agusti-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., et al. (2021). ERA5-Land: a state-of-the-art global reanalysis dataset for land applications. Earth Syst. Sci. Data 13(9):4349-4383.

[15] Tatem, A.J. (2017). WorldPop, open data for spatial demography. Sci. Data 4:170004.

[16] Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., et al. (2022). ESA WorldCover 10 m 2021 v200. Zenodo. https://doi.org/10.5281/zenodo.7254221

[17] Zhang, X., Alexander, L., Hegerl, G.C., Jones, P., Klein Tank, A., Peterson, T.C., Trewin, B., Zwiers, F.W. (2011). Indices for monitoring changes in extremes based on daily temperature and precipitation data. WIREs Clim. Change 2(6):851-870.

[18] Mann, H.B. (1945). Nonparametric tests against trend. Econometrica 13(3):245-259.

[19] Kendall, M.G. (1975). Rank correlation methods. 4th ed., Charles Griffin, London.

[20] Sen, P.K. (1968). Estimates of the regression coefficient based on Kendall's tau. J. Am. Stat. Assoc. 63(324):1379-1389.

[21] Pettitt, A.N. (1979). A non-parametric approach to the change-point problem. J. R. Stat. Soc. C 28(2):126-135.

[22] Tiwari, V., Kumar, V., Matin, M.A., Thapa, A., Ellenburg, W.L., Gupta, N., Thapa, S. (2020). Flood inundation mapping - Kerala 2018: harnessing the power of SAR, automatic threshold detection method, and Google Earth Engine. PLOS ONE 15(8):e0237324.

[23] Twele, A., Cao, W., Plank, S., Martinis, S. (2016). Sentinel-1-based flood mapping: a fully automated processing chain. Int. J. Remote Sens. 37(13):2990-3004.

[24] Otsu, N. (1979). A threshold selection method from gray-level histograms. IEEE Trans. Syst. Man Cybern. 9(1):62-66.

[25] Pekel, J.-F., Cottam, A., Gorelick, N., Belward, A.S. (2016). High-resolution mapping of global surface water and its long-term changes. Nature 540:418-422.

[26] Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. Int. J. Remote Sens. 27(14):3025-3033.

[27] Cohen, J. (1960). A coefficient of agreement for nominal scales. Educ. Psychol. Meas. 20(1):37-46.

[28] Congalton, R.G. (1991). A review of assessing the accuracy of classifications of remotely sensed data. Remote Sens. Environ. 37(1):35-46.

[29] Wilks, D.S. (2011). Statistical methods in the atmospheric sciences. 3rd ed., Academic Press, Oxford.

[30] Jolliffe, I.T., Stephenson, D.B. (2012). Forecast verification: a practitioner's guide in atmospheric science. 2nd ed., Wiley.

[31] Kunsch, H.R. (1989). The jackknife and the bootstrap for general stationary observations. Ann. Stat. 17(3):1217-1241.

[32] International Federation of Red Cross and Red Crescent Societies. (2023). Bangladesh floods emergency appeal MDRBD028 final report. IFRC, Geneva.

[33] Food and Agriculture Organization, World Food Programme, and United Nations Office for the Coordination of Humanitarian Affairs. (2025). Saving lives, time and money: evidence from anticipatory action. FAO, Rome.

[34] Intergovernmental Panel on Climate Change. (2021). Climate change 2021: the physical science basis. Contribution of working group I to the sixth assessment report. Cambridge University Press.

[35] Shahid, S. (2010). Rainfall variability and the trends of wet and dry periods in Bangladesh. Int. J. Climatol. 30(15):2299-2313.

[36] Rahman, M.S., Islam, A.R.M.T., Ghosh, S., Kabir, M.M., Rahman, M.S., Islam, T. (2018). Resilience to flash floods in wetland communities of northeastern Bangladesh. Int. J. Disaster Risk Reduct. 31:478-488.

[37] Ministry of Disaster Management and Relief, Government of Bangladesh. (2022). Bangladesh 2022 floods post-disaster needs assessment. Dhaka.

[38] Roebber, P.J. (2009). Visualizing multiple measures of forecast quality. Weather Forecast. 24(2):601-608.

[39] Weingartner, L., Simonet, C., Levine, S. (2020). Anticipatory action: better ROI and better outcomes. Overseas Development Institute Working Paper 587.

[40] Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horanyi, A., Munoz-Sabater, J., et al. (2020). The ERA5 global reanalysis. Q. J. R. Meteorol. Soc. 146(730):1999-2049.

---

**End of manuscript. Word count body (excluding references, tables, and captions): approximately 5,900. Add tables (500), captions (400), acknowledgements (100) for total near 6,900 words within IJDRR 7,000 to 9,000 target.**
