import streamlit as st
from supabase import create_client
from datetime import datetime, timezone

st.set_page_config(page_title="Layanan Permohonan Arsip", layout="centered")

# Initialize Supabase client
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Initialize session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.last_data = {}

# Header
st.markdown("## 🏛️ Layanan Permohonan Arsip")
st.divider()

# Main form
if not st.session_state.submitted:
    with st.form("form"):
        nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama lengkap Anda")
        domisili = st.text_input("Domisili", placeholder="Masukkan alamat domisili")
        no_rekom = st.text_input("Nomor Surat Rekomendasi DPMPTSP", placeholder="Contoh: 123/REK/2024")
        submit = st.form_submit_button("Kirim", use_container_width=True)

    if submit:
        # Validation
        if not nama or not domisili or not no_rekom:
            st.error("⚠️ Semua kolom wajib diisi")
        else:
            # Prepare payload
            payload = {
                "waktu_pengajuan": datetime.now(timezone.utc).isoformat(),
                "nama": nama.strip(),
                "domisili": domisili.strip(),
                "no_rekomendasi": no_rekom.strip()
            }

            # Insert to Supabase with error handling
            try:
                response = supabase.table("permohonan_arsip").insert(payload).execute()
                
                st.session_state.submitted = True
                st.session_state.last_data = payload
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat menyimpan data")
                st.error(f"Detail error: {str(e)}")
                
                # Troubleshooting hints
                with st.expander("💡 Solusi Troubleshooting"):
                    st.write("""
                    **Kemungkinan penyebab error:**
                    1. **RLS (Row Level Security)** aktif di Supabase tanpa policy INSERT
                    2. Menggunakan **anon key** instead of **service_role key**
                    3. **Schema tabel** tidak sesuai dengan payload
                    4. **Network issue** atau Supabase sedang down
                    
                    **Cara mengatasinya:**
                    - Cek Supabase Dashboard → Table `permohonan_arsip`
                    - Matikan RLS atau buat policy untuk INSERT
                    - Gunakan `service_role key` di secrets
                    - Pastikan kolom tabel sesuai: `waktu_pengajuan`, `nama`, `domisili`, `no_rekomendasi`
                    """)

# Success page
else:
    d = st.session_state.last_data
    
    st.success("✅ Permohonan berhasil dicatat!")
    st.balloons()
    
    # Display submitted data
    st.markdown("### 📋 Data yang Telah Diajukan:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Nama Lengkap", d.get("nama", "-"))
        st.metric("Domisili", d.get("domisili", "-"))
    
    with col2:
        st.metric("No. Rekomendasi", d.get("no_rekomendasi", "-"))
        waktu = d.get("waktu_pengajuan", "-")
        if waktu != "-":
            waktu_display = datetime.fromisoformat(waktu.replace('Z', '+00:00')).strftime("%d/%m/%Y %H:%M")
            st.metric("Waktu Pengajuan", waktu_display)
    
    st.divider()
    
    # Reset button
    if st.button("🔄 Ajukan Permohonan Baru", use_container_width=True):
        st.session_state.submitted = False
        st.session_state.last_data = {}
        st.rerun()
