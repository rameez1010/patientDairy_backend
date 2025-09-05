from datetime import datetime, timedelta
from typing import List, Optional

from google.cloud.firestore import FieldFilter

from config.config import patients_collection
from models.patient_models import (
    BloodWorkReport,
    GeneResultReport,
    GeneResultsUpdate,
    Patient,
    PatientCreate,
    PatientId,
    PatientUpdate,
)

patient_ref = patients_collection


async def insert_patient(patient: PatientCreate, doctor_id: str) -> Patient:
    patient_data = patient.model_dump()
    patient_data["doctor_id"] = doctor_id
    new_patient_ref = patient_ref.document()
    patient_data["id"] = new_patient_ref.id
    await new_patient_ref.set(patient_data)
    new_patient = Patient(**patient_data)
    return new_patient


async def get_patient(patient_id: PatientId, docter_id: str) -> Optional[Patient]:
    query = patients_collection.where("id", "==", patient_id).where("doctor_id", "==", docter_id)
    patient_refs = query.stream()
    async for patient_ref in patient_refs:
        patient_data = patient_ref.to_dict()
        patient_data["id"] = patient_id
        return Patient(**patient_data)
    return None


async def get_all_patients_in_db(doctor_id: str) -> List[Patient]:
    patients = []
    query = patients_collection.where("doctor_id", "==", doctor_id)
    patients_refs = query.stream()

    async for ref in patients_refs:
        patient_data = ref.to_dict()
        patient_data["id"] = ref.id
        patients.append(Patient(**patient_data))
    return patients


async def delete_patient(patient_id: PatientId) -> None:
    patient_ref = patients_collection.document(patient_id)
    await patient_ref.delete()


async def update_patient_show_report(patient_id: str, doctor_id: str, show_report: bool) -> bool:
    """
    Update the showReport field for a patient.
    """
    query = patients_collection.where("id", "==", patient_id).where("doctor_id", "==", doctor_id)
    patient_refs = query.stream()
    async for patient_ref in patient_refs:
        doc_ref = patient_ref.reference
        await doc_ref.update({"showReport": show_report})
        return True
    return False

async def update_patient(update_data: PatientUpdate, patient_id: PatientId, doctor_id: str) -> Patient:
    query = patients_collection.where("id", "==", patient_id).where("doctor_id", "==", doctor_id)
    patient_refs = query.stream()
    async for patient_ref in patient_refs:
        doc_ref = patient_ref.reference
        await doc_ref.update(update_data.model_dump())
        updated_doc = await doc_ref.get()
        updated_doc_dict = updated_doc.to_dict()
        updated_patient = Patient(**updated_doc_dict)
        return updated_patient
    raise ValueError("Patient Not found")


async def add_gene_results_to_patient(
    gene_results_update: GeneResultsUpdate, patient_id: str, doctor_id: str
) -> Patient:
    # Query to find the patient based on patient_id and doctor_id
    query = patients_collection.where("id", "==", patient_id).where("doctor_id", "==", doctor_id)

    # Stream the patient documents based on the query
    patient_refs = query.stream()

    async for patient_ref in patient_refs:
        doc_ref = patient_ref.reference
        patient_data = await doc_ref.get()
        patient_dict = patient_data.to_dict()

        # Get existing gene results or initialize an empty list
        existing_gene_results = patient_dict.get("gene_results", [])

        if existing_gene_results is None:
            existing_gene_results = []  # Ensure it is always a list

        # Append new gene results from the update request
        for gene_result in gene_results_update.gene_results:
            existing_gene_results.append(gene_result.model_dump())  # Convert GeneResult to dictionary

        # Update the patient document with the new gene results
        await doc_ref.update({"gene_results": existing_gene_results})

        # Fetch the updated patient document
        updated_doc = await doc_ref.get()
        updated_doc_dict = updated_doc.to_dict()

        # Return the updated patient object
        updated_patient = Patient(**updated_doc_dict)
        return updated_patient

    # Raise an error if the patient was not found
    raise ValueError("Patient not found")


