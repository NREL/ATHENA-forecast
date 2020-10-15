""" Author: Monte Lunacek
    Purpose: Create a sklearn-compatible rmse scorer
"""
import numpy as np
from sklearn.metrics import make_scorer, mean_squared_error, r2_score

def rmse(y, y_pred):
    # Returns RMSE
    return np.sqrt(mean_squared_error(y_pred, y))

# Creates the scorer compatible with sklearn 
rmse_scorer = make_scorer(rmse, greater_is_better=False)