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
├── app/
│   ├── main.py                      # Flask app entrypoint
│   ├── interface/
│   │   └── alexa_adapter.py         # Alexa intent handlers
│   ├── infrastructure/
│   │   ├── json_meal_repository.py  # Meal storage per user (JSON)
│   │   └── default_recipe_provider.py
│   ├── domain/
│   │   ├── ports.py                 # Interfaces for repositories
│   │   └── use_cases.py             # Core logic
│   └── __main__.py                  # Main entry point
├── meals/                           # Folder for user JSON files
├── requirements.txt
├── README.md
```

## 🚀 Run Locally

```bash
# Install dependencies
pip install flask

# Start the app
python -m app
```

## 📤 Example CURL Tests

```bash
# Suggest a random dinner
curl -X POST http://127.0.0.1:5000/ \
  -H "Content-Type: application/json" \
  -d "{\"session\":{\"user\":{\"userId\":\"test-user-123\"}},\"request\":{\"type\":\"IntentRequest\",\"intent\":{\"name\":\"RandomDinnerIntent\"}}}"

# Confirm the suggestion
curl -X POST http://127.0.0.1:5000/ \
  -H "Content-Type: application/json" \
  -d "{\"session\":{\"user\":{\"userId\":\"test-user-123\"}},\"request\":{\"type\":\"IntentRequest\",\"intent\":{\"name\":\"YesIntent\"}}}"
```

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

User meal lists are stored as JSON files in the `meals/` directory, one file per user ID.

## 📘 License

MIT — free for personal and commercial use.