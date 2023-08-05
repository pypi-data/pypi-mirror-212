import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine
import os

CONNECTION_SUCCESS_MESSAGE = "Connection to PostgreSQL DB successful"
EXECUTION_SUCCESS = "Query executed successfully"


def _get_env():
    return "aws_rds" if os.getenv("environment.type") == "AWS" else "local"


def _get_parameters(env: str, database: str):
    return "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
        os.getenv(f"db.user.{env}"),
        os.getenv(f"db.password.{env}"),
        os.getenv(f"db.host.{env}"),
        database)


def make_connection(database: str = "gbase"):
    env = _get_env()
    try:
        connection = psycopg2.connect(
            database=database,
            host=os.getenv(f"db.host.{env}"),
            port=int(os.getenv(f"db.port.{env}")),
            user=os.getenv(f"db.user.{env}"),
            password=os.getenv(f"db.password.{env}")
        )
        print(CONNECTION_SUCCESS_MESSAGE)
        return connection
    except OperationalError:
        raise


def make_pandas_connection(database: str = 'gbase'):
    env = _get_env()
    try:
        engine_connect_params = _get_parameters(env, database)
        engine = create_engine(engine_connect_params)
        con = engine.connect()
        print(CONNECTION_SUCCESS_MESSAGE)
        return con
    except OperationalError:
        raise


def execute_query(connection, query: str, return_value: bool = False):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print(EXECUTION_SUCCESS)
        if return_value:
            res = cursor.fetchone()
            cursor.close()
            return res
        cursor.close()
    except OperationalError:
        raise
    return None


def create_engine_for_pd(database: str = "gbase"):
    env = _get_env()
    try:
        engine_connect_params = _get_parameters(env, database)
        return create_engine(engine_connect_params)
    except OperationalError:
        raise
