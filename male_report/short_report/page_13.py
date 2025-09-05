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


def page_13(results: List[BioMarker]):
    # c = canvas.Canvas("male_report/short_report/page_13.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "CBC Continued...")

    text1 = """
        The CBC Panel measures key blood components like Hemoglobin, HCT, WBC, RBC, MCV, MCH,
          MCHC, RDW, and Platelets to assess overall health and detect conditions such as anemia,
            infections, or blood disorders. It provides essential insights for diagnosis and monitoring.
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
    c.drawString(70, 520, "Patient’s CBC results")

    legend_image_path = "male_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # MCHC
    mchc = get_bio_marker_from_group(results, "mchc")
    if mchc is not None:
        mchc_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(mchc_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "MCHC")
        c.drawString(116, y_position + 5, str(mchc.value) + " " + str(mchc.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "305.0")
        c.drawString(433, y_position + 35, "360.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if mchc.value < 305:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 305 <= mchc.value <= 360:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # RDW
    rdw = get_bio_marker_from_group(results, "rdw")
    if rdw is not None:
        rdw_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(rdw_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "RDW")
        c.drawString(116, y_position + 5, str(rdw.value) + " " + str(rdw.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "11.50")
        c.drawString(433, y_position + 35, "17.30")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if rdw.value < 11.50:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 11.50 <= rdw.value <= 17.30:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Platelet Count
    platlets = get_bio_marker_from_group(results, "plateletCount")
    if platlets is not None:
        platlet_bar = convert_png_to_white_bg("male_report/short_report/ANONA_bar.png")
        c.drawImage(platlet_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Platelet Count")
        c.drawString(116, y_position + 5, str(platlets.value) + " " + str(platlets.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "150.0")
        c.drawString(346, y_position + 35, "190.0")
        c.drawString(412, y_position + 35, "350.0")
        c.drawString(476, y_position + 35, "400.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if platlets.value < 150:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 150 <= platlets.value < 190:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 190 <= platlets.value <= 350:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 350 < platlets.value <= 400:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_13()
