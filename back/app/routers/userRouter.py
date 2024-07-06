from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token import Token
from app.schemas.userSchema import UserGet, UserCreated, UserAdd, UserLogin, LogedIn
from app.services.userService import fetch_users, create_user, login_user
from app.utils.exceptions.WrongCredentials import WrongCredentials
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("")
async def get_users(current_user: UserGet = Depends(get_current_user)) -> List[UserGet]:
    users = await fetch_users()
    return users

@router.post("/register")
async def register_user(user: UserAdd) -> UserCreated:
    try:
        new_user_id = await create_user(user)
        return UserCreated(message="created", id=new_user_id)
    except AlreadyExistEx as e:
        raise HTTPException(status_code=403, detail=e.message)

@router.post("/login")
async def login_for_access_token(form_data : UserLogin) -> Token:
    try:
        access_token = await login_user(UserLogin(email=form_data.email, password=form_data.password))
        return access_token
    except WrongCredentials as e:
        raise HTTPException(status_code=401, detail=e.message)
