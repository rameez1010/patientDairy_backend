import os
import tempfile
from google.cloud import firestore
from config.env_config import settings

if settings.ENVIRONMENT != "production":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestore.json"
database_id = "production-db" if settings.ENVIRONMENT == "production" else "(default)"

try:
    db = firestore.AsyncClient(database=database_id)
    doctors_collection = db.collection("doctors")
    patients_collection = db.collection("patients")
    recommendations_collection = db.collection("recommendations")
    pdf_summaries_collection = db.collection("pdf_summaries")
except Exception as e:
    raise RuntimeError(f"Failed to initialize Firestore: {str(e)}")
