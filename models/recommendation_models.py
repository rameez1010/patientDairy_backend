from typing import List, Optional

from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    action: str = Field(..., description="The recommendation action")
    details: List[str] = Field(..., description="Detailed breakdown of the recommendation")


class Recommendation(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the recommendation")
    recommendation_family: str = Field(..., description="Family of the recommendation (e.g., bloodwork, hormones)")
    biomarker_group: str = Field(..., description="Group of biomarkers (e.g., lipids, glucose)")
    diet: List[ActionItem] = Field(default_factory=list, description="Diet recommendations")
    activity: List[ActionItem] = Field(default_factory=list, description="Activity recommendations")
    lifestyle: List[ActionItem] = Field(default_factory=list, description="Lifestyle recommendations")
    supplements: List[ActionItem] = Field(default_factory=list, description="Supplements recommendations")

    class Config:
        json_schema_extra = {
            "example": {
                "recommendation_family": "bloodwork",
                "biomarker_group": "lipids",
                "diet": [
                    {
                        "action": "Limit unhealthy fats",
                        "details": [
                            "Limit saturated fats (processed foods)",
                            "Consume red meats and/or plant-based proteins",
                            "Avoid trans fats (fried foods, baked goods, margarine) that raise LDL and lower HDL cholesterol",
                        ],
                    },
                    {
                        "action": "Increase fiber",
                        "details": ["Consume oats, beans, veggies to help lower LDL cholesterol"],
                    },
                    {
                        "action": "Use healthy fats",
                        "details": ["Use olive oil, avocado, fatty fish instead of unhealthy fats"],
                    },
                ],
                "activity": [
                    {
                        "action": "Exercise",
                        "details": [
                            "30 min of aerobic exercise (walking, cycling) to raise HDL and lower LDL cholesterol"
                        ],
                    },
                    {
                        "action": "Strength training",
                        "details": ["Twice a week to improve heart health and reduce cholesterol"],
                    },
                    {
                        "action": "More movement",
                        "details": ["Gardening, walking, or taking stairs", "75 minutes of vigorous activity"],
                    },
                ],
                "lifestyle": [
                    {
                        "action": "Quit smoking",
                        "details": ["Smoking cessation improves HDL cholesterol and reduces cardiovascular risk"],
                    },
                    {
                        "action": "Limit alcohol",
                        "details": [
                            "Restrict alcohol to 2 drinks/day to prevent negative effects on cholesterol levels",
                            "Restrict alcohol to 1 drink/day to prevent negative effects on cholesterol levels",
                        ],
                    },
                    {
                        "action": "Weight loss",
                        "details": ["Losing 5-10% body weight improves lipids, lowers LDL/triglycerides, raises HDL"],
                    },
                ],
                "supplements": [
                    {
                        "action": "Introduce Desiccated Thyroid",
                        "details": [
                            "Increase dose by 30 mg when Free T3 is suboptimal (below 4.8 pmol/L)",
                            "Used to address symptoms of hypothyroidism including fatigue, weight gain, cold intolerance",
                            "Decrease dose by 30 mg if side effects occur (palpitations, tachycardia, anxiety, etc.)",
                        ],
                    },
                ],
            }
        }


class RecommendationCreate(Recommendation):
    recommendation_family: str = Field(..., description="Family of the recommendation (e.g., bloodwork, hormones)")
    biomarker_group: str = Field(..., description="Group of biomarkers (e.g., lipids, glucose)")
    diet: List[ActionItem] = Field(default_factory=list, description="Diet recommendations")
    activity: List[ActionItem] = Field(default_factory=list, description="Activity recommendations")
    lifestyle: List[ActionItem] = Field(default_factory=list, description="Lifestyle recommendations")
    supplements: List[ActionItem] = Field(default_factory=list, description="Supplements recommendations")


class RecommendationResponse(Recommendation):
    id: str = Field(..., description="Unique identifier for the recommendation")


class RecommendationUpdate(BaseModel):
    recommendation_family: Optional[str] = Field(
        None, description="Family of the recommendation (e.g., bloodwork, hormones)"
    )
    biomarker_group: Optional[str] = Field(None, description="Group of biomarkers (e.g., lipids, glucose)")
    diet: Optional[List[ActionItem]] = Field(None, description="Diet recommendations")
    activity: Optional[List[ActionItem]] = Field(None, description="Activity recommendations")
    lifestyle: Optional[List[ActionItem]] = Field(None, description="Lifestyle recommendations")
    supplements: Optional[List[ActionItem]] = Field(None, description="Supplements recommendations")
