from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    gender = Column(Integer, nullable=True)
    DOB = Column(Date, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    vendor_id = Column(
        Integer,
        ForeignKey(
            "vendors.id",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
    )
    vendor = relationship("Vendor", backref="own_by_vendor", foreign_keys=[vendor_id])
    
    class Config:
        orm_mode = True
