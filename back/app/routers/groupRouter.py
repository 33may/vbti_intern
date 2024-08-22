from fastapi import APIRouter

from app.schemas.generalSchema import Message
from app.schemas.groupSchema import GroupGet, UserToGroup, UsersToGroup

router = APIRouter(
    prefix="/group",
    tags=["group-user"],
)

@router.get("/{group_id}")
async def get_group(group_id: int) -> GroupGet:
    return

@router.post("/{group_id}/add_user")
async def add_user_to_group(group_id: int, request: UserToGroup) -> Message:
    return

@router.post("/{group_id}/add_users")
async def add_users_to_group(group_id: int, request: UsersToGroup) -> Message:
    return

@router.post("/{group_id}/delete_user")
async def delete_group(project_id: int, reqyest: UserToGroup) -> Message:
    return