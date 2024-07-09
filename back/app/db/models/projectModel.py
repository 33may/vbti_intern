from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    users = relationship("User", secondary="users_projects", back_populates="projects", lazy="selectin")


class UserProject(Base):
    __tablename__ = "users_projects"
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), primary_key=True)