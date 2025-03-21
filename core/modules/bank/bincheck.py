import json

def search(dump, bin):
    val = dump.get(bin)
    return val

def bincheck(self, session, bin):
    with open("core/dependencies/bins.json", "r") as f:
        data = json.load(f)
    val = search(data, bin[0:6])
    if val:
        return val
    val = search(data, bin[0:8])
    if val:
        return val
    return None