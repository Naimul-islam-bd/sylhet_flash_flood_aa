/**
 * 05_sentinel2_validation.js  (v3 - MULTI-SATELLITE OPTICAL)
 * ------------------------------------------------------------------
 * Reference water mask for Stage B accuracy assessment. Combines:
 *   - Sentinel-2 SR (10 m, from 2015)
 *   - Landsat-8 SR (30 m, from 2013)
 *   - Landsat-9 SR (30 m, from 2021)
 *
 * All three converted to a common MNDWI water mask and merged into
 * a single ImageCollection. Per-scene cloud tolerance raised to 80%
 * because pixel-level QA masking (SCL for S2, QA_PIXEL bit-6 for
 * Landsat) handles actual clouds; scene-level filter only keeps
 * scenes that have SOME useful pixels.
 *
 * Handles empty-collection case gracefully with a check + informative
 * error message.
 *
 * Study region: FAO GAUL 2015 Level 1 polygon for Sylhet Division.
 *
 * Reference: Xu (2006) IJRS 27(14) - MNDWI = (Green - SWIR1)/(Green + SWIR1)
 * ------------------------------------------------------------------
 */

var EVENT_ID = 'ev_2019_jul';

var EVENTS = {
  'ev_2017_apr': {start: '2017-03-28', end: '2017-05-15'},
  'ev_2019_jul': {start: '2019-07-05', end: '2019-07-25'},
  'ev_2020_jul': {start: '2020-06-25', end: '2020-07-31'},
  'ev_2022_may': {start: '2022-05-11', end: '2022-05-25'},
  'ev_2022_jun': {start: '2022-06-15', end: '2022-06-30'},
  'ev_2023_may': {start: '2023-05-10', end: '2023-05-30'},
  'ev_2024_jul': {start: '2024-05-27', end: '2024-07-31'}
};

var EV = EVENTS[EVENT_ID];
if (EV === undefined) throw new Error('EVENT_ID not in catalogue.');

// ---- Sylhet Division polygon (FAO GAUL 2015 Level 1) ----
var gaul1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var SYLHET_FC = gaul1
    .filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh'))
    .filter(ee.Filter.eq('ADM1_NAME', 'Sylhet'));
var REGION = SYLHET_FC.geometry();

var DRIVE_FOLDER = 'gee_exports_sylhet';
var CLOUD_MAX_SCENE = 80;   // per-scene cloud cover threshold (%)
Map.centerObject(REGION, 8);
Map.addLayer(SYLHET_FC, {color: 'red'}, 'Sylhet Division');

// ================================================================
// SATELLITE 1: Sentinel-2 SR (Bands B3 = green, B11 = SWIR1)
// ================================================================
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterDate(EV.start, EV.end)
    .filterBounds(REGION)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', CLOUD_MAX_SCENE))
    .map(function (img) {
      // SCL classes: 4=vegetation, 5=bare, 6=water, 11=snow (keep valid land+water)
      var scl = img.select('SCL');
      var good = scl.eq(4).or(scl.eq(5)).or(scl.eq(6)).or(scl.eq(11));
      var mndwi = img.updateMask(good)
                     .normalizedDifference(['B3', 'B11'])
                     .rename('MNDWI');
      return mndwi.copyProperties(img, ['system:time_start']).set('sensor', 'S2');
    });

// ================================================================
// SATELLITE 2: Landsat-8 SR (Bands SR_B3 = green, SR_B6 = SWIR1)
// ================================================================
var l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    .filterDate(EV.start, EV.end)
    .filterBounds(REGION)
    .filter(ee.Filter.lt('CLOUD_COVER', CLOUD_MAX_SCENE))
    .map(function (img) {
      // QA_PIXEL bit 6 = clear pixel (per USGS Landsat 8-9 Level-2 spec)
      var qa = img.select('QA_PIXEL');
      var clear = qa.bitwiseAnd(1 << 6).neq(0);
      var mndwi = img.updateMask(clear)
                     .normalizedDifference(['SR_B3', 'SR_B6'])
                     .rename('MNDWI');
      return mndwi.copyProperties(img, ['system:time_start']).set('sensor', 'L8');
    });

