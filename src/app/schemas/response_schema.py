from typing import List

from pydantic import BaseModel


class ResponseData(BaseModel):
    status: bool
    message: str
    data: dict

    class Config:
        orm_mode = True


class ResponseArray(BaseModel):
    status: bool
    message: str
    data: List[dict]

    class Config:
        orm_mode = True


class ResponseToken(ResponseData):
    token: str
