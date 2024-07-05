from sqlalchemy import select

from app.db.db import sessionLocal
from app.db.models.userModel import User
from app.schemas.userSchema import UserAdd


class UserRepo:
    @classmethod
    async def db_add_user(cls, data: UserAdd):
        async with sessionLocal() as session:
            user_dict = data.model_dump()

            user = User(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()

            return user.id

    @classmethod
    async def db_get_users(cls):
        async with sessionLocal() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            return users

