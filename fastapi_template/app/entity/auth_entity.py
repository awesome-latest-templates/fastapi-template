from typing import Union, Optional

from pydantic import BaseModel, UUID4


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    id: Optional[Union[int, UUID4]] = None
    roles: list = []
