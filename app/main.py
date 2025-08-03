"""
Main Flask application to handle Alexa Skill webhook.

Routes POST requests from Alexa to corresponding intent handlers defined in `alexa_adapter`.
"""

from flask import Flask, request, jsonify
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

app = Flask(__name__)

@app.route("/", methods=["POST"])
def alexa_webhook():
    """
    Main endpoint for Alexa requests.
    
    Parses the intent name and routes the request to the appropriate handler.
    """
    data = request.json
    intent = data['request']['intent']['name']
    user_id = data['session']['user']['userId']

    if intent == "SuggestDinnerIntent":
        return jsonify(handle_meal_intent("dinner", user_id))

    elif intent == "AddLunchIntent":
        dish = data['request']['intent']['slots']['dish']['value']
        return jsonify(handle_add_meal_intent("lunch", dish, user_id))

    elif intent == "AddDinnerIntent":
        dish = data['request']['intent']['slots']['dish']['value']
        return jsonify(handle_add_meal_intent("dinner", dish, user_id))

    elif intent == "RecommendDinnerIntent":
        return jsonify(handle_recommend_meal_intent("dinner", user_id))
    
    elif intent == "RandomDinnerIntent":
        return jsonify(handle_random_meal_intent("dinner", user_id))
    
    elif intent == "YesIntent":
        return jsonify(handle_yes_intent(user_id))
    
    elif intent == "NoIntent":
        return jsonify(handle_no_intent(user_id))
    
    elif intent == "AddToMealListIntent":
        meal_type = data["request"]["intent"]["slots"]["meal_type"]["value"]
        dish = data["request"]["intent"]["slots"]["dish"]["value"]
        return jsonify(handle_add_to_meal_list_intent(meal_type, dish, user_id))
    
    elif intent == "RemoveFromMealListIntent":
        meal_type = data["request"]["intent"]["slots"]["meal_type"]["value"]
        dish = data["request"]["intent"]["slots"]["dish"]["value"]
        return jsonify(handle_remove_from_meal_list_intent(meal_type, dish, user_id))
    
    elif intent == "SuggestAddFromRecipeIntent":
        dish = data["request"]["intent"]["slots"]["dish"]["value"]
        return jsonify(handle_suggest_add_from_recipe_intent(dish))

    return jsonify({})  # Default empty response if no intent matched

if __name__ == "__main__":
    app.run(debug=True)