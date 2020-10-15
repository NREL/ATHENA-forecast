""" Author: Lindy Williams
    Purpose: Example using the athena database and learning module on a Seasonal ARIMAX model.
"""
import athena
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Pull summary table
db = athena.database.AthenaDatabase(cache=True, write=True)
df = db.summary_table()     

# Add time features
athena.learning.add_features(df)

# Assign columns
y_cols = ['vehicles']
num_cols = ['passengers','wind','precip','snow','temp']
cat_cols = []
no_trans_cols = []

# Assign forecast window and how we split.
group_name = "obs_group" # 'obs_group' or 'day_group', 'week_group'
split_on = "time" # 'time' or 'group'

# Create splitter to provide hold out set and CV
splitter = athena.learning.Splitter(df, split_on, group_name, y_cols, 
                                    num_cols + cat_cols + no_trans_cols)

# Split data
X, y, group = splitter.train_Xygroup
X_hold, y_hold, group_hold = splitter.test_Xygroup

# Set steps for forecasting
if group_name == "obs_group":
    the_steps = 1
elif group_name == "week_group":
    the_steps = 48
else:
    the_steps = 336

# Set the SARIMAX parameters
the_order = (1, 0, 0)
the_seasonal_order = (0, 1, 1, 48)

# Results and cross-validation
results = []
cv = splitter.fold(n_splits=10).split(X, y, group)
for train_index, test_index in cv:
    history = y.iloc[train_index]
    model = SARIMAX(history, exog=X.iloc[train_index], order=the_order, seasonal_order=the_seasonal_order)
    model_fit = model.fit(disp=0)
    yhat = model_fit.forecast(steps = the_steps, exog=X.iloc[test_index])
    yhat = yhat[:the_steps]
    true_value = y.iloc[test_index].values[:the_steps]

    rmse = athena.learning.rmse(yhat, true_value)
    results.append(rmse)
  

print(np.mean(results), np.std(results))