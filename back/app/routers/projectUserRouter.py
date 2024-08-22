from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_admin_user
from app.schemas.generalSchema import Message
from app.schemas.projectSchema import AddUserToProjectRequestById, DeleteUserFromProjectRequestById, ProjectUser
from app.schemas.token import TokenData
from app.services.projectService import add_user_to_project, delete_user_from_project, get_project_users
from app.utils.exceptions.NotFound import NotFound
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx

router = APIRouter(
    prefix="/projects",
    tags=["project-user"],
)

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