import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data


def page_12_g(results):
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
    c.drawString(615, -40, "Genes : Hormones")
    c.restoreState()

    # Gene HTR2A
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "HTR2A ")

    # Gene details: HTR2A
    text1 = """
    The HTR2A gene encodes the serotonin receptor 2A (5-HT2A), which regulates mood and is linked
      to psychiatric disorders like schizophrenia and depression.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: HTR2A
    HTR2A = get_gene_data(results, "HTR2A")
    # print(HTR2A)

    if HTR2A == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, HTR2A)

        # Result Description
        result = """
        Lower HTR2A receptor activity may increase susceptibility to psychotic or impulsive
          behaviors, as serotonin plays a key role in emotional regulation and cognitive processing.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif HTR2A == "AG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, HTR2A)

        # Result Description
        result = """
        May confer serotonin receptor activity and Intermediate risk for
          psychiatric conditions.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif HTR2A == "AA":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, HTR2A)

        # Result Description
        result = """
        Higher serotonin receptor activity may increase susceptibility to mood disorders like
          anxiety or depression, particularly in stressful environments or with other risk factors.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene UGT2B17
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 550, "UGT2B17")

    # Gene details: UGT2B17
    text1 = """
    The UGT2B17 gene encodes an enzyme in the UDP-glucuronosyltransferase (UGT) family,
      crucial for detoxifying and metabolizing steroids, drugs, and toxins.
    """

    text_object = c.beginText(80, 530)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: UGT2B17
    UGT2B17 = get_gene_data(results, "UGT2B17")
    # print(UGT2B17)

    if UGT2B17 == "0":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, UGT2B17)

        # Result Description
        result = """
        Absence of UGT2B17 leads to higher testosterone and estradiol levels and affects drug responses,
          especially for glucuronidated drugs, such as anti-cancer treatments and steroids like testosterone.
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif UGT2B17 == "1":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, UGT2B17)

        # Result Description
        result = """
        Associated with moderate enzyme activity and moderate concentrations of circulating
          testosterone and estradiol levels.
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif UGT2B17 == "2":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, UGT2B17)

        # Result Description
        result = """
        Associated with increased enzyme activity and decreased concentrations of circulating
          testosterone and estradiol levels. Associated with low BMD and increased risk for osteoporosis.
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene CYP3A4
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 405, "CYP3A4")

    # Gene details: CYP3A4
    text1 = """
    CYP3A4 is a key enzyme in the liver and intestines that metabolizes drugs (e.g., acetaminophen,
      codeine), steroids, and other substances, as part of the cytochrome P450 enzyme family.
    """

    text_object = c.beginText(80, 385)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: CYP3A4
    CYP3A4 = get_gene_data(results, "CYP3A4")
    # print(CYP3A4)

    if CYP3A4 == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, CYP3A4)

        # Result Description
        result = """
        Increased CYP3A4 activity can raise production of 16α-OH-estrogen metabolites, linked to higher
          risks of hormone-related cancers (e.g., breast, prostate, ovarian) and increased testosterone catabolism.
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP3A4 == "AA":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, CYP3A4)

        # Result Description
        result = """
        Decreased CYP3A4 activity lowers 16α-OH-estrogen metabolites and testosterone catabolism,
          but may slow drug metabolism, increasing the risk of drug toxicity.
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP3A4 == "AG":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, CYP3A4)

        # Result Description
        result = """
        Associated with increased enzyme activity, increased production of 16α-OH-estrogen
          metabolites, and increased catabolism of testosterone.
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene MAOA
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 255, "MAOA")

    # Gene details: MAOA
    text1 = """
    MAOA breaks down serotonin, epinephrine, norepinephrine, and dopamine. Serotonin affects
      mood and sleep, epinephrine/norepinephrine control stress, and dopamine enables movement.
    """

    text_object = c.beginText(80, 235)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: MAOA
    MAOA = get_gene_data(results, "MAOA")
    # print(MAOA)

    if MAOA == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, MAOA)

        # Result Description
        result = """
        Low MAO-A activity slows neurotransmitter breakdown, increasing the risk of mood disorders,
          aggression, impulsivity, and substance abuse, particularly under stress.
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif MAOA == "GT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, MAOA)

        # Result Description
        result = """
        Associated with moderate MAO activity and medial dopamine half-life, Moderate risk for
          mood disorders, aggression, or impulsivity (higher if environmental stress is present).
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif MAOA == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, MAOA)

        # Result Description
        result = """
        Associated with highest MAO activity and shortest dopamine half-life , Lower risk for
          aggression, mood disorders, or impulsivity.
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
    c.drawString(80, 50, "Page - 12")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
