from peewee import *
import config

def get_db():
    if config.db == "mysql":
        return MySQLDatabase(
            database=config.db_name,
            user=config.db_user,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port
        )

    if config.db == "postgresql":
        return PostgresqlDatabase(
            database=config.db_name,
            user=config.db_user,
            password=config.db_password,
            host=config.db_host
        )