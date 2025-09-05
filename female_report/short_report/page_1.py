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
pdfmetrics.registerFont(
    TTFont("Roboto-Regular", "female_report/fonts/Roboto-Regular.ttf")
)
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


def page_1(results: List[BioMarker]):
    # c = canvas.Canvas("female_report/short_report/page_1.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "female_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Lipids")

    text1 = """
        The Lipids panel measures key fats in the blood, including total cholesterol, LDL, HDL,
triglycerides, non-HDL cholesterol, and the cholesterol-to-HDL ratio. These values help
assess the risk of cardiovascular diseases and guide treatment to manage lipid imbalances.
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
    c.drawString(70, 520, "Patient’s lipid results")

    legend_image_path = "female_report/short_report/colors.jpg"
    c.drawImage(
        legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False
    )

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # Cholesterol
    cholesterol = get_bio_marker_from_group(results, "cholesterol")
    if cholesterol is not None:
        cholesterol_bar = convert_png_to_white_bg(
            "female_report/short_report/OA_bar.png"
        )
        c.drawImage(
            cholesterol_bar,
            70,
            y_position,
            width=480,
            height=35,
            preserveAspectRatio=False,
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Cholesterol")
        c.drawString(
            116, y_position + 5, str(cholesterol.value) + " " + str(cholesterol.unit)
        )

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(375, y_position + 35, "5.2")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if cholesterol.value <= 5.2:
            c.circle(320, y_position + 17, 11, fill=1)
        else:
            c.circle(450, y_position + 17, 11, fill=1)
        y_position -= 53

    # LDL Cholesterol
    ldl_cholesterol = get_bio_marker_from_group(results, "ldlCholesterol")
    if ldl_cholesterol is not None:
        ldl_bar = convert_png_to_white_bg("female_report/short_report/OA_bar.png")
        c.drawImage(
            ldl_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "LDL")
        c.drawString(
            116,
            y_position + 5,
            str(ldl_cholesterol.value) + " " + str(ldl_cholesterol.unit),
        )

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(375, y_position + 35, "3.5")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if ldl_cholesterol.value <= 3.5:
            c.circle(320, y_position + 17, 11, fill=1)
        else:
            c.circle(450, y_position + 17, 11, fill=1)
        y_position -= 53

    # HDL Cholesterol
    hdl_cholesterol = get_bio_marker_from_group(results, "hdlCholesterol")
    if hdl_cholesterol is not None:
        hdl_bar = convert_png_to_white_bg("female_report/short_report/ANO_bar.png")
        c.drawImage(
            hdl_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "HDL")
        c.drawString(
            116,
            y_position + 5,
            str(hdl_cholesterol.value) + " " + str(hdl_cholesterol.unit),
        )

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "1.3")
        c.drawString(433, y_position + 35, "2.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if hdl_cholesterol.value < 1.3:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 1 <= hdl_cholesterol.value < 2:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # non-HDL Cholesterol
    non_hdl = get_bio_marker_from_group(results, "nonHdlCholesterol")
    if non_hdl is not None:
        nonhdl_bar = convert_png_to_white_bg("female_report/short_report/ONA_bar.png")
        c.drawImage(
            nonhdl_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "non-HDL")
        c.drawString(116, y_position + 5, str(non_hdl.value) + " " + str(non_hdl.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "3.5")
        c.drawString(433, y_position + 35, "4.2")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if non_hdl.value <= 3.5:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 3.5 < non_hdl.value <= 4.2:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Triglycerides
    triglycerides = get_bio_marker_from_group(results, "triglyceride")
    if triglycerides is not None:
        triglycerides_bar = convert_png_to_white_bg(
            "female_report/short_report/ONA_bar.png"
        )
        c.drawImage(
            triglycerides_bar,
            70,
            y_position,
            width=480,
            height=35,
            preserveAspectRatio=False,
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Triglycerides")
        c.drawString(
            116,
            y_position + 5,
            str(triglycerides.value) + " " + str(triglycerides.unit),
        )

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "1")
        c.drawString(433, y_position + 35, "1.7")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if triglycerides.value <= 1:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 1 < triglycerides.value <= 1.7:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)
        y_position -= 53

    # Cholesterol to HDL Ratio
    choHDL = get_bio_marker_from_group(results, "cholesterolToHdlRatio")
    if choHDL is not None:
        cholHDL_bar = convert_png_to_white_bg("female_report/short_report/ONA_bar.png")
        c.drawImage(
            cholHDL_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False
        )
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Chol-HDL Ratio")
        c.drawString(116, y_position + 5, str(choHDL.value) + " " + str(choHDL.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(328, y_position + 35, "3.0")
        c.drawString(433, y_position + 35, "6.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if choHDL.value <= 3:
            c.circle(280, y_position + 17, 11, fill=1)
        elif 3.5 < choHDL.value <= 6.0:
            c.circle(380, y_position + 17, 11, fill=1)
        else:
            c.circle(480, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_1()
