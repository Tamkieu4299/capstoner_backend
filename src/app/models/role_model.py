
from sqlalchemy import Column, Integer, String

from ._base_model import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    
    class Config:
        orm_mode = True 