async def add_blood_work_reports_to_patient(
    patient_id: str,
    doctor_id: str,
    sex,
    age,
    dateOfBirth,
    reportDate,
    blood_work_report,
    file_hash: str = None,
    file_name: str = None,
) -> Patient:
    query = patients_collection.where("id", "==", patient_id).where("doctor_id", "==", doctor_id)
    patient_refs = query.stream()
    async for patient_ref in patient_refs:
        patient_ref = patient_ref.reference
        patient_data = await patient_ref.get()
        patient_dict = patient_data.to_dict()

        # Get existing blood work reports or initialize an empty list
        existing_blood_work_reports = patient_dict.get("bloodWorkReports", [])
        if existing_blood_work_reports is None:
            existing_blood_work_reports = []

        # Append new blood work reports
        # Convert the report to a dictionary and ensure it follows the BloodWorkReport structure

        report_dict = {
            "sex": sex,
            "age": age,
            "createdAt": datetime.now(),
            "reportDate": reportDate,
            "dateOfBirth": dateOfBirth,
            "bloodWorkBioMarkerGroup": blood_work_report,
            "fileHash": file_hash,
            "fileName": file_name,
        }
        existing_blood_work_reports.append(report_dict)

        # Update the patient document with the new blood work reports
        await patient_ref.update({"bloodWorkReports": existing_blood_work_reports})

        # Fetch the updated patient document
        updated_doc = await patient_ref.get()
        updated_doc_dict = updated_doc.to_dict()
        updated_patient = Patient(**updated_doc_dict)
        return updated_patient

    raise ValueError("Patient Not found")


async def add_gene_result_reports_to_patient(
    patient_id: str,
    doctor_id: str,
    gene_result_report: GeneResultReport,
    file_hash: str = None,
    file_name: str = None,
) -> Patient:
    query = patients_collection.where("id", "==", patient_id).where("doctor_id", "==", doctor_id)
    patient_refs = query.stream()
    async for patient_ref in patient_refs:
        patient_ref = patient_ref.reference
        patient_data = await patient_ref.get()
        patient_dict = patient_data.to_dict()

        # Get existing gene result reports or initialize an empty list
        existing_gene_result_reports = patient_dict.get("geneResultReports", [])
        if existing_gene_result_reports is None:
            existing_gene_result_reports = []

        # Append new gene result report
        # Convert the report to a dictionary and add file hash and name
        report_dict = gene_result_report.model_dump()
        report_dict["fileHash"] = file_hash
        report_dict["fileName"] = file_name
        existing_gene_result_reports.append(report_dict)

        # Update the patient document with the new gene result reports
        await patient_ref.update({"geneResultReports": existing_gene_result_reports})

        # Fetch the updated patient document
        updated_doc = await patient_ref.get()
        updated_doc_dict = updated_doc.to_dict()
        updated_patient = Patient(**updated_doc_dict)
        return updated_patient

    raise ValueError("Patient not found")


# Starting of the patient loging stream and patient control stream


async def check_patient_exists(patient_id: str) -> bool:
    patient_doc_ref = patient_ref.document(patient_id)
    patient_doc = await patient_doc_ref.get()
    patient_exists = patient_doc.exists
    return patient_exists


async def select_patient_by_email(email: str) -> Optional[Patient]:
    filter_by_email = FieldFilter("email", "==", email)
    query = patient_ref.where(filter=filter_by_email)
    patient_docs = [doc async for doc in query.stream()]
    if patient_docs:
        patient_doc = patient_docs[0]
        patient_data = patient_doc.to_dict()
        patient_data["id"] = patient_doc.id
        patient = Patient(**patient_data)
        return patient

    return None


async def select_patient_by_phone(phone: str) -> Optional[Patient]:
    filter_by_phone = FieldFilter("phone", "==", phone)
    query = patient_ref.where(filter=filter_by_phone)
    patient_docs = [doc async for doc in query.stream()]
    if patient_docs:
        patient_doc = patient_docs[0]
        patient_data = patient_doc.to_dict()
        patient_data["id"] = patient_doc.id
        patient = Patient(**patient_data)
        return patient
    return None


async def select_patient_by_id(patient_id: str) -> Optional[Patient]:
    patient_doc_ref = patient_ref.document(patient_id)
    patient_doc = await patient_doc_ref.get()
    if not patient_doc.exists:  # Check if the document exists
        return None
    patient = Patient(**patient_doc.to_dict())
    return patient


async def get_patient_latest_blood_work_report(
    patient_id: str,
) -> Optional[BloodWorkReport]:
    patient = await select_patient_by_id(patient_id)
    if patient and patient.bloodWorkReports:
        latest_blood_work_dict = max(patient.bloodWorkReports, key=lambda x: x["reportDate"])
        latest_blood_work_dict["practitioner"] = patient.practitioner
        return BloodWorkReport(**latest_blood_work_dict)
    return None


