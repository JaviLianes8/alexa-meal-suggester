"""
DynamoDB implementation of MealRepository with partition key 'userId' and
sort key 'mealType'. Each item stores the list of dishes for that meal type.
"""

import logging
import os
from typing import Dict

import boto3
from boto3.dynamodb.conditions import Key

from ..domain.ports import MealRepository

logger = logging.getLogger(__name__)


class DynamoDBMealRepository(MealRepository):
    """Meal storage backed by DynamoDB."""

    def __init__(self, table_name: str = "MealSuggestions", dynamodb=None):
        region = os.environ.get("AWS_REGION", "us-east-1")
        self.dynamodb = dynamodb or boto3.resource("dynamodb", region_name=region)
        self.table = self.dynamodb.Table(table_name)

    def get_meals(self, user_id: str) -> Dict[str, list]:
        """Retrieve all meal lists for a user.

        Args:
            user_id: User identifier.

        Returns:
            Dictionary mapping meal types to list of dishes.
        """
        logger.info("Fetching meals for user %s", user_id)
        response = self.table.query(
            KeyConditionExpression=Key("userId").eq(user_id)
        )
        meals: Dict[str, list] = {}
        for item in response.get("Items", []):
            meals[item["mealType"]] = item.get("dishes", [])
        return meals

    def save_meals(self, user_id: str, meals: Dict[str, list]) -> None:
        """Persist meal lists for a user.

        Args:
            user_id: User identifier.
            meals: Mapping of meal types to dishes.
        """
        logger.info(
            "Saving meals for user %s: %s", user_id, list(meals.keys())
        )
        for meal_type, dishes in meals.items():
            self.table.put_item(
                Item={
                    "userId": user_id,
                    "mealType": meal_type,
                    "dishes": dishes,
                }
            )

