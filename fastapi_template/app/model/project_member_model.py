from sqlalchemy import Column, Integer
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class ProjectMember(BaseSQLModel, table=True):
    project_id: int = Field(sa_column=Column('project_id', Integer, nullable=False))
    user_id: int = Field(sa_column=Column('user_id', Integer, nullable=False))
