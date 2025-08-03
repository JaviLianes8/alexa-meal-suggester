"""
Utility function to load a meals dictionary from a JSON file.
"""

import json

def load_meals(filepath="meals.json") -> dict:
    """
    Loads meals from a JSON file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: Dictionary containing meals by type (e.g., lunch, dinner).
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)