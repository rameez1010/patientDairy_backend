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


def page_7(results: List[BioMarker]):
    # c = canvas.Canvas("female_report/short_report/page_7.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "female_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Electrolytes")

    text1 = """
        The Electrolytes Panel evaluates key minerals like Sodium, Potassium, and Phosphorus to
          assess the body's fluid balance, nerve function, and muscle activity. These tests help
            detect imbalances, guide treatment, and maintain proper cellular and organ function.
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
    c.drawString(70, 520, "Patient’s electrolytes results")

    legend_image_path = "female_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # Sodium
    sodium = get_bio_marker_from_group(results, "sodium")
    if sodium is not None:
        sodium_bar = convert_png_to_white_bg("female_report/short_report/ANONA_bar.png")
        c.drawImage(sodium_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Sodium")
        c.drawString(116, y_position + 5, str(sodium.value) + " " + str(sodium.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "135.0")
        c.drawString(346, y_position + 35, "137.0")
        c.drawString(412, y_position + 35, "142.0")
        c.drawString(476, y_position + 35, "146.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if sodium.value < 135.0:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 135.0 <= sodium.value < 137.0:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 137.0 <= sodium.value <= 142.0:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 142.0 < sodium.value <= 146.0:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)
        y_position -= 53

    # Potassium
    potassium = get_bio_marker_from_group(results, "potassium")
    if potassium is not None:
        potassium_bar = convert_png_to_white_bg("female_report/short_report/ANONA_bar.png")
        c.drawImage(potassium_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Potassium")
        c.drawString(116, y_position + 5, str(potassium.value) + " " + str(potassium.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "3.50")
        c.drawString(346, y_position + 35, "4.00")
        c.drawString(412, y_position + 35, "5.00")
        c.drawString(476, y_position + 35, "5.40")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if potassium.value < 3.5:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 3.5 <= potassium.value < 4.0:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 4.0 <= potassium.value <= 5.0:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 5.0 < potassium.value <= 5.4:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)
        y_position -= 53

    # Phosphorus
    phosphorus = get_bio_marker_from_group(results, "phosphorus")
    if phosphorus is not None:
        phosphorus_bar = convert_png_to_white_bg("female_report/short_report/ANONA_bar.png")
        c.drawImage(phosphorus_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Phosphorus")
        c.drawString(116, y_position + 5, str(phosphorus.value) + " " + str(phosphorus.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "0.80")
        c.drawString(346, y_position + 35, "0.84")
        c.drawString(412, y_position + 35, "1.20")
        c.drawString(476, y_position + 35, "1.50")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if phosphorus.value < 0.8:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 0.8 <= phosphorus.value < 0.84:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 0.84 <= phosphorus.value <= 1.2:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 1.2 < phosphorus.value <= 1.5:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_7()
