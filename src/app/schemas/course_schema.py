from typing import List

from pydantic import BaseModel

class CourseRegisterSchema(BaseModel):
    code: str
    name: str
    semester: str
    year: str
    school_id: int
    

class Assignment(BaseModel):
    id: int
    name: str
    course_id: int
    
    class Config:
        orm_mode = True
    
class School(BaseModel):
    id: int
    name: str

class CourseResponseSchema(BaseModel):
    id: int
    code: str
    name: str
    semester: str
    year: str
    school: School = None
    assignments: List[Assignment] = []
    
    class Config:
        orm_mode = True