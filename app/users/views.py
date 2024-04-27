from loguru import logger
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.users.models import User as UserModel
from app.auth.schema import SignUpSchema, LogInSchema, Token
from app.auth.jwt import create_access_token, get_current_user, get_token
from app.users.schema import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


auth_scheme = HTTPBearer()


router = APIRouter()





@router.get("/users/me", status_code=200)
async def get_me(db: Session = Depends(get_db), token: str = Depends(get_token)):

    current_user = await get_current_user(token, db)
    return current_user
