""" Author: Monte Lunacek
    Purpose: Provide a data transformation object that converts a Dataset into the expected
    inputs for SkLearn algorithms.
"""

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

import numpy as np

class DataTransformSKLearn(object):

    """
        Class to facilitate mapping a dataset object to SKlearn input formats

        Inputs:
            target: list of column values (1 actually) to be forecasted.
            dynamic_real: list of real-valued variables to aid in learning.
            dynamic_cat: list of categorical varaibles to use as features.

        methods:
            (): generator for cross-validation sets.
    """

    def __init__(self, target=[], 
                       dynamic_real=[], 
                       dynamic_cat=[],
                       scaler_real = MinMaxScaler(),
                       scaler_target = MinMaxScaler(),
                       scaler_cat = OneHotEncoder(categories='auto')
                ):
        self._target = target
        self._dynamic_real = dynamic_real
        self._dynamic_cat = dynamic_cat
        
        self._scaler_target = scaler_target
        self._scaler_real = scaler_real
        self._scaler_cat = scaler_cat
        
        real_transformer = Pipeline(steps=[('scaler', self._scaler_real)])
        cat_transformer = Pipeline(steps=[('onehot', self._scaler_cat)])

        self._preprocessor = ColumnTransformer( transformers=[
                                ('real', real_transformer, self._dynamic_real),
                                ('cat', cat_transformer, self._dynamic_cat),
                                ])
    
        
    def __call__(self, dataset):

        
        df = dataset.df
        df[self._dynamic_cat] = df[self._dynamic_cat].astype(str)
        
        for row in dataset.cv: 
            train_df = df.iloc[row['train_start']:row['train_stop']]
            test_df = df.iloc[row['test_start']:row['test_stop']]

            self._preprocessor.fit(train_df)
            X_train = self._preprocessor.transform(train_df)
            X_test = self._preprocessor.transform(test_df)
            self._scaler_target.fit(train_df[self._target])
            y_train = self._scaler_target.transform(train_df[self._target])
            y_test = self._scaler_target.transform(test_df[self._target])

            train_start = train_df.index[0]
            test_start = test_df.index[0]
            
            yield  train_start, X_train, y_train, test_start, X_test, y_test
        