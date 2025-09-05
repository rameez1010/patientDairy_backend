import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from male_report.gene_report.parse_gene_data import get_gene_data


def page_6_g(results):
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

    # Gene PSRC1
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 700, "PSRC1 ")

    # Gene details: PSRC1
    text1 = """
    The PSRC1 (Proline/Serine-Rich Coiled-Coil 1) gene has been studied for its role in lipid
      metabolism and cardiovascular disease.
    """

    text_object = c.beginText(80, 680)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: PSRC1
    PSRC1 = get_gene_data(results, "PSRC1")
    # print(PSRC1)

    if PSRC1 == "AA":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, PSRC1)

        # Result Description
        result = """
        According to your genetic profile your body is associated with higher LDL-C levels, potentially 
        increasing risk of coronary artery disease (CAD).
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif PSRC1 == "AG":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, PSRC1)

        # Result Description
        result = """
        According to your genetic profile your body Associated with moderate risk of
          coronary artery disease (CAD)
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif PSRC1 == "GG":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 600, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 611, PSRC1)

        # Result Description
        result = """
        Your genetic profile shows protective and Associted with lower levels of LDL cholesterol (LDL-C),
          which reduce the risk of coronary artery disease (CAD).
        """
        text_object = c.beginText(120, 634)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene SLCO1B1
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 550, "SLCO1B1")

    # Gene details: SLCO1B1
    text1 = """
    Your SLCO1B1 gene is primarily responsible for controling statin metabolism.
    The use of statins blocks cholesterol production.
    """

    text_object = c.beginText(80, 530)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: SLCO1B1
    SLCO1B1 = get_gene_data(results, "SLCO1B1")
    # print(SLCO1B1)

    if SLCO1B1 == "CC":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, SLCO1B1)

        # Result Description
        result = """
        Your genetic profile shows decreased ability to clear statins from the bloodstream, increasing 
        the risk of statin-induced muscle toxicity and increased risk of myopathy.
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif SLCO1B1 == "CT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, SLCO1B1)

        # Result Description
        result = """
        Your genetic profile shows moderate ability to clear statins from the bloodstream with a risk of
          myopathy a disease that affects the muscles that control voluntary movement in the body.
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif SLCO1B1 == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 450, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(92, 460, SLCO1B1)

        # Result Description
        result = """
        Your genetic profile shows Normal  ability to clear statins from the bloodstream 
        with no side effects.
        """
        text_object = c.beginText(120, 485)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene APOE_rs7412
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 405, "APOE_rs7412")

    # Gene details: APOE_rs7412
    text1 = """
    The APOE_rs7412 gene, essential for lipid metabolism and transport. When not optimal can lead to faster
      cholesterol buildup and higher levels in the bloodstream. Increasing your risk of high cholesterol.
    """

    text_object = c.beginText(80, 385)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: APOE_rs7412
    APOE_rs7412 = get_gene_data(results, "APOE", "rs7412")
    # print(APOE_rs7412)

    if APOE_rs7412 == "CC":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, APOE_rs7412)

        # Result Description
        result = """
        According to your genetic profile you are associated with a higher risk of Hypercholesterolemia 
        ( High Cholesterol) and triglycerides  leading to the risk of risk of coronary artery disease (CAD).
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif APOE_rs7412 == "CT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, APOE_rs7412)

        # Result Description
        result = """
        According to your genetic profile you are Associated with moderate risk of of Hypercholesterolemia 
        ( High Cholesterol) and triglycerides and moderate risk of coronary artery disease (CAD).
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif APOE_rs7412 == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 305, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 315, APOE_rs7412)

        # Result Description
        result = """
        According to your genetic profile you are associated with a lower risk of Hypercholesterolemia 
        (High Cholesterol) and triglycerides and lower risk of coronary artery disease (CAD).
        """
        text_object = c.beginText(120, 339)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    # Gene APOE_rs429358
    c.setFillColor("#BF7BD3")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(80, 255, "APOE_rs429358")

    # Gene details: APOE_rs429358
    text1 = """
    The APOE_rs429358 gene, essential for lipid metabolism and transport. When not optimal can lead to faster
      cholesterol buildup and higher levels in the bloodstream. Increasing your risk of high cholesterol.
    """

    text_object = c.beginText(80, 235)
    text_object.setFont("Helvetica", 10)
    text_object.setFillColor("black")
    text_object.setWordSpace(1.5)
    text_object.setLeading(14)

    for line in text1.split("\n"):
        text_object.textLine(line.strip())

    c.drawText(text_object)

    # Gene Results: APOE_rs429358
    APOE_rs429358 = get_gene_data(results, "APOE", "rs429358")
    # print(APOE_rs429358)

    if APOE_rs429358 == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, APOE_rs429358)

        # Result Description
        result = """
        According to your genetic profile you are associated with a higher risk of Hypercholesterolemia 
        ( High Cholesterol) and triglycerides leading to the risk of risk of coronary artery disease (CAD).
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif APOE_rs429358 == "CT":
        # For Backgroud Rectangle
        c.setStrokeColor("#ff9f1c")
        c.setFillColor("#ff9f1c")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, APOE_rs429358)

        # Result Description
        result = """
        According to your genetic profile you are Associated with moderate risk of of Hypercholesterolemia 
        ( High Cholesterol) and triglycerides and moderate risk of coronary artery disease (CAD).
        """
        text_object = c.beginText(120, 190)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor("black")
        text_object.setWordSpace(1.5)
        text_object.setLeading(14)

        for line in result.split("\n"):
            text_object.textLine(line.strip())

        c.drawText(text_object)

    elif APOE_rs429358 == "TT":
        # For Backgroud Rectangle
        c.setStrokeColor("#BF7BD3")
        c.setFillColor("#BF7BD3")
        c.rect(80, 155, 30, 30, fill=1)

        # Results AC, GG or AG
        c.setFillColor("white")
        c.setFont("Helvetica", 10)
        c.drawString(88, 165, APOE_rs429358)

        # Result Description
        result = """
        According to your genetic profile you are associated with a lower risk of Hypercholesterolemia 
        (High Cholesterol) and triglycerides and lower risk of coronary artery disease (CAD).
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
    c.drawString(80, 50, "Page - 6")

    c.showPage()
    c.save()

    buffer.seek(0)

    return buffer
