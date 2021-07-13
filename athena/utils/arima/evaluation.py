""" Author: Monte Lunacek
    Purpose: Provide an evaluation of the ARIMA family of models given a dataset and transformation.
"""

import pandas as pd
import numpy as np
import shutil
import os
import json
import time

#from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima.model import ARIMA

from statsmodels.tsa.api import SARIMAX

from ... scorer import mse
from .. results import ensure_directory, save_results, get_uuid, save_partial

import itertools
import multiprocessing as mp


def evaluate_ARIMA(dataset, transform, config={}):
    """ This will evaluate the entire cross-valiidation set defined by the dataset object
         for ARIMA.
    """
    ensure_directory(config.get('directory'))
    if config.get('uuid') is None:
        config['uuid'] = get_uuid()

    train_mse = []
    test_mse = []
    dfs = []
    cvs = transform(dataset)

    results = []
    for i, cv in enumerate(cvs):
        results.append(evaluate_ARMIMA_inner(dataset.prediction_length, config, cv, i))

    test_mse = [ x[0] for x in results]
    dfs = [x[1] for x in results]

    df = pd.concat(dfs)
    save_results(config, df, test_mse)

def evaluate_ARMIMA_inner(prediction_length, config, params, test_number):
    """ This is the inner function for evaluating a single train/test set of ARIMA.
    """
    tic = time.time()
    train_start, X_train, y_train, test_start, X_test, y_test = params
    
    y_train.index.freq = config['freq']
    X_train.index.freq = config['freq']
    y_test.index.freq = config['freq']
    X_test.index.freq = config['freq']

    order = config['params'].get('arima_order', (0,0,0))
    seasonal_order = config['params'].get('seasonal_order', (0,0,0,0))

    if len(X_train) == 0:
        model = ARIMA(endog=y_train, 
                      order=order,
                      seasonal_order=seasonal_order, 
                      exog=X_train,
                      freq=config['freq'])

        model_fit = model.fit()       
        yhat = model_fit.forecast(steps = prediction_length,
                                                     exog=X_test)
    else:
        mod = ARIMA(endog=y_train, 
                    order=order,
                    seasonal_order=seasonal_order, 
                    freq=config['freq'])

        model_fit = mod.fit()
        yhat = model_fit.forecast(steps = prediction_length)   

    toc = time.time()

    y_test = y_test.tail(len(yhat)).copy()
    y_test.columns = ['actual']    
    y_test['predicted'] = yhat
    
    res = {'rmse': np.sqrt(mse(y_test['actual'], y_test['predicted'])), 
            'train_rmse': np.sqrt(np.mean(model_fit.resid*model_fit.resid)),
            'time': toc-tic}
  
    return res, y_test



   
