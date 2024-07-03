import json

from pydantic import BaseModel

class StudentAnswerRegisterSchema(BaseModel):
    assignment_id: int

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class StudentAnswerResponseSchema(BaseModel):
    id: int
    answer: str
    assignment_id: int
    question_id: int
    protected_answer: str = None

    class Config:
        orm_mode = True

class PrivacyInputSchema(BaseModel):
    assignment_id: int

    class Config:
        orm_mode = True