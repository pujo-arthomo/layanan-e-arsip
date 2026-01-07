import streamlit as st
import psycopg2
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Layanan Permohonan Arsip",
    layout="centered"
)

# =========================
# DB CONNECTION
# =========================
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
    )

# =========================
# SESSION STATE
# =========================
if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.last_data = {}

# =========================
# UI
# =========================
st.markdown("## 🏛️ Layanan Permohonan Arsip")
st.markdown("Silakan isi data berikut dengan benar.")
st.divider()

if not st.session_state.submitted:
    with st.form("form_permohonan"):
        nama = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
        domisili = st.text_input("Domisili", placeholder="Contoh: Kota Depok")
        no_rekom = st.text_input(
            "Nomor Surat Rekomendasi DPMPTSP",
            placeholder="Contoh: 123/REK-DPMPTSP/2026"
        )

        submit = st.form_submit_button("📩 Kirim Permohonan")

    if submit:
        if not nama or not domisili or not no_rekom:
            st.error("⚠️ Semua kolom wajib diisi.")
        else:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO permohonan_arsip
                (waktu_pengajuan, nama, domisili, no_rekomendasi)
                VALUES (%s, %s, %s, %s)
                """,
                (datetime.now(), nama, domisili, no_rekom)
            )

            conn.commit()
            cur.close()
            conn.close()

            st.session_state.submitted = True
            st.session_state.last_data = {
                "waktu": datetime.now().strftime("%d %B %Y %H:%M"),
                "nama": nama,
                "domisili": domisili,
                "no_rekom": no_rekom
            }
            st.rerun()

# =========================
# CONFIRMATION SCREEN
# =========================
else:
    data = st.session_state.last_data

    st.success("✅ Permohonan Anda telah tercatat")
    st.markdown("### 📄 Ringkasan Data Permohonan")

    st.write(f"**Tanggal & Waktu:** {data['waktu']}")
    st.write(f"**Nama:** {data['nama']}")
    st.write(f"**Domisili:** {data['domisili']}")
    st.write(f"**Nomor Rekomendasi:** {data['no_rekom']}")

    st.info("Silakan menuju petugas arsip untuk proses selanjutnya.")

    if st.button("🔁 Selesai"):
        st.session_state.submitted = False
        st.session_state.last_data = {}
        st.rerun()
