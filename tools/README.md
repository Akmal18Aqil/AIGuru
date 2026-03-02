# License Generator Tool

Tool untuk generate license keys SiGURU dengan expiry tracking dan checksum validation.

## Format License Key

```
SIGURU-[TIER]-[ORG]-[YYYYMMDD]-[CHECKSUM]
```

- **TIER**: License tier (TRIAL, BASIC, PRO, ENT)
- **ORG**: Organization ID (4 chars max, alphanumeric)
- **YYYYMMDD**: Expiry date
- **CHECKSUM**: SHA-256 checksum (4 chars)

## Usage

### Generate License

```bash
python generate_license.py --tier PRO --org SDN1 --days 365
```

**Output:**
```
============================================================
 ✅  LICENSE KEY GENERATED SUCCESSFULLY
============================================================

  License Key:  SIGURU-PRO-SDN1-20270217-A7F3

  Tier:         PRO
  Organization: SDN1
  Duration:     365 days
  Expires:      2027-02-17 16:53:21

============================================================

📧 Copy license key above and send to customer via email.
💡 Customer will input this during Setup Wizard.
```

### Validate License

```bash
python generate_license.py --validate SIGURU-PRO-SDN1-20270217-A7F3
```

## Examples

```bash
# Trial license (30 days)
python generate_license.py --tier TRIAL --org DEMO --days 30

# Basic license (1 year)
python generate_license.py --tier BASIC --org SDN1 --days 365

# Pro license (1 year)
python generate_license.py --tier PRO --org YAS8 --days 365

# Enterprise (2 years)
python generate_license.py --tier ENT --org CORP --days 730
```

## Tier Recommendations

| Tier | Duration | Typical Use |
|------|----------|-------------|
| TRIAL | 30 days | Demo/evaluation |
| BASIC | 1 year | Small schools (1-3 teachers) |
| PRO | 1 year | Medium schools (10+ teachers) |
| ENT | Custom | Large institutions/districts |

## Customer Workflow

1. **Generate license**: Run generator script
2. **Send via email**: Copy license key to customer
3. **Customer activates**: Input in Setup Wizard
4. **Validation**: Offline checksum + expiry check
5. **Done**: Customer can use app

## Security Features

- ✅ SHA-256 checksum prevents tampering
- ✅ Expiry date embedded in key
- ✅ Offline validation (no internet needed)
- ✅ Organization ID for tracking
- ✅ Tier-based access control (future)
