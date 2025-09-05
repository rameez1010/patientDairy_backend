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


def page_10(results: List[BioMarker]):
    # c = canvas.Canvas("male_report/short_report/page_10.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Hormones")

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
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # FSH
    fsh = get_bio_marker_from_group(results, "follitropin")
    if fsh is not None:
        fsh_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(fsh_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "FSH")
        c.drawString(116, y_position + 5, str(fsh.value) + " " + str(fsh.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "1.0")
        c.drawString(433, y_position + 35, "8.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if fsh.value < 1:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 1 <= fsh.value <= 8:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # LH
    lh = get_bio_marker_from_group(results, "lutropin")
    if lh is not None:
        lh_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(lh_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "LH")
        c.drawString(116, y_position + 5, str(lh.value) + " " + str(lh.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "1.0")
        c.drawString(433, y_position + 35, "7.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if lh.value < 1:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 1 <= lh.value <= 7:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Estradiol
    estradiol = get_bio_marker_from_group(results, "estradiol")
    if estradiol is not None:
        estradiol_bar = convert_png_to_white_bg("male_report/short_report/ONA_bar.png")
        c.drawImage(estradiol_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Estradiol")
        c.drawString(116, y_position + 5, str(estradiol.value) + " " + str(estradiol.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "150.0")
        c.drawString(433, y_position + 35, "162.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if estradiol.value <= 150:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 150 < estradiol.value <= 162:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Progesterone
    progesterone = get_bio_marker_from_group(results, "progesterone")
    if progesterone is not None:
        progesterone_bar = convert_png_to_white_bg("male_report/short_report/OA_bar.png")
        c.drawImage(progesterone_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Progesterone")
        c.drawString(116, y_position + 5, str(progesterone.value) + " " + str(progesterone.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(375, y_position + 35, "0.7")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if progesterone.value <= 0.7:
            c.circle(320, y_position + 17, 11, fill=1)
        else:
            c.circle(450, y_position + 17, 11, fill=1)
        y_position -= 53

        # Total Testosterone

    testosterone = get_bio_marker_from_group(results, "testosterone")
    if testosterone is not None:
        testosterone_bar = convert_png_to_white_bg("male_report/short_report/ANOA_bar.png")
        c.drawImage(testosterone_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Total Testosterone")
        c.drawString(116, y_position + 5, str(testosterone.value) + " " + str(testosterone.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(300, y_position + 35, "7.6")
        c.drawString(380, y_position + 35, "28.0")
        c.drawString(460, y_position + 35, "38.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if testosterone.value < 7.6:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 7.6 <= testosterone.value < 28:
            c.circle(345, y_position + 17, 11, fill=1)
        elif 28 <= testosterone.value <= 38:
            c.circle(425, y_position + 17, 11, fill=1)
        else:
            c.circle(500, y_position + 17, 11, fill=1)
        y_position -= 53

    # Free Testosterone
    testosteronefree = get_bio_marker_from_group(results, "testosteroneFree")
    if testosteronefree is not None:
        testosteronefree_bar = convert_png_to_white_bg("male_report/short_report/ANAO_bar.png")
        c.drawImage(testosteronefree_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Free Testosterone")
        c.drawString(116, y_position + 5, str(testosteronefree.value) + " " + str(testosteronefree.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "196.0")
        c.drawString(380, y_position + 35, "636.0")
        c.drawString(460, y_position + 35, "700.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if testosteronefree.value < 196:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 196 <= testosteronefree.value <= 636:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 636 <= testosteronefree.value < 700:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_10()
