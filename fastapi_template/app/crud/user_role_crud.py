from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar

from fastapi_template.app.core.db import db
from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.entity.user_role_entity import UserRoleCreateRequest, UserRoleUpdateRequest
from fastapi_template.app.model import UserRole


class UserRoleCrud(BaseCrud[UserRole, UserRoleCreateRequest, UserRoleUpdateRequest]):

    async def query_by_user_id(self,
                               *,
                               user_id: int,
                               db_session: Optional[AsyncSession] = None) -> Optional[List[UserRole]]:
        db_session = db_session or db.session
        select_sql: SelectOfScalar = select(UserRole).where(UserRole.user_id == user_id)
        users = await db_session.execute(select_sql)
        return users.scalars().all()


user_role = UserRoleCrud(UserRole)
