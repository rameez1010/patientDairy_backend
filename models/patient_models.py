from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field

from datetime import datetime
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

# Define the valid biomarker groups as a type
BioMarkerGroup = Literal[
    "full",
    "lipids",
    "glucose",
    "renal",
    "mineral",
    "inflammation_Markers",
    "vitamin",
    "electrolytes",
    "liver_Enzymes",
    "thyroid_Functions",
    "hormone",
    "cbc",
]

# Define gender options
Gender = Literal["male", "female"]

class FirestoreBaseModel(BaseModel):
    def safe_dump(self, exclude_fields: set = None) -> dict:
        default_exclude = {
            "password",
            "otp_code",
            "otp_expires_at",
            "refresh_token",
            "last_activity"
        }
        exclude_fields = exclude_fields or set()
        return self.model_dump(exclude=default_exclude.union(exclude_fields))

class BloodWorkResults(BaseModel):
    cholesterol: Optional[float] = Field(None)
    ldlCholesterol: Optional[float] = Field(None)
    hdlCholesterol: Optional[float] = Field(None)
    nonHdlCholesterol: Optional[float] = Field(None)
    triglyceride: Optional[float] = Field(None)
    cholesterolToHdlRatio: Optional[float] = Field(None)
    hbA1c: Optional[float] = Field(None)
    creatinine: Optional[float] = Field(None)
    eGFR: Optional[float] = Field(None)
    sodium: Optional[float] = Field(None)
    potassium: Optional[float] = Field(None)
    phosphorus: Optional[float] = Field(None)
    totalBilirubin: Optional[float] = Field(None)
    calcium: Optional[float] = Field(None)
    albumin: Optional[float] = Field(None)
    sedimentationRate: Optional[float] = Field(None)
    vitaminD: Optional[float] = Field(None)
    vitaminB12: Optional[float] = Field(None)
    ferritin: Optional[float] = Field(None)
    progesterone: Optional[float] = Field(None)
    prolactin: Optional[float] = Field(None)
    sexHormoneBindGlobulin: Optional[float] = Field(None)
    reverseT3: Optional[float] = Field(None)
    freeT3: Optional[float] = Field(None)
    freeT4: Optional[float] = Field(None)
    testosteroneFree: Optional[float] = Field(None)
    follitropin: Optional[float] = Field(None)
    lutropin: Optional[float] = Field(None)
    testosterone: Optional[float] = Field(None)
    magnesium: Optional[float] = Field(None)
    zinc: Optional[float] = Field(None)
    vitaminA: Optional[float] = Field(None)
    cortisolAm: Optional[float] = Field(None)
    totalPsa: Optional[float] = Field(None)
    dhea: Optional[float] = Field(None)
    estradiol: Optional[float] = Field(None)
    alkalinePhosphate: Optional[float] = Field(None)
    alanineTransaminase: Optional[float] = Field(None)
    aspartateTransaminase: Optional[float] = Field(None)
    gammaGlutamylTransferase: Optional[float] = Field(None)
    thyroidStimulatingHormone: Optional[float] = Field(None)
    thyroidPeroxidaseAntibody: Optional[float] = Field(None)
    thyroglobulinAntibodies: Optional[float] = Field(None)
    seleniumPlasma: Optional[float] = Field(None)
    cReactiveProtein: Optional[float] = Field(None)
    hemoglobin: Optional[float] = Field(None)
    hematocrit: Optional[float] = Field(None)
    rbc: Optional[float] = Field(None)
    wbc: Optional[float] = Field(None)
    neutrophils: Optional[float] = Field(None)
    lymphocytes: Optional[float] = Field(None)
    lonocytes: Optional[float] = Field(None)
    eosinophils: Optional[float] = Field(None)
    basophils: Optional[float] = Field(None)
    mcv: Optional[float] = Field(None)
    mch: Optional[float] = Field(None)
    mchc: Optional[float] = Field(None)
    rdw: Optional[float] = Field(None)
    plateletCount: Optional[float] = Field(None)
    sex: Optional[str] = Field(None)
    collectionDate: Optional[str] = Field(None)
    fibrinogen: Optional[float] = Field(None)
    uricAcid: Optional[float] = Field(None)
    glucose: Optional[float] = Field(None)
    insulin: Optional[float] = Field(None)
    patient: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    age: Optional[str] = Field(None)
    dateOfBirth: Optional[str] = Field(None)
    practitioner: Optional[str] = Field(None)


