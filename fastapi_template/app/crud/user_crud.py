from typing import Optional

from fastapi_cache import FastAPICache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from fastapi_template.app.core.db import db
from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.common_entity import PageDataModel
from fastapi_template.app.entity.user_entity import UserCreateRequest, UserUpdateRequest, UserDetail
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
        select_sql = select(User).where(User.user_name == username)
        users = await db_session.execute(select_sql)
        return users.scalar_one_or_none()

    async def get_user_list(self,
                            name: str,
                            page: int = 0,
                            page_size: int = 50,
                            db_session: Optional[AsyncSession] = None) -> PageDataModel:
        users = await self.execute(sql=f"SELECT * FROM User WHERE user_name like :name or nick_name like :name",
                                   params={"name": f"%{name}%", "page": page, "size": page_size},
                                   entity=UserDetail,
                                   db_session=db_session
                                   )
        return users


user = UserCrud(User)
