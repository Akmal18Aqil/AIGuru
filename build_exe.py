import PyInstaller.__main__
import os
import shutil
from pathlib import Path

def build():
    # Remove old builds
    if os.path.exists("build"): shutil.rmtree("build")
    if os.path.exists("dist"): shutil.rmtree("dist")
    
    print("🚀 Memulai proses pengemasan SiGURU ke .EXE...")
    
    # PyInstaller arguments
    # --onefile: Create a single executable
    # --additional-hooks-dir: Streamlit needs specific hooks
    # --collect-all: Ensure all streamlit assets are included
    # --add-data: Include project folders
    
    args = [
        'run_app.py',
        '--name=SiGURU_AI',
        '--onefile',
        '--windowed',
        '--clean',
        '--add-data=ui;ui',
        '--add-data=ai_guru;ai_guru',
        '--collect-all=streamlit',
        '--collect-all=langgraph',
        '--collect-all=langchain',
        '--collect-all=google',
        '--hidden-import=streamlit.web.cli',
    ]
    
    PyInstaller.__main__.run(args)
    
    # Cleanup after build
    print("🧹 Membersihkan file temporary...")
    if os.path.exists("build"): shutil.rmtree("build")
    spec_file = Path("SiGURU_AI.spec")
    if spec_file.exists(): spec_file.unlink()
    
    print("\n✅ SELESAI! File .EXE Anda ada di folder: dist/SiGURU_AI.exe")
    print("Anda bisa membagikan file tersebut ke guru-guru.")

if __name__ == "__main__":
    build()
