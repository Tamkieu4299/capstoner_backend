from typing import Optional, List
import json
from pydantic import BaseModel

class JobRegisterSchema(BaseModel):
    title: str
    description: str
    min_salary: float
    max_salary: float
    items: List[int]
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class Item(BaseModel):
    key: str
    value: str
    description: str = None
    label: str
    
    class Config:
        orm_mode = True


class Vendor(BaseModel):
    id: int
    name: str = None
    phone: str = None
    email: str = None
    address: str = None
    avatar: str = None
    business_license: str = None

    class Config:
        orm_mode = True


class JobResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    min_salary: float
    max_salary: float
    vendor: Vendor
    items: List[Item] = []

    class Config:
        orm_mode = True


class JobUpdateInfoSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    min_salary: Optional[float]
    max_salary: Optional[float]
    items: Optional[List[int]]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
class JobPictureUrlSchema(BaseModel):
    url: str
