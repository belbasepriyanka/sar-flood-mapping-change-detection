// Sentinel-1 flood event mapping template for Google Earth Engine.
// Replace AOI and dates with the target event. Validate outputs before operational use.
var aoi = ee.Geometry.Rectangle([90.30, 23.65, 90.55, 23.90]);
var preStart = '2024-07-01';
var preEnd = '2024-07-20';
var postStart = '2024-07-21';
var postEnd = '2024-08-10';
function s1Collection(start, end) {
  return ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(aoi).filterDate(start, end)
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .select('VV');
}
var pre = s1Collection(preStart, preEnd).median();
var post = s1Collection(postStart, postEnd).median();
var change = post.subtract(pre).rename('change_db');
var rawFlood = change.lt(-3.0); // demonstration threshold — calibrate locally
var permanentWater = ee.Image('JRC/GSW1_4/GlobalSurfaceWater').select('occurrence').gt(80);
var slope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'));
var flood = rawFlood.updateMask(permanentWater.not()).updateMask(slope.lt(5)).selfMask();
Map.centerObject(aoi, 10);
Map.addLayer(pre, {min:-20,max:0}, 'Pre-event VV');
Map.addLayer(post, {min:-20,max:0}, 'Post-event VV');
Map.addLayer(change, {min:-8,max:3,palette:['08306b','f7fbff','cb181d']}, 'VV change');
Map.addLayer(flood, {palette:['00bfff']}, 'New flood candidate');
var floodArea = flood.multiply(ee.Image.pixelArea()).reduceRegion({reducer: ee.Reducer.sum(), geometry: aoi, scale: 10, maxPixels: 1e10});
print('Flooded area m² (candidate)', floodArea);
