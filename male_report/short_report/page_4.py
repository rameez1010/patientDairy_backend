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


def page_4(results: List[BioMarker]):
    # c = canvas.Canvas("male_report/short_report/page_4.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Minerals")

    text1 = """
        The Minerals Panel measures essential nutrients like Calcium, Magnesium, Zinc, Ferritin,
          and Selenium Plasma. These tests help assess mineral balance in the body, identify
            deficiencies or excesses, and guide interventions to support overall health.
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
    c.drawString(70, 520, "Patient’s mineral results")

    legend_image_path = "male_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_postion = 455
    # Calcium
    calcium = get_bio_marker_from_group(results, "calcium")
    if calcium is not None:
        calcium_bar = convert_png_to_white_bg("male_report/short_report/ANONA_bar.png")
        c.drawImage(calcium_bar, 70, y_postion, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_postion + 20, "Calcium")
        c.drawString(116, y_postion + 5, str(calcium.value) + " " + str(calcium.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_postion + 35, "2.15")
        c.drawString(346, y_postion + 35, "2.22")
        c.drawString(412, y_postion + 35, "2.45")
        c.drawString(476, y_postion + 35, "2.60")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if calcium.value < 2.15:
            c.circle(260, y_postion + 17, 11, fill=1)
        elif 2.15 <= calcium.value < 2.22:
            c.circle(325, y_postion + 17, 11, fill=1)
        elif 2.22 <= calcium.value <= 2.45:
            c.circle(390, y_postion + 17, 11, fill=1)
        elif 2.45 < calcium.value <= 2.60:
            c.circle(455, y_postion + 17, 11, fill=1)
        else:
            c.circle(515, y_postion + 17, 11, fill=1)
        y_postion -= 53

    # Magnesium Serum
    magnesiumS = get_bio_marker_from_group(results, "magnesium")
    if magnesiumS is not None:
        magnesiumS_bar = convert_png_to_white_bg("male_report/short_report/ANOA_bar.png")
        c.drawImage(magnesiumS_bar, 70, y_postion, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_postion + 20, "Magnesium Serum")
        c.drawString(116, y_postion + 5, str(magnesiumS.value) + " " + str(magnesiumS.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_postion + 35, "0.65")
        c.drawString(380, y_postion + 35, "0.90")
        c.drawString(460, y_postion + 35, "1.10")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if magnesiumS.value < 0.65:
            c.circle(270, y_postion + 17, 11, fill=1)
        elif 0.65 <= magnesiumS.value < 0.90:
            c.circle(347, y_postion + 17, 11, fill=1)
        elif 0.90 <= magnesiumS.value <= 1.10:
            c.circle(430, y_postion + 17, 11, fill=1)
        else:
            c.circle(510, y_postion + 17, 11, fill=1)
        y_postion -= 53

    # Magnesium RBC
    magnesiumR = get_bio_marker_from_group(results, "magnesiumR")
    if magnesiumR is not None:
        magnesiumR_bar = convert_png_to_white_bg("male_report/short_report/ANOA_bar.png")
        c.drawImage(magnesiumR_bar, 70, 345, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_postion + 20, "Magnesium RBC")
        c.drawString(116, y_postion + 5, str(magnesiumR.value) + " " + str(magnesiumR.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_postion + 35, "4.00")
        c.drawString(380, y_postion + 35, "5.50")
        c.drawString(460, y_postion + 35, "6.40")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if magnesiumR.value < 4:
            c.circle(270, y_postion + 17, 11, fill=1)
        elif 4 <= magnesiumR.value < 5.5:
            c.circle(347, y_postion + 17, 11, fill=1)
        elif 5.5 <= magnesiumR.value <= 6.4:
            c.circle(430, y_postion + 17, 11, fill=1)
        else:
            c.circle(510, y_postion + 17, 11, fill=1)
        y_postion -= 53

    # Zinc
    zinc = get_bio_marker_from_group(results, "zinc")
    if zinc is not None:
        zinc_bar = convert_png_to_white_bg("male_report/short_report/ANOA_bar.png")
        c.drawImage(zinc_bar, 70, y_postion, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_postion + 20, "Zinc")
        c.drawString(116, y_postion + 5, str(zinc.value) + " " + str(zinc.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_postion + 35, "7.80")
        c.drawString(380, y_postion + 35, "12.00")
        c.drawString(460, y_postion + 35, "16.80")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if zinc.value < 7.8:
            c.circle(270, y_postion + 17, 11, fill=1)
        elif 7.8 <= zinc.value < 12:
            c.circle(347, y_postion + 17, 11, fill=1)
        elif 12 <= zinc.value <= 16.8:
            c.circle(430, y_postion + 17, 11, fill=1)
        else:
            c.circle(510, y_postion + 17, 11, fill=1)
        y_postion -= 53

    # Ferritin
    ferritin = get_bio_marker_from_group(results, "ferritin")
    if ferritin is not None:
        ferritin_bar = convert_png_to_white_bg("male_report/short_report/ANONA_bar.png")
        c.drawImage(ferritin_bar, 70, y_postion, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_postion + 20, "Ferritin")
        c.drawString(116, y_postion + 5, str(ferritin.value) + " " + str(ferritin.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_postion + 35, "18.00")
        c.drawString(346, y_postion + 35, "90.00")
        c.drawString(412, y_postion + 35, "250.0")
        c.drawString(476, y_postion + 35, "543.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if ferritin.value < 18:
            c.circle(260, y_postion + 17, 11, fill=1)
        elif 18 <= ferritin.value < 90:
            c.circle(325, y_postion + 17, 11, fill=1)
        elif 90 <= ferritin.value <= 250:
            c.circle(390, y_postion + 17, 11, fill=1)
        elif 250 < ferritin.value <= 543:
            c.circle(455, y_postion + 17, 11, fill=1)
        else:
            c.circle(515, y_postion + 17, 11, fill=1)
        y_postion -= 53

    # Selenium
    selenium = get_bio_marker_from_group(results, "seleniumPlasma")
    if selenium is not None:
        selenium_bar = convert_png_to_white_bg("male_report/short_report/ANOA_bar.png")
        c.drawImage(selenium_bar, 70, y_postion, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_postion + 20, "Selenium")
        c.drawString(116, y_postion + 5, str(selenium.value) + " " + str(selenium.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_postion + 35, "105.3")
        c.drawString(380, y_postion + 35, "120.0")
        c.drawString(460, y_postion + 35, "160.4")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if selenium.value < 105.3:
            c.circle(270, y_postion + 17, 11, fill=1)
        elif 105.3 <= selenium.value < 120.0:
            c.circle(347, y_postion + 17, 11, fill=1)
        elif 120 <= selenium.value <= 160.40:
            c.circle(430, y_postion + 17, 11, fill=1)
        else:
            c.circle(510, y_postion + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_4()
