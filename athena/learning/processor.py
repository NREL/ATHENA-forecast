""" Author: Monte Lunacek
    Purpose: Wrap the data processing tasks into class
"""
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, OneHotEncoder

from sklearn.impute import SimpleImputer

class Processor:
    """
    Class to process Athena features.

    Attributes:
        fit: Fit the data to the specified transformation
        transform: Transform other data to previously fit model
        column_description: One-hot encoded descriptions
    
    """
    def __init__(self, numeric_columns, 
                       categorical_columns, 
                       no_tranform_columns=[],
                       numeric_scaler=MinMaxScaler(feature_range=(0,1))):
        """
        Args:
            numeric_columns : list, The columns processed as numeric data
            categorical_columns : list, The columns processed as categorical, one-hot data
            no_tranform_columns: list, do not transform
        """

        self._num_cols = numeric_columns
        self._cat_cols = categorical_columns
        self._no_transform = no_tranform_columns
        
        numeric_transformer = Pipeline(steps=[('scaler', numeric_scaler)])
        categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])
        no_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value=None))])

        self._preprocessor = ColumnTransformer( transformers=[
                                ('shifted', numeric_transformer, self._num_cols),
                                ('time_cols', categorical_transformer, self._cat_cols),
                                ('no_trans_cols', no_transformer, self._no_transform),
                                ])
        
    def fit(self, X):
        self._preprocessor.fit(X[self._num_cols + self._cat_cols + self._no_transform])
        self._cols = [ x for x in self._num_cols ] +  [ x for x in self._no_transform ] 
        for col in self._cat_cols:
            num_values = len(X[col].drop_duplicates())
            self._cols.extend([ "{}_{}".format(col, x) for x in range(num_values)])

    def transform(self, X):
        return self._preprocessor.transform(X[self._num_cols + self._cat_cols + self._no_transform])

    @property
    def column_description(self):
        return self._cols