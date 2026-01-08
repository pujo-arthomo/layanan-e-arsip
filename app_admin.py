import streamlit as st
import pandas as pd
from supabase import create_client

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Admin Diskarpus", layout="wide")

ADMIN_USER = "admin"
ADMIN_PASS = "arsip123"

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================
# SESSION LOGIN
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.logged_in:
    st.markdown("## 🔐 Login Admin Diskarpus")

    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        login = st.form_submit_button("Masuk")

    if login:
        if u == ADMIN_USER and p == ADMIN_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Username atau password salah")

# =========================
# DASHBOARD
# =========================
else:
    st.sidebar.title("📁 Admin Diskarpus")
    menu = st.sidebar.radio(
        "Menu",
        [
            "📊 Dashboard",
            "📄 Permohonan Arsip",
            "🗄️ Koleksi Arsip",
            "➕ Input Arsip"
        ]
    )

    # =========================
    # DASHBOARD HOME
    # =========================
    if menu == "📊 Dashboard":
        st.markdown("## 📊 Dashboard Admin")
        st.write("Selamat datang di sistem kearsipan Diskarpus.")

    # =========================
    # PERMOHONAN ARSIP
    # =========================
    elif menu == "📄 Permohonan Arsip":
        st.markdown("## 📄 Permohonan Arsip")

        res = supabase.table("permohonan_arsip") \
            .select("*") \
            .order("waktu_pengajuan", desc=True) \
            .execute()

        df = pd.DataFrame(res.data)

        if df.empty:
            st.info("Belum ada permohonan.")
        else:
            st.dataframe(df, use_container_width=True)

    # =========================
    # KOLEKSI ARSIP (READ)
    # =========================
    elif menu == "🗄️ Koleksi Arsip":
        st.markdown("## 🗄️ Koleksi Arsip Diskarpus")

        res = supabase.table("koleksi_arsip") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()

        df = pd.DataFrame(res.data)

        if df.empty:
            st.info("Belum ada data koleksi arsip.")
        else:
            # Nomor urut UI
            df.insert(0, "No", range(1, len(df) + 1))

            st.dataframe(
                df[
                    [
                        "No",
                        "no_berkas",
                        "kode_klasifikasi",
                        "lokasi_bangunan",
                        "jenis_bangunan",
                        "kurun_waktu",
                        "jumlah_arsip",
                        "tingkat_perkembangan",
                        "keterangan_boks"
                    ]
                ],
                use_container_width=True
            )

    # =========================
    # INPUT ARSIP MANUAL
    # =========================
    elif menu == "➕ Input Arsip":
        st.markdown("## ➕ Input Koleksi Arsip Baru")

        with st.form("input_arsip"):
            no_berkas = st.text_input("No Berkas")
            kode_klasifikasi = st.text_input("Kode Klasifikasi")
            lokasi_bangunan = st.text_input("Lokasi Bangunan")
            jenis_bangunan = st.text_input("Jenis Bangunan")
            retribusi = st.text_input("Retribusi")
            kurun_waktu = st.text_input("Kurun Waktu")
            jumlah_arsip = st.number_input("Jumlah Arsip", min_value=0, step=1)
            tingkat_perkembangan = st.text_input("Tingkat Perkembangan")
            keterangan_boks = st.text_input("Keterangan Nomor Boks")

            submit = st.form_submit_button("💾 Simpan Arsip")

        if submit:
            if not no_berkas or not kode_klasifikasi:
                st.error("No Berkas dan Kode Klasifikasi wajib diisi.")
            else:
                supabase.table("koleksi_arsip").insert({
                    "no_berkas": no_berkas,
                    "kode_klasifikasi": kode_klasifikasi,
                    "lokasi_bangunan": lokasi_bangunan,
                    "jenis_bangunan": jenis_bangunan,
                    "retribusi": retribusi,
                    "kurun_waktu": kurun_waktu,
                    "jumlah_arsip": jumlah_arsip,
                    "tingkat_perkembangan": tingkat_perkembangan,
                    "keterangan_boks": keterangan_boks
                }).execute()

                st.success("✅ Arsip berhasil ditambahkan")
                st.rerun()

    st.sidebar.divider()
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()
