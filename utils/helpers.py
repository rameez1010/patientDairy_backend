
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds
from datetime import datetime
import re


def serialize_firestore_data(obj):
    """Convert Firestore objects to JSON-serializable format"""
    if isinstance(obj, DatetimeWithNanoseconds):
        return obj.isoformat()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: serialize_firestore_data(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_firestore_data(item) for item in obj]
    else:
        return obj

def normalize_name(name: str) -> str:
    """
    Normalize a name string by:
    - Lowercasing
    - Removing commas and extra spaces
    - Handling 'Last, First' and 'First Last' formats
    - Sorting name parts for robust matching
    """
    if not name:
        return ""
    # Remove punctuation (commas, periods, etc.)
    name = re.sub(r'[,.]', '', name)
    # Lowercase and strip spaces
    name = name.lower().strip()
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    # If name is in 'last, first' format, swap
    parts = name.split()
    if len(parts) == 2 and ',' in name:
        parts = [parts[1], parts[0]]
    # Sort for order-insensitive match
    return ' '.join(sorted(parts))

def is_name_match(name1: str, name2: str) -> bool:
    """
    Compare two names after normalization.
    """
    return normalize_name(name1) == normalize_name(name2)

# Example usage inside your blood work processing logic:
# extracted_name = ... # e.g., from blood report: 'NOWAK, ALEXANDRA'
# patient_full_name = f"{patient.firstName} {patient.lastName}"
# if is_name_match(extracted_name, patient_full_name):
#     # It's a match!
#     ...