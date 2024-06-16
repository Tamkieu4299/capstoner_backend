from typing import List

from ..secret import get_current_active_user
from ..models.course_model import Course
from ..models.assignment_model import Assignment
from ..models.school_model import School
from ..crud.course_crud import CRUDCourse
from ..crud.assignment_crud import CRUDAssignment
from ..crud.school_crud import CRUDSchool
from ..utils.logger import setup_logger
from app.db.database import get_db
from ..schemas.course_schema import CourseRegisterSchema, CourseResponseSchema
from app.utils.exception import CommonInvalid
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

logger = setup_logger(__name__)

router = APIRouter()

course_crud = CRUDCourse(Course)
assignment_crud = CRUDAssignment(Assignment)
school_crud = CRUDSchool(School)

@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED
)
async def register(
    data: CourseRegisterSchema,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_active_user),
):
    data_dict = data.dict()
    new = await course_crud.create(data_dict, db)
    if new is None:
        logger.info(
            f"Fail to create course"
        )
        raise CommonInvalid(detail=f"Fail to create course")
    return new.__dict__

@router.get("/search", response_model=List[CourseResponseSchema])
async def get(
    db: Session = Depends(get_db), 
    # current_user=Depends(get_current_active_user)
):
    courses = course_crud.get_all(db)
    courses_dict_list = []
    for course in courses:
        assignments = assignment_crud.read_by_course_id(course.id, db)
        school = school_crud.read(course.school_id, db)
        course_dict = course.__dict__
        course_dict["assignments"] = assignments
        course_dict["school"] = school.__dict__
        courses_dict_list.append(course_dict)
    logger.info(f"Number of course: {len(courses_dict_list)}")
    return courses_dict_list