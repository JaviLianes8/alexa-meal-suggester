# 🍽️ Alexa Meal Suggester

An Alexa Skill that suggests random meals (lunch or dinner), lets users manage their personal list of dishes, and optionally responds to recipe-related queries.

## ✅ Features

### 🎲 1. Random Meal Suggestion

- **User:** "Alexa, I want a random dinner"
- **Skill:** "How about tortilla de patatas? Do you like it or want another suggestion?"
- **User response:**
  - **Yes / silence (after 5 seconds):** "Perfect. Enjoy your meal. To get a recipe, say: Alexa, give me the recipe for tortilla de patatas"
  - **No:** Another suggestion is offered automatically

### 📚 2. Add Dishes After Recipes

- **User:** "Alexa, give me the recipe for tomato bread"
- **Skill:** (after the external recipe finishes)  
  "Do you want to add tomato bread to your random meals?"

### ➕ 3. Manual Add/Remove

- **Add:** "Alexa, add lasagna to my dinners"
- **Remove:** "Alexa, remove lentils from my lunches"

## 📁 Project Structure

```
alexa_meal_suggester/
├── lambda/
│   ├── __init__.py
│   ├── lambda_function.py           # AWS Lambda handler entrypoint
│   ├── domain/
│   │   ├── ports.py                 # Interfaces for repositories
│   │   └── use_cases.py             # Core logic
│   ├── infrastructure/
│   │   ├── json_meal_repository.py  # Meal storage per user (JSON)
│   │   ├── dynamodb_meal_repository.py
│   │   └── default_recipe_provider.py
│   └── interface/
│       └── alexa_adapter.py         # Alexa intent handlers
├── models/                          # Interaction models
├── README.md
└── LICENSE
```

## 🚀 Deploy

This project is intended to run as an AWS Lambda function. Zip the `lambda/`
directory so that it sits at the root of the archive and deploy the
`lambda.lambda_function.lambda_handler` entrypoint as the handler for your
Alexa skill.

## ⚙️ Intents Supported

- `SuggestDinnerIntent`
- `AddDinnerIntent`
- `AddLunchIntent`
- `RecommendDinnerIntent`
- `RandomDinnerIntent`
- `YesIntent`
- `NoIntent`
- `AddToMealListIntent`
- `RemoveFromMealListIntent`
- `SuggestAddFromRecipeIntent`

## 💾 Data Storage

User meal lists are stored in a DynamoDB table (`MealSuggestions`) using `userId` as
the partition key and `mealType` as the sort key.

## 📘 License

MIT — free for personal and commercial use.
