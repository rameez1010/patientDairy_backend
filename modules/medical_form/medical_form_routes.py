from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from auth.token_patient import get_current_patient_id
from models.patient_models import FunctionalMedicineIntakeFormUpdate
from modules.medical_form.medical_form_service import MedicalFormService
from utils.api_response import APIResponse, error_response, success_response

# Create router
medical_form_router = APIRouter(prefix="/medical-form", tags=["medical-form"])
medical_form_service = MedicalFormService()
security = HTTPBearer()


@medical_form_router.get("/completion-status", response_model=APIResponse)
async def check_form_completion_status(current_patient_id=Depends(get_current_patient_id)):
    """
    Check if the patient's Functional Medicine Intake Form is complete
    """
    try:
        patient_id = current_patient_id.id

        result = await medical_form_service.check_form_completion(patient_id)

        return success_response(data=result, message="Form completion status retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to check form completion status: {str(e)}", status_code=500)


@medical_form_router.get("/completion-status/{patient_id}", response_model=APIResponse)
async def check_form_completion_status_param(patient_id: str):
    """
    Check medical form completion status via path parameter (admin/staff access)
    """
    try:
        result = await medical_form_service.check_form_completion(patient_id)
        return success_response(data=result, message="Status fetched via path param")
    except Exception as e:
        return error_response(
            message=f"Failed to check form completion status via path param: {str(e)}",
            status_code=500
        )

@medical_form_router.get("/", response_model=APIResponse)
async def get_medical_form(current_patient_id=Depends(get_current_patient_id)):
    """
    Get the patient's current Functional Medicine Intake Form
    """
    try:
        patient_id = current_patient_id.id

        form_data = await medical_form_service.get_medical_form(patient_id)

        if form_data is None:
            return success_response(data=None, message="No medical form data found", status_code=200)

        return success_response(
            data=form_data.model_dump() if form_data else None,
            message="Medical form data retrieved successfully",
            status_code=200,
        )
    except Exception as e:
        return error_response(message=f"Failed to get medical form: {str(e)}", status_code=500)


@medical_form_router.post("/", response_model=APIResponse)
async def save_medical_form(
    form_data: FunctionalMedicineIntakeFormUpdate, current_patient_id=Depends(get_current_patient_id)
):
    """
    Save/Update the patient's Functional Medicine Intake Form
    """
    try:
        patient_id = current_patient_id.id

        result = await medical_form_service.update_medical_form(patient_id, form_data)

        return success_response(data=result, message="Medical form saved successfully", status_code=200)
    except Exception as e:
        print(f"MedicalFormRoutes: Error saving medical form: {str(e)}")
        return error_response(message=f"MedicalFormRoutes: Failed to save medical form: {str(e)}", status_code=500)
