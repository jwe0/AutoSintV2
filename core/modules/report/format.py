def flatten(data):
    message = ""
    for key, value in data.items():
        message += "┃         ┃  ┣    " +  key + " > "
        if type(value) == dict:
            message += flatten(value)
        elif type(value) == list:
            message += str(", ".join(value))
        else:
            message += str(value) + "\n"
    return message.rstrip("\n")
def show(data):
    message = "┏━━ \n"
    for i in data:
        root = "┣  " + i + "\n"
        message +=  root
        info = data[i]
        for sec in info:
            message += "┃\n┣━   {}\n┃      ┗━━┓\n".format(sec)
            sec_info =  info[sec]
            for func in sec_info:
                if type(sec_info[func]) == str:
                    message += "┃         ┣ {} > {}\n".format(func, sec_info[func])
                elif type(sec_info[func]) == dict:

                    message += "┃         ┣  {}\n┃ 	  ┣━━┓ \n".format(func)
                    data2 = flatten(sec_info[func]).rstrip("\n")
                    message += "{}\n┃         ┃  ┗\n".format(data2)
            message += "┃         ┗\n"
    message += "┗━━\n"
    print(message)