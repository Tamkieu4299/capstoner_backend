
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class StudentAnswer(BaseModel):
    __tablename__ = "student_answers"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    student_name = Column(String, nullable=True)
    answer = Column(String, nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=True)
    question_title = Column(String, nullable=True)
    result = Column(String, nullable=True)
    class Config:
        orm_mode = True 
