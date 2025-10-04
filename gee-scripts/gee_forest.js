// Forest Loss Detection Example (Sentinel-1 or NDVI)
const area = ee.Geometry.Rectangle([-122.092, 37.42], [-122.08, 37.438]); // Example AOI

// Pre
const pre = ee.ImageCollection("COPERNICUS/S2_SR")
  .filterBounds(area)
  .filterDate("2022-01-01", "2022-01-31")
  .median()
  .normalizedDifference(["B8","B4"]); // NDVI

// Post
const post = ee.ImageCollection("COPERNICUS/S2_SR")
  .filterBounds(area)
  .filterDate("2022-06-01", "2022-06-30")
  .median()
  .normalizedDifference(["B8","B4"]);

const loss = pre.subtract(post).gt(0.3);

Map.centerObject(area, 9);
Map.addLayer(loss, {palette:['red']}, "Forest Loss");

Export.table.toDrive({
  collection: loss.reduceToVectors({geometry: area}),
  description: "forest_post",
  fileFormat: "GeoJSON"
});
