from sqlalchemy import Column, Text, text
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class Role(BaseSQLModel, table=True):
    name: str = Field(sa_column=Column('name', Text, nullable=False, unique=True))
    description: str = Field(sa_column=Column('description', Text, nullable=False, server_default=text("''")))
