from enum import Enum
from typing import Union

import sqlite3
import oracledb
import pandas as pd
import pymssql

import bsc_utils.config as config
from bsc_utils.helpers import dict_factory
from bsc_utils.exceptions import NotDatabaseError


class Database(Enum):
    MSSQL = 'mssql'
    ORACLE = 'oracle'
    SQLITE = 'sqlite'


def connect(database: Database):
    if not isinstance(database, Database):
        raise NotDatabaseError('Must be a database.Database instance.')

    if database == Database.MSSQL:
        return pymssql.connect(
            server=config.mssql_server,
            user=config.mssql_user,
            password=config.mssql_password,
            database=config.mssql_database,
        )
    elif database == Database.ORACLE:
        return oracledb.connect(
            user=config.oracle_user,
            password=config.oracle_password,
            dsn=config.oracle_dsn
        )
    elif database == Database.SQLITE:
        return sqlite3.connect(database=config.sqlite_path)


def query(
    database: Database,
    query: str,
    params: Union[list, tuple] = None,
    fetch: bool = True,
    as_df: bool = True,
    index_col: str = None
) -> Union[list, pd.DataFrame]:
    con = connect(database)
    if database == Database.MSSQL:
        cur = con.cursor(as_dict=True)

    if database == Database.SQLITE:
        con.row_factory = dict_factory
        cur = con.cursor()

    if database == Database.ORACLE:
        cur = con.cursor()

    cur.execute(query) if params is None else (
        cur.executemany(query, params)
        if isinstance(params, list) else cur.execute(query, params)
    )

    if database == Database.ORACLE:
        cols = [col[0] for col in cur.description]
        cur.rowfactory = lambda *args: dict(zip(cols, args))

    obj = None
    if fetch:
        obj = cur.fetchall()
        if as_df:
            obj = make_tabular(obj, index_col)
            
    con.commit()
    con.close()

    return obj


def make_tabular(obj: list[dict], index_col: str) -> pd.DataFrame:
    df = pd.DataFrame(obj)
    if index_col:
        df.set_index(index_col, inplace=True)

    return df