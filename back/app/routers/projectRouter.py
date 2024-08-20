from typing import List
from fastapi import APIRouter, Depends, HTTPException


from app.dependencies import get_current_admin_user, get_current_user
from app.schemas.generalSchema import Message
from app.schemas.projectSchema import ProjectGet, ProjectAdd, AddUserToProjectRequestById, ProjectUser, \
    deleteProgectRequest
from app.schemas.token import TokenData
from app.schemas.userSchema import UserGet
from app.services.projectService import get_projects, create_new_project, \
    get_project, get_user_projects, add_user_to_project, get_project_users, delete_project
from app.services.userService import get_user_by_email

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.get("/my")
async def get_my_project(user_token: TokenData = Depends(get_current_user)) -> List[ProjectGet]:
    projects = await get_user_projects(user_token.email)
    return projects

@router.get("/all")
async def get_all_projects(admin_token: TokenData = Depends(get_current_admin_user)) -> List[ProjectGet]:
    projects = await get_projects()
    return projects


@router.post("/create")
async def create_project(project_data: ProjectAdd, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await create_new_project(project_data)
        return Message(message="Project created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete")
async def delete_proj(request: deleteProgectRequest, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await delete_project(request.project_id)
        return Message(message="Project deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{project_id}")
async def get_proj(project_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> ProjectGet:
    try:
        project = await get_project(project_id)
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/add_user")
async def add_user(project_id: int, request: AddUserToProjectRequestById, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await add_user_to_project(project_id, request.user_id, request.user_role)
        return Message(message=f"User added to project successfully")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}/get_users")
async def get_users_on_project(project_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> List[ProjectUser]:
    try:
        users = await get_project_users(project_id)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
