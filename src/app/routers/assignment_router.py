from typing import List

from app.crud.assignment_crud import CRUDAssignment
from app.crud.assignment_question_crud import CRUDAssignmentQuestion
from app.db.database import get_db
from app.models.assignment_model import Assignment
from app.models.assignment_question_model import AssignmentQuestion
from app.utils.exception import CommonInvalid
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from app.schemas.assignment_schema import AssignmentRegisterSchema, AssignmentResponseSchema
from sqlalchemy.orm import Session
from ..utils import s3_driver
from rq import Queue
from redis import Redis
from ..processors.create_assignment_processor import create_assignment_processor
from ..secret import get_current_active_user
from io import BytesIO

logger = setup_logger(__name__)

router = APIRouter()

assignment_crud = CRUDAssignment(Assignment)
assignment_question_crud = CRUDAssignmentQuestion(AssignmentQuestion)

redis_conn = Redis(host='redis-internal', port=6379)
queue = Queue('default', connection=redis_conn)

@router.post(
"/add",
    status_code=status.HTTP_201_CREATED,
    # response_model=AssignmentRegisterSchema,
)
async def register_assignment(
    assignment_data: AssignmentRegisterSchema = Form(...),
    student_answers_file: UploadFile = File(...),
    questions_file: UploadFile = File(...),
    criteria_file: UploadFile = File(...),
    # current_user=Depends(get_current_active_user),
):  
    student_answers_file_bytes = await student_answers_file.read()
    student_answers_zip = BytesIO(student_answers_file_bytes)

    queue.enqueue(create_assignment_processor, assignment_data, student_answers_file, student_answers_zip, questions_file, criteria_file)
    return "Successfully sent to queue"


@router.get("/search", response_model=List[AssignmentResponseSchema])
async def get_assignments(
    db: Session = Depends(get_db)
):
    assignments = assignment_crud.get_all(db)
    assignments_dict_list = []
    for assignment in assignments:
        questions = assignment_question_crud.get_questions_by_assignment(assignment.id, db)
        assignment_dict = assignment.__dict__
        assignment_dict["questions"] = questions
        assignments_dict_list.append(assignment_dict)
    logger.info(f"Number of assignments: {len(assignments_dict_list)}")
    return assignments_dict_list

@router.get("/search/{id}", response_model=AssignmentResponseSchema)
async def get_assignment(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    assignment = assignment_crud.read(id, db)
    questions = assignment_question_crud.get_questions_by_assignment(assignment.id, db)
    assignment_dict = assignment.__dict__
    assignment_dict["questions"] = questions
    return assignment.__dict__

@router.get("/search_by_course/{course_id}", response_model=List[AssignmentResponseSchema])
async def get_assignment(
    course_id: int, db: Session = Depends(get_db)
):
    assignments = assignment_crud.read_by_course_id(course_id, db)
    logger.info(f"Number of assignments: {len(assignments)}")
    return assignments