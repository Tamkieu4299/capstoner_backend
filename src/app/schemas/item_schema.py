from typing import Optional, List
import json
from pydantic import BaseModel

class ItemRegisterSchema(BaseModel):
    key: str
    value: str
    description: str = None
    label: str

class ItemResponseSchema(BaseModel):
    key: str
    value: str
    description: str = None
    label: str
    
    class Config:
        orm_mode = True


class ItemUpdateInfoSchema(BaseModel):
    key: Optional[str]
    value: Optional[str]
    description: Optional[str]
    label: Optional[str]
