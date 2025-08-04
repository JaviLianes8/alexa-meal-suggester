"""Alexa adapter functions to handle meal-related intents."""

import logging

from ..domain.use_cases import get_random_meal, add_meal
from ..infrastructure.dynamodb_meal_repository import DynamoDBMealRepository
from ..infrastructure.default_recipe_provider import get_random_response

logger = logging.getLogger(__name__)

repo = DynamoDBMealRepository()
current_suggestions = {}

def alexa_response(text: str, end_session: bool = False):
    """
    Generates a standard Alexa response.

    Args:
        text (str): The text Alexa will say.
        end_session (bool): Whether the session should end.

    Returns:
        dict: Alexa-compatible response structure.
    """
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text
            },
            "shouldEndSession": end_session
        }
    }

def handle_meal_intent(meal_type: str, user_id: str):
    """
    Handles intent to suggest a meal.

    Args:
        meal_type (str): Type of meal ('lunch', 'dinner').
        user_id (str): Unique user ID.

    Returns:
        dict: Alexa response with meal suggestion.
    """
    logger.info("Suggesting %s for user %s", meal_type, user_id)
    meals = repo.get_meals(user_id)
    suggestion = get_random_meal(meal_type, meals)
    return alexa_response(suggestion, end_session=False)

def handle_add_meal_intent(meal_type: str, dish: str, user_id: str):
    """
    Adds a dish to the user's meal list.

    Args:
        meal_type (str): 'lunch' or 'dinner'.
        dish (str): Name of the dish to add.
        user_id (str): Unique user ID.

    Returns:
        dict: Confirmation message.
    """
    logger.info("Adding %s to %s for user %s", dish, meal_type, user_id)
    meals = repo.get_meals(user_id)
    updated = add_meal(meal_type, dish, meals)
    repo.save_meals(user_id, updated)
    return alexa_response(f"{dish} añadido a {meal_type}", end_session=False)

def handle_recommend_meal_intent(meal_type: str, user_id: str):
    """
    Suggests a random meal with a default description.

    Args:
        meal_type (str): Type of meal.
        user_id (str): User ID.

    Returns:
        dict: Alexa response with predefined suggestion.
    """
    logger.info("Recommending %s for user %s", meal_type, user_id)
    meals = repo.get_meals(user_id)
    dish = get_random_meal(meal_type, meals)
    response_text = get_random_response(dish, meals)
    return alexa_response(response_text, end_session=True)

def handle_random_meal_intent(meal_type: str, user_id: str):
    """
    Suggests a random dish and stores it for follow-up Yes/No intents.

    Args:
        meal_type (str): Meal type.
        user_id (str): User ID.

    Returns:
        dict: Suggestion with follow-up question.
    """
    logger.info("Random suggestion for %s to user %s", meal_type, user_id)
    suggestion = get_random_meal(meal_type, repo.get_meals(user_id))
    current_suggestions[user_id] = (meal_type, suggestion)
    return alexa_response(f"¿Qué te parece {suggestion}? ¿Te gusta o te sugiero otra?", end_session=False)

def handle_yes_intent(user_id: str):
    """
    Confirms the suggested meal.

    Args:
        user_id (str): User ID.

    Returns:
        dict: Confirmation message and optional recipe hint.
    """
    logger.info("User %s accepted suggestion", user_id)
    if user_id in current_suggestions:
        meal_type, dish = current_suggestions[user_id]
        return alexa_response(f"Perfecto. Buen provecho. Para obtener una receta, di: Alexa, dame una receta de {dish}")
    return alexa_response("Perfecto.")

def handle_no_intent(user_id: str):
    """
    Re-suggests a different meal if the user rejects the previous one.

    Args:
        user_id (str): User ID.

    Returns:
        dict: New suggestion or fallback response.
    """
    logger.info("User %s rejected suggestion", user_id)
    if user_id in current_suggestions:
        meal_type, _ = current_suggestions[user_id]
        return handle_random_meal_intent(meal_type, user_id)
    return alexa_response("Vale, dime qué prefieres entonces.")

def handle_add_to_meal_list_intent(meal_type: str, dish: str, user_id: str):
    """
    Adds a dish to a specific meal type.

    Args:
        meal_type (str): 'lunch' or 'dinner'.
        dish (str): Dish name.
        user_id (str): User ID.

    Returns:
        dict: Confirmation.
    """
    logger.info("Adding %s to %s list for user %s", dish, meal_type, user_id)
    meals = repo.get_meals(user_id)
    updated = add_meal(meal_type, dish, meals)
    repo.save_meals(user_id, updated)
    return alexa_response(f"{dish} añadido a {meal_type}s.")

def handle_remove_from_meal_list_intent(meal_type: str, dish: str, user_id: str):
    """
    Removes a dish from a meal type list.

    Args:
        meal_type (str): 'lunch' or 'dinner'.
        dish (str): Dish name.
        user_id (str): User ID.

    Returns:
        dict: Success or not-found message.
    """
    logger.info("Removing %s from %s list for user %s", dish, meal_type, user_id)
    meals = repo.get_meals(user_id)
    if dish in meals.get(meal_type, []):
        meals[meal_type].remove(dish)
        repo.save_meals(user_id, meals)
        return alexa_response(f"{dish} eliminado de {meal_type}s.")
    return alexa_response(f"{dish} no está en tu lista de {meal_type}s.")

def handle_suggest_add_from_recipe_intent(dish: str):
    """
    Suggests adding a dish mentioned in a recipe to the user's meal list.

    Args:
        dish (str): Dish name.

    Returns:
        dict: Prompt asking if the user wants to add the dish.
    """
    logger.info("Suggesting to add %s from recipe", dish)
    return alexa_response(f"¿Quieres añadir {dish} a tus comidas o cenas aleatorias?")

