from typing import List
import io
import os

from dotenv import (
    load_dotenv,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import (
    StreamingResponse,
)
from google.cloud import (
    storage,
)
from PyPDF2 import (
    PdfMerger,
)

from ai.rag import (
    patient_rag_function,
)
from ai.recommendation_ai import patient_recommendation_function
from auth.password import (
    hash_password,
    validate_hashed_password,
)
from auth.token import (
    get_current_doctor_id,
)
from auth.token_patient import (
    create_patient_password_token,
    create_tokens_for_patient,
    get_current_patient_id,
    refresh_access_token,
    verify_patient_password_reset_token,
    decode_patient_password_token_ignore_exp,
)
from config.cloud_storage import (
    upload_blob,
)
from config.env_config import settings
from email_sending.sendgrid_patient import (
    send_patient_otp_email,
    send_patient_password_reset_email,
    send_patient_set_password_email,
    sendgrid_email,
)
from male_report.gene_report.generate_gene_report import (
    generate_gene_report_pages,
)
from models.credentials_models import (
    Credentials,
    PasswordUpdate,
)
from models.doctor_models import (
    DoctorId,
)
from models.patient_models import (
    ShowReportUpdate,
)
from models.patient_models import (
    GenerateGeneReport,
    GeneResultsUpdate,
    PatientCreate,
    PatientForgotPasswordRequest,
    PatientId,
    PatientOTPRequest,
    PatientResetPasswordRequest,
    PatientSetPasswordRequest,
    PatientUpdate,
    RagQuery,
    RefreshTokenRequest,
)
from queries.patient_queries import (
    add_gene_results_to_patient,
    clear_patient_otp,
    clear_patient_refresh_token,
    delete_patient,
    get_all_patients_in_db,
    get_patient,
    get_patient_latest_blood_work_report,
    get_patient_self,
    insert_patient,
    select_patient_by_email,
    select_patient_by_id,
    select_patient_by_phone,
    update_patient,
    update_patient_invitation_status,
    update_patient_otp,
    update_patient_password,
    verify_patient_otp,
    update_patient_show_report
)
from utils.api_response import APIResponse, error_response, success_response
from utils.helpers import serialize_firestore_data
from utils.otp_utils import (
    generate_otp_code,
    get_otp_expiration_time,
    is_otp_valid,
)

load_dotenv()

FRONTEND_PATIENT_RESET_PASSWORD_URL = settings.FRONTEND_PATIENT_RESET_PASSWORD_URL
FRONTEND_SET_PASSWORD_URL = settings.FRONTEND_PATIENT_SET_PASSWORD_URL


patient_router = APIRouter(
    prefix="/patients",
    tags=["patients & lab results"],
)


@patient_router.post("/add", response_model=APIResponse)
async def create_patient(
    patient_data: PatientCreate,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        # Check if a patient with this email already exists
        existing_patient = await select_patient_by_email(patient_data.email)
        if existing_patient:
            return error_response(message="A patient with this email already exists", status_code=400)

        # Check if a patient with this phone number already exists
        existing_patient_by_phone = await select_patient_by_phone(patient_data.phone)
        if existing_patient_by_phone:
            return error_response(message="A patient with this phone number already exists", status_code=400)

        # patient_data.password = hash_password(patient_data.password)
        new_patient = await insert_patient(
            patient_data,
            doctor_id.id,
        )

        # Remove sensitive data from response
        patient_dict = new_patient.safe_dump()

        return success_response(data=patient_dict, message="Patient created successfully", status_code=201)
    except Exception as e:
        return error_response(message=f"Failed to create patient: {str(e)}", status_code=500)


@patient_router.get("/{patient_id}", response_model=APIResponse)
async def get_patient_by_id(
    patient_id: str,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        patient_data = await get_patient(
            patient_id,
            doctor_id.id,
        )
        if not patient_data:
            return error_response(message="Patient not found", status_code=404)

        final_response = serialize_firestore_data(patient_data.safe_dump())
        return success_response(data=final_response, message="Patient retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to retrieve patient: {str(e)}", status_code=500)


@patient_router.get("/", response_model=APIResponse)
async def get_all_patients(
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        patients = await get_all_patients_in_db(doctor_id.id)
        patients_data = [serialize_firestore_data(patient.safe_dump()) for patient in patients]
        return success_response(data=patients_data, message="Patients retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to retrieve patients: {str(e)}", status_code=500)


@patient_router.delete("/{patient_id}", response_model=APIResponse)
async def delete_patient_by_id(
    patient_id: str,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        await delete_patient(patient_id)
        return success_response(message="Patient deleted successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to delete patient: {str(e)}", status_code=500)


@patient_router.put("/update-password", response_model=APIResponse)
async def update_password(
    password_data: PasswordUpdate,
    patient_id: PatientId = Depends(get_current_patient_id),
):
    try:
        # Get the current patient
        current_patient = await get_patient_self(patient_id.id)
        if not current_patient:
            return error_response(message="Patient not found!", status_code=404)

        # Validate the current password
        if not validate_hashed_password(
            current_patient.password,
            password_data.current_password,
        ):
            return error_response(message="Current password is incorrect!", status_code=400)

        # Hash the new password
        hashed_new_password = hash_password(password_data.new_password)

        # Update the password in the database
        await update_patient_password(
            patient_id.id,
            hashed_new_password,
        )

        return success_response(message="Password updated successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to update password: {str(e)}", status_code=500)


@patient_router.put("/{patient_id}", response_model=APIResponse)
async def update(
    update_data: PatientUpdate,
    patient_id: str,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        updated_patient = await update_patient(
            update_data,
            patient_id,
            doctor_id.id,
        )
        
        final_response = serialize_firestore_data(updated_patient.safe_dump())
        return success_response(data=final_response, message="Patient updated successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to update patient: {str(e)}", status_code=500)


@patient_router.put("/{patient_id}/show-report", response_model=APIResponse)
async def set_patient_show_report(
    patient_id: str,
    show_report: ShowReportUpdate,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    """
    Update the showReport field for a patient (allow patient to see reports).
    """
    try:
        result = await update_patient_show_report(patient_id, doctor_id.id, show_report.show_report)
        if result:
            return success_response(message="Patient report visibility updated successfully", status_code=200)
        else:
            return error_response(message="Patient not found or update failed", status_code=404)
    except Exception as e:
        return error_response(message=f"Failed to update patient report visibility: {str(e)}", status_code=500)

@patient_router.post("/{patient_id}/gene_results", response_model=APIResponse)
async def add_gene_results(
    gene_results_update: GeneResultsUpdate,
    patient_id: str,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        # Call the function to add gene results to the patient
        updated_patient = await add_gene_results_to_patient(
            gene_results_update,
            patient_id,
            doctor_id.id,
        )

        final_response = serialize_firestore_data(updated_patient.safe_dump())
        return success_response(data=final_response, message="Gene results added successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to add gene results: {str(e)}", status_code=500)


@patient_router.post("/generate_gene_report", response_model=APIResponse)
async def generate_gene_pdf_report(
    report_data: GenerateGeneReport,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        merger = PdfMerger()
        report = report_data.model_dump()
        print(
            "report is:",
            report,
        )

        buffers = generate_gene_report_pages(report)
        # merge all page buffers
        for (
            i,
            buffer,
        ) in enumerate(buffers):
            merger.append(buffer)

        final_buffer = io.BytesIO()
        merger.write(final_buffer)
        merger.close

        final_buffer.seek(0)
        upload_blob(
            final_buffer,
            f"{report.get('firstName', '')}_{report.get('lastName', '')}_{report.get('id', '')}_gene_report_.pdf",
        )

        return success_response(message="Gene report generated successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to generate gene report: {str(e)}", status_code=500)


# route to get the pdf Gene report of each patient from the storage
@patient_router.get(
    "/get_gene_report/{first_name}_{last_name}_{patient_id}",
    response_model=None,
)
async def get_patient_gene_pdf_report(
    patient_id: str,
    first_name: str,
    last_name: str,
    doctor_id: str = Depends(get_current_doctor_id),
):
    storage_client = storage.Client()
    bucket_name = "my_test_bucket_for_fastapi"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{first_name}_{last_name}_{patient_id}_gene_report_.pdf")  # Ensure filename matches storage

    if not blob.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    pdf_buffer = io.BytesIO()
    blob.download_to_file(pdf_buffer)

    pdf_buffer.seek(0)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={first_name}_{last_name}_{patient_id}_gene_report_.pdf"},
    )


# route to get the pdf report of each patient from the storage
@patient_router.get(
    "/get_report/{first_name}_{last_name}_{patient_id}",
    response_model=None,
)
async def get_patient_pdf_report(
    patient_id: str,
    first_name: str,
    last_name: str,
    doctor_id: str = Depends(get_current_doctor_id),
):
    storage_client = storage.Client()
    bucket_name = "my_test_bucket_for_fastapi"
    bucket = storage_client.bucket(bucket_name)
    latest_blood_work_report = await get_patient_latest_blood_work_report(patient_id)
    report_date = getattr(latest_blood_work_report, 'reportDate', '')
    filename = f"{first_name}_{last_name}_{patient_id}_{report_date}_full_report_.pdf"
    blob = bucket.blob(filename)  # Ensure filename matches storage

    if not blob.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    pdf_buffer = io.BytesIO()
    blob.download_to_file(pdf_buffer)

    pdf_buffer.seek(0)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={first_name}_{last_name}_{patient_id}_report_.pdf"},
    )

@patient_router.get(
    "/get_report_by_file/{file_name}",
    response_model=None,
)
async def get_patient_pdf_report(
    file_name: str,
):
    print(file_name)
    storage_client = storage.Client()
    bucket_name = "my_test_bucket_for_fastapi"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)  # Ensure filename matches storage

    if not blob.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    pdf_buffer = io.BytesIO()
    blob.download_to_file(pdf_buffer)

    pdf_buffer.seek(0)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )



@patient_router.get("/get_all_reports_grouped/{first_name}_{last_name}_{patient_id}", response_model=None)
async def get_all_reports_grouped(
    first_name: str,
    last_name: str,
    patient_id: str,
):
    """
    Receives patient_id, first_name, last_name as GET params. Returns all report files grouped by reportDate.
    """
    try:
        storage_client = storage.Client()
        bucket_name = "my_test_bucket_for_fastapi"
        bucket = storage_client.bucket(bucket_name)

        if not patient_id or not first_name or not last_name:
            raise HTTPException(status_code=400, detail="Missing patient_id, first_name, or last_name")

        patient = await get_patient_self(patient_id)
        print(patient)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # If the patient is a pydantic model, use patient.bloodWorkReports
        if hasattr(patient, "bloodWorkReports"):
            blood_work_reports = patient.bloodWorkReports or []

        # Collect all unique report dates
        date_to_files = {}
        for report in blood_work_reports:
            report_date = report.get("reportDate") or (hasattr(report, "reportDate") and getattr(report, "reportDate"))
            if not report_date:
                continue
            # List all blobs that start with the pattern
            prefix = f"{first_name}_{last_name}_{patient_id}_{report_date}_"
            blobs = bucket.list_blobs(prefix=prefix)
            files = [blob.name for blob in blobs]
            if files:
                if report_date not in date_to_files:
                    date_to_files[report_date] = {"files": []}
                date_to_files[report_date]["files"].extend(files)

        return success_response(
            data=date_to_files,
            message="Grouped report files fetched successfully.",
            status_code=200,
        )
    except Exception as e:
        return error_response(message=f"Error fetching grouped reports: {str(e)}", status_code=500)


# patient route for login
@patient_router.post("/login_patient", response_model=APIResponse)
async def login_patient(
    credentials: Credentials,
):
    try:
        existing_patient = await select_patient_by_email(credentials.email)
        if not existing_patient:
            return error_response(message="No account exists with the provided email. Please contact your doctor to get valid login credentials.", status_code=400)
        if not existing_patient.password:
            return error_response(
        message="Your password has not been set yet. Please check your email and follow the link to set your password.",
        status_code=403
    )  
        if not validate_hashed_password(
            existing_patient.password,
            credentials.password,
        ):
            return error_response(message="Authentication failed. Wrong password.", status_code=400)

        # Generate and send OTP
        otp_code = generate_otp_code()
        otp_expires_at = get_otp_expiration_time()

        # Update patient with OTP
        otp_updated = await update_patient_otp(existing_patient.id, otp_code, otp_expires_at)
        if not otp_updated:
            return error_response(message="Failed to generate OTP. Please try again.", status_code=500)

        # Send OTP email
        email_sent = send_patient_otp_email(
            existing_patient.email,
            existing_patient.firstName,
            otp_code,
        )

        if not email_sent:
            return error_response(message="Failed to send OTP email. Please try again.", status_code=500)

        return success_response(
            data={"requires_otp": True},
            message="OTP sent to your email. Please verify to complete login.",
            status_code=200,
        )
    except Exception as e:
        return error_response(message=f"Login failed: {str(e)}", status_code=500)


@patient_router.post("/verify-otp", response_model=APIResponse)
async def verify_patient_otp_endpoint(
    otp_request: PatientOTPRequest,
):
    """
    Verify patient OTP and return access and refresh tokens
    """
    try:
        existing_patient = await select_patient_by_email(otp_request.email)
        if not existing_patient:
            return error_response(message="Invalid request!", status_code=400)

        # Validate OTP
        is_valid, reason = is_otp_valid(
            otp_request.otp_code,
            existing_patient.otp_code,
            existing_patient.otp_expires_at,
            existing_patient.otp_verified,
        )

        if not is_valid:
            if reason == "expired":
                return error_response(message="Your OTP has expired. Please request a new one.", status_code=400)
            elif reason == "used":
                return error_response(message="This OTP has already been used.", status_code=400)
            else:
                return error_response(message="Invalid OTP. Please check and try again.", status_code=400)

        # Mark OTP as verified
        await verify_patient_otp(existing_patient.id)

        # Generate access and refresh tokens
        tokens = await create_tokens_for_patient(existing_patient)

        # Clear OTP data
        await clear_patient_otp(existing_patient.id)

        return success_response(data=tokens, message="OTP verified successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"OTP verification failed: {str(e)}", status_code=500)


@patient_router.post("/refresh-token", response_model=APIResponse)
async def refresh_patient_token(
    refresh_request: RefreshTokenRequest,
):
    """
    Refresh access token using refresh token
    """
    try:
        tokens = await refresh_access_token(refresh_request.refresh_token)
        return success_response(data=tokens, message="Token refreshed successfully", status_code=200)
    except HTTPException as e:
        return error_response(message=e.detail, status_code=e.status_code)
    except Exception:
        return error_response(message="Failed to refresh token", status_code=500)


@patient_router.post("/logout", response_model=APIResponse)
async def logout_patient(
    patient_id: PatientId = Depends(get_current_patient_id),
):
    """
    Logout patient by clearing their refresh token
    """
    try:
        success = await clear_patient_refresh_token(patient_id.id)
        if not success:
            return error_response(message="Failed to logout", status_code=500)

        return success_response(message="Successfully logged out", status_code=200)
    except Exception as e:
        return error_response(message=f"Logout failed: {str(e)}", status_code=500)


@patient_router.get("/self/{patient_id}", response_model=APIResponse)
async def get_patient_by_id_self(
    patient_id: PatientId = Depends(get_current_patient_id),
):
    try:
        patient_data = await get_patient_self(patient_id.id)
        # check if the patient exist
        if not patient_data:
            return error_response(message="Patient not found", status_code=404)

        final_response = serialize_firestore_data(patient_data.safe_dump())
        return success_response(data=final_response, message="Patient data retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to retrieve patient data: {str(e)}", status_code=500)


# route for patinet to get their own pdf report from cloud storage
@patient_router.get(
    "/get_self_report/{first_name}_{last_name}_{patient_id}",
    response_model=None,
)
async def get_patient_pdf_self_report(
    first_name: str,
    last_name: str,
    patient_id: PatientId = Depends(get_current_patient_id),
):
    storage_client = storage.Client()
    bucket_name = "my_test_bucket_for_fastapi"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{first_name}_{last_name}_{patient_id.id}_report_.pdf")  # Ensure filename matches storage

    if not blob.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    pdf_buffer = io.BytesIO()
    blob.download_to_file(pdf_buffer)

    pdf_buffer.seek(0)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={first_name}_{last_name}_{patient_id.id}_report_.pdf"},
    )


# route for patinet to get their own GENE pdf report from cloud storage
@patient_router.get(
    "/get_self_gene_report/{first_name}_{last_name}_{patient_id}",
    response_model=None,
)
async def get_patient_pdf_self_gene_report(
    first_name: str,
    last_name: str,
    patient_id: PatientId = Depends(get_current_patient_id),
):
    storage_client = storage.Client()
    bucket_name = "my_test_bucket_for_fastapi"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{first_name}_{last_name}_{patient_id.id}_gene_report_.pdf")  # Ensure filename matches storage

    if not blob.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    pdf_buffer = io.BytesIO()
    blob.download_to_file(pdf_buffer)

    pdf_buffer.seek(0)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={first_name}_{last_name}_{patient_id.id}_gene_report_.pdf"
        },
    )


# patient rag endpoint
@patient_router.post("/{patient_id}/rag", response_model=APIResponse)
async def perform_rag_on_patient_data(
    patient_id: str,
    query: RagQuery,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        patient_data = await get_patient(
            patient_id,
            doctor_id.id,
        )

        # check if the patient exists
        if not patient_data:
            return error_response(message="Patient not found", status_code=404)

        # Perform the RAG operation
        rag_response = patient_rag_function(
            query.query,
            patient_data,
        )

        return success_response(data=rag_response, message="RAG analysis completed successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to perform RAG analysis: {str(e)}", status_code=500)


# patient recommendtion AI endpoint
@patient_router.post("/{patient_id}/recommendationAI", response_model=APIResponse)
async def perform_recommendations_on_patient_data(
    patient_id: str,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        patient_data = await get_patient(
            patient_id,
            doctor_id.id,
        )

        latest_blood_work_report = await get_patient_latest_blood_work_report(patient_id)

        # check if the patient exists
        if not patient_data:
            return error_response(message="Patient not found", status_code=404)

        # Perform the recommendation operation
        recommendation_response = patient_recommendation_function(latest_blood_work_report)

        return success_response(
            data=recommendation_response, message="AI recommendations generated successfully", status_code=200
        )
    except Exception as e:
        return error_response(message=f"Failed to generate AI recommendations: {str(e)}", status_code=500)


# Add the forgot password and reset password endpoints here
@patient_router.post("/forgot-password", response_model=APIResponse)
async def forgot_password(
    request: PatientForgotPasswordRequest,
):
    """
    Send a password reset email to the patient's email address.
    """
    try:
        patient = await select_patient_by_email(request.email)
        if not patient:
            # For security reasons, don't reveal if the email exists or not
            return success_response(
                message="If your email is registered, you will receive a password reset link.", status_code=200
            )

        # Create a password reset token
        reset_token = create_patient_password_token(
            patient.id,
            patient.email,
        )

        # Create the reset link
        reset_link = f"{FRONTEND_PATIENT_RESET_PASSWORD_URL}?token={reset_token}"

        # Send the password reset email
        email_sent = send_patient_password_reset_email(
            patient.email,
            patient.firstName,
            reset_link,
        )

        if not email_sent:
            return error_response(
                message="Failed to send password reset email. Please try again later.", status_code=500
            )

        return success_response(
            message="If your email is registered, you will receive a password reset link.", status_code=200
        )
    except Exception as e:
        return error_response(message=f"Failed to process password reset request: {str(e)}", status_code=500)


@patient_router.post("/reset-password", response_model=APIResponse)
async def reset_password(
    request: PatientResetPasswordRequest,
):
    """
    Reset the patient's password using the token from the email.
    """
    try:
        # Verify the token
        token_data = await verify_patient_password_reset_token(request.token)

        # Hash the new password
        hashed_password = hash_password(request.new_password)

        # Update the patient's password
        success = await update_patient_password(
            token_data["patient_id"],
            hashed_password,
        )

        if not success:
            return error_response(message="Failed to update password. Please try again later.", status_code=500)

        # Update invitation_status to 'active'
        await update_patient_invitation_status(token_data["patient_id"], "active")

        return success_response(
            message="Password has been reset successfully. You can now log in with your new password.", status_code=200
        )
    except Exception as e:
        return error_response(message=f"Failed to reset password: {str(e)}", status_code=400)

@patient_router.post("/resend-set-password-email", response_model=APIResponse)
async def resend_set_password_email(
    request: PatientSetPasswordRequest,
):
    """
    Resend the set password email to the patient's email address.
    """
    try:
        # Decode the token and extract data, ignoring expiration
        token_data = decode_patient_password_token_ignore_exp(request.token)
        reset_token = create_patient_password_token(
            token_data["patient_id"],
            token_data["email"],
            168,
            "patient_set_password",
        )

        # Create the reset link
        set_password_link = f"{FRONTEND_PATIENT_RESET_PASSWORD_URL}?token={reset_token}"
        # Send the set password email
        email_sent = send_patient_set_password_email(
            token_data["email"],
            set_password_link,
        )

        if not email_sent:
            return error_response(
                message="Failed to send set password email. Please try again later.", status_code=500
            )

        return success_response(
            message="Set password email has been sent successfully.", status_code=200
        )
    except Exception as e:
        return error_response(message=f"Failed to reset password: {str(e)}", status_code=400)

@patient_router.post("/{patient_id}/invite", response_model=APIResponse)
async def invite_patient(
    patient_id: str,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    """
    Send invitation email to patient, generate reset token, update invitation_status.
    """
    try:
        # Fetch patient data
        patient = await select_patient_by_id(patient_id)
        if not patient:
            return error_response(message="Patient not found", status_code=404)

        # Create password reset token
        reset_token = create_patient_password_token(
            patient.id,
            patient.email,
            168,
            "patient_set_password"
        )
        set_password_link = f"{settings.FRONTEND_PATIENT_SET_PASSWORD_URL}?token={reset_token}"

        # Send invitation email
        sendgrid_email(
            patient.email,
            patient.firstName,
            set_password_link
        )

        # Update invitation_status
        await update_patient_invitation_status(patient_id, "invite_sent")

        return success_response(message="Invitation sent successfully.", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to invite patient: {str(e)}", status_code=500)