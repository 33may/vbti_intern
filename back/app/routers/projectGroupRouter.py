from typing import List

from fastapi import APIRouter

from app.schemas.generalSchema import Message
from app.schemas.groupSchema import GroupGet, GroupCreate, GroupDelete

router = APIRouter(
    prefix="/projects",
    tags=["project-group"],
)


@router.get("/{project_id}/groups")
async def get_project_groups(project_id: int) -> List[GroupGet]:
    return

@router.post("/{project_id}/groups/create")
async def create_group(project_id: int, request: GroupCreate) -> Message:
    return

@router.post("/{project_id}/groups/delete")
async def delete_group(project_id: int, reqyest: GroupDelete) -> Message:
    return