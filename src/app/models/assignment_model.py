
from sqlalchemy import Column, Integer, String, ForeignKey

from ._base_model import BaseModel

class Assignment(BaseModel):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
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
