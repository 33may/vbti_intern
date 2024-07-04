from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://admin:admin@localhost/vbti"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

sessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

# async def get_db():
#     async with sessionLocal() as session:
#         yield session
