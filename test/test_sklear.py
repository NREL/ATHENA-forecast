import os
import pytest
import athena
import pandas as pd
import glob

import shutil

from sklearn.svm import SVR

from sklearn.linear_model import LinearRegression
from athena.utils.sklearn import DataTransformSKLearn

try:
    import xgboost as xgb
except:
    pass

os.environ['ATHENA_DATA_PATH'] = os.path.join( os.path.dirname(os.path.abspath(__file__)), "data")

def evaluate_model(model, config):
    if os.path.exists("results"):
        shutil.rmtree("results")

    dataset = athena.Dataset("dfw_demand.csv.gz", 
                    index="timestamp", 
                    freq="30min",
                    max_days=500,
                    max_training_days=200,
                    predition_length=1,
                    test_start_values=["2019-07-27 13:00:00"],
                    test_sequence_length=4
                    )

    transform = DataTransformSKLearn(['vehicles'], 
                                     ['vehicles_1', 'vehicles_2', 'vehicles_3'], 
                                     ['hour'])

    athena.utils.sklearn.evaluate_sklearn(dataset, transform, model, config)

    df = pd.read_csv(glob.glob("{}/*.csv".format(config['directory']))[0])
    
    assert len(df) ==  4 #test_sequence_length*len(test_start_values) 

def test_sklearn_linear():
    model = LinearRegression()
    config = {}
    config['directory'] = 'results/linear'
    evaluate_model(model, config)
    
def test_sklearn_xgboost():
    model = xgb.XGBRegressor()
    config = {}
    config['directory'] = 'results/xgboost'
    evaluate_model(model, config)

def test_sklearn_SVR():
    model = SVR()
    config = {}
    config['directory'] = 'results/svr'
    evaluate_model(model, config)


