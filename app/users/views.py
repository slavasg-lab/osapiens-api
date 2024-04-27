from loguru import logger
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.users.models import User as UserModel
from app.auth.schema import SignUpSchema, LogInSchema, Token
from app.auth.jwt import create_access_token, get_current_user
from app.users.schema import User


router = APIRouter()


@router.get("/me", response_model=User)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
