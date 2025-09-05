import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Font registration
pdfmetrics.registerFont(TTFont("Roboto-Regular", "male_report/fonts/Roboto-Regular.ttf"))


def cover_page(results):
    # c = canvas.Canvas('male_report/short_report/page_0.pdf', pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/gene_report/cover_background.png"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    full_name = f"{results.get('firstName', '')} {results.get('lastName', '')}"

    c.setFillColor("gray")
    c.setFont("Roboto-Regular", 12)
    c.drawString(125, 365, full_name + ", 38 years old female born on June 18 1983")
    c.drawString(125, 310, "Alex Nowak")
    c.drawString(125, 255, "BioKrystal AI")

    c.showPage()
    c.save()

    return buffer


# cover_page()
