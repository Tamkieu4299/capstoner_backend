import json
from typing import List

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
    
class Question(BaseModel):
    id: int
    standard_answer: str = None
    assignment_id: int
    instruction: str
    marking_criteria: str

    class Config:
        orm_mode = True

class AssignmentResponseSchema(BaseModel):
    id: int
    name: str
    course_id: int
    questions: List[Question] = []
    
    class Config:
        orm_mode = True