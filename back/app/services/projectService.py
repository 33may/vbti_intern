from typing import List

from app.db.models.projectModel import Project
from app.db.models.userModel import User
from app.db.repos.projectRepo import ProjectRepo
from app.db.repos.userRepo import UserRepo
from app.schemas.projectSchema import ProjectAdd, ProjectUser, UserRole


async def get_projects() -> List[Project]:
    result = await ProjectRepo.get_projects()
    return result


async def get_project(project_id: int) -> Project:
    result = await ProjectRepo.get_project(project_id)
    return result


async def create_new_project(project_data: ProjectAdd):
    await ProjectRepo.create_project(project_data)
    return

async def delete_project(project_id: int):
    success = await ProjectRepo.db_delete_project(project_id)
    if success:
        return
    else:
        raise ValueError(f'Project {project_id} does not exist')


async def add_user_to_project(project_id: int, user_id: int, user_role: str):
    user = await UserRepo.db_get_user_by_id(user_id)
    user_projects = await get_user_projects(user.email)
    if any(project.id == project_id for project in user_projects):
        raise ValueError("User is already in the project")
    await ProjectRepo.add_user_to_project(project_id, user, user_role)


async def get_project_users(project_id: int) -> List[User]:
    result = await ProjectRepo.get_project_users(project_id)
    project_users = [
        ProjectUser(
            id=user.id,
            email=user.email,
            role=UserRole(user_role)
        )
        for user, user_role in result
    ]
    return project_users


async def get_user_projects(user_email: str) -> List[Project]:
    projects = await ProjectRepo.get_projects_by_user_email(user_email)
    return projects