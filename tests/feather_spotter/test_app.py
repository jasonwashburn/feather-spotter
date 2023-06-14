"""Implements tests for Feather Spotter FastAPI application."""
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from feather_spotter.app import app
from feather_spotter.models.bird_detection import BirdDetection

client = TestClient(app)


def test_read_main() -> None:
    """Tests root endpoint for Feather Spotter."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Feather Spotter!",
        "version": "0.0.1",
    }


@pytest.mark.asyncio()
async def test_upload_file(mocker: MockerFixture) -> None:
    """Tests upload_file endpoint for Feather Spotter."""
    mocker.patch(
        "feather_spotter.app.detect",
        return_value=[
            BirdDetection(
                timestamp=datetime(2021, 1, 1, tzinfo=UTC),
                species="mock-species",
                detection_confidence=100.0,
                species_confidence=100.0,
                box=(0, 0, 0, 0),
                trimmed_image_location="s3://mock/mock-trim-image.jpg",
                orig_image_location="s3://mock/mock.jpg",
                client_name="mock-client",
                geographical_location={
                    "lat": 41.8781,
                    "lon": 87.6298,
                },
            ),
        ],
    )
    sample_path = Path("tests/test-files/sample1.jpg")
    with Path.open(sample_path, "rb") as image:
        response = client.post("/detect", files={"file": ("sample1.jpg", image)})
    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "_id": None,
                "timestamp": "2021-01-01T00:00:00+00:00",
                "species": "mock-species",
                "detection_confidence": 100.0,
                "species_confidence": 100.0,
                "box": [0, 0, 0, 0],
                "trimmed_image_location": "s3://mock/mock-trim-image.jpg",
                "orig_image_location": "s3://mock/mock.jpg",
                "client_name": "mock-client",
                "geographical_location": {
                    "lat": 41.8781,
                    "lon": 87.6298,
                },
            },
        ],
    }
