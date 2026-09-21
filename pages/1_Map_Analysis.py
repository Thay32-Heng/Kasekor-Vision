import streamlit as st
import folium
from folium.plugins import MousePosition
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Map Analysis | Kasekor Vision", layout="wide")

geolocator = Nominatim(user_agent="kasekor_vision_app")

st.sidebar.title("🌍 Environment Conditions")

soil = st.sidebar.selectbox("Soil Type", ["Sandy Soil", "Clay Soil", "Red Soil", "Alluvial Soil"])
climate = st.sidebar.selectbox("Climate", ["Hot & Humid", "Moderate/Cool", "Hot & Dry"])
landscape = st.sidebar.selectbox("Landscape", ["Flatland", "Sloping/Hillside", "Floodplain"])
water = st.sidebar.selectbox("Water Source", ["Rain-fed", "Irrigation System", "Near Natural Water Source"])

st.sidebar.info("👆 Select conditions, then click on the map.")

st.title("🗺️ Interactive Map Analysis")
st.markdown("Click on any region in Cambodia to discover the best crops to grow.")

if "clicked_lat" not in st.session_state:
    st.session_state.clicked_lat = None
if "clicked_lon" not in st.session_state:
    st.session_state.clicked_lon = None

# បង្កើតផែនទី
m = folium.Map(
    location=[12.5657, 104.9910], 
    zoom_start=7,
    min_zoom=7,
    max_bounds=True,
    min_lat=10.0,
    max_lat=15.0,
    min_lon=102.0,
    max_lon=108.0
)

MousePosition(
    position="topright",
    separator=" | ",
    empty_string="Hover over the map to see coordinates",
    lng_first=False,
    prefix="📍 Hover:"
).add_to(m)

# ---------------------------------------------------------
# 🌟 THE GUARANTEED FIX 🌟
# ប្រើ ClickForMarker() ដែលមានស្រាប់ក្នុង Folium
# វាអនុញ្ញាតឱ្យអ្នកចុចលើផែនទី វានឹងលោត Marker ភ្លាមៗដោយស្វ័យប្រវត្តិ
# ---------------------------------------------------------
m.add_child(folium.ClickForMarker(popup="Selected Location"))
# ---------------------------------------------------------

# បង្ហាញផែនទី និងចាប់យក last_clicked ប៉ុណ្ណោះ
map_data = st_folium(m, height=550, use_container_width=True, returned_objects=["last_clicked"])

# ចាប់យកទិន្នន័យ (គ្មាន st.rerun ទេ ដូច្នេះមិនបាត់ Zoom ទេ)
if map_data and map_data.get("last_clicked"):
    new_lat = map_data["last_clicked"]["lat"]
    new_lon = map_data["last_clicked"]["lng"]
    
    st.session_state.clicked_lat = new_lat
    st.session_state.clicked_lon = new_lon

# បង្ហាញលទ្ធផលនៅខាងក្រោម
if st.session_state.clicked_lat and st.session_state.clicked_lon:
    clicked_lat = st.session_state.clicked_lat
    clicked_lon = st.session_state.clicked_lon
    
    with st.spinner("Analyzing location..."):
        # 1. កំណត់តម្លៃដើម (Default) ដើម្បីការពារ Error ពេលរកទីតាំងមិនឃើញ
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
            # បើមានបញ្ហាអ៊ីនធឺណិត វានឹងប្រើតម្លៃ Default ខាងលើ
            pass
        
        # Mock Logic (រក្សាទុកនៅដដែល)
        if soil == "Sandy Soil" and landscape == "Sloping/Hillside":
# ... (កូដផ្សេងៗនៅរក្សាដដែល) ...
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
        
        with st.expander("🔍 Click to show detail (Environment & Crop Info)", expanded=True):
            st.markdown(f"**Coordinates:** Lat {clicked_lat:.4f}, Lon {clicked_lon:.4f}")
            st.markdown(f"- **Soil:** {soil} | **Climate:** {climate} | **Landscape:** {landscape} | **Water:** {water}")
            st.divider()
            st.markdown("### 🌾 Crop Recommendation Details")
            st.markdown(crop_details_md) 
            
            st.divider()
            st.markdown("### 📥 Export Result")
            
            report_content = f"""=====================================
KASEKOR VISION - CROP RECOMMENDATION REPORT
=====================================

[ 1. LOCATION DETAILS ]
- Area Name: {location_name}
- Coordinates: Latitude {clicked_lat:.4f}, Longitude {clicked_lon:.4f}

[ 2. ENVIRONMENT CONDITIONS ]
- Soil Type: {soil}
- Climate: {climate}
- Landscape: {landscape}
- Water Source: {water}

[ 3. RECOMMENDED CROP ]
- Best Option: {best_crop}
{crop_details}

=====================================
Powered by Kasekor Vision (Project Year)
====================================="""

            st.download_button(
                label="📥 Download Report (TXT)",
                data=report_content,
                file_name=f"Kasekor_Report_{province.replace(' ', '')}.txt",
                mime="text/plain",
                type="primary"
            )
else:
    st.info("👈 Please click on the map to begin analysis.")