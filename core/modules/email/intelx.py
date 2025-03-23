def intelx(self, session, email):
    api = "https://public.intelx.io/intelligent/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-key": "e0eb96e8-100b-401b-b0d8-a7d1c7c45282",
        "Origin": "https://intelx.io",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://intelx.io/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=0",
        "TE": "trailers"
    }
    form = {
        "term":email,
        "buckets":[
            "leaks.public.wikileaks",
            "leaks.public.general",
            "dumpster",
            "documents.public.scihub"
        ],
        "lookuplevel":0,
        "maxresults":1000,
        "timeout":None,
        "datefrom":"",
        "dateto":"",
        "sort":2,
        "media":0,
        "terminate":[]
        }
    r = session.post(api, headers=headers, json=form)
    if r.status_code == 200:
        data = r.json()

        id = data.get("id")

        api2 = "https://public.intelx.io/intelligent/search/result?id={}&limit=10&statistics=1&previewlines=8".format(id)
        r2 = session.get(api2, headers=headers)
        while r2.status_code != 200:
            r2 = session.get(api2, headers=headers)
        report = {}
        records = r2.json().get("records")
        for record in records:
            name = record.get("name")
            added = record.get("added")
            bucket = record.get("bucket")
            storage_id = record.get("storageid")
            report[name] = {
                "added": added,
                "bucket": bucket,
                "storage_id": storage_id
            }
        return report