async def get_patient_self(patient_id: PatientId) -> Optional[Patient]:
    query = patients_collection.where("id", "==", patient_id)
    patient_refs = query.stream()
    async for patient_ref in patient_refs:
        patient_data = patient_ref.to_dict()
        patient_data["id"] = patient_id
        return Patient(**patient_data)
    return None


def parse_lab_result(response, key):
    """Helper function to parse lab results generated by Gemini safely."""
    if key in response:
        # Check if the value is a number
        if isinstance(response[key], dict) and response[key].get("number") is not None:
            return float(response[key]["number"])
        # Handle the case for 'sex'
        elif key == "sex":
            return response[key]  # Assuming it's a string and doesn't need conversion
    return None


def parse_gene_result(response, gene_name):
    """Helper function to parse gene result from the response."""
    # Check if the gene exists in the response and return the value, else return None
    return response.get(gene_name, None)


def parse_collection_date(collection_date):
    # Define a dictionary to map month abbreviations to numeric months
    month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }

    # Try parsing the date in 'YYYY-MM-DD' format (numeric month)
    try:
        new_date = datetime.strptime(collection_date, "%Y-%m-%d")
        # Add 1 day to the parsed date
        new_date += timedelta(days=1)
        return new_date.strftime("%Y-%m-%d")  # Return in 'YYYY-MM-DD' format
    except ValueError:
        pass  # Continue to handle the other format if the first fails

    # Try parsing the date in 'YYYY-Mon-DD' format (month abbreviation)
    try:
        # Split the input string into components: year, month abbreviation, and day
        year, month_str, day = collection_date.split("-")

        # Convert the month abbreviation to a numeric month
        month = month_map.get(month_str, None)
        if not month:
            raise ValueError(f"Invalid month abbreviation: {month_str}")

        # Reconstruct the new date string in 'YYYY-MM-DD' format
        new_date_str = f"{year}-{month}-{day}"

        # Parse the reconstructed date string into a datetime object
        new_date = datetime.strptime(new_date_str, "%Y-%m-%d")

        # Add 1 day to the parsed date
        new_date += timedelta(days=1)

        return new_date.strftime("%Y-%m-%d")  # Return in 'YYYY-MM-DD' format
    except ValueError:
        raise ValueError(f"Invalid date format: {collection_date}. Expected formats are YYYY-MM-DD or YYYY-Mon-DD.")


# Add the update_patient_password function here
async def update_patient_password(patient_id: str, hashed_password: str) -> bool:
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        await patient_doc_ref.update({"password": hashed_password})
        return True
    except Exception as e:
        print(f"Error updating patient password: {str(e)}")
        return False
async def update_patient_invitation_status(patient_id: str, invitation_status: str) -> bool:
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        await patient_doc_ref.update({"invitation_status": invitation_status})
        return True
    except Exception as e:
        print(f"Error updating patient invitation status: {str(e)}")
        return False


async def get_patient_by_id(patient_id: str) -> Patient:
    """Get a patient by their ID from Firestore."""
    patient_doc_ref = patient_ref.document(patient_id)
    patient_doc = await patient_doc_ref.get()
    if patient_doc.exists:
        patient_data = patient_doc.to_dict()
        patient_data["id"] = patient_doc.id
        return Patient(**patient_data)
    return None


async def update_patient_fullscript_id(patient_id: str, fullscript_patient_id: str) -> bool:
    """
    Update a patient record with their Fullscript patient ID
    """
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        await patient_doc_ref.update({"fullscriptPatientId": fullscript_patient_id})
        return True
    except Exception as e:
        print(f"Error updating patient with Fullscript ID: {str(e)}")
        return False


async def update_patient_otp(patient_id: str, otp_code: str, otp_expires_at) -> bool:
    """
    Update patient's OTP code and expiration time
    """
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        await patient_doc_ref.update({"otp_code": otp_code, "otp_expires_at": otp_expires_at, "otp_verified": False})
        return True
    except Exception as e:
        print(f"Error updating patient OTP: {str(e)}")
        return False


async def verify_patient_otp(patient_id: str) -> bool:
    """
    Mark patient's OTP as verified
    """
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        await patient_doc_ref.update({"otp_verified": True})
        return True
    except Exception as e:
        print(f"Error verifying patient OTP: {str(e)}")
        return False


async def clear_patient_otp(patient_id: str) -> bool:
    """
    Clear patient's OTP data after successful login
    """
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        await patient_doc_ref.update({"otp_code": None, "otp_expires_at": None, "otp_verified": False})
        return True
    except Exception as e:
        print(f"Error clearing patient OTP: {str(e)}")
        return False


