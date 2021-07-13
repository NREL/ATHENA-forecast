
""" Author: Monte Lunacek
    Purpose: function(s) for adding features.
"""
import numpy as np
import pandas as pd
from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay
import holidays

def add_time_features(df):
    """
    Adds features for learning to df

    Args:
        df: dataframe with timeseries index

    Returns:
        DataFrame
    """
    df['year'] = df.index.map(lambda x: x.year)
    df['month'] = df.index.map(lambda x: x.month)
    df['week'] = df.index.map(lambda x: x.week)
    df['weekday'] = df.index.map(lambda x: x.weekday()+1)
    df['day'] = df.index.map(lambda x: x.day)
    df['weekend'] = df['day'].map(lambda x: x>5)
    df['hour'] = df.index.map(lambda x: x.hour)
    df['time'] = df.index.map(lambda x: x.time)
    df['minute'] = df.index.map(lambda x: x.minute)

    def encode(data, col, max_val):
        data[col + '_sin'] = np.sin(2 * np.pi * data[col]/max_val)
        data[col + '_cos'] = np.cos(2 * np.pi * data[col]/max_val)
        return data

    # create cyclical columns for time values
    df['time_minutes'] = df['time'].map(lambda x: x.hour*60 + x.minute)

    encode(df, 'month', 12)
    encode(df, 'day', 7)
    encode(df, 'week', 52)
    encode(df, 'hour', df['hour'].max())
    encode(df, 'time_minutes', df['time_minutes'].max())

    us_holidays = holidays.UnitedStates()
    df['holiday'] = df.index.map(lambda x: x in us_holidays).values

    df.dropna(inplace=True, axis=1)
    return df