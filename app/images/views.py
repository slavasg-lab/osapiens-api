from loguru import logger
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.sneakers.models import Sneaker as SneakerModel
from app.sneakers.schema import SneakerSchema



router = APIRouter()


@router.post("/mask", status_code=200)
async def get_mask(file: UploadFile):
    """
    gets an image.

    Returns:
        mask: of the same size of as the image.
    """

    return {"filename": file.filename}
