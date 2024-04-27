from loguru import logger
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.users.models import User as UserModel
from app.auth.schema import SignUpSchema, LogInSchema, Token
from app.auth.jwt import create_access_token, get_current_user, get_token_from_header
from app.users.schema import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


auth_scheme = HTTPBearer()


router = APIRouter()


def get_token(authorization22: str = Header(None)):
    if authorization22 is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        return authorization22.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Authorization header invalid")


@router.get("/me", status_code=200)
async def get_me(db: Session = Depends(get_db), token: str = Depends(get_token)):

    current_user = await get_current_user(token, db)
    return current_user
