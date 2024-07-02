from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    email: str

users = [User(id=1, name="John Doe", email="john@example.com")]

@router.get("/users", response_model=List[User])
def get_users():
    return users

@router.post("/users", response_model=User)
def add_user(user: User):
    users.append(user)
    return user
