import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data


def page_9_g(results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    # with open("male_report/results_g.json", "r") as file:
    #     results = json.load(file)
    # c = canvas.Canvas("male_report/page_4_g.pdf", pagesize=letter)

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
    c.drawString(615, -40, "Genes : CBC")
    c.restoreState()

    # Gene TMPRSS2
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "TMPRSS2 ")

    # Gene details: TMPRSS2
    text1 = """
    TThe TMPRSS2 gene encodes a serine protease involved in the activation of certain viral proteins,
      including the spike protein of SARS-CoV-2, the virus responsible for COVID-19.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: TMPRSS2
    TMPRSS2 = get_gene_data(results, "TMPRSS2")
    # print(TMPRSS2)

    if TMPRSS2 == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, TMPRSS2)

        # Result Description
        result = """
        According to your genetic profile your body is Strongly associated with increased susceptibility to
          severe respiratory infections such as  COVID-19 infection.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif TMPRSS2 == "AG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, TMPRSS2)

        # Result Description
        result = """
        According to your genetic profile your body may confer moderate susceptibility
          to severe respiratory infections.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif TMPRSS2 == "AA":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, TMPRSS2)

        # Result Description
        result = """
        Your genetic profile shows reduced susceptibility to severe respiratory
          infections such as COVID-19 infection.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene CDKN2A
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 550, "CDKN2A")

    # Gene details: CDKN2A
    text1 = """
    The CDKN2A gene is linked to cardiovascular diseases like coronary artery disease (CAD) and is also
      associated with cancer susceptibility, as well as abdominal aortic and brain aneurysms.
    """

    text_object = c.beginText(80, 530)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: CDKN2A
    CDKN2A = get_gene_data(results, "CDKN2A")
    # print(CDKN2A)

    if CDKN2A == "CC":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, CDKN2A)

        # Result Description
        result = """
        Your genetic profile shows you are associated with a higher risk of CAD and ischemic stroke
          (vascular endothelial dysfunction ).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CDKN2A == "CT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, CDKN2A)

        # Result Description
        result = """
        Your genetic profile shows you are associated with moderate  risk of coronary artery disease (CAD)
          and ischemic stroke  (vascular endothelial dysfunction).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CDKN2A == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, CDKN2A)

        # Result Description
        result = """
        Your genetic profile shows you are associated with a lower risk of coronary artery disease (CAD)
          and ischemic stroke  (vascular endothelial dysfunction).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    else:
        # For Backgroud Rectangle
        c.setStrokeColor("#7d8597")
        c.setFillColor("#7d8597")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, "N/A")

        # Result Description
        result = """
        Not Reported!
        """
        text_object = c.beginText(120, 485)
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
    c.drawString(80, 50, "Page - 9")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
