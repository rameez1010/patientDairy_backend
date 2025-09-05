from typing import List, Literal, Optional

from models.patient_models import BioMarker

BiomarkerName = Literal[
    # Lipids
    "cholesterol",
    "ldlCholesterol",
    "hdlCholesterol",
    "nonHdlCholesterol",
    "triglyceride",
    "cholesterolToHdlRatio",
    # Glucose
    "hbA1c",
    "insulin",
    "glucose",
    # Renal
    "creatinine",
    "eGFR",
    # Mineral
    "calcium",
    "ferritin",
    "magnesium",
    "zinc",
    "seleniumPlasma",
    # Inflammation Markers
    "sedimentationRate",
    "cReactiveProtein",
    "fibrinogen",
    "uricAcid",
    # Vitamin
    "vitaminA",
    "vitaminB12",
    "vitaminD",
    # Electrolytes
    "sodium",
    "potassium",
    "phosphorus",
    # Liver Enzymes
    "alanineTransaminase",
    "alkalinePhosphate",
    "aspartateTransaminase",
    "albumin",
    "gammaGlutamylTransferase",
    "totalBilirubin",
    # Thyroid Functions
    "thyroidStimulatingHormone",
    "thyroidPeroxidaseAntibody",
    "thyroglobulinAntibodies",
    "reverseT3",
    "freeT3",
    "freeT4",
    # Hormone
    "follitropin",
    "lutropin",
    "estradiol",
    "progesterone",
    "testosterone",
    "testosteroneFree",
    "dhea",
    "prolactin",
    "sexHormoneBindGlobulin",
    "cortisolAm",
    # CBC
    "hemoglobin",
    "hematocrit",
    "rbc",
    "wbc",
    "neutrophils",
    "lymphocytes",
    "lonocytes",
    "eosinophils",
    "basophils",
    "mcv",
    "mch",
    "mchc",
    "rdw",
    "plateletCount",
]


def get_bio_marker_from_group(group: List[BioMarker], biomarker_name: BiomarkerName) -> Optional[BioMarker]:
    for biomarker in group:
        if biomarker.name == biomarker_name:
            return biomarker

    return None
