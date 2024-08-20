from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str

class tokenRole(str, Enum):
    admin = "admin"
    user = "user"

class TokenData(BaseModel):
    email: str
    exp: datetime
    account_type: tokenRole