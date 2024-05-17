from typing import List

from app.crud.student_answer_crud import CRUDStudenAnswer
from app.db.database import get_db
from app.models.student_answer_model import StudentAnswer
from app.models.question_model import Question
from app.utils.exception import CommonInvalid
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from app.schemas.student_answer_schema import (
    StudentAnswerRegisterSchema,
    StudentAnswerResponseSchema,
)
from sqlalchemy.orm import Session
from ..utils import s3_driver
from openai import AzureOpenAI
from ..secret import get_current_active_user
from app.crud.question_crud import CRUDQuestion
import io
llm = AzureOpenAI(
    azure_endpoint="https://autograding-testing.openai.azure.com/",
    api_key="43a6c04255634b67803c38900d403bc0",
    api_version="2024-02-15-preview",
)
logger = setup_logger(__name__)

router = APIRouter()

sa_crud = CRUDStudenAnswer(StudentAnswer)
question_crud = CRUDQuestion(Question)


@router.post("/auto-grader", status_code=status.HTTP_201_CREATED)
async def auto_grader(
    student_answer_data: StudentAnswerRegisterSchema= Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    initial_prompt = "You are a teacher assistant who help to grade student code assesment."
    url = s3_driver.upload(file = file, dest_dir = "answer", protocol="")
    q = question_crud.read(student_answer_data.question_id, db)

    student_answer = s3_driver.get_file(url)
    prompt = " ".join(
        [initial_prompt, q.instruction, student_answer, q.marking_criteria]
    )
    messages = [
        {
            "role": "system",
            "content": "You are a teacher assistant who help to grade student code assesment.",
        },
        {"role": "user", "content": prompt},
    ]

    completion = llm.chat.completions.create(
        model="AzureCodeGrader",
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )

    sa_dict = student_answer_data.__dict__
    sa_dict["result"] = completion.choices[0].message.content
    sa_dict["answer"] = url
    new_sa = await sa_crud.create(sa_dict, db)
    return new_sa