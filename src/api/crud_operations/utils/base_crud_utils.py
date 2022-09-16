from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DBAPIError

from src.utils.exceptions.base import CRUDException


@dataclass
class QueryExecutor:

    @staticmethod
    async def get_single_result(query, session: AsyncSession):
        query_result = await session.execute(query)
        return query_result.scalar()

    @staticmethod
    async def get_multiple_result(query, session: AsyncSession):
        query_result = await session.execute(query)
        return query_result.scalars().all()

    @classmethod
    async def delete_obj(cls, query, session: AsyncSession) -> bool:
        return await cls._execute_query(query, session)

    @classmethod
    async def patch_obj(cls, query, session: AsyncSession, model_name: str) -> bool:
        return await cls._execute_query(query, session, model_name)

    @classmethod
    async def add_obj(cls, query, session: AsyncSession, model_name: str) -> bool:
        return await cls._execute_query(query, session, model_name)

    @classmethod
    async def _execute_query(cls, query, session: AsyncSession, model_name: str = None) -> bool:
        """Executes query for delete, patch and post operations."""
        try:
            await session.execute(query)
            await session.commit()
            return True

        except IntegrityError:
            await session.rollback()
            if model_name:
                CRUDException.raise_duplicate_err(model_name)
            else:
                CRUDException.raise_error_500()

        except DBAPIError:
            await session.rollback()
            CRUDException.raise_error_500()
