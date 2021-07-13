import os
import pytest
import athena
import pandas as pd
import glob

import shutil
from gluonts.mx.trainer import Trainer

os.environ['ATHENA_DATA_PATH'] = os.path.join( os.path.dirname(os.path.abspath(__file__)), "data")


def evaluate_model(model, config):
    if os.path.exists("results"):
        shutil.rmtree("results")
    
    dataset = athena.Dataset("dfw_demand.csv.gz", 
                    index="timestamp", 
                    freq="30min",
                    max_training_days=5,
                    predition_length=48,
                    test_start_values=["2019-07-27 00:00:00"],
                    test_sequence_length=1
                    )

    transform = athena.utils.gluonts.DataTransformGluon(['vehicles'])

    athena.utils.gluonts.evaluate_gluonts(dataset, transform, model, config)

    df = pd.read_csv(glob.glob("{}/*.csv".format(config['directory']))[0])
    assert len(df) == 48

def test_deepar():
    from gluonts.model.deepar import DeepAREstimator

    config = {}
    config['directory'] = 'results/deepar'

    model = DeepAREstimator(freq="30min", 
                        prediction_length=48, 
                        trainer=Trainer(epochs=3))

    evaluate_model(model, config)

def test_nn():
    from gluonts.model.simple_feedforward import SimpleFeedForwardEstimator

    config = {}
    config['directory'] = 'results/nn'

    model = SimpleFeedForwardEstimator(freq="30min", 
                                prediction_length=48, 
                                trainer=Trainer(epochs=3))

    evaluate_model(model, config)
  