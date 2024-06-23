from typing import List

from app.crud.question_crud import CRUDQuestion
from app.db.database import get_db
from app.models.question_model import Question
from app.utils.exception import CommonInvalid
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from app.schemas.question_schema import QuestionRegisterSchema, QuestionResponseSchema, QuestionRegisterByFileSchema
from sqlalchemy.orm import Session
from ..utils import s3_driver

from ..secret import get_current_active_user
logger = setup_logger(__name__)

router = APIRouter()

question_crud = CRUDQuestion(Question)

@router.post(
"/add",
    status_code=status.HTTP_201_CREATED,
    response_model=QuestionRegisterSchema,
)
async def register_question(
    question_data: QuestionRegisterSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    question_data_dict = question_data
    question_data_dict["created_by"] = current_user["user"].id
    new_question = await question_crud.create(question_data_dict, db)
    if new_question is None:
        logger.info(
            f"Fail to create question"
        )
        raise CommonInvalid(detail=f"Fail to create question")
    return new_question.__dict__

@router.post(
"/create-by-files",
    status_code=status.HTTP_201_CREATED,
)
async def register_question_by_files(
    question_data: QuestionRegisterByFileSchema = Form(...),
    instruction: UploadFile = File(...),
    criteria: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    url_instruction = s3_driver.upload(file = instruction, dest_dir = "instruction", protocol="")
    instruction_data = s3_driver.get_file(url_instruction)
    
    url_criteria = s3_driver.upload(file = criteria, dest_dir = "criteria", protocol="")
    criteria_data = s3_driver.get_file(url_criteria)

    question_data_dict = question_data.dict()
    question_data_dict["created_by"] = current_user["user"].id

    new_question = await question_crud.create(question_data_dict, db)
    if new_question is None:
        logger.info(
            f"Fail to create question"
        )
        raise CommonInvalid(detail=f"Fail to create question")
    return new_question.__dict__

@router.get("/search/", response_model=List[QuestionResponseSchema])
async def get_questions(
    db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    questions = question_crud.get_all(db)
    questions_dict_list = [i.__dict__ for i in questions]
    logger.info(f"Number of questions: {len(questions)}")
    return questions_dict_list

@router.get("/search_by_assignment/{assignment_id}", response_model=List[QuestionResponseSchema])
async def get_questions_by_assigment_id(
    assignment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    questions = question_crud.read_by_assignment_id(assignment_id, db)
    questions_dict_list = [i.__dict__ for i in questions]
    logger.info(f"Number of questions: {len(questions)}")
    return questions_dict_list

@router.get("/search/{id}", response_model=QuestionResponseSchema)
async def get_questions(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    questions = question_crud.read(id, db)
    return questions.__dict__