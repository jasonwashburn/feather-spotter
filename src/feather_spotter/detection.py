"""Iplelements detection functionality of the Feather Spotter application."""
import datetime

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel
from ultralytics import YOLO
from ultralytics.yolo.engine.results import Boxes

from feather_spotter.models.bird_detection import UpdateBirdDetection


class Detection(BaseModel):
    """Represents a parsed record of a detected object."""

    index: int
    name: str | None
    confidence: float
    box: tuple[int, int, int, int]

    def to_dict(self) -> dict[str, int | str | float | tuple[int, int, int, int]]:
        """Converts the detection to a dictionary.

        Returns:
            dict[str, int | str | float | tuple[int, int, int, int]]: Dictionary
                representation of the detection.
        """
        return self.dict()


def parse_detections(
    boxes: Boxes,
    names: dict[int, str],
) -> list[UpdateBirdDetection]:
    """Parses detection results into a list of dictionaries."""
    detections = []
    for _index, box in enumerate(boxes):
        flat_box = box.data.flatten()
        top, left, bottom, right = (
            int(np.floor(flat_box[coord_idx])) for coord_idx in range(4)
        )
        name_index = int(flat_box[5])
        confidence = round(float(flat_box[4]), 4) * 100
        name = names.get(name_index)
        detections.append(
            UpdateBirdDetection(
                timestamp=datetime.datetime.now(tz=datetime.UTC),
                species=name,
                detection_confidence=confidence,
                species_confidence=0.0,
                box=(top, left, bottom, right),
                trimmed_image_location="s3://example/example.jpg",
                orig_image_location="s3://example/example.jpg",
                client_name="camera_1",
                geographical_location={
                    "lat": 41.8781,
                    "lon": 87.6298,
                },
            ),
        )
    return detections


def detect(image: NDArray) -> list[UpdateBirdDetection]:
    """Detects objects in an image.

    Args:
        image (str): Path to the image to detect objects in.

    """
    model = YOLO("yolov8n.pt")
    results = model.predict(source=image, save=True)
    return parse_detections(results[0].boxes, results[0].names)
