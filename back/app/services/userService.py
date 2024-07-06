from app.db.exceptions.alreadyExistEx import AlreadyExistEx
from app.db.repos.userRepo import UserRepo
from app.schemas.userSchema import UserAdd

async def fetch_users():
    result = await UserRepo.db_get_users()
    return result

async def create_user(user: UserAdd):
    existing_user = await UserRepo.db_get_user_by_email(user.email)
    if existing_user:
        raise AlreadyExistEx(message="Email already registered")
    id = await UserRepo.db_add_user(user)
    return id
