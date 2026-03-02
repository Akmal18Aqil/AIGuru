import PyInstaller.__main__
import os
import shutil

# Define paths
current_dir = os.getcwd()
app_path = os.path.join(current_dir, 'ui', 'app.py')
dist_path = os.path.join(current_dir, 'dist')
work_path = os.path.join(current_dir, 'build')

# Clean previous builds
if os.path.exists(dist_path):
    shutil.rmtree(dist_path)
if os.path.exists(work_path):
    shutil.rmtree(work_path)

print("🚀 Starting Build Process... (This may take a while)")

# PyInstaller arguments
args = [
    app_path, # Main file
    '--name=SiGURU',
    '--onefile', # Single .exe file
    '--clean',
    '--noconsole', # Don't show console window (optional, keep for debugging initially)
    # Streamlit requires generic datas:
    '--collect-all=streamlit',
    '--collect-all=langchain',
    '--collect-all=langchain_google_genai',
    '--collect-all=docx',
    # Add recursion depth if needed
    '--recursive-copy-metadata=streamlit',
]

# Run PyInstaller
PyInstaller.__main__.run(args)

print(f"✅ Build Complete! Check {dist_path}")
