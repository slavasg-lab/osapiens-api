from loguru import logger
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from PIL import Image
import numpy as np
import io




router = APIRouter()


# @router.post("/images/mask", status_code=200)
# async def get_mask(file: UploadFile):
#     """
#     gets an image.

#     Returns:
#         mask: of the same size of as the image.
#     """

#     image_data = await file.read()
#     image = Image.open(io.BytesIO(image_data))

#     mask = process_image(image)
    
#     return StreamingResponse(mask, media_type='image/png', headers={"Content-Disposition": "attachment; filename=mask.png"})
