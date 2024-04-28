from loguru import logger
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Header
from sqlalchemy.orm import Session, joinedload
from app.core.db.session import get_db
from app.auth.jwt import create_access_token, get_current_user, get_token
from app.pinpoints.models import Pinpoint as PinpointModel
from fastapi.security import HTTPBearer
from app.pinpoints.schema import CreatePinpointPayloadSchema
import random


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
async def create_pinpoint(
    max_latitude: float,
    min_latitude: float,
    max_longitude: float,
    min_longitude: float,
    db: Session = Depends(get_db),
):
    pinpoints = (
        db.query(PinpointModel)
        .filter(PinpointModel.latitude <= max_latitude)
        .filter(PinpointModel.latitude >= min_latitude)
        .filter(PinpointModel.longitude <= max_longitude)
        .filter(PinpointModel.longitude >= min_longitude)
        .options(joinedload(PinpointModel.user))
        .all()
    )

    db.close()
    return {"pinpoints": pinpoints}


@router.post("/pinpoints/create_random", status_code=200)
async def create_pinpoint(
    db: Session = Depends(get_db),
):
    def create_random_locations(num_locations):
        locations = []
        for _ in range(num_locations):
            # Generate random latitude and longitude
            lat = random.uniform(-90, 90)
            lon = random.uniform(-180, 180)
            locations.append(
                PinpointModel(
                    latitude=lat,
                    longitude=lon,
                    user_id=1,
                    comment=str(random.randint(237, 1000)),
                )
            )

        return locations

    locations = create_random_locations(10000)

    batch_size = 10000  # Insert 10,000 entries at a time
    for i in range(0, len(locations), batch_size):
        db.bulk_save_objects(locations[i : i + batch_size])
        db.commit()
    db.close()

    return {}
