
""" Author: Monte Lunacek
    Purpose: Enumerate and save a grid of possible arrival and departure shifts.
"""

import scipy.stats
import pandas as pd
import numpy as np

import athena 

def compute_correlation(a, astd, d, dstd, flights, control):
    """ Given an arrival shift mean (a) and a std (astd) and a departure shift mean (d)
        and a std (dstd), this function computes the resulting correlation in the data.

        Returns: A dictionary of the inputs and the r_squared value
    """
    flight_summary = athena.database.shift_flights(flights, a, astd, d, dstd)

    comb = pd.concat([control, flight_summary['shifted']], axis=1)
    comb.dropna(inplace=True)
    comb = comb.reset_index().rename(columns={'index': 'period'})
    comb.columns = ['period', 'vehicles', 'passengers']
    comb.set_index('period', inplace=True)

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(comb['passengers'].values, 
                                                                        comb['vehicles'].values)

    return {'amu': a, 'astd': astd, 'dmu': d, 'dstd': dstd, 'r_square': r_value**2}


# Get the flight and vehicle data
db = athena.database.AthenDatabase(cache=True, write=True)
flights = db.flight_passengers()
control = db.control_plaza()

amu = np.arange(0, 90, 5)
dmu = np.arange(0, 180, 10)
arrival_std = [0, 5, 10]
depart_std = [0, 5, 10]

results = []
# Loop over all combinations and save in results
for a in amu:
    for astd in arrival_std:
        for d in dmu:
            for dstd in depart_std:
                res = compute_correlation(a, astd, d, dstd, flights, control)
                print(res)
                results.append(res)

# Save results as a csv
df = pd.DataFrame(results)
df.to_csv("correlation.csv", index=False)

    