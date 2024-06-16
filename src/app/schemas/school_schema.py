from pydantic import BaseModel

class SchoolRegisterSchema(BaseModel):
    name: str

class SchoolResponseSchema(BaseModel):
    id: int
    name: str