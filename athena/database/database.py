""" Author: Monte Lunacek
    Purpose: Provide database access to select queries
"""

import json
import os
import psycopg2
import pandas as pd
import logging

from sqlalchemy import create_engine, event

from . import queries

logger = logging.getLogger(__name__)

class AthenaDatabase(object):
    """
    Class to access Athena AWS RDS. Attributes return specific queries.

    Attributes:    
        bus_ridership_passengers
        control_plaza
        flight_passengers
        weather_table
        summary_table

        engine: create_engine for the connection

    Examples
    >>> db = athena.database.AthenaDatabase(cache=True, write=True)
    >>> df = db.summary_table()     
    """

    def __init__(self, write=False, cache=False):
        """
        Args:
            write : bool, attempt to use read and write access
            cache : bool, use the cache or force a database pull
        """
        
        # Read the correct credentials file
        cred_file = os.path.join( os.environ['ATHENA_CREDENTIALS_PATH'], "athena_internal.json")
        if write:
            cred_file = os.path.join( os.environ['ATHENA_CREDENTIALS_PATH'], "athena_internal.json")
    
        # Load credentials
        try: 
            self._credentials = json.loads(open(cred_file).read())
        except FileNotFoundError:

            if not cache:
                logger.error('You need the following credentials \
                            file {} to access the database'.format(cred_file))

        # Try to connect
        try:
            self._connection = psycopg2.connect(user=self._credentials['user'],
                                                password=self._credentials['password'],
                                                host=self._credentials['host'],
                                                port=self._credentials['port'],
                                                database=self._credentials['database'],
                                                connect_timeout=3)
        except psycopg2.OperationalError:
            if not cache:
                logger.warn("You are not connected to the database, using cache data.")
            self._connection = None

        self._cache = cache

    def __del__(self):
        # Disconnect from the database
        if self._connection is not None:
            self._connection.close()              

    def _index_time_zone(self, df):
        # Change the period to datetime and set as index
        df['period'] = pd.to_datetime(df['period'], utc=True)
        df.set_index('period', inplace=True)

    def _query_and_cache(self, filename, qry):
        # if cache is true, try to read from local directory
        if self._cache:
            # read local
            try:
                df = pd.read_csv(os.path.join(os.environ['ATHENA_DATA_PATH'], filename))
            except FileNotFoundError:
                # Attempt to read from database
                df = pd.read_sql_query(qry, self._connection)
                self.save_as(df, filename)
            self._index_time_zone(df)
            return df
        else:
            # query database and save
            df = pd.read_sql_query(qry, self._connection)
            df.rename(columns={'weather_time': 'period'}, inplace=True)
            self.save_as(df, filename)
            self._index_time_zone(df)
            return df

    def save_as(self, df, filename):
        # Save the dataframe to cache directory as filename
        filename = os.path.join(os.environ['ATHENA_DATA_PATH'], filename)
        df.to_csv(filename, index=False)

    def bus_ridership_passengers(self):
        return self._query_and_cache("bus_ridership_passengers.csv", queries.bus_ridership)

    def control_plaza(self):
        return self._query_and_cache("control_plaza.csv", queries.control_plaza)

    def flight_passengers(self):
        return self._query_and_cache("flight_passengers.csv", queries.flights)

    def dfw_weather(self):
        return self._query_and_cache("dfw_weather.csv", queries.dfw_weather)


    def weather_table(self):
        return self._query_and_cache("weather_table.csv", queries.weather_table)

    def summary_table(self):
        return self._query_and_cache("summary_table.csv", queries.summary_table)

    def dfw_plaza_entryexit(self):
        return self._query_and_cache("dfw_plaza_entryexit.csv", queries.dfw_plaza_entryexit)

    def airport_country_codes(self):
        return pd.read_csv(os.path.join(os.environ['ATHENA_DATA_PATH'], "codes.csv"))

    @property
    def engine(self): 
        # Return engine from connection string
        engine_str = "postgresql://"
        engine_str += self._credentials['user'] + ":"
        engine_str += self._credentials['password'] + "@"
        engine_str += self._credentials['host'] + ":"
        engine_str += self._credentials['port'] + "/"
        engine_str += self._credentials['database']
        db_engine = create_engine(engine_str)
        return db_engine

