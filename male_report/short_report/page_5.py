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


def page_5(results: List[BioMarker]):
    # c = canvas.Canvas("male_report/short_report/page_5.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Inflammation")

    text1 = """
        The Inflammation Panel evaluates key markers like ESR, hs-CRP, Fibrinogen, CK, and Uric
          Acid to assess inflammation levels in the body. These tests help identify and monitor
            inflammatory conditions, infections, or tissue damage.
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
    c.drawString(70, 520, "Patient’s inflamation results")

    legend_image_path = "male_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # ESR
    esr = get_bio_marker_from_group(results, "sedimentationRate")
    if esr is not None:
        esr_bar = convert_png_to_white_bg("male_report/short_report/ONA_bar.png")
        c.drawImage(esr_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "ESR")
        c.drawString(116, y_position + 5, str(esr.value) + " " + str(esr.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "5.0")
        c.drawString(433, y_position + 35, "20.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if esr.value <= 5:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 5 < esr.value <= 20:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # hs-CRP
    hs_CRP = get_bio_marker_from_group(results, "cReactiveProtein")
    if hs_CRP is not None:
        hs_CRP_bar = convert_png_to_white_bg("male_report/short_report/ANO_bar.png")
        c.drawImage(hs_CRP_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "hs-CRP")
        c.drawString(116, y_position + 5, str(hs_CRP.value) + " " + str(hs_CRP.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "1.0")
        c.drawString(433, y_position + 35, "3.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if hs_CRP.value <= 1:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 1 < hs_CRP.value <= 3:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Fibrinogen quantitative
    fibrinogen = get_bio_marker_from_group(results, "fibrinogen")
    if fibrinogen is not None:
        fibrinogen_bar = convert_png_to_white_bg("male_report/short_report/NONA_bar.png")
        c.drawImage(fibrinogen_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Fibrinogen Q")
        c.drawString(116, y_position + 5, str(fibrinogen.value) + " " + str(fibrinogen.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "2.00")
        c.drawString(380, y_position + 35, "3.50")
        c.drawString(460, y_position + 35, "3.90")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if fibrinogen.value < 2:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 2 <= fibrinogen.value <= 3:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 3 < fibrinogen.value <= 3.9:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # Creatine Kinase
    creatine = get_bio_marker_from_group(results, "creatineKinase")
    if creatine is not None:
        creatine_bar = convert_png_to_white_bg("male_report/short_report/ANONA_bar.png")
        c.drawImage(creatine_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Creatine Kinase")
        c.drawString(116, y_position + 5, str(creatine.value) + " " + str(creatine.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "44.0")
        c.drawString(346, y_position + 35, "65.0")
        c.drawString(412, y_position + 35, "200.0")
        c.drawString(476, y_position + 35, "275.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if creatine.value < 44.0:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 44 <= creatine.value < 65:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 65 <= creatine.value <= 200:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 200 < creatine.value <= 275:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)
        y_position -= 53

    # Uric Acid
    uric_acid = get_bio_marker_from_group(results, "uricAcid")
    if uric_acid is not None:
        uric_acid_bar = convert_png_to_white_bg("male_report/short_report/AONA_bar.png")
        c.drawImage(uric_acid_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Uric Acid")
        c.drawString(116, y_position + 5, str(uric_acid.value) + " " + str(uric_acid.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(300, y_position + 35, "230.0")
        c.drawString(380, y_position + 35, "350.0")
        c.drawString(460, y_position + 35, "480.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if uric_acid.value < 230:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 230 <= uric_acid.value <= 350:
            c.circle(345, y_position + 17, 11, fill=1)
        elif 350 < uric_acid.value <= 480:
            c.circle(425, y_position + 17, 11, fill=1)
        else:
            c.circle(500, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_5()
