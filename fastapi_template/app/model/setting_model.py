from typing import Optional

from sqlalchemy import Column, Text, text
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class Setting(BaseSQLModel, table=True):
    setting_type: str = Field(sa_column=Column('setting_type', Text, nullable=False, server_default=text("''")))
    setting_value: Optional[str] = Field(default=None,
                                         sa_column=Column('setting_value', Text, server_default=text("''")))
