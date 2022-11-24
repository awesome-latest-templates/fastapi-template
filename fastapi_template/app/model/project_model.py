from typing import Optional

from sqlalchemy import Column, Text, text
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class Project(BaseSQLModel, table=True):
    name: str = Field(sa_column=Column('name', Text, nullable=False, server_default=text("''")))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text))
