from fastapi import APIRouter, HTTPException, Request
from app.schemas.generalSchema import Message
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

@router.post("/register", response_model=Token, responses={
    201: {"description": "User registered successfully", "content": {"application/json": {"example": {"access_token": "string"}}}},
    403: {"description": "User already exists", "content": {"application/json": {"example": {"detail": "Email already registered"}}}},
    422: {"description": "Validation Error", "content": {"application/json": {"example": {"detail": [{"loc": ["body", "email"], "msg": "value is not a valid email address", "type": "value_error.email"}]}}}},
})
async def register_user(user: UserAdd) -> Token:
    try:
        access_token = await create_user(user)
        return access_token
    except AlreadyExistEx as e:
        raise HTTPException(status_code=403, detail=e.message)


@router.post("/login", response_model=Token, responses={
    200: {"description": "User logged in successfully", "content": {"application/json": {"example": {"access_token": "string"}}}},
    401: {"description": "Invalid credentials", "content": {"application/json": {"example": {"detail": "Invalid credentials"}}}},
    422: {"description": "Validation Error", "content": {"application/json": {"example": {"detail": [{"loc": ["body", "email"], "msg": "value is not a valid email address", "type": "value_error.email"}]}}}},
})
async def login(form_data: UserLogin) -> Token:
    try:
        access_token = await login_user(form_data)
        return access_token
    except WrongCredentials as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.post("/logout", response_model=Message, responses={
    200: {"description": "User logged out successfully", "content": {"application/json": {"example": {"message": "Successfully logged out"}}}},
    401: {"description": "Could not validate credentials", "content": {"application/json": {"example": {"detail": "Could not validate credentials"}}}},
})
async def logout(request: Request) -> Message:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        add_token_to_blacklist(token)
        return Message(message="Successfully logged out")
    raise HTTPException(status_code=401, detail="Could not validate credentials")
