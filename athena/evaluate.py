""" Author: Monte Lunacek
    Purpose: Provide a single function that evaluates a configuration.
"""

import pandas as pd
import athena
import copy
import sys
import json

from gluonts.mx.trainer import Trainer


from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

from athena.utils.sklearn import DataTransformSKLearn
from athena.utils.arima import DataTransformARIMA, evaluate_ARIMA

try:
    import xgboost as xgb
except:
    pass

def evaluate(config):
    """ Main evaluate decision function """
    task = copy.deepcopy(config)
    if task['algorithm'] == "linear":
        evaluate_linear(task)
    if task['algorithm'] == "svr":
        evaluate_svr(task)
    if task['algorithm'] == "xgboost":
        evaluate_xgboost(task)
    if task['algorithm'] == "deepar":
        evaluate_deepar(task)
    if task['algorithm'] == "nn":
        evaluate_nn(task)
    if task['algorithm'] == "arima":
        evaluate_arima(task)
    if task['algorithm'] == "sarimax":
        evaluate_sarimax(task)


def get_dataset(config):
    dataset = athena.Dataset(config['filename'], 
                    index=config['index'], 
                    freq=config['freq'],
                    max_days=config['max_days'],
                    max_training_days=config['max_training_days'],
                    predition_length=config['prediction_length'],
                    test_start_values=config['test_start_values'],
                    test_sequence_length=config['test_sequence_length']
                    )
    return dataset

def evaluate_sklearn(config, model):
    """ General method for evaluating SKlearn models """
    dataset = get_dataset(config)

    transform = DataTransformSKLearn(config['target'], 
                                     config['dynamic_real'], 
                                     config['dynamic_cat'])

    athena.utils.sklearn.evaluate_sklearn(dataset, transform, model, config)

def evaluate_linear(config):
    model = LinearRegression(**config['params'])
    evaluate_sklearn(config, model)
    
def evaluate_svr(config):
    model = SVR(**config['params'])
    evaluate_sklearn(config, model)

def evaluate_xgboost(config):
    model = xgb.XGBRegressor(**config['params'])
    evaluate_sklearn(config, model)



def evaluate_gluon(config, model):
    """ General method for evaluating Gluonts DeepAR-like  models """
    dataset = get_dataset(config)
    
    transform = athena.utils.gluonts.DataTransformGluon(config['target'], 
                                                        config['dynamic_real'], 
                                                        config['dynamic_cat'])

    athena.utils.gluonts.evaluate_gluonts(dataset, transform, model, config)


def evaluate_deepar(config):
    """ Pass DeepAR to evaluate_gluon"""
    from gluonts.model.deepar import DeepAREstimator

    model = DeepAREstimator(freq=config['freq'], 
                                use_feat_dynamic_real=config['params'].get('use_feat_dynamic_real', False),
                                prediction_length=config['prediction_length'], 
                                trainer=Trainer(epochs=config['params'].get('epochs', 10),
                                                learning_rate=config['params'].get('learning_rate', 1e-3),
                                                num_batches_per_epoch=config['params'].get('num_batches_per_epoch', 100),
                                                ))
                                                
    evaluate_gluon(config, model)

def evaluate_nn(config):
    """ Pass a simple neural network to evaluate_gluon"""
    from gluonts.model.simple_feedforward import SimpleFeedForwardEstimator
    model = SimpleFeedForwardEstimator(freq=config['freq'], 
                                prediction_length=config['prediction_length'], 
                                trainer=Trainer(epochs=config['params'].get('epochs', 10)))

    evaluate_gluon(config, model)
  

def evaluate_arima(config):
    config['directory'] = 'results/arima'
    dataset = get_dataset(config)
    transform = DataTransformARIMA(config['target'], 
                                   config['dynamic_real'], 
                                   config['dynamic_cat'])
    
    evaluate_ARIMA(dataset, transform, config)

def evaluate_sarimax(config):
    config['directory'] = 'results/sarimax'
    dataset = get_dataset(config)
    transform = DataTransformARIMA(config['target'], 
                                   config['dynamic_real'], 
                                   config['dynamic_cat'])
    
    evaluate_ARIMA(dataset, transform, config)

