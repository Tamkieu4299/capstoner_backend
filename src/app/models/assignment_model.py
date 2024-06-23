
from sqlalchemy import Column, Integer, String,Boolean

from ._base_model import BaseModel

class Assignment(BaseModel):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    course_id = Column(Integer, nullable=False)
    marking_criteria_filepath = Column(String, nullable=False)
    questions_filepath = Column(String, nullable=False)
    instruction = Column(String, nullable=True)
    student_answer_filepath = Column(String, nullable=False)
    number_of_questions = Column(Integer, default=0)
    number_of_submissions = Column(Integer, default = 0)
    evaluation_status = Column(Boolean, default=False)

    class Config:
        orm_mode = True 
