from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

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

class FullscriptData(FirestoreBaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    scope: str
    created_at: datetime
    resource_owner_id: str
    resource_owner_type: str


class DoctorBase(FirestoreBaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="First name of the Doctor",
        example="John",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Last name of the Doctor",
        example="Doe",
    )
    email: EmailStr = Field(..., description="Email of the Doctor", example="john_doe@example.com")
    password: str = Field(..., min_length=6, description="Password of the Doctor", example="123456Aa")
    fullscript_data: Optional[FullscriptData] = None

    # OTP fields for two-factor authentication
    otp_code: Optional[str] = Field(None, description="Current OTP code for login verification")
    otp_expires_at: Optional[datetime] = Field(None, description="OTP expiration timestamp")
    otp_verified: Optional[bool] = Field(False, description="Whether the current OTP has been verified")

    # Refresh token fields
    refresh_token: Optional[str] = Field(None, description="Current refresh token for the doctor")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp for token refresh")


class DoctorCreate(DoctorBase):
    pass


class DoctorId(BaseModel):
    id: str


class Doctor(DoctorBase, DoctorId):
    pass


class DoctorUpdate(DoctorBase):
    pass


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email of the Doctor", example="john_doe@example.com")


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=6, description="New password for the Doctor", example="newPassword123")


class OTPRequest(BaseModel):
    email: EmailStr = Field(..., description="Email of the Doctor", example="john_doe@example.com")
    otp_code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code", example="123456")


class OTPResponse(BaseModel):
    message: str = Field(..., description="Response message")
    requires_otp: Optional[bool] = Field(None, description="Whether OTP verification is required")


class DoctorRefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token to exchange for new access token")


class DoctorTokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="Refresh token for getting new access tokens")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class ChatMessage(BaseModel):
    role: str  # 'user' or 'model'
    content: str

class QuestionRequest(BaseModel):
    question: str
    chatHistory: list[ChatMessage] = []


class Reference(BaseModel):
    title: str
    url: str
    originalUrl:str

class QuestionResponse(BaseModel):
    answer: str
    question: str
    references: list[Reference] = []

class PDFSummaryRequest(BaseModel):
    gsUrl: str