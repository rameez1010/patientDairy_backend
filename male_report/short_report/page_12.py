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


def page_12(results: List[BioMarker]):
    # c = canvas.Canvas("male_report/short_report/page_12.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "CBC")

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
    # Hemoglobin
    hemoglobin = get_bio_marker_from_group(results, "hemoglobin")
    if hemoglobin is not None:
        hemoglobin_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(hemoglobin_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Hemoglobin")
        c.drawString(116, y_position + 5, str(hemoglobin.value) + " " + str(hemoglobin.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "129.0")
        c.drawString(433, y_position + 35, "175.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if hemoglobin.value < 129:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 129 <= hemoglobin.value <= 175:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Hematocrit
    hematocrit = get_bio_marker_from_group(results, "hematocrit")
    if hematocrit is not None:
        hematocrit_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(hematocrit_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Hematocrit")
        c.drawString(116, y_position + 5, str(hematocrit.value) + " " + str(hematocrit.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "0.39")
        c.drawString(433, y_position + 35, "0.50")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if hematocrit.value < 0.39:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 0.39 <= hematocrit.value <= 0.5:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # WBC
    wbc = get_bio_marker_from_group(results, "wbc")
    if wbc is not None:
        wbc_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(wbc_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "WBC")
        c.drawString(116, y_position + 5, str(wbc.value) + " " + str(wbc.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "3.20")
        c.drawString(433, y_position + 35, "11.00")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if wbc.value < 3.2:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 3.2 <= wbc.value <= 11:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # RBC
    rbc = get_bio_marker_from_group(results, "rbc")
    if rbc is not None:
        rbc_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(rbc_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "RBC")
        c.drawString(116, y_position + 5, str(rbc.value) + " " + str(rbc.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "4.2")
        c.drawString(433, y_position + 35, "6.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if rbc.value < 4.2:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 4.2 <= rbc.value <= 6:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # MCV
    mcv = get_bio_marker_from_group(results, "mcv")
    if mcv is not None:
        mcv_bar = convert_png_to_white_bg("male_report/short_report/ANONA_bar.png")
        c.drawImage(mcv_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "MCV")
        c.drawString(116, y_position + 5, str(mcv.value) + " " + str(mcv.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "80.0")
        c.drawString(346, y_position + 35, "82.0")
        c.drawString(412, y_position + 35, "90.0")
        c.drawString(476, y_position + 35, "100.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if mcv.value < 80:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 80 <= mcv.value < 82:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 82 <= mcv.value <= 90:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 90 < mcv.value <= 100:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)
        y_position -= 53

    # MCH
    mch = get_bio_marker_from_group(results, "mch")
    if mch is not None:
        mch_bar = convert_png_to_white_bg("male_report/short_report/AOA_bar.png")
        c.drawImage(mch_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "MCH")
        c.drawString(116, y_position + 5, str(mch.value) + " " + str(mch.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "27.0")
        c.drawString(433, y_position + 35, "33.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if mch.value < 27:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 27 <= mch.value <= 33:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_12()
