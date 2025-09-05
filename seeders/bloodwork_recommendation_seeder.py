import asyncio
import os
import sys

from config.config import recommendations_collection
from models.recommendation_models import ActionItem, RecommendationCreate

# Add the parent directory to sys.path to allow importing from the root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the bloodwork recommendations data
BLOODWORK_RECOMMENDATIONS = {
    "lipids": {
        "diet": [
            {
                "action": "Limit unhealthy fats",
                "details": [
                    "Limit saturated fats (processed foods)",
                    "Consume red meats and/or plant-based proteins",
                    "Avoid trans fats (fried foods, baked goods, margarine) that raise LDL and lower HDL cholesterol",
                ],
            },
            {"action": "Increase fiber", "details": ["Consume oats, beans, veggies to help lower LDL cholesterol"]},
            {"action": "Use healthy fats", "details": ["Use olive oil, avocado, fatty fish instead of unhealthy fats"]},
        ],
        "activity": [
            {
                "action": "Excersise",
                "details": ["30 min of aerobic exercise (walking, cycling) to raise HDL and lower LDL cholesterol"],
            },
            {"action": "Strength training", "details": ["Twice a week to improve heart health and reduce cholesterol"]},
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
    },
    "glucose": {
        "diet": [
            {
                "action": "Balanced meals",
                "details": [
                    "Include lean proteins, healthy fats (olive oil, avocado)",
                    "Add complex carbs (whole grains, legumes) to stabilize blood sugar",
                ],
            },
            {
                "action": "Low glycemic foods",
                "details": ["Incorporate leafy greens, whole grains, and vegetables to prevent rapid glucose spikes"],
            },
            {
                "action": "Increase fiber",
                "details": ["Eat oats, beans, fruits, and veggies to manage glucose and improve health"],
            },
            {
                "action": "Limit refined carbs",
                "details": ["Avoid sugary foods, sweetened beverages, baked goods, and processed snacks"],
            },
            {
                "action": "Control portions",
                "details": ["Moderate portions prevent overeating and elevated blood sugar"],
            },
            {
                "action": "Stay hydrated",
                "details": ["Drink 8-10 glasses of water daily to support kidney function and glucose regulation"],
            },
        ],
        "activity": [
            {
                "action": "Regular cardio",
                "details": [
                    "150 minutes of moderate exercise (walking, cycling, swimming) weekly to improve insulin sensitivity"
                ],
            },
            {
                "action": "Strength training",
                "details": ["Muscle-building activities twice a week to improve glucose utilization"],
            },
            {"action": "Post-meal activity", "details": ["Light walking after meals reduces post-meal glucose levels"]},
        ],
        "lifestyle": [
            {"action": "Quit smoking", "details": ["Improves insulin sensitivity and reduces health risks"]},
            {"action": "Limit alcohol", "details": ["1 drink/day for women, 2 for men to avoid raising blood sugar"]},
            {
                "action": "Weight loss",
                "details": ["Losing 5-10% of body weight improves insulin sensitivity and reduces HbA1C"],
            },
            {
                "action": "Reduce belly fat",
                "details": ["Focus on abdominal fat reduction to improve insulin resistance"],
            },
        ],
    },
    "renal": {
        "diet": [
            {
                "action": "Limit protein",
                "details": [
                    "Reduce dietary protein (0.6-0.8 g/kg/day) to ease kidney workload and prevent further damage",
                    "Especially in chronic kidney disease (CKD)",
                ],
            },
            {
                "action": "Lower sodium/potassium",
                "details": ["Avoid foods high in sodium and potassium to reduce strain on the kidneys"],
            },
            {
                "action": "Control phosphorus",
                "details": ["For CKD stages 3-5, limit phosphorus-rich foods and use phosphate binders if needed"],
            },
            {
                "action": "Maintain hydration",
                "details": [
                    "Drink adequate water to support kidney function and prevent dehydration-related creatinine spikes"
                ],
            },
        ],
        "activity": [
            {
                "action": "Avoid strain",
                "details": [
                    "Limit intense physical activity that could temporarily elevate creatinine due to muscle breakdown"
                ],
            }
        ],
    },
    "mineral": {
        "diet": [
            {
                "action": "Increase calcium-rich foods",
                "details": [
                    "Dairy, leafy greens, fortified plant milk, almonds",
                    "Pair with vitamin D sources (fatty fish, eggs, fortified foods)",
                ],
            },
            {
                "action": "Boost magnesium intake",
                "details": ["Eat leafy greens, nuts, seeds, legumes, fish, and dark chocolate"],
            },
            {
                "action": "Increase zinc-rich foods",
                "details": [
                    "Eat meat, poultry, shellfish, legumes, and nuts",
                    "Soak/sprout grains for better absorption (vegetarians)",
                ],
            },
            {
                "action": "Optimize iron intake",
                "details": ["For low ferritin: red meat, fish + vitamin C", "For high ferritin: limit iron/alcohol"],
            },
            {"action": "Add selenium sources", "details": ["Brazil nuts (2-6/day), fish, poultry, eggs"]},
        ]
    },
    "inflammation_Markers": {
        "diet": [
            {
                "action": "Eat anti-inflammatory foods",
                "details": [
                    "Fruits, vegetables, whole grains, healthy fats (olive oil, nuts, fatty fish)",
                    "Limit processed foods, refined sugars, and saturated fats",
                ],
            },
            {
                "action": "Increase omega-3 fatty acids",
                "details": ["Flaxseeds, chia seeds, fatty fish to reduce inflammation"],
            },
        ],
        "activity": [
            {
                "action": "Exercise regularly",
                "details": [
                    "At least 30 minutes daily (walking, cycling, swimming)",
                    "Align exercise with meal times for optimal benefits",
                ],
            }
        ],
        "lifestyle": [
            {
                "action": "Maintain a healthy weight",
                "details": ["Balanced eating and physical activity to reduce inflammation risk"],
            },
            {
                "action": "Manage stress",
                "details": [
                    "Meditation, deep breathing, spending time outdoors",
                    "Prevent chronic stress-related inflammation",
                ],
            },
            {"action": "Prioritize sleep", "details": ["7-9 hours of quality sleep nightly to regulate inflammation"]},
            {
                "action": "Avoid smoking & limit alcohol",
                "details": [
                    "Smoking and excessive alcohol exacerbate inflammation",
                    "Minimize or eliminate these habits",
                ],
            },
        ],
    },
    "vitamin": {
        "diet": [
            {
                "action": "Increase Vitamin B12 intake",
                "details": [
                    "Animal-based foods: meat, fish, eggs, dairy",
                    "For vegetarians/vegans: B12-fortified foods (plant-based milks, cereals, nutritional yeast)",
                    "Regular supplementation may be needed for at-risk groups (older adults, low gastric acid)",
                ],
            },
            {
                "action": "Boost Vitamin D sources",
                "details": [
                    "Fatty fish (salmon, mackerel), cod liver oil, eggs",
                    "Fortified foods: milk, plant-based alternatives (soy/almond), cereals, orange juice",
                    "Aim for 10-20 minutes of midday sun several times weekly",
                ],
            },
            {
                "action": "Optimize Vitamin A intake",
                "details": [
                    "Preformed vitamin A: liver, dairy, fish oils",
                    "Beta-carotene: colorful veggies (carrots, sweet potatoes, spinach), fruits (mangoes, apricots)",
                    "Fortified options for limited food access",
                ],
            },
        ],
        "lifestyle": [
            {
                "action": "Vitamin B12 considerations",
                "details": [
                    "Regular screening for at-risk groups",
                    "Supplementation (oral/injectable) if low gastric acid or plant-based diet",
                ],
            },
            {
                "action": "Vitamin D considerations",
                "details": [
                    "Ensure adequate sun exposure",
                    "Supplements if dietary intake is insufficient or in low-sunlight regions",
                ],
            },
            {
                "action": "Vitamin A considerations",
                "details": [
                    "Monitor intake for fat malabsorption/liver disease",
                    "May require higher doses/supplementation",
                    "Ensure adequate zinc for vitamin A metabolism",
                ],
            },
        ],
    },
    "electrolytes": {
        "diet": [
            {
                "action": "Manage sodium intake",
                "details": [
                    "Focus on fresh, whole foods, limit processed foods (<2,300 mg sodium/day)",
                    "Use herbs/spices instead of salt",
                ],
            },
            {
                "action": "Increase potassium-rich foods",
                "details": ["Bananas, oranges, spinach, potatoes", "Consider potassium-sparing diuretics if needed"],
            },
            {
                "action": "Optimize phosphorus intake",
                "details": ["Dairy, meat, nuts for most people", "Adjust phosphate binders for CKD patients"],
            },
        ],
        "lifestyle": [
            {
                "action": "Maintain proper hydration",
                "details": [
                    "Stay hydrated for sodium balance",
                    "Limit fluids (800-1,200 mL/day) for hyponatremia/SIADH",
                ],
            },
            {
                "action": "Limit dehydrating substances",
                "details": ["Reduce excessive caffeine/alcohol", "Increase water intake if consuming these"],
            },
        ],
    },
    "liver_Enzymes": {
        "diet": [
            {
                "action": "Eat a liver-friendly diet",
                "details": [
                    "Focus on fruits, vegetables, whole grains and choose lean proteins and healthy fats",
                    "Avoid alcohol, processed foods, sugary drinks",
                ],
            }
        ],
        "activity": [
            {
                "action": "Exercise regularly",
                "details": ["150-300 minutes of moderate exercise weekly", "Include weight-bearing activities"],
            },
            {
                "action": "Manage weight",
                "details": ["Lose 5-10% of body weight if overweight", "Improves liver function markers"],
            },
        ],
        "lifestyle": [
            {
                "action": "Eliminate alcohol",
                "details": ["Complete abstinence recommended to prevents further liver damage"],
            },
            {
                "action": "Reduce stress",
                "details": ["Practice yoga or meditation", "Chronic stress worsens liver inflammation"],
            },
            {"action": "Quit smoking", "details": ["Reduces systemic inflammation and supports liver regeneration"]},
            {
                "action": "Avoid toxins",
                "details": ["Limit environmental/industrial chemical exposure doing this reduces GGT elevation risk"],
            },
        ],
    },
    "thyroid_Functions": {
        "diet": [
            {
                "action": "Eat thyroid-supportive foods",
                "details": [
                    "Ensure adequate iodine, selenium, zinc, and iron",
                    "Focus on antioxidant-rich foods",
                    "Limit raw cruciferous vegetables if iodine low",
                    "Avoid excessive soy",
                ],
            },
            {
                "action": "Support gut health",
                "details": ["Use probiotics and digestive enzymes", "Address digestive issues promptly"],
            },
        ],
        "activity": [
            {
                "action": "Exercise regularly",
                "details": ["150 minutes moderate exercise weekly supports metabolism and thyroid function"],
            }
        ],
        "lifestyle": [
            {
                "action": "Reduce stress",
                "details": ["Practice meditation, deep breathing, yoga", "Chronic stress impairs thyroid function"],
            },
            {
                "action": "Minimize toxins",
                "details": [
                    "Avoid heavy metals and pesticides",
                    "Choose organic produce when possible",
                    "Use non-toxic household products",
                ],
            },
            {
                "action": "Optimize sleep",
                "details": ["Prioritize 7-9 hours quality sleep, it is essential for hormonal balance"],
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
            {
                "action": "Cytomel",
                "details": [
                    "Add 5 mcg daily when Free T3 remains suboptimal on levothyroxine",
                    "Increase by additional 5 mcg as tolerated when needed",
                    "Reduce by 5 mcg if side effects occur",
                    "Helps improve T3 levels when T4 to T3 conversion is impaired",
                ],
            },
            {
                "action": "Adjust Levothyroxine",
                "details": [
                    "Reduce by 25 mcg if side effects occur",
                    "Initial treatment for hypothyroidism symptoms",
                    "May require supplementation with T3 medications for optimal results",
                ],
            },
            {
                "action": "Monitor for side effects",
                "details": [
                    "Watch for palpitations, tachycardia, anxiety, restlessness, insomnia",
                    "Monitor for heat intolerance, excessive sweating, weight loss, tremors, headaches",
                    "Reduce appropriate medication if these symptoms occur",
                ],
            },
        ],
    },
    "hormone": {
        "diet": [
            {
                "action": "Eat a hormone-supportive diet",
                "details": [
                    "Focus on fruits, vegetables, whole grains, lean proteins",
                    "Include vitamins (C, B5, B6, D) and minerals (magnesium, zinc)",
                    "Minimize processed foods and excess sugar",
                ],
            }
        ],
        "activity": [
            {
                "action": "Exercise",
                "details": [
                    "Regular moderate exercise with resistance training",
                    "Avoid excessive exercise that elevates cortisol",
                ],
            }
        ],
        "lifestyle": [
            {
                "action": "Manage stress",
                "details": [
                    "Practice meditation, yoga, and deep breathing to will lower cortisol and support hormone balance"
                ],
            },
            {
                "action": "Prioritize sleep",
                "details": ["7-9 hours nightly for adrenal health", "Essential for optimal hormone production"],
            },
            {
                "action": "Reduce toxin exposure",
                "details": ["Limit endocrine-disrupting chemicals", "Choose natural personal care products"],
            },
            {"action": "Maintain work-life balance", "details": ["Limit screen time and schedule regular relaxation"]},
        ],
    },
}


async def seed_bloodwork_recommendations():
    """
    Seed bloodwork recommendations into the database.
    """
    print("Starting to seed bloodwork recommendations...")

    for biomarker_group, content in BLOODWORK_RECOMMENDATIONS.items():
        # Create action items for diet
        diet_actions = []
        for item in content.get("diet", []):
            diet_actions.append(ActionItem(action=item["action"], details=item["details"]))

        # Create action items for activity
        activity_actions = []
        for item in content.get("activity", []):
            activity_actions.append(ActionItem(action=item["action"], details=item["details"]))

        # Create action items for lifestyle
        lifestyle_actions = []
        for item in content.get("lifestyle", []):
            lifestyle_actions.append(ActionItem(action=item["action"], details=item["details"]))

        # Create recommendation
        recommendation = RecommendationCreate(
            recommendation_family="bloodwork",
            biomarker_group=biomarker_group,
            diet=diet_actions,
            activity=activity_actions,
            lifestyle=lifestyle_actions,
        )

        try:
            # Convert to dictionary for Firestore
            recommendation_dict = recommendation.model_dump(exclude={"id"})

            # Check if recommendation already exists to avoid duplicates
            query = recommendations_collection.where("recommendation_family", "==", "bloodwork").where(
                "biomarker_group", "==", biomarker_group
            )
            existing_docs = await query.get()

            if not existing_docs:
                # Add to collection
                doc_ref = recommendations_collection.document()
                await doc_ref.set(recommendation_dict)
                print(f"Added recommendation for bloodwork - {biomarker_group}")
            else:
                print(f"Recommendation for bloodwork - {biomarker_group} already exists.")

        except Exception as e:
            print(f"Error adding recommendation for {biomarker_group}: {str(e)}")

    print("Finished seeding bloodwork recommendations.")


async def main():
    try:
        await seed_bloodwork_recommendations()
        print("Successfully seeded all bloodwork recommendations!")
    except Exception as e:
        print(f"Error seeding bloodwork recommendations: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
