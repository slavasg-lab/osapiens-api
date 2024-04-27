from loguru import logger
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.users.models import User as UserModel
from app.auth.schema import SignUpSchema, LogInSchema, Token
from app.auth.jwt import create_access_token


router = APIRouter()


@router.post("/auth/sign-up", status_code=200)
async def sign_up(payload: SignUpSchema, db: Session = Depends(get_db)):
    """
    signs up a user.

    Returns:
        { accessToken }
    """

    user = db.query(UserModel).filter(UserModel.email == payload.email).first()


    if user:
        desc = "User with this email already exists"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)
    
    user_model = UserModel(email = payload.email, password=payload.password, full_name = payload.full_name)

    db.add(user_model)
    db.commit()
    
    access_token = create_access_token(user_model.email)

    return Token(access_token=access_token, token_type="bearer")


@router.post("/auth/log-in", status_code=200)
async def sign_up(payload: LogInSchema, db: Session = Depends(get_db)):
    """
    signs up a user.

    Returns:
        { accessToken }
    """

    user = db.query(UserModel).filter(UserModel.email == payload.email).first()


    if not user:
        desc = "User with this email doesn't exist"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)
    
    is_password_match = user.password == payload.password

    if not is_password_match:
        desc = "Wrong password"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)
    
    access_token = create_access_token(payload.email)

    return Token(access_token=access_token, token_type="bearer")