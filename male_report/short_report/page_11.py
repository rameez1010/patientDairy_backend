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
pdfmetrics.registerFont(
    TTFont("Roboto-Regular", "male_report/fonts/Roboto-Regular.ttf")
)
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


def page_11(results: List[BioMarker]):
    # c = canvas.Canvas("male_report/short_report/page_11.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/short_report/bg_new.jpg"
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

    legend_image_path = "male_report/short_report/colors.jpg"
    c.drawImage(
        legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False
    )

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # DHEA
    dhea = get_bio_marker_from_group(results, "dhea")
    if dhea is not None:
        dhea_bar = convert_png_to_white_bg("male_report/short_report/NAOA_bar.png")
        c.drawImage(
            dhea_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "DHEA")
        c.drawString(116, y_position + 5, str(dhea.value) + " " + str(dhea.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "9.8")
        c.drawString(380, y_position + 35, "10.0")
        c.drawString(460, y_position + 35, "20.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if dhea.value <= 9.8:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 9.8 < dhea.value < 10:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 10 <= dhea.value <= 20:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # Prolactain
    prolactain = get_bio_marker_from_group(results, "prolactin")
    if prolactain is not None:
        prolactain_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(
            prolactain_bar,
            70,
            y_position,
            width=480,
            height=35,
            preserveAspectRatio=False,
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Prolactain")
        c.drawString(
            116, y_position + 5, str(prolactain.value) + " " + str(prolactain.unit)
        )

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "4.0")
        c.drawString(433, y_position + 35, "19.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if prolactain.value < 4:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 4 <= prolactain.value <= 19:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Sex Hormone
    sexhormone = get_bio_marker_from_group(results, "sexHormoneBindGlobulin")
    if sexhormone is not None:
        sexhormone_bar = convert_png_to_white_bg(
            "male_report/short_report/AONA_bar.png"
        )
        c.drawImage(
            sexhormone_bar,
            70,
            y_position,
            width=480,
            height=35,
            preserveAspectRatio=False,
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Sex Hormone")
        c.drawString(
            116, y_position + 5, str(sexhormone.value) + " " + str(sexhormone.unit)
        )

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "10.0")
        c.drawString(380, y_position + 35, "40.0")
        c.drawString(460, y_position + 35, "70.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if sexhormone.value < 10.0:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 10 <= sexhormone.value <= 40:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 40 < sexhormone.value <= 70:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # AM Cortisol
    cortisol = get_bio_marker_from_group(results, "cortisolAm")
    if cortisol is not None:
        cortisol_bar = convert_png_to_white_bg("male_report/short_report/ANONA_bar.png")
        c.drawImage(
            cortisol_bar,
            70,
            y_position,
            width=480,
            height=35,
            preserveAspectRatio=False,
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "AM Cortisol")
        c.drawString(
            116, y_position + 5, str(cortisol.value) + " " + str(cortisol.unit)
        )

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

        if cortisol.value < 130:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 130 <= cortisol.value < 250:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 250 <= cortisol.value <= 350:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 350 < cortisol.value <= 540:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)
        y_position -= 53

    # Total PSA
    total_psa = get_bio_marker_from_group(results, "totalPsa")
    if total_psa is not None:
        total_psa_bar = convert_png_to_white_bg("male_report/short_report/ONA_bar.png")
        c.drawImage(
            total_psa_bar,
            70,
            y_position,
            width=480,
            height=35,
            preserveAspectRatio=False,
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Total PSA")
        c.drawString(
            116, y_position + 5, str(total_psa.value) + " " + str(total_psa.unit)
        )

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "1.0")
        c.drawString(433, y_position + 35, "2.5")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if total_psa.value < 1.0:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 1.0 <= total_psa.value < 2.5:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_11()
