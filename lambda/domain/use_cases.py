"""
Domain use cases for managing meals: random suggestion and addition.
"""

import random

def get_random_meal(meal_type: str, meals_dict: dict) -> str:
    """
    Returns a random dish from the user's meals for the given meal type.

    Args:
        meal_type (str): "lunch" or "dinner"
        meals_dict (dict): User's meal data

    Returns:
        str: Random meal or fallback message
    """
    options = meals_dict.get(meal_type, [])
    return random.choice(options) if options else f"No meals found for {meal_type}"

def add_meal(meal_type: str, dish: str, meals_dict: dict) -> dict:
    """
    Adds a dish to the given meal type if not already present.

    Args:
        meal_type (str): "lunch" or "dinner"
        dish (str): Meal name to add
        meals_dict (dict): User's meal data

    Returns:
        dict: Updated meal data
    """
    meals = meals_dict.get(meal_type, [])
    if dish not in meals:
        meals.append(dish)
    meals_dict[meal_type] = meals
    return meals_dict
