from sqlalchemy import select, Boolean
from app.db.db import sessionLocal
from app.db.models.projectModel import Project, UserProject
from app.db.models.userModel import User
from app.db.repos.userRepo import UserRepo
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
    async def db_delete_project(cls, project_id: int):
        async with sessionLocal() as session:
            query = select(Project).where(Project.id == project_id)
            result = await session.execute(query)
            project = result.scalars().first()

            if project:
                await session.delete(project)
                await session.commit()
            return

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
    async def add_user_to_project(cls, project_id: int, user_data: User, user_role: str):
        async with sessionLocal() as session:
            user_project = UserProject(user_id=user_data.id, project_id=project_id, user_role=user_role)
            session.add(user_project)
            await session.commit()
            return

    @classmethod
    async def delete_user_from_project(cls, project_id: int, user_data: User):
        async with sessionLocal() as session:
            query = select(UserProject).where(
                UserProject.project_id == project_id,
                UserProject.user_id == user_data.id
            )
            result = await session.execute(query)
            user_project = result.scalars().first()

            if user_project:
                await session.delete(user_project)
                await session.commit()
            return

    @classmethod
    async def get_project_users(cls, project_id: int) -> list[User]:
        async with sessionLocal() as session:
            query = (select(User, UserProject.user_role)
                .join(UserProject, User.id == UserProject.user_id)
                .where(UserProject.project_id == project_id))
            result = await session.execute(query)
            users_data = result.all()
            return users_data

    @classmethod
    async def get_projects_by_user_email(cls, user_email: str) -> list[Project]:
        async with sessionLocal() as session:
            query = select(User).where(User.email == user_email)
            result = await session.execute(query)
            user = result.scalars().first()
            return user.projects

