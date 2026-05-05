import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from difflib import get_close_matches

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

# ================= LOCAL DATA =================
LOCAL_PLACES = [
    ("Barra 1, Kanpur", 26.4175, 80.3080),
    ("Barra 2, Kanpur", 26.4180, 80.3090),
    ("Barra 3, Kanpur", 26.4190, 80.3100),
    ("Barra 4, Kanpur", 26.4200, 80.3110),
    ("Barra 5, Kanpur", 26.4210, 80.3120),
    ("Kidwai Nagar, Kanpur", 26.4330, 80.3340),
    ("Govind Nagar, Kanpur", 26.4490, 80.3030),
    ("Kalyanpur, Kanpur", 26.5120, 80.2350),
    ("Rawatpur, Kanpur", 26.4790, 80.2940),
    ("Kakadeo, Kanpur", 26.4680, 80.2900),
    ("Naubasta, Kanpur", 26.4030, 80.3310),
]

# ================= SEARCH =================
def search_location(query):
    query = query.lower().strip()
    names = [p[0].lower() for p in LOCAL_PLACES]

    # direct match
    local_results = [p for p in LOCAL_PLACES if query in p[0].lower()]

    # fuzzy match
    if not local_results:
        matches = get_close_matches(query, names, n=5, cutoff=0.4)
        local_results = [p for p in LOCAL_PLACES if p[0].lower() in matches]

    if local_results:
        return local_results

    # API fallback
    try:
        enhanced_query = f"{query}, India"
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={enhanced_query}&limit=5"
        headers = {"User-Agent": "traffic-app"}

        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code != 200:
            return []

        data = res.json()

        return [
            (p["display_name"], float(p["lat"]), float(p["lon"]))
            for p in data
        ]
    except:
        return []

# ================= ROUTE =================
def get_route(start, end):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return [], 0

        data = res.json()
        route = data["routes"][0]

        coords = route["geometry"]["coordinates"]
        distance = route["distance"] / 1000

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

        st.session_state.traffic_result = result
        st.session_state.distance = distance
        st.session_state.route_coords = coords

# ================= LAYOUT =================
col1, col2 = st.columns([2, 1])

# ================= MAP =================
with col1:
    st.markdown("## 🗺 Map")

    m = folium.Map(location=[26.4499, 80.3319], zoom_start=12)

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

    if st.session_state.route_coords:
        route_latlon = [[c[1], c[0]] for c in st.session_state.route_coords]
        folium.PolyLine(route_latlon, color="blue", weight=5).add_to(m)

    st_folium(m, height=500)

# ================= RIGHT PANEL =================
with col2:
    if st.session_state.traffic_result is None:
        st.info("👈 Enter locations and click Predict")
    else:
        ui.right_panel(
            st.session_state.traffic_result,
            st.session_state.distance
        )

# ================= RESULT =================
if st.session_state.traffic_result is not None:
    ui.show_result(
        st.session_state.traffic_result,
        st.session_state.distance
    )

# ================= FOOTER =================
ui.footer()