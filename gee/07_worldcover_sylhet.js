/**
 * 07_worldcover_sylhet.js
 * ------------------------------------------------------------------
 * Export ESA WorldCover 2021 v200 (10m land cover) for Sylhet Division
 * FAO GAUL polygon. Used for Stage C landcover-flood intersection.
 *
 * Class codes:
 *   10 = Tree cover
 *   20 = Shrubland
 *   30 = Grassland
 *   40 = Cropland
 *   50 = Built-up
 *   60 = Bare / sparse vegetation
 *   70 = Snow and ice
 *   80 = Permanent water bodies
 *   90 = Herbaceous wetland
 *   95 = Mangroves
 *  100 = Moss and lichen
 *
 * Reference: Zanaga et al. (2022). ESA WorldCover 10 m 2021 v200.
 *            doi:10.5281/zenodo.7254221
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

// ESA WorldCover 2021 v200
var wcCollection = ee.ImageCollection('ESA/WorldCover/v200');
var wc = wcCollection.first();  // single global mosaic
var wcClipped = wc.clip(REGION);

print('WorldCover 2021 v200 (single global mosaic)');

var vis = {
  min: 10, max: 100,
  palette: ['006400','ffbb22','ffff4c','f096ff','fa0000',
            'b4b4b4','f0f0f0','0064c8','0096a0','00cf75','fae6a0']
};
Map.addLayer(wcClipped, vis, 'ESA WorldCover 2021');

// Class area summary
var areaImage = ee.Image.pixelArea().addBands(wcClipped);
var areas = areaImage.reduceRegion({
  reducer: ee.Reducer.sum().group({groupField: 1, groupName: 'class'}),
  geometry: REGION,
  scale: 10,
  maxPixels: 1e10,
  bestEffort: true
});
print('Land cover class areas (m2):', areas);

Export.image.toDrive({
  image: wcClipped.uint8(),
  description: 'sylhet_worldcover_2021',
  fileNamePrefix: 'sylhet_worldcover_2021',
  folder: DRIVE_FOLDER,
  region: REGION,
  scale: 10,
  maxPixels: 1e10
});

print('Task queued. Filename: sylhet_worldcover_2021.tif');
print('Expected file size: 100-300 MB (10 m resolution over Sylhet Division).');
