import requests, re

def load_headers():
    headers = {}
    with open("core/assets/headers.txt", "r") as f:
        for line in f.read().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
    return headers 

def flatten(array):
    result = []
    for item in array:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def decode(row):
    table = {
        r"lh3.googleusercontent.com" : "Profile photo",
        r"@gmail.com" : "Email",
        r"^\d{3,21}$" : "ID",
    }
    for item in table:
        value = table[item]

        item = re.compile(item)
        
        if item.search(str(row)):
            return value

def emailpfp(self, session, email):
    report = {}
    emails = email.split(",")
    print("This function will require autocomplete headers in 'core/assets/headers.txt'")
    for email in emails:
        report[email] = {}
        if "@gmail.com" in email:
            api = "https://peoplestack-pa.clients6.google.com/$rpc/peoplestack.PeopleStackAutocompleteService/Autocomplete"
            data = [134,email,[1,2],8]
            r = requests.post(api, json=data, headers=load_headers())
            if r.status_code == 401:
                report[email]["error"] = "Unauthorized"
                continue
            response_data = r.json()
            data = flatten(response_data)
            
            for row in data:
                val = decode(row)
                if val:
                    report[email][val] = row
        else:
            report[email]["error"] = "Not Gmail"
    return report