# ATHENA-forecast

Database access and analysis code for project ATHENA data.

## Authors

- Lunacek, Monte <Monte.Lunacek@nrel.gov>
- Williams, Lindy <Lindy.Williams@nrel.gov>
- Ge, Yanbo <Yanbo.Ge@nrel.gov>
- Ficenec, Karen <Karen.Ficenec@nrel.gov>
- Eash, Matthew <Matthew.Eash@nrel.gov>
- Phillips, Caleb <Caleb.Phillips@nrel.gov>

## Purpose

There are two primary purposes for this repo:
1) Access to the AWS RDS database
2) Supporting code for analysis

## Environment Installation

You will need to build the conda environment defined in the [environment.yml](environment.yml) file. This can be done with the following command:

                conda env create

This will create the `athena-twin` environment.  You will also need to define two environment variables:

                ATHENA_DATA_PATH
                ATHENA_CREDENTIALS_PATH

The `ATHENA_DATA_PATH` is local directory that will be used to cache data from the database so that the code can be used offline.  The `ATHENA_CREDENTIALS_PATH` is the directory where you store the database credentials json file.  Please email monte.lunacek@nrel.gov for a credentials file.

Finally, you will need to install the athena module by activating the environment and then running the [setup.py](setup.py) command.

                source env.sh
                python setup.py develop

The [env.sh](env.sh) command is for convenience only as it defines the environment variables for the session.  

## Quick start

The two primary purposes of this repository are to provide 1) database access and 2) Analysis support.

### Database Module

The `database` module provides the `AthenaDatabase` class which can be used to access the tables in the AWS RDS database.  It will read your credentials file and connect to the database and provides a few queries that are common.  For example, you can instantiate the class and pass `cache=True` if you do not need to force a new read from the database.  Then you can call select methods to retrieve the data you'd like as a `pandas.DataFrame`.

                db = athena.database.AthenaDatabase(cache=True)
                df = db.summary_table()     


### Examples

The `learning` module provides several helper functions that can be used in the modeling phase. Please see the [examples](examples) directory for use cases.

### Notebooks

The analysis for Athena is located in the [notebooks](notebooks) directory.  This includes:
- Examples using the [Tom Tom](notebooks/tom_tom_api) data API.  Please see the 
[README.md](notebooks/tom_tom_api/README.md) for more information.
- The [exploratory data analysis](notebooks/exploratory) used in predicting vehicle counts.
- A [tubecount](notebooks/tubecount) analysis (see [README.md](notebooks/tubecountREADME.md) for details).
- A [wavelet](notebooks/wavelet) analysis of the traffic data.

### Scripts

We have included a set of scripts that we use for:
- Scanning the traffic and vehicle data for an effective [correlation](bin/correlation).
- Gathering data and publishing summary tables to the database [database](bin/database).
- Scanning the parameters for effective [modeling](bin/modeling).

Please see the [README.md](bin/README.md) for more information.
