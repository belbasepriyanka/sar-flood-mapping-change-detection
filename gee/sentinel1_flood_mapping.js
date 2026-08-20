// Sentinel-1 change-detection template. Replace AOI/dates for an operational event.
var aoi = ee.Geometry.Rectangle([-80.45,25.55,-80.25,25.75]);
function vv(start,end){ return ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(aoi).filterDate(start,end).filter(ee.Filter.eq('instrumentMode','IW')).filter(ee.Filter.listContains('transmitterReceiverPolarisation','VV')).select('VV').median(); }
var pre=vv('2025-05-01','2025-05-31'); var post=vv('2025-06-01','2025-06-30'); var change=post.subtract(pre); var flood=change.lt(-3.5);
Map.centerObject(aoi,10); Map.addLayer(change,{min:-8,max:3},'VV change'); Map.addLayer(flood.selfMask(),{palette:['00FFFF']},'Flood candidate');
