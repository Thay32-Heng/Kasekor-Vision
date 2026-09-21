import streamlit as st

# កំណត់ទំហំ និងឈ្មោះទំព័រ
st.set_page_config(
    page_title="Kasekor Vision",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# រចនា UI ផ្នែកខាងលើ
st.title("🌾 Welcome to Kasekor Vision (ទស្សនៈវិស័យកសិករ)")
st.subheader("Empowering Cambodian Agriculture with Data")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🎯 About This Project
    **Kasekor Vision** is a volunteer startup project developed to assist the agricultural sector in Cambodia. 
    By analyzing geographical locations and environmental conditions, this platform recommends the most suitable crops for farmers.

    ### 🚀 Key Features
    - **Interactive Map Analysis:** Click anywhere on the map of Cambodia to identify the location.
    - **Environmental Matching:** Input soil, climate, landscape, and water conditions to get crop recommendations.
    - **Smart Insights:** Learn about specific crop varieties, planting density, and potential risks (pests/diseases).

    👈 **Please select a page from the sidebar to get started!**
    """)

with col2:
    st.info("📌 **Project Year Status**\n\nPrototype Phase (Volunteer Startup)")
    st.success("👨‍💻 **Developer:** [Heng Sengthay / Data Science and Engineering]")