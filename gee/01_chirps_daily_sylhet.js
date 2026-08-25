/**
 * 01_chirps_daily_sylhet.js  (CORRECTED v2)
 * ------------------------------------------------------------------
 * Export CHIRPS v2.0 DAILY rainfall for Sylhet Division, 1981-2024
 * as CSV. Now uses the FAO GAUL Level 1 official administrative
 * boundary of Sylhet Division instead of an arbitrary bounding box.
 *
 * Reviewer defense: "The study region is defined by the official
 * FAO/GAUL 2015 Level 1 administrative boundary of Sylhet Division,
 * Bangladesh (Food and Agriculture Organization of the United Nations,
 * 2015). Basin-averaged daily precipitation is computed within this
 * polygon."
 *
 * Data reference: Funk et al. (2015), Scientific Data 2:150066.
 * ------------------------------------------------------------------
 */

// ---- OFFICIAL Sylhet Division polygon ----
var gaul1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var SYLHET = gaul1
    .filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh'))
    .filter(ee.Filter.eq('ADM1_NAME', 'Sylhet'));

print('Sylhet Division feature count (should be 1):', SYLHET.size());
print('Sylhet Division area (km2):',
       SYLHET.geometry().area().divide(1e6));

Map.centerObject(SYLHET, 8);
Map.addLayer(SYLHET, {color: 'red'}, 'Sylhet Division (FAO GAUL 2015)');

// ---- Data ----
var START = '1981-01-01';
var END   = '2025-01-01';    // exclusive
var SCALE = 5000;
var DRIVE_FOLDER = 'gee_exports_sylhet';

var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
    .filterDate(START, END)
    .filterBounds(SYLHET)
    .select('precipitation');

print('CHIRPS image count (expect ~16071):', chirps.size());

Map.addLayer(chirps.mean().clip(SYLHET),
             {min: 0, max: 30, palette: ['white', 'blue']},
             'Long-term mean daily rain over Sylhet');

var dailySeries = chirps.map(function (img) {
  var mean = img.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: SYLHET.geometry(),
    scale: SCALE,
    maxPixels: 1e9,
    bestEffort: true
  });
  return ee.Feature(null, {
    date: img.date().format('YYYY-MM-dd'),
    precipitation_mm: mean.get('precipitation')
  });
});

Export.table.toDrive({
  collection: ee.FeatureCollection(dailySeries),
  description: 'sylhet_chirps_daily_1981_2024_gaul',
  fileNamePrefix: 'sylhet_chirps_daily_1981_2024_gaul',
  folder: DRIVE_FOLDER,
  fileFormat: 'CSV',
  selectors: ['date', 'precipitation_mm']
});

print('Task queued. Filename: sylhet_chirps_daily_1981_2024_gaul.csv');
