from datetime import timedelta
from typing import List

from pycparser.ply.yacc import token

from app.db.models.userModel import User
from app.db.repos.userRepo import UserRepo
from app.schemas.token import Token
from app.schemas.userSchema import UserAdd, UserLogin, UserGet, UserFull
from app.utils.core.config import settings
from app.utils.exceptions.WrongCredentials import WrongCredentials
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx
from app.utils.jwt import create_access_token, createToken
from app.utils.exceptions.NotFound import NotFound


async def fetch_users() -> List[User]:
    result = await UserRepo.db_get_users()
    return result


async def fetch_user(id: int) -> User:
    result = await UserRepo.db_get_user_by_id(id)
    if result is None:
        raise NotFound("User not found")
    return result


async def create_user(user: UserAdd) -> Token:
    existing_user = await UserRepo.db_get_user_by_email(user.email)
    if existing_user:
        raise AlreadyExistEx(message="Email already registered")
    created_user = await UserRepo.db_add_user(user)
    token = createToken(created_user)
    return token


async def login_user(user: UserLogin) -> Token:
    user_record = await UserRepo.db_verify_user(user.email, user.password)
    if not user_record:
        raise WrongCredentials(message="Invalid credentials")
    token = createToken(user_record)
    return token

async def get_user_by_email(email: str) -> User:
    result = await UserRepo.db_get_user_by_email(email)
    return result
