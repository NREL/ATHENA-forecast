""" Author: Monte Lunacek
    Purpose: Create a Split method that matches the scikit learn model
"""
import random
import numpy as np


class TimeSeriesSplit:
    """
    Class to interface for the scikit learn version that is specific to
    TimeSeries in Athena

    Attributes:
        split: generator of test and train index values

    Examples
    >>> cv = TimeSeriesSplit(n_splits=10).split(X, y, group)
    
    """

    def __init__(self, train_size=10, test_size=1, n_splits=10, seed=None):
        """
        Args:
            train_size : int, Training size
            test_size : int, Test size 
            n_splits: int, Number of splits to create
            seed: int, Random seed
        """
        self._train_size = train_size
        self._test_size = test_size
        self._n_splits = n_splits
        self._seed = seed
        
    def split(self, X, y=None, group=None):
        # returns a generator with train and test ranges
        number_of_observations = X.shape[0]
        
        index_values = list(range(self._train_size, 
                              number_of_observations-self._test_size-self._train_size))

        # random.seed(self._seed)
        # random.shuffle(index_values)

        for i, index  in enumerate(index_values):
            if self._n_splits is not None:
                if self._n_splits < i:
                    break
            train_range = np.array(range(0+index, self._train_size+index))
            test_range = np.array(range(self._train_size+index, self._train_size+self._test_size+index))
            yield train_range, test_range
        


