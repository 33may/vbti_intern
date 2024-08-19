from pydantic import BaseModel, EmailStr, constr, field_validator

from app.db.models.userModel import User


class UserAdd(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)

    @field_validator("password")
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v


class UserGet(BaseModel):
    id: int
    email: EmailStr

class UserFull(UserGet):
    type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LogedIn(BaseModel):
    message: str


def convert_user_model_to_schema(user: User) -> UserGet:
    return UserGet(email=user.email, id=user.id)