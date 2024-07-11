from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request


from app.dependencies import get_current_user, get_current_admin_user
from app.schemas.generalSchema import Message
from app.schemas.projectSchema import ProjectGet, ProjectAdd, AddUserToProjectRequest
from app.schemas.userSchema import UserGet, UserAdd
from app.services.projectService import get_projects, create_new_project, add_user_to_project, get_project_users, \
    get_project

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.get("/all")
async def get_all_projects(admin: UserGet = Depends(get_current_admin_user)) -> List[ProjectGet]:
    projects = await get_projects()
    return projects


@router.post("")
async def create_project(project_data: ProjectAdd, admin: UserGet = Depends(get_current_admin_user)) -> Message:
    try:
        await create_new_project(project_data)
        return Message(message="Project created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}")
async def get_users_on_project(project_id: int, admin: UserGet = Depends(get_current_admin_user)) -> ProjectGet:
    try:
        project = await get_project(project_id)
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/add_user")
async def add_user(project_id: int, request: AddUserToProjectRequest, admin: UserGet = Depends(get_current_admin_user)) -> Message:
    try:
        await add_user_to_project(project_id, request.user_email)
        return Message(message=f"User {request.user_email} added to project successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}/get_users")
async def get_users_on_project(project_id: int, admin: UserGet = Depends(get_current_admin_user)) -> List[UserGet]:
    try:
        users = await get_project_users(project_id)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
