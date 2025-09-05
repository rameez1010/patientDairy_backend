from typing import Any, Dict, List, Optional

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from utils.api_response import error_response


class ValidationErrorDetail(BaseModel):
    """Individual validation error detail"""

    field: str
    message: str
    value: Any
    type: str


class ValidationErrorResponse(BaseModel):
    """Structured validation error response"""

    field: str
    message: str
    value: Any
    type: str
    suggestions: Optional[List[str]] = None


def format_validation_error(error: RequestValidationError) -> List[ValidationErrorResponse]:
    """
    Format FastAPI request validation errors into a frontend-friendly structure
    """
    formatted_errors = []

    for error_detail in error.errors():
        # Extract field path
        field_path = ".".join(str(loc) for loc in error_detail["loc"])

        # Get the error type and message
        error_type = error_detail["type"]
        error_message = error_detail["msg"]
        input_value = error_detail.get("input")

        # Create user-friendly messages based on error type
        user_message = get_user_friendly_message(error_type, error_message, field_path)

        # Get suggestions for common validation errors
        suggestions = get_validation_suggestions(error_type, field_path)

        formatted_errors.append(
            ValidationErrorResponse(
                field=field_path, message=user_message, value=input_value, type=error_type, suggestions=suggestions
            )
        )

    return formatted_errors


def get_user_friendly_message(error_type: str, original_message: str, field_path: str) -> str:
    """
    Convert technical validation messages to user-friendly messages
    """

    print("--------------------------------")
    print(error_type)
    print("--------------------------------")
    field_name = field_path.split(".")[-1] if "." in field_path else field_path

    # Common error type mappings
    error_messages = {
        "int_parsing": f"'{field_name}' must be a whole number",
        "float_parsing": f"'{field_name}' must be a valid number",
        "string_type": f"'{field_name}' must be text",
        "boolean_type": f"'{field_name}' must be yes or no",
        "email": f"'{field_name}' must be a valid email address",
        "url": f"'{field_name}' must be a valid URL",
        "date": f"'{field_name}' must be a valid date",
        "datetime": f"'{field_name}' must be a valid date and time",
        "missing": f"'{field_name}' is required",
        "value_error": f"'{field_name}' has an invalid value",
        "type_error": f"'{field_name}' has an incorrect type",
        "length": f"'{field_name}' has an invalid length",
        "min_length": f"'{field_name}' is too short",
        "max_length": f"'{field_name}' is too long",
        "min_value": f"'{field_name}' is too small",
        "max_value": f"'{field_name}' is too large",
        "regex": f"'{field_name}' format is invalid",
        "uuid": f"'{field_name}' must be a valid ID",
        "json": f"'{field_name}' must be valid JSON",
        "enum": f"'{field_name}' must be one of the allowed values",
        "literal_error": f"'{field_name}' must be one of the allowed values",
        "list_type": f"'{field_name}' must be a list",
        "dict_type": f"'{field_name}' must be an object",
    }

    # Special handling for missing required fields
    if error_type == "missing":
        # Map field names to more user-friendly names
        field_mapping = {
            "fullName": "Full name",
            "address": "Address",
            "phone": "Phone number",
            "email": "Email address",
            "dateOfBirth": "Date of birth",
            "age": "Age",
            "maritalStatus": "Marital status",
            "gender": "Gender",
            "weight": "Weight",
            "height": "Height",
            "bloodPressure": "Blood pressure",
            "primaryCareProvider": "Primary care provider",
            "generalSymptoms": "General symptoms",
            "additionalSymptoms": "Additional symptoms",
            "symptomDuration": "Symptom duration",
            "symptomTiming": "Symptom timing",
            "symptomImpact": "Symptom impact",
            "pastMedicalHistory": "Past medical history",
            "cardiacHistory": "Cardiac history",
            "conditions": "Family conditions",
            "fatherAgeOrDeath": "Father's age or death",
            "fatherHealthStatus": "Father's health status",
            "motherAgeOrDeath": "Mother's age or death",
            "motherHealthStatus": "Mother's health status",
            "lastPhysicalExam": "Last physical exam date",
            "allergies": "Allergies",
            "medicationsAndSupplements": "Medications and supplements",
            "smokingOrCannabis": "Smoking or cannabis use",
            "alcoholConsumption": "Alcohol consumption",
            "exerciseRegimen": "Exercise regimen",
            "desireForChildren": "Desire for children",
            "referralSource": "Referral source",
            "acceptedTerms": "Terms acceptance",
            "signature": "Signature",
            "healthCardNumber": "Health card number",
            "menstrualProblems": "Menstrual problems",
            "ageAtFirstPeriod": "Age at first period",
            "cycleRegularity": "Cycle regularity",
            "flowType": "Flow type",
            "lastMenstrualCycle": "Last menstrual cycle",
            "hasSymptoms": "Premenstrual symptoms",
            "total": "Number of miscarriages",
            "gestationAge": "Gestation age",
            "used": "Usage status",
            "firstName": "First name",
            "lastName": "Last name",
            "practitioner": "Practitioner name",
            "password": "Password",
        }

        friendly_name = field_mapping.get(field_name, field_name)
        return f"{friendly_name} is required"

    return error_messages.get(error_type, f"'{field_name}' is invalid: {original_message}")


