"""
API Key Manager untuk SiGURU Desktop App
Mengelola API key dengan multi-tier support:
- Organization key (dari .env)
- User key (dari database terenkripsi)
- Trial key (temporary)
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import google.generativeai as genai


class APIKeyManager:
    """Manages API keys for the application with multi-tier support"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent
        self.config_path = self.root_dir / "config.json"
        self.env_path = self.root_dir / ".env"
        
    def is_setup_completed(self) -> bool:
        """Check if initial setup has been completed"""
        if not self.config_path.exists():
            return False
        
        try:
            config = self._load_config()
            return config.get('setup_completed', False)
        except:
            return False
    
    def get_llm_provider_config(self) -> Dict[str, Any]:
        """Get the current LLM provider configuration from .env"""
        config = {
            'provider': 'Google Gemini',
            'api_key': '',
            'custom_base_url': '',
            'custom_model_name': ''
        }
        
        if not self.env_path.exists():
            return config
            
        try:
            with open(self.env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GOOGLE_API_KEY=') and not config['api_key']:
                        config['api_key'] = line.split('=', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('API_KEY='):
                        config['api_key'] = line.split('=', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('LLM_PROVIDER='):
                        config['provider'] = line.split('=', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('CUSTOM_BASE_URL='):
                        config['custom_base_url'] = line.split('=', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('CUSTOM_MODEL_NAME='):
                        config['custom_model_name'] = line.split('=', 1)[1].strip().strip('"').strip("'")
        except Exception as e:
            print(f"Error reading .env: {e}")
            
        return config

    def get_api_key(self) -> Optional[str]:
        """
        Get API key with priority order:
        1. Organization key dari .env (highest priority)
        2. User key dari database (future feature)
        3. Trial key (future feature)
        4. None (trigger setup)
        """
        # Check LLM provider config
        config = self.get_llm_provider_config()
        if config['api_key'] and config['api_key'] != 'your_api_key_here':
            return config['api_key']
        
        # Priority 2: Check config.json untuk fallback
        try:
            config_json = self._load_config()
            if config_json.get('api_key_source') == 'env':
                # Already checked .env above, so this is a problem
                return None
        except:
            pass
        
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current API key status for display"""
        api_key = self.get_api_key()
        provider_config = self.get_llm_provider_config()
        
        if not api_key:
            return {
                'active': False,
                'type': 'Tidak ada',
                'source': None,
                'provider': 'None'
            }
        
        # Test if API key is valid
        is_valid = self._test_api_key(
            api_key, 
            provider_config['provider'], 
            provider_config['custom_base_url'], 
            provider_config['custom_model_name']
        )
        
        if is_valid:
            config = self._load_config()
            deployment_type = config.get('deployment_type', 'organization')
            org_name = config.get('organization_name', 'Organisasi')
            
            return {
                'active': True,
                'type': f'Lisensi {org_name}' if deployment_type == 'organization' else 'Lisensi Individual',
                'source': 'env',
                'provider': provider_config['provider']
            }
        else:
            return {
                'active': False,
                'type': 'API Key tidak valid',
                'source': 'env',
                'provider': provider_config['provider']
            }
    
    def save_organization_setup(self, api_key: str, organization_name: str, license_key: str = None, 
                                provider: str = "Google Gemini", custom_base_url: str = "", 
                                custom_model_name: str = "") -> bool:
        """
        Save organization setup with API key, org name, and license key
        """
        # Test API key first
        if not self._test_api_key(api_key, provider, custom_base_url, custom_model_name):
            return False
        
        # Save to .env
        if not self._save_to_env(api_key, organization_name, provider, custom_base_url, custom_model_name):
            return False
        
        # Save config.json
        config = {
            'deployment_type': 'organization',
            'organization_name': organization_name,
            'setup_completed': True,
            'setup_date': datetime.now().isoformat(),
            'api_key_source': 'env',
            'license_key': license_key if license_key else None,
            'license_verified': True if license_key else False,
            'llm_provider': provider
        }
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_license_status(self) -> Dict[str, Any]:
        """
        Get license status from config and extract metadata from license key
        
        Returns:
            {
                'has_license': bool,
                'license_key': str (masked),
                'is_valid': bool,
                'tier': str,
                'expiry_date': datetime,
                'days_remaining': int
            }
        """
        if not self.config_path.exists():
            return {'has_license': False, 'is_valid': False, 'license_key': ''}
        
        try:
            config = self._load_config()
            license_key = config.get('license_key')
            
            if not license_key:
                return {'has_license': False, 'is_valid': False, 'license_key': ''}
            
            # Extract metadata from license key
            from ai_guru.utils.licensing import LicenseManager
            manager = LicenseManager()
            
            # Get metadata
            metadata = manager.get_license_metadata(license_key)
            
            if not metadata.get('is_valid', False):
                return {
                    'has_license': True,
                    'is_valid': False,
                    'license_key': self._mask_license(license_key)
                }
            
            # Mask license key for display
            masked_key = self._mask_license(license_key)
            
            return {
                'has_license': True,
                'license_key': masked_key,
                'is_valid': True,
                'tier': metadata.get('tier', 'UNKNOWN'),
                'org_id': metadata.get('org_id', ''),
                'expiry_date': metadata.get('expiry_date'),
                'days_remaining': metadata.get('days_remaining', 0),
                'full_key': license_key  # For internal use only
            }
        
        except Exception as e:
            print(f"Error getting license status: {e}")
            return {'has_license': False, 'is_valid': False, 'license_key': ''}
    
    def _mask_license(self, license_key: str) -> str:
        """Mask license key for display"""
        if license_key == "DEV-MODE-123":
            return "DEV-MODE-123"
        
        parts = license_key.split('-')
        if len(parts) >= 3:
            # Show tier and org, hide rest
            return f"****-{parts[1]}-{parts[2]}-****"
        else:
            return "****-****"
    
    def _load_from_env(self) -> Optional[str]:
        """Load API key from .env file"""
        config = self.get_llm_provider_config()
        return config.get('api_key') or None
    
    def _save_to_env(self, api_key: str, organization_name: str = "", provider: str = "Google Gemini", 
                     custom_base_url: str = "", custom_model_name: str = "") -> bool:
        """Save API key and provider config to .env file"""
        try:
            existing_lines = []
            if self.env_path.exists():
                with open(self.env_path, 'r', encoding='utf-8') as f:
                    existing_lines = f.readlines()
            
            keys_to_update = {
                'GOOGLE_API_KEY': api_key if provider == 'Google Gemini' else None,
                'API_KEY': api_key,
                'ORGANIZATION_NAME': organization_name,
                'LLM_PROVIDER': provider,
                'CUSTOM_BASE_URL': custom_base_url,
                'CUSTOM_MODEL_NAME': custom_model_name
            }
            
            new_lines = []
            found_keys = set()
            
            for line in existing_lines:
                updated = False
                for k, v in keys_to_update.items():
                    if line.strip().startswith(f'{k}='):
                        if v is not None:
                            new_lines.append(f'{k}={v}\n')
                        found_keys.add(k)
                        updated = True
                        break
                if not updated:
                    new_lines.append(line)
            
            # Add missing keys
            for k, v in keys_to_update.items():
                if k not in found_keys and v is not None:
                    new_lines.append(f'{k}={v}\n')
            
            with open(self.env_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            return True
        except Exception as e:
            print(f"Error saving to .env: {e}")
            return False
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json"""
        if not self.config_path.exists():
            return {}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _test_api_key(self, api_key: str, provider: str = "Google Gemini", 
                      custom_base_url: str = "", custom_model_name: str = "") -> bool:
        """
        Test if API key is valid by making a simple API call
        """
        try:
            if provider == 'Google Gemini':
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content("Test")
                return True
            else:
                # Use the new LLM factory for other providers
                import sys
                from pathlib import Path
                
                # Setup temp env so LLMFactory can pick it up
                import os
                old_provider = os.environ.get('LLM_PROVIDER')
                old_key = os.environ.get('API_KEY')
                old_url = os.environ.get('CUSTOM_BASE_URL')
                old_model = os.environ.get('CUSTOM_MODEL_NAME')
                
                # Mock environment variables for LLMFactory
                # But since LLMFactory reads from get_llm_provider_config, we need a slight workaround.
                # Actually, we can just instantiate directly here to test!
                if provider == 'Groq':
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(api_key=api_key, model_name="llama3-8b-8192", temperature=0)
                    llm.invoke("Test")
                elif provider == 'Anthropic':
                    from langchain_anthropic import ChatAnthropic
                    llm = ChatAnthropic(api_key=api_key, model_name="claude-3-haiku-20240307", temperature=0)
                    llm.invoke("Test")
                elif provider == 'OpenRouter':
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key, model="google/gemini-2.5-flash", temperature=0)
                    llm.invoke("Test")
                elif provider == 'Custom Provider':
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(base_url=custom_base_url, api_key=api_key, model=custom_model_name, temperature=0)
                    llm.invoke("Test")
                
                return True
        except Exception as e:
            print(f"API key validation failed: {e}")
            return False
    
    def reset_setup(self) -> bool:
        """Reset setup configuration (for troubleshooting)"""
        try:
            if self.config_path.exists():
                self.config_path.unlink()
            return True
        except:
            return False
