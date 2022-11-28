from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_template.app.core.db import db
from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.model import User
from fastapi_template.app.schema.base_schema import BasePageResponseModel
from fastapi_template.app.schema.user_schema import UserCreateRequest, UserUpdateRequest, UserDetailResponse


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
                            db_session: Optional[AsyncSession] = None) -> BasePageResponseModel:
        query = f"SELECT * FROM User WHERE (user_name like :name or nick_name like :name) and is_active=1"
        users = await self.execute(sql=query,
                                   params={"name": f"%{name}%", "page": page, "size": page_size},
                                   schema=UserDetailResponse,
                                   db_session=db_session
                                   )
        return users


user = UserCrud(User)
