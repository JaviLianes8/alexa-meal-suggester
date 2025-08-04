"""AWS Lambda handler to process Alexa Skill webhook events."""

import logging

from .interface.alexa_adapter import (
    handle_meal_intent,
    handle_add_meal_intent,
    handle_recommend_meal_intent,
    handle_random_meal_intent,
    handle_yes_intent,
    handle_no_intent,
    handle_add_to_meal_list_intent,
    handle_remove_from_meal_list_intent,
    handle_suggest_add_from_recipe_intent,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Entrypoint for AWS Lambda invoked by Alexa."""
    intent = event["request"]["intent"]["name"]
    user_id = event["session"]["user"]["userId"]
    logger.info("Received intent %s from user %s", intent, user_id)

    if intent == "SuggestDinnerIntent":
        return handle_meal_intent("dinner", user_id)

    elif intent == "AddLunchIntent":
        dish = event["request"]["intent"]["slots"]["dish"]["value"]
        return handle_add_meal_intent("lunch", dish, user_id)

    elif intent == "AddDinnerIntent":
        dish = event["request"]["intent"]["slots"]["dish"]["value"]
        return handle_add_meal_intent("dinner", dish, user_id)

    elif intent == "RecommendDinnerIntent":
        return handle_recommend_meal_intent("dinner", user_id)

    elif intent == "RandomDinnerIntent":
        return handle_random_meal_intent("dinner", user_id)

    elif intent == "YesIntent":
        return handle_yes_intent(user_id)

    elif intent == "NoIntent":
        return handle_no_intent(user_id)

    elif intent == "AddToMealListIntent":
        meal_type = event["request"]["intent"]["slots"]["meal_type"]["value"]
        dish = event["request"]["intent"]["slots"]["dish"]["value"]
        return handle_add_to_meal_list_intent(meal_type, dish, user_id)

    elif intent == "RemoveFromMealListIntent":
        meal_type = event["request"]["intent"]["slots"]["meal_type"]["value"]
        dish = event["request"]["intent"]["slots"]["dish"]["value"]
        return handle_remove_from_meal_list_intent(meal_type, dish, user_id)

    elif intent == "SuggestAddFromRecipeIntent":
        dish = event["request"]["intent"]["slots"]["dish"]["value"]
        return handle_suggest_add_from_recipe_intent(dish)

    logger.warning("Unknown intent %s", intent)
    return {}


