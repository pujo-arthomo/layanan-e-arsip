import streamlit as st
from supabase import create_client
from datetime import datetime

st.set_page_config(page_title="Layanan Permohonan Arsip", layout="centered")

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.last_data = {}

st.markdown("## 🏛️ Layanan Permohonan Arsip")
st.divider()

if not st.session_state.submitted:
    with st.form("form"):
        nama = st.text_input("Nama Lengkap")
        domisili = st.text_input("Domisili")
        no_rekom = st.text_input("Nomor Surat Rekomendasi DPMPTSP")
        submit = st.form_submit_button("Kirim")

    if submit:
        if not nama or not domisili or not no_rekom:
            st.error("Semua kolom wajib diisi")
        else:
            payload = {
                "waktu_pengajuan": datetime.utcnow().isoformat(),
                "nama": nama,
                "domisili": domisili,
                "no_rekomendasi": no_rekom
            }

            supabase.table("permohonan_arsip").insert(payload).execute()

            st.session_state.submitted = True
            st.session_state.last_data = payload
            st.rerun()
else:
    d = st.session_state.last_data
    st.success("Permohonan berhasil dicatat")
    st.write(d)

    if st.button("Selesai"):
        st.session_state.submitted = False
        st.session_state.last_data = {}
        st.rerun()
