from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_template.app.core.db import db
from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.base_entity import IdResponse
from fastapi_template.app.entity.user_role_entity import UserRoleCreateRequest, UserRoleUpdateRequest
from fastapi_template.app.model import UserRole


class UserRoleCrud(BaseCrud[UserRole, UserRoleCreateRequest, UserRoleUpdateRequest]):

    async def query_by_user_id(self,
                               *,
                               user_id: int,
                               db_session: Optional[AsyncSession] = None):
        db_session = db_session or db.session
        select_sql = select(UserRole).where(UserRole.user_id == user_id)
        users = await db_session.execute(select_sql)
        return users.scalars().all()

    async def add_user_role(self,
                            user_id: int,
                            roles: list,
                            created_by: int = None,
                            db_session: Optional[AsyncSession] = None):
        user_role_data = []
        for role in roles:
            user_role_data.append({
                "user_id": user_id,
                "role_id": role
            })

        created_data = await self.add_all(create_entities=user_role_data,
                                          created_by=created_by,
                                          db_session=db_session)
        resp = list(map(lambda a: IdResponse(id=a.id), created_data))
        return resp


user_role = UserRoleCrud(UserRole)
