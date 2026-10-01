import streamlit as st
import requests
from datetime import datetime

# Page Setup
st.set_page_config(
    page_title="SkyPulse | Modern Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Custom Glassmorphism CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    
    .weather-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.12);
        text-align: center;
        margin-bottom: 16px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00d2ff;
        margin-top: 6px;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #b0bec5;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# API Key Config
API_KEY = "bfbf122180186df4597152ab41b4549f"

# Time & Icon Helpers
def convert_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%I:%M %p')

def get_weather_icon(icon_code):
    icons = {
        "01d": "☀️", "01n": "🌙",
        "02d": "⛅", "02n": "☁️",
        "03d": "☁️", "03n": "☁️",
        "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌧️",
        "11d": "🌩️", "11n": "🌩️",
        "13d": "❄️", "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️"
    }
    return icons.get(icon_code, "🌤️")

# Sidebar Controls
st.sidebar.title("⚙️ Controls")
unit_option = st.sidebar.radio("Temperature Unit", ["Celsius (°C)", "Fahrenheit (°F)"])
unit_param = "metric" if "Celsius" in unit_option else "imperial"
unit_symbol = "°C" if unit_param == "metric" else "°F"
speed_unit = "m/s" if unit_param == "metric" else "mph"

# Header
st.title("🌤️ SkyPulse Weather Dashboard")
st.caption("Real-time weather metrics powered by Python & Streamlit")

# Search Bar
col_search, col_btn = st.columns([4, 1])
with col_search:
    city = st.text_input("Enter City", value="Mumbai", label_visibility="collapsed", placeholder="Enter city name (e.g., Mumbai, London, Tokyo)...")
with col_btn:
    search_clicked = st.button("🔍 Search", use_container_width=True, type="primary")

# Fetch Data
def fetch_weather(city_name, key, unit):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city_name, 'appid': key, 'units': unit}
    return requests.get(url, params=params)

if search_clicked or city:
    if city.strip():
        with st.spinner("Fetching data..."):
            response = fetch_weather(city, API_KEY, unit_param)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract Values
                city_name = data['name']
                country = data['sys']['country']
                temp = round(data['main']['temp'], 1)
                feels_like = round(data['main']['feels_like'], 1)
                temp_min = round(data['main']['temp_min'], 1)
                temp_max = round(data['main']['temp_max'], 1)
                humidity = data['main']['humidity']
                pressure = data['main']['pressure']
                wind_speed = data['wind']['speed']
                weather_desc = data['weather'][0]['description'].title()
                icon_code = data['weather'][0]['icon']
                weather_emoji = get_weather_icon(icon_code)
                sunrise = convert_time(data['sys']['sunrise'])
                sunset = convert_time(data['sys']['sunset'])

                st.markdown("---")
                
                # Main Hero Card
                st.markdown(f"""
                <div class="weather-card">
                    <h2>📍 {city_name}, {country}</h2>
                    <h1 style="font-size: 4.2rem; margin: 12px 0;">{weather_emoji} {temp} {unit_symbol}</h1>
                    <p style="font-size: 1.25rem; color: #e0e0e0; margin-bottom: 6px;"><b>{weather_desc}</b> &nbsp;|&nbsp; Feels like {feels_like} {unit_symbol}</p>
                    <p style="color: #b0bec5; font-size: 0.95rem;">Min: {temp_min} {unit_symbol} &nbsp;•&nbsp; Max: {temp_max} {unit_symbol}</p>
                </div>
                """, unsafe_allow_html=True)

                st.write("")
                
                # Metrics Grid
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    st.markdown(f"""
                    <div class="weather-card">
                        <div class="metric-label">💧 Humidity</div>
                        <div class="metric-value">{humidity}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                with m2:
                    st.markdown(f"""
                    <div class="weather-card">
                        <div class="metric-label">💨 Wind Speed</div>
                        <div class="metric-value">{wind_speed} {speed_unit}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with m3:
                    st.markdown(f"""
                    <div class="weather-card">
                        <div class="metric-label">⏲️ Pressure</div>
                        <div class="metric-value">{pressure} hPa</div>
                    </div>
                    """, unsafe_allow_html=True)

                with m4:
                    st.markdown(f"""
                    <div class="weather-card">
                        <div class="metric-label">🌅 Sun Cycle</div>
                        <div style="font-size: 1rem; font-weight: 600; margin-top: 8px;">☀️ {sunrise}</div>
                        <div style="font-size: 1rem; font-weight: 600; color: #b0bec5;">🌙 {sunset}</div>
                    </div>
                    """, unsafe_allow_html=True)

            elif response.status_code == 404:
                st.error("❌ City not found! Please check spelling.")
            else:
                st.error(f"⚠️ Unable to fetch data (Code: {response.status_code})")