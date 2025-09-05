import io

from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data

yellow = "male_report/gene_report/yellow.png"
purple = "male_report/gene_report/purple.png"


def convert_png_to_white_bg(image_path):
    img = Image.open(image_path)
    # Create a new image with a white background
    new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    new_img.paste(img, (0, 0), img)
    # Save it as a new PNG
    new_image_path = image_path.replace(".png", "_white_bg.png")
    new_img.convert("RGB").save(new_image_path, "PNG")
    return new_image_path


def page_1_g(results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    # with open("male_report/results_g.json", "r") as file:
    #     results = json.load(file)
    # c = canvas.Canvas("male_report/page_1_g.pdf", pagesize=letter)

    c.setStrokeColor("black")
    c.setLineWidth(0.5)
    c.line(80, 750, 537, 750)

    c.setFont("Helvetica", 7)
    full_name = f"{results.get('firstName', '')} {results.get('lastName', '')}"
    c.drawString(80, 730, full_name)
    c.drawString(500, 730, "YEAR 2025")

    # Gene CYP2R1
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "CYP2R1")

    # For Backgroud Rectangle
    c.setStrokeColor("#BF7BD3")
    c.setFillColor("#BF7BD3")
    c.rect(15, 600, 40, 150, fill=1)

    # Gene CYP2R1
    c.setFillColor("white")
    c.setFont("Helvetica", 12)
    c.saveState()
    c.rotate(90)
    c.drawString(615, -40, "Genes : Vitamin D")
    c.restoreState()

    # Gene details: CYP2R1
    text1 = """
    Your CYP2R1 gene plays a central role in converting the D3 that your skin makes (or that you take
    as a supplement) into the activated hormone, 1,25 dihydroxy calciferol.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: CYP2R1
    CYP2R1 = get_gene_data(results, "CYP2R1")
    # print(CYP2R1)

    if CYP2R1 == "AG" or CYP2R1 == "GG":
        # For Backgroud Rectangle
        c.drawImage(
            convert_png_to_white_bg(yellow),
            80,
            600,
            width=35,
            height=35,
            preserveAspectRatio=False,
        )

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 615, CYP2R1)

        # Result Description
        result = """
        According to your genetic profile you tend to have lower vitamin D levels - associated 
        with lower circulating levels of 25(OH)D. You may have a higher risk of vitamin D deficiency.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP2R1 == "AA":
        # For Backgroud Rectangle
        c.drawImage(
            convert_png_to_white_bg(purple),
            80,
            600,
            width=35,
            height=35,
            preserveAspectRatio=False,
        )

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 615, CYP2R1)

        # Result Description
        result = """
        According to your genetic profile you tend to have higher vitamin D levels - associated 
        with normal or higer levels of 25-hydroxyvitamin D (25(OH)D).
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene VDR
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 550, "VDR")

    # Gene details: VDR
    text1 = """
    The VDR gene provides instructions for making a protein called vitamin D receptor (VDR).
    """

    text_object = c.beginText(80, 530)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: VDR
    VDR = get_gene_data(results, "VDR")
    # print(VDR)

    if VDR == "CT" or VDR == "TT":
        # For Backgroud Rectangle
        c.drawImage(
            convert_png_to_white_bg(yellow),
            80,
            465,
            width=35,
            height=35,
            preserveAspectRatio=False,
        )

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 478, VDR)

        # Result Description
        result = """
        According to your genetic profile due to the removal of three amino acids at the N-terminus.
        Produces a shorter version of the VDR protein. You may have a higher risk.
        """
        text_object = c.beginText(120, 500)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif VDR == "CC":
        # For Backgroud Rectangle
        c.drawImage(
            convert_png_to_white_bg(purple),
            80,
            465,
            width=35,
            height=35,
            preserveAspectRatio=False,
        )

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 478, VDR)

        # Result Description
        result = """
        According to your genetic profile your body Produces the full-length version of the VDR protein.
        You may not be at Risk.
        """
        text_object = c.beginText(120, 500)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Page Number and Logo
    c.setFont("Helvetica", 7)
    c.setFillColor("black")
    c.drawString(80, 50, "Page - 1")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
