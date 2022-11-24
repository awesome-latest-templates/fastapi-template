from sqlalchemy import Column, Integer
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class UserRole(BaseSQLModel, table=True):
    user_id: int = Field(sa_column=Column('user_id', Integer, nullable=False))
    role_id: int = Field(sa_column=Column('role_id', Integer, nullable=False))
