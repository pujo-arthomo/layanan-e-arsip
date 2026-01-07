import streamlit as st
import pandas as pd
import os
from pandas.errors import EmptyDataError

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Admin - Permohonan Arsip",
    layout="wide"
)

# =========================
# KONFIGURASI LOGIN (CORE)
# =========================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "arsip123"

# =========================
# KONFIGURASI DATA
# =========================
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "submissions.csv")

COLUMNS = [
    "waktu_pengajuan",
    "nama",
    "domisili",
    "no_rekomendasi"
]

# =========================
# PASTIKAN FILE DATA ADA
# =========================
os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)

# =========================
# SESSION STATE LOGIN
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# FUNGSI BACA DATA (AMAN)
# =========================
def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
    except EmptyDataError:
        df = pd.DataFrame(columns=COLUMNS)
    return df

# =========================
# HALAMAN LOGIN
# =========================
if not st.session_state.logged_in:
    st.markdown("## 🔐 Login Petugas Arsip")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Masuk")

    if login_btn:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username atau password salah")

# =========================
# DASHBOARD ADMIN
# =========================
else:
    st.markdown("## 📊 Dashboard Permohonan Arsip")
    st.markdown("Data permohonan yang masuk melalui kiosk")

    st.divider()

    df = load_data()

    if df.empty:
        st.info("Belum ada data permohonan.")
    else:
        # Urutkan terbaru di atas
        df = df.sort_values(by="waktu_pengajuan", ascending=False)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()
