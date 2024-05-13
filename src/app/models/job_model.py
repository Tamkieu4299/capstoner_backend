from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel


class Job(BaseModel):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    min_salary = Column(Float, nullable=False)
    max_salary = Column(Float, nullable=False)
    picture = Column(String, nullable=False)
    vendor_id = Column(
        Integer,
        ForeignKey(
            "vendors.id",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
    )
    created_by = Column(
        Integer,
        ForeignKey(
            "users.id",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
    )
    updated_by = Column(
        Integer,
        ForeignKey(
            "users.id",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
    )
    category_id = Column(Integer, nullable=True)

    vendor = relationship("Vendor", backref="belongs_to_vendor", foreign_keys=[vendor_id])

    class Config:
        orm_mode = True