# Genes Model
class GeneResults(BaseModel):
    CYP2R1: Optional[str] = Field(None, description="CYP2R1 gene result")
    VDR: Optional[str] = Field(None, description="CYP2R1 VDR result")
    TCF7L2_rs7903146: Optional[str] = Field(None, description="TCF7L2_rs7903146 gene result")
    TCF7L2_rs12255372: Optional[str] = Field(None, description="TCF7L2_rs12255372 gene result")
    MTNR1B: Optional[str] = Field(None, description="MTNR1B gene result")
    DIO2: Optional[str] = Field(None, description="DIO2 gene result")
    CYP17A1: Optional[str] = Field(None, description="CYP17A1 gene result")
    SRD5A2: Optional[str] = Field(None, description="SRD5A2 gene result")
    UGT2B15: Optional[str] = Field(None, description="UGT2B15 gene result")
    CYP19A1: Optional[str] = Field(None, description="CYP19A1 gene result")
    COMT: Optional[str] = Field(None, description="COMT gene result")
    CYP1A1: Optional[str] = Field(None, description="CYP1A1 gene result")
    CYP1B1: Optional[str] = Field(None, description="CYP1B1 gene result")
    GSTT1: Optional[str] = Field(None, description="GSTT1 gene result")
    GSTP1: Optional[str] = Field(None, description="GSTP1 gene result")
    GSTM1: Optional[str] = Field(None, description="GSTM1 gene result")
    PSRC1: Optional[str] = Field(None, description="PSRC1 gene result")
    SLCO1B1: Optional[str] = Field(None, description="SLCO1B1 gene result")
    APOE_rs7412: Optional[str] = Field(None, description="APOE_rs7412 gene result")
    APOE_rs429358: Optional[str] = Field(None, description="APOE_rs429358 gene result")
    MLXIPL: Optional[str] = Field(None, description="MLXIPL gene result")
    NineP21_rs10757278: Optional[str] = Field(None, description="NineP21_rs10757278 gene result")
    NineP21_rs10757274: Optional[str] = Field(None, description="NineP21_rs10757274 gene result")
    NineP21_rs4977574: Optional[str] = Field(None, description="NineP21_rs4977574 gene result")
    PCSK9: Optional[str] = Field(None, description="PCSK9 gene result")
    TMPRSS2: Optional[str] = Field(None, description="TMPRSS2 gene result")
    CDKN2A: Optional[str] = Field(None, description="CDKN2A gene result")
    PPARG: Optional[str] = Field(None, description="PPARG gene result")
    MTHFR_rs1801133: Optional[str] = Field(None, description="MTHFR_s1801133 gene result")
    MTHFR_rs1801131: Optional[str] = Field(None, description="MTHFR_rs1801131 gene result")
    SOD2: Optional[str] = Field(None, description="SOD2 gene result")
    GPx: Optional[str] = Field(None, description="GPx gene result")
    FOXO3: Optional[str] = Field(None, description="FOXO3 gene result")
    SIRT1: Optional[str] = Field(None, description="SIRT1 gene result")
    CYP1A2: Optional[str] = Field(None, description="CYP1A2 gene result")
    HTR2A: Optional[str] = Field(None, description="HTR2A gene result")
    UGT2B17: Optional[str] = Field(None, description="UGT2B17 gene result")
    CYP3A4: Optional[str] = Field(None, description="CYP3A4 gene result")
    MAOA: Optional[str] = Field(None, description="MAOA gene result")
    DRD2: Optional[str] = Field(None, description="DRD2 gene result")
    ADRA2B: Optional[str] = Field(None, description="ADRA2B gene result")
    SLC6A4: Optional[str] = Field(None, description="SLC6A4 gene result")
    TPH2: Optional[str] = Field(None, description="TPH2 gene result")
    OPRM1: Optional[str] = Field(None, description="OPRM1 gene result")
    BDNF: Optional[str] = Field(None, description="BDNF gene result")
    CLOCK: Optional[str] = Field(None, description="CLOCK gene result")


# Gene Results
class GeneResultEntry(BaseModel):
    results: GeneResults = Field(..., description="The gene results for this entry")
    date: datetime = Field(..., description="Date of the gene result")


class BioMarker(BaseModel):
    name: str = Field(..., description="Name of the biomarker (key)")
    title: str = Field(..., description="Human-readable title of the biomarker")
    value: Optional[float] = Field(None, description="Value of the biomarker")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    range_status: Optional[str] = Field(None, description="Range status from biomarker engine service")


