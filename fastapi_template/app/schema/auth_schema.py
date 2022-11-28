from typing import Union, Optional

from pydantic import UUID4

from fastapi_template.app.schema.base_schema import BaseSchemaModel


class AuthLoginRequest(BaseSchemaModel):
    username: str
    password: str


class TokenResponse(BaseSchemaModel):
    access_token: str
    expires_in: int
    token_type: str = "bearer"


class TokenPayload(BaseSchemaModel):
    upn: Optional[Union[int, UUID4]] = None
