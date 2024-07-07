from app.db.repos.userRepo import UserRepo
from app.schemas.userSchema import UserAdd, UserLogin, UserGet
from app.utils.exceptions.WrongCredentials import WrongCredentials
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx
from app.utils.jwt import create_access_token
from datetime import timedelta
from app.utils.core.config import settings


async def fetch_users():
    result = await UserRepo.db_get_users()
    return result


async def create_user(user: UserAdd):
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
        data={"sub": user_record.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_user_by_email(email: str) -> UserGet:
    result = await UserRepo.db_get_user_by_email(email)
    return result
