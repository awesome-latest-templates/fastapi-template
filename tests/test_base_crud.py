import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from fastapi_template.app import crud
from fastapi_template.app.entity.user_entity import UserDetailResponse
from fastapi_template.config import settings

pytestmark = pytest.mark.asyncio


async def test_execute_sql():
    engine_args = {
        "echo": False,
        "pool_pre_ping": True,
    }
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, **engine_args)
    global _Session
    session_args = {}
    _Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)(**session_args)
    sql = "SELECT * FROM User WHERE user_name like :name"
    result = await crud.user.execute(sql=sql, entity=UserDetailResponse,
                                     params={"page":1, "size": 10,"name": "%admin%"},
                                     db_session=_Session)
    print(result)
