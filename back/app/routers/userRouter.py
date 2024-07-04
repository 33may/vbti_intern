from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.userService import get_users, create_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("")
async def get_users():
    users = await get_users()
    return users

@router.post("")
async def add_user():
    new_user = await create_user()
    return new_user
