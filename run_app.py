import sys
import streamlit.web.cli as stcli
import os
from pathlib import Path

def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

if __name__ == "__main__":
    # Get the directory of this script
    current_dir = Path(__file__).parent
    app_path = current_dir / "ui" / "app.py"
    
    if not app_path.exists():
        print(f"Error: {app_path} not found.")
        sys.exit(1)
        
    # Streamlit requires the path to the app.py
    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
