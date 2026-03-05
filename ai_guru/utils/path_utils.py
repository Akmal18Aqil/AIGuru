import os
import sys
from pathlib import Path

def get_persistent_data_dir():
    """
    Returns a writable directory for persistent data (.env, config.json, .salt).
    When frozen, use %APPDATA%/SiGURU_AI.
    When developing, use the project root.
    """
    if getattr(sys, 'frozen', False):
        appdata = Path(os.getenv('APPDATA', Path.home()))
        data_dir = appdata / "SiGURU_AI"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    else:
        return Path(__file__).parent.parent.parent

def get_base_dir():
    """Returns the executable directory (for read-only access to bundled files)."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent.parent

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    PyInstaller unpacks data to sys._MEIPASS.
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent.parent
    
    return base_path / relative_path
