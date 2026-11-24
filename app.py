import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# ============================================================
# MOTORCYCLE OBD SCANNER — AJIT GORAI
# Premium UI prototype | Simulation only
# ============================================================

st.set_page_config(
    page_title="Motorcycle OBD Scanner | Ajit Gorai",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------- STATE ---------------------------
DEFAULTS = {
    "page": "Welcome",
    "intro_done": False,
    "logged_in": False,
    "username": "",
    "demo_users": {},
    "selected_brand": "Hero",
    "selected_model": "Splendor Plus",
    "selected_year": 2022,
    "selected_variant": "Standard",
    "history": [],
    "recording": False,
    "selected_vehicle_confirmed": False,
    "auth_mode": "Login",
    "connection_check_started": False,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------- CATALOGUE ------------------------
CATALOGUE = {
    "Hero": ["Splendor Plus", "Splendor Plus XTEC", "HF Deluxe", "Passion Plus",
             "Passion Pro", "Glamour", "Glamour XTEC", "Super Splendor",
             "Xtreme 125R", "Xtreme 160R", "Xtreme 200S", "Xpulse 200 4V",
             "Karizma XMR", "Destini 125", "Pleasure Plus", "Maestro Edge 125",
             "Xoom 110", "Xoom 125"],
    "Honda": ["Shine 100", "Shine 125", "SP 125", "Unicorn", "Hornet 2.0",
              "Livo", "SP160", "CB200X", "H'ness CB350", "CB350RS",
              "Activa 6G", "Activa 125", "Dio", "Dio 125", "Grazia 125"],
    "TVS": ["XL100", "Sport", "Star City Plus", "Radeon", "Apache RTR 160",
            "Apache RTR 160 4V", "Apache RTR 180", "Apache RTR 200 4V",
            "Apache RR 310", "Raider 125", "Ronin", "Jupiter", "Jupiter 125",
            "NTORQ 125", "Zest 110", "Scooty Pep Plus", "iQube"],
    "Bajaj": ["Platina 100", "Platina 110", "CT 110", "CT 125X", "Pulsar 125",
              "Pulsar NS125", "Pulsar NS160", "Pulsar NS200", "Pulsar N160",
              "Pulsar N250", "Pulsar 150", "Pulsar 220F", "Dominar 250",
              "Dominar 400", "Avenger 160", "Avenger 220", "Chetak"],
    "Suzuki": ["Access 125", "Burgman Street", "Avenis 125", "Gixxer 150",
               "Gixxer SF 150", "Gixxer 250", "Gixxer SF 250", "V-Strom SX",
               "Hayabusa"],
    "Yamaha": ["FZ-S FI", "FZ-FI", "FZ-X", "MT-15", "R15 V4", "R15S", "R3",
               "MT-03", "Fascino 125", "Ray ZR 125", "Aerox 155"],
    "Royal Enfield": ["Classic 350", "Bullet 350", "Hunter 350", "Meteor 350",
                      "Himalayan 450", "Scram 411", "Guerrilla 450",
                      "Interceptor 650", "Continental GT 650",
                      "Super Meteor 650", "Shotgun 650", "Bear 650"],
    "KTM": ["Duke 125", "Duke 200", "Duke 250", "Duke 390", "RC 200",
            "RC 390", "Adventure 250", "Adventure 390"],
    "Ather": ["450X", "450S", "Rizta"],
    "Ola Electric": ["S1 X", "S1 Air", "S1 Pro", "S1 Pro Plus"],
    "Other": ["Other Motorcycle", "Other Scooter"],
}
BRAND_MARKS = {
    "Hero": "H", "Honda": "翼", "TVS": "TVS", "Bajaj": "B",
    "Suzuki": "S", "Yamaha": "Y", "Royal Enfield": "RE",
    "KTM": "KTM", "Ather": "A", "Ola Electric": "O", "Other": "＋"
}
BRAND_COLORS = {
    "Hero": "#e34a4a", "Honda": "#e43d4d", "TVS": "#3d8bff",
    "Bajaj": "#5b7cff", "Suzuki": "#3987db", "Yamaha": "#e8edf7",
    "Royal Enfield": "#d5a44c", "KTM": "#f18b32", "Ather": "#6ed6c4",
    "Ola Electric": "#d6e5f3", "Other": "#a6b4c8"
}

# --------------------------- STYLES ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --bg:#10151b; --panel:#171f28; --panel2:#202b35; --line:#34424d;
        --blue:#25b7ad; --cyan:#72e0d5; --muted:#a2b0ba; --white:#f1f5f7; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:
 radial-gradient(ellipse at 12% 0%, rgba(37,183,173,.12), transparent 35%),
 radial-gradient(ellipse at 92% 15%, rgba(193,126,76,.08), transparent 30%),
 linear-gradient(135deg,#10151b 0%,#151e26 55%,#10171e 100%); color:var(--white); }
[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:1500px; padding-top:1.7rem; padding-bottom:3rem; }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; color:#f2f7ff !important; letter-spacing:-.5px; }
p, label, .stMarkdown { color:#d7e3f1; }
small, .muted { color:var(--muted); }
section[data-testid="stSidebar"] { background:#111920; border-right:1px solid #34424d; }
.stButton > button, .stDownloadButton > button {
  border:1px solid #287f79; border-radius:12px; min-height:44px;
  color:#f4fffe; font-weight:700; background:linear-gradient(115deg,#176e69,#219b91);
  transition:all .2s ease; box-shadow:0 5px 18px rgba(20,150,140,.10);
}
.stButton > button:hover, .stDownloadButton > button:hover {
  border-color:#79e3d8; transform:translateY(-2px); box-shadow:0 8px 25px rgba(37,183,173,.20); color:white;
}
div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] input { background:#1b252e; color:#f1f5f7; border-color:#465762; border-radius:10px; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,#202d37,#18232c); border:1px solid #3b4c57; padding:16px; border-radius:16px; }
div[data-testid="stMetricLabel"] { color:#9fb5cc; }
div[data-testid="stMetricValue"] { color:#f2f8ff; }
div[data-testid="stDataFrame"] { border:1px solid #203b56; border-radius:14px; overflow:hidden; }
hr { border-color:#203750; }
div[data-testid="stAlert"] { border-radius:12px; }
div[data-testid="stTabs"] button { color:#b9cce0; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#55c7ff; }
div[data-testid="stRadio"] label { color:#dce9f7; }
.brand-card { background:linear-gradient(145deg,#11253b,#0c1a2a); border:1px solid #25425e;
  border-radius:15px; padding:13px 8px; text-align:center; min-height:90px; }
.brand-mark { width:43px;height:43px;border-radius:13px;display:flex;align-items:center;justify-content:center;
  margin:0 auto 7px auto;font-weight:800;font-size:17px;background:#1c3855;color:#eaf6ff;border:1px solid #3c668d; }
.model-visual { height:90px; border-radius:12px; display:flex; align-items:center; justify-content:center;
  background:radial-gradient(ellipse at center,#1b4263 0%,#10253a 55%,#0b1928 100%);
  border:1px solid #25445f; font-size:42px; }
.model-card { background:linear-gradient(145deg,#11243a,#0b1929);border:1px solid #24415d;border-radius:15px;padding:10px; }
.eyebrow { color:#58c8ff; text-transform:uppercase; letter-spacing:2px; font-size:11px; font-weight:700; }
.hero-panel { border:1px solid #244b6c; border-radius:22px; padding:30px;
 background:radial-gradient(ellipse at 80% 15%,rgba(37,153,220,.25),transparent 35%),linear-gradient(135deg,#10243a,#091727); }
.glow { text-shadow:0 0 24px rgba(59,174,255,.55); }
.pill { display:inline-block;padding:5px 10px;border:1px solid #2d638b;border-radius:30px;color:#83d7ff;font-size:11px;letter-spacing:1px; }
.footer { text-align:center;color:#738ba5;font-size:12px;padding:22px 0 5px; }
@keyframes rise { from {opacity:0;transform:translateY(18px)} to {opacity:1;transform:translateY(0)} }
@keyframes pulse { 0%,100% {box-shadow:0 0 0 0 rgba(57,174,255,.15)} 50% {box-shadow:0 0 25px 3px rgba(57,174,255,.22)} }
.animate { animation:rise .65s ease both; }
.pulse { animation:pulse 3s infinite; }
</style>
""", unsafe_allow_html=True)

# --------------------------- HELPERS --------------------------
def navigate(page):
    st.session_state.page = page

def sample_reading():
    return {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
        "Ignition Timing (°)": round(random.uniform(5, 35), 1),
    }

def footer():
    st.markdown("""
    <div class="footer">MOTORCYCLE OBD SCANNER TOOL &nbsp;·&nbsp; MADE BY <b>AJIT GORAI</b><br>
    JHARKHAND, INDIA 🇮🇳 &nbsp;·&nbsp; SOFTWARE PROTOTYPE</div>
    """, unsafe_allow_html=True)

def vehicle_name():
    return f"{st.session_state.selected_brand} {st.session_state.selected_model}"

def login_user(email, password):
    users = st.session_state.demo_users
    if email in users and users[email] == password:
        st.session_state.logged_in = True
        st.session_state.username = email.split("@")[0]
        st.session_state.page = "Dashboard"
        return True
    return False

# --------------------------- WELCOME / AUTH -------------------
if not st.session_state.logged_in:
    st.markdown('<div class="hero-panel animate">', unsafe_allow_html=True)
    left, right = st.columns([1.15, 0.85], vertical_alignment="center")
    with left:
        st.markdown('<div class="eyebrow">NEXT GENERATION TWO-WHEELER DIAGNOSTICS</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="glow" style="font-size:54px;line-height:1.05;margin:14px 0 8px">Hii! 👋<br>WELCOME TO<br><span style="color:#54c8ff">MOTORCYCLE<br>OBD SCANNER</span></h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:16px;color:#a9bfd5;max-width:560px">A smarter workspace for motorcycle diagnostics, live data and vehicle health insights.</p>', unsafe_allow_html=True)
        st.markdown('<div style="margin:22px 0"><span class="pill">BUILT FOR TWO-WHEELERS</span> &nbsp; <span class="pill">MADE IN INDIA</span></div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#b8cce0;font-size:13px;letter-spacing:2px">MADE BY <b style="color:#fff">AJIT GORAI</b><br>JHARKHAND, INDIA 🇮🇳</div>', unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="model-visual pulse" style="height:260px;font-size:100px;border-radius:22px">
        🏍️
        </div>
        <div style="text-align:center;color:#8fa9c2;font-size:12px;margin-top:10px;letter-spacing:2px">PRECISION · PERFORMANCE · INSIGHT</div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    auth_col, _ = st.columns([0.8, 0.2])
    with auth_col:
        st.markdown("### Get started")
        st.caption("Sign in or create your free account to open your workspace.")
        mode = st.radio("Choose", ["Login", "Create account"], horizontal=True, label_visibility="collapsed", key="auth_mode")
        with st.container(border=True):
            if mode == "Login":
                email = st.text_input("Email address", placeholder="you@example.com", key="login_email")
                password = st.text_input("Password", type="password", placeholder="Enter password", key="login_password")
                if st.button("LOGIN TO SCANNER  →", use_container_width=True):
                    if login_user(email.strip().lower(), password):
                        st.rerun()
                    else:
                        st.error("Account not found in this demo session. Create an account below first.")
            else:
                new_email = st.text_input("Email address", placeholder="you@example.com", key="signup_email")
                new_password = st.text_input("Create password", type="password", placeholder="At least 8 characters", key="signup_password")
                confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter password", key="signup_confirm")
                if st.button("CREATE FREE ACCOUNT  →", use_container_width=True):
                    if not new_email or "@" not in new_email:
                        st.error("Please enter a valid email address.")
                    elif len(new_password) < 8:
                        st.error("Password must contain at least 8 characters.")
                    elif new_password != confirm:
                        st.error("Passwords do not match.")
                    elif new_email.strip().lower() in st.session_state.demo_users:
                        st.error("An account with this email already exists in this session.")
                    else:
                        st.session_state.demo_users[new_email.strip().lower()] = new_password
                        st.success("Demo account created. Please switch to Login.")
        st.caption("Prototype note: accounts currently exist only in this browser session. Persistent, secure public accounts require a cloud database and authentication service.")
    footer()
    st.stop()

# --------------------------- SIDEBAR --------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 4px 18px">
      <div style="font-size:11px;color:#58c8ff;letter-spacing:2px;font-weight:700">AJIT GORAI PRESENTS</div>
      <div style="font-family:Space Grotesk;font-size:22px;font-weight:700;color:#f2f7ff">🏍️ OBD SCANNER</div>
      <div style="font-size:10px;color:#8fa5bd;letter-spacing:1px">MOTORCYCLE DIAGNOSTIC SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Hi, {st.session_state.username}**")
    st.caption("FREE ACCOUNT · SIMULATION MODE")
    st.divider()
    menu = ["Dashboard", "Select Vehicle", "Connection Check", "Live Data", "Fault Codes", "Reports", "About"]
    for item in menu:
        if st.button(("●  " if st.session_state.page == item else "　 ") + item,
                     key="nav_" + item, use_container_width=True):
            navigate(item)
            st.rerun()
    st.divider()
    st.markdown("**VEHICLE PROFILE**")
    st.caption(vehicle_name())
    st.caption(f"{st.session_state.selected_year} · {st.session_state.selected_variant}")
    st.divider()
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "Welcome"
        st.session_state.username = ""
        st.rerun()

# --------------------------- TOP BAR --------------------------
top_a, top_b = st.columns([5, 1])
with top_a:
    st.markdown('<div class="eyebrow">MOTORCYCLE DIAGNOSTIC WORKSPACE</div>', unsafe_allow_html=True)
    st.markdown(f"<h1 style='margin:0'>{st.session_state.page}</h1>", unsafe_allow_html=True)
with top_b:
    st.markdown('<div style="text-align:right;padding-top:12px"><span class="pill">● SYSTEM READY</span></div>', unsafe_allow_html=True)
st.divider()

# --------------------------- DASHBOARD ------------------------
if st.session_state.page == "Dashboard":
    st.markdown(f"""
    <div class="hero-panel animate">
      <div class="eyebrow">YOUR WORKSPACE</div>
      <h2 style="font-size:30px;margin:8px 0">Welcome back, {st.session_state.username} 👋</h2>
      <div style="color:#a8bfd5">Your selected vehicle: <b style="color:#fff">{vehicle_name()}</b> · {st.session_state.selected_year} · {st.session_state.selected_variant}</div>
      <div style="margin-top:18px"><span class="pill">SIMULATION MODE</span> &nbsp; <span class="pill">ECU NOT CONNECTED</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("ECU CONNECTION", "Offline", help="No physical scanner is connected.")
    c2.metric("RECORDED SAMPLES", len(st.session_state.history))
    c3.metric("FAULT CODES", "Demo")
    c4.metric("ACCOUNT", "Free")
    st.markdown("### Quick actions")
    q1,q2,q3 = st.columns(3)
    with q1:
        with st.container(border=True):
            st.markdown("### 📈 Live data")
            st.caption("Explore sensor readings and charts.")
            if st.button("Open live data →", key="dash_live", use_container_width=True):
                navigate("Live Data"); st.rerun()
    with q2:
        with st.container(border=True):
            st.markdown("### 🏍️ Select vehicle")
            st.caption("Choose brand, model, year and variant.")
            if st.button("Choose vehicle →", key="dash_vehicle", use_container_width=True):
                navigate("Select Vehicle"); st.rerun()
    with q3:
        with st.container(border=True):
            st.markdown("### 📄 Reports")
            st.caption("Review and export your recorded samples.")
            if st.button("Open reports →", key="dash_reports", use_container_width=True):
                navigate("Reports"); st.rerun()
    st.warning("DEMO MODE: No motorcycle ECU is connected. All displayed sensor readings are simulated.")

# --------------------------- VEHICLE GALLERY ------------------
elif st.session_state.page == "Select Vehicle":
    st.markdown('<div class="eyebrow">STEP 1 · MANUFACTURER</div>', unsafe_allow_html=True)
    st.markdown("### Choose your vehicle brand")
    brands = list(CATALOGUE.keys())
    brand_cols = st.columns(6)
    for idx, brand in enumerate(brands):
        with brand_cols[idx % 6]:
            selected = st.session_state.selected_brand == brand
            mark = BRAND_MARKS[brand]
            color = BRAND_COLORS[brand]
            st.markdown(f"""
            <div class="brand-card" style="border-color:{'#3caeff' if selected else '#25425e'}">
              <div class="brand-mark" style="color:{color}">{mark}</div>
              <div style="font-size:12px;font-weight:700;color:#eaf3ff">{brand}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Selected" if selected else "Choose", key="brand_" + brand, use_container_width=True):
                st.session_state.selected_brand = brand
                st.session_state.selected_model = CATALOGUE[brand][0]
                st.rerun()

    st.divider()
    st.markdown('<div class="eyebrow">STEP 2 · MODEL</div>', unsafe_allow_html=True)
    st.markdown(f"### Select a {st.session_state.selected_brand} model")
    search = st.text_input("Search model", placeholder="Type model name...", label_visibility="collapsed", key="model_search")
    models = [m for m in CATALOGUE[st.session_state.selected_brand] if search.lower() in m.lower()]
    if not models:
        st.info("No matching model. Try another search.")
    else:
        model_cols = st.columns(4)
        for idx, model in enumerate(models):
            with model_cols[idx % 4]:
                selected = st.session_state.selected_model == model
                st.markdown(f"""
                <div class="model-card" style="border-color:{'#39aaff' if selected else '#24415d'}">
                  <div class="model-visual">🏍️</div>
                  <div style="font-weight:700;color:#f2f7ff;margin-top:9px">{model}</div>
                  <div style="font-size:10px;color:#8fa5bd;margin-top:3px">{st.session_state.selected_brand}</div>
                </div>""", unsafe_allow_html=True)
                if st.button("✓ Selected" if selected else "Select model", key="model_" + st.session_state.selected_brand + "_" + str(idx), use_container_width=True):
                    st.session_state.selected_model = model
                    st.rerun()
    st.divider()
    st.markdown('<div class="eyebrow">STEP 3 · VEHICLE DETAILS</div>', unsafe_allow_html=True)
    d1,d2,d3 = st.columns([1,1,1.3])
    with d1:
        st.session_state.selected_year = st.selectbox("Manufacturing year", list(range(2026, 1999, -1)), index=list(range(2026, 1999, -1)).index(st.session_state.selected_year) if st.session_state.selected_year in range(2000,2027) else 4)
    with d2:
        st.session_state.selected_variant = st.selectbox("Variant", ["Standard", "Base", "Deluxe", "Disc", "Drum", "ABS", "Other"])
    with d3:
        st.markdown(f"""
        <div class="model-card" style="padding:16px">
          <div class="eyebrow">SELECTED VEHICLE</div>
          <div style="font-size:18px;font-weight:700;color:#fff">{vehicle_name()}</div>
          <div style="color:#9db3ca;font-size:12px">{st.session_state.selected_year} · {st.session_state.selected_variant}</div>
        </div>""", unsafe_allow_html=True)
    if st.button("CONFIRM VEHICLE  →", use_container_width=True):
        st.session_state.selected_vehicle_confirmed = True
        st.session_state.connection_check_started = False
        st.session_state.page = "Connection Check"
        st.rerun()
    st.caption("Catalogue contains starter model examples, not every model. Model selection does not confirm ECU compatibility. Model photos and official brand logo assets can be added after sourcing verified image assets.")

# ----------------------- CONNECTION CHECK ----------------------
elif st.session_state.page == "Connection Check":
    st.markdown('<div class="eyebrow">STEP 4 · HARDWARE CONNECTION</div>', unsafe_allow_html=True)
    st.markdown("### Check your scanner connection")
    st.markdown(
        f"Selected vehicle: **{vehicle_name()} · {st.session_state.selected_year} · "
        f"{st.session_state.selected_variant}**"
    )
    st.info(
        "This is the connection-check interface preview. The current app has no physical "
        "scanner driver or bike connected, so it cannot automatically detect the USB adapter, "
        "coupler or ECU yet."
    )

    checks = [
        ("01", "USB / Bluetooth scanner", "Waiting for compatible scanner hardware"),
        ("02", "Bike coupler", "Cannot verify until the scanner and correct bike cable are connected"),
        ("03", "ECU communication", "Requires verified vehicle protocol and a successful ECU handshake"),
    ]
    for number, heading, detail in checks:
        with st.container(border=True):
            left, right = st.columns([0.15, 0.85], vertical_alignment="center")
            with left:
                st.markdown(
                    f'<div style="font-size:22px;font-weight:800;color:#72e0d5">{number}</div>',
                    unsafe_allow_html=True
                )
            with right:
                st.markdown(f"**{heading}**")
                st.caption(detail)
                st.markdown('<span class="pill">NOT VERIFIED</span>', unsafe_allow_html=True)

    st.warning(
        "Do not connect wires to unknown ECU pins or apply 12V to an unidentified connector. "
        "The exact wiring and protocol must be verified for the selected motorcycle."
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("↻ CHECK HARDWARE (NOT AVAILABLE YET)", use_container_width=True):
            st.warning("Automatic checking will be enabled after scanner hardware and its driver are integrated.")
    with c2:
        if st.button("OPEN DEMO LIVE DATA →", use_container_width=True):
            st.session_state.page = "Live Data"
            st.rerun()
    st.caption("Demo Live Data uses generated sample values only. It is not a real ECU connection.")

# --------------------------- LIVE DATA ------------------------
elif st.session_state.page == "Live Data":
    st.markdown("### Sensor monitoring")
    st.warning("SIMULATION MODE — These values are randomly generated and are not actual ECU measurements.")
    a,b,c = st.columns(3)
    with a:
        if st.button("▶ START (ADD DEMO SAMPLE)", use_container_width=True):
            st.session_state.recording = True
            st.session_state.history.append(sample_reading())
    with b:
        if st.button("■ STOP MONITORING", use_container_width=True):
            st.session_state.recording = False
    with c:
        if st.button("＋ ADD SAMPLE", use_container_width=True):
            st.session_state.history.append(sample_reading())
    st.caption("This prototype adds a sample when you press Start or Add Sample; it is not continuous live ECU monitoring.")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        latest = df.iloc[-1]
        st.markdown("#### Latest readings")
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Engine RPM", f"{latest['RPM']} rpm")
        m2.metric("Engine temperature", f"{latest['Engine Temperature (°C)']} °C")
        m3.metric("Throttle", f"{latest['Throttle Position (%)']} %")
        m4.metric("Battery", f"{latest['Battery Voltage (V)']} V")
        m5,m6,m7,m8 = st.columns(4)
        m5.metric("Engine load", f"{latest['Engine Load (%)']} %")
        m6.metric("Speed", f"{latest['Vehicle Speed (km/h)']} km/h")
        m7.metric("Intake temperature", f"{latest['Intake Air Temperature (°C)']} °C")
        m8.metric("MAP pressure", f"{latest['MAP Pressure (kPa)']} kPa")
        sensors = ["RPM","Engine Temperature (°C)","Throttle Position (%)","Battery Voltage (V)","Engine Load (%)","Vehicle Speed (km/h)","Intake Air Temperature (°C)","MAP Pressure (kPa)","Fuel Level (%)","Oxygen Sensor (V)","Ignition Timing (°)"]
        selected = st.multiselect("Choose sensors to graph", sensors, default=sensors[:4])
        if selected:
            st.line_chart(df.set_index("Time")[selected], use_container_width=True)
        st.markdown("#### Recorded samples")
        st.dataframe(df.tail(50).iloc[::-1], use_container_width=True, hide_index=True)
        st.download_button("⬇ DOWNLOAD CSV", df.to_csv(index=False).encode("utf-8"), "Motorcycle_OBD_Report.csv", "text/csv")
    else:
        st.info("No samples yet. Press Add Sample to generate demo readings.")

# --------------------------- FAULT CODES ----------------------
elif st.session_state.page == "Fault Codes":
    st.markdown("### Diagnostic trouble codes")
    st.warning("DEMO EXAMPLES ONLY — No fault codes are being read from a motorcycle.")
    faults = {
        "P0107": ("MAP / Barometric Pressure Circuit Low", "Sensor circuit voltage below expected range", "Check wiring and sensor only after vehicle-specific diagnosis."),
        "P0115": ("Engine Coolant Temperature Sensor Circuit", "Temperature sensor circuit fault example", "Verify the sensor type and service manual before testing."),
        "P0120": ("Throttle Position Sensor Circuit", "Throttle position circuit fault example", "Inspect connector and reference voltage using verified service data."),
        "P0130": ("Oxygen Sensor Circuit", "Oxygen sensor circuit fault example", "Confirm whether the selected vehicle uses this sensor and protocol."),
        "P0560": ("System Voltage Malfunction", "System voltage fault example", "Check battery and charging system to the manufacturer's procedure."),
    }
    for code,(title,detail,action) in faults.items():
        with st.container(border=True):
            x,y = st.columns([1,4])
            with x:
                st.markdown(f"<h2 style='color:#ffbd69'>{code}</h2>", unsafe_allow_html=True)
                st.caption("EXAMPLE")
            with y:
                st.markdown(f"**{title}**")
                st.caption(detail)
                st.write(action)

# --------------------------- REPORTS --------------------------
elif st.session_state.page == "Reports":
    st.markdown("### Your diagnostic reports")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.metric("Total demo samples", len(df))
        st.dataframe(df.tail(100).iloc[::-1], use_container_width=True, hide_index=True)
        st.download_button("⬇ DOWNLOAD COMPLETE CSV", df.to_csv(index=False).encode("utf-8"), "Motorcycle_OBD_Report.csv", "text/csv")
    else:
        st.info("No report data yet. Visit Live Data and add a demo sample.")

# --------------------------- ABOUT ----------------------------
elif st.session_state.page == "About":
    st.markdown("""
    <div class="hero-panel">
      <div class="eyebrow">ABOUT THE PROJECT</div>
      <h2>Motorcycle OBD Scanner Tool</h2>
      <p style="color:#a9bfd5">A multi-brand two-wheeler diagnostic software prototype.</p>
      <h3>Made by Ajit Gorai</h3>
      <p>Jharkhand, India 🇮🇳</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("**Current prototype modules**")
    st.write("- Vehicle brand and model selection")
    st.write("- Simulated sensor dashboard")
    st.write("- Example fault-code reference")
    st.write("- CSV sample reports")
    st.info("Real ECU communication, reading/clearing faults and supported resets require verified vehicle-specific protocols and compatible hardware.")

footer()
