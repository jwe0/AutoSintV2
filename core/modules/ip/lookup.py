def lookup(self, session, ip):
    api = "https://freeipapi.com/api/json/{}".format(ip)

    response = session.get(api)
    data = response.json()

    return data