# async def fetch_project(project_id):
from app.db.repos.projectRepo import ProjectRepo
from app.schemas.projectSchema import ProjectAdd


async def get_projects():
    result = await ProjectRepo.get_projects()
    return result


async def create_new_project(project_data: ProjectAdd):
    await ProjectRepo.create_project(project_data)
    return