class Gene(BaseModel):
    """Individual gene with its genotype and risk assessment"""

    name: str = Field(..., description="Gene name (e.g., CYP2R1, VDR)")
    genotype: Optional[str] = Field(None, description="Genotype result (e.g., AG, GG, AA)")
    risk_level: Optional[str] = Field(None, description="Risk level assessment (normal, increased)")
    rs_id: Optional[str] = Field(None, description="Reference SNP ID")
    panel: str = Field(..., description="Panel this gene belongs to")


class GenePanel(BaseModel):
    """Gene panel containing related genes"""

    panel_name: str = Field(..., description="Name of the gene panel")
    genes: List[Gene] = Field(..., description="List of genes in this panel")


class GeneResultsGrouped(BaseModel):
    """Gene results grouped by panels"""

    vitamin_d: Optional[List[Gene]] = Field(None, description="Vitamin D related genes")
    serum_glucose: Optional[List[Gene]] = Field(None, description="Serum Glucose related genes")
    sex_hormones: Optional[List[Gene]] = Field(None, description="Sex Hormones related genes")
    thyroid_function: Optional[List[Gene]] = Field(None, description="Thyroid Function related genes")
    lipids: Optional[List[Gene]] = Field(None, description="Lipids related genes")
    cbc: Optional[List[Gene]] = Field(None, description="CBC related genes")
    vitamins_b: Optional[List[Gene]] = Field(None, description="Vitamins B related genes")
    minerals_detox: Optional[List[Gene]] = Field(None, description="Minerals - Detox related genes")
    hormones: Optional[List[Gene]] = Field(None, description="Hormones related genes")

    class Config:
        """Configuration for the model"""

        arbitrary_types_allowed = True


class GeneResultReport(BaseModel):
    """Single gene result report with metadata"""

    createdAt: Optional[datetime] = Field(None, description="Creation date of the gene result report")
    reportDate: Optional[str] = Field(None, description="Collection date of the gene results")
    geneResultsGrouped: GeneResultsGrouped = Field(..., description="Grouped gene results data")
    fileHash: Optional[str] = Field(None, description="SHA-256 hash of the uploaded file for duplicate detection")
    fileName: Optional[str] = Field(None, description="Original filename of the uploaded file")


class GeneResultsGroupedUpdate(BaseModel):
    """Update model for adding grouped gene results to a patient"""

    gene_results_grouped: List[GeneResultReport] = Field(..., description="List of new grouped gene results to add")


class BloodWorkBioMarkerGroup(BaseModel):
    """Blood work biomarkers grouped by category"""

    lipids: Optional[List[BioMarker]] = Field(None, description="Lipid biomarkers group")
    glucose: Optional[List[BioMarker]] = Field(None, description="Glucose biomarkers group")
    renal: Optional[List[BioMarker]] = Field(None, description="Renal biomarkers group")
    mineral: Optional[List[BioMarker]] = Field(None, description="Mineral biomarkers group")
    inflammation_Markers: Optional[List[BioMarker]] = Field(None, description="Inflammation markers group")
    vitamin: Optional[List[BioMarker]] = Field(None, description="Vitamin biomarkers group")
    electrolytes: Optional[List[BioMarker]] = Field(None, description="Electrolytes biomarkers group")
    liver_Enzymes: Optional[List[BioMarker]] = Field(None, description="Liver enzymes biomarkers group")
    thyroid_Functions: Optional[List[BioMarker]] = Field(None, description="Thyroid functions biomarkers group")
    hormone: Optional[List[BioMarker]] = Field(None, description="Hormone biomarkers group")
    cbc: Optional[List[BioMarker]] = Field(None, description="Complete blood count biomarkers group")

    class Config:
        """Configuration for the model"""

        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "lipids": {
                    "cholesterol": {
                        "name": "cholesterol",
                        "title": "Total Cholesterol",
                        "value": 200.0,
                        "unit": "mg/dL",
                        "range_status": "normal",
                    }
                }
            }
        }


