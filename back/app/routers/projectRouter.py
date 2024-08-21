from typing import List
from fastapi import APIRouter, Depends, HTTPException


from app.dependencies import get_current_admin_user, get_current_user
from app.schemas.generalSchema import Message
from app.schemas.projectSchema import ProjectGet, ProjectAdd, AddUserToProjectRequestById, ProjectUser, \
    deleteProgectRequest, DeleteUserFromProjectRequestById
from app.schemas.token import TokenData
from app.services.projectService import get_projects, create_new_project, \
    get_project, get_user_projects, add_user_to_project, get_project_users, delete_project, delete_user_from_project
from app.utils.exceptions.NotFound import NotFound
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.get("/my")
async def get_my_project(user_token: TokenData = Depends(get_current_user)) -> List[ProjectGet]:
    try:
        projects = await get_user_projects(user_token.email)
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_projects(admin_token: TokenData = Depends(get_current_admin_user)) -> List[ProjectGet]:
    try:
        projects = await get_projects()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}")
async def get_proj(project_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> ProjectGet:
    try:
        project = await get_project(project_id)
        return project
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/add_user")
async def add_user_project(project_id: int, request: AddUserToProjectRequestById, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await add_user_to_project(project_id, request.user_id, request.user_role)
        return Message(message="User added to project successfully")
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExistEx as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/delete_user")
async def delete_user_project(project_id: int, request: DeleteUserFromProjectRequestById, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await delete_user_from_project(project_id, request.user_id)
        return Message(message="User removed from project successfully")
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}/get_users")
async def get_users_on_project(project_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> List[ProjectUser]:
    try:
        users = await get_project_users(project_id)
        return users
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
