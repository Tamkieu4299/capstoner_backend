
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class Course(BaseModel):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    code = Column(String, nullable=True)
    name = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    year = Column(String, nullable=False)
    school_id = Column(Integer, nullable=False)

    created_by = Column(
        Integer,
        ForeignKey(
            "users.id",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
    )

    class Config:
        orm_mode = True 
