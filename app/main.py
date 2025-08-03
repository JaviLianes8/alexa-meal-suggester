"""
AWS Lambda handler to process Alexa Skill webhook events.

Routes incoming Alexa requests to the appropriate intent handlers defined in
`alexa_adapter`.
"""

from interface.alexa_adapter import (
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


def lambda_handler(event, context):
    """Entrypoint for AWS Lambda invoked by Alexa."""
    data = event
    intent = data["request"]["intent"]["name"]
    user_id = data["session"]["user"]["userId"]

    if intent == "SuggestDinnerIntent":
        return handle_meal_intent("dinner", user_id)

    elif intent == "AddLunchIntent":
        dish = data["request"]["intent"]["slots"]["dish"]["value"]
        return handle_add_meal_intent("lunch", dish, user_id)

    elif intent == "AddDinnerIntent":
        dish = data["request"]["intent"]["slots"]["dish"]["value"]
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
        meal_type = data["request"]["intent"]["slots"]["meal_type"]["value"]
        dish = data["request"]["intent"]["slots"]["dish"]["value"]
        return handle_add_to_meal_list_intent(meal_type, dish, user_id)

    elif intent == "RemoveFromMealListIntent":
        meal_type = data["request"]["intent"]["slots"]["meal_type"]["value"]
        dish = data["request"]["intent"]["slots"]["dish"]["value"]
        return handle_remove_from_meal_list_intent(meal_type, dish, user_id)

    elif intent == "SuggestAddFromRecipeIntent":
        dish = data["request"]["intent"]["slots"]["dish"]["value"]
        return handle_suggest_add_from_recipe_intent(dish)

    return {}

