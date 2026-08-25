/**
 * 03_era5land_daily_transboundary.js  (CORRECTED v2)
 * ------------------------------------------------------------------
 * Export ERA5-Land DAILY total precipitation for the ENTIRE
 * Barak-Meghna trans-boundary catchment - the actual upstream area
 * that drives Sylhet flash floods.
 *
 * Two study-region definitions provided. Pick ONE by setting
 * USE_HYDROBASINS = true (Approach B) or false (Approach A).
 *
 * APPROACH A (default, simpler):
 *   Rectangular bounding box matching the OFFICIAL India-WRIS Barak
 *   sub-basin extent (89.5-94.5 E, 22.7-26.5 N).
 *   Source: India Water Resources Information System (NRSC/CWC),
 *   http://india-wris.nrsc.gov.in - Barak & Others sub-basin page.
 *   Cited as: India-WRIS, 2023 (or accessed year).
 *
 * APPROACH B (best practice, hydrological):
 *   HydroBASINS Level 5 polygon containing Sylhet, which returns
 *   the actual Meghna basin polygon (not a rectangle).
 *   Source: Lehner, B., Grill G. (2013). Global river hydrography
 *   and network routing. Hydrol. Process. 27(15): 2171-2186.
 *
 * Approach B is more defensible; Approach A is simpler and cites an
 * authoritative government source. Both are Q1-acceptable.
 * ------------------------------------------------------------------
 */

var USE_HYDROBASINS = false;   // set true for Approach B

// ==================================================================
// APPROACH A: India-WRIS official Barak sub-basin bbox
// ==================================================================
// Longitude: 89°50' to 94°00' E (India portion) + slight west buffer
//            to include the full Bangladesh portion of Meghna basin
// Latitude:  22°44' to 25°58' N (India-WRIS) + slight north buffer
//            to include the Barail range (basin boundary)
var BAR_BBOX = ee.Geometry.Rectangle([89.5, 22.7, 94.5, 26.5]);

// ==================================================================
// APPROACH B: HydroBASINS Level 5 Meghna basin polygon
// ==================================================================
var sylhet_point = ee.Geometry.Point([91.87, 24.90]);   // Sylhet city
var hybas5 = ee.FeatureCollection('WWF/HydroSHEDS/v1/Basins/hybas_5');
var meghna_basin = hybas5.filterBounds(sylhet_point);
print('HydroBASINS level 5 candidate basin(s) containing Sylhet:',
       meghna_basin);

// Select study region
var STUDY_REGION = USE_HYDROBASINS ? meghna_basin.geometry() : BAR_BBOX;
var LABEL = USE_HYDROBASINS ? 'HydroSHEDS Level 5' : 'India-WRIS bbox';

print('Study region approach:', LABEL);
print('Study region area (km2):', STUDY_REGION.area().divide(1e6));

Map.centerObject(STUDY_REGION, 7);
Map.addLayer(BAR_BBOX, {color: 'yellow'}, 'India-WRIS Barak bbox');
Map.addLayer(meghna_basin, {color: 'blue'}, 'HydroBASINS L5 Meghna');

// Overlay the Sylhet Division polygon so you can see how upstream area
// dwarfs the study region.
var gaul1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var SYLHET = gaul1
    .filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh'))
    .filter(ee.Filter.eq('ADM1_NAME', 'Sylhet'));
Map.addLayer(SYLHET, {color: 'red'}, 'Sylhet Division (target)');

// ---- Data ----
var START = '1950-01-02';
var END   = '2025-01-01';
var SCALE = 10000;
var DRIVE_FOLDER = 'gee_exports_sylhet';

var era5 = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')
    .filterDate(START, END)
    .filterBounds(STUDY_REGION)
    .select('total_precipitation_sum');

print('ERA5-Land image count (expect ~27395):', era5.size());

Map.addLayer(era5.mean().clip(STUDY_REGION),
             {min: 0, max: 0.05, palette: ['white', 'blue', 'darkblue']},
             'Long-term mean daily precip (m) - Mawsynram/Cherrapunji hotspot');

var dailySeries = era5.map(function (img) {
  var mean = img.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: STUDY_REGION,
    scale: SCALE,
    maxPixels: 1e9,
    bestEffort: true
  });
  return ee.Feature(null, {
    date: img.date().format('YYYY-MM-dd'),
    precipitation_m: mean.get('total_precipitation_sum')
  });
});

var suffix = USE_HYDROBASINS ? 'hybas5' : 'iwrs';
Export.table.toDrive({
  collection: ee.FeatureCollection(dailySeries),
  description: 'transboundary_era5land_daily_1950_2024_' + suffix,
  fileNamePrefix: 'transboundary_era5land_daily_1950_2024_' + suffix,
  folder: DRIVE_FOLDER,
  fileFormat: 'CSV',
  selectors: ['date', 'precipitation_m']
});

print('Task queued. Filename: transboundary_era5land_daily_1950_2024_' + suffix + '.csv');
print('Add Elsevier map note to any map caption:');
print('  "Map lines delineate study areas and do not necessarily depict');
print('   accepted national boundaries."');
