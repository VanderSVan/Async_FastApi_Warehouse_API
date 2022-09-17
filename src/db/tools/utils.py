import sys

from psycopg2 import connect, OperationalError
from psycopg2.extensions import connection as psycopg2_conn, ISOLATION_LEVEL_AUTOCOMMIT
from dataclasses import dataclass

from src.utils.color_logging.main import logger
from src.config import get_settings

setting = get_settings()


@dataclass
class PsqlDatabaseConnection:
    """Connection through superuser"""
    dbname: str = setting.PG_SUPER_DB
    user: str = setting.PG_SUPER_USER
    password: str = setting.PG_SUPER_PASSWORD
    host: str = setting.PG_HOST
    port: str = setting.PG_PORT
    isolation_level: int = ISOLATION_LEVEL_AUTOCOMMIT

    @staticmethod
    def print_psycopg2_exception(err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()

        # get the line number when exception occured
        line_num = traceback.tb_lineno
        logger.exception(f"===psycopg2 exception in more detail==="
                         f"psycopg2 ERROR: {err} on line number: {line_num}\n"
                         f"psycopg2 traceback: {traceback} -- type:: {err_type}\n"
                         f"extensions.Diagnostics: {err.diag}\n"
                         f"obj=, {err_obj.args}\n"
                         f"pgerror: {err.pgerror}\n"
                         f"pgcode: {err.pgcode}\n"
                         f"===end psycopg2 exception===\n")

    def __enter__(self):
        try:
            self.connection = connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port)
        except OperationalError as err:
            logger.exception("Error: Unable to connect!\nInput connection data is probably wrong.\n")
            self.print_psycopg2_exception(err)

        self.connection.set_isolation_level(self.isolation_level)
        logger.info("POSTGRES CONNECTION OPEN...")
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        logger.info("POSTGRES CONNECTION CLOSE.")


def _get_pure_notices(notices: list) -> str:
    if len(notices) > 1:
        pure_notices_list = [notice.split(sep=':')[1].lstrip().rstrip() for notice in notices]
        pure_result = "\n".join(pure_notices_list)
    elif len(notices) == 0:
        pure_result = ""
    else:
        pure_result = notices[0].split(sep=':')[1].lstrip().rstrip()
    return pure_result


def print_notices(notices: list):
    pure_notices = _get_pure_notices(notices)
    if len(notices) > 0:
        logger.info(f"===SQL notices==\n"
                    f"\n{pure_notices}\n"
                    f"\n===End SQL notices===")


def print_sql_error(error: Exception):
    logger.error(f"===SQL error===\n"
                 f"\n{error}\n"
                 f"\n===End SQL error===")


def try_except_decorator(error):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except error as err:
                print_sql_error(err)
            except Exception as default_err:
                logger.exception(f"Got an exception: {default_err}"
                                 f"Type exception = {type(default_err)}")
            finally:
                if isinstance(self.connection, psycopg2_conn):
                    print_notices(self.connection.notices)

        return inner_wrapper

    return outer_wrapper
