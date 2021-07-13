""" Author: Monte Lunacek
    Purpose: functions for storing results.
"""

import os
import shutil
import json
import uuid

def ensure_directory(directory):
    """ Ensure the directory exists. """
    if directory is not None:
        if not os.path.exists(os.path.split(directory)[0]):
            os.mkdir(os.path.split(directory)[0])
        if not os.path.exists(directory):
            os.mkdir(directory)

def get_uuid():
    """ Provide a unique identifier for saving the json and csv files"""
    trial = "trial-{}".format(str(uuid.uuid1()))
    return trial

def save_partial(config, results_list):
    """saves the config and results_list to file"""
    trial = config.get('uuid')   
    directory = config.get('directory')
    tmp = config.copy()
    tmp['rmse'] = results_list
    with open("{}/results_{}.json".format(directory, trial), "w") as outfile:
        outfile.write(json.dumps(tmp))

def save_results(config, df, rmse):
    """ Saves the df to a csv and the config and rmse to json."""
    trial = config.get('uuid')   
    directory = config.get('directory')

    if directory is not None:
        if df is not None:
            df.to_csv("{}/results_{}.csv".format(directory, trial))
        tmp = config.copy()
        tmp['rmse'] = rmse

        with open("{}/results_{}.json".format(directory, trial), "w") as outfile:
            outfile.write(json.dumps(tmp))
