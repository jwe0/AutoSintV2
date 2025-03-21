import json

def known_vpn(self, session, ip):
    result = {}
    with open("core/dependencies/vpn_list.json", "r") as f:
        data = json.load(f)

    for provider in data:
        if ip in data[provider]:
            result["provider"] = provider
            result["ip"] = ip
            break
    if not result.get("provider"):
        result["provider"] = "Unknown"
        result["ip"] = ip
    return result