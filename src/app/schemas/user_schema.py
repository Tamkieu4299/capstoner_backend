from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    id: int
    user_name: str
    first_name: str
    last_name: str
    phone: str
    password: str
    gender: bool  # male is false because woman is always true

    class Config:
        orm_mode = True

class UserResponseSchema(BaseModel):
    id: int
    user_name: str
    first_name: str
    last_name: str
    phone: str
    gender: Optional[bool]
    DOB: Optional[date]
    email: Optional[str]
    address: Optional[str]
    avatar: Optional[str]

    class Config:
        orm_mode = True


class UserUpdateInfoSchema(BaseModel):
    user_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[bool]
    DOB: Optional[date]
    email: Optional[str]
    address: Optional[str]

   