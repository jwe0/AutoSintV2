import json

def phone_basic(self, session, phone):
    report = {}
    numbers = phone.split(",")
    for number in numbers:
        num = phone.removeprefix("+")
        data = json.load(open("core/dependencies/carriers.json", "r"))
        for i in range(len(num)):
            car = data.get(num[:i])
            if car:
                report[number] = car
    return report