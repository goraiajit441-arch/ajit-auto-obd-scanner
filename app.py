
import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AJIT AUTO | Motorcycle Diagnostics",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "recording" not in st.session_state:
    st.session_state.recording = False

# ---------------- DESIGN ----------------

# ---------------- PROFESSIONAL DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1120, #111827, #172033);
    color: #f8fafc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263449;
}

/* Main headings */
h1, h2, h3 {
    color: #f8fafc !important;
    letter-spacing: 0.3px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1e293b, #26364b);
    border: 1px solid #3b506b;
    border-radius: 14px;
    padding: 18px;
    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #38bdf8;
    box-shadow: 0 8px 25px rgba(56,189,248,0.12);
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    border: 1px solid #3b506b;
    background: linear-gradient(120deg, #1e3a5f, #164e63);
    color: white;
    font-weight: 600;
    transition: all 0.25s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #38bdf8;
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 18px rgba(56,189,248,0.18);
}

/* Inputs */
input, textarea {
    border-radius: 9px !important;
}

/* Data tables */
div[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 12px;
    overflow: hidden;
}

/* Smooth scrolling and transitions */
html {
    scroll-behavior: smooth;
}

.stMarkdown, .stMetric, .stPlotlyChart {
    animation: fadeIn 0.35s ease;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(5px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- DATA GENERATOR ----------------
def generate_data():
    return {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "RPM": random.randint(1300, 3500),
        "Engine Temperature (°C)": round(random.uniform(75, 105), 1),
        "Throttle Position (%)": round(random.uniform(5, 80), 1),
        "Battery Voltage (V)": round(random.uniform(12.2, 14.5), 2),
        "Engine Load (%)": round(random.uniform(15, 85), 1),
        "Vehicle Speed (km/h)": random.randint(0, 80),
        "Intake Air Temperature (°C)": round(random.uniform(20, 45), 1),
        "MAP Pressure (kPa)": round(random.uniform(25, 100), 1),
        "Fuel Level (%)": round(random.uniform(10, 100), 1),
        "Oxygen Sensor (V)": round(random.uniform(0.1, 0.9), 2),
        "Ignition Timing (°)": round(random.uniform(5, 35), 1)
    }

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏍️ AJIT AUTO")
st.sidebar.subheader("VEHICLE SETUP")

brand = st.sidebar.selectbox(
    "Brand",
    ["Hero", "TVS", "Bajaj", "Honda", "Suzuki", "Yamaha", "Royal Enfield"]
)

model = st.sidebar.text_input(
    "Bike Model",
    "Splendor Plus Standard"
)

year = st.sidebar.selectbox(
    "Manufacturing Year",
    list(range(2026, 2015, -1)),
    index=4
)

st.sidebar.divider()
st.sidebar.info("SIMULATION MODE")
st.sidebar.caption("No ECU hardware connected")
st.sidebar.caption("Demo sensor readings only")

# ---------------- HEADER ----------------
st.title("🏍️ MOTORCYCLE OBD SCANNER TOOL")

st.warning(
    "SIMULATION MODE: These are randomly generated demo readings, "
    "not actual readings from your motorcycle."
)

# ---------------- CONTROL BUTTONS ----------------
st.header("Live Monitoring Controls")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ START MONITORING", use_container_width=True):
        st.session_state.recording = True

with col2:
    if st.button("■ STOP MONITORING", use_container_width=True):
        st.session_state.recording = False

with col3:
    if st.button("🗑 CLEAR HISTORY", use_container_width=True):
        st.session_state.history = []

if st.session_state.recording:
    st.success("Recording status: RUNNING")
else:
    st.info("Recording status: STOPPED")

# ---------------- LIVE MONITOR ----------------
@st.fragment(run_every="1s")
def live_monitor():

    if st.session_state.recording:
        new_data = generate_data()
        st.session_state.history.append(new_data)

        # Keep latest 300 readings
        st.session_state.history = st.session_state.history[-300:]

    if not st.session_state.history:
        st.info("Press START MONITORING to generate demo readings.")
        return

    df = pd.DataFrame(st.session_state.history)
    latest = df.iloc[-1]

    # ---------------- LIVE METRICS ----------------
    st.header("⚡ Live Sensor Readings")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Engine RPM", f"{latest['RPM']} rpm")
    c2.metric("Engine Temperature", f"{latest['Engine Temperature (°C)']} °C")
    c3.metric("Throttle Position", f"{latest['Throttle Position (%)']} %")
    c4.metric("Battery Voltage", f"{latest['Battery Voltage (V)']} V")

    c5, c6, c7, c8 = st.columns(4)

    c5.metric("Engine Load", f"{latest['Engine Load (%)']} %")
    c6.metric("Vehicle Speed", f"{latest['Vehicle Speed (km/h)']} km/h")
    c7.metric("Intake Air Temp", f"{latest['Intake Air Temperature (°C)']} °C")
    c8.metric("MAP Pressure", f"{latest['MAP Pressure (kPa)']} kPa")

    # ---------------- DEMO ALERTS ----------------
    st.header("⚠️ Demo Reading Alerts")

    alerts = []

    if latest["Engine Temperature (°C)"] > 100:
        alerts.append("Demo alert: Engine temperature is above 100°C.")

    if latest["Battery Voltage (V)"] < 12:
        alerts.append("Demo alert: Battery voltage is below 12V.")

    if latest["RPM"] > 6000:
        alerts.append("Demo alert: RPM is above 6000.")

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("No demo alert at this moment.")

    st.caption(
        "Demo alert thresholds are illustrative only, not official "
        "manufacturer limits or a real fault diagnosis."
    )

    # ---------------- SEPARATE GRAPHS ----------------
    st.header("📊 Individual Live Sensor Graphs")

    graph_options = [
        "RPM",
        "Engine Temperature (°C)",
        "Throttle Position (%)",
        "Battery Voltage (V)",
        "Engine Load (%)",
        "Vehicle Speed (km/h)",
        "Intake Air Temperature (°C)",
        "MAP Pressure (kPa)",
        "Fuel Level (%)",
        "Oxygen Sensor (V)",
        "Ignition Timing (°)"
    ]

    selected = st.multiselect(
        "Select sensors to display",
        graph_options,
        default=[
            "RPM",
            "Engine Temperature (°C)",
            "Throttle Position (%)",
            "Battery Voltage (V)"
        ]
    )

    for i in range(0, len(selected), 2):
        left, right = st.columns(2)

        with left:
            sensor = selected[i]
            st.subheader(sensor)
            st.line_chart(
                df.set_index("Time")[[sensor]],
                height=240
            )

        if i + 1 < len(selected):
            with right:
                sensor = selected[i + 1]
                st.subheader(sensor)
                st.line_chart(
                    df.set_index("Time")[[sensor]],
                    height=240
                )

    # ---------------- SENSOR TABLE ----------------
    st.header("🔬 Advanced Sensor Table")

    st.dataframe(
        df.tail(20).iloc[::-1],
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Total recorded samples: {len(df)}")

    # ---------------- CSV EXPORT ----------------
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ DOWNLOAD SENSOR DATA (CSV)",
        data=csv_data,
        file_name="AJIT_AUTO_LIVE_DATA.csv",
        mime="text/csv",
        use_container_width=True
    )


live_monitor()

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    
st.divider()

st.caption(
    "Motorcycle OBD Scanner | Professional Diagnostic Tool | "
    "Developed by Ajit Gorai | Jamshedpur, Jharkhand, India"
)


