"""Implements the BirdDetection model and UpdateBirdDetection model."""
import os
from datetime import UTC, datetime

import pymongo
from beanie import Document
from pydantic import BaseModel

host = os.environ.get("MONGODB_HOST", "localhost")
user = os.environ.get("MONGODB_USERNAME", "root")
password = os.environ.get("MONGODB_PASSWORD", "example")


class BirdDetection(Document):
    """Represents a bird detection."""

    timestamp: datetime
    species: str
    detection_confidence: float
    species_confidence: float
    box: tuple
    trimmed_image_location: str
    orig_image_location: str
    client_name: str
    geographical_location: dict

    class Settings:
        """Settings for the BirdDetection document."""

        name = "bird_detections"
        indexes = [
            [
                ("species", pymongo.TEXT),
                ("timestamp", pymongo.ASCENDING),
            ],
        ]

    class Config:
        """Pydantic configuration for the BirdDetection document."""

        schema_extra = {
            "example": {
                "timestamp": datetime.now(tz=UTC),
                "species": "American Goldfinch",
                "detection_confidence": 0.9,
                "species_confidence": 0.9,
                "box": (0, 0, 100, 100),
                "trimmed_image_location": "s3://feather-spotter/trimmed_images/2021-01-01/trimmed_image_1.jpg",
                "orig_image_location": "s3://feather-spotter/orig_images/2021-01-01/orig_image_1.jpg",
                "client_name": "camera_1",
                "geographical_location": {
                    "lat": 41.8781,
                    "lon": 87.6298,
                },
            },
        }


class UpdateBirdDetection(BaseModel):
    """Pydantic model which Represents a bird detection for use in updating MongoDB."""

    timestamp: datetime
    species: str | None
    detection_confidence: float
    species_confidence: float
    box: tuple
    trimmed_image_location: str
    orig_image_location: str
    client_name: str
    geographical_location: dict

    class Config:
        """Pydantic configuration for the UpdateBirdDetection model."""

        schema_extra = {
            "example": {
                "timestamp": datetime.now(tz=UTC),
                "species": "American Goldfinch",
                "detection_confidence": 0.9,
                "species_confidence": 0.9,
                "box": (0, 0, 100, 100),
                "trimmed_image_location": "s3://feather-spotter/trimmed_images/2021-01-01/trimmed_image_1.jpg",
                "orig_image_location": "s3://feather-spotter/orig_images/2021-01-01/orig_image_1.jpg",
                "client_name": "camera_1",
                "geographical_location": {
                    "lat": 41.8781,
                    "lon": 87.6298,
                },
            },
        }
