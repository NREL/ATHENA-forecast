""" Author: Monte Lunacek
    Purpose: This file holds helper utility functions.
"""

import numpy as np
import pandas as pd
from datetime import timedelta
from operator import add, sub

def shift_flights(df, arrival_mu, arrival_std, departure_mu, departure_std):
    """ Given a dataframe of flight information, this function shifts the arrivals
    by arrival_mu+/-arrival_std and departures by departure_mu +/- departure_std 
    and then resamples the dataframe at the 30 minute rate.  It returns a dataframe 
    with 3 columns:
        shifted: the shifted values for the number of seats
        flights: the number of flights
        num_seats: the number of seats

    Args:
        df: Athena summary DataFrame
        arrival_mu: The arrival mean
        arrival_std: The arrival standard deviation
        departure_mu: The departure mean
        departure_std: The departure standard deviation
        
    Returns:
        Modified DataFrame

    """

    df['count'] = 1
    
    arrivals = df[df.flight_operation=='A'].copy()
    departures = df[df.flight_operation=='D'].copy()

    arrivals['rand'] = np.random.normal(arrival_mu, arrival_std, len(arrivals))
    arrivals['min'] = arrivals['rand'].map(lambda x: timedelta(minutes=x))
    arrivals['time'] = arrivals.index + arrivals['min']

    departures['rand'] = np.random.normal(departure_mu, departure_std, len(departures))
    departures['min'] = departures['rand'].map(lambda x: timedelta(minutes=x))
    departures['time'] = departures.index - departures['min']

    a_ser = arrivals.set_index('time').resample("30min")['num_seats'].sum()
    d_ser = departures.set_index('time').resample("30min")['num_seats'].sum()

    total_shift = pd.concat([a_ser, d_ser], axis=1).sum(axis=1)

    tmp = df.resample("30min")[['count', 'num_seats']].sum()

    total = pd.concat([total_shift, tmp], axis=1)
    total.columns = ['shifted', 'flights', 'seats']
    return total


def shift_flight(df, mu, std, operator=add):
    df['rand'] = np.random.normal(mu, std, len(df))
    df['min'] = df['rand'].map(lambda x: timedelta(minutes=x))
    df['time'] = operator(df.index, df['min'])
    return df.set_index('time').resample("30min")['num_seats'].sum()

def shift_flights_international(df, arrival_mu, arrival_std, departure_mu, departure_std,
                                 int_arrival_mu, int_arrival_std, int_departure_mu, int_departure_std):
    df['count'] = 1
    
    arrivals_domestic = df.query("flight_operation=='A' and DI=='domestic'").copy()
    a_ser = shift_flight(arrivals_domestic, arrival_mu, arrival_std, add)
    
    departures_domestic = df.query("flight_operation=='D' and DI=='domestic'").copy()
    d_ser = shift_flight(departures_domestic, departure_mu, departure_std, sub)

    arrivals_int = df.query("flight_operation=='A' and DI=='international'").copy()
    int_a_ser = shift_flight(arrivals_int, int_arrival_mu, int_arrival_std, add)

    departures_int = df.query("flight_operation=='D' and DI=='international'").copy()
    int_d_ser = shift_flight(departures_int, int_departure_mu, int_departure_std, sub)

    res = pd.concat([a_ser, d_ser, int_a_ser, int_d_ser], axis=1)
    
    res.columns = ['arival_domestic', 'departure_domestic', 'arrival_international', 'departure_international']
    res.fillna(0, inplace=True)
    row_sum = res.sum(axis=1)
    tmp = res.divide(row_sum, axis=0)
    tmp['shifted'] = row_sum
    
    df_sample = df.resample("30min")[['count', 'num_seats']].sum()
    total = pd.concat([tmp, df_sample], axis=1)
    total.columns = ['arival_domestic', 'departure_domestic', 'arrival_international', 'departure_international', 'shifted', 'flights', 'seats']
    return total



