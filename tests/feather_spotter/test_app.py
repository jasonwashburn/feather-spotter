"""Implements tests for Feather Spotter FastAPI application."""
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from feather_spotter.app import app
from feather_spotter.detection import Detection

client = TestClient(app)


def test_read_main() -> None:
    """Tests root endpoint for Feather Spotter."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Feather Spotter!",
        "version": "0.0.1",
    }


def test_upload_file(mocker: MockerFixture) -> None:
    """Tests upload_file endpoint for Feather Spotter."""
    mocker.patch(
        "feather_spotter.app.detect",
        return_value=[
            Detection(
                index=0,
                name="mock",
                confidence=100.0,
                box=(0, 0, 0, 0),
            ),
        ],
    )
    response = client.post("/detect", files={"file": ("mock.jpg", b"mocked")})
    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {"index": 0, "name": "mock", "confidence": 100.0, "box": [0, 0, 0, 0]},
        ],
    }
