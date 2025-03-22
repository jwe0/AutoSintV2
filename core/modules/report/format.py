def flatten(data, prefix = None):
    message = ""
    for key, value in data.items():
        key = key
        if prefix:
            prefix = prefix
        if type(value) == dict:
            if prefix:
                message += flatten(value, f"{prefix} | {key}")
            else:
                message += flatten(value,  key)
        elif type(value) == list:
            if prefix:
                message += f"│        │       ├ {prefix} | {key}: {', '.join(value)}\n"
            else: 
                message += f"│        │       ├ {key}: \n│        │       ├      {'\n│        │       ├      '.join(value)}\n"
        else: 
            if prefix: 
                message += f"│        │       ├ {prefix} | {key}: {value}\n"
            else: 
                message += f"│        │       ├ {key}: {value}\n"
            

    return message
def show(data):
    message = "Report: \n"
    for sec in data:
        sec_info = data[sec]
        if sec_info:
            message += f"├    {sec}: \n│     └──┐\n"
            for func in sec_info:
                func_info = sec_info[func]
                if func_info:
                    message += f"│        ├ {func}: \n│        │    └──┐\n"
                    if isinstance(func_info, dict):
                        message += flatten(func_info)
                        message += "│        │       └\n"
                    else:
                        message += f"├            {func_info}\n"
    message += "│        └  \n└"
    print(message)