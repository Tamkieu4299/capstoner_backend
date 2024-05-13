
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class Review(BaseModel):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    comment = Column(String, nullable=False)
    attachment = Column(String,  nullable=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=True)
    created_by = Column(
        Integer,
        ForeignKey(
            "users.id",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
    )

    job = relationship(
        "Job", backref="review_for_job", foreign_keys=[job_id]
    )

    class Config:
        orm_mode = True 
