"""
Provides fallback random responses for meal suggestions when no user data is available.
"""

import random

# Default responses per meal type
default_responses = {
    "dinner": {
        "responses": [
            "Te sugiero espaguetis con tomate y atún.",
            "¿Qué tal una tortilla de patatas?",
            "Prueba una ensalada de pollo con aguacate.",
            "Cena ligera: crema de calabacín y pan.",
        ]
    },
    "lunch": {
        "responses": [
            "Hoy podrías hacer lentejas con chorizo.",
            "Arroz con pollo suena bien.",
            "Una ensalada de garbanzos con atún está genial.",
            "Macarrones con queso siempre funcionan.",
        ]
    }
}

def get_random_response(meal: str, meals: dict = default_responses) -> str:
    """
    Returns a random hardcoded meal suggestion for the given meal type.

    Args:
        meal (str): "lunch" or "dinner"
        meals (dict, optional): Custom responses. Defaults to `default_responses`.

    Returns:
        str: Suggested meal or fallback text
    """
    meal_info = meals.get(meal, {})
    responses = meal_info.get("responses", [])
    return random.choice(responses) if responses else f"Apuntado: {meal}"
