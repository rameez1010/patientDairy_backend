from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from auth.token import get_current_doctor_id
from models.doctor_models import DoctorId, QuestionRequest, QuestionResponse, PDFSummaryRequest
from modules.ai_knowledge.ai_knowledge_service import AIKnowledgeService
from utils.api_response import APIResponse, error_response, success_response
from utils.helpers import serialize_firestore_data
from queries.pdf_summary_queries import get_pdf_summary, set_pdf_summary

ai_knowledge_router = APIRouter(prefix="/ai-knowledge", tags=["ai-knowledge"])
ai_knowledge_service = AIKnowledgeService()


@ai_knowledge_router.post("/ask", response_model=APIResponse)
async def ask_question(
    request: QuestionRequest,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    """
    Ask a question to the AI Knowledge system using RAG pipeline.
    This endpoint processes medical questions using Vertex AI and returns responses
    based on the medical knowledge corpus.
    """
    chat_history = request.chatHistory if hasattr(request, 'chatHistory') else []
    try:
        print(f"Processing question from doctor {doctor_id}: {request.question}")
        result = await ai_knowledge_service.process_question(request.question, chat_history=chat_history)
        response_data = QuestionResponse(
            answer=result["answer"],
            question=request.question,
            references=result.get("references", [])
        )

        return success_response(
            data=serialize_firestore_data(response_data.dict()),
            message="Question processed successfully"
        )
    except Exception as e:
        print(f"Error processing question: {str(e)}")
        return error_response(
           message=f"Error generating response: {str(e)}", status_code=500
        )


@ai_knowledge_router.post("/summarize-pdf", response_model=APIResponse)
async def summarize_pdf(
    request: PDFSummaryRequest,
    doctor_id: DoctorId = Depends(get_current_doctor_id),
):
    """
    Summarize a PDF file from a Vertex AI GCS URL using Vertex AI file API.
    Implements caching: returns cached summary if exists, otherwise generates and stores it.
    """
    try:
        print(f"Summarizing PDF for doctor {doctor_id}: {request.gsUrl}")
        cached = await get_pdf_summary(request.gsUrl)
        
        if cached and cached.get("summary"):
            return success_response(data={"summary": cached["summary"], "cached": True}, message="PDF summary retrieved from cache")

        summary = await ai_knowledge_service.summarize_pdf(request.gsUrl)
        
        await set_pdf_summary(request.gsUrl, title=request.gsUrl.split('/')[-1], summary=summary)
        return success_response(data={"summary": summary, "cached": False}, message="PDF summarized successfully")
    except Exception as e:
        print(f"Error summarizing PDF: {str(e)}")
        return error_response(message=f"Error summarizing PDF: {str(e)}", status_code=500)


