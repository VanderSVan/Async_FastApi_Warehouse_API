from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_sqlalchemy import async_session


async def get_db() -> Generator[AsyncSession, None, None]:
    async with async_session() as session:
        yield session
