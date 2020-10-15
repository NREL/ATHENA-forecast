""" Author: Monte Lunacek
    Purpose: Class to handle the different groups (obs, day, week) and the different ways
    to cross-validate (split on time or on group)
"""

from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import GroupKFold

from . fold import TimeSeriesSplit

class Splitter(object):
    """
    Class for handling cross-validation 

    Attributes
        train_Xygroup: returns the X, y, ang group arrays for the training set
        test_Xygroup: returns the X, y, ang group arrays for the test set
        fold: generator, returns either the TimeSeriesSplit or the GroupKFold
  
    Examples
    >>> splitter = athena.learning.Splitter(df, "time", "day_group", ["vehicles"], 
                                    ["passengers"])

    >>> X, y, group = splitter.train_Xygroup
    >>> X_hold, y_hold, group_hold = splitter.test_Xygroup
    >>> cv = splitter.fold(n_splits=10).split(X, y, group)

    """

    def __init__(self, df, split_on, group_col, y_cols, x_cols, test_size=0.05, seed=None):
        """
        Args:
            df : DataFrame, The dataframe to be split
            split_on : String, 'time' or 'group'
            group_col: String, 'obs_group', 'day_group', or 'week_group'
            y_cols : list, The y column(s)
            x_cols : list, The X column(s)
            test_size : float, Size of test group used for hold out set
            seed: int, Random seed
        """
        self._test_size = test_size
        self._seed = seed
        self._group_col = group_col
        self._split_on = split_on
        self._y_cols = y_cols
        self._x_cols = x_cols
        
        self._df = df.copy()
        # Add some groups
        self._df['obs_group'] = self._df.index.map(lambda x: x.strftime("%Y-%m-%d-%H-%M"))
        self._df['day_group'] = self._df.index.map(lambda x: x.strftime("%Y-%m-%d"))
        self._df['week_group'] = self._df.index.map(lambda x: x.strftime("%Y-%W"))

        assert self._split_on in ['time', 'group']
        assert self._group_col in ['obs_group', 'day_group', 'week_group']
        
        self._create_split()
        
    def _create_split(self):
        y = self._df[self._y_cols].values
        X = self._df[self._x_cols].values
        if self._split_on == "group":
            group_values = self._df[self._group_col].values

            gss = GroupShuffleSplit(test_size=self._test_size, random_state=self._seed)
            gen = gss.split(X, y, group_values)

            self._train_inds, self._test_inds = next(gen)
        elif self._split_on == "time":
            index_range = list(range(len(self._df)))
            last_index = int(index_range[-1]*self._test_size)

            self._train_inds = index_range[:-last_index]
            self._test_inds = index_range[-last_index:]

    @property
    def test_df(self):
        return self._df.reset_index().loc[self._test_inds]

    @property
    def train_df(self):
        return self._df.reset_index().loc[self._train_inds] 
    
    def _split(self, df):
        y = df[self._y_cols]
        X = df[self._x_cols]
        if self._split_on == "group":
            group = df[self._group_col]
        elif self._split_on == "time":
            group = None
        return X, y, group
    
    @property
    def train_Xygroup(self):
        df_train = self.train_df
        return self._split(df_train)
    
    @property
    def test_Xygroup(self):
        df_test = self.test_df
        return self._split(df_test)

    def fold(self, n_splits=10, train_size=48*180):
        if self._split_on == "time":
            test_sizes = {'week_group': 48*7,
                          'day_group': 48,
                          'obs_group': 1}
            test_size = test_sizes.get(self._group_col, 1)
            return TimeSeriesSplit(n_splits=n_splits, seed=self._seed, train_size=train_size, test_size=test_size)
        elif self._split_on == "group":
            return GroupKFold(n_splits=n_splits)
