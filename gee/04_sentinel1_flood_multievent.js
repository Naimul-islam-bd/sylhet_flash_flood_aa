/**
 * 04_sentinel1_flood_multievent.js  (CORRECTED v2)
 * ------------------------------------------------------------------
 * Multi-event flash flood inundation mapping for Sylhet Division
 * using Sentinel-1 GRD IW (VV), Otsu thresholding, permanent-water
 * masking. Study region: FAO GAUL 2015 Level 1 polygon for Sylhet
 * Division (consistent with Stage A analysis).
 *
 * Set EVENT_ID at the top, Save, Run, then click Run in Tasks tab.
 * Repeat for each event.
 *
 * References:
 *   Otsu (1979) IEEE Trans SMC 9(1).
 *   Tiwari et al. (2020) PLOS ONE 15(8).
 *   Twele et al. (2016) Int J Remote Sensing 37.
 * ------------------------------------------------------------------
 */

var EVENT_ID = 'ev_2017_apr';

// ---- Event catalogue: 7 documented flash flood events ------------
// Sentinel-1 launched April 2014; only post-2015 events mappable.
// Each event: pre-event window (baseline) + event window (flood).
// Dates sourced from OCHA/ReliefWeb/DDM primary reports.
var EVENTS = {
  'ev_2017_apr': {pre_start: '2017-02-01', pre_end: '2017-03-15',
                  evt_start: '2017-03-28', evt_end: '2017-05-15'},
  'ev_2019_jul': {pre_start: '2019-06-01', pre_end: '2019-06-25',
                  evt_start: '2019-07-05', evt_end: '2019-07-25'},
  'ev_2020_jul': {pre_start: '2020-06-01', pre_end: '2020-06-20',
                  evt_start: '2020-06-25', evt_end: '2020-07-31'},
  'ev_2022_may': {pre_start: '2022-03-15', pre_end: '2022-05-05',
                  evt_start: '2022-05-11', evt_end: '2022-05-25'},
  'ev_2022_jun': {pre_start: '2022-04-01', pre_end: '2022-05-05',
                  evt_start: '2022-06-15', evt_end: '2022-06-30'},
  'ev_2023_may': {pre_start: '2023-03-15', pre_end: '2023-04-30',
                  evt_start: '2023-05-10', evt_end: '2023-05-30'},
  'ev_2024_jul': {pre_start: '2024-04-01', pre_end: '2024-05-15',
                  evt_start: '2024-05-27', evt_end: '2024-07-31'}
};

var EVENT = EVENTS[EVENT_ID];
if (EVENT === undefined) throw new Error('EVENT_ID not in catalogue.');
print('Processing event:', EVENT_ID, EVENT);

// ---- OFFICIAL Sylhet Division polygon (FAO GAUL 2015 Level 1) ----
var gaul1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var SYLHET_FC = gaul1
    .filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh'))
    .filter(ee.Filter.eq('ADM1_NAME', 'Sylhet'));
var REGION = SYLHET_FC.geometry();

print('Sylhet Division feature count (should be 1):', SYLHET_FC.size());
print('Sylhet Division area (km2):', REGION.area().divide(1e6));

var DRIVE_FOLDER = 'gee_exports_sylhet';
Map.centerObject(REGION, 8);
Map.addLayer(SYLHET_FC, {color: 'red'}, 'Sylhet Division (FAO GAUL 2015)');

// ---- Sentinel-1 loader ----
function loadS1(startDate, endDate) {
  return ee.ImageCollection('COPERNICUS/S1_GRD')
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
    .filter(ee.Filter.eq('resolution_meters', 10))
    .filterBounds(REGION)
    .filterDate(startDate, endDate)
    .select('VV');
}

var preCol = loadS1(EVENT.pre_start, EVENT.pre_end);
var evtCol = loadS1(EVENT.evt_start, EVENT.evt_end);

print('Pre-event S1 scenes:', preCol.size());
print('Event S1 scenes:',     evtCol.size());

if (evtCol.size().getInfo() === 0) {
  throw new Error('No Sentinel-1 scenes in event window. Widen the window.');
}

// ---- Speckle filtering (focal mean, 50 m window ~ 5 pixels) ----
function speckleFilter(img) {
  return img.focal_mean(50, 'square', 'meters')
            .copyProperties(img, ['system:time_start']);
}

var preFilt = preCol.map(speckleFilter);
var evtFilt = evtCol.map(speckleFilter);
var preImg = preFilt.median().clip(REGION);
var evtImg = evtFilt.median().clip(REGION);

