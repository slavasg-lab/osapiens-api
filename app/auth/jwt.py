import os
from dotenv import load_dotenv
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.auth.schema import TokenData
from sqlalchemy.orm import Session
from app.users.models import User as UserModel
from fastapi.security import OAuth2PasswordBearer


load_dotenv(".env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(email: str, expires_delta: timedelta | None = None):
    to_encode = {"email": email}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=3600)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"])
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.email == token_data.username).first()

    if user is None:
        raise credentials_exception
    return user
