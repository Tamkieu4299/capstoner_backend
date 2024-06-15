from typing import List

from pydantic import BaseModel

class CourseRegisterSchema(BaseModel):
    code: str
    name: str
    semester: str
    year: str
    

class Assignment(BaseModel):
    id: int
    name: str
    course_id: int
    
    class Config:
        orm_mode = True
    

class CourseResponseSchema(BaseModel):
    id: int
    code: str
    name: str
    semester: str
    year: str
    assignments: List[Assignment] = []
    
    class Config:
        orm_mode = True