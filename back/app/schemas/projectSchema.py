from pydantic import BaseModel


class ProjectAdd(BaseModel):
    name: str
    description: str | None = None


class ProjectGet(ProjectAdd):
    id: int
