import json

from fastapi import APIRouter, Depends, File, UploadFile

from ai.gemini_csv import gemini_csv_extractor
from ai.gemini_pdf import gemini_pdf_extractor
from auth.token import get_current_doctor_id
from models.doctor_models import DoctorId
from models.patient_models import GenerateReport
from modules.patients.patient_service import PatientService
from utils.api_response import APIResponse, error_response, success_response
from utils.helpers import serialize_firestore_data
from queries.patient_queries import get_patient_by_id

patients_router = APIRouter(prefix="/patients", tags=["patients"])
patient_service = PatientService()


@patients_router.post("/upload/{patient_id}/blood_work", response_model=APIResponse)
async def upload_report(
    patient_id: str,
    file: UploadFile = File(...),
    doctor_id: DoctorId = Depends(get_current_doctor_id),
    force_upload: bool = False,
):
    """
    Upload and process lab results for a patient.
    This endpoint handles the upload of lab result PDFs, processes them using Gemini AI,
    and stores the results in the patient's record.
    """
    try:
        print("uploading lab results for patient:....", patient_id)
        file_content = await file.read()

        raw_response = gemini_pdf_extractor(file_content)
        # print("raw_response:....", raw_response)

        # Remove the triple backticks and "json" if they exist
        if raw_response.startswith("```json") and raw_response.endswith("```"):
            raw_response = raw_response[7:-3].strip()

        # Parse the JSON response
        response = json.loads(raw_response)
        # Process and store lab results using the service with file content and name for duplicate detection
        # Fetch patient info to get the full name
        patient = await get_patient_by_id(patient_id)
        if not patient:
            return error_response(message="Patient not found", status_code=404)
        patient_full_name = f"{patient.firstName} {patient.lastName}"

        updated_patient = await patient_service.add_patient_blood_work_report(
            patient_id=patient_id,
            doctor_id=doctor_id.id,
            raw_response=response,
            file_content=file_content,
            file_name=file.filename,
            patient_full_name=patient_full_name,
            force_upload=force_upload,
        )

        # Handle name mismatch error for frontend alert
        if isinstance(updated_patient, dict) and updated_patient.get("error_type") == "name_mismatch":
            return error_response(
                message=updated_patient["message"],
                status_code=409,
                errors={
                    "error_type": "name_mismatch",
                    "extracted_name": updated_patient["extracted_name"],
                    "patient_full_name": updated_patient["patient_full_name"],
                    "can_force_upload": True
                }
            )
        
        final_response = serialize_firestore_data(updated_patient.safe_dump())
        return success_response(
            data=final_response, message="Blood work report uploaded and processed successfully", status_code=200
        )

    except ValueError as e:
        if "already been uploaded" in str(e):
            return error_response(
                message="This file has already been uploaded for this patient. Please check your previous uploads.",
                status_code=409,
            )
        return error_response(message=str(e), status_code=400)
    except Exception as e:
        return error_response(message=f"Error processing file: {str(e)}", status_code=500)


@patients_router.post("/upload/{patient_id}/gene_results", response_model=APIResponse)
async def upload_gene_results(
    patient_id: str,
    file: UploadFile = File(...),
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    """
    Upload and process gene results for a patient.
    This endpoint handles the upload of gene result CSVs, processes them using Gemini AI,
    and stores the results in the patient's record using the new grouped structure.
    """
    try:
        print("uploading gene results for patient:....", patient_id)
        file_content = await file.read()

        raw_response = gemini_csv_extractor(file_content)
        print("raw gene response:....", raw_response)

        # Remove the triple backticks and "json" if they exist
        if raw_response.startswith("```json") and raw_response.endswith("```"):
            raw_response = raw_response[7:-3].strip()

        # Parse the JSON response
        response = json.loads(raw_response)

        # Process and store gene results using the service with file content and name for duplicate detection
        updated_patient = await patient_service.add_patient_gene_results_report(
            patient_id=patient_id,
            doctor_id=doctor_id.id,
            raw_response=response,
            collection_date=response.get("collection_date"),
            file_content=file_content,
            file_name=file.filename,
        )

        final_response = serialize_firestore_data(updated_patient.safe_dump())
        return success_response(
            data=final_response, message="Gene results uploaded and processed successfully", status_code=200
        )

    except ValueError as e:
        if "already been uploaded" in str(e):
            return error_response(
                message="This file has already been uploaded for this patient. Please check your previous uploads.",
                status_code=409,
            )
        return error_response(message=str(e), status_code=400)
    except Exception as e:
        return error_response(message=f"Error processing file: {str(e)}", status_code=500)


@patients_router.post("/generate_report", response_model=APIResponse)
async def generate_pdf_report(
    req: GenerateReport,
):
    """
    Generate a PDF report for a patient based on their blood work results.
    """
    try:
        request_data = req.model_dump()
        await patient_service.generate_report(request_data)

        return success_response(message="Report generated successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Error generating report: {str(e)}", status_code=500)
