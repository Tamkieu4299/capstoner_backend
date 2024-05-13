from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel


class VendorBusinessCategory(BaseModel):
    __tablename__ = "vendor_business_categories"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
    )
    business_category_id = Column(
        Integer,
        ForeignKey("business_categories.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
    )

    vendor = relationship(
        "Vendor", backref="vendor_business_category_vendor_id", foreign_keys=[vendor_id]
    )
    business_category = relationship(
        "BusinessCategory",
        backref="vendor_business_category_business_category_id",
        foreign_keys=[business_category_id],
    )

    class Config:
        orm_mode = True
