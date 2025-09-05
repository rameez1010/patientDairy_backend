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


def page_8(results: List[BioMarker]):
    # c = canvas.Canvas("female_report/short_report/page_8.pdf", pagesize=letter)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    bg_image_path = "female_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, "Liver")

    text1 = """
        The Liver Panel measures key markers like ALP, ALT, AST, GGT, Bilirubin, and Albumin to
          assess liver health and function. These tests help detect liver damage, inflammation,
            or disease, guiding treatment and monitoring to support optimal liver performance.
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
    c.drawString(70, 520, "Patient’s liver results")

    legend_image_path = "female_report/short_report/colors.jpg"
    c.drawImage(legend_image_path, 340, 520, width=200, height=15, preserveAspectRatio=False)

    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 505, 550, 505)

    # BioMarkers list and Bars
    y_position = 455
    # ALP
    alp = get_bio_marker_from_group(results, "alkalinePhosphate")
    if alp is not None:
        alp_bar = convert_png_to_white_bg("female_report/short_report/ANONA_bar.png")
        c.drawImage(alp_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "ALP")
        c.drawString(116, y_position + 5, str(alp.value) + " " + str(alp.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(280, y_position + 35, "35.0")
        c.drawString(346, y_position + 35, "45.0")
        c.drawString(412, y_position + 35, "100.0")
        c.drawString(476, y_position + 35, "122.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if alp.value < 35:
            c.circle(260, y_position + 17, 11, fill=1)
        elif 35 <= alp.value < 45:
            c.circle(325, y_position + 17, 11, fill=1)
        elif 45 <= alp.value <= 100:
            c.circle(390, y_position + 17, 11, fill=1)
        elif 100 < alp.value <= 122:
            c.circle(455, y_position + 17, 11, fill=1)
        else:
            c.circle(515, y_position + 17, 11, fill=1)
        y_position -= 53

    # ALT
    alt = get_bio_marker_from_group(results, "alanineTransaminase")
    if alt is not None:
        alt_bar = convert_png_to_white_bg("female_report/short_report/OA_bar.png")
        c.drawImage(alt_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "ALT")
        c.drawString(116, y_position + 5, str(alt.value) + " " + str(alt.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(375, y_position + 35, "46.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if alt.value <= 46:
            c.circle(320, y_position + 17, 11, fill=1)
        else:
            c.circle(450, y_position + 17, 11, fill=1)
        y_position -= 53

    # AST
    ast = get_bio_marker_from_group(results, "aspartateTransaminase")
    if ast is not None:
        ast_bar = convert_png_to_white_bg("female_report/short_report/NONA_bar.png")
        c.drawImage(ast_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "AST")
        c.drawString(116, y_position + 5, str(ast.value) + " " + str(ast.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "10.0")
        c.drawString(380, y_position + 35, "26.0")
        c.drawString(460, y_position + 35, "30.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if ast.value < 10:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 10 <= ast.value <= 26:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 26 < ast.value <= 30:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # GGT
    ggt = get_bio_marker_from_group(results, "gammaGlutamylTransferase")
    if ggt is not None:
        ggt_bar = convert_png_to_white_bg("female_report/short_report/NONA_bar.png")
        c.drawImage(ggt_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "GGT")
        c.drawString(116, y_position + 5, str(ggt.value) + " " + str(ggt.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "10.00")
        c.drawString(380, y_position + 35, "30.00")
        c.drawString(460, y_position + 35, "44.00")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if ggt.value < 10:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 10 <= ggt.value <= 30:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 30 < ggt.value <= 44:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)
        y_position -= 53

    # Total Bilirubin
    bilirubin = get_bio_marker_from_group(results, "totalBilirubin")
    if bilirubin is not None:
        bilirubin_bar = convert_png_to_white_bg("female_report/short_report/NONA_bar.png")
        c.drawImage(bilirubin_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Bilirubin")
        c.drawString(116, y_position + 5, str(bilirubin.value) + " " + str(bilirubin.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(300, y_position + 35, "5.0")
        c.drawString(380, y_position + 35, "15.0")
        c.drawString(460, y_position + 35, "20.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if bilirubin.value < 5:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 5 <= bilirubin.value <= 15:
            c.circle(345, y_position + 17, 11, fill=1)
        elif 15 < bilirubin.value <= 20:
            c.circle(425, y_position + 17, 11, fill=1)
        else:
            c.circle(500, y_position + 17, 11, fill=1)
        y_position -= 53

    # Albumin
    albumin = get_bio_marker_from_group(results, "albumin")
    if albumin is not None:
        albumin_bar = convert_png_to_white_bg("female_report/short_report/ANOA_bar.png")
        c.drawImage(albumin_bar, 70, y_position, width=480, height=35, preserveAspectRatio=False)
        c.setFillColor("#4b4b4b")
        c.setFont("Roboto-Regular", 11)
        c.drawString(116, y_position + 20, "Albumin")
        c.drawString(116, y_position + 5, str(albumin.value) + " " + str(albumin.unit))

        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 9)
        c.drawString(295, y_position + 35, "35.0")
        c.drawString(380, y_position + 35, "45.0")
        c.drawString(460, y_position + 35, "52.0")

        # draw circle (needle)
        c.setStrokeColor("gray")
        c.setFillColor("white")
        c.setLineWidth(3.5)

        if albumin.value < 35:
            c.circle(270, y_position + 17, 11, fill=1)
        elif 35 <= albumin.value < 45:
            c.circle(347, y_position + 17, 11, fill=1)
        elif 45 <= albumin.value <= 52:
            c.circle(430, y_position + 17, 11, fill=1)
        else:
            c.circle(510, y_position + 17, 11, fill=1)

    c.showPage()
    c.save()

    return buffer


# page_8()
