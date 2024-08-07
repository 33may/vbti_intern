from typing import List
from fastapi import APIRouter, Depends, HTTPException


from app.dependencies import get_current_admin_user, get_current_user
from app.schemas.generalSchema import Message
from app.schemas.projectSchema import ProjectGet, ProjectAdd
from app.schemas.token import TokenData
from app.schemas.userSchema import UserGet
from app.services.projectService import get_projects, create_new_project, \
    get_project, get_user_projects
from app.services.userService import get_user_by_email
from app.utils.exceptions.NotFound import NotFound

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/user")
async def get_user_project(admin_token: TokenData = Depends(get_current_user)) -> List[ProjectGet]:
    user = await get_user_by_email(admin_token.email)
    projects = await get_user_projects(user.id)
    return projects

@router.get("/all")
async def get_all_projects(admin_token: TokenData = Depends(get_current_admin_user)) -> List[ProjectGet]:
    projects = await get_projects()
    return projects


@router.post("")
async def create_project(project_data: ProjectAdd, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await create_new_project(project_data)
        return Message(message="Project created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}")
async def get_users_on_project(project_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> ProjectGet:
    try:
        project = await get_project(project_id)
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/projects")
async def get_user(user_id: int, current_user_token: TokenData = Depends(get_current_admin_user)) -> List[ProjectGet]:
    try:
        projects = await get_user_projects(user_id)
        return projects
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e.message))

