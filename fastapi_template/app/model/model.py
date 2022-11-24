from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Index, Integer, Numeric, Table, Text, text
from sqlalchemy.sql.sqltypes import NullType
from sqlmodel import Field, SQLModel

metadata = SQLModel.metadata


class FileInfo(SQLModel, table=True):
    __table_args__ = (
        Index('FileInfo_FileKey_IDX', 'FileKey'),
    )

    FileKey: str = Field(sa_column=Column('FileKey', Text, nullable=False))
    FileUrl: str = Field(sa_column=Column('FileUrl', Text, nullable=False))
    CreateTime: str = Field(sa_column=Column('CreateTime', Text, nullable=False))
    UpdateTime: str = Field(
        sa_column=Column('UpdateTime', Text, nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    CreateBy: str = Field(sa_column=Column('CreateBy', Text, nullable=False, server_default=text("''")))
    UpdateBy: str = Field(sa_column=Column('UpdateBy', Text, nullable=False, server_default=text("''")))
    IsActive: int = Field(sa_column=Column('IsActive', Integer, nullable=False, server_default=text('1')))
    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    FileName: Optional[str] = Field(default=None, sa_column=Column('FileName', Text, server_default=text("''")))
    FileSize: Optional[Decimal] = Field(default=None, sa_column=Column('FileSize', Numeric, server_default=text('0')))
    ContentType: Optional[str] = Field(default=None, sa_column=Column('ContentType', Text, server_default=text("''")))


class Logging(SQLModel, table=True):
    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    UserName: str = Field(sa_column=Column('UserName', Text, nullable=False))
    OperationType: str = Field(sa_column=Column('OperationType', Text, nullable=False, server_default=text("''")))
    CreateTime: str = Field(sa_column=Column('CreateTime', Text, nullable=False, server_default=text("''")))
    UpdateTime: str = Field(
        sa_column=Column('UpdateTime', Text, nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    CreateBy: str = Field(sa_column=Column('CreateBy', Text, nullable=False, server_default=text("''")))
    UpdateBy: str = Field(sa_column=Column('UpdateBy', Text, nullable=False, server_default=text("''")))
    IsActive: int = Field(sa_column=Column('IsActive', Integer, nullable=False, server_default=text('1')))


class Menu(SQLModel, table=True):
    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    Pid: int = Field(sa_column=Column('Pid', Integer, nullable=False, server_default=text('0')))
    Title: str = Field(sa_column=Column('Title', Text, nullable=False, server_default=text("''")))
    KeepAlive: int = Field(sa_column=Column('KeepAlive', Integer, nullable=False, server_default=text('1')))
    UpdateTime: str = Field(
        sa_column=Column('UpdateTime', Text, nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    Name: Optional[str] = Field(default=None, sa_column=Column('Name', Text))
    Type: Optional[str] = Field(default=None, sa_column=Column('Type', Text))
    Path: Optional[str] = Field(default=None, sa_column=Column('Path', Text))
    Icon: Optional[str] = Field(default=None, sa_column=Column('Icon', Text))
    MenuType: Optional[str] = Field(default=None, sa_column=Column('MenuType', Text))
    Component: Optional[str] = Field(default=None, sa_column=Column('Component', Text))
    Extend: Optional[str] = Field(default=None, sa_column=Column('Extend', Text))
    Remark: Optional[str] = Field(default=None, sa_column=Column('Remark', Text))
    CreateTime: Optional[str] = Field(default=None, sa_column=Column('CreateTime', Text))
    CreateBy: Optional[str] = Field(default=None, sa_column=Column('CreateBy', Text))
    UpdateBy: Optional[str] = Field(default=None, sa_column=Column('UpdateBy', Text))
    IsActive: Optional[int] = Field(default=None, sa_column=Column('IsActive', Integer, server_default=text('1')))


class Project(SQLModel, table=True):
    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    Name: str = Field(sa_column=Column('Name', Text, nullable=False, server_default=text("''")))
    CreateTime: str = Field(sa_column=Column('CreateTime', Text, nullable=False))
    UpdateTime: str = Field(
        sa_column=Column('UpdateTime', Text, nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    UpdateBy: str = Field(sa_column=Column('UpdateBy', Text, nullable=False, server_default=text("''")))
    IsActive: int = Field(sa_column=Column('IsActive', Integer, nullable=False, server_default=text('1')))
    Description: Optional[str] = Field(default=None, sa_column=Column('Description', Text))
    CreateBy: Optional[str] = Field(default=None, sa_column=Column('CreateBy', Text, server_default=text("''")))


class ProjectMember(SQLModel, table=True):
    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    ProjectId: int = Field(sa_column=Column('ProjectId', Integer, nullable=False))
    UserId: int = Field(sa_column=Column('UserId', Integer, nullable=False))
    CreateTime: str = Field(sa_column=Column('CreateTime', Text, nullable=False, server_default=text("''")))
    UpdateTime: str = Field(
        sa_column=Column('UpdateTime', Text, nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    CreateBy: str = Field(sa_column=Column('CreateBy', Text, nullable=False, server_default=text("''")))
    UpdateBy: str = Field(sa_column=Column('UpdateBy', Text, nullable=False, server_default=text("''")))
    IsActive: int = Field(sa_column=Column('IsActive', Integer, nullable=False, server_default=text('1')))


class Role(SQLModel, table=True):
    __table_args__ = (
        Index('Role_Id_IDX', 'Id', 'Name'),
    )

    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    Name: str = Field(sa_column=Column('Name', Text, nullable=False, unique=True))
    Description: str = Field(sa_column=Column('Description', Text, nullable=False, server_default=text("''")))
    CreateTime: str = Field(sa_column=Column('CreateTime', Text, nullable=False, server_default=text("''")))
    UpdateTime: str = Field(
        sa_column=Column('UpdateTime', Text, nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    CreateBy: str = Field(sa_column=Column('CreateBy', Text, nullable=False, server_default=text("''")))
    UpdateBy: str = Field(sa_column=Column('UpdateBy', Text, nullable=False, server_default=text("''")))
    IsActive: int = Field(sa_column=Column('IsActive', Integer, nullable=False, server_default=text('1')))


class Setting(SQLModel, table=True):
    __table_args__ = (
        Index('Setting_SettingKey_IDX', 'SettingType'),
    )

    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    SettingType: str = Field(sa_column=Column('SettingType', Text, nullable=False, server_default=text("''")))
    IsActive: int = Field(sa_column=Column('IsActive', Integer, nullable=False, server_default=text('1')))
    SettingValue: Optional[str] = Field(default=None, sa_column=Column('SettingValue', Text, server_default=text("''")))
    CreateTime: Optional[str] = Field(default=None, sa_column=Column('CreateTime', Text))
    UpdateTime: Optional[str] = Field(default=None,
                                      sa_column=Column('UpdateTime', Text, server_default=text('CURRENT_TIMESTAMP')))
    CreateBy: Optional[str] = Field(default=None, sa_column=Column('CreateBy', Text, server_default=text("'system'")))
    UpdateBy: Optional[str] = Field(default=None, sa_column=Column('UpdateBy', Text, server_default=text("'system'")))


class User(SQLModel, table=True):
    __table_args__ = (
        Index('USER_NAME', 'UserName', 'Password'),
    )

    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    UserName: str = Field(sa_column=Column('UserName', Text, nullable=False, server_default=text("''")))
    Password: str = Field(sa_column=Column('Password', Text, nullable=False, server_default=text("''")))
    IsActive: int = Field(sa_column=Column('IsActive', Integer, nullable=False, server_default=text('1')))
    NickName: Optional[str] = Field(default=None, sa_column=Column('NickName', Text, server_default=text("''")))
    Email: Optional[str] = Field(default=None, sa_column=Column('Email', Text, server_default=text("''")))
    LastLoginTime: Optional[str] = Field(default=None, sa_column=Column('LastLoginTime', Text))
    Avatar: Optional[str] = Field(default=None, sa_column=Column('Avatar', Text))
    CreateTime: Optional[str] = Field(default=None, sa_column=Column('CreateTime', Text))
    UpdateTime: Optional[str] = Field(default=None,
                                      sa_column=Column('UpdateTime', Text, server_default=text('CURRENT_TIMESTAMP')))
    CreateBy: Optional[str] = Field(default=None, sa_column=Column('CreateBy', Text, server_default=text("''")))
    UpdateBy: Optional[str] = Field(default=None, sa_column=Column('UpdateBy', Text, server_default=text("''")))


class UserRole(SQLModel, table=True):
    Id: Optional[int] = Field(default=None, sa_column=Column('Id', Integer, primary_key=True))
    UserId: int = Field(sa_column=Column('UserId', Integer, nullable=False))
    RoleId: int = Field(sa_column=Column('RoleId', Integer, nullable=False))
    IsActive: int = Field(sa_column=Column('IsActive', Integer, nullable=False, server_default=text('1')))
    CreateTime: Optional[str] = Field(default=None, sa_column=Column('CreateTime', Text))
    UpdateTime: Optional[str] = Field(default=None,
                                      sa_column=Column('UpdateTime', Text, server_default=text('CURRENT_TIMESTAMP')))
    CreateBy: Optional[str] = Field(default=None, sa_column=Column('CreateBy', Text, server_default=text("''")))
    UpdateBy: Optional[str] = Field(default=None, sa_column=Column('UpdateBy', Text, server_default=text("''")))


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)
