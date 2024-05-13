from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel


class Vendor(BaseModel):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    business_license = Column(String, nullable=False, unique=True)
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

    created_by_user = relationship(
        "User", backref="vendor_created_user", foreign_keys=[created_by]
    )
    updated_by_user = relationship(
        "User", backref="vendor_updated_user", foreign_keys=[updated_by]
    )

    class Config:
        orm_mode = True
