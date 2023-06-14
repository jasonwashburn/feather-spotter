"""Implements database functionality for Feather Spotter."""
import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from feather_spotter.models.bird_detection import BirdDetection

host = os.environ.get("MONGODB_HOST", "localhost")
user = os.environ.get("MONGODB_USERNAME", "root")
password = os.environ.get("MONGODB_PASSWORD", "example")


async def init_db() -> None:
    """Initializes the database connection.

    Returns:
        None
    """
    # Create Motor client
    client = AsyncIOMotorClient(
        f"mongodb://{user}:{password}@{host}:27017",
    )

    # Initialize beanie with the Product document class and a database
    await init_beanie(database=client.db_name, document_models=(BirdDetection))
