import logging
import os
from pathlib import Path
from ai_guru.utils.path_utils import get_persistent_data_dir


def get_logger(name: str):
    """
    Get a configured logger for production.
    In a desktop/streamlit app, we log to a file and console.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create logs directory in persistent data folder (APPDATA)
        # to avoid PermissionError in Program Files
        log_dir = get_persistent_data_dir() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        
        # File Handler
        fh = logging.FileHandler(log_dir / "siguru.log", encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # Console Handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger
