def flatten(data, indent_level=0):
    message = ""
    for key, value in data.items():
        if isinstance(value, dict):
            message += "    " * indent_level + "   • {}:\n".format(key)
            message += flatten(value, indent_level + 1)
        elif isinstance(value, list):
            message += "    " * indent_level
            message += f"   • {key}\n"
            for val in value:
                message += "    " * indent_level
                message += f"       • {val}\n"
        else:
            message += "    " * indent_level
            message += f"   • {key}: {value}\n"

    return message


def show(data):
    message = ""
    for sec in data:
        message += f"\n○ {sec}\n"
        sec_info = data[sec]
        for func in sec_info:
            message += f"  ‣ {func}\n"
            func_info = sec_info[func]
            if func_info:
                if isinstance(func_info, dict):
                    message += flatten(func_info)
    print(message)