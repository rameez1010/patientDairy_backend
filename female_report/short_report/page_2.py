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
pdfmetrics.registerFont(TTFont("Roboto-Thin", "female_report/fonts/Roboto-Thin.ttf"))
pdfmetrics.registerFont(TTFont("Roboto-Regular", "female_report/fonts/Roboto-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Roboto-Bold", "female_report/fonts/Roboto-Bold.ttf"))


def convert_png_to_white_bg(image_path):
    img = Image.open(image_path)
    # Create a new image with a white background
    new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    new_img.paste(img, (0, 0), img)
    # Save it as a new PNG
    new_image_path = image_path.replace(".png", "_white_bg.png")
    new_img.convert("RGB").save(new_image_path, "PNG")
    return new_image_path


def page_2(results: List[BioMarker]):
    # c = canvas.Canvas("female_report/short_report/page_2.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "female_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Glucose")

    text1 = """
        The Glucose Panel measures key markers like Glucose, HbA1c, and Insulin to assess blood
          sugar regulation. It helps diagnose and monitor diabetes, insulin resistance, and metabolic
            disorders, guiding treatment and preventing complications from abnormal glucose levels.
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
    c.drawString(70, 520, "Patient’s glucose results")

    legend_image_path = "female_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # Glucose
    glucose = get_bio_marker_from_group(results, "glucose")
    if glucose is not None:
        glucose_bar = convert_png_to_white_bg("female_report/short_report/AONA_bar.png")
        c.drawImage(glucose_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Glucose")
        c.drawString(116, y_position + 5, str(glucose.value) + " " + str(glucose.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(300, y_position + 35, "3.6")
        c.drawString(380, y_position + 35, "5.0")
        c.drawString(460, y_position + 35, "6.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if glucose.value <= 3.6:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 3.6 <= glucose.value <= 5:
            c.circle(345, y_position + 17, 11, fill=1)
        elif 5 < glucose.value <= 6:
            c.circle(425, y_position + 17, 11, fill=1)
        else:
            c.circle(500, y_position + 17, 11, fill=1)
        y_position -= 53

    # HBA1C
    hba1c = get_bio_marker_from_group(results, "hbA1c")
    if hba1c is not None:
        hba1c_bar = convert_png_to_white_bg("female_report/short_report/NONA_bar.png")
        c.drawImage(hba1c_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "HBA1C")
        c.drawString(116, y_position + 5, str(hba1c.value) + " " + str(hba1c.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(300, y_position + 35, "4.6")
        c.drawString(380, y_position + 35, "5.3")
        c.drawString(460, y_position + 35, "6.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if hba1c.value < 4.6:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 4.6 <= hba1c.value <= 5.3:
            c.circle(345, y_position + 17, 11, fill=1)
        elif 5.3 < hba1c.value <= 6:
            c.circle(425, y_position + 17, 11, fill=1)
        else:
            c.circle(500, y_position + 17, 11, fill=1)
        y_position -= 53

    # Insulin
    insulin = get_bio_marker_from_group(results, "insulin")
    if insulin is not None:
        insulin_bar = convert_png_to_white_bg("female_report/short_report/AONA_bar.png")
        c.drawImage(insulin_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Insulin")
        c.drawString(116, y_position + 5, str(insulin.value) + " " + str(insulin.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(300, y_position + 35, "15.0")
        c.drawString(380, y_position + 35, "60.0")
        c.drawString(460, y_position + 35, "180.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if insulin.value < 15:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 15 <= insulin.value <= 60:
            c.circle(345, y_position + 17, 11, fill=1)
        elif 60 < insulin.value <= 180:
            c.circle(425, y_position + 17, 11, fill=1)
        else:
            c.circle(500, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_2()
