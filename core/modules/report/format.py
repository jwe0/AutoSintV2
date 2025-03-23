def flatten(data, indentation_level=1):
    message = ""
    for key, value in data.items():
        message += f"{'│        ' * indentation_level}├ {key}\n"

        if type(value) == dict:
            message += flatten(value, indentation_level + 1)

        elif type(value) == list:
            ""
        else:
            message += f"{'│        ' * indentation_level}├     {value}\n"
    
    return message
def show(data):
    msg = flatten(data)
    print(msg)