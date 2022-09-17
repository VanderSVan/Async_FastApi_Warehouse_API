# !!! Inserting data into an empty database only !!!
from typing import NoReturn

from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_sqlalchemy import BaseModel
from src.api.models.user import UserModel
from src.api.models.product import ProductModel
from src.utils.db_populating.data_preparation import prepare_data_for_insertion
from src.utils.color_logging.main import logger
from src.utils.db_populating.input_data import (users_json,
                                                products_json,
                                                warehouse_groups_json,
                                                warehouses_json,
                                                prices_json)


async def insert_data_to_db(async_session: AsyncSession) -> NoReturn:
    """Inserts prepared data into an empty database only!"""
    user_count: int = await _get_count(UserModel, async_session)
    product_count: int = await _get_count(ProductModel, async_session)
    total_count = sum([user_count, product_count])

    if total_count == 0:
        prepared_data: dict = prepare_data_for_insertion(users_json,
                                                         products_json,
                                                         warehouse_groups_json,
                                                         warehouses_json,
                                                         prices_json
                                                         )
        await _insert_full_data_to_db(prepared_data, async_session)
        logger.success("Data has been added to db")

    else:
        logger.info("Data cannot be inserted into the database because the database is not empty")


async def _get_count(model: BaseModel,
                     async_session: AsyncSession
                     ) -> NoReturn:
    query = select(func.count(model.id))
    query_result = await async_session.execute(query)
    return query_result.scalar()


async def _insert_full_data_to_db(data: dict,
                                  async_session: AsyncSession
                                  ) -> NoReturn:
    for model, data_list in data.items():
        await _insert_data_to_db(data_list, model, async_session)
    await async_session.commit()


async def _insert_data_to_db(data: list,
                             model: BaseModel,
                             async_session: AsyncSession
                             ) -> NoReturn:
    insert_query = insert(model).values(data)
    await async_session.execute(insert_query)
