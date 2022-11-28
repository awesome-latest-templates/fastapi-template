import uuid
from enum import Enum
from typing import TypeVar

from pydantic import BaseModel, conint, create_model

T = TypeVar("T")


class OrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class BasePageParamModel(BaseModel):
    page: int = 1
    size: int = 50


class BasePageResponseModel(BaseModel):
    total: int = 0
    items: list = []
    page: conint(ge=1)  # type: ignore
    size: conint(ge=1)  # type: ignore


class BaseEntityModel(BaseModel):

    @classmethod
    def create_model(cls, **field_definitions):
        """
        :refer:
        https://pydantic-docs.helpmanual.io/usage/models/#dynamic-model-creation
        https://github.com/pydantic/pydantic/issues/1937
        :example:  new_user = UserUpdateRequest.create_model(update_by=update_by)(**update_user.dict())
        :param field_definitions:
        :return:
        """
        model_name = f"{cls.__name__}{str(uuid.uuid4().hex)}"
        return create_model(model_name, __base__=cls, **field_definitions)

    class Config:
        # for using method: .from_orm(modelCls)
        orm_mode = True


class IdRequest(BaseEntityModel):
    id: int


class IdResponse(BaseEntityModel):
    id: int
