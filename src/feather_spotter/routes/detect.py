"""Implements detect endpoint for Feather Spotter."""
import io
import logging

import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile
from PIL import Image

from feather_spotter.detection import detect
from feather_spotter.models.bird_detection import UpdateBirdDetection

router = APIRouter()
logger = logging.getLogger("app")


@router.post("/")
async def upload_file(
    file: UploadFile,
) -> dict[str, list[UpdateBirdDetection]]:
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
    return {"results": detections}
