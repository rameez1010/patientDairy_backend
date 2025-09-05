import os
import json

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini
from config.env_config import settings

GOOGLE_API_KEY = settings.GOOGLE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Load recommendations data
with open("ai/recommendations.json", "r") as f:
    recommendations_data = json.load(f)


def patient_recommendation_function(latest_blood_work: str) -> str:
    """
    Simpler approach using direct LLM prompting with recommendations context
    Returns structured JSON string response
    """
    Settings.llm = Gemini(model="models/gemini-2.0-flash-001")

    # Convert recommendations to text for context
    recommendations_text = json.dumps(recommendations_data, indent=2)

    prompt = f"""
    You are a health recommendations AI. Analyze the following blood work results and provide targeted, specific recommendations.
    
    BLOOD WORK RESULTS:
    {latest_blood_work}
    
    AVAILABLE RECOMMENDATIONS CONTEXT:
    {recommendations_text}
    
    INSTRUCTIONS:
    1. Identify which biomarkers are abnormal or normal
    2. Focus on the most concerning findings
    3. Select only the most relevant recommendations
    4. Prioritize recommendations that directly address abnormal biomarkers
    5. Format your response as valid JSON with the structure shown below
    
    RESPONSE FORMAT (ALWAYS OUTPUT VALID JSON):
    {{
        "key_findings": {{
            "Lipids": [
                {{
                    "biomarker": "HDL Cholesterol",
                    "value": "1.21 mmol/L",
                    "status": "low"
                }}
            ],
            "Vitamins": [
                {{
                    "biomarker": "Vitamin D",
                    "value": "539.4 nmol/L",
                    "status": "high"
                }}
            ]
        }},
        "priority_recommendations": [
            "Recommendation 1",
            "Recommendation 2"
        ],
        "specific_recommendations": {{
            "dietary": [
                {{
                    "action": "Increase healthy fats",
                    "details": ["avocados", "olive oil"]
                }}
            ],
            "lifestyle": [
                {{
                    "action": "Stress management",
                    "details": ["meditation", "yoga"]
                }}
            ],
            "supplements": [
                {{
                    "action": "Stop Vitamin D",
                    "details": ["until retested"]
                }}
            ]
        }},
        "important_considerations": [
            "Thyroid results require specialist attention",
            "DHEA elevation needs investigation"
        ]
    }}
    
    Only include fields with relevant data. Keep recommendations specific to the abnormal findings.
    """

    response = Settings.llm.complete(prompt)

    # Return the JSON string directly
    return str(response)
