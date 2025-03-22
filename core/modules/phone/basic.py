import json

def phone_basic(self, session, phone):
    num = phone.removeprefix("+")
    data = json.load(open("core/dependencies/carriers.json", "r"))
    for i in range(len(num)):
        car = data.get(num[:i])
        if car:
            return {"carrier": car}
        continue
    return {"carrier": "Unknown"}