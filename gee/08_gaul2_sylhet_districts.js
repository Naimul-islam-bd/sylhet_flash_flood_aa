/**
 * 08_gaul2_sylhet_districts.js
 * ------------------------------------------------------------------
 * Export FAO GAUL 2015 Level 2 polygons for the four Sylhet Division
 * districts (Sylhet, Sunamganj, Habiganj, Moulvibazar) as a single
 * GeoJSON file for use in Stage C district-level exposure analysis.
 *
 * Small task (~30 sec), tiny file (~50 KB).
 * ------------------------------------------------------------------
 */

var gaul2 = ee.FeatureCollection('FAO/GAUL/2015/level2');
var SYLHET_DISTRICTS = gaul2
    .filter(ee.Filter.eq('ADM0_NAME', 'Bangladesh'))
    .filter(ee.Filter.eq('ADM1_NAME', 'Sylhet'));

print('District feature count (should be 4):', SYLHET_DISTRICTS.size());
print('District names:');
print(SYLHET_DISTRICTS.aggregate_array('ADM2_NAME'));

// Add area for each district
var withArea = SYLHET_DISTRICTS.map(function (f) {
  return f.set('area_km2', f.geometry().area().divide(1e6));
});

print('District areas (km2):');
withArea.aggregate_array('area_km2').evaluate(function(a) { print(a); });

var DRIVE_FOLDER = 'gee_exports_sylhet';

Map.centerObject(SYLHET_DISTRICTS, 8);
var vis = ['blue', 'red', 'green', 'orange'];
SYLHET_DISTRICTS.evaluate(function(fc) {
  if (fc && fc.features) {
    fc.features.forEach(function(f, i) {
      Map.addLayer(ee.Feature(f), {color: vis[i % vis.length]},
                   f.properties.ADM2_NAME);
    });
  }
});

Export.table.toDrive({
  collection: withArea,
  description: 'sylhet_districts_gaul2',
  fileNamePrefix: 'sylhet_districts_gaul2',
  folder: DRIVE_FOLDER,
  fileFormat: 'GeoJSON'
});

print('Task queued. Filename: sylhet_districts_gaul2.geojson (~50 KB)');
