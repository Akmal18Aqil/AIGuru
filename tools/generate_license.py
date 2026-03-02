"""
License Key Generator untuk SiGURU
Generates secure license keys dengan expiry tracking dan checksum validation

Format: SIGURU-[TIER]-[ORG]-[YYYYMMDD]-[CHECKSUM]
Example: SIGURU-PRO-SDN1-20270217-A7F3

Usage:
    python generate_license.py --tier PRO --org SDN1 --days 365
    python generate_license.py --tier TRIAL --org DEMO --days 30
"""

import argparse
import hashlib
from datetime import datetime, timedelta


class LicenseGenerator:
    """Generate secure license keys for SiGURU"""
    
    VALID_TIERS = ['TRIAL', 'BASIC', 'PRO', 'ENT']
    
    TIER_DEFAULTS = {
        'TRIAL': 30,   # 30 days
        'BASIC': 365,  # 1 year
        'PRO': 365,    # 1 year
        'ENT': 730     # 2 years
    }
    
    def generate_license(self, tier: str, org_id: str, days: int) -> tuple:
        """
        Generate a license key
        
        Args:
            tier: License tier (TRIAL, BASIC, PRO, ENT)
            org_id: Organization identifier (max 4 chars)
            days: Number of days until expiry
            
        Returns:
            (license_key, expiry_date)
        """
        # Validate inputs
        tier = tier.upper()
        if tier not in self.VALID_TIERS:
            raise ValueError(f"Invalid tier. Must be one of: {', '.join(self.VALID_TIERS)}")
        
        org_id = org_id.upper()
        if len(org_id) > 4:
            raise ValueError("Organization ID must be max 4 characters")
        
        if not org_id.isalnum():
            raise ValueError("Organization ID must be alphanumeric only")
        
        if days <= 0:
            raise ValueError("Days must be positive")
        
        # Calculate expiry date
        expiry_date = datetime.now() + timedelta(days=days)
        expiry_str = expiry_date.strftime('%Y%m%d')
        
        # Build base key (without checksum)
        base_key = f"SIGURU-{tier}-{org_id}-{expiry_str}"
        
        # Generate checksum
        checksum = self._generate_checksum(base_key)
        
        # Complete license key
        license_key = f"{base_key}-{checksum}"
        
        return license_key, expiry_date
    
    def _generate_checksum(self, base_key: str) -> str:
        """Generate 4-character checksum using SHA-256"""
        hash_obj = hashlib.sha256(base_key.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()
        # Take first 4 characters and uppercase
        return hash_hex[:4].upper()
    
    def validate_checksum(self, license_key: str) -> bool:
        """Validate license key checksum"""
        try:
            parts = license_key.split('-')
            if len(parts) != 5:
                return False
            
            # Reconstruct base key
            base_key = '-'.join(parts[:4])
            provided_checksum = parts[4]
            
            # Calculate expected checksum
            expected_checksum = self._generate_checksum(base_key)
            
            return provided_checksum == expected_checksum
        
        except Exception:
            return False


def print_license_info(license_key: str, expiry_date: datetime, tier: str, org: str, days: int):
    """Print formatted license information"""
    print("\n" + "="*60)
    print(" ✅  LICENSE KEY GENERATED SUCCESSFULLY")
    print("="*60)
    print()
    print(f"  License Key:  {license_key}")
    print()
    print(f"  Tier:         {tier}")
    print(f"  Organization: {org}")
    print(f"  Duration:     {days} days")
    print(f"  Expires:      {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("="*60)
    print()
    print("📧 Copy license key above and send to customer via email.")
    print("💡 Customer will input this during Setup Wizard.")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Generate SiGURU license keys',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 1-year PRO license for SDN 01
  python generate_license.py --tier PRO --org SDN1 --days 365
  
  # Generate 30-day TRIAL license
  python generate_license.py --tier TRIAL --org DEMO --days 30
  
  # Generate 2-year ENTERPRISE license
  python generate_license.py --tier ENT --org YAS8 --days 730

Valid tiers: TRIAL, BASIC, PRO, ENT
        """
    )
    
    parser.add_argument(
        '--tier',
        required=True,
        choices=['TRIAL', 'BASIC', 'PRO', 'ENT', 'trial', 'basic', 'pro', 'ent'],
        help='License tier'
    )
    
    parser.add_argument(
        '--org',
        required=True,
        help='Organization ID (max 4 alphanumeric characters)'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        required=True,
        help='Number of days until expiry'
    )
    
    parser.add_argument(
        '--validate',
        type=str,
        help='Validate an existing license key (optional)'
    )
    
    args = parser.parse_args()
    
    generator = LicenseGenerator()
    
    # Validation mode
    if args.validate:
        is_valid = generator.validate_checksum(args.validate)
        if is_valid:
            print(f"✅ License key '{args.validate}' has valid checksum")
        else:
            print(f"❌ License key '{args.validate}' has INVALID checksum")
        return
    
    # Generation mode
    try:
        license_key, expiry_date = generator.generate_license(
            tier=args.tier,
            org_id=args.org,
            days=args.days
        )
        
        print_license_info(
            license_key=license_key,
            expiry_date=expiry_date,
            tier=args.tier.upper(),
            org=args.org.upper(),
            days=args.days
        )
        
        # Validate checksum (self-check)
        assert generator.validate_checksum(license_key), "Self-validation failed!"
        
    except ValueError as e:
        print(f"\n❌ Error: {e}\n")
        parser.print_help()
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        exit(1)


if __name__ == '__main__':
    main()
