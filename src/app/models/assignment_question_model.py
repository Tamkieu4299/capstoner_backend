
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class AssignmentQuestion(BaseModel):
    __tablename__ = "assignment_questions"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=True)

    question = relationship("Question", backref="belongs_to_question", foreign_keys=[question_id])
    assignment = relationship("Assignment", backref="belongs_to_assignment", foreign_keys=[assignment_id])

    class Config:
        orm_mode = True 
