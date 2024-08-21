from enum import Enum

from pydantic import BaseModel, EmailStr


class ProjectAdd(BaseModel):
    name: str
    description: str | None = None


class ProjectGet(ProjectAdd):
    id: int


class UserRole(str, Enum):
    MANAGER = "manager"
    ANNOTATOR = "annotator"
    REVIEWER = "reviewer"


class ProjectUser(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

class deleteProgectRequest(BaseModel):
    project_id: int

class AddUserToProjectRequestById(BaseModel):
    user_role: UserRole
    user_id: int

class DeleteUserFromProjectRequestById(BaseModel):
    user_id: int