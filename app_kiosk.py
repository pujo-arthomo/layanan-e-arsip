import streamlit as st
from supabase import create_client
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Layanan Permohonan Arsip",
    layout="centered"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================
# STATE
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
        nama = st.text_input("Nama Lengkap")
        domisili = st.text_input("Domisili")
        no_rekom = st.text_input("Nomor Surat Rekomendasi DPMPTSP")

        submit = st.form_submit_button("📩 Kirim Permohonan")

    if submit:
        if not nama or not domisili or not no_rekom:
            st.error("Semua kolom wajib diisi.")
        else:
            data = {
                "waktu_pengajuan": datetime.now().isoformat(),
                "nama": nama,
                "domisili": domisili,
                "no_rekomendasi": no_rekom
            }

            supabase.table("permohonan_arsip").insert(data).execute()

            st.session_state.submitted = True
            st.session_state.last_data = data
            st.rerun()

else:
    data = st.session_state.last_data

    st.success("✅ Permohonan Anda telah tercatat")
    st.markdown("### 📄 Ringkasan Data Permohonan")

    st.write(f"**Tanggal & Waktu:** {data['waktu_pengajuan']}")
    st.write(f"**Nama:** {data['nama']}")
    st.write(f"**Domisili:** {data['domisili']}")
    st.write(f"**Nomor Rekomendasi:** {data['no_rekomendasi']}")

    st.info("Silakan menuju petugas arsip untuk proses selanjutnya.")

    if st.button("Selesai"):
        st.session_state.submitted = False
        st.session_state.last_data = {}
        st.rerun()
