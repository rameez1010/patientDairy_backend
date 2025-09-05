import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data


def page_7_g(results):
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
    c.drawString(615, -40, "Genes : Lipids")
    c.restoreState()

    # Gene MLXIPL
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "MLXIPL ")

    # Gene details: MLXIPL
    text1 = """
    MLXIPL encodes a transcription factor that regulates glucose and lipid metabolism, activating in response
      to glucose metabolites to control genes involved in glycolysis, fat storage, and fatty acid synthesis.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: MLXIPL
    MLXIPL = get_gene_data(results, "MLXIPL")
    # print(MLXIPL)

    if MLXIPL == "CC":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, MLXIPL)

        # Result Description
        result = """
        According to your genetic profile your body is Associated with Higher triglyceride levels, 
        Lower HDL cholesterol, Increased risk of metabolic syndrome.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif MLXIPL == "CG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, MLXIPL)

        # Result Description
        result = """
        According to your genetic profile your body is associated with moderate triglyceride levels,
          Lower HDL cholesterol, moderate  risk of metabolic syndrome.
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif MLXIPL == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, MLXIPL)

        # Result Description
        result = """
        Your genetic profile shows protective and Associated with Most protective genotype, Lower
          triglyceride levels, Higher HDL cholesterol, Reduced risk of metabolic syndrome.
        """
        text_object = c.beginText(120, 634)
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
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, "N/A")

        # Result Description
        result = """
        Not Reported!
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene 9P21_rs10757278
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 550, "9P21_rs10757278")

    # Gene details: 9P21_rs10757278
    text1 = """
    The 9p21 locus is the most recognized genetic risk factor for coronary heart disease, identified through
      genome-wide association studies of first CHD events.
    """

    text_object = c.beginText(80, 530)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: 9P21_rs10757278
    P21_rs10757278 = get_gene_data(results, "NineP21", "rs10757278")
    # print(9P21_rs10757278)

    if P21_rs10757278 == "CC":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, P21_rs10757278)

        # Result Description
        result = """
        Your genetic profile shows you are associated with increased risk of coronary artery disease
          and ischemic stroke (vascular endothelial dysfunction ).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif P21_rs10757278 == "CT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, P21_rs10757278)

        # Result Description
        result = """
        Your genetic profile shows you are associated with moderately increased risk of coronary 
        artery disease and ischemic stroke (vascular endothelial dysfunction ).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif P21_rs10757278 == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, P21_rs10757278)

        # Result Description
        result = """
        Your genetic profile shows you are ssociated with lowest risk of coronary artery disease 
        and ischemic stroke (vascular endothelial dysfunction ).
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene PCSK9
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 405, "PCSK9")

    # Gene details: PCSK9
    text1 = """
    The PCSK9 gene encodes a protein that plays a crucial role in regulating low-density lipoprotein
      cholesterol (LDL-C) levels in the bloodstream.
    """

    text_object = c.beginText(80, 385)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: PCSK9
    PCSK9 = get_gene_data(results, "PCSK9")
    # print(PCSK9)

    if PCSK9 == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, PCSK9)

        # Result Description
        result = """
        You have the Common genotype. Offers no additional protection against cardiovascular disease
          have average LDL cholesterol levels and thus carry the typical risk seen in the general population.
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif PCSK9 == "GT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, PCSK9)

        # Result Description
        result = """
        According to your genetic profile you are Associated leads to moderate LDL cholesterol levels, which
          significantly reduces the risk of cardiovascular events (e.g., heart attack, stroke).
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif PCSK9 == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, PCSK9)

        # Result Description
        result = """
        According to your genetic profile you are associated with lower LDL cholesterol levels, which 
        significantly reduces the risk of cardiovascular events (e.g., heart attack, stroke).
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene 9P21_rs10757274
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 255, "9P21_rs10757274")

    # Gene details: 9P21_rs10757274
    text1 = """
    The 9p21 locus is the most recognized genetic risk factor for coronary heart disease, identified through
      genome-wide association studies of first CHD events.
    """

    text_object = c.beginText(80, 235)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: P21_rs10757274
    P21_rs10757274 = get_gene_data(results, "NineP21", "rs10757274")
    # print(P21_rs10757274)

    if P21_rs10757274 == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, P21_rs10757274)

        # Result Description
        result = """
        Your genetic profile shows you are associated with increased risk of coronary artery disease
          and ischemic stroke (vascular endothelial dysfunction ).
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif P21_rs10757274 == "AG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, P21_rs10757274)

        # Result Description
        result = """
        Your genetic profile shows you are associated with moderately increased risk of coronary 
        artery disease and ischemic stroke (vascular endothelial dysfunction ).
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif P21_rs10757274 == "AA":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, P21_rs10757274)

        # Result Description
        result = """
        Your genetic profile shows you are ssociated with lowest risk of coronary artery disease 
        and ischemic stroke (vascular endothelial dysfunction ).
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
    c.drawString(80, 50, "Page - 7")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
