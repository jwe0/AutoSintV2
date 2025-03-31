from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def flatten(data, indent_level=0):
    message = ""
    for key, value in data.items():
        if isinstance(value, dict):
            message += flatten(value, indent_level + 1)
        elif isinstance(value, list):
            message += "    " * indent_level
            message += "• " if indent_level > 0 else " "
            message += f" {key}: {', '.join(value)}\n"
        else:
            message += "    " * indent_level
            message += "• " if indent_level > 0 else " "
            message += f" {key}: {value}\n"

    return message


def show(data):
    message = ""
    for sec in data:
        message += f"\n# {sec}\n"
        sec_info = data[sec]
        for func in sec_info:
            message += f"## {func}\n"
            func_info = sec_info[func]
            if func_info:
                if isinstance(func_info, dict):
                    message += flatten(func_info)
    return message


def create(data):
    message = show(data)
    c = canvas.Canvas("report.pdf", pagesize=letter)
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