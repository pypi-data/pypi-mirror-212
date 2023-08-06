import pathlib
import configparser
import os
from pdb import set_trace as bp
import logging
from typing import Dict, Literal, List
from functools import lru_cache


import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text as sql_text

_cache_mode_options = Literal[0,1,2]

def parse_db_access(config_path: str, section_name:str)->Dict:
    """parse the configuration file to acquire required information for connecting MsSql DB

    Args:
        config_path (str): path of configuration file
        section_name (str): section name for db access in config file

    Returns:
        Dict: access information
    """
    logger = logging.getLogger(__name__)
    try:
        config = configparser.ConfigParser()
        _ = config.read(config_path)

        db_access = config._sections[section_name]
        # db_access = {}
        # db_access["server_username"] = config.get(section_name, 'username')
        # db_access["server_password"] = config.get(section_name, 'password')
        # db_access["server"] = config.get(section_name, 'server')
        if "db_type" not in db_access.keys(): raise ValueError("can't find key 'db_type'")
        return db_access

    except Exception as e:
        print(f"function parse_db_access got exception message: {e}")
        logger.info(
            "unable to parse from configuration file:/n {config_path} for database access information"
        )


class DBConnector:
    default_port = {
            "ORACLE":1521,
            "MSSQL":1433,
            "AZURE-BLOB":None
        }

    def __init__(self, db_access, **kwargs):
        """connecting object for a database

        Args:
            db_access (dict): return of parse_db_access()
        """

        self.logger = logging.getLogger(__name__)
        self.cache_mode = 0
        self.cache_dir = "."

        self._db_access = db_access

        self.queries_dir = None             
        self.__not_yet_purge = True

        self._db_type, self._port = self._check_nondefault_port()

    def set_cache_dir(self, cache_dir: str, cache_mode: _cache_mode_options = 1)->None:
        """set up path for directory where cached files are stored

        Args:
            cache_mode (int, optional): 0: always pull data from db
                                1: only pull data if cache doesn't exist
                                2: refresh cache before using 
                                Defaults to 0.
            cache_dir (str): directory for keeping/searching cache files; only works if cache_mode in {1,2}
        """

        self.cache_dir = cache_dir
        self.cache_mode = cache_mode
        

    def _check_nondefault_port(self)-> List:
        db_type = self._db_access["db_type"].upper()
        
        if "port" in self._db_access.keys():
            port = self._db_access["port"]
        else:
            port = self.default_port[db_type]

        return [db_type, port]
        
    def set_queries_dir(self,queires_dir: str, **kwargs)->None:
        """set up path for directory where predefined sql statement files are stored

        Args:
            queires_dir (str): path of directory
        **kwargs:
            all variables within predefiend sql queries can pass to DBConnector via keyword arguments
        """
        self.queries_dir = queires_dir
        self.query_args = dict(kwargs)

    def del_cache(self)->None:             
        dir = self.cache_dir
        for f in os.listdir(dir):
            if f.endswith(".pkl"):
                os.remove(os.path.join(dir, f))

    def _check_cache_dir(self)->None:
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _correct_datetime_format_for_mssql(self):
        for k,v in self.query_args.items():
            if type(v)==np.datetime64: 
                self.query_args[k] = str(v.astype('M8[D]'))

    
    def _get_mssql_conn_str(self,):
        conn_str=''.join(
            [
            'DRIVER={ODBC Driver 17 for SQL Server};',
            f'SERVER={self._db_access["server"]},{self._port};',
            f'DATABASE={self._db_access["database_name"]};UID={self._db_access["server_username"]};PWD={self._db_access["server_password"]}'
            ]
        )
        conn_str = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})
        return conn_str

    
    def _get_oracle_conn_str(self):
        conn_str = f'oracle+cx_oracle://{self._db_access["server_username"]}:{self._db_access["server_password"]}@{self._db_access["server"]}:{self._port}/?service_name={self._db_access["service_name"]}'

        return conn_str

    @property
    def _conn_str(self):

        conn_str = {
            "MSSQL": self._get_mssql_conn_str,
            "ORACLE": self._get_oracle_conn_str,
        }

        return conn_str[self._db_type]()

    def pull_SQL(
            self,
            query,
    ):
        """
        Args:
            query (str): sql statement

        Return:
            df (DataFrame): results of executing SQL statement if it has return
        """
        conn_str = self._conn_str

        eng = create_engine(conn_str)
        with eng.connect() as conn:
            df = pd.read_sql(
                sql_text(query),
                conn,
            )
        return df

    def pull_predefined_query(
        self,
        query_name,
        capitalize_column_name:bool=False,
        **kwargs
    ):
        """pull data by predefined sql statement file including variables.

        Args:
            query_name (str): name of a predefined sql statement file; no extension needed
            capitalize_column_name (bool): convert all column name to uppercase or not

        Raises:
            Exception: queries_dir can't be empty, set by method set_queries_dir() first
            ValueError: if <query_name>.sql can't be found in queries_dir

        Returns:
            DataFrame: result of executing SQL statement
        """
        if self.queries_dir is None:
            raise Exception("Use method set_queries_dir(queries_dir:str) to enable method pull_predefined_query")

        
        executor = {
            0: self._run_cache_mode_0,
            1: self._run_cache_mode_1,
            2: self._run_cache_mode_2,
        }

        if f"{query_name}.sql" in os.listdir(self.queries_dir):
            df = executor[self.cache_mode](query_name)
        else:
            raise ValueError('Query for {} is undefined'.format(query_name))
        
        if capitalize_column_name:
            df.columns = df.columns.str.upper()
        
        return df

    def _run_cache_mode_0(self,query_name):
        query_file = os.path.join(self.queries_dir, f"{query_name}.sql")
        with open(query_file, 'r') as fname:
            query = fname.read()
            query = query.format(
            **self.query_args
            )
        try:
            df = self.pull_SQL(query)
        except Exception as e:
            print(f"predefined query {query_name} got exception message: {e}")
            self.logger.info(f"predefined query {query_name} got exception message: {e}")
        return df

    def _run_cache_mode_1(self,query_name):
        pickle_path = os.path.join(self.cache_dir, f"{query_name}.pkl")
        if f"{query_name}.pkl" in os.listdir(self.cache_dir):  
            df = pd.read_pickle(pickle_path)
        else:
            df = self._run_cache_mode_0(query_name)
            df.to_pickle(pickle_path)
        return df

    def _run_cache_mode_2(self,query_name):
        if self.__not_yet_purge: 
            self._del_cache()
            self.__not_yet_purge = False

        df = self._run_cache_mode_1(query_name)
        return df

if __name__ == "__main__":
    pass 