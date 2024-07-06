from typing import List
from fastapi import APIRouter
from fastapi import HTTPException

from app.db.exceptions.alreadyExistEx import AlreadyExistEx
from app.schemas.userSchema import UserGet, UserCreated, UserAdd
from app.services.userService import fetch_users, create_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("")
async def get_users() -> List[UserGet]:
    users = await fetch_users()
    return users

@router.post("")
async def add_user(user: UserAdd) -> UserCreated:
    try:
        new_user_id = await create_user(user)
        return UserCreated(message="created", id=new_user_id)
    except AlreadyExistEx as e:
        raise HTTPException(status_code=400, detail=e.message)