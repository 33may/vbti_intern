from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request

from app.schemas.token import Token, TokenData
from app.schemas.userSchema import UserGet, UserCreated, UserAdd, UserLogin, LogedIn
from app.services.userService import fetch_users, create_user, login_user
from app.utils.exceptions.WrongCredentials import WrongCredentials
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx
from app.dependencies import get_current_user, get_current_admin_user
from app.utils.jwt import add_token_to_blacklist

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("")
async def get_users(current_user: UserGet = Depends(get_current_admin_user)) -> List[UserGet]:
    users = await fetch_users()
    return users

@router.get("/admin")
async def get_admin_data(current_user: TokenData = Depends(get_current_admin_user)):
    return {"message": "This is an admin-only endpoint"}


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


@router.post("/logout")
async def logout(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        add_token_to_blacklist(token)
        return {"message": "Successfully logged out"}
    raise HTTPException(status_code=401, detail="Could not validate credentials")