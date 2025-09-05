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


def page_9(results: List[BioMarker]):
    # c = canvas.Canvas("female_report/short_report/page_9.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "female_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Thyroid")

    text1 = """
        The Thyroid Panel evaluates key markers like TSH, Free T4, Free T3, Reverse T3, TPO
          Antibodies, and Anti-TG to assess thyroid function. These tests help diagnose and monitor
            thyroid disorders, such as hypothyroidism or hyperthyroidism.
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
    c.drawString(70, 520, "Patient’s thyroid results")

    legend_image_path = "female_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # TSH
    tsh = get_bio_marker_from_group(results, "thyroidStimulatingHormone")
    if tsh is not None:
        tsh_bar = convert_png_to_white_bg("female_report/short_report/AONA_bar.png")
        c.drawImage(tsh_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "TSH")
        c.drawString(116, y_position + 5, str(tsh.value) + " " + str(tsh.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "0.32")
        c.drawString(380, y_position + 35, "1.00")
        c.drawString(460, y_position + 35, "4.00")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if tsh.value < 0.32:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 0.32 <= tsh.value <= 1:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 1 < tsh.value <= 4:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # Free T4
    freet4 = get_bio_marker_from_group(results, "freeT4")
    if freet4 is not None:
        freet4_bar = convert_png_to_white_bg("female_report/short_report/ANOA_bar.png")
        c.drawImage(freet4_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Free T4")
        c.drawString(116, y_position + 5, str(freet4.value) + " " + str(freet4.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(300, y_position + 35, "9.0")
        c.drawString(380, y_position + 35, "10.0")
        c.drawString(460, y_position + 35, "23.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if freet4.value < 9:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 9 <= freet4.value < 10:
            c.circle(345, y_position + 17, 11, fill=1)
        elif 10 <= freet4.value <= 23:
            c.circle(425, y_position + 17, 11, fill=1)
        else:
            c.circle(500, y_position + 17, 11, fill=1)
        y_position -= 53

    # Free T3
    freet3 = get_bio_marker_from_group(results, "freeT3")
    if freet3 is not None:
        freet3_bar = convert_png_to_white_bg("female_report/short_report/ANOA_bar.png")
        c.drawImage(freet3_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Free T3")
        c.drawString(116, y_position + 5, str(freet3.value) + " " + str(freet3.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "3.40")
        c.drawString(380, y_position + 35, "4.80")
        c.drawString(460, y_position + 35, "6.00")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if freet3.value < 3.4:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 3.4 <= freet3.value < 4.8:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 4.8 <= freet3.value <= 6:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # Reverse T3
    reverset3 = get_bio_marker_from_group(results, "reverseT3")
    if reverset3 is not None:
        reverset3_bar = convert_png_to_white_bg("female_report/short_report/ANONA_bar.png")
        c.drawImage(reverset3_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Reverse T3")
        c.drawString(116, y_position + 5, str(reverset3.value) + " " + str(reverset3.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "8.0")
        c.drawString(346, y_position + 35, "10.0")
        c.drawString(412, y_position + 35, "16.0")
        c.drawString(476, y_position + 35, "25.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if reverset3.value < 8.0:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 8 <= reverset3.value < 10:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 10 <= reverset3.value <= 16.0:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 16 < reverset3.value <= 25.0:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)
        y_position -= 53

    # anti-TPO
    tpo = get_bio_marker_from_group(results, "thyroidPeroxidaseAntibody")
    if tpo is not None:
        tpo_bar = convert_png_to_white_bg("female_report/short_report/OA_bar.png")
        c.drawImage(tpo_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "anti-TPO")
        c.drawString(116, y_position + 5, str(tpo.value) + " " + str(tpo.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(375, y_position + 35, "35.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if tpo.value <= 35:
            c.circle(320, y_position + 17, 11, fill=1)
        else:
            c.circle(450, y_position + 17, 11, fill=1)
        y_position -= 53

    # anti-TG
    tg = get_bio_marker_from_group(results, "thyroglobulinAntibodies")
    if tg is not None:
        tg_bar = convert_png_to_white_bg("female_report/short_report/OA_bar.png")
        c.drawImage(tg_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "anti-TG")
        c.drawString(116, y_position + 5, str(tg.value) + " " + str(tg.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(375, y_position + 35, "41.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if tg.value <= 41:
            c.circle(320, y_position + 17, 11, fill=1)
        else:
            c.circle(450, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_9()
