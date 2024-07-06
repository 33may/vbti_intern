from pydantic import BaseModel, EmailStr, constr, field_validator


class UserAdd(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)

    @field_validator("password")
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v


class UserGet(UserAdd):
    id: int

class UserLogin(UserAdd):
    pass

class UserCreated(BaseModel):
    message: str
    id: int

class LogedIn(BaseModel):
    message: str