from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_template.app.core.db import db
from fastapi_template.app.crud.base_crud import BaseCrud
from fastapi_template.app.model import UserRole
from fastapi_template.app.schema.user_role_schema import UserRoleCreateRequest, UserRoleUpdateRequest


class UserRoleCrud(BaseCrud[UserRole, UserRoleCreateRequest, UserRoleUpdateRequest]):

    async def query_by_user_id(self,
                               *,
                               user_id: int,
                               db_session: Optional[AsyncSession] = None):
        db_session = db_session or db.session
        select_sql = select(UserRole).where(and_(UserRole.user_id == user_id, UserRole.is_active == 1))
        users = await db_session.execute(select_sql)
        return users.scalars().all()

    async def add_user_role(self,
                            user_id: int,
                            roles: list,
                            created_by: int = None,
                            db_session: Optional[AsyncSession] = None):
        db_session = db_session or db.session
        user_role_data = []
        for role in roles:
            create_user_role_data = {}
            # query the user_role data firstly
            query = select(UserRole).where(UserRole.user_id == user_id)
            user_role = await self.list(query=query)
            if user_role:
                item_ids = list(map(lambda item: item.id, user_role))
                await self.delete_all(item_ids=item_ids)
            create_user_role_data['user_id'] = user_id
            create_user_role_data['role_id'] = role
            user_role_data.append(create_user_role_data)

        created_data = await self.add_all(create_schemas=user_role_data, created_by=created_by, db_session=db_session)
        return created_data


user_role = UserRoleCrud(UserRole)
