# Autosint
> *AutoSint provides tools to perform open source intelligence using a mix of active and passive OSINT techniques*

## Instillation
1. Clone the repository `git clone https://github.com/jwe0/autosintv2`
2. Change your current directory with `cd autosintv2`
3. Create a virtual environment (only required on Linux) `python3 -m venv env`
4. If you create a virtual environment run `source env/bin/activate`
5. Run `pip install -r requirements.txt` to install the requirements
6. Execute `python3 main.py`
7. Fill in the prompted information
8. Wait


## Example data


```json 
{
    "Identity": {
        "Namelog": {
            "first_name": "John",
            "last_name": "Doe"
        }
    },
    "Bank": {
        "Bincheck": {
            "bin": "123456",
            "brand": "VISA",
            "type": "CREDIT",
            "category": "CLASSIC",
            "issuer": "Example Bank",
            "alpha2": "XX",
            "alpha3": "XXX",
            "country": "Exampleland",
            "latitude": "0.0000",
            "longitude": "0.0000",
            "bank_phone": "000-000-0000",
            "bank_url": "https://www.examplebank.com"
        }
    },
    "Email": {
        "Intelx": {
            "example_paste.txt": {
                "added": "2025-01-01T00:00:00.000000Z",
                "bucket": "public-dump",
                "storage_id": "example-storage-id"
            }
        },
        "Email PFP": {
            "pfp": "https://example.com/profile.jpg",
            "id": "example-google-id"
        },
        "Protonmail": {
            "created_at": "2025-01-01",
            "method": "RSA-2048",
            "public_key": "-----BEGIN PGP PUBLIC KEY BLOCK-----\nExamplePublicKeyData\n-----END PGP PUBLIC KEY BLOCK-----"
        }
    },
    "IP": {
        "Lookup": {
            "ipVersion": 4,
            "ipAddress": "0.0.0.0",
            "latitude": 0.0000,
            "longitude": 0.0000,
            "countryName": "Nowhere",
            "countryCode": "XX",
            "timeZone": "+00:00",
            "zipCode": "00000",
            "cityName": "Null City",
            "regionName": "Null Region",
            "isProxy": false,
            "continent": "Unknown",
            "continentCode": "XX",
            "currency": {
                "code": "XXX",
                "name": "Example Currency"
            },
            "language": "Example Language",
            "timeZones": [
                "Etc/UTC"
            ],
            "tlds": [
                ".xx"
            ]
        },
        "Banner": "Example Server Banner",
        "Known VPN": {
            "provider": "ExampleVPN",
            "ip": "0.0.0.0"
        }
    },
    "Online": {
        "Username": {
            "https://github.com/example": {
                "site": "https://github.com/example",
                "result": 200,
                "extra": {
                    "fullname": "John Doe",
                    "username": "example_user",
                    "emails": [
                        "example@example.com"
                    ]
                }
            },
            "https://api.mojang.com/users/profiles/minecraft/example": {
                "site": "https://api.mojang.com/users/profiles/minecraft/example",
                "result": 200,
                "extra": {
                    "id": "example_mojang_id",
                    "name": "ExampleMC"
                }
            },
            "https://www.snapchat.com/add/example": {
                "site": "https://www.snapchat.com/add/example",
                "result": 200,
                "extra": null
            }
    }
    "Phone": {
        "Basic": {
            "carrier": {
                "en": "Example Carrier"
            }
        },
        "Codeinfo": {
            "FIFA": "XXX",
            "Dial": "000",
            "ISO3166-1-Alpha-3": "XXX",
            "ISO3166-1-Alpha-2": "XX",
            "ITU": "X",
            "ISO4217-currency_name": "Example Currency",
            "ISO4217-currency_alphabetic_code": "XXX",
            "ISO4217-currency_minor_unit": "0",
            "official_name_en": "Exampleland",
            "Region Name": "Example Region",
            "Sub-region Name": "Example Sub-region",
            "Capital": "Example City",
            "Continent": "Example Continent",
            "TLD": ".xx",
            "Languages": "ex-EX",
            "Geoname ID": "0000000"
        }
    }
}
```
