from loguru import logger
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Header
from sqlalchemy.orm import Session, joinedload
from app.core.db.session import get_db
from app.auth.jwt import create_access_token, get_current_user, get_token
from app.pinpoints.models import Pinpoint as PinpointModel
from fastapi.security import HTTPBearer
from app.pinpoints.schema import CreatePinpointPayloadSchema


auth_scheme = HTTPBearer()


router = APIRouter()


@router.post("/pinpoints/", status_code=200)
async def create_pinpoint(
    payload: CreatePinpointPayloadSchema,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    current_user = await get_current_user(token, db)

    pinpoint_model = PinpointModel(
        latitude=payload.latitude,
        longitude=payload.longitude,
        comment=payload.comment,
        user_id=current_user.id,
    )

    db.add(pinpoint_model)
    db.commit()

    return {}


@router.get("/pinpoints/", status_code=200)
async def create_pinpoint(db: Session = Depends(get_db)):
    pinpoints = db.query(PinpointModel).options(joinedload(PinpointModel.user)).all()

    db.close()
    return {"pinpoints": pinpoints}
