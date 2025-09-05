import json
from pathlib import Path
from typing import Dict, List, Union


def load_biomarker_data(gender: str = "male") -> List[Dict]:
    """Load biomarker reference data from the appropriate JSON file."""
    file_path = (
        Path(__file__).parent.parent / f"cleanedBioMarkers_{gender.lower()}.json"
    )
    with open(file_path, "r") as f:
        return json.load(f)


def is_value_in_range(value: float, ranges: List[List[float]]) -> bool:
    """Check if a value falls within any of the given ranges."""
    return any(
        lower <= value <= upper
        for range_pair in ranges
        for lower, upper in [range_pair]
    )


def evaluate_biomarker(
    biomarker_name: str, value: float, gender: str = "male"
) -> Dict[str, Union[str, float]]:
    """
    Evaluate a biomarker value against reference ranges.

    Args:
        biomarker_name (str): The name of the biomarker to evaluate
        value (float): The value to evaluate
        gender (str): The gender to use for reference ranges ("male" or "female")

    Returns:
        Dict containing:
            - unit: The unit of measurement
            - range_status: Which range the value falls into (normal, abnormal, optimal)
            - title: The display title of the biomarker
    """
    # Load the appropriate reference data
    biomarkers = load_biomarker_data(gender)

    # Find the biomarker in the reference data
    biomarker_data = next((b for b in biomarkers if b["name"] == biomarker_name), None)

    if not biomarker_data:
        return {
            "unit": "unknown",
            "range_status": "unknown",
            "title": biomarker_name,
            "error": "Biomarker not found",
        }

    # Determine which range the value falls into
    range_status = "unknown"
    if is_value_in_range(value, biomarker_data["optimal_range"]):
        range_status = "optimal"
    elif is_value_in_range(value, biomarker_data["normal_range"]):
        range_status = "normal"
    elif is_value_in_range(value, biomarker_data["abnormal_range"]):
        range_status = "abnormal"

    return {
        "name": biomarker_name,
        "unit": biomarker_data["unit"],
        "range_status": range_status,
        "title": biomarker_data["title"],
        "value": value,
    }


def evaluate_biomarkers_batch(
    biomarkers_data: Dict[str, float], gender: str = "male"
) -> Dict[str, Dict[str, str]]:
    """
    Evaluate multiple biomarkers from an object and return their evaluations.

    Args:
        biomarkers_data (Dict[str, float]): Dictionary of biomarker names and their values
        gender (str): The gender to use for reference ranges ("male" or "female")

    Returns:
        Dict[str, Dict[str, str]]: Dictionary of biomarker names and their evaluation results
    """
    result = {}
    # Convert Pydantic model to dictionary
    if hasattr(biomarkers_data, "model_dump"):  # Pydantic v2
        data_dict = biomarkers_data.model_dump()
    elif hasattr(biomarkers_data, "dict"):  # Pydantic v1
        data_dict = biomarkers_data.dict()
    else:
        data_dict = dict(biomarkers_data)

    # Remove None values from the dictionary
    data_dict = {k: v for k, v in data_dict.items() if v is not None}

    # print("biomarkers_data is:", biomarkers_data)
    # print the type of biomarkers_data
    print("type of biomarkers_data is:", type(data_dict))
    # print length of biomarkers_data
    # print("length of biomarkers_data is:", len(biomarkers_data))
    for biomarker_name, value in data_dict.items():
        # Skip if value is None or not a number
        if value is None:
            continue

        try:
            value_float = float(value)
        except (ValueError, TypeError):
            continue

        # Evaluate the individual biomarker
        evaluation = evaluate_biomarker(biomarker_name, value_float, gender)

        # Only add to results if there's no error
        if "error" not in evaluation:
            result[biomarker_name] = evaluation

    return result


# create a new function to evaluate the biomakers and then group them by the biomarkers_groups.json file
def evaluate_biomarkers_and_group(
    biomarkers_data: Dict[str, float], gender: str = "male"
) -> Dict[str, Dict[str, str]]:
    """
    Evaluate multiple biomarkers from an object and group them by the biomarkers_groups.json file.
    """
    # Load the biomarkers_groups.json file
    with open("biomarkers_groups.json", "r") as f:
        biomarkers_groups = json.load(f)

    # Evaluate the biomarkers
    bioMarkersData = evaluate_biomarkers_batch(biomarkers_data, gender)

    # Group the biomarkers by the biomarkers_groups.json file
    grouped_evaluations = {}
    for group_name in biomarkers_groups:
        grouped_evaluations[group_name] = []
        for biomarker in biomarkers_groups[group_name]:
            if biomarker in bioMarkersData:
                grouped_evaluations[group_name].append(bioMarkersData[biomarker])

    return grouped_evaluations
