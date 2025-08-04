"""
Domain contract for a repository that manages user meal data.
"""

from typing import Protocol

class MealRepository(Protocol):
    """
    Protocol (interface) for meal repositories.

    Methods:
        get_meals(user_id): Retrieves the user's meal dictionary.
        save_meals(user_id, meals): Persists the updated meal dictionary.
    """
    def get_meals(self, user_id: str) -> dict:
        ...

    def save_meals(self, user_id: str, meals: dict) -> None:
        ...
