import datetime, re

def pub_key(session, email):
    api = "https://api.protonmail.ch/pks/lookup?op=get&search={}".format(email)
    r = session.get(api)
    return r.text.replace("\n", "")

def protonmail(self, session, email):
    api = "https://api.protonmail.ch/pks/lookup?op=index&search={}".format(email)
    r = session.get(api)
    if "info:1:1" in r.text:
        patterns = [("2048:(.*)::", "RSA 2048"), ("4096:(.*)::", "RSA 4096"), ("22::(.*)::", "X25519")]
        for pattern, method in patterns:
            try:
                timestamp = int(re.search(pattern, r.text).group(1))
                dtO = datetime.datetime.fromtimestamp(timestamp)
                pub = pub_key(session, email)
                return {"created_at": dtO.strftime("%Y-%m-%d %H:%M:%S"), "method" : method, "public_key": pub}
            except:
                pass
        return {"created_at": "Unknown", "method" : "Unknown"}
    return {"created_at": "Unknown", "method" : "Unknown"}