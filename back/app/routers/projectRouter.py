from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request


from app.dependencies import get_current_user, get_current_admin_user
from app.schemas.generalSchema import Message
from app.schemas.projectSchema import ProjectGet, ProjectAdd
from app.schemas.userSchema import UserGet
from app.services.projectService import get_projects, create_new_project

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.get("/all")
async def get_all_projects(current_user: UserGet = Depends(get_current_admin_user)) -> List[ProjectGet]:
    users = await get_projects()
    return users


@router.post("")
async def create_project(project_data: ProjectAdd, current_user: UserGet = Depends(get_current_admin_user)) -> Message:
    try:
        await create_new_project(project_data)
        return Message(message="Project created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

