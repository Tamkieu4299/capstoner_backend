
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class JobItem(BaseModel):
    __tablename__ = "job_items"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=True)

    item = relationship("Item", backref="belongs_to_item", foreign_keys=[item_id])
    job = relationship("Job", backref="belongs_to_job", foreign_keys=[job_id])

    class Config:
        orm_mode = True 
