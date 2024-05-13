from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.user_model import User
from ..schemas.auth_schema import (
    LoginWebSchema,
    LoginResponse,
    RegisterBaseSchema,
    RegisterResponse,
)
from ..constants.config import Settings, get_settings
from ..schemas.response_schema import ResponseData
from ..utils.exception import InvalidDestination, NotFoundException
from ..utils.hash import hash_password, verify_password
from ..utils.logger import setup_logger
from ..utils.response import convert_response
from ..crud.user_crud import CRUDUser
from ..secret import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    TOKEN_TYPE,
    authenticate_user,
    create_access_token,
)

logger = setup_logger(__name__)

router = APIRouter()

user_crud = CRUDUser(User)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def register_user(
    user_data: RegisterBaseSchema,
    db: Session = Depends(get_db),
):

    phone = user_data.phone
    user = user_crud.search_user_by_phone_number(phone, db)
    if user:
        raise HTTPException(
            status_code=422, detail="This phone number is already register."
        )

    hash_user_data = user_data.dict()
    hash_user_data["password"] = hash_password(hash_user_data["password"])

    new_user = await user_crud.create(hash_user_data, db)

    if new_user is None:
        logger.info(f"Phone number {user_data.phone} has been registered")
        raise InvalidDestination(detail=f"Phone number has been registered")
    response_data = parse_obj_as(RegisterResponse, new_user.__dict__)
    return convert_response(True, "Register Successfully", response_data)


@router.post(
    "/login-web",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def login(
    login_data: LoginWebSchema,
    db: Session = Depends(get_db),
):
    user = user_crud.search_user(login_data.username, db)
    if user is None:
        raise NotFoundException(detail=f"Invalid user name")

    valid_password = verify_password(login_data.password, user.password)

    if not valid_password:
        logger.info(f"Invalid password")
        raise InvalidDestination(detail=f"Invalid password")
    response_data = parse_obj_as(LoginResponse, user.__dict__)
    return convert_response(True, "Login Successfully", response_data)


@router.post("/token", response_model=ResponseData)
def login_for_access_token(
    form_data: LoginWebSchema,
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
):

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not user:
        logger.error(
            f"user_name={form_data.username} User authentication failed because the user name or password is invalid."
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": TOKEN_TYPE},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": str(user.id),
        },
        expires_delta=access_token_expires,
    )

    logger.info(f"user_name={form_data.username} authentication succeeded")
    user.access_token = access_token
    user.token_type = TOKEN_TYPE
    response_data = parse_obj_as(LoginResponse, user.__dict__)
    return convert_response(True, "Login Successfully", response_data)
