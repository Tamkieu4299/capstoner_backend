import json

from pydantic import BaseModel


class ReviewRegisterSchema(BaseModel):
    job_id: int
    comment: str
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class ReviewResponseSchema(BaseModel):
    id: int
    created_by: int
    job_id: int
    comment: str = None

    class Config:
        orm_mode = True

class ReviewAttachmentSchema(BaseModel):
    url: str