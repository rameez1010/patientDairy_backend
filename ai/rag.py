import os
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini

from models.patient_models import Patient
from config.env_config import settings

GOOGLE_API_KEY = settings.GOOGLE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def patient_rag_function(query: str, patient: Patient) -> str:
    # Embeddings model
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    # Create a Document object from the patient data
    documents = [Document(text=str(patient))]

    # Language model
    # Settings.llm = Ollama(model="llama3", request_timeout=360.0)
    Settings.llm = Gemini(model="models/gemini-2.0-flash-001")

    # Create index
    index = VectorStoreIndex.from_documents(documents)

    # Perform RAG query
    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    return response.response if hasattr(response, "response") else str(response)
