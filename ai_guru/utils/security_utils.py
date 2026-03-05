import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from ai_guru.utils.path_utils import get_persistent_data_dir

class SecretManager:
    """
    Handles encryption and decryption of sensitive strings (API Keys)
    Uses a machine-specific or salt-based key derivation for security.
    """
    
    def __init__(self):
        # We need a stable salt. In a real desktop app, we might use machine ID.
        # Here we'll use a hidden salt file or a default if not present.
        self.salt_file = get_persistent_data_dir() / ".salt"
        if not self.salt_file.exists():
            with open(self.salt_file, "wb") as f:
                f.write(os.urandom(16))
        
        with open(self.salt_file, "rb") as f:
            self.salt = f.read()
            
        # "Master Key" derived from a fixed string + salt
        # In production, this could be more complex, but for local .env protection,
        # it prevents casual reading of the .env file.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(b"siguru-internal-secure-key-2024"))
        self.fernet = Fernet(key)

    def encrypt(self, text: str) -> str:
        """Encrypt string and return as base64 string"""
        if not text:
            return ""
        try:
            return self.fernet.encrypt(text.encode()).decode()
        except Exception:
            return text

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt string. Returns original if not encrypted or error."""
        if not encrypted_text or not encrypted_text.startswith("gAAAA"): # Fernet token start
            return encrypted_text
        try:
            return self.fernet.decrypt(encrypted_text.encode()).decode()
        except Exception:
            return encrypted_text

# Singleton instance
secrets = SecretManager()
