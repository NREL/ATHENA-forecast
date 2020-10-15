""" Author: Monte Lunacek
    Purpose: Example using the athena database and learning module on a linear regression model.
"""
from sklearn.linear_model import LinearRegression
import numpy as np
import athena

# Pull summary table
db = athena.database.AthenaDatabase(cache=True, write=True)
df = db.summary_table()     

# Add time features
athena.learning.add_features(df)

# Assign columns
y_cols = ['vehicles']
num_cols = ['passengers', 'p1', 'p2', 'p3', 'v1', 'v2', 'v3', 'temp', 'snow']
cat_cols = ['time', 'hour', 'day', 'week', 'month', 'year']
no_trans_cols = []

# Assign forecast window and how we split.
group_name = "obs_group" # 'obs_group' or 'day_group', 'week_group'
split_on = "group" # 'time' or 'group'

# Linear model
m = LinearRegression()

# Create processor for scaling and transforming data
processor = athena.learning.Processor(num_cols, cat_cols, no_trans_cols)
processor.fit(df)

# Create splitter to provide hold out set and CV
splitter = athena.learning.Splitter(df, split_on, group_name, y_cols, 
                                    num_cols + cat_cols + no_trans_cols)

# Split data
X, y, group = splitter.train_Xygroup
X_hold, y_hold, group_hold = splitter.test_Xygroup

# Transform split data
Xt = processor.transform(X)
Xt_hold = processor.transform(X_hold)


# results and cross-validation
results = []
cv = splitter.fold(n_splits=10).split(Xt, y, group)
for train_index, test_index in cv:
    m.fit(Xt[train_index], y.iloc[train_index])

    rmse = athena.learning.rmse_scorer(m, Xt[test_index], y.iloc[test_index])
    results.append(rmse)
    print(train_index.shape, test_index.shape, rmse)

print(np.mean(results), np.std(results))
