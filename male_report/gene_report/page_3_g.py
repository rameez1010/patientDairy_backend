import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data

yellow = "male_report/gene_report/yellow_white_bg.png"
purple = "male_report/gene_report/purple_white_bg.png"


def page_3_g(results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    # with open("male_report/results_g.json", "r") as file:
    #     results = json.load(file)
    # c = canvas.Canvas("male_report/page_3_g.pdf", pagesize=letter)

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

    # Gene COMT
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "COMT")

    # Gene details: COMT
    text1 = """
    Your COMT gene gives your cells the instructions to make your COMT enzyme which eliminates
    your estrogen metabolites.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: COMT
    COMT = get_gene_data(results, "COMT")
    # print(COMT)

    if COMT == "TT":
        # For Backgroud Rectangle
        c.drawImage(purple, 80, 600, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 614, COMT)

        # Result Description
        result = """
        According to your genetic profile you are Associated with lowest COMT activity
          and longest dopamine half-life which could lead to Potentially better stress management.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif COMT == "CT":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 600, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 614, COMT)

        # Result Description
        result = """
        According to your genetic profile you are associated with moderate COMT
          activity and medial dopamine half-life.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif COMT == "CC":
        # For Backgroud Rectangle
        c.drawImage(purple, 80, 600, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 614, COMT)

        # Result Description
        result = """
        According to your genetic profile your body is Associated with lowest COMT activity
          and longest dopamine half-life which could lead to Potentially better stress management.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene CYP1A1
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 550, "CYP1A1")

    # Gene details: CYP1A1
    text1 = """
    Your CYP1A1 gene encodes the instruction for one of the most important metabolizers 
    of both estradiol and estrone.
    """

    text_object = c.beginText(80, 530)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: CYP1A1
    CYP1A1 = get_gene_data(results, "CYP1A1")
    # print(CYP1A1)

    if CYP1A1 == "CC":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 445, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 459, CYP1A1)

        # Result Description
        result = """
        Associated to higher enzyme activity, increased 2-OH-estrogen metabolites, and greater enzyme
          inducibility in response to toxins, raising the risk of toxic intermediates and ROS accumulation.

        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP1A1 == "CT":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 445, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 459, CYP1A1)

        # Result Description
        result = """
        Associated to moderate enzyme activity, increased 2-OH-estrogen metabolites, and higher
          enzyme inducibility, raising the risk of toxic intermediates and ROS.
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP1A1 == "TT":
        # For Backgroud Rectangle
        c.drawImage(purple, 80, 445, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 459, CYP1A1)

        # Result Description
        result = """
        Linked to lower enzyme activity, reduced 2-OH-estrogen metabolites, and decreased enzyme
          inducibility, lowering the risk of toxic intermediates and ROS.
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene CYP1B1
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 405, "CYP1B1")

    # Gene details: CYP1B1
    text1 = """
    Your CYP1B1 gene is primarily responsible for metabolizing your estrogens (both estradiol
      and estrone) into the more toxic/inflammatory 4OHE metabolite.
    """

    text_object = c.beginText(80, 385)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: CYP1B1
    CYP1B1 = get_gene_data(results, "CYP1B1")
    # print(CYP1B1)

    if CYP1B1 == "CC":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 293, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 308, CYP1B1)

        # Result Description
        result = """
        According to your genetic profile you are faster at metabolizing your estrogens into 
        their 4OHE metabolites. Risk of toxic 4OHE.
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP1B1 == "CG":
        # For Backgroud Rectangle
        c.drawImage(purple, 80, 293, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 308, CYP1B1)

        # Result Description
        result = """
        According to your genetic profile you are at normal for metabolizing your estrogens
          into their 4OHE metabolites
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif CYP1B1 == "GG":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 293, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 308, CYP1B1)

        # Result Description
        result = """
        According to your genetic profile your body is slower for metabolizing your estrogens
          into their 4OHE metabolites
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene UGT2B15
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 255, "UGT2B15")

    # Gene details: UGT2B15
    text1 = """
    UGT2B genes encode enzymes that make androgens more water-soluble for excretion, playing
      a key role in detoxification, regulating steroid hormones, and metabolizing drugs and toxins.
    """

    text_object = c.beginText(80, 235)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: UGT2B15
    UGT2B15 = get_gene_data(results, "UGT2B15")
    # print(UGT2B15)

    if UGT2B15 == "TT":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 155, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 169, UGT2B15)

        # Result Description
        result = """
        Associated with increased glucuronidation of androgens and androgen
          metabolites, including DHT.
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif UGT2B15 == "TG":
        # For Backgroud Rectangle
        c.drawImage(purple, 80, 155, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 169, UGT2B15)

        # Result Description
        result = """
        Associated with moderate glucuronidation of androgens and androgen metabolites,
          including DHT ,keeping a moderate balanced endrogine in your body.
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif UGT2B15 == "GG":
        # For Backgroud Rectangle
        c.drawImage(yellow, 80, 155, width=35, height=35, preserveAspectRatio=False)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(91, 169, UGT2B15)

        # Result Description
        result = """
        Associated with lower testosterone/DHT clearance and higher enzyme activity, increasing DHT
          levels, linked to male pattern baldness, BPH, and androgen-sensitive conditions.
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
    c.drawString(80, 50, "Page - 3")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
