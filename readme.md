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
        },
        "Address" : {
            "postal_code": "12345",
            "city": "Example City",
            "state": "Example State",
            "country": "Example Country",
            "address": "123 Example Street"
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
            "isProxy": False,
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
        "Banner": {
            "banner": "Example Banner"
        },
        "Known VPN": {
            "provider": "ExampleVPN",
            "ip": "0.0.0.0"
        },
        "Portscan" : {
            "143": {
                "service": "IMAP",
                "protocol": "TCP, UDP",
                "banner": "* OK IMAP ready for requests."
            },
            "37": {
                "service": "Unknown",
                "protocol": "Unknown",
                "banner": "Unknown"
            },
            "21": {
                "service": "FTP",
                "protocol": "TCP, UDP, SCTP",
                "banner": "220-Welcome to FTP server!\r\n220 If you don't have an account, log in as 'anonymous' or 'ftp'."
            },
            "13": {
                "service": "Unknown",
                "protocol": "Unknown",
                "banner": "Mon, 31 Mar 2025 14:13:37 GMT"
            },
            "22": {
                "service": "SSH/SCP/SFTP",
                "protocol": "TCP, UDP, SCTP",
                "banner": "SSH-2.0-GenericSSH_5.0"
            },
            "80": {
                "service": "HTTP",
                "protocol": "TCP, UDP, SCTP",
                "banner": "Unknown"
            },
            "990": {
                "service": "FTPS",
                "protocol": "TCP",
                "banner": "Unknown"
            }
        }
    },
    "Online": {
        "Username": {
            "https://github.com/example_user": {
                "site": "https://github.com/example_user",
                "result": 200,
                "extra": {
                    "fullname": "",
                    "username": "example_user",
                    "emails": []
                }
            },
            "https://www.snapchat.com/add/example_user": {
                "site": "https://www.snapchat.com/add/example_user",
                "result": 200,
                "extra": None
            },
            "https://api.mojang.com/users/profiles/minecraft/example_user": {
                "site": "https://api.mojang.com/users/profiles/minecraft/example_user",
                "result": 200,
                "extra": {
                    "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "name": "ExampleUser"
                }
            },
            "https://www.pornhub.com/users/anonymous123": {
                "site": "https://www.pornhub.com/users/anonymous123",
                "result": 200,
                "extra": {
                    "username": "anonymous123",
                    "more_info": {
                        "Gender": "Male",
                        "Last Login": "1 month ago",
                        "Interested In": "Categories",
                        "Profile Views": "26",
                        "Videos Watched": "1"
                    },
                    "achievements": [
                        "Achievement 1",
                        "Achievement 2"
                    ]
                }
            }
        }
    },
    "Phone": {
        "Basic": {
            "carrier": "Example Carrier"
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
