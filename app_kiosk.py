import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Layanan Permohonan Arsip",
    layout="centered"
)

# =========================
# PATH DATA
# =========================
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "submissions.csv")

# Pastikan folder & file ada
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "waktu_pengajuan",
        "nama",
        "domisili",
        "no_rekomendasi"
    ])
    df_init.to_csv(DATA_FILE, index=False)

# =========================
# STATE
# =========================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "last_data" not in st.session_state:
    st.session_state.last_data = {}

# =========================
# HEADER
# =========================
st.markdown("## 🏛️ Layanan Permohonan Arsip")
st.markdown(
    "Silakan isi data berikut dengan benar untuk mengajukan permohonan arsip."
)
st.divider()

# =========================
# FORM INPUT (KIOSK)
# =========================
if not st.session_state.submitted:
    with st.form("form_permohonan"):
        nama = st.text_input(
            "Nama Lengkap",
            placeholder="Contoh: Budi Santoso"
        )

        domisili = st.text_input(
            "Domisili",
            placeholder="Contoh: Kota Depok"
        )

        no_rekomendasi = st.text_input(
            "Nomor Surat Rekomendasi DPMPTSP",
            placeholder="Contoh: 123/REK-DPMPTSP/2026"
        )

        submit = st.form_submit_button("📩 Kirim Permohonan")

    if submit:
        if not nama or not domisili or not no_rekomendasi:
            st.error("⚠️ Semua kolom wajib diisi.")
        else:
            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_data = {
                "waktu_pengajuan": waktu,
                "nama": nama,
                "domisili": domisili,
                "no_rekomendasi": no_rekomendasi
            }

            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.session_state.last_data = new_data
            st.session_state.submitted = True
            st.rerun()

# =========================
# LAYAR KONFIRMASI
# =========================
else:
    st.success("✅ Permohonan Anda telah tercatat")

    st.markdown("### 📄 Ringkasan Data Permohonan")

    data = st.session_state.last_data

    st.markdown(
        f"""
        **Tanggal & Waktu**  
        {data['waktu_pengajuan']}

        **Nama Pemohon**  
        {data['nama']}

        **Domisili**  
        {data['domisili']}

        **Nomor Surat Rekomendasi**  
        {data['no_rekomendasi']}
        """
    )

    st.info(
        "Silakan menuju petugas arsip untuk proses layanan selanjutnya."
    )

    if st.button("🔁 Selesai"):
        st.session_state.submitted = False
        st.session_state.last_data = {}
        st.rerun()
