from datetime import datetime
from typing import Optional

from google.cloud.firestore import FieldFilter

from config.config import doctors_collection
from models.doctor_models import Doctor, DoctorCreate, DoctorUpdate, FullscriptData

doctor_ref = doctors_collection


async def insert_doctor(doctor: DoctorCreate) -> Doctor:
    doctor_data = doctor.model_dump()
    new_doctor_ref = doctor_ref.document()
    await new_doctor_ref.set(doctor_data)
    doctor_data["id"] = new_doctor_ref.id
    new_doctor = Doctor(**doctor_data)
    return new_doctor


async def select_doctor_by_email(email: str) -> Optional[Doctor]:
    filter_by_email = FieldFilter("email", "==", email)
    query = doctor_ref.where(filter=filter_by_email)
    doctor_docs = [doc async for doc in query.stream()]
    if doctor_docs:
        doctor_doc = doctor_docs[0]
        doctor_data = doctor_doc.to_dict()
        doctor_data["id"] = doctor_doc.id
        doctor = Doctor(**doctor_data)
        return doctor

    return None


async def delete_doctor(doctor_id: str) -> None:
    doctor_doc_ref = doctor_ref.document(doctor_id)
    await doctor_doc_ref.delete()


async def check_doctor_exists(doctor_id: str) -> bool:
    doctor_doc_ref = doctor_ref.document(doctor_id)
    doctor_doc = await doctor_doc_ref.get()
    doctor_exists = doctor_doc.exists
    return doctor_exists


async def select_doctor_by_id(doctor_id: str) -> Doctor:
    doctor_doc_ref = doctor_ref.document(doctor_id)
    doctor_doc = await doctor_doc_ref.get()
    doctor = Doctor(id=doctor_doc.id, **doctor_doc.to_dict())
    return doctor


async def update_doctor(update_data: DoctorUpdate, doctor_id: str) -> Doctor:
    doctor_doc_ref = doctor_ref.document(doctor_id)
    update_data_dict = update_data.model_dump()
    await doctor_doc_ref.update(update_data_dict)
    updated_doctor = Doctor(id=doctor_id, **update_data_dict)
    return updated_doctor


async def update_doctor_password(doctor_id: str, hashed_password: str) -> bool:
    try:
        doctor_doc_ref = doctor_ref.document(doctor_id)
        await doctor_doc_ref.update({"password": hashed_password})
        return True
    except Exception as e:
        print(f"Error updating password: {str(e)}")
        return False


async def update_doctor_fullscript_data(doctor_id: str, fullscript_data: FullscriptData) -> bool:
    doctor_doc_ref = doctor_ref.document(doctor_id)
    await doctor_doc_ref.update({"fullscript_data": fullscript_data.model_dump()})
    return True


async def update_doctor_otp(doctor_id: str, otp_code: str, otp_expires_at) -> bool:
    """
    Update doctor's OTP code and expiration time
    """
    try:
        doctor_doc_ref = doctor_ref.document(doctor_id)
        await doctor_doc_ref.update({"otp_code": otp_code, "otp_expires_at": otp_expires_at, "otp_verified": False})
        return True
    except Exception as e:
        print(f"Error updating doctor OTP: {str(e)}")
        return False


async def verify_doctor_otp(doctor_id: str) -> bool:
    """
    Mark doctor's OTP as verified
    """
    try:
        doctor_doc_ref = doctor_ref.document(doctor_id)
        await doctor_doc_ref.update({"otp_verified": True})
        return True
    except Exception as e:
        print(f"Error verifying doctor OTP: {str(e)}")
        return False


async def clear_doctor_otp(doctor_id: str) -> bool:
    """
    Clear doctor's OTP data after successful login
    """
    try:
        doctor_doc_ref = doctor_ref.document(doctor_id)
        await doctor_doc_ref.update({"otp_code": None, "otp_expires_at": None, "otp_verified": False})
        return True
    except Exception as e:
        print(f"Error clearing doctor OTP: {str(e)}")
        return False


async def update_doctor_refresh_token(
    doctor_id: str, refresh_token: str = None, last_activity: datetime = None
) -> bool:
    """
    Update doctor's refresh token and/or last activity timestamp
    """
    try:
        doctor_doc_ref = doctor_ref.document(doctor_id)
        update_data = {}

        if refresh_token is not None:
            update_data["refresh_token"] = refresh_token

        if last_activity is not None:
            update_data["last_activity"] = last_activity

        if update_data:
            await doctor_doc_ref.update(update_data)

        return True
    except Exception as e:
        print(f"Error updating doctor refresh token: {str(e)}")
        return False


async def get_doctor_by_refresh_token(refresh_token: str) -> Optional[Doctor]:
    """
    Get doctor by their refresh token
    """
    try:
        filter_by_refresh_token = FieldFilter("refresh_token", "==", refresh_token)
        query = doctor_ref.where(filter=filter_by_refresh_token)
        doctor_docs = [doc async for doc in query.stream()]

        if doctor_docs:
            doctor_doc = doctor_docs[0]
            doctor_data = doctor_doc.to_dict()
            doctor_data["id"] = doctor_doc.id
            doctor = Doctor(**doctor_data)
            return doctor

        return None
    except Exception as e:
        print(f"Error getting doctor by refresh token: {str(e)}")
        return None


async def clear_doctor_refresh_token(doctor_id: str) -> bool:
    """
    Clear doctor's refresh token (for logout)
    """
    try:
        doctor_doc_ref = doctor_ref.document(doctor_id)
        await doctor_doc_ref.update({"refresh_token": None, "last_activity": None})
        return True
    except Exception as e:
        print(f"Error clearing doctor refresh token: {str(e)}")
        return False


async def clear_doctor_fullscript_data(doctor_id: str) -> bool:
    """
    Clear doctor's Fullscript integration data
    """
    try:
        doctor_doc_ref = doctor_ref.document(doctor_id)
        await doctor_doc_ref.update({"fullscript_data": None})
        return True
    except Exception as e:
        print(f"Error clearing doctor Fullscript data: {str(e)}")
        return False
