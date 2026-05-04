import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from model import train_model, predict_congestion

# ================= CONFIG =================
st.set_page_config(page_title="Smart Traffic", layout="wide")

# ================= MODEL =================
@st.cache_resource
def load_model():
    model, _ = train_model()
    return model

model = load_model()

# ================= SESSION STATE =================
if "start_coords" not in st.session_state:
    st.session_state.start_coords = None

if "end_coords" not in st.session_state:
    st.session_state.end_coords = None

# ================= SEARCH FUNCTION =================
def search_location(query):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}, India&limit=5"
    headers = {"User-Agent": "traffic-app"}

    try:
        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code != 200:
            return []

        data = res.json()

        results = []
        for place in data:
            name = place["display_name"]
            lat = float(place["lat"])
            lon = float(place["lon"])
            results.append((name, lat, lon))

        return results

    except:
        return []

# ================= ROUTE FUNCTION =================
def get_route(start, end):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
        data = requests.get(url, timeout=5).json()

        coords = data["routes"][0]["geometry"]["coordinates"]
        distance = data["routes"][0]["distance"] / 1000
        return coords, distance

    except:
        return [], 0

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Controls")
hour = st.sidebar.slider("Hour", 0, 23, 9)
day = st.sidebar.slider("Day (1=Mon,7=Sun)", 1, 7, 1)

# ================= HEADER =================
st.title("🚦 Smart Traffic Prediction")
st.markdown("### Plan smarter routes with AI 🚀")
st.divider()

# ================= INPUT =================
st.markdown("## 📍 Enter Route")

col1, col2 = st.columns(2)

with col1:
    start_q = st.text_input("From", key="start_input")

with col2:
    end_q = st.text_input("To", key="end_input")

# ================= START SEARCH =================
if start_q:
    start_results = search_location(start_q)

    if start_results:
        start_choice = st.selectbox(
            "Select Start Location",
            start_results,
            key="start_select"
        )
        st.session_state.start_coords = [start_choice[1], start_choice[2]]

# ================= END SEARCH =================
if end_q:
    end_results = search_location(end_q)

    if end_results:
        end_choice = st.selectbox(
            "Select Destination",
            end_results,
            key="end_select"
        )
        st.session_state.end_coords = [end_choice[1], end_choice[2]]

# ================= USE STORED VALUES =================
start_coords = st.session_state.start_coords
end_coords = st.session_state.end_coords

# ================= BUTTON =================
predict_btn = st.button("🚀 Predict Traffic")

st.divider()

# ================= MAP =================
st.markdown("## 🗺 Route Map")

if not (start_coords and end_coords):
    st.info("👆 Enter and select locations to see route")

if start_coords and end_coords:
    coords, distance = get_route(start_coords, end_coords)
else:
    coords, distance = [], 0
    start_coords = [26.4499, 80.3319]  # Default Kanpur

m = folium.Map(location=start_coords, zoom_start=13)

if coords:
    folium.PolyLine(
        [(c[1], c[0]) for c in coords],
        color="blue",
        weight=6
    ).add_to(m)

folium.Marker(start_coords, icon=folium.Icon(color="green")).add_to(m)

if end_coords:
    folium.Marker(end_coords, icon=folium.Icon(color="red")).add_to(m)

st_folium(m, width=1200, height=600)

if distance > 0:
    st.success(f"📏 Distance: {distance:.2f} km")

# ================= RESULT =================
if predict_btn:
    st.divider()
    st.markdown("## 🔮 Traffic Result")

    result = predict_congestion(model, hour, day)

    if result == 0:
        factor = 1
        st.success("🟢 Low Traffic")
    elif result == 1:
        factor = 1.5
        st.warning("🟡 Moderate Traffic")
    else:
        factor = 2
        st.error("🔴 Heavy Traffic")

    st.markdown("### 🚗 Estimated Travel Time")

    col1, col2, col3 = st.columns(3)

    car_time = (distance / 40) * 60 * factor if distance else 0
    bike_time = (distance / 50) * 60 * factor if distance else 0
    cycle_time = (distance / 15) * 60 * factor if distance else 0

    col1.metric("🚗 Car", f"{car_time:.1f} min")
    col2.metric("🏍 Bike", f"{bike_time:.1f} min")
    col3.metric("🚴 Cycle", f"{cycle_time:.1f} min")

# ================= FOOTER =================
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>Made with ❤️ | Smart Traffic System</p>",
    unsafe_allow_html=True
)