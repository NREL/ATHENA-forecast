""" Author: Yanbo Ge, Lindy Williams, and Monte Lunacek
    Purpose: Example using the athena database and learning module on a prophet model.
"""
import athena
from fbprophet import Prophet
import numpy as np

# Pull summary table
db = athena.database.AthenaDatabase(cache=True, write=True)
df = db.summary_table()     

# Add time features and rename columns
athena.learning.add_features(df)
df["X"] = df.index.to_series()
df = df[["X","vehicles", "passengers","wind","precip","snow","temp"]]
df = df.rename(columns={"X": "ds", "vehicles": "y"})

# Assign columns
y_cols = ['y']
num_cols = ['ds','passengers','wind','precip','snow','temp']
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
X['y'] = y

# Start RMSE list 
results = []

# Results and cross-validation
cv = splitter.fold(n_splits=10).split(X, y, group)
for train_index, test_index in cv:
    m = Prophet()
    m.fit(X.iloc[train_index])
    forecasted = m.predict(X.iloc[test_index])

    yhat = forecasted['yhat']
    rmse = athena.learning.rmse(yhat, X.iloc[test_index]['y'])
    results.append(rmse)

print(np.mean(results), np.std(results))