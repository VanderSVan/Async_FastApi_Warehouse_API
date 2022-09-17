import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.tools.db_operations import (PsqlDatabaseConnection,
                                        DatabaseOperation)
from src.config import get_settings
from src.db.db_sqlalchemy import async_engine, BaseModel
from src.api.factory_app import create_app
from src.utils.db_populating.inserting_data_into_db import insert_data_to_db


setting = get_settings()

api_url = setting.API_URL
db_config = setting.TEST_DATABASE


@pytest.fixture(scope="package", autouse=True)
def create_test_db():
    with PsqlDatabaseConnection() as conn:
        database = DatabaseOperation(connection=conn,
                                     db_name=db_config['db_name'],
                                     user_name=db_config['username'],
                                     user_password=db_config['user_password'])
        database.drop_all()
        database.create_all()


@pytest.fixture(scope="session", autouse=True)
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
            app=create_app(with_logger=False),
            base_url=f"http://{api_url}"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_session() -> AsyncSession:
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
            await insert_data_to_db(async_session=conn)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await async_engine.dispose()
