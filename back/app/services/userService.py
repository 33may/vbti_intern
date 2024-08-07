from datetime import timedelta
from typing import List

from app.db.models.userModel import User
from app.db.repos.userRepo import UserRepo
from app.schemas.token import TokenData
from app.schemas.userSchema import UserAdd, UserLogin, UserGet, UserFull
from app.utils.core.config import settings
from app.utils.exceptions.WrongCredentials import WrongCredentials
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx
from app.utils.jwt import create_access_token
from app.utils.exceptions.NotFound import NotFound


async def fetch_users() -> List[User]:
    result = await UserRepo.db_get_users()
    return result


async def fetch_user(id: int) -> User:
    result = await UserRepo.db_get_user_by_id(id)
    if result is None:
        raise NotFound("User not found")
    return result


async def create_user(user: UserAdd) -> int:
    existing_user = await UserRepo.db_get_user_by_email(user.email)
    if existing_user:
        raise AlreadyExistEx(message="Email already registered")
    id = await UserRepo.db_add_user(user)
    return id


async def login_user(user: UserLogin):
    user_record = await UserRepo.db_verify_user(user.email, user.password)
    if not user_record:
        raise WrongCredentials(message="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_record.email, "account_type": user_record.type}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}


async def get_user_by_email(email: str) -> User:
    result = await UserRepo.db_get_user_by_email(email)
    return result
