import sys
import streamlit.web.cli as stcli
import os
import traceback
from pathlib import Path


def ensure_appdata_dirs():
    """
    Pastikan semua subfolder di APPDATA/SiGURU_AI ada sebelum Streamlit dijalankan.
    Ini mencegah FileNotFoundError saat aplikasi pertama kali dijalankan.
    """
    try:
        from ai_guru.utils.path_utils import get_persistent_data_dir
        data_dir = get_persistent_data_dir()
        # Subfolder yang harus ada
        subdirs = ["logs", "temp_upload"]
        for sub in subdirs:
            (data_dir / sub).mkdir(parents=True, exist_ok=True)
        print(f"✅ Data folder siap: {data_dir}")
    except Exception as e:
        # Jangan crash — hanya log warning
        print(f"⚠️  Gagal inisialisasi folder APPDATA: {e}")


if __name__ == "__main__":
    try:
        from ai_guru.utils.path_utils import get_resource_path

        # Pastikan folder APPDATA tersedia sebelum apapun dijalankan
        ensure_appdata_dirs()

        # Cari app.py di dalam bundle (frozen) atau di folder proyek (dev)
        app_path = get_resource_path("ui/app.py")

        print("====================================================")
        print("          SIGURU AI ASSISTANT STARTUP               ")
        print("====================================================")
        print(f"DEBUG: Resource path: {app_path}")

        if not app_path.exists():
            print(f"ERROR: File antarmuka (ui/app.py) tidak ditemukan di {app_path}")
            # Fallback untuk development
            current_dir = Path(__file__).parent
            app_path = current_dir / "ui" / "app.py"
            print(f"DEBUG: Mencoba fallback ke: {app_path}")

        if not app_path.exists():
            raise FileNotFoundError(f"CRITICAL ERROR: ui/app.py tidak ditemukan di manapun.")

        sys.argv = [
            "streamlit",
            "run",
            str(app_path),
            "--global.developmentMode=false",
            "--server.port=8501",
            "--server.address=localhost",
            "--server.headless=true",          # Tidak buka browser otomatis di beberapa env
            "--browser.gatherUsageStats=false", # Matikan telemetri Streamlit
        ]

        print("🚀 Membuka antarmuka... Mohon tunggu sebentar.")
        sys.exit(stcli.main())

    except Exception as e:
        print("\n" + "!" * 50)
        print("CRITICAL ERROR DURING STARTUP:")
        print(str(e))
        print("!" * 50)
        traceback.print_exc()
        print("\n" + "=" * 50)
        input("Tekan ENTER untuk menutup jendela ini...")
        sys.exit(1)
