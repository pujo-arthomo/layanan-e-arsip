import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Admin Arsip", layout="wide")

ADMIN_USER = "admin"
ADMIN_PASS = "arsip123"

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("## 🔐 Login Admin")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Masuk"):
        if u == ADMIN_USER and p == ADMIN_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Login gagal")

else:
    st.markdown("## 📊 Dashboard Permohonan Arsip")

    res = supabase.table("permohonan_arsip").select("*").order(
        "waktu_pengajuan", desc=True
    ).execute()

    df = pd.DataFrame(res.data)

    if df.empty:
        st.info("Belum ada data.")
    else:
        st.dataframe(df, use_container_width=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
