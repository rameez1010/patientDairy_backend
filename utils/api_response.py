from typing import Any, Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Unified API Response Model"""

    success: bool
    statusCode: int
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Error Response Model"""

    success: bool = False
    statusCode: int
    message: str
    errors: Optional[Any] = None


def create_success_response(data: Any = None, message: str = "Success!", status_code: int = 200) -> dict:
    """Create a standardized success response"""
    return {"success": True, "statusCode": status_code, "message": message, "data": data}


def create_error_response(message: str, status_code: int = 400, errors: Any = None) -> dict:
    """Create a standardized error response"""
    return {"success": False, "statusCode": status_code, "message": message, "errors": errors}


def success_response(data: Any = None, message: str = "Success!", status_code: int = 200) -> JSONResponse:
    """Return a JSONResponse with success format"""
    response_data = create_success_response(data, message, status_code)
    return JSONResponse(status_code=status_code, content=response_data)


def error_response(message: str, status_code: int = 400, errors: Any = None) -> JSONResponse:
    """Return a JSONResponse with error format"""
    response_data = create_error_response(message, status_code, errors)
    return JSONResponse(status_code=status_code, content=response_data)


def handle_http_exception(exc: HTTPException) -> JSONResponse:
    """Convert HTTPException to unified error response"""
    return error_response(message=exc.detail, status_code=exc.status_code)


def handle_generic_exception(exc: Exception) -> JSONResponse:
    """Convert generic exception to unified error response"""
    return error_response(message=f"Internal server error: {str(exc)}", status_code=500)
