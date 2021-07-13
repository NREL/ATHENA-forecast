""" Author: Monte Lunacek
    Purpose: Provide an evaluation of of SKLearn models given a dataset and transformation.
"""

import pandas as pd
import numpy as np
import shutil
import os
import json
import time
import multiprocessing as mp

from ... scorer import mse
from .. results import ensure_directory, save_results, get_uuid, save_partial

def inner_sklearn(transform, model, params, test_number):
    """ This is the inner function for evaluating a single train/test set.
    """
    train_start, X_train, y_train, test_start, X_test, y_test = params

    tic = time.time()
    model.fit(X_train, y_train.ravel())
    y_pred = model.predict(X_test)
    y_train_pred = model.predict(X_train)

    y_test_pred = transform._scaler_target.inverse_transform(y_pred.reshape(-1,1))
    y_test_actual = transform._scaler_target.inverse_transform(y_test.reshape(-1,1))
    

    y_train_pred = transform._scaler_target.inverse_transform(y_train_pred.reshape(-1,1))
    y_train_actual = transform._scaler_target.inverse_transform(y_train.reshape(-1,1))

    toc = time.time()

    res_mse = {'rmse': np.sqrt(mse(y_test_pred, y_test_actual)), 
            'train_rmse': np.sqrt(mse(y_train_pred, y_train_actual)),
            'time': toc-tic}

    train_index = pd.date_range(train_start, periods=len(y_train_pred), freq="30min" )
    test_index = pd.date_range(test_start, periods=len(y_test_pred), freq="30min" )

    df = pd.DataFrame({'predicted': y_test_pred.flatten(),
                            'actual': y_test_actual.flatten(),
                            'kind': 'test'}, 
                            index=pd.date_range(test_start, periods=len(y_test_pred), freq="30min" ))

    return df, res_mse


def evaluate_sklearn(dataset, transform, model, config={}):
    """ This will evaluate the entire cross-valiidation set defined by the dataset object.
        In this instance, we parallelize the execution across multiple CPUs using multiprocessing.
    """

    ensure_directory(config.get('directory'))
    if config.get('uuid') is None:
        config['uuid'] = get_uuid()

    mse = []
    dfs = []

    results = []
    cvs = transform(dataset)
    for test_number, cv in enumerate(cvs):
        results.append(inner_sklearn(transform, model, cv, test_number))

    dfs = [ x[0] for x in results]
    test_mse = [x[1] for x in results]

    df = pd.concat(dfs).sort_index()
    save_results(config, df, test_mse)

       
    