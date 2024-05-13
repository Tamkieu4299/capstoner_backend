from datetime import date
from typing import Optional

from pydantic import BaseModel


class VendorRegisterSchema(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    business_license: str
    
    class Config:
        orm_mode = True

class VendorResponseSchema(BaseModel):
    id: int
    name: str = None
    phone: str = None
    email: str = None
    address: str = None
    avatar: str = None
    business_license: str = None

    class Config:
        orm_mode = True


class VendorUpdateInfoSchema(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[bool]
    DOB: Optional[date]
    avatar: Optional[str]
    business_license: Optional[str]

   