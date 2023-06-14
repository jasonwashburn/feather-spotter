"""Implements FastAPI application for Feather Spotter."""
import io
import logging

import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile
from PIL import Image

from feather_spotter.__about__ import __version__ as version
from feather_spotter.database import init_db
from feather_spotter.detection import detect
from feather_spotter.models.bird_detection import BirdDetection

logger = logging.getLogger("app")

app = FastAPI()


@app.on_event("startup")
async def start_db() -> None:
    """Starts the database connection."""
    await init_db()


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint for Feather Spotter.

    Returns:
        dict[str, str]: Welcome message and version number.
    """
    return {"message": "Welcome to Feather Spotter!", "version": version}


@app.post("/detect")
async def upload_file(
    file: UploadFile,
) -> dict[str, list[BirdDetection]]:
    """Implements upload_file endpoint for Feather Spotter.

    Args:
        file (UploadFile): File to be processed.

    Returns:
        dict[str, list[dict[str, float]]]: Dictionary of detection results.
    """
    logger.info("Received file: {file_name}", extra={"file_name": file.filename})
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=404,
            detail="Only JPEG and PNG files are supported.",
        )
    if file.filename is None:
        raise HTTPException(
            status_code=404,
            detail="File name is missing.",
        )
    # load jpeg or png file from file.file as numpy ndarray
    image = file.file.read()
    image_array = np.array(Image.open(io.BytesIO(image)))
    detections = detect(image_array)
    result = await BirdDetection.insert_many(detections)
    logger.info("Inserted {count} records", extra={"count": len(result.inserted_ids)})

    return {"results": detections}
