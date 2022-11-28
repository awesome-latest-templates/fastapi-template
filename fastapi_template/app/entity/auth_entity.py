from typing import Union, Optional

from pydantic import UUID4

from fastapi_template.app.entity.base_entity import BaseEntityModel


class AuthLoginRequest(BaseEntityModel):
    username: str
    password: str


class TokenResponse(BaseEntityModel):
    access_token: str
    expires_in: int
    token_type: str = "bearer"


class TokenPayload(BaseEntityModel):
    upn: Optional[Union[int, UUID4]] = None
