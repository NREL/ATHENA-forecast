""" Author: Monte Lunacek
    Purpose: Provide a data transformation object that converts a Dataset into the expected
    inputs for GluonTS algorithms.
"""

from gluonts.dataset.common import ListDataset
import pandas as pd
import numpy as np
       
class DataTransformGluon(object):
    
    def __init__(self, target=[], 
                       dynamic_real=[], 
                       dynamic_cat=[]
                ):
        self._target = target
        self._dynamic_real = dynamic_real
        self._dynamic_cat = dynamic_cat
        
        
    def __call__(self, dataset, prediction_window=48):
        
        df = dataset.df
        def create_train_list(df, row):
            start_index = int(row['train_start'])
            stop_index = int(row['train_stop'])

            res = {"start": str(df.index[start_index]), 
                    "target": df.iloc[start_index:stop_index][self._target[0]].values,
                    "feat_dynamic_real": [ df.iloc[start_index:stop_index][col].values for col in self._dynamic_real],
                    "feat_dynamic_cat": [ df.iloc[start_index:stop_index][col].values for col in self._dynamic_cat],
                   }

            if len(res['feat_dynamic_real']) == 0:
                del res['feat_dynamic_real']

            if len(res['feat_dynamic_cat']) == 0:
                del res['feat_dynamic_cat']

            return res


        def create_test_list(df, row, period=48, step=0):
            start_index = row['train_start']
            stop_index = row['train_stop'] + step + period

            res = {"start": str(df.index[start_index]), 
                    "target": df.iloc[start_index:stop_index][self._target[0]].values,
                    "feat_dynamic_real": [ df.iloc[start_index:stop_index][col].values for col in self._dynamic_real],
                    "feat_dynamic_cat": [ df.iloc[start_index:stop_index][col].values for col in self._dynamic_cat],
                   }
                   
            if len(res['feat_dynamic_real']) == 0:
                del res['feat_dynamic_real']

            if len(res['feat_dynamic_cat']) == 0:
                del res['feat_dynamic_cat']

            return res

        for row in dataset.cv:
            train_dataset = ListDataset(
                [ create_train_list(df, row)],
                 freq=dataset.freq
            )

       
            test_dataset = ListDataset(
                [ create_test_list(df, row, period=prediction_window) ],
                 freq=dataset.freq
            )

            yield  {'train': train_dataset, 'test': test_dataset}