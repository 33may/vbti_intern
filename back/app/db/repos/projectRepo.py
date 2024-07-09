from sqlalchemy import select
from app.db.db import sessionLocal
from app.db.models.projectModel import Project
from app.schemas.projectSchema import ProjectAdd


class ProjectRepo:
    @classmethod
    async def create_project(cls, data: ProjectAdd) -> Project:
        async with sessionLocal() as session:
            project_dict = data.model_dump()
            project = Project(**project_dict)
            session.add(project)
            await session.commit()
            return project

    @classmethod
    async def get_projects(cls) -> list[Project]:
        async with sessionLocal() as session:
            query = select(Project)
            result = await session.execute(query)
            projects = result.scalars().all()
            return projects
