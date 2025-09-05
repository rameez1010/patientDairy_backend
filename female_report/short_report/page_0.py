import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Font registration
pdfmetrics.registerFont(TTFont("Roboto-Regular", "female_report/fonts/Roboto-Regular.ttf"))


def cover_page(results):
    # c = canvas.Canvas('female_report/short_report/page_0.pdf', pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "female_report/short_report/cover.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    full_name = f"{results.get('firstName', '')} {results.get('lastName', '')}"

    c.setFillColor("gray")
    c.setFont("Roboto-Regular", 12)
    c.drawString(125, 369, results.get("collectionDate", ""))
    c.drawString(125, 314, full_name + ", " + str(results.get("age", "")) + " years old female born on " + results.get("dateOfBirth", ""))
    c.drawString(125, 259, results.get("practitioner", ""))
    c.drawString(125, 205, "BioKrystal AI")

    c.showPage()
    c.save()

    return buffer


# cover_page()