// ================================================================
// SATELLITE 3: Landsat-9 SR (same bands as L8)
// ================================================================
var l9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
    .filterDate(EV.start, EV.end)
    .filterBounds(REGION)
    .filter(ee.Filter.lt('CLOUD_COVER', CLOUD_MAX_SCENE))
    .map(function (img) {
      var qa = img.select('QA_PIXEL');
      var clear = qa.bitwiseAnd(1 << 6).neq(0);
      var mndwi = img.updateMask(clear)
                     .normalizedDifference(['SR_B3', 'SR_B6'])
                     .rename('MNDWI');
      return mndwi.copyProperties(img, ['system:time_start']).set('sensor', 'L9');
    });

// ---- Combine all three ----
var combined = s2.merge(l8).merge(l9);

var n_s2 = s2.size();
var n_l8 = l8.size();
var n_l9 = l9.size();
var n_total = combined.size();
print('S2  scenes (cloud <' + CLOUD_MAX_SCENE + '%):', n_s2);
print('L8  scenes (cloud <' + CLOUD_MAX_SCENE + '%):', n_l8);
print('L9  scenes (cloud <' + CLOUD_MAX_SCENE + '%):', n_l9);
print('Total optical scenes for ' + EVENT_ID + ':', n_total);

// ---- Graceful empty-collection handling ----
if (n_total.getInfo() === 0) {
  print('===============================================================');
  print('ERROR: No cloud-free optical scenes in event window for ' + EVENT_ID);
  print('This event cannot be validated with optical satellite reference.');
  print('OPTIONS:');
  print(' 1. Widen the event window in EVENTS above.');
  print(' 2. Increase CLOUD_MAX_SCENE to 100 (accept all scenes, rely on');
  print('    pixel-level QA_PIXEL / SCL masking).');
  print(' 3. Report this event as "no optical validation available" in');
  print('    the paper Table 2 (S1 flood map is still valid, just no');
  print('    independent accuracy check for this specific event).');
  print('===============================================================');
  throw new Error('No optical scenes available. See console messages.');
}

// ---- Median composite of MNDWI, then threshold at 0.0 for water ----
var mndwiImg = combined.median().clip(REGION);
var waterRef = mndwiImg.gt(0.0);

Map.addLayer(mndwiImg, {min: -0.5, max: 0.5, palette: ['brown', 'white', 'blue']},
             'MNDWI median (' + EVENT_ID + ')');
Map.addLayer(waterRef.selfMask(), {palette: ['cyan']},
             'Reference water (' + EVENT_ID + ')');

// ---- Compute reference water area for the metadata ----
var refArea = waterRef.multiply(ee.Image.pixelArea().divide(1e6)).reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: REGION, scale: 30, maxPixels: 1e10, bestEffort: true
}).get('MNDWI');
print('Reference water area (km2):', refArea);

// ---- Export ----
Export.image.toDrive({
  image: waterRef.uint8(),
  description: EVENT_ID + '_s2l8l9_reference_water',
  fileNamePrefix: EVENT_ID + '_s2l8l9_reference_water',
  folder: DRIVE_FOLDER,
  region: REGION, scale: 30, maxPixels: 1e10
});

Export.table.toDrive({
  collection: ee.FeatureCollection([
    ee.Feature(null, {
      event_id: EVENT_ID,
      evt_start: EV.start, evt_end: EV.end,
      s2_scenes: n_s2, l8_scenes: n_l8, l9_scenes: n_l9, total_scenes: n_total,
      cloud_max_scene_pct: CLOUD_MAX_SCENE,
      reference_water_km2: refArea,
      region_definition: 'FAO GAUL 2015 Level 1 Sylhet Division'
    })
  ]),
  description: EVENT_ID + '_s2l8l9_metadata',
  fileNamePrefix: EVENT_ID + '_s2l8l9_metadata',
  folder: DRIVE_FOLDER, fileFormat: 'CSV'
});

print('Both tasks queued. Change EVENT_ID and re-run for next event.');
print('EVENT_IDs: ev_2017_apr, ev_2019_jul, ev_2020_jul, ev_2022_may,');
print('           ev_2022_jun, ev_2023_may, ev_2024_jul (7 total)');
