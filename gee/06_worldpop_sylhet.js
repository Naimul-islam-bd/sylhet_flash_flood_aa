/**
 * 06_worldpop_sylhet.js
 * ------------------------------------------------------------------
 * Export WorldPop 2020 population density (100m) for Sylhet Division
 * FAO GAUL polygon. Used for Stage C exposure quantification.
 *
 * Reference: Tatem, A.J. (2017). WorldPop, open data for spatial
 *            demography. Scientific Data 4, 170004.
 * ------------------------------------------------------------------
 */

var gaul1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var SYLHET_FC = gaul1
    .filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh'))
    .filter(ee.Filter.eq('ADM1_NAME', 'Sylhet'));
var REGION = SYLHET_FC.geometry();

var DRIVE_FOLDER = 'gee_exports_sylhet';
Map.centerObject(REGION, 8);
Map.addLayer(SYLHET_FC, {color: 'red'}, 'Sylhet Division');

// WorldPop unconstrained population count for Bangladesh 2020
// asset: WorldPop/GP/100m/pop/BGD_2020
var pop = ee.Image('WorldPop/GP/100m/pop/BGD_2020');
print('WorldPop 2020 Bangladesh info:', pop);

var popClipped = pop.clip(REGION);

// Summary statistic
var totalPop = popClipped.reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: REGION,
  scale: 100,
  maxPixels: 1e10,
  bestEffort: true
});
print('Total population in Sylhet Division (WorldPop 2020):', totalPop);

Map.addLayer(popClipped, {min: 0, max: 100, palette: ['white', 'yellow', 'red']},
             'Population density (people per 100m pixel)');

Export.image.toDrive({
  image: popClipped,
  description: 'sylhet_worldpop_2020',
  fileNamePrefix: 'sylhet_worldpop_2020',
  folder: DRIVE_FOLDER,
  region: REGION,
  scale: 100,
  maxPixels: 1e10
});

print('Task queued. Filename: sylhet_worldpop_2020.tif');
print('Expected total population: about 10-12 million people.');
