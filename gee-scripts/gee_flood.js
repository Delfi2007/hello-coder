// Flood Detection Example (Sentinel-1)
const area = ee.Geometry.Rectangle([-122.092, 37.42, -122.08, 37.431]);
let before = ee.ImageCollection("COPERNICUS/S1_GRD")
  .filterBounds(area)
  .filterDate("2022-06-01", "2022-06-15")
  .mean();

let after = ee.ImageCollection("COPERNICUS/S1_GRD")
  .filterBounds(area)
  .filterDate("2022-07-01", "2022-07-15")
  .mean();

// Simple threshold (adjust manually)
let diff = after.subtract(before).gt(1);

Map.centerObject(area, 9);
Map.addLayer(diff, {palette: ['blue']}, "Flooded");

Export.table.toDrive({
  collection: diff.reduceToVectors({geometry: area}),
  description: "flood_post",
  fileFormat: "GeoJSON"
});
