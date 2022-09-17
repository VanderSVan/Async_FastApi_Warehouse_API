# Wrappers for sql operations

from psycopg2.sql import SQL


class DatabaseSQLOperation:
    @staticmethod
    def check_db_existence(db_name: str):
        return SQL(f"SELECT COUNT(*) = 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")

    @staticmethod
    def create_db(db_name: str):
        return SQL(f"CREATE DATABASE {db_name}")

    @staticmethod
    def drop_db(db_name: str):
        return SQL(f"DROP DATABASE {db_name}")


class UserSQLOperation:
    @staticmethod
    def check_user_existence(username: str):
        return SQL(f"SELECT COUNT(*)=1 FROM pg_roles WHERE rolname = '{username}'")

    @staticmethod
    def create_new_user(username: str, password: str):
        return SQL(f"CREATE USER {username} WITH PASSWORD '{password}'")

    @staticmethod
    def drop_user(username: str):
        return SQL(f"DROP USER IF EXISTS {username}")

    @staticmethod
    def check_membership(username: str):
        return SQL(f"""
                        SELECT COUNT(rolname) = 1
                        FROM pg_authid
                        WHERE EXISTS (SELECT member FROM pg_auth_members
                                      WHERE member = pg_authid.oid AND rolname = '{username}')
                    """)


class RoleSQLOperation:
    @staticmethod
    def check_role_existence(role_name: str):
        return SQL(f"SELECT COUNT(*)=1 FROM pg_roles WHERE rolname = '{role_name}'")

    @staticmethod
    def create_new_role(role_name: str):
        return SQL(f"CREATE ROLE {role_name}")

    @staticmethod
    def drop_role(role_name: str):
        return SQL(f"DROP ROLE IF EXISTS {role_name}")

    @staticmethod
    def join_user_to_role(role_name: str, username: str):
        return SQL(f"GRANT {role_name} TO {username}")

    @staticmethod
    def remove_user_from_role(role_name: str, username: str):
        return SQL(f"REVOKE {role_name} FROM {username}")


class PrivilegeSQLOperation:
    @staticmethod
    def grant_all_privileges(db_name: str, role_name: str):
        return SQL(f"""
                        GRANT ALL ON DATABASE {db_name} TO {role_name};
                        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {role_name};
                    """)

    @staticmethod
    def remove_all_privileges(db_name: str, role_name: str):
        return SQL(f"""
                        REVOKE ALL ON DATABASE {db_name} FROM {role_name};
                        REVOKE ALL ON SCHEMA public FROM {role_name};
                    """)
