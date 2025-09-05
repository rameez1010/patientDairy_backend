import vertexai
from vertexai.generative_models import GenerativeModel, Part
from config.env_config import settings

project_id = settings.GCP_PROJECT_ID
location = settings.GCP_LOCATION

vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-2.0-flash-001")


def pdf_to_bytes(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    return pdf_bytes


prompt = """You are a document entity extraction specialist. Given a document of lab results, your task is to extract the text value of the following entities:
{
    "patient": "",
    "sex": "",
    "age": "",
    "collection_date": "",
    "date_of_birth": "",
    "cholesterol": {
        "number": "",
        "unit": ""
    },
    "triglycerides": {
        "number": "",
        "unit": ""
    },
    "hdl_cholesterol": {
        "number": "",
        "unit": ""
    },
    "ldl_cholesterol": {
        "number": "",
        "unit": ""
    },
    "non_hdl_cholesterol": {
        "number": "",
        "unit": ""
    },
    "cholesterol_to_hdl_ratio": {
        "number": "",
        "unit": ""
    },
    "hemoglobin_a1c_hba1c": {
        "number": "",
        "unit": ""
    },
    "Creatinine": {
        "number": "",
        "unit": ""
    },
    "Glomerular_Filtration_Rate_eGFR": {
        "number": "",
        "unit": ""
    },
    "Sodium": {
        "number": "",
        "unit": ""
    },
    "Potassium": {
        "number": "",
        "unit": ""
    },
    "Phosphorus": {
        "number": "",
        "unit": ""
    },
    "Total_Bilirubin": {
        "number": "",
        "unit": ""
    },
    "Calcium": {
        "number": "",
        "unit": ""
    },
    "Albumin": {
        "number": "",
        "unit": ""
    },
    "Sedimentation_rate_ESR": {
        "number": "",
        "unit": ""
    },
    "Vitamin_D_25_Hydroxy": {
        "number": "",
        "unit": ""
    },
    "Vitamin_B12": {
        "number": "",
        "unit": ""
    },
    "Ferritin": {
        "number": "",
        "unit": ""
    },
    "Progesterone": {
        "number": "",
        "unit": ""
    },
    "Prolactin_Total": {
        "number": "",
        "unit": ""
    },
    "Sex_Hormone_Bind_Globulin": {
        "number": "",
        "unit": ""
    },
    "Reverse_T3": {
        "number": "",
        "unit": ""
    },
    "Free_Triiodothyrodnine_T3": {
        "number": "",
        "unit": ""
    },
    "Free_Thyroxine_T4": {
        "number": "",
        "unit": ""
    },
    "Testosterone_Free": {
        "number": "",
        "unit": ""
    },
    "Follitropin_FSH": {
        "number": "",
        "unit": ""
    },
    "Lutropin_LH": {
        "number": "",
        "unit": ""
    },
    "Testosterone": {
        "number": "",
        "unit": ""
    },
    "Magnesium": {
        "number": "",
        "unit": ""
    },
    "Zinc": {
        "number": "",
        "unit": ""
    },
    "Vitamin_A": {
        "number": "",
        "unit": ""
    },
    "Cortisol_am": {
        "number": "",
        "unit": ""
    },
    "DHEA": {
        "number": "",
        "unit": ""
    },
    "Estradiol": {
        "number": "",
        "unit": ""
    },
    "Alkaline_Phosphate_ALP": {
        "number": "",
        "unit": ""
    },
    "Alanine_Transaminase_ALT": {
        "number": "",
        "unit": ""
    },
    "Aspartate_Transaminase_AST": {
        "number": "",
        "unit": ""
    },
    "Gamma_Glutamyl_Transferase_GGT": {
        "number": "",
        "unit": ""
    },
    "Thyroid_Stimulating_Hormone_TSH": {
        "number": "",
        "unit": ""
    },
    "Thyroid_Peroxidase_Antibody_TPO": {
        "number": "",
        "unit": ""
    },
    "Thyroglobulin_Antibodies_Anti_TG": {
        "number": "",
        "unit": ""
    },
    "Selenium_plasma": {
        "number": "",
        "unit": ""
    },
    "C_Reactive_Protien": {
        "number": "",
        "unit": ""
    },
    "Insulin": {
        "number": "",
        "unit": ""
    },
    "Glucose": {
        "number": "",
        "unit": ""
    },
    "Fibrinogen": {
        "number": "",
        "unit": ""
    },
    "Uric_Acid": {
        "number": "",
        "unit": ""
    },
    "Hemoglobin": {
        "number": "",
        "unit": ""
    },
    "Hematocrit": {
        "number": "",
        "unit": ""
    },
    "WBC": {
        "number": "",
        "unit": ""
    },
    "RBC": {
        "number": "",
        "unit": ""
    },
    "MCV": {
        "number": "",
        "unit": ""
    },
    "Neutrophils": {
        "number": "",
        "unit": ""
    },
    "Lymphocytes": {
        "number": "",
        "unit": ""
    },
    "Monocytes": {
        "number": "",
        "unit": ""
    },
    "Eosinophils": {
        "number": "",
        "unit": ""
    },
    "Basophils": {
        "number": "",
        "unit": ""
    },
    "MCH": {
        "number": "",
        "unit": ""
    },
    "MCHC": {
        "number": "",
        "unit": ""
    },
    "RDW": {
        "number": "",
        "unit": ""
    },
    "Platelet_Count": {
        "number": "",
        "unit": ""
    }
    "Total_PSA": {
        "number": "",
        "unit": ""
    }
}

- The JSON schema must be followed during the extraction.
- The values must only include text found in the document.
- Do not normalize any entity value.
- If an entity is not found in the document, set the entity value to null.
- Do not include < and > operators as part of the number.
- For collection_date & date_of_birth  return the date in the format of Year-Month-Day (YYYY-M-DD).
- For age, return the age in years as a number.
"""


def gemini_pdf_extractor(file_content: bytes):
    pdf_file = Part.from_data(
        data=file_content,
        mime_type="application/pdf",
    )
    contents = [pdf_file, prompt]

    response = model.generate_content(contents)
    return response.text