async def update_patient_refresh_token(
    patient_id: str, refresh_token: str = None, last_activity: datetime = None
) -> bool:
    """
    Update patient's refresh token and/or last activity timestamp
    """
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        update_data = {}

        if refresh_token is not None:
            update_data["refresh_token"] = refresh_token

        if last_activity is not None:
            update_data["last_activity"] = last_activity

        if update_data:
            await patient_doc_ref.update(update_data)

        return True
    except Exception as e:
        print(f"Error updating patient refresh token: {str(e)}")
        return False


async def get_patient_by_refresh_token(refresh_token: str) -> Optional[Patient]:
    """
    Get patient by their refresh token
    """
    try:
        filter_by_refresh_token = FieldFilter("refresh_token", "==", refresh_token)
        query = patient_ref.where(filter=filter_by_refresh_token)
        patient_docs = [doc async for doc in query.stream()]

        if patient_docs:
            patient_doc = patient_docs[0]
            patient_data = patient_doc.to_dict()
            patient_data["id"] = patient_doc.id
            patient = Patient(**patient_data)
            return patient

        return None
    except Exception as e:
        print(f"Error getting patient by refresh token: {str(e)}")
        return None


async def clear_patient_refresh_token(patient_id: str) -> bool:
    """
    Clear patient's refresh token (for logout)
    """
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        await patient_doc_ref.update({"refresh_token": None, "last_activity": None})
        return True
    except Exception as e:
        print(f"Error clearing patient refresh token: {str(e)}")
        return False


async def check_duplicate_blood_work_file_hash(patient_id: str, doctor_id: str, file_hash: str) -> bool:
    query = patients_collection.where("id", "==", patient_id).where("doctor_id", "==", doctor_id)
    patient_refs = query.stream()

    async for patient_ref in patient_refs:
        patient_data = patient_ref.to_dict()

        # Safely get bloodWorkReports list
        blood_work_reports = patient_data.get("bloodWorkReports", []) or []

        for report in blood_work_reports:
            if report.get("fileHash") == file_hash:
                return True

    return False


async def check_duplicate_gene_result_file_hash(patient_id: str, doctor_id: str, file_hash: str) -> bool:
    query = patients_collection.where("id", "==", patient_id).where("doctor_id", "==", doctor_id)
    patient_refs = query.stream()

    async for patient_ref in patient_refs:
        patient_data = patient_ref.to_dict()
        gene_result_reports = patient_data.get("geneResultReports", []) or []

        for report in gene_result_reports:
            if report.get("fileHash") == file_hash:
                return True

    return False


# Medical Form Queries
async def update_patient_medical_form(patient_id: str, form_data) -> dict:
    """
    Update a patient's Functional Medicine Intake Form
    """
    try:
        patient_doc_ref = patient_ref.document(patient_id)

        # Convert form data to dict and remove None values
        form_dict = form_data.model_dump(exclude_unset=True)

        # Add timestamp
        update_data = {"functionalMedicineIntakeForm": form_dict}

        await patient_doc_ref.update(update_data)

        # Get updated patient data
        updated_doc = await patient_doc_ref.get()
        updated_doc_dict = updated_doc.to_dict()

        return updated_doc_dict
    except Exception as e:
        print(f"PatientQueries: Error updating patient medical form: {str(e)}")
        raise Exception(f"PatientQueries: Failed to update medical form: {str(e)}")


async def check_medical_form_completion(patient_id: str) -> bool:
    """
    Check if the patient's Functional Medicine Intake Form is complete
    """
    try:
        patient_doc_ref = patient_ref.document(patient_id)
        patient_doc = await patient_doc_ref.get()

        if not patient_doc.exists:
            return False

        patient_data = patient_doc.to_dict()
        form_data = patient_data.get("functionalMedicineIntakeForm")

        if not form_data:
            return False

        # Check if all required sections are filled
        required_sections = [
            "personalInformation",
            "symptoms",
            "medicalHistory",
            "familyHistory",
            "lifestyle",
            "consent",
        ]

        # Check if all required sections exist and have data
        for section in required_sections:
            if section not in form_data or not form_data[section]:
                return False

        # Check gender-specific sections
        # get gender from patient data
        gender = patient_data.get("gender", "").lower()

        if gender == "male":
            if "maleReproductiveHormonal" not in form_data or not form_data["maleReproductiveHormonal"]:
                return False
        elif gender == "female":
            if "menstrualReproductiveHistory" not in form_data or not form_data["menstrualReproductiveHistory"]:
                return False

        return True
    except Exception as e:
        print(f"Error checking medical form completion: {str(e)}")
        return False
