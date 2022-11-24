from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Numeric, Text, text
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class FileInfo(BaseSQLModel, table=True):
    file_key: str = Field(sa_column=Column('file_key', Text, nullable=False))
    file_url: str = Field(sa_column=Column('file_url', Text, nullable=False))
    file_name: Optional[str] = Field(default=None, sa_column=Column('file_name', Text, server_default=text("''")))
    file_size: Optional[Decimal] = Field(default=None, sa_column=Column('file_size', Numeric, server_default=text('0')))
    content_type: Optional[str] = Field(default=None, sa_column=Column('content_type', Text, server_default=text("''")))
