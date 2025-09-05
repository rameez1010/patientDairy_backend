import io

from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Font registration
pdfmetrics.registerFont(TTFont("Roboto-Thin", "female_report/fonts/Roboto-Thin.ttf"))
pdfmetrics.registerFont(TTFont("Roboto-Regular", "female_report/fonts/Roboto-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Roboto-Bold", "female_report/fonts/Roboto-Bold.ttf"))

from typing import List

from models.patient_models import BioMarker
from utils.biomarker_helpers import get_bio_marker_from_group


def convert_png_to_white_bg(image_path):
    img = Image.open(image_path)
    # Create a new image with a white background
    new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    new_img.paste(img, (0, 0), img)
    # Save it as a new PNG
    new_image_path = image_path.replace(".png", "_white_bg.png")
    new_img.convert("RGB").save(new_image_path, "PNG")
    return new_image_path


def page_11(results: List[BioMarker]):
    # c = canvas.Canvas("female_report/short_report/page_11.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "female_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Hormones Continued...")

    text1 = """
        The Hormones Panel measures key markers like FSH, LH, Estradiol, Progesterone, Total
          Testosterone, Free Testosterone, DHEA, Prolactin, SHBG, and AM Cortisol to assess hormonal
            balance and function. These tests help diagnose and manage related conditions.
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
    c.drawString(70, 520, "Patient’s hormone results")

    legend_image_path = "female_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # DHEA
    dhea = get_bio_marker_from_group(results, "dhea")
    if dhea is not None:
        dhea_bar = convert_png_to_white_bg("female_report/short_report/ANOA_bar.png")
        c.drawImage(dhea_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "DHEA")
        c.drawString(116, y_position + 5, str(dhea.value) + " " + str(dhea.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "2.68")
        c.drawString(380, y_position + 35, "5.00")
        c.drawString(460, y_position + 35, "10.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if dhea.value < 2.68:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 2.68 <= dhea.value < 5:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 5.0 <= dhea.value <= 10.0:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # Prolactain
    prolactain = get_bio_marker_from_group(results, "prolactin")
    if prolactain is not None:
        prolactain_bar = convert_png_to_white_bg("female_report/short_report/AOA_bar.png")
        c.drawImage(prolactain_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Prolactain")
        c.drawString(116, y_position + 5, str(prolactain.value) + " " + str(prolactain.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "5.0")
        c.drawString(433, y_position + 35, "27.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if prolactain.value < 5:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 5 <= prolactain.value <= 27:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Sex Hormone
    sexhormone = get_bio_marker_from_group(results, "sexHormoneBindGlobulin")
    if sexhormone is not None:
        sexhormone_bar = convert_png_to_white_bg("female_report/short_report/ANOA_bar.png")
        c.drawImage(sexhormone_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Sex Hormone")
        c.drawString(116, y_position + 5, str(sexhormone.value) + " " + str(sexhormone.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "20.0")
        c.drawString(380, y_position + 35, "80.0")
        c.drawString(460, y_position + 35, "180.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if sexhormone.value < 20.0:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 20.0 <= sexhormone.value <= 80.0:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 80.0 < sexhormone.value <= 180.0:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # AM Cortisol
    cortisol = get_bio_marker_from_group(results, "cortisolAm")
    if cortisol is not None:
        cortisol_bar = convert_png_to_white_bg("female_report/short_report/ANONA_bar.png")
        c.drawImage(cortisol_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "AM Cortisol")
        c.drawString(116, y_position + 5, str(cortisol.value) + " " + str(cortisol.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "130.0")
        c.drawString(346, y_position + 35, "250.0")
        c.drawString(412, y_position + 35, "350.0")
        c.drawString(476, y_position + 35, "540.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if cortisol.value < 130.0:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 130.0 <= cortisol.value < 250.0:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 250.0 <= cortisol.value <= 350.0:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 350.0 < cortisol.value <= 540.0:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_11()
