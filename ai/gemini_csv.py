import vertexai
from vertexai.generative_models import GenerativeModel, Part
from config.env_config import settings

project_id = settings.GCP_PROJECT_ID
location = settings.GCP_LOCATION

vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-2.0-flash-001")


def csv_to_bytes(csv_path):
    with open(csv_path, "rb") as csv_file:
        csv_bytes = csv_file.read()
    return csv_bytes


prompt = """You are a csv entity extraction specialist. Given a csv file of gene results, your task is to extract the text value of the results of the following entities:
{
    "CYP2R1": "",
    "VDR": "",
    "TCF7L2_rs7903146": "",
    "TCF7L2_rs12255372": "",
    "MTNR1B": "",
    "DIO2": "",
    "CYP17A1": "",
    "SRD5A2": "",
    "UGT2B15": "",
    "CYP19A1": "",
    "COMT": "",
    "CYP1A1": "",
    "CYP1B1": "",
    "GSTT1": "",
    "GSTP1": "",
    "GSTM1": "",
    "PSRC1": "",
    "SLCO1B1": "",
    "APOE_rs7412": "",
    "APOE_rs429358": "",
    "MLXIPL": "",
    "9P21_rs10757278": "",
    "9P21_rs10757274": "",
    "9P21_rs4977574": "",
    "PCSK9": "",
    "TMPRSS2": "",
    "CDKN2A": "",
    "PPARG": "",
    "MTHFR_rs1801133": "",
    "MTHFR_rs1801131": "",
    "SOD2": "",
    "GPx": "",
    "FOXO3": "",
    "SIRT1": "",
    "CYP1A2": "",
    "HTR2A": "",
    "UGT2B17": "",
    "CYP3A4": "",
    "MAOA": "",
    "DRD2": "",
    "ADRA2B": "",
    "SLC6A4": "",
    "TPH2": "",
    "OPRM1": "",
    "BDNF": "",
    "CLOCK": ""
}


- The JSON schema must be followed during the extraction.
- The values must only include text found in the csv file
- Do not normalize any entity value.
- If an entity is not found in the document, set the entity value to null.
"""


def gemini_csv_extractor(file_content: bytes):
    csv_file = Part.from_data(data=file_content, mime_type="text/csv")
    contents = [csv_file, prompt]

    response = model.generate_content(contents)
    return response.text
