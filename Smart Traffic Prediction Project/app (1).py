import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="Smart Traffic Predictor", page_icon="🚦", layout="centered")

# Custom CSS for black and blue theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000, #000510, #00112a);
        color: white;
    }
    
    .glass-container {
        background: rgba(0, 123, 255, 0.03); /* very slight blue tint */
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 123, 255, 0.2);
        padding: 30px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 30px rgba(0, 123, 255, 0.15);
    }
    
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #007bff, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 30px;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #0044aa, #007bff);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 20px;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.5);
        color: white !important;
    }
    
    label {
        color: #99c2ff !important;
        font-weight: 600 !important;
    }
    
    /* Input fields styling */
    .stTextInput>div>div>input {
        background-color: rgba(0, 10, 30, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(0, 123, 255, 0.3) !important;
        border-radius: 6px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚦 Smart Traffic Predictor")

@st.cache_resource
def load_model():
    with open("Smart_Traffic_Prediction_System.pickle", "rb") as f:
        return pickle.load(f)

try:
    data = load_model()
    model = data['model']
    le_main = data['le_main']
    le_desc = data['le_desc']
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("📊 Weather Conditions")
    col1, col2 = st.columns(2)
    with col1:
        temp_str = st.text_input("Temperature (Kelvin)", value="290.0")
        rain_1h_str = st.text_input("Rain 1H (mm)", value="0.0")
        snow_1h_str = st.text_input("Snow 1H (mm)", value="0.0")
    with col2:
        clouds_all_str = st.text_input("Cloud Cover (%)", value="40")
        weather_main = st.text_input("Main Weather (e.g. Clear, Clouds, Rain)", value="Clear")
        weather_desc = st.text_input("Weather Description (e.g. sky is clear)", value="sky is clear")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader("📅 Date & Time")
    col3, col4 = st.columns(2)
    with col3:
        hour_str = st.text_input("Hour of Day (0-23)", value="12")
        month_str = st.text_input("Month (1-12)", value="6")
    with col4:
        day_of_week = st.text_input("Day of Week (e.g. Monday)", value="Monday")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Predict Traffic Volume"):
        try:
            # Parse inputs
            temp = float(temp_str)
            rain_1h = float(rain_1h_str)
            snow_1h = float(snow_1h_str)
            clouds_all = int(clouds_all_str)
            hour = int(hour_str)
            month = int(month_str)
            
            day_map = {
                "Monday": 0, "Tuesday": 1, "Wednesday": 2, 
                "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
            }
            if day_of_week not in day_map:
                st.error("Invalid Day of Week. Please enter a valid day (e.g. Monday).")
                st.stop()
            day_of_week_encoded = day_map[day_of_week]
            
            # Encode categorical variables with fallback for unseen labels
            try:
                w_main_enc = le_main.transform([weather_main])[0]
            except ValueError:
                st.warning(f"'{weather_main}' not recognized. Using default ({le_main.classes_[0]}).")
                w_main_enc = le_main.transform([le_main.classes_[0]])[0]
                
            try:
                w_desc_enc = le_desc.transform([weather_desc])[0]
            except ValueError:
                st.warning(f"'{weather_desc}' not recognized. Using default ({le_desc.classes_[0]}).")
                w_desc_enc = le_desc.transform([le_desc.classes_[0]])[0]
            
            # Prepare input array
            input_data = pd.DataFrame([
                [temp, rain_1h, snow_1h, clouds_all, w_main_enc, w_desc_enc, hour, day_of_week_encoded, month]
            ], columns=['Temp', 'Rain_1H', 'Snow_1H', 'Clouds_All', 'Weather_Main', 'Weather_Description', 'hour', 'day_of_week', 'month'])
            
            with st.spinner('Calculating prediction...'):
                prediction = model.predict(input_data)[0]
                
            st.markdown(f"""
            <div class="glass-container" style="text-align: center; border-color: #007bff;">
                <h3 style="margin:0; color: #00aaff; font-weight: 600;">Predicted Traffic Volume</h3>
                <h1 style="font-size: 3.5em; margin: 10px 0; background: none; -webkit-text-fill-color: white;">{int(prediction):,}</h1>
                <p style="color: #ccc; font-size: 1.1em;">vehicles per hour</p>
            </div>
            """, unsafe_allow_html=True)
            
        except ValueError as ve:
            st.error("Please enter valid numeric values for Temperature, Rain, Snow, Cloud Cover, Hour, and Month.")

except FileNotFoundError:
    st.error("Model file not found. Please run the training script first.")
except Exception as e:
    st.error(f"An error occurred: {e}")
