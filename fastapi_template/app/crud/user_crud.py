from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar

from fastapi_template.app.core.db import db
from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.user_entity import UserCreateRequest, UserUpdateRequest
from fastapi_template.app.model import User


class UserCrud(BaseCrud[User, UserCreateRequest, UserUpdateRequest]):

    async def query_by_username(self,
                                *,
                                username: str,
                                db_session: Optional[AsyncSession] = None):
        db_session = db_session or db.session
        select_sql: SelectOfScalar = select(User).where(User.user_name == username)
        users = await db_session.execute(select_sql)
        return users.scalar_one_or_none()


user = UserCrud(User)
