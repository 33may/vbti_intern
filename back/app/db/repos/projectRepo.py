from sqlalchemy import select
from app.db.db import sessionLocal
from app.db.models.projectModel import Project, UserProject
from app.db.models.userModel import User
from app.schemas.projectSchema import ProjectAdd, ProjectGet
from app.schemas.userSchema import UserGet


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

    @classmethod
    async def get_project(cls, id: int) -> Project:
        async with sessionLocal() as session:
            query = select(Project).where(Project.id == id)
            result = await session.execute(query)
            project = result.scalars().first()
            return project

    @classmethod
    async def db_get_project_by_id(cls, id: int):
        async with sessionLocal() as session:
            query = select(Project).where(Project.id == id)
            result = await session.execute(query)
            project = result.scalars().first()
            return project

    @classmethod
    async def add_user_to_project(cls, project_data: Project, user_data: User):
        async with sessionLocal() as session:
            user_project = UserProject(user_id=user_data.id, project_id=project_data.id)
            session.add(user_project)
            await session.commit()
            return

    @classmethod
    async def get_project_users(cls, project: Project) -> list[User]:
        async with sessionLocal() as session:
            query = select(User).where(Project.id == project.id)
            result = await session.execute(query)
            users = result.scalars().all()
            return users

    @classmethod
    async def get_projects_by_user(cls, user: User) -> list[Project]:
        async with sessionLocal() as session:
            query = select(Project).where(User.id == user.id)
            result = await session.execute(query)
            users = result.scalars().all()
            return users
