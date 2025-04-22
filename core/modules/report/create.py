import os, random, string, json, requests
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

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
    blacklist = ["Images"]
    message = ""
    for sec in data:
        if sec in blacklist:
            continue
        message += f"\n○ {sec}\n"
        sec_info = data[sec]
        for func in sec_info:
            message += f"  ‣ {func}\n"
            func_info = sec_info[func]
            if func_info:
                if isinstance(func_info, dict):
                    message += flatten(func_info)
    return message


def create(data, id):
    message = show(data)
    c = canvas.Canvas("reports/{}/report.pdf".format(id), pagesize=letter)
    c.setFont("Helvetica", 10)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)

    margin_top = 750
    margin_bottom = 50
    line_height = 12 
    x_position = 40
    y_position = margin_top

    for line in message.split("\n"):
        if y_position < margin_bottom:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = margin_top
        if "##" in line:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x_position, y_position, line.replace("##", ""))
            y_position -= line_height
            c.drawString(x_position, y_position, " ")
        elif "#" in line:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(x_position, y_position, line.replace("#", ""))
            y_position -= line_height
            c.drawString(x_position, y_position, " ")
        else:
            c.setFont("Helvetica", 10)
            c.drawString(x_position, y_position, line)
        
        y_position -= line_height

    c.showPage()
    c.save()

def dirs(json_data):
    def find_ext(url):
        types = [
            "jpg",
            "png",
            "jpeg",
            "gif",
            "svg",
        ]

        for type_ in types:
            if type_ in url:
                return type_


    id = "".join(random.choices(string.ascii_letters + string.digits, k=10))

    dirs_ = [
        "reports",
        f"reports/{id}",
        f"reports/{id}/media",
        f"reports/{id}/media/images",
    ]

    for dir_ in dirs_:
        if not os.path.exists(dir_):
            os.mkdir(dir_)


    if not os.path.exists(f"reports/{id}"):
        os.mkdir(f"reports/{id}")

    with open(f"reports/{id}/report.json", "w") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=True)

    with open(f"reports/{id}/report.txt", "w") as f:
        message = show(json_data)
        f.write(message)


    images = json_data["Images"]
    print("Downloading images...")
    for image in images:
        if not os.path.exists(f"reports/{id}/media/images/{image}"):
            os.mkdir(f"reports/{id}/media/images/{image}")
        for album in images[image]:
            if not os.path.exists(f"reports/{id}/media/images/{image}/{album}"):
                os.mkdir(f"reports/{id}/media/images/{image}/{album}")
            for img in images[image][album]:
                r = requests.get(img)
                name = "".join(random.choices(string.ascii_letters + string.digits, k=10))
                ext = find_ext(img)
                with open(f"reports/{id}/media/images/{image}/{album}/{name}.{ext}", "wb") as f:
                    f.write(r.content)
    create(json_data, id)