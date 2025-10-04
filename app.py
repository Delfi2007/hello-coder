import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap


st.set_page_config(page_title="SAR Disaster Lens", layout="wide")

st.title("🌍 SAR-Disaster-Lens")
st.markdown("Compare **pre- and post-disaster** geospatial data exported from Google Earth Engine.")

# Sidebar
hazard = st.sidebar.selectbox("Select Hazard", ["Flood", "Forest Loss", "Fire"])

# File paths
data_map = {
    "Flood": ("data/flood_pre.geojson", "data/flood_post.geojson"),
    "Forest Loss": ("data/forest_pre.geojson", "data/forest_post.geojson"),
    "Fire": ("data/fire_pre.geojson", "data/fire_post.geojson"),
}

pre_file, post_file = data_map[hazard]

# Load GeoJSONs
try:
    gdf_pre = gpd.read_file(pre_file)
    gdf_post = gpd.read_file(post_file)
except Exception:
    st.error(f"⚠️ Missing files for {hazard}. Please export from GEE.")
    st.stop()

# Map
m = leafmap.Map(center=[20, 80], zoom=4)

m.add_gdf(gdf_pre, layer_name=f"{hazard} - Pre", style={"color": "blue"})
m.add_gdf(gdf_post, layer_name=f"{hazard} - Post", style={"color": "red"})

st.write("**Blue = Pre-disaster | Red = Post-disaster**")
m.to_streamlit(height=600)
