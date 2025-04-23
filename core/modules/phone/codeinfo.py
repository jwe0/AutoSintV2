import json

def codeinfo(self, session, number):
    report = {}
    numbers = number.split(",")
    for number in numbers:
        number = number.strip().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        def search(dump, code):
            return dump.get(code)
        with open("core/dependencies/callingcodes.json", "r") as f:
            codes = json.load(f)
        number = number.removeprefix("+")
        info   = search(codes, number[:3])
        if not info:
            info = search(codes, number[:2])
        if not info:
            info = search(codes, number[:1])
        if not info:
            info = {"country": "Unknown"}
        report[number] = info
    return report