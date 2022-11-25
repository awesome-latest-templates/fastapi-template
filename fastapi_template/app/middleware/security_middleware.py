import typing
from typing import Optional

from starlette.authentication import AuthenticationBackend, BaseUser, AuthenticationError, AuthCredentials
from starlette.requests import HTTPConnection

from fastapi_template.app.api.deps import get_token_data
from fastapi_template.config import settings


class JWTUser(BaseUser):
    def __init__(self, user_id: int, token: str) -> None:
        self.user_id = user_id
        self.token = token

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return str(self.user_id)


class JWTAuthenticationBackend(AuthenticationBackend):

    def __init__(self,
                 secret_key: str = settings.JWT_SECRET_KEY,
                 algorithm: str = settings.JWT_ALGORITHM,
                 scheme_name: str = settings.JWT_TOKEN_SCHEME_NAME,
                 issuer: str = settings.JWT_ISSUER,
                 audience: Optional[str] = settings.JWT_AUDIENCE,
                 options: Optional[dict] = None) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.scheme_name = scheme_name
        self.issuer = issuer
        self.audience = audience
        self.options = options or dict()

    @classmethod
    def get_token_from_header(cls, authorization: str, scheme_name: str) -> str:
        """Parses the Authorization header and returns only the token"""
        try:
            scheme, _, token = authorization.partition(" ")
            if not token:
                scheme, token = token, scheme
        except ValueError:
            raise AuthenticationError('Could not separate Authorization scheme and token')
        if scheme.lower() != scheme_name.lower():
            raise AuthenticationError(f'Authorization scheme {scheme} is not supported')
        return token

    async def authenticate(self, conn: HTTPConnection) -> typing.Optional[typing.Tuple["AuthCredentials", "BaseUser"]]:
        if settings.JWT_TOKEN_HEADER_NAME not in conn.headers:
            return None

        auth_value = conn.headers[settings.JWT_TOKEN_HEADER_NAME]
        token = self.get_token_from_header(authorization=auth_value, scheme_name=self.scheme_name)
        user_detail = await get_token_data(token)
        roles = user_detail.role + ["authenticated"]
        return AuthCredentials(roles), JWTUser(user_id=user_detail.id, token=token)
