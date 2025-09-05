import io
from typing import List

from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from models.patient_models import BioMarker
from utils.biomarker_helpers import get_bio_marker_from_group

# Font registration
pdfmetrics.registerFont(TTFont("Roboto-Thin", "male_report/fonts/Roboto-Thin.ttf"))
pdfmetrics.registerFont(TTFont("Roboto-Regular", "male_report/fonts/Roboto-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Roboto-Bold", "male_report/fonts/Roboto-Bold.ttf"))


def convert_png_to_white_bg(image_path):
    img = Image.open(image_path)
    # Create a new image with a white background
    new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    new_img.paste(img, (0, 0), img)
    # Save it as a new PNG
    new_image_path = image_path.replace(".png", "_white_bg.png")
    new_img.convert("RGB").save(new_image_path, "PNG")
    return new_image_path


def page_3(results: List[BioMarker]):
    # c = canvas.Canvas("male_report/short_report/page_3.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Renal")

    text1 = """
        The Renal Panel evaluates kidney function by measuring key markers such as Creatinine and
          eGFR. These tests help detect and monitor kidney disease, assess kidney health, and guide
            treatment to prevent or manage complications related to impaired renal function.
        """

    text_object = c.beginText(70, 600)
    text_object.setFont("Roboto-Regular", 11)
    text_object.setFillColor("gray")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    c.setFillColor("#4b4b4b")
    c.setFont("Roboto-Regular", 15)
    c.drawString(70, 520, "Patient’s renal results")

    legend_image_path = "male_report/short_report/colors.jpg"
    c.drawImage(
        legend_image_path,
        340,
        520,
        width=200,
        height=15,
        preserveAspectRatio=False,
    )

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # Creatinine
    creatinine = get_bio_marker_from_group(results, "creatinine")
    if creatinine is not None:
        creatinine_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(
            creatinine_bar,
            70,
            y_position,
            width=480,
            height=35,
            preserveAspectRatio=False,
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Creatinine")
        c.drawString(116, y_position + 5, str(creatinine.value) + " " + str(creatinine.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "67.0")
        c.drawString(433, y_position + 35, "117.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if creatinine.value < 67:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 67 <= creatinine.value <= 117:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # eFGR
    egfr = get_bio_marker_from_group(results, "eGFR")
    if egfr is not None:
        efgr_bar = convert_png_to_white_bg("male_report/short_report/ANO_bar.png")
        c.drawImage(
            efgr_bar,
            70,
            y_position,
            width=480,
            height=35,
            preserveAspectRatio=False,
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "eGFR")
        c.drawString(116, y_position + 5, str(egfr.value) + " " + str(egfr.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "60.0")
        c.drawString(433, y_position + 35, "99.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if egfr.value < 60:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 60 <= egfr.value < 90:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_3()
