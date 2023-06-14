"""Implements test fixtures for Feather Spotter."""
import pytest_asyncio
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from feather_spotter.models.bird_detection import BirdDetection


@pytest_asyncio.fixture(autouse=True)
async def setup_db() -> None:
    """Sets up the database for testing."""
    client = AsyncMongoMockClient()
    await init_beanie(
        document_models=[BirdDetection],
        database=client.get_database(name="db"),
    )
