from datetime import datetime, timedelta, timezone
import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from models.patient_models import Patient, PatientId
from queries.patient_queries import check_patient_exists, get_patient_by_refresh_token, update_patient_refresh_token

from config.env_config import settings


JWT_KEY = settings.JWT_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = 1  # Access token expires in 1 hour
REFRESH_TOKEN_EXPIRE_HOURS = 24  # Refresh token expires in 24 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="patient_token")


def generate_refresh_token() -> str:
    """Generate a secure random refresh token"""
    return secrets.token_urlsafe(32)


def create_access_token(patient: Patient) -> str:
    payload = {
        "sub": patient.id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
        "first_name": patient.firstName,
        "last_name": patient.lastName,
        "type": "access",
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_tokens_for_patient(patient: Patient) -> dict:
    """Create both access and refresh tokens for a patient"""
    access_token = create_access_token(patient)
    refresh_token = generate_refresh_token()

    # Update patient with refresh token and last activity
    await update_patient_refresh_token(patient.id, refresh_token, datetime.now(timezone.utc))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_HOURS * 3600,  # Convert to seconds
    }


async def refresh_access_token(refresh_token: str) -> dict:
    """Generate new access token using refresh token"""
    # Get patient by refresh token
    patient = await get_patient_by_refresh_token(refresh_token)
    if not patient:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    # Check if refresh token is still valid (24 hours from last activity)
    if not patient.last_activity:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    time_since_last_activity = datetime.now(timezone.utc) - patient.last_activity
    if time_since_last_activity > timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    # Generate new tokens
    new_access_token = create_access_token(patient)
    new_refresh_token = generate_refresh_token()

    # Update patient with new refresh token and last activity
    await update_patient_refresh_token(patient.id, new_refresh_token, datetime.now(timezone.utc))

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_HOURS * 3600,
    }


def create_patient_password_token(patient_id: str, email: str, hours: int = 24, token_type:str = "patient_password_reset") -> str:
    payload = {
        "sub": patient_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=hours),
        "type": token_type,
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_patient_password_token_ignore_exp(token: str) -> dict:
    """
    Decode patient password reset/set-password token and extract patient_id and email, ignoring expiration.
    For use in flows where we just need the data, not authentication.
    """
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        patient_id = payload.get("sub")
        email = payload.get("email")
        token_type = payload.get("type")

        if not patient_id or not email or token_type not in ["patient_password_reset", "patient_set_password"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        return {"patient_id": patient_id, "email": email}
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

async def verify_patient_password_reset_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        patient_id = payload.get("sub")
        email = payload.get("email")
        token_type = payload.get("type")

        if not patient_id or not email or token_type not in ["patient_password_reset", "patient_set_password"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        if not await check_patient_exists(patient_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

        return {"patient_id": patient_id, "email": email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


async def verify_token(token: str, credentials_exception: HTTPException) -> PatientId:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        patient_id_str = payload.get("sub")
        token_type = payload.get("type")

        if not patient_id_str or token_type != "access":
            raise credentials_exception
        if not await check_patient_exists(patient_id_str):
            raise credentials_exception

        # Update last activity when token is used
        await update_patient_refresh_token(
            patient_id_str,
            None,  # Don't update refresh token, just last activity
            datetime.now(timezone.utc),
        )

    except jwt.PyJWTError:
        raise credentials_exception
    patient_id = PatientId(id=patient_id_str)
    return patient_id


async def get_current_patient_id(token: str = Depends(oauth2_scheme)) -> PatientId:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await verify_token(token, credentials_exception)
