
""" Author: Monte Lunacek
    Purpose: functions related to adding features.
"""
import numpy as np

def add_features(df, passenger_history=5, traffic_history=5, forecast=0):
    """
    Adds features for learning to df

    Args:
        df: dataframe with timeseries index
        passenger_history: int, number of shifts of "passengers" col
        traffic_history: int, number of shifts of "vehicles" col

    Returns:
        None
    """
    df['year'] = df.index.map(lambda x: x.year)
    df['month'] = df.index.map(lambda x: x.month)
    df['week'] = df.index.map(lambda x: x.week)
    df['day'] = df.index.map(lambda x: x.weekday()+1)
    df['hour'] = df.index.map(lambda x: x.hour)
    df['time'] = df.index.map(lambda x: x.time)

    for i in range(1, passenger_history):
        df["p{}".format(i)] = df['passengers'].shift(i)

    for i in range(1, traffic_history):
        df["v{}".format(i)] = df['vehicles'].shift(i)
    
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

    # add 24 steps forward
    y_cols = []
    for r in range(forecast):
        name = "y{0:02d}".format(r)
        y_cols.append(name)
        df[name] = df['vehicles'].shift(-1*(r+1))
        
    df['day_group'] = df.index.map(lambda x: x.strftime("%Y-%m-%d"))
    df['obs_group'] = df.index.map(lambda x: x.strftime("%Y-%m-%d-%H-%M"))
    df['week_group'] = df.index.map(lambda x: x.strftime("%Y-%W"))


    df.dropna(inplace=True)
    return y_cols
