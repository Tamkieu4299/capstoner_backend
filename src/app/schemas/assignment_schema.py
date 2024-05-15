import json
from typing import List

from pydantic import BaseModel

class AssignmentRegisterSchema(BaseModel):
    id: int
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
    standard_answer: str
    assignment_id: int

    class Config:
        orm_mode = True

class AssignmentResponseSchema(BaseModel):
    id: int
    name: str
    questions: List[Question] = []
    
    class Config:
        orm_mode = True