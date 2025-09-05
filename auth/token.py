from datetime import datetime, timedelta, timezone
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from models.doctor_models import Doctor, DoctorId
from queries.doctor_queries import check_doctor_exists, get_doctor_by_refresh_token, update_doctor_refresh_token

from config.env_config import settings


JWT_KEY = settings.JWT_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = 1  # Access token expires in 1 hour
REFRESH_TOKEN_EXPIRE_HOURS = 24  # Refresh token expires in 24 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_refresh_token() -> str:
    """Generate a secure random refresh token"""
    return secrets.token_urlsafe(32)


def create_access_token(doctor: Doctor) -> str:
    payload = {
        "sub": doctor.id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
        "first_name": doctor.first_name,
        "last_name": doctor.last_name,
        "type": "access",
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_tokens_for_doctor(doctor: Doctor) -> dict:
    """Create both access and refresh tokens for a doctor"""
    access_token = create_access_token(doctor)
    refresh_token = generate_refresh_token()

    # Update doctor with refresh token and last activity
    await update_doctor_refresh_token(doctor.id, refresh_token, datetime.now(timezone.utc))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_HOURS * 3600,  # Convert to seconds
    }


async def refresh_access_token(refresh_token: str) -> dict:
    """Generate new access token using refresh token"""
    # Get doctor by refresh token
    doctor = await get_doctor_by_refresh_token(refresh_token)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    # Check if refresh token is still valid (24 hours from last activity)
    if not doctor.last_activity:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    time_since_last_activity = datetime.now(timezone.utc) - doctor.last_activity
    if time_since_last_activity > timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    # Generate new tokens
    new_access_token = create_access_token(doctor)
    new_refresh_token = generate_refresh_token()

    # Update doctor with new refresh token and last activity
    await update_doctor_refresh_token(doctor.id, new_refresh_token, datetime.now(timezone.utc))

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_HOURS * 3600,
    }


def create_password_reset_token(doctor_id: str, email: str) -> str:
    payload = {
        "sub": doctor_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),  # Token expires in 24 hours
        "type": "password_reset",
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_password_reset_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        doctor_id = payload.get("sub")
        email = payload.get("email")
        token_type = payload.get("type")

        if not doctor_id or not email or token_type != "password_reset":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        if not await check_doctor_exists(doctor_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

        return {"doctor_id": doctor_id, "email": email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


async def verify_token(token: str, credentials_exception: HTTPException) -> DoctorId:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        doctor_id_str = payload.get("sub")
        token_type = payload.get("type")

        if not doctor_id_str or token_type != "access":
            raise credentials_exception
        if not await check_doctor_exists(doctor_id_str):
            raise credentials_exception

        # Update last activity when token is used
        await update_doctor_refresh_token(
            doctor_id_str,
            None,  # Don't update refresh token, just last activity
            datetime.now(timezone.utc),
        )

    except jwt.PyJWTError:
        raise credentials_exception
    doctor_id = DoctorId(id=doctor_id_str)
    return doctor_id


async def get_current_doctor_id(token: str = Depends(oauth2_scheme)) -> DoctorId:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await verify_token(token, credentials_exception)
