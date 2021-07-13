import json
import os
import athena

def test_config_interface_linear():
    os.environ['ATHENA_DATA_PATH'] = os.path.join( os.path.dirname(os.path.abspath(__file__)), "data")
    config = json.loads(open(os.path.join(os.environ['ATHENA_DATA_PATH'], "config_linear.json")).read())
    athena.evaluate(config)

