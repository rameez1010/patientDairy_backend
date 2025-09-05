from datetime import datetime, timedelta, timezone
import random
import string


def generate_otp_code(length: int = 6) -> str:
    """
    Generate a random OTP code with specified length
    """
    return "".join(random.choices(string.digits, k=length))


def get_otp_expiration_time(minutes: int = 10) -> datetime:
    """
    Get OTP expiration time (default 10 minutes from now)
    """
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


def is_otp_expired(expires_at: datetime) -> bool:
    """
    Check if OTP has expired
    """
    if expires_at is None:
        return True
    return datetime.now(timezone.utc) > expires_at


def is_otp_valid(
    provided_otp: str,
    stored_otp: str,
    expires_at: datetime,
    is_verified: bool = False
) -> tuple[bool, str]:
    """
    Validate OTP code and return (is_valid, reason)
    """
    if is_verified:
        return False, "used"  # OTP already used

    if is_otp_expired(expires_at):
        return False, "expired"  # OTP expired

    if provided_otp != stored_otp:
        return False, "invalid"  # OTP doesn't match

    return True, "valid"
