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


def page_6(results: List[BioMarker]):
    # c = canvas.Canvas("male_report/short_report/page_6.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Vitamins")

    text1 = """
        The Vitamin Panel measures essential nutrients like Vitamin B12, Vitamin D (25-hydroxy),
          and Vitamin A. These tests help identify deficiencies or imbalances, supporting proper
            immune function, bone health, vision, and overall well-being.
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
    c.drawString(70, 520, "Patient’s vitamin results")

    legend_image_path = "male_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # Vitamin B12
    vitaminb12 = get_bio_marker_from_group(results, "vitaminB12")
    if vitaminb12 is not None:
        vitaminb12_bar = convert_png_to_white_bg("male_report/short_report/ANAO_bar.png")
        c.drawImage(vitaminb12_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Vitamin B12")
        c.drawString(116, y_position + 5, str(vitaminb12.value) + " " + str(vitaminb12.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "220.0")
        c.drawString(380, y_position + 35, "652.0")
        c.drawString(460, y_position + 35, "800.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if vitaminb12.value < 220:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 220 <= vitaminb12.value <= 652:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 652 < vitaminb12.value < 800:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # Vitamin D
    vitamind = get_bio_marker_from_group(results, "vitaminD")
    if vitamind is not None:
        vitamind_bar = convert_png_to_white_bg("male_report/short_report/ANOA_bar.png")
        c.drawImage(vitamind_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Vitamin D")
        c.drawString(116, y_position + 5, str(vitamind.value) + " " + str(vitamind.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(300, y_position + 35, "76.0")
        c.drawString(380, y_position + 35, "200.0")
        c.drawString(460, y_position + 35, "250.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if vitamind.value < 76:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 76 <= vitamind.value < 200:
            c.circle(345, y_position + 17, 11, fill=1)
        elif 200 <= vitamind.value <= 250:
            c.circle(425, y_position + 17, 11, fill=1)
        else:
            c.circle(500, y_position + 17, 11, fill=1)
        y_position -= 53

    # Vitamin A
    vitamina = get_bio_marker_from_group(results, "vitaminA")
    if vitamina is not None:
        vitamina_bar = convert_png_to_white_bg("male_report/short_report/ANONA_bar.png")
        c.drawImage(vitamina_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Vitamin A")
        c.drawString(116, y_position + 5, str(vitamina.value) + " " + str(vitamina.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "1.20")
        c.drawString(346, y_position + 35, "1.99")
        c.drawString(412, y_position + 35, "3.00")
        c.drawString(476, y_position + 35, "3.50")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if vitamina.value < 1.2:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 1.2 <= vitamina.value < 1.99:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 1.99 <= vitamina.value <= 3.0:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 3.0 < vitamina.value <= 3.5:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_6()
