from typing import Any

from fastapi_pagination import Params
from sqlalchemy import select, and_, text

from fastapi_template.app import crud
from fastapi_template.app.core import ResponseCode
from fastapi_template.app.exception import HttpException
from fastapi_template.app.model import Role
from fastapi_template.app.schema.base_schema import IdResponse
from fastapi_template.app.schema.role_schema import RoleCreateRequest, RoleSearchRequest, RoleUpdateRequest


class RoleService:

    async def create_role(self, role_create: RoleCreateRequest, create_by=None):
        created_role = await crud.role.add(create_schema=role_create, created_by=create_by)
        resp = IdResponse(id=created_role.id)
        return resp

    async def update_role(self, update_role: RoleUpdateRequest, update_by: Any = None):
        item_id = update_role.id
        new_role = update_role.create_model(update_by=update_by)(**update_role.dict())
        updated_role = await crud.role.update_by_id(item_id=item_id, update_schema=new_role)
        if updated_role is None:
            raise HttpException(code=ResponseCode.NOT_FOUND, detail="not found role")
        resp = IdResponse(id=updated_role.id)
        return resp

    async def inactive_role(self, user_id: int, update_by=None):
        user = await crud.role.inactive(item_id=user_id, update_by=update_by)
        if user is None:
            raise HttpException(code=ResponseCode.NOT_FOUND, detail="role not exists")
        resp = IdResponse(id=user.id)
        return resp

    async def list_roles(self, role_search: RoleSearchRequest):
        name = role_search.name
        query = select(Role).where(and_(
            Role.name.contains(name) if name else text("1=1")),
            Role.is_active == 1).order_by(Role.id.desc())
        params = Params(page=role_search.page, size=role_search.size)
        results = await crud.role.list_paginated_ordered(query=query, params=params)
        return results


role = RoleService()