// ---- Otsu automatic threshold ----
function otsu(histogram) {
  var counts = ee.Array(ee.Dictionary(histogram).get('histogram'));
  var means  = ee.Array(ee.Dictionary(histogram).get('bucketMeans'));
  var size = means.length().get([0]);
  var total = counts.reduce(ee.Reducer.sum(), [0]).get([0]);
  var sum = means.multiply(counts).reduce(ee.Reducer.sum(), [0]).get([0]);
  var mean = sum.divide(total);
  var indices = ee.List.sequence(1, size);
  var bss = indices.map(function (i) {
    i = ee.Number(i);
    var aCounts = counts.slice(0, 0, i);
    var aCount  = aCounts.reduce(ee.Reducer.sum(), [0]).get([0]);
    var aMeans  = means.slice(0, 0, i);
    var aMean   = aMeans.multiply(aCounts).reduce(ee.Reducer.sum(), [0]).get([0])
                        .divide(aCount);
    var bCount  = total.subtract(aCount);
    var bMean   = sum.subtract(aCount.multiply(aMean)).divide(bCount);
    return aCount.multiply(aMean.subtract(mean).pow(2))
       .add(bCount.multiply(bMean.subtract(mean).pow(2)));
  });
  return means.sort(bss).get([-1]);
}

var histogram = evtImg.reduceRegion({
  reducer: ee.Reducer.histogram(255, 0.5),
  geometry: REGION, scale: 30, maxPixels: 1e10, bestEffort: true
}).get('VV');

var threshold = ee.Number(otsu(histogram));
print('Otsu threshold (dB) for event image:', threshold);

// ---- Flood detection ----
var eventWater = evtImg.lt(threshold);
var preWater   = preImg.lt(threshold);
var floodOnly  = eventWater.and(preWater.not());

// ---- Mask permanent water using JRC GSW (occurrence > 80%) ----
var gsw = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence');
var permWaterMask = gsw.gt(80).unmask(0);
var floodClean = floodOnly.updateMask(permWaterMask.not()).selfMask();

// ---- Remove small objects (< 50 pixels ~ 0.5 ha at 10 m) ----
var connections = floodClean.connectedPixelCount(50, true);
var floodFinal  = floodClean.updateMask(connections.gte(50)).clip(REGION);

// ---- Visualisation ----
Map.addLayer(evtImg, {min: -25, max: 0}, 'S1 VV event median', false);
Map.addLayer(gsw.updateMask(gsw.gt(50)),
             {min: 50, max: 100, palette: ['blue', 'darkblue']},
             'JRC permanent water', false);
Map.addLayer(floodFinal, {palette: ['red']}, 'Flood extent (' + EVENT_ID + ')');

// ---- Area calculation ----
var pixelArea = ee.Image.pixelArea().divide(1e6);
var totalArea = floodFinal.multiply(pixelArea).reduceRegion({
  reducer: ee.Reducer.sum(), geometry: REGION, scale: 30, maxPixels: 1e10
}).get('VV');
print('Total flooded area (km2):', totalArea);

// ---- Export flood raster ----
Export.image.toDrive({
  image: floodFinal.uint8(),
  description: EVENT_ID + '_flood_extent',
  fileNamePrefix: EVENT_ID + '_flood_extent',
  folder: DRIVE_FOLDER,
  region: REGION, scale: 30, maxPixels: 1e10
});

// ---- Export metadata CSV ----
Export.table.toDrive({
  collection: ee.FeatureCollection([
    ee.Feature(null, {
      event_id: EVENT_ID,
      pre_start: EVENT.pre_start, pre_end: EVENT.pre_end,
      evt_start: EVENT.evt_start, evt_end: EVENT.evt_end,
      pre_scenes: preCol.size(),
      evt_scenes: evtCol.size(),
      otsu_threshold_dB: threshold,
      flood_area_km2: totalArea,
      region_definition: 'FAO GAUL 2015 Level 1 Sylhet Division'
    })
  ]),
  description: EVENT_ID + '_metadata',
  fileNamePrefix: EVENT_ID + '_metadata',
  folder: DRIVE_FOLDER, fileFormat: 'CSV'
});

print('Both tasks queued. Change EVENT_ID and re-run for the next event.');
print('EVENT_IDs: ev_2017_apr, ev_2019_jul, ev_2020_jul, ev_2022_may,');
print('           ev_2022_jun, ev_2023_may, ev_2024_jul (7 total)');