class BloodWorkReport(BaseModel):
    """Single blood work report with metadata"""

    sex: Optional[str] = Field(None, description="Patient's biological sex")
    age: Optional[int] = Field(None)
    practitioner: Optional[str] = Field(None)
    createdAt: Optional[datetime] = Field(None, description="Creation date of the blood work report")
    reportDate: Optional[str] = Field(None, description="Collection date of the lab results")
    dateOfBirth: Optional[str] = Field(None)
    bloodWorkBioMarkerGroup: BloodWorkBioMarkerGroup = Field(..., description="Grouped biomarkers data")
    fileHash: Optional[str] = Field(None, description="SHA-256 hash of the uploaded file for duplicate detection")
    fileName: Optional[str] = Field(None, description="Original filename of the uploaded file")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="Refresh token for getting new access tokens")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


# Functional Medicine Intake Form Models
class PersonalInformation(BaseModel):
    fullName: str = Field(..., description="Full name of the patient", min_length=3, max_length=100)
    address: str = Field(..., description="Patient's address")
    phone: str = Field(..., description="Patient's phone number")
    email: str = Field(..., description="Patient's email")
    dateOfBirth: str = Field(..., description="Patient's date of birth")
    age: int = Field(..., description="Patient's age")
    maritalStatus: str = Field(..., description="Patient's marital status")
    gender: str = Field(..., description="Patient's gender")
    weight: float = Field(..., description="Patient's weight")
    height: str = Field(..., description="Patient's height")
    bloodPressure: str = Field(..., description="Patient's blood pressure")
    primaryCareProvider: str = Field(..., description="Primary care provider name")


class Symptoms(BaseModel):
    generalSymptoms: List[str] = Field(..., description="General symptoms (multi-select)")
    additionalSymptoms: List[str] = Field(..., description="Additional symptoms (multi-select)")
    symptomDuration: str = Field(..., description="Duration of symptoms")
    symptomTiming: str = Field(..., description="Timing of symptoms")
    symptomImpact: str = Field(..., description="Impact of symptoms on daily life")


class MedicalHistory(BaseModel):
    pastMedicalHistory: List[str] = Field(..., description="Past medical history (multi-select)")
    otherMedicalHistory: Optional[str] = Field(None, description="Other medical history details")
    cardiacHistory: List[str] = Field(..., description="Cardiac history (multi-select)")
    otherCardiacHistory: Optional[str] = Field(None, description="Other cardiac history details")


class FamilyHistory(BaseModel):
    conditions: List[str] = Field(..., description="Family conditions (multi-select)")
    otherFamilyHistory: Optional[str] = Field(None, description="Other family history details")
    fatherAgeOrDeath: str = Field(..., description="Father's age or death information")
    fatherHealthStatus: str = Field(..., description="Father's health status")
    fatherHealthReason: Optional[str] = Field(None, description="Reason for father's health status")
    motherAgeOrDeath: str = Field(..., description="Mother's age or death information")
    motherHealthStatus: str = Field(..., description="Mother's health status")
    motherHealthReason: Optional[str] = Field(None, description="Reason for mother's health status")


class HormoneTherapy(BaseModel):
    used: bool = Field(..., description="Whether hormone therapy was used")
    details: Optional[str] = Field(None, description="Details about hormone therapy")


class RecreationalDrugs(BaseModel):
    used: bool = Field(..., description="Whether recreational drugs were used")
    details: Optional[str] = Field(None, description="Details about recreational drug use")


class Lifestyle(BaseModel):
    lastPhysicalExam: str = Field(..., description="Date of last physical exam")
    allergies: str = Field(..., description="Patient's allergies")
    medicationsAndSupplements: str = Field(..., description="Current medications and supplements")
    hormoneTherapy: Optional[HormoneTherapy] = Field(None, description="Hormone therapy information")
    smokingOrCannabis: bool = Field(..., description="Whether patient smokes or uses cannabis")
    recreationalDrugs: Optional[RecreationalDrugs] = Field(None, description="Recreational drug use information")
    alcoholConsumption: str = Field(..., description="Alcohol consumption pattern")
    exerciseRegimen: str = Field(..., description="Exercise regimen")
    desireForChildren: str = Field(..., description="Desire for children")
    referralSource: str = Field(..., description="Source of referral")
    referrerName: Optional[str] = Field(None, description="Name of referrer")


class Consent(BaseModel):
    acceptedTerms: bool = Field(..., description="Whether terms were accepted")
    signature: str = Field(..., description="Patient's signature")
    healthCardNumber: Optional[str] = Field(None, description="Patient's health card number")


