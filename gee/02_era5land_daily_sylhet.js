/**
 * 02_era5land_daily_sylhet.js  (CORRECTED v2)
 * ------------------------------------------------------------------
 * Export ERA5-Land DAILY total precipitation for Sylhet Division
 * (FAO GAUL Level 1 official administrative boundary) from 1950 to
 * 2024 as a CSV. This gives a 75-year rainfall record for long-term
 * climate trend analysis.
 *
 * total_precipitation_sum is in METRES per day; the Python loader
 * (sylhet_aa.data.load.load_daily_rainfall) auto-converts to mm.
 *
 * Data reference: Munoz-Sabater et al. (2021), Earth Syst. Sci. Data 13.
 * ------------------------------------------------------------------
 */

// ---- OFFICIAL Sylhet Division polygon ----
var gaul1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var SYLHET = gaul1
    .filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh'))
    .filter(ee.Filter.eq('ADM1_NAME', 'Sylhet'));

Map.centerObject(SYLHET, 8);
Map.addLayer(SYLHET, {color: 'red'}, 'Sylhet Division (FAO GAUL 2015)');

// ---- Data ----
var START = '1950-01-02';
var END   = '2025-01-01';
var SCALE = 10000;   // coarse enough for reasonable CSV size
var DRIVE_FOLDER = 'gee_exports_sylhet';

var era5 = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')
    .filterDate(START, END)
    .filterBounds(SYLHET)
    .select('total_precipitation_sum');

print('ERA5-Land image count (expect ~27395):', era5.size());

Map.addLayer(era5.mean().clip(SYLHET),
             {min: 0, max: 0.03, palette: ['white', 'blue']},
             'Long-term mean daily precip (m) over Sylhet');

var dailySeries = era5.map(function (img) {
  var mean = img.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: SYLHET.geometry(),
    scale: SCALE,
    maxPixels: 1e9,
    bestEffort: true
  });
  return ee.Feature(null, {
    date: img.date().format('YYYY-MM-dd'),
    precipitation_m: mean.get('total_precipitation_sum')
  });
});

Export.table.toDrive({
  collection: ee.FeatureCollection(dailySeries),
  description: 'sylhet_era5land_daily_1950_2024_gaul',
  fileNamePrefix: 'sylhet_era5land_daily_1950_2024_gaul',
  folder: DRIVE_FOLDER,
  fileFormat: 'CSV',
  selectors: ['date', 'precipitation_m']
});

print('Task queued. Filename: sylhet_era5land_daily_1950_2024_gaul.csv');
print('This export takes 1-2 hours. Safe to close the browser tab.');
