
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class StudentAnswer(BaseModel):
    __tablename__ = "student_answers"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    answer = Column(String, nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=True)
    result = Column(String, nullable=True)
    created_by = Column(
        Integer,
        ForeignKey(
            "users.id",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
    )

    assignment = relationship(
        "Assignment", backref="answer_for_assignment", foreign_keys=[assignment_id]
    )
    question = relationship(
        "Question", backref="answer_for_question", foreign_keys=[question_id]
    )

    class Config:
        orm_mode = True 
