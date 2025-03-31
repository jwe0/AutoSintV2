def namelog(self, session, name):
    return {
        "first_name" : name.split(" ")[0],
        "last_name" : name.split(" ")[1]
    }