from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.db.schemas import UserCreate

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
