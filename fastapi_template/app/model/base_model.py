from sqlalchemy import Column, Text, text, Integer
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel as _SQLModel, Field

from fastapi_template.app.util.snowflake import SnowflakeGenerator
from fastapi_template.config import settings

gen = SnowflakeGenerator(settings.SNOWFLAKE_INSTANCE)


class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__


class BaseSQLModel(SQLModel):
    id: int = Field(
        default_factory=next(gen),
        primary_key=True,
        index=True,
        nullable=False,
    )
    created_time: str = Field(sa_column=Column('create_time', Text, nullable=False))
    updated_time: str = Field(
        sa_column=Column('update_time', Text, nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    create_by: str = Field(sa_column=Column('create_by', Text, nullable=False, server_default=text("'system'")))
    update_by: str = Field(sa_column=Column('update_by', Text, nullable=False, server_default=text("'system'")))
    is_active: int = Field(sa_column=Column('is_active', Integer, nullable=False, server_default=text('1')))
