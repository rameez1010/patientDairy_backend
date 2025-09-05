import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data


def page_5_g(results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    # with open("male_report/results_g.json", "r") as file:
    #     results = json.load(file)
    # c = canvas.Canvas("male_report/page_2_g.pdf", pagesize=letter)

    c.setStrokeColor("black")
    c.setLineWidth(0.5)
    c.line(80, 750, 537, 750)

    c.setFont("Helvetica", 7)
    full_name = f"{results.get('firstName', '')} {results.get('lastName', '')}"
    c.drawString(80, 730, full_name)
    c.drawString(500, 730, "YEAR 2025")

    # For Backgroud Rectangle
    c.setStrokeColor("#BF7BD3")
    c.setFillColor("#BF7BD3")
    c.rect(15, 600, 40, 150, fill=1)

    # Panel Name
    c.setFillColor("white")
    c.setFont("Helvetica", 12)
    c.saveState()
    c.rotate(90)
    c.drawString(615, -40, "Genes :  Thyroid function")
    c.restoreState()

    # Gene DIO2
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "DIO2")

    # Gene details: DIO2
    text1 = """
    Your TSH, or thyroid stimulating hormone, stimulates your thyroid gland to produce thyroid hormones,
      T3 and T4. Your thyroid gland function is inversely related to your TSH levels.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: DIO2
    DIO2 = get_gene_data(results, "DIO2")
    # print(DIO2)

    if DIO2 == "CC":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, DIO2)

        # Result Description
        result = """
        According to your genetic you are at 1.3-1.79x risk of osteoarthritis 
        and 3.75x bipolar.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif DIO2 == "CT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, DIO2)

        # Result Description
        result = """
        According to your genetic you are at 1.3-1.79x risk of osteoarthritis 
        and 1.6x bipolar.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif DIO2 == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, DIO2)

        # Result Description
        result = """
        According to your genetic profile you are at Normal risk common
          to most cases.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # # Gene GSTT1
    # c.setFillColor("#BF7BD3")
    # c.setFont("Helvetica-Bold", 15)
    # c.drawString(80, 255, "GSTT1")

    # # Gene details: GSTT1
    # text1 = """
    # Your GSTT1 gene is primarily responsible for metabolizing your estrogens (both estradiol and
    #   estrone) into the more toxic/inflammatory 4OHE metabolite.
    # """

    # text_object = c.beginText(80, 235)
    # text_object.setFont("Helvetica", 10)
    # text_object.setFillColor("black")
    # text_object.setWordSpace(1.5)
    # text_object.setLeading(14)

    # for line in text1.split("\n"):
    #     text_object.textLine(line.strip())

    # c.drawText(text_object)

    # # Gene Results: GSTT1
    # GSTT1 = str(results["GSTT1"])
    # # print(GSTT1)

    # if GSTT1 == "1":
    #     # For Backgroud Rectangle
    #     c.setStrokeColor("#BF7BD3")
    #     c.setFillColor("#BF7BD3")
    #     c.rect(80, 155, 30, 30, fill=1)

    #     # Results AC, GG or AG
    #     c.setFillColor("white")
    #     c.setFont("Helvetica", 10)
    #     c.drawString(92, 165, GSTT1)

    #     # Result Description
    #     result = """
    #     According to your genetic profile the GSTT1 gene is present and it is associated
    #       with normal enzyme activity.
    #     """
    #     text_object = c.beginText(120, 190)
    #     text_object.setFont("Helvetica", 10)
    #     text_object.setFillColor("black")
    #     text_object.setWordSpace(1.5)
    #     text_object.setLeading(14)

    #     for line in result.split("\n"):
    #         text_object.textLine(line.strip())

    #     c.drawText(text_object)

    # elif GSTT1 == "0":
    #     # For Backgroud Rectangle
    #     c.setStrokeColor("#ff9f1c")
    #     c.setFillColor("#ff9f1c")
    #     c.rect(80, 155, 30, 30, fill=1)

    #     # Results AC, GG or AG
    #     c.setFillColor("white")
    #     c.setFont("Helvetica", 10)
    #     c.drawString(92, 165, GSTT1)

    #     # Result Description
    #     result = """
    #     According to your genetic profile the GSTT1 gene is NOT present and you lack
    #       functional GSTT1 enzyme activity.
    #     """
    #     text_object = c.beginText(120, 190)
    #     text_object.setFont("Helvetica", 10)
    #     text_object.setFillColor("black")
    #     text_object.setWordSpace(1.5)
    #     text_object.setLeading(14)

    #     for line in result.split("\n"):
    #         text_object.textLine(line.strip())

    #     c.drawText(text_object)

    # Page Number and Logo
    c.setFont("Helvetica", 7)
    c.setFillColor("black")
    c.drawString(80, 50, "Page - 5")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
