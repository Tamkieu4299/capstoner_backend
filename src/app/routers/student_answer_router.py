from app.crud.student_answer_crud import CRUDStudenAnswer
from app.models.assignment_model import Assignment
from app.crud.assignment_crud import CRUDAssignment
from app.db.database import get_db
from app.models.student_answer_model import StudentAnswer
from app.models.question_model import Question
from app.models.removed_word_model import RemovedWords
from app.crud.removed_word_crud import CRUDRemovedWord
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status
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
rm_crud = CRUDRemovedWord(RemovedWords)

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

@router.post("/privacy-protection/{assignment_id}", status_code=status.HTTP_201_CREATED)
async def auto_grader(
    assignment_id: int,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_active_user),
):
    queue.enqueue(privacy_protection_processor, assignment_id)
    return "Successfully sent to queue"

@router.get("/result-summary/{assignment_id}")
async def get_assignment(
    assignment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    sas = sa_crud.read_by_assignment_id(assignment_id, db)
    return [sa.__dict__ for sa in sas]

@router.get("/privacy-protection/{assignment_id}")
async def get_sensi_info(
    assignment_id: int, db: Session = Depends(get_db)
):
    rsp = []
    sas = sa_crud.read_by_assignment_id(assignment_id, db)
    for sa in sas:
        rmws = await rm_crud.read_by_student_answer_id(sa.id, db)
        rmws_dict = [rmw.__dict__ for rmw in rmws]
        print(rmws_dict)
        rsp.append({
            "student_answer": sa.__dict__,
            "removed_words": [f"""{r.get("order")}.{r.get("original_value")}""" for r in rmws_dict]
        })
    return rsp


@router.get("/privacy-protection/format/{assignment_id}")
async def get_sensi_info_format(
    assignment_id: int, db: Session = Depends(get_db)
):
    rsp = {
        "File Name": [],
        "Student Work": [],
        "Sensitive Data Removed": []
    }
    sas = sa_crud.read_by_assignment_id(assignment_id, db)
    for sa in sas:
        rmws = await rm_crud.read_by_student_answer_id(sa.id, db)
        rmws_dict = [rmw.__dict__ for rmw in rmws]
        print(rmws_dict)
        rsp["File Name"].append(sa.student_name)
        rsp["Student Work"].append(sa.protected_answer)
        rsp["Sensitive Data Removed"].append([f"""{r.get("order")}.{r.get("original_value")}""" for r in rmws_dict])
    return rsp

@router.get("/privacy/{student_answer_id}")
async def get_detail_sensi_info(
    student_answer_id: int, db: Session = Depends(get_db)
):
    sa = sa_crud.read(student_answer_id, db)
    rmws = await rm_crud.read_by_student_answer_id(student_answer_id, db)
    rmws_dict = [rmw.__dict__ for rmw in rmws]
    print(rmws_dict)
    rsp = {
        "protected_answer": sa.protected_answer,
        "removed_words": [f"""{r.get("order")}.{r.get("original_value")}""" for r in rmws_dict]
    }
    return rsp