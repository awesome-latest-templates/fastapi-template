from typing import Optional

from fastapi_cache import FastAPICache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar
from starlette.requests import Request
from starlette.responses import Response

from fastapi_template.app.core.db import db
from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.user_entity import UserCreateRequest, UserUpdateRequest
from fastapi_template.app.model import User


def cache_key_builder(
        func,
        namespace: Optional[str] = "",
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
):
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"
    return cache_key


class UserCrud(BaseCrud[User, UserCreateRequest, UserUpdateRequest]):

    async def query_by_username(self,
                                *,
                                username: str,
                                db_session: Optional[AsyncSession] = None) -> Optional[User]:
        db_session = db_session or db.session
        select_sql: SelectOfScalar = select(User).where(User.user_name == username)
        users = await db_session.execute(select_sql)
        return users.scalar_one_or_none()


user = UserCrud(User)
