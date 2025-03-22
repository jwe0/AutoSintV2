import json, threading
from bs4 import BeautifulSoup

class Extra:
    def __init__(self, session):
        self.session = session

    def github(self, username):
        def get_emails(username):
            url = "https://github.com/{}/{}".format(username, username)
            emails = set()
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                commits = soup.find("a", class_="prc-Button-ButtonBase-c50BI d-none d-lg-flex LinkButton-module__code-view-link-button--xvCGA flex-items-center fgColor-default")
                if commits:
                    amount = commits.get_text()
                    if amount:
                        number = amount.split(" Commits")[0]
                        commits = self.session.get("https://github.com/{}/{}/commits/main/".format(username, username))
                        if commits.status_code == 200:
                            soup = BeautifulSoup(commits.text, "html.parser")
                            a = soup.find_all("a", class_="color-fg-default", href=True)
                            for i in a:
                                if "{}/{}/commit".format(username, username) in i.get("href"):
                                    id = i.get("href").split("/")[-1]
                                    break
                            next = False
                            next_r = soup.find_all("span", class_="prc-Button-Label-pTQ3x")
                            for r in next_r:
                                if "Next" in r.text:
                                    next = True
                            if next:
                                url = "https://github.com/{}/{}/commits/main/?before={}+{}".format(username, username, id, number)
                            else:
                                url = "https://github.com/{}/{}/commits/main/".format(username, username)
                            all_commits = self.session.get(url)
                            if all_commits.status_code == 200:
                                soup = BeautifulSoup(all_commits.text, "html.parser")
                                commits = soup.find_all("a", class_="color-fg-default", href=True)
                                for commit in commits:
                                    if "{}/{}/commit".format(username, username) in commit.get("href"):
                                        patch = "https://github.com/{}.patch".format(commit.get("href"))
                                        patch_data = self.session.get(patch)
                                        if patch_data.status_code == 200 or 304:
                                            for line in patch_data.text.split("\n"):
                                                if "From" in line and "@" in line:
                                                    email = line.split("<")[1].split(">")[0]
                                                    if email not in emails:
                                                        emails.add(email)
            return list(emails)
                                                    

        result = {}
        response = self.session.get("https://github.com/{}".format(username))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            fullname = soup.find("span", class_="p-name vcard-fullname d-block overflow-hidden")
            username_ = soup.find("span", class_="p-nickname vcard-username d-block")
            vcard_details = soup.find("ul", class_="vcard-details")
            if fullname:
                result["fullname"] = fullname.text.strip()  
            if username_:
                result["username"] = username_.text.strip()

            for li in vcard_details.find_all("li"):
                prop = li.get("itemprop").strip()
                data = li.find("span", class_="p-label")
                if not data:
                    data = li.find("a")
                if data:
                    data = data.text.strip()
                result[prop] = data
            emails = get_emails(username)
            result["emails"] = emails
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