import json

from pydantic import BaseModel

class QuestionRegisterSchema(BaseModel):
    standard_answer: str = None
    instruction: str
    marking_criteria: str
    assignment_id: int
    question_title: str
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class QuestionResponseSchema(BaseModel):
    id: int
    standard_answer: str = None
    instruction: str
    marking_criteria: str
    assignment_id: int
    question_title: str

    class Config:
        orm_mode = True