import asyncio
from typing import AsyncGenerator

from google import genai
from google.genai import types
from modules.ai_knowledge.medical_prompt_utils import get_medical_system_prompt, get_medical_pdf_summary_prompt
from utils.gcs_signed_url import generate_signed_url
import os

class AIKnowledgeService:
    def __init__(self):
        """Initialize the AI Knowledge service with Vertex AI client."""
        self.client = genai.Client(
        vertexai=True,
        project="sodium-binder-419220",
        location="global",
        )
        self.model = "gemini-2.5-flash-lite"
        
        # RAG tools configuration
        self.tools = [
            types.Tool(
                retrieval=types.Retrieval(
                    vertex_rag_store=types.VertexRagStore(
                        rag_resources=[
                            types.VertexRagStoreRagResource(
                                rag_corpus="projects/sodium-binder-419220/locations/us-central1/ragCorpora/6917529027641081856"
                            )
                        ],
                        similarity_top_k=5,
                    )
                )
            )
  ]
        
        # Generation configuration
        self.generate_content_config = types.GenerateContentConfig(
            temperature = 1,
            top_p = 0.95,
            max_output_tokens = 65535,
            system_instruction=[types.Part.from_text(text=get_medical_system_prompt())],
            safety_settings = [types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )],
            tools = self.tools,
            thinking_config=types.ThinkingConfig(
                thinking_budget=0,
            )
        )

    async def process_question(self, question: str, chat_history: list = None) -> str:
        """
        Process a question using Vertex AI RAG pipeline and return the complete response.
        
        Args:
            question (str): The medical question to process
            
        Returns:
            str: The AI-generated response
        """
        try:
            print(f"Processing question: {question}")
            if chat_history is None:
                chat_history = []
            contents = []

            for msg in chat_history:
                if hasattr(msg, 'dict'):
                    msg_obj = msg.dict()
                elif isinstance(msg, dict):
                    msg_obj = msg
                else:
                    continue
                role = msg_obj.get('role')
                content = msg_obj.get('content')
                if role in ("user", "model") and content:
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=content)]
                        )
                    )

            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=question)]
                )
            )
            
            # Generate response using non-streaming approach
            reference_objs = []
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=self.generate_content_config,
            )

            # Safely extract response text
            try:
                if not response or not hasattr(response, 'candidates') or not response.candidates:
                    complete_response = "I apologize, but I couldn't generate a response at this time."
                elif not response.candidates[0] or not hasattr(response.candidates[0], 'content') or not response.candidates[0].content:
                    complete_response = "I apologize, but I couldn't generate a response at this time."
                elif not hasattr(response.candidates[0].content, 'parts') or not response.candidates[0].content.parts:
                    complete_response = "I apologize, but I couldn't generate a response at this time."
                else:
                    try:
                        complete_response = response.text or "I apologize, but I couldn't generate a response at this time."
                    except Exception as e:
                        print(f"Error extracting response text: {e}")
                        complete_response = "I apologize, but I couldn't generate a response at this time."
            except Exception as e:
                print(f"Error processing response: {e}")
                complete_response = "I apologize, but I couldn't generate a response at this time."
            
            print(complete_response)
            
            # Safely extract reference links from grounding_metadata
            try:
                if response and hasattr(response, 'candidates') and response.candidates:
                    try:
                        candidate = response.candidates[0]
                        if candidate:
                            grounding_metadata = getattr(candidate, "grounding_metadata", None)
                            if grounding_metadata and hasattr(grounding_metadata, "grounding_chunks") and grounding_metadata.grounding_chunks:
                                try:
                                    for chunk_info in grounding_metadata.grounding_chunks:
                                        try:
                                            retrieved_context = getattr(chunk_info, "retrieved_context", None)
                                            if retrieved_context:
                                                uri = getattr(retrieved_context, "uri", None)
                                                if uri:
                                                    title = getattr(retrieved_context, "title", None) or getattr(retrieved_context, "description", None) or uri
                                                    ref = {"title": str(title or uri), "url": str(uri)}
                                                    if ref not in reference_objs:
                                                        reference_objs.append(ref)
                                        except Exception as e:
                                            print(f"Error processing chunk_info: {e}")
                                            continue
                                except Exception as e:
                                    print(f"Error iterating grounding_chunks: {e}")
                    except Exception as e:
                        print(f"Error accessing candidate: {e}")
            except Exception as e:
                print(f"Error extracting references: {e}")

            # Safely process signed references
            signed_references = []
            try:
                for ref_obj in reference_objs:
                    try:
                        if not isinstance(ref_obj, dict) or "url" not in ref_obj or "title" not in ref_obj:
                            continue
                        url = str(ref_obj.get("url", ""))
                        title = str(ref_obj.get("title", ""))
                        if not url or not title:
                            continue
                        signed_url = url
                        if url.startswith("gs://"):
                            try:
                                signed_url = generate_signed_url(url, expiration_minutes=300)
                            except Exception as e:
                                print(f"Failed to sign reference {url}: {e}")
                                signed_url = url  # Use original URL if signing fails
                        signed_references.append({"title": title, "url": signed_url, "originalUrl": url})
                    except Exception as e:
                        print(f"Error processing reference object: {e}")
                        continue
            except Exception as e:
                print(f"Error processing signed references: {e}")
                signed_references = []

            print(f"Generated response length: {len(complete_response)} characters")

            # Suppress references for fallback/negative answers
            fallback_phrases = [
                "I couldn't find information",
                "I could not find information",
                "I do not have that information",
                "I'm sorry, I couldn't find information",
                "I'm sorry, I could not find information",
                "Sorry, I couldn't find information",
                "Sorry, I could not find information",
                "Sorry, I do not have that information"
            ]
            if any(phrase in complete_response for phrase in fallback_phrases):
                signed_references = []

            return {"answer": complete_response, "references": signed_references}
            
        except Exception as e:
            print(f"Error in process_question: {str(e)}")
            raise Exception(f"Failed to process question with Vertex AI: {str(e)}")
            

    async def summarize_pdf(self, gs_url: str, prompt: str = None) -> str:
        """
        Summarize a PDF file from a given GCS (gs://) URL using Vertex AI file API.
        Args:
            gs_url: The gs:// URL of the PDF file in Vertex AI
            prompt: Optional custom prompt for summarization
        Returns:
            The summary text
        """

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(file_uri=gs_url, mime_type="application/pdf"),
                    types.Part.from_text(text=get_medical_pdf_summary_prompt())
                ]
            )
        ]
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
        )
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'candidates') and response.candidates and hasattr(response.candidates[0], 'text'):
            return response.candidates[0].text
        else:
            return "No summary could be generated from the PDF."