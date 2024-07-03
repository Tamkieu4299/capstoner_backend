
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class RemovedWords(BaseModel):
    __tablename__ = "removed_words"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    student_answer_id = Column(Integer, nullable=False)
    original_value = Column(String, nullable=False)
    order = Column(Integer,  nullable=False)
    
    class Config:
        orm_mode = True 
