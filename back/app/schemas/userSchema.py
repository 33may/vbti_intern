from pydantic import BaseModel

class UserAdd(BaseModel):
    username: str
    password: str

class UserGet(UserAdd):
    id: int

class UserCreated(BaseModel):
    message : str
    id: int