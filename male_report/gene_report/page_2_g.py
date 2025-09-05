import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data

yellow = "male_report/gene_report/yellow_white_bg.png"
purple = "male_report/gene_report/purple_white_bg.png"


def page_2_g(results):
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

    # For Backgroud Rectangle
    c.setStrokeColor("#BF7BD3")
    c.setFillColor("#BF7BD3")
    c.rect(15, 600, 40, 150, fill=1)

    # Panel Name
    c.setFillColor("white")
    c.setFont("Helvetica", 12)
    c.saveState()
    c.rotate(90)
    c.drawString(615, -40, "Genes : Serum Glucose")
    c.restoreState()

    # Gene TCF7L2_rs7903146
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "TCF7L2_rs7903146")

    # Gene details: TCF7L2
    text1 = """
    Your TCF7L2_rs7903146 gene encodes an instruction that allows insulin to efficiently perform its 
    role as one of the most important tuners.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: TCF7L2
    TCF7L2_rs7903146 = get_gene_data(results, "TCF7L2", "rs7903146")
    # print(TCF7L2)

    if TCF7L2_rs7903146 == "CT":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 600, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 614, TCF7L2_rs7903146)

        # Result Description
        result = """
        According to your genetic profile you are at 1.4x Increased risk of Type 2 Diabetes,
          Impaired insulin secretion and Increased hepatic glucose production.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif TCF7L2_rs7903146 == "TT":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 600, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 614, TCF7L2_rs7903146)

        # Result Description
        result = """
        According to your genetic profile you are at 2x Increased risk of Type 2 Diabetes,
          Impaired insulin secretion and Increased hepatic glucose production.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif TCF7L2_rs7903146 == "CC":
        # For Backgroud Rectangle
        c.drawImage(purple, 80, 600, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 614, TCF7L2_rs7903146)

        # Result Description
        result = """
        According to your genetic profile you are at Normal (lower) risk  of Type 2 Diabetes,
          Impaired insulin secretion and Increased hepatic glucose production.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene TCF7L2_rs12255372
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 550, "TCF7L2_rs12255372")

    # Gene details: TCF7L2_rs12255372
    text1 = """
    Your TCF7L2_rs12255372 gene encodes an instruction that allows insulin to efficiently perform
      its role as one of the most important tuners.
    """

    text_object = c.beginText(80, 530)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: TCF7L2_rs12255372
    TCF7L2_rs12255372 = get_gene_data(results, "TCF7L2", "rs12255372")
    # print(TCF7L2_rs12255372)

    if TCF7L2_rs12255372 == "GT":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 445, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(90, 459, TCF7L2_rs12255372)

        # Result Description
        result = """
        According to your genetic profile you are associated with suboptimal insulin response
          and increased risk of Type II diabetes.
        """
        text_object = c.beginText(120, 480)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif TCF7L2_rs12255372 == "TT":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 445, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(90, 459, TCF7L2_rs12255372)

        # Result Description
        result = """
        According to your genetic profile you are associated with suboptimal insulin response
          and increased risk of Type II diabetes.
        """
        text_object = c.beginText(120, 480)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif TCF7L2_rs12255372 == "GG":
        # For Backgroud Rectangle
        c.drawImage(purple, 80, 445, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(90, 459, TCF7L2_rs12255372)

        # Result Description
        result = """
        According to your genetic profile you are associated with optimal insulin response
          and reduced risk of Type II diabetes.
        """
        text_object = c.beginText(120, 480)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene MTNR1B
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 395, "MTNR1B")

    # Gene details: MTNR1B
    text1 = """
    Your MTNR1B gene encodes an instruction that is needed for your cells to respond to melatonin
    so that melatonin can perform the above-mentioned important jobs.
    """

    text_object = c.beginText(80, 375)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: MTNR1B
    MTNR1B = get_gene_data(results, "MTNR1B")
    # print(MTNR1B)

    if MTNR1B == "CG" or MTNR1B == "GG":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 293, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(90, 308, MTNR1B)

        # Result Description
        result = """
        According to your genetic profile you are at increased risk for Type-2 diabetes and 
        Gestational Diabetes.
        """
        text_object = c.beginText(120, 329)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif MTNR1B == "CC":
        # For Backgroud Rectangle
        c.drawImage(purple, 80, 293, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(90, 308, MTNR1B)

        # Result Description
        result = """
        According to your genetic profile you are at Normal (lower) risk for Type-2 diabetes and 
        Gestational Diabetes.
        """
        text_object = c.beginText(120, 329)
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
    c.drawString(80, 50, "Page - 2")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
