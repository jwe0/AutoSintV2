import json, threading, json, time
from selenium import webdriver
from bs4 import BeautifulSoup

class Other_Methods:
    def __init__(self, session):
        self.session = session

    def of(self, username):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.page_load_strategy = 'normal'
        driver = webdriver.Chrome(options=options, )
        driver.get("https://onlyfans.com/{}".format(username))

        while "We'll try your destination again in 15 seconds" in driver.page_source:
            pass
        time.sleep(1)
        if "The link you followed may be broken, or the page may have been removed." in driver.page_source:
            print("Non exist")
            return {}
        else:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # Json scrape
            defers = soup.find_all("script", type="application/ld+json")
            if len(defers) == 1:
                datax = {}
                json_data = defers[0].get_text()
                data = json.loads(json_data)
                if "mainEntity" in data:
                    main = data["mainEntity"]
                    interactions = main["interactionStatistic"]
                    datax["interactions"] = {}
                    for interaction in interactions:
                        datax["interactions"][interaction["@type"]] = interaction["userInteractionCount"]

                    name = main["name"]
                    alternatenames = main["alternateName"]
                    identifier = main["identifier"]
                    description = main["description"]
                    image = main["image"]

                    datax["name"] = name
                    datax["alternatenames"] = alternatenames
                    datax["identifier"] = identifier
                    datax["description"] = description
                    datax["image"] = image

            location = soup.find("p", class_="b-user-info__detail m-break-word m-markdown")
            if location:
                location = location.get_text().strip()
            else:
                location = None

            join_offers = soup.find("div", class_="b-offer-join")

            if len(join_offers) > 0:
                datax["join_offers"] = []
                span = join_offers.find_all("span", class_="b-btn-text__small")
                if len(span) > 0:
                    for s in span:
                        s = s.get_text()
                        datax["join_offers"].append(s)

            posts = soup.find("a", class_="b-tabs__nav__link m-reset-wcag-link-focus router-link-active m-with-rectangle-hover m-tb-sm m-current")

            if posts:
                datax["posts"] = posts.get_text().strip()
            else:
                datax["posts"] = None

            media = soup.find("a", class_="b-tabs__nav__link m-reset-wcag-link-focus m-with-rectangle-hover m-tb-sm")

            if media:
                datax["media"] = media.get_text().strip()
            else:
                datax["media"] = None

            post_types = soup.find("ul", class_="b-purchase__list g-text-ellipsis")

            if post_types:
                datax["post_types"] = {}
                li = post_types.find_all("li")
                for l in li:
                    svg = l.find("svg")
                    svg_data = svg.get("data-icon-name").split("icon-")[1]
                    
                    count = l.find("span")
                    count = count.get_text().strip()
                    datax["post_types"][svg_data] = count

            datax["location"] = location

            driver.quit()

            return datax

class Extra:
    def __init__(self, session):
        self.session = session

    def github(self, username):
        def get_emails(username):
            url = "https://github.com/{}/{}".format(username, username)
            emails = {}
            next = False
            r = self.session.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                commits = soup.find_all("span", class_="fgColor-default")
                if len(commits) == 1:
                    commit_count = commits[0].get_text().split(" Commits")[0]
                    commits = self.session.get("https://github.com/{}/{}/commits/main/".format(username, username))
                    if commits.status_code == 200:
                        soup = BeautifulSoup(commits.text, "html.parser")
                        table = soup.find("div", class_="prc-Timeline-Timeline-iQjcc")
                        a = table.find_all("a", href=True)
                        for i in a:
                            if "{}/{}/commit".format(username, username) in i.get("href"):
                                id = i.get("href").split("/")[-1]
                                break
                        next_r = soup.find_all("span", class_="prc-Button-Label-pTQ3x")
                        for r in next_r:
                            if "Next" in r.text:
                                next = True
                        if next:
                            url = "https://github.com/{}/{}/commits/main/?before={}+{}".format(username, username, id, commit_count)
                        else:
                            url = "https://github.com/{}/{}/commits/main/".format(username, username)
                        all_commits = self.session.get(url)
                        if all_commits.status_code == 200:
                            soup = BeautifulSoup(all_commits.text, "html.parser")
                            commits = soup.find_all("a", href=True)
                            for commit_ in commits:
                                if "{}/{}/commit".format(username, username) in commit_.get("href"):
                                    patch_url = "https://github.com/{}.patch".format(commit_.get("href"))
                                    r = self.session.get(patch_url)
                                    if r.status_code == 200 or r.status_code == 304:
                                        for line in r.text.split("\n"):
                                            if "From: " in line and "@" in line:
                                                usable_data = line.split("From: ")[1]
                                                name = usable_data.split("<")[0].strip()
                                                email = usable_data.split("<")[1].split(">")[0].strip()
                                                emails[email] = {"email" : email, "name" : name}
            return emails
                                                    

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
    
    def minecraft(self, username):
        api = "https://api.mojang.com/users/profiles/minecraft/{}".format(username)
        response = self.session.get(api)
        if response.status_code == 200:
            data = response.json()
            return data
        
    def pornhub(self, username):
        result = {}
        def more_info(soup):
            info = {}
            more_info = soup.find("dl", class_="moreInformation")
            if more_info:
                dts = more_info.find_all("dt")
                dds = more_info.find_all("dd")
                for i, dt in enumerate(dts):
                    info[dt.text.strip()] = dds[i].text.strip()
            return info
        def achievments(username):
            result = []
            url = "https://www.pornhub.com/users/{}/myachievements".format(username)
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                achievments = soup.find("ul", class_="achievementsUl")
                lis = achievments.find_all("li")
                for li in lis:
                    span = li.find_all("span")
                    if len(span) > 1:
                        result.append(span[1].get_text().strip())
            return result
        url = "https://www.pornhub.com/users/{}".format(username)
        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            pclass = soup.find("div", class_="profileUserName")
            if pclass:
                a = pclass.find("a", href=True)
                if a:
                    username = a.get("href").split("/")[-1]
                    result["username"] = username
            more_info2 = more_info(soup)
            achs = achievments(username)
            result["more_info"] = more_info2
            result["achievements"] = achs

        return result

class UsernameLookup:
    def __init__(self, username, session):
        self.sites    = json.load(open("core/dependencies/sites.json", "r"))
        self.other_methods = Other_Methods(session)
        self.Other    = {
            "Onlyfans" : {
                "url" : "https://onlyfans.com/{}",
                "func" : self.other_methods.of
            }
        }
        self.result   = {}
        self.report   = {}
        self.prog     = 0
        self.username = username
        self.session  = session
        self.extra    = Extra(self.session)
        
    def check(self, type, value, url):
        try:
            url = url.format(self.username)
            response = self.session.get(url)
            if type == "status-code":
                if response.status_code == value:
                    self.result[url] = response.status_code
            elif type == "site-content":
                if value in response.text:
                    self.result[url] = response.text
        except Exception as e:
            pass
        self.prog += 1

    def post_analysis(self):
        extras = {
            "https://github.com/{}".format(self.username): self.extra.github,
            "https://api.mojang.com/users/profiles/minecraft/{}".format(self.username): self.extra.minecraft,
            "https://www.pornhub.com/users/{}".format(self.username): self.extra.pornhub
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

        for site in self.Other:
            site_info = self.Other[site]
            response = site_info["func"](self.username)

            self.report[site] = {
                "site": site,
                "result": None,
                "extra" : response
            }
        self.post_analysis()

def username_lookup(self, session, username):
    lookup = UsernameLookup(username, session)
    lookup.start()
    return lookup.report