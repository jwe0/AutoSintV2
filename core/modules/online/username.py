import json, threading
from bs4 import BeautifulSoup

class Extra:
    def __init__(self, session):
        self.session = session

    def github(self, username):
        result = {}
        response = self.session.get("https://github.com/{}".format(username))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            fullname = soup.find("span", class_="p-name vcard-fullname d-block overflow-hidden")
            username = soup.find("span", class_="p-nickname vcard-username d-block")
            vcard_details = soup.find("ul", class_="vcard-details")
            if fullname:
                result["fullname"] = fullname.text.strip()  
            if username:
                result["username"] = username.text.strip()

            for li in vcard_details.find_all("li"):
                prop = li.get("itemprop").strip()
                data = li.find("span", class_="p-label")
                if not data:
                    data = li.find("a")
                if data:
                    data = data.text.strip()
                result[prop] = data
        return result

class UsernameLookup:
    def __init__(self, username, session):
        self.sites    = json.load(open("core/dependencies/sites.json", "r"))
        self.result   = {}
        self.report   = {}
        self.prog     = 0
        self.username = username
        self.session  = session
        self.extra    = Extra(self.session)
        
    def check(self, type, value, url):
        url = url.format(self.username)
        response = self.session.get(url)
        if type == "status-code":
            if response.status_code == value:
                self.result[url] = response.status_code
        elif type == "site-content":
            if value in response.text:
                self.result[url] = response.text
        self.prog += 1

    def post_analysis(self):
        extras = {
            "https://github.com/{}".format(self.username): self.extra.github,
        }
        for site in self.result:
            if site in extras:
                result = extras[site](self.username)
                self.report[site] = {
                    "site": site,
                    "result": self.result[site],
                    "extra": result
                }
            else:
                self.report[site] = {
                    "site": site,
                    "result": self.result[site],
                    "extra": None
                }
    def start(self):
        for site in self.sites:
            site_info = self.sites[site]
            threading.Thread(target=self.check, args=(
                site_info["type"],
                site_info["check-value"],
                site_info["url"].format(self.username)
            )).start()
        while self.prog < len(self.sites):
            pass
        self.post_analysis()

def username_lookup(self, session, username):
    lookup = UsernameLookup(username, session)
    lookup.start()
    return lookup.report