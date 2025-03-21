from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def create(data):
    done = []
    c = canvas.Canvas("report.pdf", pagesize=letter)
    c.setFont("Helvetica", 10)
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)

    text = c.beginText(40, 750)
    text.setFont("Helvetica", 10)

    def add_sec(sec, title, content):
        if sec not in done:
            text.setFont("Helvetica-Bold", 11)
            text.textLine(f"{sec}")
            done.append(sec)
        text.setFont("Helvetica-Bold", 10)
        text.textLine(f"    {title}")
        text.setFont("Helvetica", 10)
        if isinstance(content, dict):
            for k, v in content.items():
                text.textLine(f"        {k}: {v}")
        else:
            text.textLine(content)
        text.textLine("")

    for sec in data:
        sec_data = data[sec]
        for func in sec_data:
            func_data = sec_data[func]
            add_sec(sec, func, func_data)

    c.drawText(text)
    c.showPage()
    c.save()