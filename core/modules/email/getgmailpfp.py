import requests


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

def emailpfp(self, session, email):
    print("This function will require autocomplete headers in 'core/assets/headers.txt'")
    if "@gmail.com" in email:
        api = "https://peoplestack-pa.clients6.google.com/$rpc/peoplestack.PeopleStackAutocompleteService/Autocomplete"
        data = [134,email,[1,2],8]
        r = requests.post(api, json=data, headers=load_headers())
        if r.status_code == 401:
            return "Unauthorized"
        response_data = r.json()
        data = flatten(response_data)
        pfp = data[0]
        id  = data[13]

        return {"pfp": pfp, "id": id}