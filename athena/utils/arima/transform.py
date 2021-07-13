""" Author: Monte Lunacek
    Purpose: Provide a data transformation object that converts a Dataset into the expected
    inputs for the ARIMA family of models.
"""

class DataTransformARIMA(object):
    """
        Class to facilitate mapping a dataset object to ARIMA nput formats

        Inputs:
            target: list of column values to be forecasted.
            dynamic_real: list of real-valued variables to aid in learning.
            dynamic_cat: list of categorical varaibles to use as features.

        methods:
            __call__: generator for cross-validation sets.
    """
    
    def __init__(self, target=[], 
                       dynamic_real=[], 
                       dynamic_cat=[],
                ):
        self._target = target
        self._dynamic_real = dynamic_real
        self._dynamic_cat = dynamic_cat
         
    def __call__(self, dataset):
        df = dataset.df
        df[self._dynamic_cat] = df[self._dynamic_cat].astype(str)
         
        for row in dataset.cv: 
            train_df = df.iloc[row['train_start']:row['train_stop']]
            test_df = df.iloc[row['test_start']:row['test_stop']]
     
            X_train = train_df[self._dynamic_real]
            X_test = test_df[self._dynamic_real]
           
            y_train = train_df[self._target]
            y_test = test_df[self._target]

            train_start = train_df.index[0]
            test_start = test_df.index[0]
            
            yield  train_start, X_train, y_train, test_start, X_test, y_test