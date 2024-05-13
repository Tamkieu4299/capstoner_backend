
from pydantic import BaseModel


class RegisterBaseSchema(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    phone: str
    password: str

    class Config:
        orm_mode = True


class LoginMobileSchema(BaseModel):
    phone: str
    password: str

    class Config:
        orm_mode = True
        
class LoginWebSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True 


class ResetPasswordBaseSchema(BaseModel):
    id: str
    password: str
    new_password: str

    class Config:
        orm_mode = True

class SimpleResetPasswordSchema(BaseModel):
    phone: str
    new_password: str

class RegisterResponse(BaseModel):
    id: int
    user_name: str
    phone: str

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    id: int
    user_name: str
    phone: str
    email: str = None
    avatar: str = None
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
