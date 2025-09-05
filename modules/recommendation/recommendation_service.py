from typing import Any, Dict, List, Optional

from models.recommendation_models import RecommendationCreate, RecommendationResponse
from queries.recommendation_queries import add_recommendation as add_recommendation_query
from queries.recommendation_queries import delete_recommendation as delete_recommendation_query
from queries.recommendation_queries import (
    get_recommendation_by_id,
    get_recommendations_by_family,
    get_recommendations_by_family_and_group,
)
from queries.recommendation_queries import update_recommendation as update_recommendation_query


class RecommendationService:
    
    async def get_recommendations_by_family(self, family: str) -> List[RecommendationResponse]:
        
        return await get_recommendations_by_family(family)

    async def get_recommendations_by_family_and_group(self, family: str, group: str) -> List[RecommendationResponse]:
        
        return await get_recommendations_by_family_and_group(family, group)

    async def add_recommendation(self, recommendation: RecommendationCreate) -> RecommendationResponse:
        
        return await add_recommendation_query(recommendation)

    async def get_recommendation_by_id(self, recommendation_id: str) -> Optional[RecommendationResponse]:
        
        return await get_recommendation_by_id(recommendation_id)

    async def update_recommendation(self, recommendation_id: str, update_data: Dict[str, Any]) -> Optional[RecommendationResponse]:
        
        return await update_recommendation_query(recommendation_id, update_data)

    async def delete_recommendation(self, recommendation_id: str) -> bool:
        
        return await delete_recommendation_query(recommendation_id) 