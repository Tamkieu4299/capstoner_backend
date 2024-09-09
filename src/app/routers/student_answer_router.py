from app.crud.student_answer_crud import CRUDStudenAnswer
from app.models.assignment_model import Assignment
from app.crud.assignment_crud import CRUDAssignment
from app.db.database import get_db
from app.models.student_answer_model import StudentAnswer
from app.models.question_model import Question
from app.models.removed_word_model import RemovedWords
from app.crud.removed_word_crud import CRUDRemovedWord
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status, Response
from app.schemas.student_answer_schema import (
    StudentAnswerRegisterSchema,
    PrivacyInputSchema,
    UpdatePrivacyInfoSchema
)
from sqlalchemy.orm import Session
from ..secret import get_current_active_user
from app.crud.question_crud import CRUDQuestion
from io import BytesIO
import zipfile
from rq import Queue
from redis import Redis
from app.processors.new_auto_evaluation_processor import auto_evaluation_processor
from app.processors.privacy_protection_processor import privacy_protection_processor
import re
logger = setup_logger(__name__)

router = APIRouter()

sa_crud = CRUDStudenAnswer(StudentAnswer)
question_crud = CRUDQuestion(Question)
asm_crud = CRUDAssignment(Assignment)
rm_crud = CRUDRemovedWord(RemovedWords)

redis_conn = Redis(host='redis-internal', port=6379)
queue = Queue('default', connection=redis_conn)

@router.post("/auto-grader/{assignment_id}", status_code=status.HTTP_201_CREATED)
async def auto_grader(
    assignment_id: int,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_active_user),
):
    
    queue.enqueue(auto_evaluation_processor, assignment_id)
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
        "original_student_work": [],
        "Sensitive Data Removed": []
    }
    sas = sa_crud.read_by_assignment_id(assignment_id, db)
    for sa in sas:
        rmws = await rm_crud.read_by_student_answer_id(sa.id, db)
        rmws_dict = [rmw.__dict__ for rmw in rmws]
        rsp["File Name"].append(sa.student_name)
        rsp["Student Work"].append(sa.protected_answer)
        rsp["original_student_work"].append(sa.answer)
        rsp["Sensitive Data Removed"].append([f"""{r.get("id")}.{r.get("order")}.{r.get("original_value")}""" for r in rmws_dict])
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

@router.post("/privacy/update")
async def update_sensi_info(
    data: UpdatePrivacyInfoSchema, db: Session = Depends(get_db)
):
    if len(data.removed_word_ids):
        sa_id = rm_crud.read(data.removed_word_ids[0], db).student_answer_id

        # delete removed info
        deleted_ids = data.removed_word_ids
        rm_crud.bulk_soft_delete(deleted_ids, db)

        # update student work
        sa_crud.update(sa_id, {"protected_answer": data.modified_student_work}, db)

    return Response()


@router.get("/result/{assignment_id}")
async def get_detail_sensi_info(
    assignment_id: int, db: Session = Depends(get_db)
):
    def get_score(text):
        if not text:
            return '0/0'
        pattern = r"Score:\s*(\d+/\d+)"
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return '0/0'
    asm = asm_crud.read(assignment_id, db)
    sas = sa_crud.read_by_assignment_id(assignment_id, db)
    
    rsp = {
        "Assignment Question": [asm.number_of_questions],
        "Student Name": [],
        "Student ID": [],
        "Question ID": [],
        "Question Score": [],
        "Question Feedbacks": []
    }

    for sa in sas:
        rsp["Student Name"].append(sa.student_name)
        rsp["Student ID"].append(sa.student_name)
        rsp["Question ID"].append(sa.question_title)
        rsp["Question Score"].append(sa.score)
        rsp["Question Feedbacks"].append(sa.result)

    return [rsp]
        

