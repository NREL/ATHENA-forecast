""" Author: Monte Lunacek
    Purpose: Create a summary table for learning curb congestion and save it to the database
"""
import athena

import pandas as pd

if __name__ == "__main__":

    # Get flight and vehicle data
    db = athena.database.AthenDatabase(cache=True, write=True)
    flights = db.flight_passengers()
    control = db.control_plaza()

    # shift the arrivals and departures (see /bin/correlation/results.ipynb)
    flight_summary = athena.database.shift_flights(flights, 40, 10, 100, 10)

    # combine the two data sets
    comb = pd.concat([control, flight_summary['shifted']], axis=1)
    comb.dropna(inplace=True)
    comb = comb.reset_index().rename(columns={'index': 'period'})
    comb.columns = ['period', 'vehicles', 'passengers']
    comb.set_index('period', inplace=True)

    weather = db.weather_table()

    weather = weather[['mean_wind', 'mean_temp', 'mean_hum', 'mean_vis', 'mean_pres', 
                    'precip', 'thunderstorm', 'fog', 'snow', 'hail', 'rain']].copy()
    weather.columns = ['wind', 'temp', 'humidity', 'visibility', 'pressure', 
                    'precip', 'thunderstorm', 'fog', 'snow', 'hail', 'rain']

    # Upsample and fill
    weather = weather.resample("30min").mean().fillna(method='ffill')
    comb.index = comb.index.map(lambda x: x.tz_convert('US/Central').replace(tzinfo=None))

    # Join weather
    merged = comb.join(weather)

    # save the table
    merged.reset_index().to_sql("summary_table", db.engine, if_exists='replace', index=False, method='multi')
    db.save_as(merged.reset_index(), "summary_table.csv")

    print(merged.shape)
    df = db.summary_table()
    print(df.shape)