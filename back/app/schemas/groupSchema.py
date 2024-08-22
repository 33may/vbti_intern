from typing import List

from pydantic import BaseModel

from app.schemas.projectSchema import ProjectUser


class GroupGet(BaseModel):
    name: str
    users: List[ProjectUser]
    id: int

class GroupCreate(BaseModel):
    name: str

class GroupDelete(BaseModel):
    id: int

class UserToGroup(BaseModel):
    user_id: int

class UsersToGroup(BaseModel):
    user_id: List[int]