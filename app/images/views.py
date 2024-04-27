from loguru import logger
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from PIL import Image
import numpy as np
import io



router = APIRouter()


@router.post("/images/mask", status_code=200)
async def get_mask(file: UploadFile):
    """
    gets an image.

    Returns:
        mask: of the same size of as the image.
    """

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    # Process your image and generate a mask as a numpy array
    mask = np.where(np.array(image) > 128, 1, 0)  # Example threshold operation
    mask_image = Image.fromarray((mask * 255).astype(np.uint8))  # Convert to uint8 image

    # Save to a BytesIO object
    buf = io.BytesIO()
    mask_image.save(buf, format='PNG')
    buf.seek(0)
    
    return StreamingResponse(buf, media_type='image/png', headers={"Content-Disposition": "attachment; filename=mask.png"})
