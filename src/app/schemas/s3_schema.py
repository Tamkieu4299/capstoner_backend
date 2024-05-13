from pydantic import BaseModel


class S3ResponseModel(BaseModel):
    bucket_name: str
    path: str

    class Config:
        orm_mode = True
