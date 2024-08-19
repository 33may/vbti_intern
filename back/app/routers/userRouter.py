from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request

from app.schemas.generalSchema import Message
from app.schemas.projectSchema import AddUserToProjectRequest
from app.schemas.token import Token, TokenData
from app.schemas.userSchema import UserGet, UserAdd, UserLogin
from app.services.projectService import  add_user_to_project, get_project_users
from app.services.userService import fetch_users, create_user, login_user, fetch_user
from app.utils.exceptions.NotFound import NotFound
from app.utils.exceptions.WrongCredentials import WrongCredentials
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx
from app.dependencies import get_current_admin_user
from app.utils.jwt import add_token_to_blacklist

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("")
async def get_users(current_user_token: TokenData = Depends(get_current_admin_user)) -> List[UserGet]:
    users = await fetch_users()
    return users


@router.get("/{user_id}")
async def get_user(user_id: int, current_user_token: TokenData = Depends(get_current_admin_user)) -> UserGet:
    try:
        user = await fetch_user(user_id)
        return user
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e.message))


@router.post("/{project_id}/add_user")
async def add_user(project_id: int, request: AddUserToProjectRequest, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await add_user_to_project(project_id, request.user_email)
        return Message(message=f"User {request.user_email} added to project successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}/get_users")
async def get_users_on_project(project_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> List[UserGet]:
    try:
        users = await get_project_users(project_id)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_user(user_id: int, current_user_token: TokenData = Depends(get_current_admin_user)) -> UserGet:
    try:
        user = await fetch_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.get("/admin")
# async def get_admin_data(current_user_token: TokenData = Depends(get_current_admin_user)):
#     return {"message": "This is an admin-only endpoint"}


@router.post("/register")
async def register_user(user: UserAdd) -> Token:
    try:
        access_token = await create_user(user)
        return access_token
    except AlreadyExistEx as e:
        raise HTTPException(status_code=403, detail=e.message)


@router.post("/login")
async def login(form_data: UserLogin) -> Token:
    try:
        access_token = await login_user(form_data)
        return access_token
    except WrongCredentials as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.post("/logout")
async def logout(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        add_token_to_blacklist(token)
        return {"message": "Successfully logged out"}
    raise HTTPException(status_code=401, detail="Could not validate credentials")
