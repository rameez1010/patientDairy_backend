from fastapi import APIRouter

from models.recommendation_models import RecommendationCreate, RecommendationUpdate
from modules.recommendation.recommendation_service import RecommendationService
from utils.api_response import APIResponse, error_response, success_response

# Create router
recommendation_router = APIRouter(prefix="/recommendation", tags=["recommendation"])
recommendation_service = RecommendationService()


@recommendation_router.get("/bloodwork", response_model=APIResponse)
async def get_bloodwork_recommendations():
    """
    Get all recommendations for bloodwork family
    """
    try:
        recommendations = await recommendation_service.get_recommendations_by_family("bloodwork")
        recommendations = [r.model_dump() for r in recommendations]

        return success_response(
            data=recommendations, message="Bloodwork recommendations retrieved successfully", status_code=200
        )
    except Exception as e:
        return error_response(message=f"Failed to retrieve bloodwork recommendations: {str(e)}", status_code=500)


@recommendation_router.post("/bloodwork", response_model=APIResponse)
async def add_bloodwork_recommendation(
    recommendation: RecommendationCreate,
):
    """
    Add a new recommendation for bloodwork family
    """
    try:
        # Ensure the recommendation is for bloodwork family
        if recommendation.recommendation_family != "bloodwork":
            recommendation.recommendation_family = "bloodwork"

        # Add the recommendation
        created_recommendation = await recommendation_service.add_recommendation(recommendation)
        created_recommendation = created_recommendation.model_dump()

        return success_response(
            data=created_recommendation, message="Bloodwork recommendation added successfully", status_code=201
        )
    except Exception as e:
        return error_response(message=f"Failed to add bloodwork recommendation: {str(e)}", status_code=500)


@recommendation_router.get("/bloodwork/{group}", response_model=APIResponse)
async def get_bloodwork_recommendations_by_group(
    group: str,
):
    """
    Get all recommendations for bloodwork family and specific biomarker group
    """
    try:
        recommendations = await recommendation_service.get_recommendations_by_family_and_group("bloodwork", group)
        recommendations = [r.model_dump() for r in recommendations]
        return success_response(
            data=recommendations,
            message=f"Bloodwork recommendations for group '{group}' retrieved successfully",
            status_code=200,
        )
    except Exception as e:
        return error_response(
            message=f"Failed to retrieve bloodwork recommendations for group '{group}': {str(e)}", status_code=500
        )


@recommendation_router.get("/{id}", response_model=APIResponse)
async def get_recommendation_by_id(
    id: str,
):
    """
    Get a recommendation by ID
    """
    try:
        recommendation = await recommendation_service.get_recommendation_by_id(id)
        recommendation = recommendation.model_dump()

        if not recommendation:
            return error_response(message="Recommendation not found", status_code=404)
        return success_response(data=recommendation, message="Recommendation retrieved successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to retrieve recommendation: {str(e)}", status_code=500)


@recommendation_router.put("/{id}", response_model=APIResponse)
async def update_recommendation(
    id: str,
    update_data: RecommendationUpdate,
):
    """
    Update a recommendation by ID
    """
    try:
        # Convert to dict and remove None values
        update_dict = update_data.model_dump(exclude_unset=True)

        # Update recommendation
        updated_recommendation = await recommendation_service.update_recommendation(id, update_dict)
        updated_recommendation = updated_recommendation.model_dump()
        if not updated_recommendation:
            return error_response(message="Recommendation not found", status_code=404)

        return success_response(
            data=updated_recommendation, message="Recommendation updated successfully", status_code=200
        )
    except Exception as e:
        return error_response(message=f"Failed to update recommendation: {str(e)}", status_code=500)


@recommendation_router.delete("/{id}", response_model=APIResponse)
async def delete_recommendation(
    id: str,
):
    """
    Delete a recommendation by ID
    """
    try:
        deleted = await recommendation_service.delete_recommendation(id)
        if not deleted:
            return error_response(message="Recommendation not found", status_code=404)

        return success_response(message="Recommendation deleted successfully", status_code=200)
    except Exception as e:
        return error_response(message=f"Failed to delete recommendation: {str(e)}", status_code=500)