class MaleReproductiveHormonal(BaseModel):
    symptoms: Optional[List[str]] = Field(None, description="Male reproductive symptoms (multi-select)")
    howLong: Optional[str] = Field(None, description="How long symptoms have been present")
    timing: Optional[str] = Field(None, description="Timing of symptoms")
    effectOnLife: Optional[str] = Field(None, description="Effect on daily life")
    hypogonadismOrSteroidsUse: Optional[List[str]] = Field(
        None, description="Hypogonadism or steroids use (multi-select)"
    )


class IUDUse(BaseModel):
    used: Optional[bool] = Field(None, description="Whether IUD was used")
    duration: Optional[str] = Field(None, description="Duration of IUD use")


class PremenstrualSymptoms(BaseModel):
    hasSymptoms: bool = Field(..., description="Whether patient has premenstrual symptoms")
    description: Optional[str] = Field(None, description="Description of premenstrual symptoms")


class Hysterectomy(BaseModel):
    had: Optional[bool] = Field(None, description="Whether patient had hysterectomy")
    ovariesRemoved: Optional[bool] = Field(None, description="Whether ovaries were removed")
    surgeryDate: Optional[str] = Field(None, description="Date of hysterectomy surgery")


class OralContraceptives(BaseModel):
    used: Optional[bool] = Field(None, description="Whether oral contraceptives were used")
    lastUseDate: Optional[str] = Field(None, description="Date of last oral contraceptive use")


class Miscarriages(BaseModel):
    total: int = Field(..., description="Total number of miscarriages")
    gestationAge: str = Field(..., description="Gestation age of miscarriages")


class Pregnancies(BaseModel):
    totalPregnancies: Optional[int] = Field(None, description="Total number of pregnancies")
    liveBirths: Optional[int] = Field(None, description="Number of live births")
    liveChildren: Optional[int] = Field(None, description="Number of live children")
    miscarriages: Optional[Miscarriages] = Field(None, description="Miscarriage information")


class MenstrualReproductiveHistory(BaseModel):
    menstrualProblems: List[str] = Field(..., description="Menstrual problems (multi-select)")
    ageAtFirstPeriod: int = Field(..., description="Age at first period")
    cycleRegularity: str = Field(..., description="Cycle regularity")
    flowType: str = Field(..., description="Flow type")
    lastMenstrualCycle: str = Field(..., description="Date of last menstrual cycle")
    iudUse: Optional[IUDUse] = Field(None, description="IUD use information")
    premenstrualSymptoms: Optional[PremenstrualSymptoms] = Field(None, description="Premenstrual symptoms")
    surgeries: Optional[str] = Field(None, description="Reproductive surgeries")
    hysterectomy: Optional[Hysterectomy] = Field(None, description="Hysterectomy information")
    tubalLigation: Optional[bool] = Field(None, description="Whether tubal ligation was performed")
    oralContraceptives: Optional[OralContraceptives] = Field(None, description="Oral contraceptives information")
    lastPelvicExam: Optional[str] = Field(None, description="Date of last pelvic exam")
    lastBreastExam: Optional[str] = Field(None, description="Date of last breast exam")
    pregnancies: Optional[Pregnancies] = Field(None, description="Pregnancy information")


class FunctionalMedicineIntakeForm(BaseModel):
    personalInformation: Optional[PersonalInformation] = Field(None, description="Personal information section")
    symptoms: Optional[Symptoms] = Field(None, description="Symptoms section")
    medicalHistory: Optional[MedicalHistory] = Field(None, description="Medical history section")
    familyHistory: Optional[FamilyHistory] = Field(None, description="Family history section")
    lifestyle: Optional[Lifestyle] = Field(None, description="Lifestyle section")
    consent: Optional[Consent] = Field(None, description="Consent section")
    maleReproductiveHormonal: Optional[MaleReproductiveHormonal] = Field(
        None, description="Male reproductive and hormonal section"
    )
    menstrualReproductiveHistory: Optional[MenstrualReproductiveHistory] = Field(
        None, description="Menstrual and reproductive history section (female only)"
    )


class FunctionalMedicineIntakeFormUpdate(BaseModel):
    personalInformation: Optional[PersonalInformation] = Field(None, description="Personal information section")
    symptoms: Optional[Symptoms] = Field(None, description="Symptoms section")
    medicalHistory: Optional[MedicalHistory] = Field(None, description="Medical history section")
    familyHistory: Optional[FamilyHistory] = Field(None, description="Family history section")
    lifestyle: Optional[Lifestyle] = Field(None, description="Lifestyle section")
    consent: Optional[Consent] = Field(None, description="Consent section")
    maleReproductiveHormonal: Optional[MaleReproductiveHormonal] = Field(
        None, description="Male reproductive and hormonal section"
    )
    menstrualReproductiveHistory: Optional[MenstrualReproductiveHistory] = Field(
        None, description="Menstrual and reproductive history section (female only)"
    )


