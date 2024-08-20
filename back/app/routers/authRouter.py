
from fastapi import APIRouter, HTTPException, Request

from app.schemas.token import Token
from app.schemas.userSchema import UserAdd, UserLogin
from app.services.userService import create_user, login_user
from app.utils.exceptions.WrongCredentials import WrongCredentials
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx
from app.utils.jwt import add_token_to_blacklist

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

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