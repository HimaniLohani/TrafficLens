import streamlit as st

# ================= HEADER =================
def header():
    st.markdown("""
    <div style='background: linear-gradient(135deg,#4facfe,#00f2fe);
    padding:30px;border-radius:15px;color:white;text-align:center;'>
    <h1>🚦 Smart Traffic Predictor</h1>
    <p>Plan your route smartly with AI-based traffic prediction</p>
    </div>
    """, unsafe_allow_html=True)


# ================= ROUTE INPUT =================
def route_input():
    st.markdown("## 📍 Enter Route")

    col1, col2 = st.columns(2)

    with col1:
        start_q = st.text_input("🚩 From", placeholder="e.g. Barra 2")

    with col2:
        end_q = st.text_input("🏁 To", placeholder="e.g. Kidwai Nagar")

    return start_q, end_q


# ================= SIDEBAR =================
def controls():
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg,#43cea2,#185a9d);
    padding:20px;border-radius:12px;color:white;text-align:center;'>
    <h3>⚙️ Traffic Controls</h3>
    <p>Select time & day</p>
    </div>
    """, unsafe_allow_html=True)

    # 📅 Days mapping
    day_map = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7
    }

    selected_day = st.sidebar.selectbox("📅 Select Day", list(day_map.keys()))

    # ⏰ Time picker
    selected_time = st.sidebar.time_input("⏰ Select Time")

    hour = selected_time.hour
    day = day_map[selected_day]

    # 🎯 Selected info box
    st.sidebar.markdown(f"""
    <div style='background:#f0f2f6;padding:12px;border-radius:10px;margin-top:10px;'>
    <b>🗓 Day:</b> {selected_day}<br>
    <b>⏰ Hour:</b> {hour}:00
    </div>
    """, unsafe_allow_html=True)

    # 📊 Progress feel
    st.sidebar.progress(hour / 24)

    return hour, day


# ================= RESULT CARD =================
def show_result(result, distance):
    st.markdown("## 🔮 Traffic Result")

    if result == 0:
        factor = 1
        color = "#4CAF50"
        label = "Low Traffic"
    elif result == 1:
        factor = 1.5
        color = "#FFC107"
        label = "Moderate Traffic"
    else:
        factor = 2
        color = "#F44336"
        label = "Heavy Traffic"

    st.markdown(f"""
    <div style='background:{color};padding:20px;border-radius:12px;color:white;text-align:center;'>
    <h2>{label}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### 📏 Distance: {distance:.2f} km")

    # 🚗 Travel cards
    col1, col2, col3 = st.columns(3)

    car = (distance / 40) * 60 * factor
    bike = (distance / 50) * 60 * factor
    cycle = (distance / 15) * 60 * factor

    col1.metric("🚗 Car", f"{car:.1f} min")
    col2.metric("🏍 Bike", f"{bike:.1f} min")
    col3.metric("🚴 Cycle", f"{cycle:.1f} min")


# ================= RIGHT PANEL =================
def right_panel(result, distance):
    st.markdown("## 📊 Live Info")

    if result is None:
        st.info("👈 Enter route and click Predict")
        return

    if result == 0:
        st.success("🟢 Smooth Traffic")
    elif result == 1:
        st.warning("🟡 Medium Traffic")
    else:
        st.error("🔴 Heavy Traffic")

    st.metric("📏 Distance", f"{distance:.2f} km")

    st.markdown("### ⏱ Travel Time")

    car = (distance / 40) * 60
    bike = (distance / 50) * 60
    cycle = (distance / 15) * 60

    st.write(f"🚗 Car: {car:.1f} min")
    st.write(f"🏍 Bike: {bike:.1f} min")
    st.write(f"🚴 Cycle: {cycle:.1f} min")


# ================= FOOTER =================
def footer():
    st.markdown(
        "<p style='text-align:center; color:gray;'>Made with ❤️ | Smart Traffic System</p>",
        unsafe_allow_html=True
    )