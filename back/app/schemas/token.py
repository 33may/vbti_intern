from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    email: str | None = None
    exp: datetime | None = None
    account_type: str | None = None
