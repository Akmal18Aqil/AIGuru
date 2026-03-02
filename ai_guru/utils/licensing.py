import os
import hashlib
from datetime import datetime
import streamlit as st
from supabase import create_client, Client

class LicenseManager:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        self.client: Client = None
        if url and key:
            try:
                self.client = create_client(url, key)
            except Exception as e:
                print(f"Supabase init missing or failed: {e}")

    def verify_license(self, license_key: str) -> bool:
        """
        Verify license key with enhanced pattern-based validation
        
        Supports:
        - DEV-MODE-123 (dev bypass)  
        - SIGURU-[TIER]-[ORG]-[YYYYMMDD]-[CHECKSUM] (production format)
        - Old SIGURU-* pattern (backward compatibility)
        """
        # 1. Dev/Bypass Mode
        if license_key == "DEV-MODE-123":
            return True
        
        # 2. New format validation (SIGURU-TIER-ORG-DATE-CHECKSUM)
        if license_key.startswith("SIGURU-"):
            parts = license_key.split('-')
            
            # Check if new format (5 parts)
            if len(parts) == 5:
                try:
                    tier, org_id, expiry_str, checksum = parts[1:]
                    
                    # Validate checksum
                    base_key = '-'.join(parts[:4])
                    if not self._validate_checksum(base_key, checksum):
                        print(f"❌ Invalid checksum for {license_key}")
                        return False
                    
                    # Check expiry date
                    expiry_date = datetime.strptime(expiry_str, '%Y%m%d')
                    now = datetime.now()
                    
                    if now > expiry_date:
                        days_past = (now - expiry_date).days
                        print(f"❌ License expired {days_past} days ago")
                        return False
                    
                    # License valid!
                    days_remaining = (expiry_date - now).days
                    print(f"✅ License valid ({tier}, {days_remaining} days remaining)")
                    return True
                    
                except Exception as e:
                    print(f"❌ License validation error: {e}")
                    return False
            
            # Old format backward compatibility (SIGURU-anything)
            else:
                print(f"⚠️ Using old license format: {license_key}")
                return True  # Backward compatible
        
        # 3. Invalid format
        return False
    
    def _validate_checksum(self, base_key: str, provided_checksum: str) -> bool:
        """Validate checksum using SHA-256"""
        hash_obj = hashlib.sha256(base_key.encode('utf-8'))
        expected_checksum = hash_obj.hexdigest()[:4].upper()
        return provided_checksum == expected_checksum
    
    def get_license_metadata(self, license_key: str) -> dict:
        """
        Extract metadata from license key
        
        Returns:
            {
                'tier': str,
                'org_id': str,
                'expiry_date': datetime,
                'days_remaining': int,
                'is_valid': bool
            }
        """
        if license_key == "DEV-MODE-123":
            return {
                'tier': 'DEV',
                'org_id': 'DEV',
                'expiry_date': None,
                'days_remaining': 999999,
                'is_valid': True
            }
        
        if not license_key.startswith("SIGURU-"):
            return {'is_valid': False}
        
        parts = license_key.split('-')
        
        if len(parts) != 5:
            # Old format
            return {
                'tier': 'LEGACY',
                'org_id': '????',
                'expiry_date': None,
                'days_remaining': 0,
                'is_valid': True
            }
        
        try:
            tier, org_id, expiry_str, checksum = parts[1:]
            
            expiry_date = datetime.strptime(expiry_str, '%Y%m%d')
            now = datetime.now()
            days_remaining = (expiry_date - now).days
            
            return {
                'tier': tier,
                'org_id': org_id,
                'expiry_date': expiry_date,
                'days_remaining': days_remaining,
                'is_valid': days_remaining >= 0
            }
        
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {'is_valid': False}
