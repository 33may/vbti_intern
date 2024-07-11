# async def fetch_project(project_id):
from typing import List

from app.db.models.projectModel import Project
from app.db.models.userModel import User
from app.db.repos.projectRepo import ProjectRepo
from app.db.repos.userRepo import UserRepo
from app.schemas.projectSchema import ProjectAdd, ProjectGet


async def get_projects() -> List[Project]:
    result = await ProjectRepo.get_projects()
    return result


async def get_project(project_id: int) -> Project:
    result = await ProjectRepo.get_project(project_id)
    return result


async def create_new_project(project_data: ProjectAdd):
    await ProjectRepo.create_project(project_data)
    return


async def add_user_to_project(project_id: int, user_email: str):
    user = await UserRepo.db_get_user_by_email(user_email)
    project = await ProjectRepo.db_get_project_by_id(project_id)
    await ProjectRepo.add_user_to_project(project, user)


async def get_project_users(project_id: int) -> List[User]:
    project = await ProjectRepo.db_get_project_by_id(project_id)
    result = await ProjectRepo.get_project_users(project)
    return result
