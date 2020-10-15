
""" Author: Monte Lunacek
    Purpose: Enumerate and save a grid of possible arrival and departure shifts.
"""

import scipy.stats
import pandas as pd
import numpy as np

import athena 
import sys

def compute_correlation(a, astd, d, dstd, ina, inastd, ind, indstd, flights, control):
    """ Given an arrival shift mean (a) and a std (astd) and a departure shift mean (d)
        and a std (dstd), this function computes the resulting correlation in the data.

        Returns: A dictionary of the inputs and the r_squared value
    """
    flight_summary = athena.database.shift_flights_international(flights, a, astd, d, dstd, ina, inastd, ind, indstd)

    comb = pd.concat([control, flight_summary['shifted']], axis=1)
    comb.dropna(inplace=True)
    comb = comb.reset_index().rename(columns={'index': 'period'})
    comb.columns = ['period', 'vehicles', 'passengers']
    comb.set_index('period', inplace=True)

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(comb['passengers'].values, 
                                                                        comb['vehicles'].values)

    return {'amu': a, 'astd': astd, 'dmu': d, 'dstd': dstd, 
            'iamu': ina, 'iastd': inastd, 'idmu': ind, 'idstd': indstd, 
            'r_square': r_value**2}

# Get the flight and vehicle data
db = athena.database.AthenaDatabase(cache=True, write=True)
flights = db.flight_passengers()
control = db.control_plaza()
codes = db.airport_country_codes()

df = pd.merge(flights.reset_index(), codes, left_on='flight_dest_org', right_on='IATA Code')
df['DI'] = df['Country'].map(lambda x: "domestic" if x=='United States' else "international")
df.set_index('period', inplace=True)



a = 40
astd = 5
d = 100
dstd = 10

ina = 40
inastd = 5
ind = 100
indstd = 10

res = compute_correlation(a,     astd,   d,   dstd, 
                          ina, inastd, ind, indstd, df, control)

amu = np.arange(30, 50, 5)
dmu = np.arange(90, 120, 10)
iamu = np.arange(30, 70, 10)
idmu = np.arange(90, 180, 10)

results = []
# Loop over all combinations and save in results
for a in amu:
    for ina in iamu:
        for d in dmu:
            for ind in idmu:
                res = compute_correlation(a, 5,   d,   10, ina, 5, ind, 10, df, control)
                print(res)
                sys.stdout.flush()
                results.append(res)

# Save results as a csv
df = pd.DataFrame(results)
df.to_csv("correlation_int.csv", index=False)


# amu = np.arange(0, 90, 5)
# dmu = np.arange(0, 180, 10)
# arrival_std = [0, 5, 10]
# depart_std = [0, 5, 10]

# results = []
# # Loop over all combinations and save in results
# for a in amu:
#     for astd in arrival_std:
#         for d in dmu:
#             for dstd in depart_std:
#                 res = compute_correlation(a, astd, d, dstd, flights, control)
#                 print(res)
#                 results.append(res)

# # Save results as a csv
# df = pd.DataFrame(results)
# df.to_csv("correlation.csv", index=False)



    