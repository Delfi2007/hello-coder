// Burnt Area Detection Example
const area = ee.Geometry.Polygon([
          [
            [
              -122.092,
              37.424
            ],
            [
              -122.086,
              37.418
            ],
            [
              -122.079,
              37.425
            ],
            [
              -122.085,
              37.43
            ]
          ]
        ]);

const pre = ee.ImageCollection("MODIS/006/MOD09GA")
  .filterBounds(area)
  .filterDate("2022-01-01", "2022-01-15")
  .mean();

const post = ee.ImageCollection("MODIS/006/MOD09GA")
  .filterBounds(area)
  .filterDate("2022-02-01", "2022-02-15")
  .mean();

// Burn index (NBR)
const pre_nbr = pre.normalizedDifference(["sur_refl_b02", "sur_refl_b07"]);
const post_nbr = post.normalizedDifference(["sur_refl_b02", "sur_refl_b07"]);

const dNBR = pre_nbr.subtract(post_nbr).gt(0.2);

Map.centerObject(area, 9);
Map.addLayer(dNBR, {palette:['orange']}, "Burnt Area");

Export.table.toDrive({
  collection: dNBR.reduceToVectors({geometry: area}),
  description: "fire_post",
  fileFormat: "GeoJSON"
});
