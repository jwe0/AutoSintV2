def show(data):
    message = ""
    def identity(data):
        result = ""
        for info in data:
            data_info = data[info]
            result += f"\n├     {info}\n│         └───┐"
            for sec in data_info:
                result += f"\n│             ├ {sec}: {data_info[sec]}"
            result += "\n│             └"
        return result
    def bank(data):
        result = ""
        for info in data:
            data_info = data[info]
            result += f"\n├     {info}\n│         └───┐"
            for sec in data_info:
                result += f"\n│             ├ {sec}: {data_info[sec]}"
            result += "\n│             └"
        return result
    def email(data):
        result = ""
        for info in data:
        
            data_info = data[info]
            result += f"\n├     {info}\n│         └───┐"
            if info != "Intelx":
                for sec in data_info:
                    result += f"\n│             ├ {sec}: {data_info[sec]}"
            else:
                for bin in data[info]:
                    bin_info = data[info][bin]
                    
                    added = bin_info.get("added")
                    bucket = bin_info.get("bucket")
                    storage_id = bin_info.get("storage_id")
                    result += f"\n│             ├ {bin}:"
                    result += f"\n│             │     └───┐"
                    result += f"\n│             │         ├ added: {added}"
                    result += f"\n│             │         ├ bucket: {bucket}"
                    result += f"\n│             │         ├ storage_id: {storage_id}"
                    result += f"\n│             │         └"
            result += "\n│             └"

        return result
    def ip(data):
        result = ""
        for info in data:
            data_info = data[info]
            result += f"\n├     {info}\n│         └───┐"
            for sec in data_info:
                result += f"\n│             ├ {sec}: {data_info[sec]}"
            result += "\n│             └"
        return result
    def online(data):
        result = ""
        for info in data:
            if info == "Username":
                data_info = data[info]
                for site in data_info:
                    site_info = data_info[site]
                    result += f"\n├     {site}\n│         └───┐"

                    site = site_info.get("site")
                    resultx = site_info.get("result")
                    extra = site_info.get("extra")
                    result += f"\n│             ├ site: {site}"
                    result += f"\n│             ├ result: {resultx}"
                    if extra == None:
                        ""
                    else:
                        result += f"\n│             ├ extra: "
                        for sec in extra:
                            result += f"\n│             │     ├───┐"
                            result += f"\n│             │     │   ├ {sec}: {extra[sec]}"
                            result += f"\n│             │     │   └"
                    result += "\n│             └"
        return result
    def phone(data):
        result = ""
        for info in data:
            data_info = data[info]
            result += f"\n├     {info}\n│         └───┐"
            for sec in data_info:
                result += f"\n│             ├ {sec}: {data_info[sec]}"
            result += "\n│             └"
        return result
    secs = {
        "Identity" : identity,
        "Bank" : bank,
        "Email" : email,
        "IP" : ip,
        "Online" : online,
        "Phone" : phone
    }
    for sec in secs:
        info = data[sec]
        message += f"\n├ {sec}\n│     └───┐"
        message += secs[sec](info)

    print(message)