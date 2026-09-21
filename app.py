import streamlit as st
import folium
from folium.plugins import MousePosition # <-- NEW IMPORT: For Hover functionality
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Set webpage config
st.set_page_config(page_title="Kasekor Vision", layout="wide")

# Initialize Geocoder
geolocator = Nominatim(user_agent="kasekor_vision_app")

st.title("🌾 Kasekor Vision")
st.markdown("Select a location on the map and define the environmental conditions to receive optimal crop recommendations.")

# Split the screen into two columns
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🗺️ Map of Cambodia")
    
    # --- TASK 1: RESTRICT MAP TO CAMBODIA ONLY ---
    # Cambodia's approximate bounding box: Lat (10.0 to 15.0), Lon (102.0 to 108.0)
    m = folium.Map(
        location=[12.5657, 104.9910], 
        zoom_start=7,
        min_zoom=7,          # Prevent zooming out too far
        max_bounds=True,     # Lock the dragging to the bounds below
        min_lat=10.0,
        max_lat=15.0,
        min_lon=102.0,
        max_lon=108.0
    )
    
    # --- TASK 2: ADD MOUSE HOVER INFORMATION ---
    # This will show coordinates live when the user hovers over the map
    MousePosition(
        position="topright",
        separator=" | ",
        empty_string="Hover over the map to see coordinates",
        lng_first=False,
        prefix="📍 Hover Location:"
    ).add_to(m)
    
    # Render the map and capture click events
    map_data = st_folium(m, height=500, width=700)
    
    clicked_lat = None
    clicked_lon = None
    
    # Check if a location was clicked
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lon = map_data["last_clicked"]["lng"]
        
        # Reverse Geocoding on CLICK
        with st.spinner("Fetching location details..."):
            try:
                location = geolocator.reverse(f"{clicked_lat}, {clicked_lon}", language="en")
                address = location.raw.get("address", {})
                
                province = address.get("state", "Unknown Province")
                district = address.get("county", address.get("city", ""))
                
                if district:
                    location_name = f"{district}, {province}"
                else:
                    location_name = province
                    
                st.success(f"📍 **Clicked Area:** {location_name} (Lat: {clicked_lat:.4f}, Lon: {clicked_lon:.4f})")
            except Exception as e:
                st.success(f"📍 **Clicked Location:** Lat: {clicked_lat:.4f}, Lon: {clicked_lon:.4f}")
    else:
        st.info("👈 Please click on the map to lock in a region for analysis.")

with col2:
    st.subheader("🌍 Environment Conditions")
    
    # Input forms for Environment factors
    soil = st.selectbox("Soil Type", ["Sandy Soil", "Clay Soil", "Red Soil", "Alluvial Soil"])
    climate = st.selectbox("Climate", ["Hot & Humid", "Moderate/Cool", "Hot & Dry"])
    landscape = st.selectbox("Landscape", ["Flatland", "Sloping/Hillside", "Floodplain"])
    water = st.selectbox("Water Source", ["Rain-fed", "Irrigation System", "Near Natural Water Source"])
    
    # Prediction Button
    if st.button("🔍 Analyze & Recommend Crops", type="primary"):
        st.divider()
        st.subheader("🌾 Crop Recommendation")
        
        # Mock Logic for Prototype
        if soil == "Sandy Soil" and landscape == "Sloping/Hillside":
            st.success("This area is highly suitable for **Cassava** or **Cashew Nuts**!")
            
            st.markdown("""
            *   **Species:** Cashew Nut (ស្វាយចន្ទី)
            *   **Variety:** M23 (Large seed, high yield)
            *   **Population:** 204 trees per hectare (7m x 7m spacing)
            *   **Architecture:** Medium height, highly branched canopy
            *   **Duration:** First harvest begins 3 years after planting
            """)
            st.warning("⚠️ **Risk Factor:** Susceptible to root rot (Disease) and fruit-boring insects (Pests) if humidity is too high.")
            
        else:
            st.success("This area is highly suitable for **Rice**!")
            
            st.markdown("""
            *   **Species:** Rice (ស្រូវ)
            *   **Variety:** Phka Rumduol (ផ្ការំដួល)
            *   **Population:** Light broadcast sowing (~100kg/hectare)
            *   **Architecture:** Sturdy stem, resistant to lodging from wind
            *   **Duration:** 6 months maturity (Seasonal Rice)
            """)
            st.warning("⚠️ **Risk Factor:** Stem borers (Pests) and leaf blast (Disease) are common in stagnant water conditions.")