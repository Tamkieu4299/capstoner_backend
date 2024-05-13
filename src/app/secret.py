# coding: utf-8
from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    APIKeyHeader,
)
from fastapi.param_functions import Form
from jose import JWTError
from passlib.context import CryptContext
from .models.user_model import User
from sqlalchemy.orm import Session

from .crud.user_crud import CRUDUser
from .schemas.token import TokenData

from .log import logger
from .constants.config import Settings, get_settings
from .utils.jwt import encode_token, decode_token
from .db.database import get_db

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
TOKEN_TYPE = "Bearer"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

crud_user = CRUDUser(User)

if True:
    logger.info("start authticateion debug mode")
    oauth2_scheme = APIKeyHeader(name="Authorization")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = crud_user.search_user(username, db)
    if not user:
        return False
    if user.is_deleted:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = encode_token(to_encode)
    return encoded_jwt


def get_current_user(
    db=Depends(get_db),
    settings: Settings = Depends(get_settings),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        scheme = "Bearer "
        if True:
            logger.info(token)
            if token.startswith(scheme):
                token = token[len(scheme) :]
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated, set scheme Bearer",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = crud_user.read(id=token_data.user_id, db=db)
    if user is None:
        raise credentials_exception

    return {"user": user}


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user["user"].is_deleted:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class OAuth2CompanyPasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: str = Form(),
        password: str = Form(),
        scope: str = Form(default=""),
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
    ):
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )


# EOF
