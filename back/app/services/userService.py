from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.userModel import User
from app.db.repos.userRepo import UserRepo
from app.schemas.userSchema import UserAdd


async def fetch_users():
    result = await UserRepo.db_get_users()
    return result

async def create_user(user: UserAdd):
    id = await UserRepo.db_add_user(user)
    return id
