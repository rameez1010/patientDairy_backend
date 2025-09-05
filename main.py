from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from modules.ai_knowledge.ai_knowledge_routes import ai_knowledge_router
from modules.fullscript.fullscript_routes import fullscript_router
from modules.medical_form.medical_form_routes import medical_form_router
from modules.patients.patient_routes import patients_router
from modules.recommendation.recommendation_routes import recommendation_router
from routes.doctor_route import doctor_router
from routes.patient_route import patient_router
from utils.api_response import handle_generic_exception, handle_http_exception
from utils.validation_errors import handle_validation_error

origins = ["*"]

app = FastAPI(title="Bio Krystal")

app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(patients_router)
app.include_router(recommendation_router)
app.include_router(fullscript_router)
app.include_router(medical_form_router)
app.include_router(ai_knowledge_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTPExceptions and convert to unified response format"""
    return handle_http_exception(exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle FastAPI request validation errors and convert to structured response format"""
    return handle_validation_error(request, exc)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions and convert to unified response format"""
    return handle_generic_exception(exc)
