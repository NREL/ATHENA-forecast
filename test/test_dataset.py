import os
import pytest
import athena

os.environ['ATHENA_DATA_PATH'] = os.path.join( os.path.dirname(os.path.abspath(__file__)), "data")

def test_ds():

    ds = athena.Dataset("dfw_demand.csv.gz", 
                    index="timestamp", 
                    freq="30min",
                    max_days=500,
                    max_training_days=200,
                    predition_length=1,
                    test_start_values=["2019-07-27 00:00:00"],
                    test_sequence_length=4
                    )

    # Ensure the number of cv: len(test_start_values)*test_sequence_length
    assert len(ds.cv) == 4

    # Assert the max days in the dataset
    assert len(ds.df) == 500*ds.rows_per_day
    
    # verify each cv has a max of 200 training days
    for test in ds.cv:
        assert (test['train_stop'] - test['train_start'])/ds.rows_per_day <= 200






