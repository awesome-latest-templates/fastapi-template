from contextvars import ContextVar
from typing import Optional, Union, Dict

from sqlalchemy.engine import URL, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

_Session: Optional[sessionmaker] = None
_session: ContextVar[Optional[AsyncSession]] = ContextVar("_session", default=None)


class MissingSessionError(Exception):
    """Excetion raised for when the user tries to access a database session before it is created."""

    def __init__(self):
        msg = """
        No session found! Either you are not currently in a request context,
        or you need to manually create a session context by using a `db` instance as
        a context manager e.g.:

        async with db():
            await db.session.execute(foo.select()).fetchall()
        """

        super().__init__(msg)


class SessionNotInitialisedError(Exception):
    """Exception raised when the user creates a new DB session without first initialising it."""

    def __init__(self):
        msg = """
        Session not initialised! Ensure that DBSessionMiddleware has been initialised before
        attempting database access.
        """

        super().__init__(msg)


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            db_url: Optional[Union[str, URL]] = None,
            custom_engine: Optional[Engine] = None,
            engine_args: Dict = None,
            session_args: Dict = None,
            commit_on_exit: bool = False,
    ):
        super().__init__(app)
        self.commit_on_exit = commit_on_exit
        engine_args = engine_args or {}
        session_args = session_args or {}

        if not custom_engine and not db_url:
            raise ValueError("You need to pass a db_url or a custom_engine parameter.")
        if not custom_engine:
            engine = create_async_engine(db_url, **engine_args)
        else:
            engine = custom_engine

        global _Session
        _Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, **session_args)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        async with db(commit_on_exit=self.commit_on_exit):
            return await call_next(request)


class DBSessionMeta(type):
    # using this metaclass means that we can access db.session as a property at a class level,
    # rather than db().session
    @property
    def session(self) -> AsyncSession:
        """Return an instance of Session local to the current async context."""
        if _Session is None:
            raise SessionNotInitialisedError

        session = _session.get()
        if session is None:
            raise MissingSessionError

        return session


class DBSession(metaclass=DBSessionMeta):
    def __init__(self, session_args: Dict = None, commit_on_exit: bool = False):
        self.token = None
        self.session_args = session_args or {}
        self.commit_on_exit = commit_on_exit

    async def _init_session(self):
        self.token = _session.set(_Session(**self.session_args))  # type: ignore

    async def __aenter__(self):
        if not isinstance(_Session, sessionmaker):
            raise SessionNotInitialisedError

        await self._init_session()
        return type(self)

    async def __aexit__(self, exc_type, exc_value, traceback):
        session = _session.get()
        if exc_type is not None:
            await session.rollback()

        if self.commit_on_exit:
            await session.commit()

        await session.close()
        _session.reset(self.token)


db: DBSessionMeta = DBSession
