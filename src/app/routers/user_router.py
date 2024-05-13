from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.user_model import User
from ..schemas.response_schema import ResponseData
from ..schemas.user_schema import UserResponseSchema, UserUpdateInfoSchema
from ..utils.exception import (
    NotFoundException,
)
from ..utils.logger import setup_logger
from ..utils.response import convert_response
from ..crud.user_crud import CRUDUser
from ..secret import get_current_active_user

logger = setup_logger(__name__)

router = APIRouter()

user_crud = CRUDUser(User)


@router.get(
    "/get-user/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    user = user_crud.read(user_id, db)

    if user is None:
        logger.info(f"Invalid user id {user_id}")
        raise NotFoundException(detail=f"Invalid user id")

    response_data = parse_obj_as(UserResponseSchema, user.__dict__)
    return convert_response(True, "", response_data)


@router.get("/search/", response_model=List[UserResponseSchema])
async def get_users(
    db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    users = user_crud.get_all(db)
    users_dict_list = [i.__dict__ for i in users]
    logger.info(f"Number of users: {len(users)}")
    return users_dict_list 


@router.post("/soft-delete/{user_id}", response_model=UserResponseSchema)
async def soft_delete_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    user = user_crud.soft_delete(user_id, db)

    if user is None:
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")
    logger.info(f"Soft delete user with ID: {user_id}")
    return user.__dict__


@router.get("/search/{name}", response_model=List[UserResponseSchema])
async def search_users(
    name: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    users = user_crud.search_user(name, db)
    users_dict_list = [i.__dict__ for i in users]
    logger.info(f"Number of users: {len(users)}")
    return users_dict_list


@router.post("/update-user-info/{user_id}", response_model=UserResponseSchema)
def api_update_user_info(
    user_id: str,
    user_info: UserUpdateInfoSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    user = user_crud.update(
        user_id,
        user_info.dict(),
        db,
    )

    if user is None:
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")

    return user.__dict__
