import socket, threading

class Domainsearch:
    def __init__(self, username):
        self.username = username
        self.report   = {}
        self.prog     = 0
        self.tlds     = self.load_tlds()

    def load_tlds(self):
        with open("core/dependencies/tlds.txt", "r") as f:
            return f.read().splitlines()

    def check(self, tld):
        try:
            info = socket.gethostbyname_ex(self.username + "." + tld)
            domain = info[0]
            aliases = info[1]
            addresses = info[2]

            self.report[domain] = {
                "domain": domain,
                "aliases": aliases,
                "addresses": addresses
            }
        except:
            ""
        finally:
            self.prog += 1

    def start(self):
        for tld in self.tlds:
            threading.Thread(target=self.check, args=(tld,)).start()
        while self.prog < len(self.tlds):
            pass

def domainsearch(self, session, domain):
    search = Domainsearch(domain)
    search.start()
    return search.report