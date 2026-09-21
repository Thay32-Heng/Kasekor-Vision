import streamlit as st
import pandas as pd # ថ្មី: សម្រាប់រៀបចំទិន្នន័យគូរក្រាហ្វិក

st.set_page_config(page_title="Crop Dictionary | Kasekor Vision", layout="wide")

st.title("📚 Interactive Crop Dictionary")
st.markdown("Explore detailed information and visualize data about various crops in Cambodia.")
st.divider()

# បន្ថែមទិន្នន័យលេខ (yield_tons_ha និង duration_days) សម្រាប់គូរក្រាហ្វ
crop_data = {
    "Rice (ស្រូវ)": {
        "variety": "Phka Rumduol (ផ្ការំដួល)",
        "population": "100-120 kg per hectare",
        "architecture": "Sturdy stem, medium height",
        "duration": "180 days (Seasonal Rice)",
        "duration_days": 180, # ទិន្នន័យលេខសម្រាប់ Chart
        "yield_tons_ha": 3.5, # ទិន្នន័យលេខសម្រាប់ Chart
        "ideal_soil": "Clay Soil, Alluvial Soil",
        "ideal_climate": "Hot & Humid",
        "risks": "Stem borers, Leaf blast disease",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Rice_field_in_Cambodia.jpg/800px-Rice_field_in_Cambodia.jpg"
    },
    "Cashew Nut (ស្វាយចន្ទី)": {
        "variety": "M23 (Large seed, high yield)",
        "population": "204 trees per hectare",
        "architecture": "Medium height, highly branched",
        "duration": "First harvest in 3 years",
        "duration_days": 1095, # 3 ឆ្នាំ = 1095 ថ្ងៃ
        "yield_tons_ha": 2.0, 
        "ideal_soil": "Sandy Soil, Red Soil",
        "ideal_climate": "Hot & Dry",
        "risks": "Root rot, Fruit-boring insects",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Cashew_fruit_and_nut.jpg/800px-Cashew_fruit_and_nut.jpg"
    },
    "Cassava (ដំឡូងមី)": {
        "variety": "KU50 or Rayong 5",
        "population": "10,000 plants per hectare",
        "architecture": "Tall, upright, minimal branching",
        "duration": "10-12 months",
        "duration_days": 330,
        "yield_tons_ha": 25.0, # ដំឡូងមីមានទម្ងន់ធ្ងន់ ទិន្នផលច្រើនតោន
        "ideal_soil": "Sandy Soil, Sloping Landscape",
        "ideal_climate": "Hot & Humid",
        "risks": "Cassava Mosaic Disease (CMD), Mealybugs",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Cassava_plantation.jpg/800px-Cassava_plantation.jpg"
    }
}

search_query = st.text_input("🔍 Search for a crop (e.g., Rice, Cashew)...")

filtered_crops = {k: v for k, v in crop_data.items() if search_query.lower() in k.lower()}

if not filtered_crops:
    st.warning("No crops found. Please try another keyword.")
else:
    # ---------------------------------------------------------
    # 🌟 មុខងារថ្មីទី១: បង្ហាញក្រាហ្វិកប្រៀបធៀប (Data Visualization)
    # ---------------------------------------------------------
    st.markdown("### 📊 Data Overview")
    
    # រៀបចំទិន្នន័យដាក់ចូលក្នុង Pandas DataFrame ដើម្បីឱ្យ Streamlit ងាយយល់
    chart_data = {
        "Crop": list(filtered_crops.keys()),
        "Harvest Duration (Days)": [v["duration_days"] for v in filtered_crops.values()],
        "Avg Yield (Tons/Hectare)": [v["yield_tons_ha"] for v in filtered_crops.values()]
    }
    df = pd.DataFrame(chart_data).set_index("Crop")
    
    # បែងចែកជា ២ ជួរឈរ សម្រាប់ដាក់ក្រាហ្វិក ២ ផ្សេងគ្នា
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.caption("⏱️ Harvest Duration Comparison (Days)")
        st.bar_chart(df[["Harvest Duration (Days)"]], color="#ffaa00") # ក្រាហ្វពណ៌ទឹកក្រូច
    with chart_col2:
        st.caption("⚖️ Average Yield Comparison (Tons/Hectare)")
        st.bar_chart(df[["Avg Yield (Tons/Hectare)"]], color="#00ff00") # ក្រាហ្វពណ៌បៃតង
        
    st.divider()
    
    # ---------------------------------------------------------
    # 🌟 មុខងារថ្មីទី២: បន្ថែម Metrics ក្នុងបញ្ជីលម្អិត
    # ---------------------------------------------------------
    st.markdown("### 📖 Detailed Information")
    tabs = st.tabs(list(filtered_crops.keys()))
    
    for i, (crop_name, details) in enumerate(filtered_crops.items()):
        with tabs[i]:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                try:
                    st.image(details["image"], use_column_width=True, caption=crop_name)
                except Exception:
                    st.info("Image not available.")
            
            with col2:
                st.subheader(crop_name)
                
                # បង្ហាញតួលេខលេចធ្លោនៅពីលើអត្ថបទ
                m1, m2 = st.columns(2)
                m1.metric(label="Yield Estimate", value=f"{details['yield_tons_ha']} Tons/ha")
                m2.metric(label="Harvest Time", value=f"{details['duration_days']} Days")
                
                # ព័ត៌មានលម្អិត
                st.markdown(f"**🌱 Variety:** {details['variety']}")
                st.markdown(f"**📏 Population:** {details['population']}")
                st.markdown(f"**🌲 Architecture:** {details['architecture']}")
                
                st.markdown("**🌍 Optimal Environment:**")
                st.markdown(f"- **Soil:** {details['ideal_soil']}")
                st.markdown(f"- **Climate:** {details['ideal_climate']}")
                
                st.warning(f"**⚠️ Potential Risks:** {details['risks']}")

st.divider()
st.info("💡 Note: More crops will be added to this dictionary in the future.")