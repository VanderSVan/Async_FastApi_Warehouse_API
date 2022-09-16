# !!! Inserting data into an empty database only !!!

from sqlalchemy import select, insert, func

from src.api.models.user import UserModel
from src.utils.db_populating.data_preparation import prepare_data_for_insertion
from src.utils.color_logging.main import logger


async def insert_data_to_db(users_json: list, session) -> None:
    """Inserts prepared data into an empty database only!"""
    query = select(func.count(UserModel.id))
    query_result = await session.execute(query)
    user_count = query_result.scalar()
    if user_count == 0:
        prepared_data: dict = prepare_data_for_insertion(users_json)
        insert_query = insert(UserModel).values(prepared_data['users'])
        await session.execute(insert_query)
        await session.commit()

        logger.success("Data has been added to db")

    else:
        logger.info("Data cannot be inserted into the database because the database is not empty")
