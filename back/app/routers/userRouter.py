from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.generalSchema import Message
from app.schemas.projectSchema import ProjectGet
from app.schemas.token import TokenData
from app.schemas.userSchema import UserGet
from app.services.projectService import get_user_projects
from app.services.userService import fetch_users, fetch_user, delete_user
from app.utils.exceptions.NotFound import NotFound
from app.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("")
async def get_users(current_user_token: TokenData = Depends(get_current_admin_user)) -> List[UserGet]:
    users = await fetch_users()
    return users


@router.get("/{user_id}")
async def get_user(user_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> UserGet:
    try:
        user = await fetch_user(user_id)
        return user
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e.message))


@router.get("/{user_id}/projects")
async def get_projects_by_user_id(user_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> List[ProjectGet]:
    try:
        projects = await get_user_projects(user_id)
        return projects
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e.message))


@router.post("/{user_id}/delete")
async def delete_usr(user_id: int, admin_token: TokenData = Depends(get_current_admin_user)):
    try:
        await delete_user(user_id)
        return Message(message="User deleted successfully.")
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e.message))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e.message))