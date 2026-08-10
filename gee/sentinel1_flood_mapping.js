// Sentinel-1 SAR change-detection starter for Google Earth Engine.
// Replace roi and dates for a real flood event.
var roi = ee.Geometry.Rectangle([-81.2, 25.0, -80.0, 26.1]);

function s1(start, end) {
  return ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(roi)
    .filterDate(start, end)
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .select('VV')
    .median()
    .clip(roi);
}

var pre = s1('2025-05-01','2025-05-31');
var post = s1('2025-06-01','2025-06-30');
var change = post.subtract(pre).rename('VV_change_dB');
var flood = change.lt(-3.0).selfMask();
Map.centerObject(roi, 9);
Map.addLayer(change, {min:-8, max:4}, 'VV change');
Map.addLayer(flood, {}, 'Potential flood');
