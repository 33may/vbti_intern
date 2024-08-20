from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False, default='user')

    projects = relationship(
        "Project", secondary="users_projects", back_populates="users", lazy="selectin"
    )
