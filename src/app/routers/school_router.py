from typing import List

from ..secret import get_current_active_user
from ..models.school_model import School
from ..crud.school_crud import CRUDSchool
from ..utils.logger import setup_logger
from app.db.database import get_db
from app.utils.exception import CommonInvalid
from ..schemas.school_schema import SchoolRegisterSchema, SchoolResponseSchema
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

logger = setup_logger(__name__)

router = APIRouter()

school_crud = CRUDSchool(School)

@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=SchoolResponseSchema,
)
async def register(
    data: SchoolRegisterSchema,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_active_user),
):
    data_dict = data.dict()
    new = await school_crud.create(data_dict, db)
    if new is None:
        logger.info(
            f"Fail to create school"
        )
        raise CommonInvalid(detail=f"Fail to create school")
    return new.__dict__

@router.get(
    "/search",
    status_code=status.HTTP_201_CREATED,
    response_model=List[SchoolResponseSchema],
)
async def search(
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_active_user),
):
    schools = school_crud.get_all(db)
    dict_list = [i.__dict__ for i in schools]
    logger.info(f"Number of schools: {len(schools)}")
    return dict_list