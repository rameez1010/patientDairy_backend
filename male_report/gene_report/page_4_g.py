import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data


def page_4_g(results):
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
    c.drawString(615, -40, "Genes : Sex Hormones")
    c.restoreState()

    # Gene GSTP1
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "GSTP1")

    # Gene details: GSTP1
    text1 = """
    Your GSTP1 gene it is primarily responsible for metabolizing your estrogens (both estradiol
      and estrone) into the more toxic/inflammatory 4OHE metabolite.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: GSTP1
    GSTP1 = get_gene_data(results, "GSTP1")
    # print(GSTP1)

    if GSTP1 == "AG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, GSTP1)

        # Result Description
        result = """
        According to your genetic profile you are associated with sub-optimal enzyme function
          and suboptimal clearance of substrates and reactive oxygen species.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif GSTP1 == "AA":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, GSTP1)

        # Result Description
        result = """
        According to your genetic profile you body is associated with optimal enzyme function
          and optimal clearance of substrates and reactive oxygen species.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif GSTP1 == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, GSTP1)

        # Result Description
        result = """
        G allele (Val variant): Associated with lowest GSTP1 activity, reduced detoxification
          of carcinogens, and increased risk of cancers like lung, breast, and colorectal.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene GSTM1
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 550, "GSTM1")

    # Gene details: GSTM1
    text1 = """
    Your GSTM1 gene it is primarily responsible for metabolizing your estrogens (both estradiol
      and estrone) into the more toxic/inflammatory 4OHE metabolite.
    """

    text_object = c.beginText(80, 530)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: GSTM1
    GSTM1 = get_gene_data(results, "GSTM1")
    # print(GSTM1)

    if GSTM1 == "0":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, GSTM1)

        # Result Description
        result = """
        Associated with no enzyme production and poor clearance of substrates with decreased
          ability to detoxify environmental xenobiotics, pharmaceutics and Reactive oxygen species (ROS).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    if GSTM1 == "1":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, GSTM1)

        # Result Description
        result = """
        Associated with average enzyme function and clearance of substrates with average ability
          to detoxify environmental xenobiotics, pharmaceutics and Reactive oxygen species (ROS).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif GSTM1 == "2":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, GSTM1)

        # Result Description
        result = """
        Associated with increased enzyme function and clearance of substrates with increased ability
          to detoxify environmental xenobiotics, pharmaceutics and Reactive oxygen species (ROS).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene CYP17A1
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 405, "CYP17A1")

    # Gene details: CYP17A1
    text1 = """
    Your CYP17A1 gene is responsible for the important initial conversion of progesterone into
    testosterone (your main androgen).
    """

    text_object = c.beginText(80, 385)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: CYP17A1
    CYP17A1 = get_gene_data(results, "CYP17A1")
    # print(CYP17A1)

    if CYP17A1 == "CC":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, CYP17A1)

        # Result Description
        result = """
        Associated with increased CYP17A1 activity, leading to higher enzyme levels and altered
          steroid hormones. Linked to prostate cancer risk, PCOS, and endometriosis due to hormonal changes.
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP17A1 == "CT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, CYP17A1)

        # Result Description
        result = """
        Common and reflects genetic variability. Moderate impact on enzyme activity,
          Moderate steroid hormone production.
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP17A1 == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, CYP17A1)

        # Result Description
        result = """
        Considered the "normal" or less risk-associated with hormone-related conditions
          and Normal steroid hormone production.
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene SRD5A2
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 255, "SRD5A2")

    # Gene details: SRD5A2
    text1 = """
    Your SRD5A2 gene is responsible for the conversion of your testosterone into 
    dihydrotestosterone (DHT).
    """

    text_object = c.beginText(80, 235)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: SRD5A2
    SRD5A2 = get_gene_data(results, "SRD5A2")
    # print(SRD5A2)

    if SRD5A2 == "CC":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, SRD5A2)

        # Result Description
        result = """
        Associated with reduced enzyme activity and reduced conversion of testosterone
          into dihydrotestosterone DHT, minimizing risk associated with high DHT levels.
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif SRD5A2 == "CG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, SRD5A2)

        # Result Description
        result = """
        Associated with moderate enzyme activity and moderate conversion of testosterone
          to DHT, with potential risk associated with high DHT levels.
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif SRD5A2 == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, SRD5A2)

        # Result Description
        result = """
        Associated to moderate enzyme activity and testosterone-to-DHT conversion, potentially
          increasing the risk of androgen-dependent conditions like prostate and ovarian cancer.
        """
        text_object = c.beginText(120, 190)
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
    c.drawString(80, 50, "Page - 4")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
