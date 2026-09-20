# 🌾 Kasekor Vision (ទស្សនៈវិស័យកសិករ)

![Kasekor Vision App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Prototype-green?style=for-the-badge)

**Kasekor Vision** is a volunteer startup project designed to assist the agricultural sector in Cambodia. By utilizing an interactive map and analyzing environmental conditions, the application recommends the most suitable crops for a specific geographic location.

This project was built using **Python**, **Streamlit**, and **Folium** to provide a fast, interactive, and user-friendly prototype.

---

## 🎯 Project Objectives

1. **Map Visualization:** Provide an interactive map of Cambodia (181,035 km²) allowing users to click and select any location (village, district, or province) similar to Google Maps.
2. **Crop Recommendation:** Based on the selected location and specified environmental conditions, the system predicts and recommends the optimal crop.

### 📊 Data Analyzed for Recommendation
When predicting a crop, the system outputs detailed agricultural properties:
*   **Species:** The general plant type (e.g., Rice, Cashew).
*   **Variety:** The specific crop variety (e.g., Phka Rumduol).
*   **Population:** Planting density per hectare.
*   **Architecture:** The physical structure/height of the crop.
*   **Duration:** Time required from planting to harvest.

The recommendation is based on the following **Environmental Factors**:
*   **Soil:** Soil type (e.g., Sandy, Clay).
*   **Climate:** General weather conditions (e.g., Hot & Humid).
*   **Water:** Water source availability (e.g., Rain-fed, Irrigation).
*   **Pests & Diseases:** Potential agricultural threats.
*   **Landscape:** Topography (e.g., Flatland, Sloping).

---

## 🛠️ Tech Stack

*   **Frontend & Web Framework:** [Streamlit](https://streamlit.io/)
*   **Map Visualization:** [Folium](https://python-visualization.github.io/folium/) & `streamlit-folium`
*   **Data Handling:** Pandas, NumPy
*   **Machine Learning (Future Scope):** Scikit-learn (RandomForest) for building the predictive model.

---

## 🚀 How to Run the Application (Local Setup)

Follow these steps to run the Kasekor Vision app on your local machine.

### 1. Prerequisites
Make sure you have **Python 3.8 or higher** installed.

### 2. Install Required Libraries
Open your terminal (or Git Bash / WSL) and install the dependencies:
```bash
pip install streamlit folium streamlit-folium pandas

# Developer
Name: Heng Sengthay
Major: Data Science and Engineering