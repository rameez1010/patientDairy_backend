from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth.token import get_current_doctor_id
from models.doctor_models import DoctorId
from utils.api_response import APIResponse, error_response, success_response

from .fullscript_service import FullscriptService

fullscript_router = APIRouter(prefix="/fullscript", tags=["fullscript"])
fullscript_service = FullscriptService()


class TokenRequest(BaseModel):
    code: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@fullscript_router.post("/access-token", response_model=APIResponse)
async def get_access_token(request: TokenRequest, doctor_id: DoctorId = Depends(get_current_doctor_id)):
    """
    Exchange authorization code for access token and store in doctor's profile
    """
    try:
        response = await fullscript_service.get_access_token(request.code, doctor_id.id)
        return success_response(data=response, message="Access token retrieved successfully", status_code=200)
    except Exception as e:
        print(f"Failed to get access token ROUTE: {str(e)}")
        return error_response(message=str(e), status_code=400)


@fullscript_router.get("/session-grant-token", response_model=APIResponse)
async def get_session_grant(doctor_id: DoctorId = Depends(get_current_doctor_id)):
    """
    Get session grant for Fullscript Embed
    """
    try:
        response = await fullscript_service.get_session_grant_token(doctor_id.id)
        return success_response(data=response, message="Session grant token retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)


@fullscript_router.post("/refresh", response_model=APIResponse)
async def refresh_token(request: RefreshTokenRequest, doctor_id: DoctorId = Depends(get_current_doctor_id)):
    """
    Get new access token using refresh token and update doctor's profile
    """
    try:
        response = await fullscript_service.refresh_token(request.refresh_token, doctor_id.id)
        return success_response(data=response, message="Token refreshed successfully", status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)


@fullscript_router.post("/patients/{patient_id}", response_model=APIResponse)
async def create_fullscript_patient(patient_id: str, doctor_id: DoctorId = Depends(get_current_doctor_id)):
    """
    Create a patient in Fullscript and link it to our system
    """
    try:
        response = await fullscript_service.create_fullscript_patient(patient_id, doctor_id.id)
        return success_response(
            data={
                "fullscript_patient_id": response.get("patient", {}).get("id"),
                "data": response,
            },
            message="Successfully created patient in Fullscript",
            status_code=200,
        )
    except Exception as e:
        return error_response(message=str(e), status_code=400)


@fullscript_router.get("/patients/{patient_id}/treatment-plans", response_model=APIResponse)
async def get_patient_treatment_plans(patient_id: str, doctor_id: DoctorId = Depends(get_current_doctor_id)):
    """
    Get all treatment plans for a patient from Fullscript
    """
    try:
        response = await fullscript_service.get_patient_treatment_plans(patient_id, doctor_id.id)
        return success_response(data=response, message="Treatment plans retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)


@fullscript_router.get("/patients/{patient_id}/treatment-plans/{treatment_plan_id}", response_model=APIResponse)
async def get_treatment_plan(treatment_plan_id: str, doctor_id: DoctorId = Depends(get_current_doctor_id)):
    """
    Get a single treatment plan by ID from Fullscript
    """
    try:
        response = await fullscript_service.get_treatment_plan(treatment_plan_id, doctor_id.id)
        return success_response(data=response, message="Treatment plan retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)


@fullscript_router.post("/patients/{patient_id}/treatment-plans/{treatment_plan_id}/cancel", response_model=APIResponse)
async def cancel_treatment_plan(treatment_plan_id: str, doctor_id: DoctorId = Depends(get_current_doctor_id)):
    """
    Cancel a treatment plan in Fullscript
    """
    try:
        response = await fullscript_service.cancel_treatment_plan(treatment_plan_id, doctor_id.id)
        return success_response(data=response, message="Successfully cancelled treatment plan", status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
