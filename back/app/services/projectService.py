from typing import List

from app.db.models.projectModel import Project
from app.db.repos.projectRepo import ProjectRepo
from app.schemas.projectSchema import ProjectAdd, ProjectUser, UserRole
from app.services.userService import fetch_user
from app.utils.exceptions.NotFound import NotFound
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx


async def get_projects() -> List[Project]:
    return await ProjectRepo.get_projects()

async def get_project(project_id: int) -> Project:
    project = await ProjectRepo.get_project(project_id)
    if not project:
        raise NotFound(f"Project with ID {project_id} not found")
    return project

async def create_new_project(project_data: ProjectAdd):
    try:
        await ProjectRepo.create_project(project_data)
    except Exception as e:
        raise Exception(f"Failed to create project: {str(e)}")

async def delete_project(project_id: int):
    try:
        await ProjectRepo.db_delete_project(project_id)
    except Exception as e:
        raise NotFound(f"Project {project_id} does not exist")


async def get_project_users(project_id: int) -> List[ProjectUser]:
    result = await ProjectRepo.get_project_users(project_id)
    if not result:
        raise NotFound(f"Project with ID {project_id} not found or has no users")

    project_users = [
        ProjectUser(
            id=user.id,
            email=user.email,
            role=UserRole(user_role)
        )
        for user, user_role in result
    ]
    return project_users


async def add_user_to_project(project_id: int, user_id: int, user_role: str):
    project = await ProjectRepo.get_project(project_id)
    if not project:
        raise NotFound(f"Project with ID {project_id} not found")

    user = await fetch_user(user_id)
    if not user:
        raise NotFound(f"User with ID {user_id} not found")

    user_projects = await get_user_projects(user.email)
    if any(project.id == project_id for project in user_projects):
        raise AlreadyExistEx(f"User {user_id} is already in the project {project_id}")

    await ProjectRepo.add_user_to_project(project_id, user, user_role)


async def delete_user_from_project(project_id: int, user_id: int):
    project = await ProjectRepo.get_project(project_id)
    if not project:
        raise NotFound(f"Project with ID {project_id} not found")
    user = await fetch_user(user_id)
    if not user:
        raise NotFound(f"User with ID {user_id} not found")
    await ProjectRepo.delete_user_from_project(project_id, user)


async def get_user_projects(user_email: str) -> List[Project]:
    projects = await ProjectRepo.get_projects_by_user_email(user_email)
    return projects