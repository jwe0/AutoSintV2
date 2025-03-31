def addresslog(self, session, name):
    address = name.split(" ")

    house_number = address[0] if len(address) > 1 else "N/A"
    street       = address[1] if len(address) > 2 else "N/A"
    city         = address[2] if len(address) > 3 else "N/A"
    state        = address[3] if len(address) > 4 else "N/A"
    country      = address[4] if len(address) > 5 else "N/A"
    postal_code  = address[5] if len(address) > 6 else "N/A"
    return {
        "house_number": house_number,
        "street": street,
        "city": city,
        "state": state,
        "country": country,
        "postal_code": postal_code
    }