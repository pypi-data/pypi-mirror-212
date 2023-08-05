from typing import List
import pandas as pd
import gp_sqlconnection as sqlConnection
from psycopg2.errors import OperationalError, UndefinedTable
import sqlalchemy
from sqlalchemy.sql.expression import text


def dbReadQuery(query: str, database: str = "gbase", **kwargs):
    """
    wrapper for "pandas.read_sql_query" function - all arguments of this function can be sent explicitly
    :param query:
    :param database:
    :param kwargs:
    :return:
    """
    connection = sqlConnection.make_pandas_connection(database=database)
    try:
        df = pd.read_sql_query(text(query), connection, **kwargs)
        dbDisconnect(connection)
        return df
    except OperationalError:
        dbDisconnect(connection)
        raise
    except UndefinedTable:
        dbDisconnect(connection)
        raise
    except Exception as ex:
        dbDisconnect(connection)
        print(type(ex))
        raise


def dbExecuteQuery(query: str, database: str = "gbase", return_value: bool = False):
    """
     Execute a specific query the is not supposed to return anything
     Is not supposed to be used directly, but as part of functions like dbWriteTable
    :param return_value some execution has return value, with return_value=true you will get it
    """
    connection = sqlConnection.make_connection(database)
    try:
        res = sqlConnection.execute_query(connection, query, return_value)
        dbDisconnect(connection)
        return res
    except OperationalError:
        dbDisconnect(connection)
        raise
    except UndefinedTable:
        dbDisconnect(connection)
        raise
    except Exception as ex:
        dbDisconnect(connection)
        print(type(ex))
        raise


def dbListSchemas(database: str = "gbase"):
    query = "SELECT schema_name FROM information_schema.schemata " \
            "where schema_name not in ('pg_catalog', 'pg_toast', 'information_schema');"
    try:
        return dbReadQuery(query, database=database)
    except Exception as ex:
        print(str(ex))


def dbListTables(schema: str = "gpd", database: str = None):
    q = f"SELECT * FROM information_schema.tables WHERE table_schema = '{schema}';"
    try:
        return dbReadQuery(q, database)
    except Exception as ex:
        print(str(ex))


def dbReadTable(tableName: str, schema: str = "gpd", database: str = "gbase", index_col: bool = True):
    """
    Read table from database
    :param tableName:
    :param schema:
    :param database:
    :param index_col: include index column or not in the result data frame
    :return: 0 if table is not exist, else df of table
    """
    try:
        q = f"SELECT * FROM {schema}.{tableName}"
        df = dbReadQuery(q, database)
        return df if index_col else df.iloc[:, 1:]
    except Exception as ex:
        print(str(ex))
        return None


def dbExistsTable(tableName: str, schema: str = "gpd", database: str = "gbase"):
    q = f"SELECT * FROM {schema}.{tableName}"
    try:
        dbReadQuery(q, database)
    except Exception as e:
        print(str(e))
        return False
    else:
        return True


def dbCreateSchema(newSchemaName: str, database: str = None):
    """
    Creates schema
    :param newSchemaName:
    :param database:
    :return: 0 if schema is already exists, schema name if it was created
    """
    try:
        schema = newSchemaName.lower()
        q = f"CREATE SCHEMA {schema}"
        dbExecuteQuery(q, database)
        print(f"Schema '{schema}' created successfully.")
    except Exception as e:
        print("Error creating schema:", e)


def dbDeleteSchema(schema: str, database: str = "gbase") -> bool:
    """
    Deletes schema if it is empty
    :param schema:
    :param database:
    :return: 1 if schema was deleted, 0 if was not
    """
    try:
        schema = schema.lower()
        q = f"DROP SCHEMA {schema}"
        dbExecuteQuery(q, database)
        print("schema has been deleted successfully")
        return True
    except Exception as e:
        print(str(e))


def dbRemoveTable(tableName: str, schema: str, database: str) -> bool:
    """
    Remove given table.
    No default values on purpose
    :param tableName:
    :param schema:
    :param database:
    :return: 1 if table was deleted, 0 if it was not
    """
    try:
        tableName.lower()
        q = f"DROP TABLE {schema}.{tableName}"
        dbExecuteQuery(q, database)
        print("Table was deleted successfully")
        return True
    except Exception as e:
        print(str(e))
        return False


def dbWriteTable(df: pd.DataFrame,
                 tableName: str = None,
                 override: bool = False,
                 schema: str = "gpd",
                 append: bool = False,
                 database: str = "gbase",
                 **kwargs
                 ):
    """
    Wrapper to "pandas.to_sql" function - all arguments of this function can be sent explicitly
    :param df:
    :param tableName:
    :param override:
    :param schema:
    :param append:
    :param database:
    :return:
    """
    engine = sqlConnection.create_engine_for_pd(database)
    if append:
        if_exists = 'append'
    elif override:
        if_exists = 'replace'
    else:
        if_exists = 'fail'
    try:
        df.to_sql(tableName, engine, schema=schema,
                  if_exists=if_exists, **kwargs)
        print("Table was written successfully")
    except ValueError as e:
        print(f"{e}: Table {tableName} was not written to {schema}.{database}")
        return False
    except sqlalchemy.exc.ProgrammingError as e:
        print(f"{e}: df to be appended has more columns than table")
        return False

    return True


def dbAppendTablePartialColumns(df: pd.DataFrame,
                                tableName: str,
                                schema: str,
                                database: str,
                                append: bool = True,
                                row_names: List[str] = None,
                                row_names_label: str = None,
                                **kwargs):
    """
    Wrapper to "pandas.to_sql" function - all arguments of this function can be sent explicitly
    :param df:
    :param tableName:
    :param schema:
    :param database:
    :param append:
    :param row_names:
    :param row_names: equal to "index" argument in "pandas.to_sql" function
    :param row_names_label: equal to "index_label" argument in "pandas.to_sql" function
    :return:
    """
    return dbWriteTable(df,
                        tableName,
                        schema=schema,
                        append=append,
                        database=database,
                        index=row_names,
                        index_label=row_names_label,
                        **kwargs)


def dbDisconnect(connection: sqlalchemy.engine.Connection):
    connection.close()
