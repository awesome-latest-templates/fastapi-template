from typing import Optional

from sqlalchemy import Column, Text, text
from sqlmodel import Field

from fastapi_template.app.model import BaseSQLModel


class User(BaseSQLModel, table=True):
    user_name: str = Field(sa_column=Column('user_name', Text, nullable=False, server_default=text("''")))
    password: str = Field(sa_column=Column('password', Text, nullable=False, server_default=text("''")))

    nick_name: Optional[str] = Field(default=None, sa_column=Column('nick_name', Text, server_default=text("''")))
    email: Optional[str] = Field(default=None, sa_column=Column('email', Text, server_default=text("''")))
    last_login_time: Optional[str] = Field(default=None, sa_column=Column('last_login_time', Text))
    avatar: Optional[str] = Field(default=None, sa_column=Column('avatar', Text))
