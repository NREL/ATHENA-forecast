""" Author: Monte Lunacek
    Purpose: Helper command line script for running parameter searches on Eagle
"""
import numpy as np
import random
import pickle
import os
import argparse
import copy

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor

import athena

def translate_features(features):
    tmp = [char for char in features] 
    num_cols = []
    cat_cols = []
    no_trans_cols = []
    if "C" in tmp:
        num_cols.append('passengers')
    if "W" in tmp:
        num_cols.extend(['temp', 'snow'])
    if "P" in tmp:
        cat_cols.extend(['time', 'hour', 'day', 'week', 'month'])
    if "F" in tmp:
        num_cols.extend(['p1', 'p2', 'p3'])
    if "T" in tmp:
        num_cols.extend(['v1', 'v2', 'v3'])

    return num_cols, cat_cols, no_trans_cols

def evaluate_and_save(model, cv, parameters, directory, filename, Xt, y, Xt_hold, y_hold, results):
    reg = GridSearchCV(model, parameters, cv=cv, scoring=athena.learning.rmse_scorer, 
                    return_train_score=True, n_jobs=-1)

    reg.fit(Xt, y)

    hold_res = athena.learning.rmse_scorer(reg, Xt_hold, y_hold)

    model_name = str(model).split("(")[0]
    res = copy.deepcopy(results)
    res['model'] = model_name,
    res['hold_result'] = hold_res
    res['cv_results'] = reg.cv_results_
    res['best_estimator'] =  reg.best_estimator_

    model_filename = "{}:{}".format(model_name, filename)
    with open(os.path.join(directory, model_filename), 'wb') as ofile:
        pickle.dump(res, ofile, pickle.HIGHEST_PROTOCOL)


def main(features, split_on, group_name, n_splits):

    # Pull summary table
    db = athena.database.AthenDatabase(cache=True, write=True)
    df = db.summary_table()     

    # Add time features
    athena.learning.add_features(df)

    # Assign columns
    y_cols = ['vehicles']
    num_cols, cat_cols, no_trans_cols = translate_features(features)

    # Create processor for scaling and transforming data
    processor = athena.learning.Processor(num_cols, cat_cols, no_trans_cols)
    processor.fit(df)

    #random.seed(10)
    seed = random.randint(0, 10000)
    # seed = None

    # Create splitter to provide hold out set and CV
    splitter = athena.learning.Splitter(df, split_on, group_name, y_cols, 
                                        num_cols + cat_cols + no_trans_cols,
                                        seed = seed)

    # Split data
    X, y, group = splitter.train_Xygroup
    X_hold, y_hold, group_hold = splitter.test_Xygroup

    # Transform split data
    Xt = processor.transform(X)
    Xt_hold = processor.transform(X_hold)

    # Run the cases
    directory = "results"
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    # general results
    results = {'seed': seed,
                'start_date': df.index.min(), 
                'end_date': df.index.max(),
                'y_cols': y_cols,
                'num_cols': num_cols,
                'cat_cols': cat_cols,
                'n_splits': n_splits,
                'features': features,
                'no_trans_cols': no_trans_cols,
                'group_name': group_name,
                'split_on': split_on }

    filename = "{}:{}:{}:{}.pkl".format(split_on, group_name, n_splits, features)

    # Lasso
    # -------------------------------------------------------------------------
    parameters = [{'alpha': [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10 ]}]

    model = Lasso(max_iter=2500)
    cv = splitter.fold(n_splits=n_splits).split(Xt, y, group)
    evaluate_and_save(model, cv, parameters, directory, filename, Xt, y, Xt_hold, y_hold, results)
   

    # SVR
    # -------------------------------------------------------------------------
    parameters = [{'kernel': ['rbf'], 
                    'gamma': [0.0001, 0.001, 0.01, 0.1, 0.2, 0.5, 0.6, 0.9, 1],
                    'C': [0.01, 0.1, 1, 10, 100, 1000, 10000]},
                    ]
    model = SVR()
    cv = splitter.fold(n_splits=n_splits).split(Xt, y, group)
    evaluate_and_save(model, cv, parameters, directory, filename, Xt, y, Xt_hold, y_hold, results)


    # Boosted trees
    # -------------------------------------------------------------------------
    parameters = [{'n_estimators': [10, 20, 50, 100, 200],
                'max_features': ['auto', 'sqrt'],
                'min_samples_leaf': [10,50,100],
                'bootstrap':  [True, False]},
                ]
                
    model = RandomForestRegressor()
    cv = splitter.fold(n_splits=n_splits).split(Xt, y, group)
    evaluate_and_save(model, cv, parameters, directory, filename, Xt, y, Xt_hold, y_hold, results)


if __name__ == "__main__":

    # get the command line args
    parser = argparse.ArgumentParser(description='Scenario Grid Search for Athena')
    parser.add_argument('--features', help='eg C or CPW or CPWFT', choices=['C', 'CP', 'CPW', 'CPWF', 'CPWFT'])
    parser.add_argument('--split', help='time or group', choices=['time', 'group'])
    parser.add_argument('--group', help='obs, day, week', choices=['obs', 'day', 'week'])
    parser.add_argument('--nsplits', help='integer or None', type=int)
    
    args = parser.parse_args()
    features = args.features
    split_on = args.split
    n_splits = args.nsplits
    group_name = "{}_group".format(args.group)

    # Cross validate
    main(features, split_on, group_name, n_splits)

    
