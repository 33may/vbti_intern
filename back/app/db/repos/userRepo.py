from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import sessionLocal
from app.db.models.userModel import User
from app.schemas.userSchema import UserAdd
from app.utils.Crypt import Crypt


class UserRepo:
    @classmethod
    async def db_add_user(cls, data: UserAdd) -> User:
        async with sessionLocal() as session:
            user_dict = data.model_dump()
            user_dict['password'] = Crypt.hash_password(user_dict['password'])
            user_dict['type'] = 'user'
            user = User(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def db_delete_user(cls, data: User):
        async with sessionLocal() as session:
            await session.delete(data)
            await session.commit()
            return

    @classmethod
    async def db_get_users(cls) -> List[User]:
        async with sessionLocal() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            return users

    @classmethod
    async def db_get_user_by_id(cls, id: int) -> User:
        async with sessionLocal() as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    @classmethod
    async def db_get_user_by_email_template(cls, email: str, session: AsyncSession) -> User:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    @classmethod
    async def db_get_user_by_email(cls, email: str) -> User:
        async with sessionLocal() as session:
            user = await cls.db_get_user_by_email_template(email, session)
            return user

    @classmethod
    async def db_verify_user(cls, email: str, password: str):
        async with sessionLocal() as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            user = result.scalars().first()
            if user and Crypt.verify_password(password, user.password):
                return user
            return None