"""
Implements a MealRepository using local JSON files for persistence.
Each user has a separate JSON file identified by their user_id.
"""

import json
import os
from ..domain.ports import MealRepository

class JsonMealRepository(MealRepository):
    """
    JSON-based implementation of MealRepository.
    Stores meals per user in a local directory.
    """

    def __init__(self, base_dir="/tmp/meals"):
        """
        Initializes the repository and ensures the storage directory exists.

        Args:
            base_dir (str): Directory where user meal files are stored.
        """
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def get_meals(self, user_id: str) -> dict:
        """
        Loads the meal list for a given user from a JSON file.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            dict: Dictionary with keys like "lunch", "dinner", etc.
        """
        path = os.path.join(self.base_dir, f"{user_id}.json")
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_meals(self, user_id: str, meals: dict) -> None:
        """
        Saves the given meals dictionary for a user into their JSON file.

        Args:
            user_id (str): User identifier.
            meals (dict): Dictionary of meals to save.
        """
        path = os.path.join(self.base_dir, f"{user_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meals, f, ensure_ascii=False, indent=2)
