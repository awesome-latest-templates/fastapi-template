from enum import Enum
from typing import TypeVar

from pydantic import BaseModel, conint

T = TypeVar("T")


class OrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class PageParamModel(BaseModel):
    page: int = 1
    size: int = 50


class PageDataModel(BaseModel):
    total: int = 0
    items: list = []
    page: conint(ge=1)  # type: ignore
    size: conint(ge=1)  # type: ignore
