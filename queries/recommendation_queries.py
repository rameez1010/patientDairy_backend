from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from config.config import recommendations_collection
from models.recommendation_models import RecommendationCreate, RecommendationResponse

recommendations_collection = recommendations_collection

async def get_recommendations_by_family(family: str) -> List[RecommendationResponse]:

    query = recommendations_collection.where('recommendation_family', '==', family)
    recommendations = []
    
    # Stream the documents and convert to response models
    docs = query.stream()
    async for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        recommendations.append(RecommendationResponse(**data))
        
    return recommendations

async def get_recommendations_by_family_and_group(family: str, group: str) -> List[RecommendationResponse]:

    query = recommendations_collection.where('recommendation_family', '==', family).where('biomarker_group', '==', group)
    recommendations = []
    
    # Stream the documents and convert to response models
    docs = query.stream()
    async for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        recommendations.append(RecommendationResponse(**data))
        
    return recommendations

async def add_recommendation(recommendation: RecommendationCreate) -> RecommendationResponse:
    
    # Check if a recommendation with the same family and biomarker_group already exists
    query = recommendations_collection.where('recommendation_family', '==', recommendation.recommendation_family).where('biomarker_group', '==', recommendation.biomarker_group)
    docs = query.stream()
    
    existing = False
    async for _ in docs:
        existing = True
        break
    
    if existing:
        raise HTTPException(status_code=409, detail=f"A recommendation with family '{recommendation.recommendation_family}' and group '{recommendation.biomarker_group}' already exists")
    
    # If no existing recommendation is found, create a new one
    recommendation_dict = recommendation.model_dump(exclude={'id'})
    
    doc_ref = recommendations_collection.document()
    await doc_ref.set(recommendation_dict)
    
    return RecommendationResponse(**recommendation_dict, id=doc_ref.id)


async def get_recommendation_by_id(recommendation_id: str) -> Optional[RecommendationResponse]:

    doc_ref = recommendations_collection.document(recommendation_id)
    doc = await doc_ref.get()
    
    if not doc.exists:
        return None
        
    data = doc.to_dict()
    data['id'] = doc.id
    return RecommendationResponse(**data)

async def update_recommendation(recommendation_id: str, update_data: Dict[str, Any]) -> Optional[RecommendationResponse]:

    doc_ref = recommendations_collection.document(recommendation_id)
    doc = await doc_ref.get()
    
    if not doc.exists:
        return None
        
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    await doc_ref.update(update_data)
    
    updated_doc = await doc_ref.get()
    data = updated_doc.to_dict()
    data['id'] = recommendation_id
    
    return RecommendationResponse(**data)

async def delete_recommendation(recommendation_id: str) -> bool:

    doc_ref = recommendations_collection.document(recommendation_id)
    doc = await doc_ref.get()
    
    if not doc.exists:
        return False
        
    await doc_ref.delete()
    return True 