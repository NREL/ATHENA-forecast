import os
import sys
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import GRU as LSTM
from keras.layers import Dropout
from keras.layers import *
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from keras.callbacks import EarlyStopping

import athena
import utils

if __name__ == "__main__":

    config_filename = sys.argv[1]
    directory, config = utils.get_directory(config_filename)

    db = athena.database.AthenaDatabase(cache=True, write=True)
    df = db.summary_table() 

    y_cols = athena.learning.add_features(df, forecast=config['forecast'])
    print('Number of rows and columns:', df.shape)

    group_values = df[config['group']].values

    scaler = MinMaxScaler(feature_range=(0,1))
    yt = scaler.fit_transform(df[y_cols])

    Xt = utils.getX(df, ['passengers'], [], ['time_minutes_sin', 'time_minutes_cos', 
                                        'hour_sin', 'hour_cos', 
                                        'month_sin', 'month_cos'])

    index, X, y = utils.create_dataset(Xt, yt, look_back=config['look_back'], look_forward=config['look_forward'])

    X, y, groups = utils.data_intersection_single(index, X, y, group_values)
    print(X.shape, y.shape)

    cv = TimeSeriesSplit(n_splits=config['n_splits'], max_train_size=config['max_train_size']).split(X, y, groups)

    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=directory)

    model = Sequential()
    model.add(LSTM(config['lstm_levels'], input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(config['dropout']))
    model.add(Dense(config['forecast']))
    model.compile(loss='mean_squared_error', optimizer='adam')

    with open(os.path.join(directory, "output.csv"), "w") as outfile:
        for i, (train_index, test_index) in enumerate(cv):
            history = model.fit(X[train_index], 
                                y[train_index], 
                                epochs=config['epochs'], 
                                batch_size=70, 
                                validation_data=(X[test_index], y[test_index]), 
                                callbacks=[EarlyStopping(monitor='val_loss', patience=10), 
                                        tensorboard_callback,], 
                                verbose=1, 
                                shuffle=False)
            model.summary()
            train, test = utils.evaluate_single_model(model, scaler, X, y, train_index, test_index)
            outfile.write("{},{},{},{}\n".format(i, train, test, directory))
            outfile.flush()
        
