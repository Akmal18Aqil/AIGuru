import PyInstaller.__main__
import os
import shutil
from pathlib import Path


def build():
    # Remove old builds
    if os.path.exists("build"): shutil.rmtree("build")
    if os.path.exists("dist"):  shutil.rmtree("dist")

    print("🚀 Memulai proses pengemasan SiGURU ke folder dist/ ...")
    print("   Mode: --onedir (startup lebih cepat, tidak perlu extract ke TEMP)")

    # ── CATATAN ARSITEKTUR ─────────────────────────────────────────────────────
    # --onedir  : lebih cepat startup (~3s vs ~60s), distribusi lewat Inno Setup
    # --add-data: bundle file READ-ONLY (kode, template)
    #             Data WRITABLE (config.json, .env, .salt) disimpan di APPDATA
    #             otomatis oleh path_utils.get_persistent_data_dir()
    # ──────────────────────────────────────────────────────────────────────────

    args = [
        'run_app.py',
        '--name=SiGURU_AI',

        # ── Mode distribusi ───────────────────────────────────────────────────
        '--onedir',           # Hasilkan folder, bukan 1 file lambat
        '--console',          # Tampilkan console (untuk debug & log startup)
        '--noconfirm',
        '--clean',

        # ── Bundle kode & aset read-only ─────────────────────────────────────
        '--add-data=ui;ui',
        '--add-data=ai_guru;ai_guru',
        '--add-data=templates;templates',   # ← FIX: template DOCX untuk RPP/Soal

        # ── Hooks ────────────────────────────────────────────────────────────
        '--additional-hooks-dir=hooks',     # ← FIX: daftarkan hook-streamlit.py

        # ── Collect semua modul yang dibutuhkan ──────────────────────────────
        '--collect-all=streamlit',
        '--collect-all=langgraph',
        '--collect-all=langchain',
        '--collect-all=langchain_core',
        '--collect-all=google',
        '--collect-all=docxtpl',
        '--collect-all=docx',
        '--collect-all=pypdf',
        '--collect-all=openpyxl',
        '--collect-all=pandas',
        '--collect-all=cryptography',
        '--collect-all=supabase',

        # ── Hidden imports ────────────────────────────────────────────────────
        '--hidden-import=streamlit.web.cli',
        '--hidden-import=streamlit.runtime.scriptrunner.magic_funcs',
        '--hidden-import=docxtpl',
        '--hidden-import=docx',
        '--hidden-import=langchain_google_genai',
        '--hidden-import=langchain_openai',
        '--hidden-import=langchain_groq',
        '--hidden-import=langchain_anthropic',
    ]

    PyInstaller.__main__.run(args)

    # Cleanup setelah build
    print("\n🧹 Membersihkan file temporary build...")
    if os.path.exists("build"): shutil.rmtree("build")
    spec_file = Path("SiGURU_AI.spec")
    if spec_file.exists(): spec_file.unlink()

    dist_path = Path("dist") / "SiGURU_AI"
    print("\n" + "="*60)
    print("  ✅ SELESAI! Folder distribusi ada di:")
    print(f"     {dist_path.absolute()}")
    print()
    print("  Langkah selanjutnya:")
    print("  1. Buka Inno Setup Compiler")
    print("  2. Compile siguru_setup_script.iss")
    print("  3. Bagikan file SiGURU_Setup_vX.X.X.exe ke guru-guru")
    print("="*60)


if __name__ == "__main__":
    build()
