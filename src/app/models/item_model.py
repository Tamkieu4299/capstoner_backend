
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ._base_model import BaseModel

class Item(BaseModel):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    key = Column(String, nullable=False)
    label = Column(String, nullable=False)
    description = Column(String, nullable=True)
    value = Column(String,  nullable=False)
    
    class Config:
        orm_mode = True 
