"""
Setup Wizard - First Time Configuration
Halaman untuk setup awal aplikasi SiGURU
"""

import streamlit as st
import sys
import os

# Add src to pythonpath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_guru.config.api_key_manager import APIKeyManager

st.set_page_config(
    page_title="Setup - SiGURU",
    page_icon="⚙️",
    layout="centered"
)

# Custom CSS untuk setup wizard
st.markdown("""
<style>
    .big-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .success-box {
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Hide Streamlit Branding & Deploy Button */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stAppDeployButton"] {display: none;}

    /* === PAGE TRANSITIONS === */
    .stApp {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Loading overlay for navigation */
    #nav-loading {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #4A90E2, #357ABD, #4A90E2);
        background-size: 200% 100%;
        animation: navLoading 2s infinite linear;
        z-index: 1000;
        display: none;
    }
    
    @keyframes navLoading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>

<!-- Navigation Loading Bar -->
<div id="nav-loading"></div>

<script>
    // Logic to show loading bar when buttons are clicked
    const buttons = window.parent.document.querySelectorAll('button');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const loader = window.parent.document.getElementById('nav-loading');
            if (loader) loader.style.display = 'block';
        });
    });
</script>
""", unsafe_allow_html=True)

# Initialize API Manager
api_manager = APIKeyManager()

# Initialize session state
if 'setup_step' not in st.session_state:
    st.session_state['setup_step'] = 1
if 'deployment_type' not in st.session_state:
    st.session_state['deployment_type'] = None

