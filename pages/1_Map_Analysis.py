import streamlit as st
import folium
from folium.plugins import MousePosition
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from streamlit_geolocation import streamlit_geolocation
import requests

def get_geolocation():
    """Request the browser's current location and return its coordinates."""
    location = streamlit_geolocation()
    if location and location.get("latitude") is not None and location.get("longitude") is not None:
        return {
            "coords": {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
            }
        }
    return None

st.set_page_config(page_title="Map Analysis | Kasekor Vision", layout="wide")

geolocator = Nominatim(user_agent="kasekor_vision_app")

st.sidebar.title("🌍 Environment Conditions")

# Map Dark Mode Toggle
dark_mode = st.sidebar.toggle("🌙 Enable Dark Map Mode", value=False)
st.sidebar.divider()

soil = st.sidebar.selectbox("Soil Type", ["Sandy Soil", "Clay Soil", "Red Soil", "Alluvial Soil"])
climate = st.sidebar.selectbox("Climate", ["Hot & Humid", "Moderate/Cool", "Hot & Dry"])
landscape = st.sidebar.selectbox("Landscape", ["Flatland", "Sloping/Hillside", "Floodplain"])
water = st.sidebar.selectbox("Water Source", ["Rain-fed", "Irrigation System", "Near Natural Water Source"])

st.sidebar.info("👆 Select conditions, then click on the map.")

st.title("🗺️ Interactive Map Analysis")
st.markdown("Click on any region in Cambodia to discover the best crops to grow.")

# Use my Location 
col_map, col_btn = st.columns([4,1])

with col_btn:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("📍 Use My Location"):
        # get a data from browser (allow by user)
        loc = get_geolocation()
        if loc:
            st.session_state.clicked_lat = loc['coords']['latitude']
            st.session_state.clicked_lon = loc['coords']['longitude']
            st.rerun()
        else:
            st.warning("Please allow location access in your browser.")

if "clicked_lat" not in st.session_state:
    st.session_state.clicked_lat = None
if "clicked_lon" not in st.session_state:
    st.session_state.clicked_lon = None

map_center = [12.5657, 104.9910]
zoom_lvl = 7

if st.session_state.clicked_lat and st.session_state.clicked_lon:
    map_center = [st.session_state.clicked_lat, st.session_state.clicked_lon]
    zoom_lvl = 12

# tiles
map_tiles = "cartodbdark_matter" if dark_mode else "OpenStreetMap"

# បង្កើតផែនទី
m = folium.Map(
    location=map_center, 
    zoom_start=zoom_lvl,
    min_zoom=7,
    max_bounds=True,
    min_lat=10.0, max_lat=15.0, min_lon=102.0, max_lon=108.0,
    tiles=map_tiles
)

MousePosition(
    position="topright",
    separator=" | ",
    empty_string="Hover over the map to see coordinates",
    lng_first=False,
    prefix="📍 Hover:"
).add_to(m)

m.add_child(folium.ClickForMarker(popup="Selected Location"))

# បន្ថែម Marker ពណ៌បៃតង ក្នុងករណីប្រើប៊ូតុង "Use My Location" ឬចុច
if st.session_state.clicked_lat and st.session_state.clicked_lon:
    folium.Marker(
        [st.session_state.clicked_lat, st.session_state.clicked_lon], 
        popup="Target Location", 
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(m)

with col_map:
    map_data = st_folium(m, height=550, use_container_width=True, returned_objects=["last_clicked"])

if map_data and map_data.get("last_clicked"):
    new_lat = map_data["last_clicked"]["lat"]
    new_lon = map_data["last_clicked"]["lng"]
    st.session_state.clicked_lat = new_lat
    st.session_state.clicked_lon = new_lon

if st.session_state.clicked_lat and st.session_state.clicked_lon:
    clicked_lat = st.session_state.clicked_lat
    clicked_lon = st.session_state.clicked_lon
    
    with st.spinner("Analyzing location..."):
        province = "Unknown"
        location_name = "Unknown Location"
        
        try:
            location = geolocator.reverse(f"{clicked_lat}, {clicked_lon}", language="en")
            if location and location.raw.get("address"):
                address = location.raw.get("address", {})
                province = address.get("state", "Unknown")
                district = address.get("county", address.get("city", ""))
                location_name = f"{district}, {province}" if district else province
        except Exception:
            pass

        current_temp = None
        current_wind = None
        try:
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={clicked_lat}&longitude={clicked_lon}&current_weather=true"
            weather_response = requests.get(weather_url).json()
            if "current_weather" in weather_response:
                current_temp = weather_response["current_weather"]["temperature"]
                current_wind = weather_response["current_weather"]["windspeed"]
        except Exception:
            pass

        if soil == "Sandy Soil" and landscape == "Sloping/Hillside":
            best_crop = "Cassava or Cashew Nuts"
            crop_details = """
            *   Species: Cashew Nut (ស្វាយចន្ទី)
            *   Variety: M23
            *   Population: 204 trees per hectare
            *   Architecture: Medium height
            *   Duration: First harvest in 3 years
            """
            crop_details_md = """
            *   **Species:** Cashew Nut (ស្វាយចន្ទី)
            *   **Variety:** M23
            *   **Population:** 204 trees per hectare
            *   **Architecture:** Medium height
            *   **Duration:** First harvest in 3 years
            """
        else:
            best_crop = "Rice"
            crop_details = """
            *   Species: Rice (ស្រូវ)
            *   Variety: Phka Rumduol
            *   Population: ~100kg/hectare
            *   Architecture: Sturdy stem
            *   Duration: 6 months maturity
            """
            crop_details_md = """
            *   **Species:** Rice (ស្រូវ)
            *   **Variety:** Phka Rumduol
            *   **Population:** ~100kg/hectare
            *   **Architecture:** Sturdy stem
            *   **Duration:** 6 months maturity
            """
        
        st.success(f"📍 **Location:** {location_name} | 🌱 **Best Crop:** {best_crop}")
        
        # បង្ហាញទិន្នន័យអាកាសធាតុលើផ្ទៃ UI
        if current_temp is not None:
            w1, w2, w3 = st.columns(3)
            w1.metric(label="🌡️ Live Temp", value=f"{current_temp} °C")
            w2.metric(label="💨 Wind Speed", value=f"{current_wind} km/h")
            w3.metric(label="🌤️ Data Source", value="Open-Meteo")
            st.divider()

        with st.expander("🔍 Click to show detail (Environment & Crop Info)", expanded=True):
            st.markdown(f"**Coordinates:** Lat {clicked_lat:.4f}, Lon {clicked_lon:.4f}")
            st.markdown(f"- **Soil:** {soil} | **Climate:** {climate} | **Landscape:** {landscape} | **Water:** {water}")
            st.divider()
            st.markdown("### 🌾 Crop Recommendation Details")
            st.markdown(crop_details_md) 
            
            st.divider()
            st.markdown("### 📥 Export Result")
            
            st.download_button(
                label="📥 Download Report (TXT)",
                data=f"Location: {location_name}\nTemperature: {current_temp}°C\nCrop: {best_crop}\nDetails:\n{crop_details}",
                file_name=f"Kasekor_Report_{province.replace(' ', '')}.txt",
                mime="text/plain",
                type="primary"
            )
else:
    st.info("👈 Please click on the map or use your current location.")