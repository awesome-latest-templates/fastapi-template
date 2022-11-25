from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Text, Integer
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
    id: Optional[int] = Field(
        default_factory=gen.__next__,
        primary_key=True,
        index=True,
        nullable=False,
    )
    create_time: Optional[str] = Field(
        sa_column=Column('create_time', Text, nullable=False))
    update_time: Optional[str] = Field(
        sa_column=Column('update_time', Text, nullable=False), default=datetime.utcnow())
    create_by: Optional[str] = Field(
        sa_column=Column('create_by', Text, nullable=False), default="system")
    update_by: Optional[str] = Field(
        sa_column=Column('update_by', Text, nullable=False), default="system")
    is_active: int = Field(
        sa_column=Column('is_active', Integer, nullable=False), default=1)
