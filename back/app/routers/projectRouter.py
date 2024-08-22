from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_admin_user, get_current_user
from app.schemas.generalSchema import Message
from app.schemas.projectSchema import ProjectGet, ProjectAdd, deleteProgectRequest
from app.schemas.token import TokenData
from app.services.projectService import get_projects, create_new_project, \
    get_project, get_user_projects, delete_project
from app.utils.exceptions.NotFound import NotFound

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.get("/my", response_model=List[ProjectGet], responses={
    401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Could not validate credentials"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "An unexpected error occurred"}}}},
})
async def get_my_project(user_token: TokenData = Depends(get_current_user)) -> List[ProjectGet]:
    try:
        projects = await get_user_projects(user_token.email)
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[ProjectGet], responses={
    401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Could not validate credentials"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "An unexpected error occurred"}}}},
})
async def get_all_projects(admin_token: TokenData = Depends(get_current_admin_user)) -> List[ProjectGet]:
    try:
        projects = await get_projects()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create", response_model=Message, responses={
    201: {"description": "Project created successfully", "content": {"application/json": {"example": {"message": "Project created successfully"}}}},
    401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Could not validate credentials"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "An unexpected error occurred"}}}},
})
async def create_project(project_data: ProjectAdd, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await create_new_project(project_data)
        return Message(message="Project created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete", response_model=Message, responses={
    200: {"description": "Project deleted successfully", "content": {"application/json": {"example": {"message": "Project deleted successfully"}}}},
    401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Could not validate credentials"}}}},
    404: {"description": "Project Not Found", "content": {"application/json": {"example": {"detail": "Project with ID X not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "An unexpected error occurred"}}}},
})
async def delete_proj(request: deleteProgectRequest, admin_token: TokenData = Depends(get_current_admin_user)) -> Message:
    try:
        await delete_project(request.project_id)
        return Message(message="Project deleted successfully")
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}", response_model=ProjectGet, responses={
    200: {"description": "Project found", "content": {"application/json": {"example": {"id": 1, "name": "Project Name", "description": "Project Description"}}}},
    401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Could not validate credentials"}}}},
    404: {"description": "Project Not Found", "content": {"application/json": {"example": {"detail": "Project with ID X not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "An unexpected error occurred"}}}},
})
async def get_proj(project_id: int, admin_token: TokenData = Depends(get_current_admin_user)) -> ProjectGet:
    try:
        project = await get_project(project_id)
        return project
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
