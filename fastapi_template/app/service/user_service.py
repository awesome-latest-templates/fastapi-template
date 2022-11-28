import copy
from typing import Optional, Dict, Any

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi_pagination import Page
from sqlalchemy import select, and_
from starlette.requests import Request
from starlette.responses import Response

from fastapi_template.app import crud
from fastapi_template.app.core import ResponseCode
from fastapi_template.app.core.auth.security import create_hash_password
from fastapi_template.app.exception import HttpException
from fastapi_template.app.model import User, Role
from fastapi_template.app.schema.base_schema import IdResponse
from fastapi_template.app.schema.user_schema import UserDetailResponse, UserSearchRequest, UserCreateRequest, \
    UserUpdateRequest, UserRoleRequest
from fastapi_template.config import constants


def cache_key_builder(
        func,
        namespace: Optional[str] = "",
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
):
    prefix = FastAPICache.get_prefix()
    user_id = kwargs['kwargs'].get("user_id") if kwargs['kwargs'].get("user_id", None) else (
        f"{func.__module__}:{func.__name__}:{args}:{kwargs}")
    cache_key = f"{namespace}:{prefix}:{user_id}"
    return cache_key


class UserService:

    async def create_user(self, create_user: UserCreateRequest, create_by: Any = None):
        new_user = copy.deepcopy(create_user)
        query = select(User).where(and_(User.user_name == create_user.user_name, User.is_active == 1))
        data = await crud.user.get(query=query)
        if data:
            raise HttpException(code=ResponseCode.DATA_DUPLICATED, detail="user already exists")
        new_user.password = create_hash_password(create_user.password)
        created_user = await crud.user.add(create_schema=new_user, created_by=create_by)
        resp = IdResponse(id=created_user.id)
        return resp

    async def update_user(self, update_user: UserUpdateRequest, update_by: Any = None):
        item_id = update_user.id
        new_user = UserUpdateRequest.create_model(update_by=update_by)(**update_user.dict())
        updated_user = await crud.user.update_by_id(item_id=item_id, update_schema=new_user)
        if updated_user is None:
            raise HttpException(code=ResponseCode.NOT_FOUND, detail="not found user")
        resp = IdResponse(id=updated_user.id)
        return resp

    async def inactive_user(self, user_id: int, update_by: None):
        user = await crud.user.inactive(item_id=user_id, update_by=update_by)
        if user is None:
            raise HttpException(code=ResponseCode.NOT_FOUND, detail="user not exists")
        resp = IdResponse(id=user.id)
        return resp

    @cache(key_builder=cache_key_builder, namespace=constants.CACHE_USER_NAMESPACE)
    async def get_user_detail(self, user_id: int, user_data: User = None) -> Optional[Dict]:
        # get user roles
        if user_data is None:
            user_data = await crud.user.get_by_id(item_id=user_id)
        if not user_data:
            return None
        if not user_data.is_active:
            return None
        user_role_data = await crud.user_role.query_by_user_id(user_id=user_id)
        if not user_role_data:
            role_names = []
        else:
            role_ids = list(map(lambda d: d.role_id, user_role_data))
            role_datas = await crud.role.get_by_ids(list_ids=role_ids)
            role_names = list(map(lambda d: d.name, role_datas))
        user_detail = UserDetailResponse.from_orm(user_data)
        user_detail.role = role_names
        return user_detail.dict()

    async def get_users(self, user_request: UserSearchRequest) -> Page[UserDetailResponse]:
        schemas = await crud.user.get_user_list(name=user_request.name,
                                                page=user_request.page,
                                                page_size=user_request.size)
        return schemas

    async def assign_role(self, user_role: UserRoleRequest, create_by: int = None):
        user_id = user_role.user_id
        roles = user_role.roles
        user_data = await crud.user.get_by_id(item_id=user_id)
        if user_data is None:
            raise HttpException(code=ResponseCode.NOT_FOUND, detail="user not exists")
        query = select(Role).where(Role.name.in_(roles))
        role_data = await crud.role.list(query=query)
        role_ids = list(map(lambda a: a.id, role_data))
        if role_ids is None:
            raise HttpException(code=ResponseCode.NOT_FOUND, detail="roles not exist")
        if len(role_ids) != len(roles):
            raise HttpException(code=ResponseCode.BAD_REQUEST, detail="invalid role data")
        created_data = await crud.user_role.add_user_role(user_id=user_id, roles=role_ids, created_by=create_by)
        resp = list(map(lambda a: IdResponse(id=a.id), created_data))
        # TODO explicit refresh the user role cache
        backend: InMemoryBackend = FastAPICache.get_backend()
        cache_key = f"{FastAPICache.get_prefix()}:{user_id}"
        count = await backend.clear(namespace=constants.CACHE_USER_NAMESPACE, key=cache_key)
        return resp


user = UserService()
