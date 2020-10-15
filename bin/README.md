# Scripts

This directory contains scripts used to do the following:
- [database](database): Gathering data and publishing summary tables to the database.
- [correlation](correlation): Shifting the arrival and departure times of the traffic and vehicle data for a better correlation.
- [modeling](modeling): Running parameter scans on *Eagle* to find the best parameters for the various models.

## Database

The [database/dfw_weather.ipynb](database/dfw_weather.ipynb) notebook scrapes DFW weather from wunderground and saves it to the database.

The script [database/pull.py](database/pull.py) pulls the three main tables we use for learning and caches them locally.  This could be combined with another script in the future.

The summary table for DFW learning is created by [database/summary.py](database/summary.py).

## Correlation

The [correlation/correlation.py](correlation/correlation.py) script enumerates various shifts for the arrival and departure times and stores this information in a *csv* file.

You can sort and view the results in the [correlation/results.ipynb](correlation/results.ipynb) notebook.

## Modeling

The [modeling/supervised_machine_learning/create_sbatch.py](modeling/supervised_machine_learning/create_sbatch.py) script create several `*.sbatch` files that can be submitted to the SLURM scheduler on Eagle using the command:

        bash submit.sh

which contains the SLURM command for each created file.  These files use the command line script, 
[modeling/supervised_machine_learning/supervised_machine_learning.py](modeling/supervised_machine_learning/supervised_machine_learning.py).

In order for this script to work, you will need to:
- Be on the `athena` Eagle allocation
- Clone the repo on scratch such that it is available from your home directory:

        $HOME/athena/ATHENA-twin

- Create an `eagle.sh` script that loads the environment.  Here is an example:

        module load conda
        export CONDA_ENVS_PATH=`pwd`
        source activate athena-twin
        module unload conda

        export ATHENA_DATA_PATH=`pwd`/.data
        mkdir -p $ATHENA_DATA_PATH
        export ATHENA_CREDENTIALS_PATH=$HOME/.athena
        mkdir -p $ATHENA_CREDENTIALS_PATH





