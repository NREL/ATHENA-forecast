# Athena forecasting

Analysis code for ATHENA project demand forecasting.  This is one module of the larger [Athena project](athena-mobility.org).

## Authors

- Lunacek, Monte <Monte.Lunacek@nrel.gov>
- Williams, Lindy <Lindy.Williams@nrel.gov>
- Ge, Yanbo <Yanbo.Ge@nrel.gov>
- Ficenec, Karen <Karen.Ficenec@nrel.gov>
- Eash, Matthew <Matthew.Eash@nrel.gov>
- Phillips, Caleb <Caleb.Phillips@nrel.gov>

## Purpose

The primary purpose of the repository is to forecast vehicle demand at the DFW airport and to enable training and testing of a variety of algorithms with a simple and consistent interface.  

The algorithms we focus on are:
1) The traditional machine learning models: Linear Regression, Support Vector Regression, XG Boost.
2) The ARIMA family of timeseries forecasting models (ARIMA, SARIMAX).
3) The GluonTS ecosystem (DeepAR, Simple Neural Networks).

## Environment Installation

You will need to build the conda environment defined in the [environment.yml](environment.yml) file. This can be done with the following command:

                conda env create

This will create the `athena-forecast` environment. Optionally, you may also need to define an environment variables, `ATHENA_DATA_PATH`, where the code will look for a specified filename if the full path is not provided.

Finally, you will need to install the athena module by activating the environment and then running the [setup.py](setup.py) command.

                conda activate athena-forecast
                python setup.py develop

### Installation note for XGBoost

The XGBoost installation may require some platform-dependent instructions.  Please see the [XGBoost documentation](https://xgboost.readthedocs.io/en/latest/build.html) to ensure it is installed correctly.


## Testing

We use a limited set of tests to verify the installation.  Run `pytest -s -v` to test your installation and be patient, the tests, although small and efficient, may take up to a few minutes to complete.

## Getting started

The best way to understand how to use this code is though our [notebook](notebooks) examples and by reading the [test](test) cases.

In general, the preferred way to use this code is with a json configuration as this will allow for the easy definition and execution of thousands of different algorithm combinations, in parallel, while searching for the best prediction.  We review this configuration in the final example [notebook](notebooks) and in the [test_config_interface.py](test/test_config_interface.py) test case, which reads three example configuration files stored in [test/data](test/data).










