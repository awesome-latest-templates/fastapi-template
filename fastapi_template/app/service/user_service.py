from typing import Optional, Dict

from fastapi_cache.decorator import cache
from fastapi_pagination import Page

from fastapi_template.app import crud
from fastapi_template.app.entity.user_entity import UserDetail, UserSearchRequest
from fastapi_template.app.model import User


class UserService:

    @cache()
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
        user_detail = UserDetail.from_orm(user_data)
        user_detail.role = role_names
        return user_detail.dict()

    async def get_users(self, user_request: UserSearchRequest) -> Page[UserDetail]:
        entities = await crud.user.get_user_list(name=user_request.name,
                                                 page=user_request.page,
                                                 page_size=user_request.size)
        return entities


user = UserService()
