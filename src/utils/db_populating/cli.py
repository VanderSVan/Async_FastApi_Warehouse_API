import argparse

from src.utils.db_populating.inserting_data_into_db import insert_data_to_db
from src.utils.db_populating.input_data import users_json
from src.db.db_sqlalchemy import engine, async_session


def create_arguments():
    parser = argparse.ArgumentParser(
        prog="Populate the database with prepared data",
        description="Populate the database with prepared data. "
                    "Prepared data are located: 'src.api.utils.db_populating. "
                    "Populate data into an empty database only",
        epilog="Try '--populate_db'"
    )
    parser.add_argument('--populate_db', type=str, metavar="", default=None,
                        help='Populate the empty database with prepared data.')
    return parser.parse_args()


async def main():
    async with engine.begin() as conn:
        await insert_data_to_db(
            users_json=users_json,
            session=conn
        )
