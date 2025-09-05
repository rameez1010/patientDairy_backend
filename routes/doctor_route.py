import os

from dotenv import (
    load_dotenv,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from auth.password import (
    hash_password,
    validate_hashed_password,
)
from auth.token import (
    create_password_reset_token,
    create_tokens_for_doctor,
    get_current_doctor_id,
    refresh_access_token,
    verify_password_reset_token,
)
from config.env_config import settings
from email_sending.sendgrid_email import (
    send_doctor_otp_email,
    send_password_reset_email,
    sendgrid_email,
)
from models.credentials_models import (
    Credentials,
    PasswordUpdate,
)
from models.doctor_models import (
    DoctorCreate,
    DoctorId,
    DoctorRefreshTokenRequest,
    DoctorUpdate,
    ForgotPasswordRequest,
    OTPRequest,
    ResetPasswordRequest,
)
from queries.doctor_queries import (
    clear_doctor_fullscript_data,
    clear_doctor_otp,
    clear_doctor_refresh_token,
    delete_doctor,
    insert_doctor,
    select_doctor_by_email,
    select_doctor_by_id,
    update_doctor,
    update_doctor_otp,
    update_doctor_password,
    verify_doctor_otp,
)
from utils.api_response import APIResponse, error_response, success_response
from utils.helpers import serialize_firestore_data
from utils.otp_utils import (
    generate_otp_code,
    get_otp_expiration_time,
    is_otp_valid,
)

load_dotenv()

FRONTEND_RESET_PASSWORD_URL = settings.FRONTEND_RESET_PASSWORD_URL

doctor_router = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
)


@doctor_router.post("/register", response_model=APIResponse)
async def create_doctor(
    doctor_data: DoctorCreate,
):
    try:
        existing_doctor = await select_doctor_by_email(doctor_data.email)
        if existing_doctor:
            return error_response(message="Email is already registered!", status_code=400)

        doctor_data.password = hash_password(doctor_data.password)
        new_doctor = await insert_doctor(doctor_data)
        sendgrid_email(
            doctor_data.email,
            doctor_data.first_name,
        )

        final_response = serialize_firestore_data (new_doctor.safe_dump())
        return success_response(data=final_response, message="Doctor registered successfully", status_code=201)
    except Exception as e:
        return error_response(message=f"Failed to register doctor: {str(e)}", status_code=500)


