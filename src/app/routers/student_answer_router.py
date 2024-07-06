from app.crud.student_answer_crud import CRUDStudenAnswer
from app.models.assignment_model import Assignment
from app.crud.assignment_crud import CRUDAssignment
from app.db.database import get_db
from app.models.student_answer_model import StudentAnswer
from app.models.question_model import Question
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from app.schemas.student_answer_schema import (
    StudentAnswerRegisterSchema,
    PrivacyInputSchema
)
from sqlalchemy.orm import Session
from ..secret import get_current_active_user
from app.crud.question_crud import CRUDQuestion
from io import BytesIO
import zipfile
from rq import Queue
from redis import Redis
from app.processors.auto_evaluation_processor import auto_evaluation_processor
from app.processors.privacy_protection_processor import privacy_protection_processor

logger = setup_logger(__name__)

router = APIRouter()

sa_crud = CRUDStudenAnswer(StudentAnswer)
question_crud = CRUDQuestion(Question)
asm_crud = CRUDAssignment(Assignment)

redis_conn = Redis(host='redis-internal', port=6379)
queue = Queue('default', connection=redis_conn)

@router.post("/auto-grader", status_code=status.HTTP_201_CREATED)
async def auto_grader(
    student_answer_data: StudentAnswerRegisterSchema,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_active_user),
):
    
    queue.enqueue(auto_evaluation_processor, student_answer_data.assignment_id)
    return "Successfully sent to queue"

@router.post("/privacy-protection", status_code=status.HTTP_201_CREATED)
async def auto_grader(
    privacy_input: PrivacyInputSchema,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_active_user),
):
    queue.enqueue(privacy_protection_processor, privacy_input.assignment_id)
    return "Successfully sent to queue"

@router.get("/result-summary/{assignment_id}")
async def get_assignment(
    assignment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    sas = sa_crud.read_by_assignment_id(assignment_id, db)
    return [sa.__dict__ for sa in sas]

@router.put("/privacy-protection")
async def get_assignment(
    assignment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    sas = sa_crud.read_by_assignment_id(assignment_id, db)
    return [sa.__dict__ for sa in sas]