# ===== STEP 1: Welcome & Deployment Type Selection =====
if st.session_state['setup_step'] == 1:
    st.markdown('<p class="big-title">🎓 Selamat Datang di SiGURU!</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Asisten AI untuk Guru Indonesia</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Pilih Tipe Deployment")
    st.info("""
    **Lisensi Organisasi** cocok untuk:
    - Seluruh guru di sekolah/yayasan menggunakan 1 API key yang sama
    - Setup sekali oleh admin IT, semua guru langsung bisa pakai
    - Lebih mudah untuk manajemen dan monitoring
    """)
    
    deployment = st.radio(
        "Tipe Deployment:",
        ["Lisensi Organisasi (Rekomendasi)", "Lisensi Individual (Coming Soon)"],
        key="deployment_radio"
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Lanjutkan ➡️", type="primary"):
            if "Organisasi" in deployment:
                st.session_state['deployment_type'] = 'organization'
                st.session_state['setup_step'] = 2
                st.rerun()
            else:
                st.warning("Lisensi Individual akan tersedia segera. Silakan pilih Lisensi Organisasi.")

# ===== STEP 2: License Key Validation (NEW!) =====
elif st.session_state['setup_step'] == 2:
    st.markdown('<p class="big-title">🔐 Validasi Lisensi</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Aktivasi SiGURU untuk Organisasi Anda</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.info("""
    📧 Masukkan **License Key** yang Anda dapatkan dari:
    - Email konfirmasi pembelian
    - Dashboard admin SiGURU
    - Tim support kami
    """)
    
    license_input = st.text_input(
        "License Key",
        type="password",
        placeholder="SIGURU-XXXX-XXXX-XXXX",
        help="License key akan divalidasi sebelum melanjutkan setup"
    )
    
    st.caption("📝 **Format:** `SIGURU-[NAMA-ORGANISASI]` atau `DEV-MODE-123` untuk testing")
    
    with st.expander("❓ Belum punya License Key?"):
        st.markdown("""
        **Untuk mendapatkan License Key:**
        
        1. 📧 Hubungi tim sales kami di: sales@siguru.app
        2. 💬 WhatsApp: +62-XXX-XXXX-XXXX 
        3. 🌐 Kunjungi: https://siguru.app/pricing
        
        **Untuk Testing/Demo:**
        - Gunakan: `DEV-MODE-123` (tidak ada batasan)
        - Atau format: `SIGURU-[NAMA-SEKOLAH-ANDA]`
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Kembali"):
            st.session_state['setup_step'] = 1
            st.rerun()
    
    with col2:
        if st.button("Validasi & Lanjutkan ✅", type="primary"):
            if not license_input:
                st.error("License Key wajib diisi!")
            elif len(license_input) < 8:
                st.error("License Key tidak valid (terlalu pendek)")
            else:
                with st.spinner("🔍 Memvalidasi license..."):
                    from ai_guru.utils.licensing import LicenseManager
                    manager = LicenseManager()
                    
                    if manager.verify_license(license_input):
                        st.session_state['license_key'] = license_input
                        st.session_state['setup_step'] = 3  # Go to API key step
                        st.success("✅ License valid!")
                        st.rerun()
                    else:
                        st.error("""
                        ❌ **License tidak valid atau sudah expired!**
                        
                        Mohon periksa kembali license key Anda:
                        - Pastikan tidak ada spasi atau karakter tambahan
                        - License belum expired
                        - License sesuai dengan organisasi Anda
                        
                        💡 **Tips:**
                        - Untuk testing, gunakan: `DEV-MODE-123`
                        - Atau gunakan format: `SIGURU-NAMA-SEKOLAH`
                        """)

# ===== STEP 3: API Key Input (Previously Step 2) =====
elif st.session_state['setup_step'] == 3:
    st.markdown('<p class="big-title">🔑 Setup API Key</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Organization info
    st.markdown("### Informasi Lembaga")
    organization_name = st.text_input(
        "Nama Sekolah/Lembaga",
        placeholder="Contoh: SDN 01 Jakarta",
        help="Nama ini akan ditampilkan di aplikasi"
    )
    
    st.markdown("### LLM Provider Konfigurasi")
    
    # Provider Selection
    provider_options = ["Google Gemini", "OpenRouter", "Groq", "Anthropic", "Custom Provider"]
    selected_provider = st.selectbox(
        "Pilih AI Provider",
        options=provider_options,
        index=0,
        help="Google Gemini adalah opsi default dengan integrasi terbaik untuk Free Tier."
    )
    
    # Dynamic Help Text
    if selected_provider == "Google Gemini":
        with st.expander("ℹ️ Cara mendapatkan Google API Key"):
            st.markdown("""
            1. Buka [Google AI Studio](https://aistudio.google.com/apikey)
            2. Login dengan akun Google Anda
            3. Klik "Create API Key"
            4. Copy API key yang muncul
            """)
    elif selected_provider == "OpenRouter":
        with st.expander("ℹ️ Cara mendapatkan OpenRouter API Key"):
            st.markdown("""
            1. Buka [OpenRouter.ai](https://openrouter.ai/keys)
            2. Buat akun dan top-up (atau pilih model gratis)
            3. Generate API Key
            """)
    elif selected_provider == "Groq":
        with st.expander("ℹ️ Cara mendapatkan Groq API Key"):
            st.markdown("""
            1. Buka [Groq Console](https://console.groq.com/keys)
            2. Login dan generate API Key yang sangat cepat ini!
            """)
    elif selected_provider == "Anthropic":
        with st.expander("ℹ️ Cara mendapatkan Anthropic API Key"):
            st.markdown("""
            1. Buka [Anthropic Console](https://console.anthropic.com/)
            2. Login dan generate API Key (Berbayar)
            """)
    
    # Custom fields if applicable
    custom_base_url = ""
    custom_model_name = ""
    if selected_provider == "Custom Provider":
        col_url, col_model = st.columns(2)
        with col_url:
            custom_base_url = st.text_input(
                "Base URL", 
                placeholder="http://localhost:11434/v1",
                help="URL server AI (contoh: Ollama local API)"
            )
        with col_model:
            custom_model_name = st.text_input(
                "Model Name",
                placeholder="llama3",
                help="Nama model yang digunakan"
            )
    
    api_key_input = st.text_input(
        f"Masukkan API Key ({selected_provider})",
        type="password",
        placeholder="AIzaSy... atau sk-...",
        help="API key akan disimpan dengan aman"
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Kembali"):
            st.session_state['setup_step'] = 2  # Back to license step
            st.rerun()
    
    with col2:
        if st.button("Test & Simpan ✅", type="primary"):
            if not organization_name:
                st.error("Nama lembaga wajib diisi!")
            elif not api_key_input:
                st.error("API Key wajib diisi!")
            elif selected_provider == "Google Gemini" and len(api_key_input) < 30:
                st.error("API Key Google tidak valid (terlalu pendek)")
            elif len(api_key_input) < 5:
                st.error("API Key tidak valid (terlalu pendek)")
            else:
                with st.spinner("🧪 Memvalidasi API key..."):
                    # Save setup with license key and specific provider details
                    license_key = st.session_state.get('license_key', '')
                    
                    success = api_manager.save_organization_setup(
                        api_key=api_key_input,
                        organization_name=organization_name,
                        license_key=license_key,
                        provider=selected_provider,
                        custom_base_url=custom_base_url,
                        custom_model_name=custom_model_name
                    )
                    
                    if success:
                        st.session_state['setup_step'] = 4
                        st.session_state['org_name'] = organization_name
                        st.rerun()
                    else:
                        st.error("""
                        ❌ **API Key tidak valid!**
                        
                        Mohon periksa kembali API key Anda. Pastikan:
                        - API key sudah benar (tidak ada spasi atau karakter tambahan)
                        - API key masih aktif
                        - Anda memiliki koneksi internet
                        """)

# ===== STEP 4: Success (Previously Step 3) =====
elif st.session_state['setup_step'] == 4:
    st.markdown('<p class="big-title">✅ Setup Berhasil!</p>', unsafe_allow_html=True)
    
    org_name = st.session_state.get('org_name', 'Organisasi Anda')
    
    st.markdown(f"""
    <div class="success-box">
        <h2>🎉 Selamat!</h2>
        <p style="font-size: 1.2rem; margin: 1rem 0;">
            SiGURU telah berhasil dikonfigurasi untuk<br/>
            <strong>{org_name}</strong>
        </p>
        <p style="margin-top: 1.5rem;">
            Semua guru di lembaga Anda sekarang dapat menggunakan aplikasi ini
            tanpa perlu setup tambahan!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ✨ Langkah Selanjutnya:")
    st.markdown("""
    1. ✅ Konfigurasi telah tersimpan di file `.env` dan `config.json`
    2. 🔐 License key tervalidasi dan tersimpan
    3. 📚 Mulai buat Modul Ajar (RPP) atau Jadwal Pelajaran
    4. 👥 Bagikan aplikasi ini ke guru-guru lain (mereka tidak perlu setup lagi!)
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Mulai Menggunakan SiGURU", type="primary"):
            # Clear setup state
            st.session_state['setup_step'] = 1
            st.session_state['deployment_type'] = None
            if 'org_name' in st.session_state:
                del st.session_state['org_name']
            if 'license_key' in st.session_state:
                del st.session_state['license_key']
            
            # Redirect to main page
            st.switch_page("app.py")
    
    st.markdown("---")
    st.caption("💡 **Tip:** Jika Anda perlu mengubah konfigurasi nanti, Anda bisa mengedit file `.env` secara manual atau menjalankan setup ulang.")

