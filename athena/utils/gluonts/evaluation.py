""" Author: Monte Lunacek
    Purpose: Provide an evaluation of GluonTS models given a dataset and transformation.
"""

import os
import shutil
import json
import pandas as pd
import numpy as np
import time

from gluonts.evaluation import Evaluator
from gluonts.evaluation.backtest import make_evaluation_predictions

from .. results import ensure_directory, save_results, get_uuid, save_partial

from functools import partial
import multiprocessing as mp

def evaluate_gluonts(dataset, transform, model, config):
    """ Main method for evaluating the CV for DeepAR like Gluonts algorithms"""
    ensure_directory(config.get('directory'))
    config['uuid'] = get_uuid() 
    if os.environ.get('ATHENA_DEBUG', False)=='true':
        config['uuid'] = 'evaluate_gluonts_debug'

    gen = transform(dataset, prediction_window=model.prediction_length)
    trials = [ (test_set, ds) for test_set, ds in enumerate(gen)]

    result_ids = []
    results = []
    for trial in trials:
        results.append(inner_loop_function(model, trial))

    dfs = [ x[0] for x in results]
    test_mse = [x[1] for x in results]
    df = pd.concat(dfs)
    save_results(config, df, test_mse)  

def inner_loop_function(model, config):
    """ Execute single cross-validation trial """
    test_set, ds = config
    tic = time.time()
    df = execute_gluonts_dataframe(model, ds, test_set )
    res = execute_gluonts_json(df)
    toc = time.time()
    res['time'] = toc-tic
    return df, res

def execute_gluonts_dataframe(model, trial, test_set):
    """ Extract dataframe from the predictor """
    predictor = model.train(training_data=trial['train'])
    forecast_it, ts_it = make_evaluation_predictions(trial['test'], 
                                                     predictor=predictor, 
                                                     num_samples=10)
    for forecast, ts in zip(forecast_it, ts_it):
        df = pd.DataFrame(ts).rename(columns={0:'actual'})
        tmp = pd.concat([df, pd.DataFrame({'predicted': forecast.mean,
                                           'q25': forecast.quantile(0.25),
                                           'q75': forecast.quantile(0.75),
                                           'q95': forecast.quantile(0.95),
                                           'q05': forecast.quantile(0.05),
                                      }, index=forecast.index)], axis=1)
        tmp.dropna(inplace=True)
        
    tmp['test_set'] = test_set    
    return tmp

def execute_gluonts_json(df):
    """ Extract the json information from the dataframe"""
    mse = np.mean((df['predicted'] - df['actual'])*(df['predicted'] - df['actual']))
    res = {'rmse': float(np.sqrt(mse)), 'test_set': 1 }
    return res




