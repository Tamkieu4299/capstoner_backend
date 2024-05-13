
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class Question(BaseModel):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    standard_answer = Column(String, nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=True)
    created_by = Column(
        Integer,
        ForeignKey(
            "users.id",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
    )

    assignment = relationship(
        "Assignment", backref="question_for_assignment", foreign_keys=[assignment_id]
    )

    class Config:
        orm_mode = True 