class PatientCreate(FirestoreBaseModel):
    firstName: str = Field(..., min_length=3, description="First name of the patient")
    lastName: str = Field(..., min_length=3, description="Last name of the patient")
    practitioner: str = Field(..., min_length=3, description="Full name of the practitioner")
    phone: str = Field(..., min_length=3, description="Phone number of the patient")
    address: str = Field(..., description="Address of the patient")
    email: EmailStr = Field(..., description="Email of the patient")
    showReport: bool = Field(default=True, description="Flag to show report")
    password: Optional[str] = Field(
        None,
        min_length=6,
        description="Password of the patient (optional during creation)",
        example="123456"
    )
    gender: Gender = Field(..., description="Gender of the patient (male or female)")

    fullscriptPatientId: Optional[str] = Field(None, description="Fullscript patient ID")

    gene_results: Optional[List[GeneResultEntry]] = Field(None, description="List of gene results for this patient")
    geneResultReports: Optional[List[GeneResultReport]] = Field(
        None, description="List of structured gene result reports"
    )
    bloodWorkReports: Optional[List[Dict]] = Field(None, description="List of structured blood work reports")

    # Functional Medicine Intake Form
    functionalMedicineIntakeForm: Optional[FunctionalMedicineIntakeForm] = Field(
        None, description="Functional Medicine Intake Form data"
    )

    # OTP fields for two-factor authentication
    otp_code: Optional[str] = Field(None, description="Current OTP code for login verification")
    otp_expires_at: Optional[datetime] = Field(None, description="OTP expiration timestamp")
    otp_verified: Optional[bool] = Field(False, description="Whether the current OTP has been verified")

    # Refresh token fields
    refresh_token: Optional[str] = Field(None, description="Current refresh token for the patient")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp for token refresh")
    invitation_status: Optional[str] = Field(
        default="not_sent",
        description="Invitation status for patient onboarding: not_sent, invite_sent, active, etc."
    )

class PatientId(FirestoreBaseModel):
    id: str


class Patient(PatientCreate, PatientId):
    pass


class PatientUpdate(PatientCreate):
    pass


class GeneResultsUpdate(BaseModel):
    gene_results: List[GeneResultEntry] = Field(..., description="List of new gene results to add")


class RecommendationItem(BaseModel):
    key: str = Field(..., description="Unique identifier for the recommendation")
    panel: str = Field(..., description="Panel category this recommendation belongs to")
    category: str = Field(..., description="Type of recommendation (diet/activity/lifestyle)")
    action: str = Field(..., description="The recommendation text")
    details: List[str] = Field(..., description="Detailed breakdown of the recommendation")


class GenerateReport(BloodWorkResults, PatientId):
    firstName: str = Field(..., min_length=3, description="First name of the patient")
    lastName: str = Field(..., min_length=3, description="Last name of the patient")
    recommendations: Optional[List[RecommendationItem]] = Field(
        default=None, description="List of recommendation objects for the patient"
    )
    selectedBioMarkerGroups: Optional[List[BioMarkerGroup]] = Field(
        default=None, description="List of biomarker groups to include in the report"
    )


class GenerateGeneReport(GeneResultReport, PatientId):
    firstName: str = Field(..., min_length=3, description="First name of the patient")
    lastName: str = Field(..., min_length=3, description="Last name of the patient")


class RagQuery(BaseModel):
    query: str


class PatientForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email of the Patient", example="patient@example.com")


class PatientResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(
        ...,
        min_length=6,
        description="New password for the Patient",
        example="newPassword123",
    )

class PatientSetPasswordRequest(BaseModel):
    token: str = Field(..., description="Password set token")


class PatientOTPRequest(BaseModel):
    email: EmailStr = Field(..., description="Email of the Patient", example="patient@example.com")
    otp_code: str = Field(
        ...,
        min_length=6,
        max_length=6,
        description="6-digit OTP code",
        example="123456",
    )


class PatientOTPResponse(BaseModel):
    message: str = Field(..., description="Response message")
    requires_otp: Optional[bool] = Field(None, description="Whether OTP verification is required")


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token to exchange for new access token")

class ShowReportUpdate(BaseModel):
    show_report: bool