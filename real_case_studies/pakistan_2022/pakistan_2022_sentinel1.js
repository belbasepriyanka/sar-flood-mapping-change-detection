// Real public-data case study: Pakistan floods, August 2022
// Data: COPERNICUS/S1_GRD, JRC Global Surface Water, SRTM, WorldPop
// IMPORTANT: Thresholds are demonstration starting points and require event-specific validation.

var aoi = ee.Geometry.Rectangle([67.8, 27.0, 69.2, 29.5]);
var preStart = '2022-07-01';
var preEnd   = '2022-07-31';
var postStart = '2022-08-20';
var postEnd   = '2022-09-05';

function s1(start, end) {
  return ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(aoi)
    .filterDate(start, end)
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
    .select('VV');
}

var preCol = s1(preStart, preEnd);
var postCol = s1(postStart, postEnd);
print('Pre-event scenes', preCol.size());
print('Post-event scenes', postCol.size());

var pre = preCol.median().clip(aoi);
var post = postCol.median().clip(aoi);
var change = post.subtract(pre).rename('vv_change_db');

// Candidate inundation from strong negative VV change.
var thresholdDb = -3.0;
var candidate = change.lt(thresholdDb);

// Remove persistent water and steep terrain.
var permanentWater = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')
  .select('occurrence').gt(80);
var slope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'));
var flood = candidate
  .updateMask(permanentWater.not())
  .updateMask(slope.lt(5))
  .selfMask()
  .rename('new_flood_candidate');

var floodAreaM2 = flood.multiply(ee.Image.pixelArea()).reduceRegion({
  reducer: ee.Reducer.sum(), geometry: aoi, scale: 10, maxPixels: 1e10
});
print('Candidate flood area (m²)', floodAreaM2);

// Approximate exposure overlay using WorldPop 100 m population counts.
var pop = ee.ImageCollection('WorldPop/GP/100m/pop')
  .filterBounds(aoi)
  .filterDate('2020-01-01', '2021-01-01')
  .mosaic()
  .clip(aoi);
var exposedPop = pop.updateMask(flood).reduceRegion({
  reducer: ee.Reducer.sum(), geometry: aoi, scale: 100, maxPixels: 1e10
});
print('Population within candidate flood mask (approx.)', exposedPop);

Map.centerObject(aoi, 7);
Map.addLayer(pre, {min:-22, max:2}, 'Pre-event VV');
Map.addLayer(post, {min:-22, max:2}, 'Post-event VV');
Map.addLayer(change, {min:-8,max:4,palette:['08306b','f7fbff','cb181d']}, 'Post - pre VV change');
Map.addLayer(flood, {palette:['00bfff']}, 'Candidate new flooding');

Export.image.toDrive({
  image: flood.toByte(),
  description: 'Pakistan_2022_Sentinel1_Flood_Candidate',
  folder: 'GEE_Flood_Portfolio',
  region: aoi,
  scale: 10,
  maxPixels: 1e10
});

Export.image.toDrive({
  image: change,
  description: 'Pakistan_2022_Sentinel1_VV_Change',
  folder: 'GEE_Flood_Portfolio',
  region: aoi,
  scale: 10,
  maxPixels: 1e10
});
