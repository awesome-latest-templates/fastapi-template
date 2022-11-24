from typing import Optional

from sqlalchemy import Column, Integer, Text, text
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class Menu(BaseSQLModel, table=True):
    pid: int = Field(sa_column=Column('pid', Integer, nullable=False, server_default=text('0')))
    title: str = Field(sa_column=Column('title', Text, nullable=False, server_default=text("''")))
    keep_alive: int = Field(sa_column=Column('keep_alive', Integer, nullable=False, server_default=text('1')))
    name: Optional[str] = Field(default=None, sa_column=Column('name', Text))
    type: Optional[str] = Field(default=None, sa_column=Column('type', Text))
    path: Optional[str] = Field(default=None, sa_column=Column('path', Text))
    icon: Optional[str] = Field(default=None, sa_column=Column('icon', Text))
    menu_type: Optional[str] = Field(default=None, sa_column=Column('menu_type', Text))
    component: Optional[str] = Field(default=None, sa_column=Column('component', Text))
    extend: Optional[str] = Field(default=None, sa_column=Column('extend', Text))
    remark: Optional[str] = Field(default=None, sa_column=Column('remark', Text))
