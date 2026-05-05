import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

from model import train_model, predict_congestion
import ui

# ================= CONFIG =================
st.set_page_config(page_title="Smart Traffic", layout="wide")

# ================= MODEL =================
@st.cache_resource
def load_model():
    model, _ = train_model()
    return model

model = load_model()

# ================= SESSION =================
if "start_coords" not in st.session_state:
    st.session_state.start_coords = None

if "end_coords" not in st.session_state:
    st.session_state.end_coords = None

if "traffic_result" not in st.session_state:
    st.session_state.traffic_result = None

if "distance" not in st.session_state:
    st.session_state.distance = None

if "route_coords" not in st.session_state:
    st.session_state.route_coords = []

# ================= SEARCH =================
def search_location(query):
    query = query.lower().strip()

    local_places = [
        ("Barra 2, Kanpur, India", 26.4180, 80.3090),
        ("Kidwai Nagar, Kanpur, India", 26.4330, 80.3340),
        ("Govind Nagar, Kanpur, India", 26.4490, 80.3030),
    ]

    filtered = [p for p in local_places if query in p[0].lower()]
    if filtered:
        return filtered

    url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}&limit=5"
    headers = {"User-Agent": "traffic-app"}

    try:
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()

        return [(p["display_name"], float(p["lat"]), float(p["lon"])) for p in data]

    except:
        return []

# ================= ROUTE =================
def get_route(start, end):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
        data = requests.get(url).json()

        coords = data["routes"][0]["geometry"]["coordinates"]
        distance = data["routes"][0]["distance"] / 1000

        return coords, distance
    except:
        return [], 0

# ================= UI =================
ui.header()

start_q, end_q = ui.route_input()
hour, day = ui.controls()

# ================= LOCATION =================
if start_q:
    results = search_location(start_q)
    if results:
        names = [r[0] for r in results]
        selected = st.selectbox("Start Location", names)
        idx = names.index(selected)
        st.session_state.start_coords = [results[idx][1], results[idx][2]]

if end_q:
    results = search_location(end_q)
    if results:
        names = [r[0] for r in results]
        selected = st.selectbox("Destination", names)
        idx = names.index(selected)
        st.session_state.end_coords = [results[idx][1], results[idx][2]]

# ================= BUTTON =================
if st.button("🚀 Predict Traffic"):
    if st.session_state.start_coords and st.session_state.end_coords:

        coords, distance = get_route(
            st.session_state.start_coords,
            st.session_state.end_coords
        )

        result = predict_congestion(model, hour, day)

        # SAVE STATE
        st.session_state.traffic_result = result
        st.session_state.distance = distance
        st.session_state.route_coords = coords

# ================= MAIN LAYOUT =================
col1, col2 = st.columns([2, 1])   # 👈 FIXED

# ================= MAP =================
with col1:
    st.markdown("## 🗺 Map")

    m = folium.Map(location=[26.4499, 80.3319], zoom_start=12)

    # markers
    if st.session_state.start_coords:
        folium.Marker(
            st.session_state.start_coords,
            tooltip="Start",
            icon=folium.Icon(color="green")
        ).add_to(m)

    if st.session_state.end_coords:
        folium.Marker(
            st.session_state.end_coords,
            tooltip="End",
            icon=folium.Icon(color="red")
        ).add_to(m)

    # route line
    if st.session_state.route_coords:
        route_latlon = [
            [coord[1], coord[0]] for coord in st.session_state.route_coords
        ]

        folium.PolyLine(route_latlon, color="blue", weight=5).add_to(m)

    st_folium(m, height=500, width=900)

# ================= RIGHT PANEL =================
with col2:
    ui.right_panel(
        st.session_state.traffic_result,
        st.session_state.distance
    )

# ================= RESULT BELOW =================
if st.session_state.traffic_result is not None:
    ui.show_result(
        st.session_state.traffic_result,
        st.session_state.distance
    )

# ================= FOOTER =================
ui.footer()