def get_validation_suggestions(error_type: str, field_path: str) -> Optional[List[str]]:
    """
    Provide helpful suggestions for common validation errors
    """
    field_name = field_path.split(".")[-1] if "." in field_path else field_path

    suggestions_map = {
        "int_parsing": [
            "Enter a whole number without decimals",
            "Remove any letters or special characters",
            "Make sure the field is not empty",
        ],
        "float_parsing": [
            "Enter a valid number (can include decimals)",
            "Use dot (.) as decimal separator",
            "Remove any letters or special characters",
        ],
        "email": [
            "Enter a valid email address (e.g., user@example.com)",
            "Make sure to include @ symbol",
            "Check for typos in the email address",
        ],
        "missing": [
            "This field is required",
            "Please fill in all required fields",
            "Complete this section before proceeding",
        ],
        "min_length": [
            "Enter at least the minimum required characters",
            "Add more details to meet the minimum requirement",
        ],
        "max_length": ["Shorten your input to meet the maximum limit", "Be more concise in your response"],
        "date": [
            "Use format: YYYY-MM-DD (e.g., 2024-01-15)",
            "Make sure the date is valid",
            "Check for typos in the date",
        ],
        "phone": [
            "Enter a valid phone number",
            "Include country code if required",
            "Use only numbers and basic symbols (+, -, spaces)",
        ],
        "enum": ["Please select one of the allowed values", "Check the available options and try again"],
        "literal_error": [
            "Please select one of the allowed values",
            "For gender, use 'male' or 'female'",
            "Check the available options and try again",
        ],
    }

    return suggestions_map.get(error_type)


def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle FastAPI request validation errors and return structured response
    """
    formatted_errors = format_validation_error(exc)

    # Group errors by field for easier frontend processing
    errors_by_field = {}
    for error in formatted_errors:
        if error.field not in errors_by_field:
            errors_by_field[error.field] = []
        errors_by_field[error.field].append(
            {"message": error.message, "type": error.type, "value": error.value, "suggestions": error.suggestions}
        )

    # Convert ValidationErrorResponse objects to dictionaries for JSON serialization
    validation_errors_dict = [error.model_dump() for error in formatted_errors]

    # Create a comprehensive error response
    error_data = {
        "validation_errors": validation_errors_dict,
        "errors_by_field": errors_by_field,
        "total_errors": len(formatted_errors),
        "fields_with_errors": list(errors_by_field.keys()),
    }

    return error_response(
        message="Validation failed. Please check the form and try again.", status_code=422, errors=error_data
    )


def create_field_specific_validation_error(
    field: str, message: str, error_type: str = "validation_error"
) -> Dict[str, Any]:
    """
    Create a field-specific validation error for manual validation
    """
    return {
        "field": field,
        "message": message,
        "type": error_type,
        "value": None,
        "suggestions": get_validation_suggestions(error_type, field),
    }


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[Dict[str, Any]]:
    """
    Manually validate required fields and return structured errors
    """
    errors = []

    for field in required_fields:
        if field not in data or data[field] is None or (isinstance(data[field], str) and data[field].strip() == ""):
            errors.append(
                create_field_specific_validation_error(
                    field=field, message=f"'{field}' is required", error_type="missing"
                )
            )

    return errors
