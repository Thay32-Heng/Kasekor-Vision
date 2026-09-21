import streamlit as st 
# We use Library Folium for interactive Map , it can zoom in/out can also click on the maps we want to know, also tell us about latitude/longtitude 
import folium 
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim # library find a place
from folium.plugins import MousePosition # For Hover Functionality

# Set webpage config: Wide Mode
st.set_page_config(
    page_title="Kasekor Vision - កម្មវិធីណែនាំដំណាំកសិកម្ម",
    layout= "wide"
    )

# Initialize Geocoder 
geolocator = Nominatim(user_agent="kasekor_vision_app")

st.title("Kasekor Vision - ទស្សនៈវិស័យកសិករ")
st.markdown("Select a location on the map and define the environmental condittions to receive optimal crop recommendations.")

#Split the screen into two columns (Left for Map, Right for Data input)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Map of Cambodia")
    # Task 1: Restrict Map to Cambodia Only
    # Cambodia's approximate bounding box; lat(10.0 to 15.0), lon (102.0 to 108.0) 
    m = folium.Map(
        location=[12.5657, 104.9910], 
        zoom_start=7,
        min_zoom = 7,
        max_bounds=True,
        min_lat=10.0,
        max_lat=15.0,
        min_lon=102.0,
        max_lon=108.0
        )

    # Task 2: Add Mouse Hover Information
    # This will show coordinate live when the user hovers over the map
    MousePosition(
        position = "topright",
        separator = "|",
        empty_string = "Hover over the map to see coordinates",
        lng_first = False,
        prefix= "Hover Location:"
    ).add_to(m)

    #Render the map and capture click events
    map_data = st_folium(m, height=500, width=700)

    clicked_lat = None
    clicked_lon = None

    #Check if a location was clicked
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        click_lon = map_data["last_clicked"]["lng"]

        # Function Reverse Geocoding 
        with st.spinner("Fetching location details..."):
            try:
                location = geolocator.reverse(f"{clicked_lat}, {clicked_lon}", language = "en")
                address = location.raw.get("address", {})

                # name of provice district or city
                province = address.get("state", "Unknown Provice")
                district = address.get("country", address.get("city",""))

                # show maps
                if district:
                    location_name = f"{district}, {province}"
                else:
                    location_name = province

                st.success(f"Selected Location: Latitude: {clicked_lat:.4f},Lontitude:{clicked_lon:.4f}")
            except Exception as e:
        # if has problem network or unknow
                st.success(f"**Selected Location:** Lat: {clicked_lat:.4f}, Lon: {clicked_lon:.4f}")
    else:
        st.info("Please click on any location on the map to select an area.")
with col2:
    st.subheader("Enviroment Conditions")

    #Input forms for Environment factors
    soil = st.selectbox("Soil Type", ["Sandy Soil", "Clay Soil", "Red Soil", "Alluvial Soil"])
    climate = st.selectbox("Climate", ["Hot & Humid", "Moderate/Cool", "Hot & Dry"])
    landscape = st.selectbox("Landscape", ["Flatland", "Sloping/Hillside", "Floodplain"])
    water = st.selectbox("Water Source", ["Rain-fed", "Irrigation System", "Near Natural Water Source"])

    #Prediction Button
    if st.button("Analyze & Recommend Crops", type="primary"):
        st.divider()
        st.subheader("Crop Recommendation")

        # Mock Logic for Prototype (To be replaced with Scikit-learn model later)
        if soil == "Sandy Soil" and landscape == "Sloping/Hillside":
            st.success("This area is highly suiable for **Cassava** or ** Cashew Nuts**!")

            #Display detailed crop properties as requested in the Project Year
            st.markdown("""
            *   **Species:** Cashew Nut (ស្វាយចន្ទី)
            *   **Variety:** M23 (Large seed, high yield)
            *   **Population (Density):** 204 trees per hectare (7m x 7m spacing)
            *   **Architecture:** Medium height, highly branched canopy
            *   **Duration:** First harvest begins 3 years after planting
            """)

            st.warning(" **Risk Factor:** Susceptible to root rot (Disease) and fruit-boring insect (Pests) if humidity is too hight.")

        else:
            st.success("This area is highly suitable for **Rice**!")
            
            st.markdown("""
            *   **Species:** Rice (ស្រូវ)
            *   **Variety:** Phka Rumduol (ផ្ការំដួល)
            *   **Population (Density):** Light broadcast sowing (~100kg/hectare)
            *   **Architecture:** Sturdy stem, resistant to lodging from wind
            *   **Duration:** 6 months maturity (Seasonal Rice)
            """)
            
            st.warning("⚠️ **Risk Factor:** Stem borers (Pests) and leaf blast (Disease) are common in stagnant water conditions.")