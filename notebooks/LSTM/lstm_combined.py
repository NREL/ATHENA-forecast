
import os
import argparse
import shutil

import athena
import pandas as pd
import numpy as np

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

from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, RobustScaler


def getX(df, num_cols=[], cat_cols=[]):
    no_trans_cols = []

    one_hot = OneHotEncoder(handle_unknown='ignore')

    cols = []
    for col in cat_cols:
        num_values = len(df[col].drop_duplicates())
        cols.extend([ "{}_{}".format(col, x) for x in range(num_values)])

    cat_X = one_hot.fit_transform(df[cat_cols]).todense()
    cat_df = pd.DataFrame(cat_X)
    cat_df.columns = cols
    cat_df.head()
    cat_df.index = df.index

    num_df = pd.concat([df[num_cols], cat_df], axis=1)

    #, numeric_scaler=RobustScaler()
    processor = athena.learning.Processor(num_cols, [], cols)
    processor.fit(num_df)
    X = processor.transform(num_df)
    return X

# convert an array of values into a dataset matrix
def create_dataset(X_vals, y_vals, look_back=1, look_forward=1):
    num_cols = X_vals.shape[1]
    num_rows = X_vals.shape[0]
    X, y = [], []
    X = []
    y = []
    index = []
         
    for i in range(0, look_back):
        X.append(np.zeros(X_vals[(look_back-look_back):(look_back+look_forward)].shape)) 
        y.append(np.zeros(y_vals[look_back].shape))
    
    for i in range(look_back, num_rows-look_forward):
        index.append(i)
        X.append(X_vals[(i-look_back):(i+look_forward)]) 
        y.append(y_vals[i])

    for i in range(num_rows-look_forward, num_rows):
        X.append(np.zeros(X_vals[(look_back-look_back):(look_back+look_forward)].shape)) 
        y.append(np.zeros(y_vals[look_back].shape))
            
    X = np.array(X)
    y = np.array(y)
    return index, np.reshape(X, (X.shape[0], num_cols, X.shape[1])), np.array(y)

def evaluate(ident, model, X1, X2, y, train_index, test_index):
    train_predict = model.predict([ X1[train_index], X2[train_index] ])
    train_predict = scaler.inverse_transform(train_predict)
    train_y = scaler.inverse_transform(y1[train_index])
    train_rmse = athena.learning.rmse(train_y, train_predict)
    print(train_rmse)

    test_predict = model.predict([ X1[test_index], X2[test_index] ])
    test_predict = scaler.inverse_transform(test_predict)
    test_y = scaler.inverse_transform(y1[test_index])
    test_rmse = athena.learning.rmse(test_y, test_predict)
    print(test_rmse)
    
    print("EVALUATE  {}  @ ({}, {})".format(ident, train_index[0], train_index[-1]), train_rmse, test_rmse)
    




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--forward", "-f", help="set look_forward", default=50)
    parser.add_argument("--back", "-b", help="set look_back", default=50)
    parser.add_argument("--window", "-w", help="set forecast window", default=1)
    parser.add_argument("--trainmax", help="set the max train size", default=48*180)
    args = parser.parse_args()

    FORECAST = args.window
    LOOK_FORWARD = args.forward
    LOOK_BACK = args.back
    MAX_TRAIN_SIZE = args.trainmax

    identifier = "lstm_combined_{0:02d}_{1:02d}_{2:02d}_{3}"
    identifier = identifier.format(FORECAST, LOOK_FORWARD, LOOK_BACK, MAX_TRAIN_SIZE )
    directory = os.path.join("data", identifier)
    if not os.path.exists("data"):
        os.mkdir("data")

    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)

    db = athena.database.AthenaDatabase(cache=True, write=True)
    df = db.summary_table() 

    y_cols = athena.learning.add_features(df, forecast=FORECAST)
    print('Number of rows and columns:', df.shape)

    df['day_group'] = df.index.map(lambda x: x.strftime("%Y-%m-%d"))
    group_values = df['day_group'].values

    scaler = MinMaxScaler(feature_range=(0,1))
    yt = scaler.fit_transform(df[y_cols])
    
    # define the parameters
    Xt1 = getX(df, ['passengers'],  ['hour', 'day', 'month'])
    Xt2 = getX(df, ['vehicles'],    ['hour', 'day', 'month'])

    index1, X1, y1 = create_dataset(Xt1, yt, look_back=10, look_forward=LOOK_FORWARD)
    index2, X2, y2 = create_dataset(Xt2, yt, look_back=LOOK_BACK, look_forward=0)

    # Combine common parts
    index = np.intersect1d(index1, index2)
    X1 = X1[index]
    y1 = y1[index]
    X2 = X2[index]
    y2 = y2[index]
    groups = group_values[index]

    assert np.all(y1 == y2)

    print(X1.shape, y1.shape, X2.shape, y2.shape, len(groups))

    model1 = Sequential()
    model1.add(LSTM(100, input_shape=(X1.shape[1], X1.shape[2])))
    model1.add(Dropout(0.2))
    model1.add(Dense(FORECAST))
    model1.compile(loss='mean_squared_error', optimizer='adam')

    model2 = Sequential()
    model2.add(LSTM(100, input_shape=(X2.shape[1], X2.shape[2])))
    model2.add(Dropout(0.2))
    model2.add(Dense(FORECAST))
    model2.compile(loss='mean_squared_error', optimizer='adam')

    model_concat = concatenate([model1.output, model2.output], axis=-1)
    model_concat = Dense(FORECAST)(model_concat)
    
    # model = Sequential()
	# model.add(Dense(8, input_dim=dim, activation="relu"))
	# model.add(Dense(4, activation="relu"))
    # model.add(Dense(1, activation="linear"))

    model = keras.Model(inputs=[model1.input, model2.input], outputs=model_concat)
    model.compile(loss='mean_squared_error', optimizer='adam')

    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=directory)

    cv = TimeSeriesSplit(n_splits=20, max_train_size=48*180).split(X1, y1, groups)
    for train_index, test_index in cv:
        print(len(train_index),  len(test_index))

        model.fit([X1[train_index], X2[train_index]], 
                    y1[train_index], 
                    batch_size=70, 
                    validation_data=([X1[test_index], X2[test_index]], y1[test_index]),
                    callbacks=[EarlyStopping(monitor='val_loss', patience=10), 
                               tensorboard_callback, ],
                    epochs=20,
                    verbose=True)

        evaluate("COMBINED", model, X1, X2, y1, train_index, test_index)



