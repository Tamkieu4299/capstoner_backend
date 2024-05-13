from sqlalchemy import Column, Integer, String

from ._base_model import BaseModel


class BusinessCategory(BaseModel):
    __tablename__ = "business_categories"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)

    class Config:
        orm_mode = True
