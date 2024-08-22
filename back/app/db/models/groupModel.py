from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    users = relationship(
        "User", secondary="users_projects", back_populates="projects", lazy="selectin"
    )


class ProjectGroup(Base):
    __tablename__ = "project_group"
    group_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete="CASCADE"), primary_key=True)

class UserGroup(Base):
    __tablename__ = "user_group"
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)