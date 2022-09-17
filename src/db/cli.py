import argparse

from src.config import get_settings
from src.db.tools.db_operations import DatabaseOperation
from src.db.tools.utils import PsqlDatabaseConnection

settings = get_settings()


def create_arguments():
    parser = argparse.ArgumentParser(
        prog="Creation or deletion db",
        description="By default info is taken from env variables.",
        epilog="Try '--create_db'"
    )
    parser.add_argument('-d', '--db_name', type=str, metavar="", default=None,
                        help='assign db name')
    parser.add_argument('-u', '--user_name', type=str, metavar="", default=None,
                        help='assign user name')
    parser.add_argument('-p', '--user_password', type=str, metavar="", default=None,
                        help='assign user password')
    parser.add_argument('-r', '--role_name', type=str, metavar="", default=None,
                        help='assign role name')
    parser.add_argument('--create_db', action='store_true', help='create db with params')
    parser.add_argument('--drop_db', action='store_true', help='delete db with all params')
    return parser.parse_args()


def main():
    args = create_arguments()

    with PsqlDatabaseConnection() as conn:
        parameters = dict(
            connection=conn,
            db_name=args.db_name if args.db_name else settings.PG_USER_DB or "your_really_test_db",
            user_name=args.user_name if args.user_name else settings.PG_USER or "your_really_test_user",
            user_password=(args.user_password if args.user_password
                           else settings.PG_USER_PASSWORD or "your_really_test_password"),
            role_name=args.role_name if args.role_name else settings.PG_ROLE
        )
        # init database
        database = DatabaseOperation(**parameters)

        if args.create_db:
            database.create_all()
        elif args.drop_db:
            database.drop_all()
        else:
            raise ValueError("arguments '--create_db' and '--drop_db' "
                             "cannot be empty at the same time.")
