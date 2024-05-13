from typing import Optional, Union
from pydantic import BaseModel, UUID4

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Union[str, None] = None

# EOF