@doctor_router.post("/login", response_model=APIResponse)
async def login_doctor(
    credentials: Credentials,
):
    try:
        existing_doctor = await select_doctor_by_email(credentials.email)
        if not existing_doctor:
            return error_response(message="No account exists with the provided email.", status_code=400)

        if not validate_hashed_password(
            existing_doctor.password,
            credentials.password,
        ):
            return error_response(message="Authentication failed. Wrong password.", status_code=400)

        # Generate and send OTP
        otp_code = generate_otp_code()
        otp_expires_at = get_otp_expiration_time()

        # Update doctor with OTP
        otp_updated = await update_doctor_otp(existing_doctor.id, otp_code, otp_expires_at)
        if not otp_updated:
            return error_response(message="Failed to generate OTP. Please try again.", status_code=500)

        # Send OTP email
        email_sent = send_doctor_otp_email(
            existing_doctor.email,
            existing_doctor.first_name,
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


@doctor_router.post("/verify-otp", response_model=APIResponse)
async def verify_otp(
    otp_request: OTPRequest,
):
    """
    Verify OTP and return access and refresh tokens
    """
    try:
        existing_doctor = await select_doctor_by_email(otp_request.email)
        if not existing_doctor:
            return error_response(message="Invalid request!", status_code=400)

        # Validate OTP with reason
        is_valid, reason = is_otp_valid(
            otp_request.otp_code,
            existing_doctor.otp_code,
            existing_doctor.otp_expires_at,
            existing_doctor.otp_verified,
        )

        if not is_valid:
            if reason == "expired":
                return error_response(message="Your OTP has expired. Please request a new one.", status_code=400)
            elif reason == "used":
                return error_response(message="This OTP has already been used.", status_code=400)
            else:
                return error_response(message="Invalid OTP. Please check and try again.", status_code=400)

        # Mark OTP as verified
        await verify_doctor_otp(existing_doctor.id)

        # Generate access and refresh tokens
        tokens = await create_tokens_for_doctor(existing_doctor)

        # Clear OTP data
        await clear_doctor_otp(existing_doctor.id)

        return success_response(data=tokens, message="OTP verified successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"OTP verification failed: {str(e)}", status_code=500)


@doctor_router.post("/refresh-token", response_model=APIResponse)
async def refresh_doctor_token(
    refresh_request: DoctorRefreshTokenRequest,
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


@doctor_router.post("/logout", response_model=APIResponse)
async def logout_doctor(
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    """
    Logout doctor by clearing their refresh token
    """
    try:
        success = await clear_doctor_refresh_token(doctor_id.id)
        if not success:
            return error_response(message="Failed to logout", status_code=500)

        return success_response(message="Successfully logged out", status_code=200)
    except Exception as e:
        return error_response(message=f"Logout failed: {str(e)}", status_code=500)


@doctor_router.delete("/delete", response_model=APIResponse)
async def delete(
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        await delete_doctor(doctor_id.id)
        return success_response(message="Doctor deleted successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to delete doctor: {str(e)}", status_code=500)


@doctor_router.put("/update", response_model=APIResponse)
async def update(
    update_data: DoctorUpdate,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        current_doctor = await select_doctor_by_id(doctor_id.id)
        if update_data.email != current_doctor.email:
            existing_doctor = await select_doctor_by_email(update_data.email)
            if existing_doctor:
                return error_response(message="Email is already registered!", status_code=400)

        update_data.password = hash_password(update_data.password)
        updated_doctor = await update_doctor(
            update_data,
            doctor_id.id,
        )
        final_response = serialize_firestore_data(updated_doctor.safe_dump())
        return success_response(data=final_response, message="Doctor updated successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to update doctor: {str(e)}", status_code=500)


@doctor_router.get("/me", response_model=APIResponse)
async def get_current_doctor(
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        doctor = await select_doctor_by_id(doctor_id.id)
        if not doctor:
            return error_response(message="Doctor not found!", status_code=404)

        final_response = serialize_firestore_data(doctor.safe_dump())
        return success_response(data=final_response, message="Doctor retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to retrieve doctor: {str(e)}", status_code=500)


@doctor_router.post("/forgot-password", response_model=APIResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
):
    """
    Send a password reset email to the doctor's email address.
    """
    try:
        print(request.email)
        doctor = await select_doctor_by_email(request.email)
        if not doctor:
            # For security reasons, don't reveal if the email exists or not
            return success_response(
                message="If your email is registered, you will receive a password reset link.", status_code=200
            )

        # Create a password reset token
        reset_token = create_password_reset_token(
            doctor.id,
            doctor.email,
        )

        # Create the reset link
        reset_link = f"{FRONTEND_RESET_PASSWORD_URL}?token={reset_token}"

        # Send the password reset email
        email_sent = send_password_reset_email(
            doctor.email,
            doctor.first_name,
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


@doctor_router.post("/reset-password", response_model=APIResponse)
async def reset_password(
    request: ResetPasswordRequest,
):
    """
    Reset the doctor's password using the token from the email.
    """
    try:
        # Verify the token
        token_data = await verify_password_reset_token(request.token)

        # Hash the new password
        hashed_password = hash_password(request.new_password)

        # Update the doctor's password
        success = await update_doctor_password(
            token_data["doctor_id"],
            hashed_password,
        )

        if not success:
            return error_response(message="Failed to update password. Please try again later.", status_code=500)

        return success_response(
            message="Password has been reset successfully. You can now log in with your new password.", status_code=200
        )
    except Exception as e:
        return error_response(message=f"Failed to reset password: {str(e)}", status_code=400)


@doctor_router.put("/update-password", response_model=APIResponse)
async def update_password(
    password_data: PasswordUpdate,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    try:
        # Get the current doctor
        current_doctor = await select_doctor_by_id(doctor_id.id)
        if not current_doctor:
            return error_response(message="Doctor not found!", status_code=404)

        # Validate the current password
        if not validate_hashed_password(
            current_doctor.password,
            password_data.current_password,
        ):
            return error_response(message="Current password is incorrect!", status_code=400)

        # Hash the new password
        hashed_new_password = hash_password(password_data.new_password)

        # Update the password in the database
        await update_doctor_password(
            doctor_id.id,
            hashed_new_password,
        )

        return success_response(message="Password updated successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to update password: {str(e)}", status_code=500)


@doctor_router.delete("/disconnect-fullscript", response_model=APIResponse)
async def disconnect_fullscript(
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    """
    Disconnect Fullscript integration by clearing the doctor's Fullscript data
    """
    try:
        success = await clear_doctor_fullscript_data(doctor_id.id)
        if not success:
            return error_response(
                message="Failed to disconnect Fullscript integration", 
                status_code=500
            )
        return success_response(
            message="Successfully disconnected Fullscript integration", 
            status_code=200
        )
    except Exception as e:
        return error_response(
            message=f"Failed to disconnect Fullscript integration: {str(e)}", 
            status_code=500
        )
