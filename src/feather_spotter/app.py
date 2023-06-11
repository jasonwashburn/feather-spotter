"""Implements FastAPI application for Feather Spotter."""
import logging

from fastapi import FastAPI, HTTPException, UploadFile

from feather_spotter.__about__ import __version__ as version
from feather_spotter.detection import Detection, detect

logger = logging.getLogger("app")

app = FastAPI()


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
) -> dict[str, list[Detection]]:
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
    detections = detect(file.filename)
    return {"results": detections}
