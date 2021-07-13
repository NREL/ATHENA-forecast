import pytest
import athena
import pandas as pd
import glob

import shutil
import os

from athena.utils.arima import DataTransformARIMA, evaluate_ARIMA

os.environ['ATHENA_DATA_PATH'] = os.path.join( os.path.dirname(os.path.abspath(__file__)), "data")

def test_arima():

    if os.path.exists("results"):
        shutil.rmtree("results")

    config = {
        'directory': 'results/arima',
        'freq': "30min",
        'params': {'arima_order': (1,0,0)}
    }

    dataset = athena.Dataset("dfw_demand.csv.gz", 
                    index="timestamp", 
                    freq="30min",
                    max_days=500,
                    max_training_days=200,
                    predition_length=12,
                    test_start_values=["2019-07-27 13:00:00"],
                    test_sequence_length=4
                    )

    transform = DataTransformARIMA(['vehicles'])
    
    evaluate_ARIMA(dataset, transform, config)

