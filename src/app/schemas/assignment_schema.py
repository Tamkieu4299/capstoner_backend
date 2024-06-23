import json
from typing import List
from datetime import datetime
from pydantic import BaseModel

class AssignmentRegisterSchema(BaseModel):
    course_id: int
    name: str
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class AssignmentResponseSchema(BaseModel):
    id: int
    name: str
    course_id: int
    marking_criteria_filepath: str
    questions_filepath: str
    student_answer_filepath: str
    number_of_questions: int = 0
    number_of_submissions: int = 0
    instruction: str = None
    created_at: datetime = None
    evaluation_status: bool
    lecture_check_status: bool
    sensitive_rmv_status: bool

    class Config:
        orm_mode = True