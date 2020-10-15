from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, RobustScaler
import numpy as np
import pandas as pd
import athena
import os
import uuid
import json
import shutil

def get_directory(config_filename):

    dir_name = os.path.basename(config_filename).replace(".json", "")
    directory = os.path.join("data", dir_name)
    if not os.path.exists("data"):
        os.mkdir("data")
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)

    config = json.loads(open(config_filename).read())

    with open(os.path.join(directory, "config.json"), "w") as outfile:
        outfile.write(json.dumps(config))

    print("tensorboard --logdir {}".format(directory))
    return directory, config


def getX(df, num_cols=[], cat_cols=[], no_trans_cols = []):
    
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
    num_df = pd.concat([df[num_cols+no_trans_cols], cat_df], axis=1)

    #numeric_scaler=RobustScaler()
    processor = athena.learning.Processor(num_cols, [], cols+no_trans_cols)
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

def data_intersection(index1, X1, y1, index2, X2, y2, group_values=None):
    index = np.intersect1d(index1, index2)
    X1 = X1[index]
    y1 = y1[index]
    X2 = X2[index]
    y2 = y2[index]
    assert np.all(y1 == y2)
    groups = None
    if group_values is not None:
        groups = group_values[index]
    return X1, y1, X2, y2, groups

def data_intersection_single(index, X, y, group_values=None):
    X = X[index]
    y = y[index]
    groups = None
    if group_values is not None:
        groups = group_values[index]
    return X, y, groups

def evaluate_single_model(model, scaler, X, y, train_index, test_index):
    train_predict = model.predict(X[train_index])
    train_predict = scaler.inverse_transform(train_predict)
    y_train = scaler.inverse_transform(y[train_index])
    train_rmse = athena.learning.rmse(y_train, train_predict)

    test_predict = model.predict(X[test_index])
    test_predict = scaler.inverse_transform(test_predict)
    y_test = scaler.inverse_transform(y[test_index])
    test_rmse = athena.learning.rmse(y_test, test_predict)

    return train_rmse, test_rmse

def evaluate_combined_model(model, scaler, X1, y1, X2, y2, train_index, test_index):
    train_predict = model.predict([ X1[train_index], X2[train_index] ])
    train_predict = scaler.inverse_transform(train_predict)
    train_y = scaler.inverse_transform(y1[train_index])
    train_rmse = athena.learning.rmse(train_y, train_predict)
    
    test_predict = model.predict([ X1[test_index], X2[test_index] ])
    test_predict = scaler.inverse_transform(test_predict)
    test_y = scaler.inverse_transform(y1[test_index])
    test_rmse = athena.learning.rmse(test_y, test_predict)

    return train_rmse, test_rmse