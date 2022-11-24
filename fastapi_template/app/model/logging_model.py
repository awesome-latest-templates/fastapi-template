from sqlalchemy import Column, Text, text
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class Logging(BaseSQLModel, table=True):
    user_name: str = Field(sa_column=Column('user_name', Text, nullable=False))
    operation_type: str = Field(sa_column=Column('operation_type', Text, nullable=False, server_default=text("''")))
