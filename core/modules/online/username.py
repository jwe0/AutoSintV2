import json, threading, json, time, requests
from selenium import webdriver
from bs4 import BeautifulSoup

class Other_Methods:
    def __init__(self, session, external_self):
        self.session = session
        self.external_self = external_self

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
            return {"error": "Non exist"}
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
                    if image:
                        self.external_self.report["Images"]["Misc"].append(image)

                    datax["name"] = name
                    datax["alternatenames"] = alternatenames
                    datax["identifier"] = identifier
                    datax["description"] = description

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
    def fansly(self, username):
        self.external_self.report["Images"]["Fansly"] = []
        def provider_decode(id):
            table = {
                1: "Twitter",
                4: "Instagram"
            }
            return table.get(int(id))
        def get_images(id):
            api = "https://apiv3.fansly.com/api/v1/timelinenew/{}?ngsw-bypass=false".format(id)
            
            r = requests.get(api)
            if r.status_code != 200:
                return
            data = r.json()
            
            main = data.get("response").get("accountMedia")
            for media in main:
                sub = media.get("preview").get("variants")
                for s in sub:
                    locations = s.get("locations")
                    if not locations:
                        continue
                    for l in locations:
                        url = l.get("location")
                        self.external_self.report["Images"]["Fansly"].append(url)
        result = {}
        api = "https://apiv3.fansly.com/api/v1/account?usernames={}&ngsw-bypass=true".format(username)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36"
        }
        r = requests.get(api, headers=headers)
        if r.status_code == 200:
            data = r.json()

            if data.get("response"):
                if len(data.get("response")) > 0:
                    response = data.get("response")[0]

                    id = response.get("id")
                    username = response.get("username")
                    display_name = response.get("displayName")
                    followers = response.get("followCount")
                    location = response.get("location")
                    about = response.get("about")

                    result["id"] = id
                    result["username"] = username
                    result["display_name"] = display_name
                    result["followers"] = followers
                    result["location"] = location
                    result["about"] = about

                    socials = response.get("profileSocials")
                    if socials:
                        result["socials"] = {}
                        for social in socials:
                            handle = social.get("handle")
                            provider = provider_decode(social.get("providerId"))
                            result["socials"][provider] = handle

                    walls = response.get("walls")
                    if walls:
                        result["walls"] = {}
                        for wall in walls:
                            wall_id = wall.get("id")
                            wall_name = wall.get("name")
                            result["walls"][wall_id] = wall_name

                    avatar = response.get("avatar")
                    if avatar:
                        avatar = avatar.get("variants")
                    if avatar:
                        result["avatar"] = []
                        for a in avatar:
                            location = a.get("locations")[0].get("location")
                            self.external_self.report["Images"]["Fansly"].append(location)

                    banner = response.get("banner")
                    if banner:
                        banner = banner.get("variants")
                    if banner:
                        result["banner"] = []
                        for b in banner:
                            location = b.get("locations")[0].get("location")
                            self.external_self.report["Images"]["Fansly"].append(location)


                    get_images(id)
                            
                    return result
                
                else:
                    return {"error": "No response"}
            else:
                return {"error": "No response"}
        return result
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
    
    def pornhub2(self, username):
        result = {}
        def more_info(username):
            info_ = {}
            url = "https://www.pornhub.com/model/{}/about".format(username)
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                context_columns = soup.find("div", class_="content-columns js-highestChild columns-2")
                if context_columns:
                    info_pieces = context_columns.find_all("div", class_="infoPiece")
                    for info in info_pieces:
                        spans = info.find_all("span")

                        key = spans[0].text.strip()
                        value = spans[1].text.strip()

                        info_[key] = value
                clearfix = soup.find("ul", class_="clearfix socialList")
                if clearfix:
                    result["socials"] = {}
                    socials = clearfix.find_all("li")
    
                    for social in socials:
                        a = social.find("a", href=True)
                        span = social.find("span")
                        if span:
                            title = span.get_text().strip()

                            result["socials"][title] = a.get("href").strip()

            return info_
        def achievments(username):
            result = []
            url = "https://www.pornhub.com/model/{}/achievements".format(username)
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
        url = "https://www.pornhub.com/model/{}".format(username)
        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            name = soup.find("div", class_="name")
            if name:
                name = name.get_text().strip()
                result["name"] = name

            result["stats"] = {}

            info_boxes = soup.find("div", class_="infoBoxes")

            info_divs = info_boxes.find_all("div")

            for info in info_divs:
                value = info.find("span", class_="big")
                title = info.find("div", class_="title")

                if title:
                    title = title.get_text().strip()

                    result["stats"][title] = value.get_text().strip()
                    
            more_info2 = more_info(username)
            achs = achievments(username)
            result["more_info"] = more_info2
            result["achievements"] = achs

        return result
    
    def allmylinks(self, username):
        result = {}
        url = "https://allmylinks.com/{}".format(username)
        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            box = soup.find("div", class_="left-sidebar-box")
            if box:
                username = box.find("span", class_="profile-username profile-page")
                if username:
                    username = username.get_text().strip()
                    result["username"] = username
            links = soup.find_all("a", class_="list-item link-type-web link", href=True)
            if links:
                result["links"] = {}
                for link in links:
                    data_x_url = link.get("data-x-url")
                    if data_x_url in result["links"]:
                        continue
                    title = link.find("span", class_="link-title")
                    if title:
                        title = title.get_text().strip()
                    else:
                        title = link.get_text().strip()
                    result["links"][title] = data_x_url
        return result
class UsernameLookup:
    def __init__(self, username, session, external_self):
        self.external_self = external_self
        self.sites    = json.load(open("core/dependencies/sites.json", "r"))
        self.other_methods = Other_Methods(session, external_self)
        self.Other    = {
            "Onlyfans" : {
                "url" : "https://onlyfans.com/{}",
                "func" : self.other_methods.of
            },
            "Fansly" : {
                "url" : "https://fansly.com/{}/posts",
                "func" : self.other_methods.fansly
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
                if value not in response.text:
                    self.result[url] = "{}".format(value)
        except Exception as e:
            pass
        self.prog += 1
    def post_analysis(self):
        extras = {
            "https://github.com/{}".format(self.username): self.extra.github,
            "https://api.mojang.com/users/profiles/minecraft/{}".format(self.username): self.extra.minecraft,
            "https://www.pornhub.com/users/{}".format(self.username): self.extra.pornhub,
            "https://www.pornhub.com/model/{}".format(self.username): self.extra.pornhub2,
            "https://allmylinks.com/{}".format(self.username): self.extra.allmylinks
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
                    "result": self.result[site]
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
    lookup = UsernameLookup(username, session, self)
    lookup.start()
    return lookup.report