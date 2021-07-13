""" Author: Monte Lunacek
    Purpose: Provide a common object for reading csv files, adding time features,
    and creating cross-validation indices.
"""

import os
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .features import add_time_features

def file_exists(filename):
    """ Checks to see if the file exists, and if not, looks in the ATHENA_DATA_PATH."""
    read_filename = filename
    if not os.path.exists(read_filename):
        read_filename = os.path.join(os.environ['ATHENA_DATA_PATH'], filename)
        if not os.path.exists(read_filename):
            raise Exception("Filename does not exists")
    return read_filename

def get_dataset_from_csv(filename, index="timestamp", freq="30min", max_days=None):
    """ Reads the csv file, check the frequency, limit the number of days, and 
        add time-based features.
    """
    read_filename = file_exists(filename)
    df = pd.read_csv(read_filename)
    df = df.rename(columns={index: 'period'})
    df['period'] = pd.to_datetime(df['period'], utc=True)
    df.set_index('period', inplace=True)
    df.sort_index(inplace=True)

    # Check to make sure the freq is correct
    if len(df.resample(freq).count()) != len(df):
        raise Exception("Frequency of time index does not match")

    if max_days is not None:
        rows_in_day = df.resample("24H").count().max().max()
        df = df.tail(int(rows_in_day*max_days)).copy()

    df.index = df.index.tz_localize(None)
    df = add_time_features(df)
    return df

class Dataset(object):
    """
        Class to facilitate managing CSV files for timesereis learning.

        Inputs:
            filename: full path or name of file in the ATHENA_DATA_PATH directory.
            index: the datetime index of the file.
            freq: the sample rate of the data.
            max_days: optional, limit the total number of days used for learning.
            max_training_days: optional, limit the training history.
            predition_length: forecast horizon.  e.g. number of forward observations to estimate.
            test_start_values: a list of datetime values for cross validation.
            test_sequence_length: if greater than one, test_start_values will be moved one observation 
                                  forward at a time until test_sequence_length is reached.

        Attributes:    
            df: Access the the underlying data frame.
            predicted_length: the horizon of the predicted steps.
            freq: time sample of the data.
            rows_per_day: Number of observations (rows) in a day.
            cv: returns a list of index values for cross-validation.
            
        Methods:
            plot_cv: Plots the cross-validation assigned to the Dataset.    

    """
    def __init__(self, filename, 
                    index='index', 
                    freq="30min", 
                    max_days=None, 
                    max_training_days=None,
                    predition_length=1,
                    test_start_values=[],
                    test_sequence_length=1):

        self._filename = filename
        self._freq = freq
        self._df = get_dataset_from_csv(self._filename, index, freq=freq, max_days=max_days)
        self._rows_per_day = self._df.resample("24H").count().max().max()
        self._prediction_length = predition_length
        self._max_training_days = max_training_days
        self._test_start_values = test_start_values
        self._test_sequence_length = test_sequence_length

        self._cv_index = self._test_train_split()
        
    @property
    def df(self):
        return self._df
    
    @property
    def prediction_length(self):
        return self._prediction_length

    @property
    def freq(self):
        return self._freq

    @property
    def rows_per_day(self):
        return self._df.resample("24H").count().max().max()

    @property
    def cv(self):
        return sorted(self._cv_index, key=lambda x: x['train_start'])
    
    def _test_train_split(self):
        """ Creates the cross validation splits"""
        cv_index = []
        for timestamp in self._test_start_values:
            start_index = self._df.index.get_loc(timestamp)
            for step in range(self._test_sequence_length):
                test_start = start_index + step
                test_stop = start_index + step + self._prediction_length
                train_start = 0
                train_stop = test_start 
                if self._max_training_days is not None:
                    train_start = train_stop - self._max_training_days*self.rows_per_day
                
                tmp = {"test_start": test_start,
                       "test_stop": test_stop,
                       "train_start": train_start,
                       "train_stop": train_stop,
                       "train_days": (train_stop-train_start)/self.rows_per_day
                    }
                cv_index.append(tmp)

        return cv_index

    def plot_cv(self, xmin=None, figsize=(12,4), train="grey", test='steelblue'):
        """ Visualize cross validation"""
        f, ax = plt.subplots(figsize=figsize)
        rows = self.cv
        max_length = 0
        max_height = len(rows)

        if xmin is None:
            xmin = 100000000

        for height, row in enumerate(rows):
            xmin = min(xmin, row['train_start'])

            length = (row['train_stop']-row['train_start'])
            max_length = max(max_length, row['train_stop'] )
            rect = patches.Rectangle((row['train_start'], max_height-height-1), length, 0.9, linewidth=0, alpha=0.95, facecolor=train)
            ax.add_patch(rect)

            length = (row['test_stop']-row['test_start'])
            max_length = max(max_length, row['test_stop'] )
            rect = patches.Rectangle((row['test_start'], max_height-height-1), length, 0.9, linewidth=1, alpha=0.95, facecolor=test)
            ax.add_patch(rect)

        ax.set_xlim(xmin, max_length)
        ax.set_ylim(0, max_height)
        sns.despine()
        return ax

    
